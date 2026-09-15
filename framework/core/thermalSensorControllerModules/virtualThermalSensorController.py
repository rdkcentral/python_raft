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

import yaml

from framework.core.thermalSensorControllerModules.ThermalSensorControllerInterface import ThermalSensorControllerInterface


class virtualThermalSensorController(ThermalSensorControllerInterface):
    """
    Virtual ThermalSensor controller that sends YAML commands to the vcomponent
    control-plane endpoint to simulate thermal events.
    """

    def _sendCommand(self, payload: dict):
        yaml_str = yaml.dump(payload)
        yaml_str = yaml_str.replace('"', '\\"')
        cmd = (
            f'curl -X POST -H "Content-Type: application/x-yaml" '
            f'--data-binary "{yaml_str}" '
            f'"http://localhost:{self.port}/api/postKVP"'
        )
        self.session.write(cmd)

    def triggerThermalStateChange(self, state: str, sensorName: str = "",
                                  temperatureCelsius: float = 0.0,
                                  timestampMonotonicMs: int = 0):
        if timestampMonotonicMs == 0:
            timestampMonotonicMs = int(time.time() * 1000)

        payload = {
            "IThermalSensor": {
                "command": "thermal_state_change",
                "state": state,
                "timestampMonotonicMs": timestampMonotonicMs,
            }
        }

        if sensorName:
            payload["IThermalSensor"]["sensorName"] = sensorName
            payload["IThermalSensor"]["temperatureCelsius"] = temperatureCelsius

        self._sendCommand(payload)

    def injectTemperatureUpdate(self, sensorName: str, temperatureCelsius: float,
                                timestampMonotonicMs: int = 0):
        if timestampMonotonicMs == 0:
            timestampMonotonicMs = int(time.time() * 1000)

        payload = {
            "IThermalSensor": {
                "command": "temperature_update",
                "sensorName": sensorName,
                "temperatureCelsius": temperatureCelsius,
                "timestampMonotonicMs": timestampMonotonicMs,
            }
        }

        self._sendCommand(payload)
