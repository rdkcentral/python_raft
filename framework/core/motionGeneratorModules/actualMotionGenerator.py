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

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

from .MotionGeneratorControllerInterface import MotionGeneratorControllerInterface


class actualMotionGenerator(MotionGeneratorControllerInterface):
    """
    Actual hardware MotionSensor controller stub.
    Implement methods here to trigger events on real hardware (e.g. via GPIO,
    hardware test fixture, or remote API).
    """

    def __init__(self, session, prompt: str = "~#", port: int = 8080):
        super().__init__(session, prompt, port)

    def triggerMotionEvent(self, sensorId: int):
        """Trigger a real MOTION event — not yet implemented."""
        raise NotImplementedError("actualMotionGenerator.triggerMotionEvent not implemented")

    def triggerNoMotionEvent(self, sensorId: int):
        """Trigger a real NO_MOTION event — not yet implemented."""
        raise NotImplementedError("actualMotionGenerator.triggerNoMotionEvent not implemented")
