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

from compositeModules.virtualCompositeController import virtualCompositeController
from compositeModules.manualCompositeController import manualCompositeController

class CompositeController:
    """
    High-level Composite Input controller.
    Instantiates the correct backend controller type based on configuration.
    """

    def __init__(self, log, config: dict):
        """
        Initializes the CompositeController.

        Args:
            log: Logger module instance.
            config (dict): Controller configuration from rack YAML.
                Expected keys:
                    type (str): 'virtual-composite-controller' or 'manual-composite-controller'
                    address (str): Target device IP address.
                    username (str): SSH username.
                    password (str): SSH password.
                    port (int): SSH port number.
                    control_port (int): UT control plane port.
        """
        self._log = log
        self.controllerType = config.get('type', 'virtual-composite-controller')

        if self.controllerType == 'virtual-composite-controller':
            self.controller = virtualCompositeController(
                self._log,
                address=config.get('address'),
                username=config.get('username', ''),
                password=config.get('password', ''),
                port=config.get('port', 22),
                prompt=config.get('prompt', '~#'),
                control_port=config.get('control_port', 8080)
            )
        elif self.controllerType == 'manual-composite-controller':
            self.controller = manualCompositeController(
                self._log,
                address=config.get('address'),
                username=config.get('username', ''),
                password=config.get('password', ''),
                port=config.get('port', 22),
                prompt=config.get('prompt', '~#'),
                control_port=config.get('control_port', 8080)
            )
        else:
            raise ValueError(f"[CompositeController] Unknown controller type: {self.controllerType}")

    def connectDevice(self, port: int, connected: bool):
        """
        Set the connection status for a composite input port.

        Args:
            port (int): Composite input port number.
            connected (bool): True for connected, False for disconnected.

        Returns:
            bool: True if the operation was successful.
        """
        return self.controller.connectDevice(port, connected)

    def setSignalStatus(self, port: int, signal_status: str):
        """
        Set the signal status for a composite input port.

        Args:
            port (int): Composite input port number.
            signal_status (str): Signal status string.
                Possible values: NO_SIGNAL, UNSTABLE, STABLE

        Returns:
            bool: True if the operation was successful.
        """
        return self.controller.setSignalStatus(port, signal_status)

    def setVideoMode(self, port: int, pixel_width: int, pixel_height: int,
                     interlaced: bool, frame_rate_hz: float):
        """
        Set the detected video mode for a composite input port.

        Args:
            port (int): Composite input port number.
            pixel_width (int): Horizontal resolution in pixels.
            pixel_height (int): Vertical resolution in pixels.
            interlaced (bool): True for interlaced, False for progressive.
            frame_rate_hz (float): Frame rate in Hz.

        Returns:
            bool: True if the operation was successful.
        """
        return self.controller.setVideoMode(port, pixel_width, pixel_height, interlaced, frame_rate_hz)
