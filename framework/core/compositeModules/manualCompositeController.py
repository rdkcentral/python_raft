#!/usr/bin/env python3
#** *****************************************************************************
# *
# * If not stated otherwise in this file or this component's LICENSE file the
# * following copyright and licenses apply:
# *
# * Copyright 2026 RDK Management
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *
# http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *
#* ******************************************************************************

import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
sys.path.append(os.path.join(dir_path, "../../tests/raft/"))

from framework.core.logModule import logModule
from .abstractCompositeController import CompositeInterface

class manualCompositeController(CompositeInterface):
    """
    Manual Composite Input Controller stub.
    Logs operations that would require physical/manual intervention on a real device.
    """

    def __init__(self, logger: logModule, address: str = '', username: str = '',
                 password: str = '', port: int = 22, prompt: str = '~#', control_port: int = 8080):
        """
        Initializes the manualCompositeController.

        Args:
            logger (logModule): Logger module instance.
            address (str): IP address or hostname of the target device (unused).
            username (str): SSH username (unused).
            password (str): SSH password (unused).
            port (int): SSH port number (unused).
            prompt (str): SSH prompt string (unused).
            control_port (int): UT control plane port (unused).
        """
        super().__init__(logger, address, username, password, port, prompt, control_port)

    def connectDevice(self, port: int, connected: bool):
        """
        Log a manual connection request for a composite input port.

        Args:
            port (int): Composite input port number.
            connected (bool): True for connected, False for disconnected.

        Returns:
            bool: Always True (manual action assumed).
        """
        state_str = "CONNECTED" if connected else "DISCONNECTED"
        self._log.info(f"[manualCompositeController] Please manually set port {port} to {state_str}")
        return True

    def setSignalStatus(self, port: int, signal_status: str):
        """
        Log a manual signal status change request for a composite input port.

        Args:
            port (int): Composite input port number.
            signal_status (str): Signal status string (NO_SIGNAL, UNSTABLE, STABLE).

        Returns:
            bool: Always True (manual action assumed).
        """
        self._log.info(f"[manualCompositeController] Please manually set port {port} signal to {signal_status}")
        return True

    def setVideoMode(self, port: int, pixel_width: int, pixel_height: int,
                      interlaced: bool, frame_rate_hz: float):
        """
        Log a manual video mode change request for a composite input port.

        Args:
            port (int): Composite input port number.
            pixel_width (int): Horizontal resolution in pixels.
            pixel_height (int): Vertical resolution in pixels.
            interlaced (bool): True for interlaced, False for progressive.
            frame_rate_hz (float): Frame rate in Hz.

        Returns:
            bool: Always True (manual action assumed).
        """
        self._log.info(
            f"[manualCompositeController] Please manually set port {port} video mode to "
            f"{pixel_width}x{pixel_height}, interlaced={interlaced}, fps={frame_rate_hz}"
        )
        return True

    def start(self):
        """Start the manual composite controller (stub)."""
        pass

    def stop(self):
        """Stop the manual composite controller (stub)."""
        pass
