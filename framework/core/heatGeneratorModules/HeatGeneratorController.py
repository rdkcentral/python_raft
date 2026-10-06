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

from .virtualHeatGenerator import virtualHeatGenerator
from .actualHeatGenerator import actualHeatGenerator


class HeatGeneratorController:
    """
    Factory class — returns the correct controller implementation based on platform.
    """

    def __new__(cls, platform: str, session, prompt: str = "~#", port: int = 8080):
        """
        Create and return the appropriate thermal sensor controller.

        Args:
            platform (str): Platform type.  "vDevice" returns a virtualHeatGenerator.
                            Any other value returns an actualHeatGenerator.
            session: Active pexpect / raft session on the target device.
            prompt (str): Shell prompt string used to detect command completion.
            port (int): Control-plane HTTP port the vcomponent is listening on.

        Returns:
            HeatGeneratorControllerInterface implementation.
        """
        if platform.lower() == "vdevice":
            return virtualHeatGenerator(session, prompt, port)
        return actualHeatGenerator(session, prompt, port)
