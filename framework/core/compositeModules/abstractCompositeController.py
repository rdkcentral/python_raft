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

from abc import ABC, abstractmethod

from framework.core.logModule import logModule

class CompositeInterface(ABC):

    def __init__(self, logger: logModule, address: str, username: str,
                 password: str, port: int = 22, prompt: str = '~#', control_port: int = 8080):
        """
        Abstract base class for composite input controllers.
        Defines the interface for controlling the composite input device.
        """
        self._log = logger

    @abstractmethod
    def connectDevice(self, port: int, connected: bool):
        """
        Set the connection status for the composite input port.

        Args:
            port (int): Composite input port number.
            connected (bool): True for connected, False for disconnected.

        Returns:
            bool: True if message sent successfully.
        """
        pass

    @abstractmethod
    def setSignalStatus(self, port: int, signal_status: str):
        """
        Set the signal status for the composite input port.

        Args:
            port (int): Composite input port number.
            signal_status (str): Signal status string.
                Possible values: NO_SIGNAL, UNSTABLE, STABLE

        Returns:
            bool: True if message sent successfully.
        """
        pass

    @abstractmethod
    def setVideoMode(self, port: int, pixel_width: int, pixel_height: int,
                     interlaced: bool, frame_rate_hz: float):
        """
        Set the detected video mode for the composite input port.

        Triggers an onVideoModeChanged() callback on the DUT (port must be STARTED).

        Args:
            port (int): Composite input port number.
            pixel_width (int): Horizontal resolution in pixels.
            pixel_height (int): Vertical resolution in pixels.
            interlaced (bool): True for interlaced, False for progressive.
            frame_rate_hz (float): Frame rate in Hz.

        Returns:
            bool: True if message sent successfully.
        """
        pass
