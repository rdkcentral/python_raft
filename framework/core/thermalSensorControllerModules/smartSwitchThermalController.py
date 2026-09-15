#!/usr/bin/env python3
#** *****************************************************************************
# *
# * Copyright 2026 RDK Management
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# * http://www.apache.org/licenses/LICENSE-2.0
# *
#* ******************************************************************************

import time

from framework.core.logModule import logModule
from framework.core.powerControl import powerControlClass
from framework.core.thermalSensorControllerModules.ThermalSensorControllerInterface import ThermalSensorControllerInterface


class smartSwitchThermalController(ThermalSensorControllerInterface):
    """
    Thermal controller that drives a heater or blower through the existing RAFT
    power-switch abstractions.

    Required config keys:
      type: smartswitch_thermalcontroller
      power_switch_type: kasa | tapo | hs100 | apc | apcAos | olimex | SLP
      ip: IP address of the smart switch

    Optional config keys are passed through to powerControlClass, for example:
      port, username, password, outlet, outlet_id, args, options, retryCount,
      retryDelay

    Thermal-specific optional keys:
      heating_duration_seconds: wait time after turning the blower on
      cooling_duration_seconds: wait time after turning the blower off
      heat_on_temperature_celsius: threshold used by injectTemperatureUpdate
      minimum_heating_duration_seconds: default timed heating pulse for a
          temperature update that should raise the temperature
      seconds_per_degree_celsius: extra heat-on time added for each degree
          above heat_on_temperature_celsius
      maximum_heating_duration_seconds: cap for timed heat pulses
      temperature_duration_map_seconds: optional mapping of target
          temperature to exact heat-on duration, for example
          {90: 300, 100: 600, 110: 900}
    """

    HEATING_STATES = {
        "CRITICAL_TEMPERATURE_EXCEEDED",
        "CRITICAL_SHUTDOWN_IMMINENT",
    }

    NORMAL_STATES = {
        "NORMAL",
        "CRITICAL_TEMPERATURE_RECOVERED",
    }

    DEFAULT_HEAT_ON_TEMPERATURE_CELSIUS = 90.0
    DEFAULT_MINIMUM_HEATING_DURATION_SECONDS = 300
    DEFAULT_SECONDS_PER_DEGREE_CELSIUS = 30
    DEFAULT_MAXIMUM_HEATING_DURATION_SECONDS = 1800
    DEFAULT_COOLING_DURATION_SECONDS = 15
    DEFAULT_TEMPERATURE_DURATION_MAP_SECONDS = {
        90.0: 300.0,
        100.0: 600.0,
        110.0: 900.0,
    }

    def __init__(self, session, prompt: str = "~#", port: int = 8080, config: dict = None):
        super().__init__(session, prompt, port)
        self.config = dict(config or {})
        self._log = logModule(self.__class__.__name__)
        self._log.setLevel(self._log.INFO)
        self.heatingDurationSeconds = float(self.config.get("heating_duration_seconds", 0))
        self.coolingDurationSeconds = float(
            self.config.get("cooling_duration_seconds", self.DEFAULT_COOLING_DURATION_SECONDS)
        )
        self.heatOnTemperatureCelsius = float(
            self.config.get("heat_on_temperature_celsius", self.DEFAULT_HEAT_ON_TEMPERATURE_CELSIUS)
        )
        self.minimumHeatingDurationSeconds = float(
            self.config.get(
                "minimum_heating_duration_seconds",
                self.DEFAULT_MINIMUM_HEATING_DURATION_SECONDS,
            )
        )
        self.secondsPerDegreeCelsius = float(
            self.config.get(
                "seconds_per_degree_celsius",
                self.DEFAULT_SECONDS_PER_DEGREE_CELSIUS,
            )
        )
        self.maximumHeatingDurationSeconds = float(
            self.config.get(
                "maximum_heating_duration_seconds",
                self.DEFAULT_MAXIMUM_HEATING_DURATION_SECONDS,
            )
        )
        self.temperatureDurationMapSeconds = self._parseTemperatureDurationMap(
            self.config.get(
                "temperature_duration_map_seconds",
                dict(self.DEFAULT_TEMPERATURE_DURATION_MAP_SECONDS),
            )
        )
        self.powerController = powerControlClass(self._log, self._buildPowerSwitchConfig())

    def _parseTemperatureDurationMap(self, durationMapConfig) -> list:
        if not isinstance(durationMapConfig, dict):
            return []

        parsedDurationMap = []
        for temperatureKey, durationValue in durationMapConfig.items():
            parsedDurationMap.append((float(temperatureKey), float(durationValue)))
        parsedDurationMap.sort(key=lambda item: item[0])
        return parsedDurationMap

    def _buildPowerSwitchConfig(self) -> dict:
        powerConfig = dict(self.config)
        powerSwitchType = (
            powerConfig.get("power_switch_type")
            or powerConfig.get("switch_type")
            or powerConfig.get("vendor")
        )
        if powerSwitchType is None:
            raise ValueError("smartswitch_thermalcontroller requires power_switch_type in rack config")

        powerConfig["type"] = powerSwitchType
        powerConfig.setdefault("name", "thermal-heater")
        return powerConfig

    def _waitAfterToggle(self, enabled: bool) -> None:
        delay = self.heatingDurationSeconds if enabled else self.coolingDurationSeconds
        if delay > 0:
            time.sleep(delay)

    def _setHeaterState(self, enabled: bool, reason: str) -> bool:
        self._log.info("[%s] turning heater %s", reason, "ON" if enabled else "OFF")
        result = self.powerController.powerOn() if enabled else self.powerController.powerOff()
        self._waitAfterToggle(enabled)
        return result

    def _getHeatingDurationSeconds(self, temperatureCelsius: float) -> float:
        requestedTemperature = float(temperatureCelsius)
        if self.temperatureDurationMapSeconds:
            for mappedTemperature, mappedDuration in self.temperatureDurationMapSeconds:
                if requestedTemperature <= mappedTemperature:
                    return mappedDuration
            return self.temperatureDurationMapSeconds[-1][1]

        deltaCelsius = max(0.0, float(temperatureCelsius) - self.heatOnTemperatureCelsius)
        durationSeconds = (
            self.minimumHeatingDurationSeconds +
            (deltaCelsius * self.secondsPerDegreeCelsius)
        )
        return min(durationSeconds, self.maximumHeatingDurationSeconds)

    def _runHeatingPulse(self, durationSeconds: float, reason: str) -> bool:
        if durationSeconds <= 0:
            return self._setHeaterState(False, reason)

        if not self.powerController.powerOn():
            return False

        self._log.info("[%s] keeping heater ON for %.1f seconds", reason, durationSeconds)
        time.sleep(durationSeconds)
        return self._setHeaterState(False, f"{reason}:complete")

    def triggerThermalStateChange(self, state: str, sensorName: str = "",
                                  temperatureCelsius: float = 0.0,
                                  timestampMonotonicMs: int = 0):
        del sensorName, temperatureCelsius, timestampMonotonicMs
        normalizedState = str(state or "").strip().upper()
        if normalizedState in self.HEATING_STATES:
            return self._setHeaterState(True, normalizedState)
        if normalizedState in self.NORMAL_STATES:
            return self._setHeaterState(False, normalizedState)

        self._log.warning("Unknown thermal state '%s'. Leaving heater state unchanged.", state)
        return True

    def injectTemperatureUpdate(self, sensorName: str, temperatureCelsius: float,
                                timestampMonotonicMs: int = 0):
        del sensorName, timestampMonotonicMs
        requestedTemperature = float(temperatureCelsius)
        if requestedTemperature < self.heatOnTemperatureCelsius:
            return self._setHeaterState(False, f"temperature_update:{requestedTemperature}")

        heatingDurationSeconds = self._getHeatingDurationSeconds(requestedTemperature)
        return self._runHeatingPulse(
            heatingDurationSeconds,
            f"temperature_update:{requestedTemperature}",
        )