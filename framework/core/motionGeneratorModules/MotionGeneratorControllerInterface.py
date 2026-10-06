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


class MotionGeneratorControllerInterface(metaclass=ABCMeta):
    """
    Abstract base class for MotionSensor controller implementations.
    Both virtual (vDevice) and actual hardware implementations must inherit this.
    """

    def __init__(self, session, prompt: str = "~#", port: int = 8080):
        self.session = session
        self.prompt = prompt
        self.port = port

    @abstractmethod
    def triggerMotionEvent(self, sensorId: int):
        """
        Simulate a MOTION event for the given sensor.

        Args:
            sensorId (int): ID of the sensor to trigger.
        """
        pass

    @abstractmethod
    def triggerNoMotionEvent(self, sensorId: int):
        """
        Simulate a NO_MOTION event for the given sensor.

        Args:
            sensorId (int): ID of the sensor to trigger.
        """
        pass
