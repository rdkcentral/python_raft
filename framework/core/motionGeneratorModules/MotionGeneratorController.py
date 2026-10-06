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

from .virtualMotionGenerator import virtualMotionGenerator
from .actualMotionGenerator import actualMotionGenerator


class MotionGeneratorController:
    """
    Factory wrapper that selects the appropriate MotionGenerator controller
    implementation based on the platform.

    For 'vDevice' platform, the virtualMotionGenerator is used (curl-based
    control plane). For all other platforms the actualMotionGenerator stub is used.
    """

    def __new__(cls, platform: str, session, prompt: str = "~#", port: int = 8080):
        """
        Creates and returns the appropriate controller instance.

        Args:
            platform (str): Platform identifier, e.g. "vDevice".
            session: Console/SSH session with a write() method.
            prompt (str): Shell prompt string.
            port (int): Control-plane HTTP port (used for vDevice).

        Returns:
            MotionGeneratorControllerInterface: Controller instance.
        """
        if platform == "vDevice":
            return virtualMotionGenerator(session, prompt, port)
        return actualMotionGenerator(session, prompt, port)
