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

from raft.framework.plugins.ut_raft.utUserResponse import utUserResponse

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)


from .HeatGeneratorControllerInterface import HeatGeneratorControllerInterface


class actualHeatGenerator(HeatGeneratorControllerInterface):
    """
    Actual (hardware) Thermal Sensor controller.
    On real hardware, thermal events are raised by platform firmware so they
    cannot be injected programmatically.  Each method prompts the test operator
    to manually trigger the required thermal condition and confirm the result.
    """

    def __init__(self, session, prompt: str = "~#", port: int = 8080):
        super().__init__(session, prompt, port)
        self.testUserResponse = utUserResponse(session, prompt)

    def injectTemperatureUpdate(self, sensorName: str, temperatureCelsius: float,
                                timestampMonotonicMs: int = 0):
        """
        Prompt the operator to manually set the temperature on real hardware.

        Args:
            sensorName (str): Name of the sensor to adjust.
            temperatureCelsius (float): Target temperature in degrees Celsius.
            timestampMonotonicMs (int): Unused on real hardware.

        Returns:
            bool: True if the operator confirmed the temperature was reached.
        """
        return self.testUserResponse.getUserYN(
            f"Set sensor '{sensorName}' to {temperatureCelsius} Celsius on the hardware. "
            f"Has the temperature been reached? (Y/N):"
        )
