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


class ThermalSensorControllerInterface(metaclass=ABCMeta):
    """
    Abstract base class for ThermalSensor controller implementations.
    Both virtual (vDevice) and actual hardware implementations must inherit this.
    """

    def __init__(self, session, prompt: str = "~#", port: int = 8080):
        self.session = session
        self.prompt = prompt
        self.port = port

    @abstractmethod
    def triggerThermalStateChange(self, state: str, sensorName: str = "",
                                  temperatureCelsius: float = 0.0,
                                  timestampMonotonicMs: int = 0):
        pass

    @abstractmethod
    def injectTemperatureUpdate(self, sensorName: str, temperatureCelsius: float,
                                timestampMonotonicMs: int = 0):
        pass
