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

from raft.framework.plugins.ut_raft.utUserResponse import utUserResponse

from framework.core.thermalSensorControllerModules.ThermalSensorControllerInterface import ThermalSensorControllerInterface


class actualThermalSensorController(ThermalSensorControllerInterface):
    """
    Actual (hardware) Thermal Sensor controller.
    On real hardware, thermal events are raised by platform firmware so they
    cannot be injected programmatically. Each method prompts the test operator
    to manually trigger the required thermal condition and confirm the result.
    """

    def __init__(self, session, prompt: str = "~#", port: int = 8080):
        super().__init__(session, prompt, port)
        self.testUserResponse = utUserResponse(session, prompt)

    def triggerThermalStateChange(self, state: str, sensorName: str = "",
                                  temperatureCelsius: float = 0.0,
                                  timestampMonotonicMs: int = 0):
        msg = f"Manually trigger thermal state '{state}'"
        if sensorName:
            msg += f" on sensor '{sensorName}' at {temperatureCelsius} degC"
        msg += ". Has the device reached the expected state? (Y/N):"
        return self.testUserResponse.getUserYN(msg)

    def injectTemperatureUpdate(self, sensorName: str, temperatureCelsius: float,
                                timestampMonotonicMs: int = 0):
        return self.testUserResponse.getUserYN(
            f"Set sensor '{sensorName}' to {temperatureCelsius} Celsius on the hardware. "
            f"Has the temperature been reached? (Y/N):"
        )
