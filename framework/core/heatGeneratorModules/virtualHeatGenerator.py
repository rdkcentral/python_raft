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

import os
import sys
import time
import yaml

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
sys.path.append(os.path.join(dir_path, "../"))

from .HeatGeneratorControllerInterface import HeatGeneratorControllerInterface


class virtualHeatGenerator(HeatGeneratorControllerInterface):
    """
    Virtual HeatGenerator controller that sends YAML commands to the vcomponent
    control-plane endpoint via utPlaneController to simulate thermal events.
    """

    def __init__(self, session, prompt: str = "~#", port: int = 8080):
        super().__init__(session, prompt, port)

    def _sendCommand(self, payload: dict):
        """
        Serialises *payload* as YAML and POSTs it inline to the vcomponent
        control-plane, matching the deepsleep virtual-controller pattern.

        Args:
            payload (dict): Command payload to serialise and POST.
        """
        yaml_str = yaml.dump(payload)
        yaml_str = yaml_str.replace('"', '\\"')
        cmd = (
            f'curl -X POST -H "Content-Type: application/x-yaml" '
            f'--data-binary "{yaml_str}" '
            f'"http://localhost:{self.port}/api/postKVP"'
        )
        self.session.write(cmd)

    def injectTemperatureUpdate(self, sensorName: str, temperatureCelsius: float,
                                timestampMonotonicMs: int = 0):
        """
        Inject a raw temperature reading into the vcomponent.

        Sends a temperature_update command to the vcomponent control-plane.
        The vcomponent evaluates the value against the configured operational
        thresholds and automatically fires the appropriate state-change event:

          temp >= shutdown_threshold             → CRITICAL_SHUTDOWN_IMMINENT
          temp >  max  ||  temp < min            → CRITICAL_TEMPERATURE_EXCEEDED
          temp <= recovered (from EXCEEDED)      → CRITICAL_TEMPERATURE_RECOVERED
          temp in safe range (from RECOVERED)    → NORMAL

        Args:
            sensorName (str): Name of the sensor reporting the temperature.
            temperatureCelsius (float): Current temperature in degrees Celsius.
            timestampMonotonicMs (int): Monotonic timestamp (ms); 0 uses wall-clock ms.
        """
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
