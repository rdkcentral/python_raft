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

from abc import ABCMeta, abstractmethod


class HeatGeneratorControllerInterface(metaclass=ABCMeta):
    """
    Abstract base class for ThermalSensor controller implementations.
    Both virtual (vDevice) and actual hardware implementations must inherit this.
    """

    def __init__(self, session, prompt: str = "~#", port: int = 8080):
        self.session = session
        self.prompt = prompt
        self.port = port

    @abstractmethod
    def injectTemperatureUpdate(self, sensorName: str, temperatureCelsius: float,
                                timestampMonotonicMs: int = 0):
        """
        Inject a raw temperature reading into the vcomponent.

        The vcomponent evaluates the value against the configured operational
        thresholds (operational_temperature_celsius.min / max / shutdown_threshold)
        and automatically fires the appropriate state-change event:

          temp > shutdown_threshold              → CRITICAL_SHUTDOWN_IMMINENT
          temp > max  ||  temp < min             → CRITICAL_TEMPERATURE_EXCEEDED
          temp in [min, max]  after EXCEEDED     → CRITICAL_TEMPERATURE_RECOVERED
          temp in [min, max]  after RECOVERED    → NORMAL

        Args:
            sensorName (str): Name of the sensor reporting the temperature.
            temperatureCelsius (float): Current temperature in degrees Celsius.
            timestampMonotonicMs (int): Optional monotonic timestamp (ms).
        """
        pass
