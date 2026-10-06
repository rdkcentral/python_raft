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
import yaml

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
sys.path.append(os.path.join(dir_path, "../../tests/raft/"))

command_templates_dir = os.path.join(dir_path, 'commands')
CONNECTION_STATUS_CMD_TEMPLATE = os.path.join(command_templates_dir, 'compositeinput_connection_status.yaml')
SIGNAL_STATUS_CMD_TEMPLATE     = os.path.join(command_templates_dir, 'compositeinput_signal_status.yaml')
VIDEO_MODE_CMD_TEMPLATE        = os.path.join(command_templates_dir, 'compositeinput_video_mode.yaml')

from framework.core.logModule import logModule
from framework.core.commandModules.sshConsole import sshConsole
from .abstractCompositeController import CompositeInterface
from framework.core.utPlaneController import utPlaneController

class virtualCompositeController(CompositeInterface):
    """
    Virtual Composite Input Controller.
    Drives the composite input vcomponent via the UT control plane using YAML messages.
    """

    def __init__(self, logger: logModule, address: str, username: str,
                 password: str, port: int = 22, prompt: str = '~#', control_port: int = 8080):
        """
        Initializes the virtualCompositeController.

        Args:
            logger (logModule): Logger module instance.
            address (str): IP address or hostname of the target device.
            username (str): SSH username.
            password (str): SSH password.
            port (int): SSH port number. Defaults to 22.
            prompt (str): SSH prompt string. Defaults to '~#'.
            control_port (int): UT control plane port. Defaults to 8080.
        """
        super().__init__(logger, address, username, password, port, prompt, control_port)

        self.control_port = control_port
        self.commandPrompt = prompt

        try:
            self.session = sshConsole(self._log, address, username, password, port=port, prompt=prompt)
            self.utPlaneController = utPlaneController(self.session, port=self.control_port)
        except Exception as e:
            self._log.critical(f"[virtualCompositeController] Failed to connect: {e}")
            raise

    def connectDevice(self, port: int, connected: bool):
        """
        Set the connection status for a composite input port.

        Sends a 'connection_status' command to the vcomponent via the UT control plane.

        Args:
            port (int): Composite input port number.
            connected (bool): True for connected, False for disconnected.

        Returns:
            bool: True if the message was sent successfully.
        """
        with open(CONNECTION_STATUS_CMD_TEMPLATE, 'r') as f:
            msg = yaml.safe_load(f)
        msg['compositeinput']['params']['port']      = port
        msg['compositeinput']['params']['connected'] = connected
        yaml_str = yaml.dump(msg)
        self._log.info(f"[virtualCompositeController] connectDevice(port={port}, connected={connected})")
        return self.utPlaneController.sendMessage(yaml_str)

    def setSignalStatus(self, port: int, signal_status: str):
        """
        Set the signal status for a composite input port.

        Sends a 'signal_status' command to the vcomponent via the UT control plane.

        Args:
            port (int): Composite input port number.
            signal_status (str): Signal status string.
                Possible values: NO_SIGNAL, UNSTABLE, STABLE

        Returns:
            bool: True if the message was sent successfully.
        """
        with open(SIGNAL_STATUS_CMD_TEMPLATE, 'r') as f:
            msg = yaml.safe_load(f)
        msg['compositeinput']['params']['port']         = port
        msg['compositeinput']['params']['signalStatus'] = signal_status
        yaml_str = yaml.dump(msg)
        self._log.info(f"[virtualCompositeController] setSignalStatus(port={port}, signalStatus={signal_status})")
        return self.utPlaneController.sendMessage(yaml_str)

    def setVideoMode(self, port: int, pixel_width: int, pixel_height: int,
                      interlaced: bool, frame_rate_hz: float):
        """
        Set the detected video mode for a composite input port.

        Sends a 'video_mode' command to the vcomponent via the UT control plane.
        The port must be in STARTED state for the event to be processed.

        Args:
            port (int): Composite input port number.
            pixel_width (int): Horizontal resolution in pixels.
            pixel_height (int): Vertical resolution in pixels.
            interlaced (bool): True for interlaced, False for progressive.
            frame_rate_hz (float): Frame rate in Hz.

        Returns:
            bool: True if the message was sent successfully.
        """
        with open(VIDEO_MODE_CMD_TEMPLATE, 'r') as f:
            msg = yaml.safe_load(f)
        msg['compositeinput']['params']['port']         = port
        msg['compositeinput']['params']['pixelWidth']   = pixel_width
        msg['compositeinput']['params']['pixelHeight']  = pixel_height
        msg['compositeinput']['params']['interlaced']   = interlaced
        msg['compositeinput']['params']['frameRateInHz'] = frame_rate_hz
        yaml_str = yaml.dump(msg)
        self._log.info(
            f"[virtualCompositeController] setVideoMode(port={port}, "
            f"{pixel_width}x{pixel_height}, interlaced={interlaced}, fps={frame_rate_hz})"
        )
        return self.utPlaneController.sendMessage(yaml_str)

    def start(self):
        """Start the virtual composite controller (stub)."""
        pass

    def stop(self):
        """Stop the virtual composite controller (stub)."""
        pass
