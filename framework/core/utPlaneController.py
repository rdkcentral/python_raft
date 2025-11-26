#!/usr/bin/env python3
#** *****************************************************************************
# *
# * If not stated otherwise in this file or this component's LICENSE file the
# * following copyright and licenses apply:
# *
# * Copyright 2025 RDK Management
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
sys.path.append(os.path.join(dir_path, "..", "..", ".."))

from framework.core.logModule import logModule

class utPlaneController():
    """
    UT Plane Controller class for managing communication with the ut-controller.

    This class provides an interface to interact with the ut-controller running on a device.
    It facilitates sending commands and YAML configuration files to the controller via HTTP requests
    using curl commands. The controller operates over a configurable port (default: 8080) and uses
    the session object to execute commands on the target device.

    Typical usage involves:
    1. Creating an instance with an active session and optional port/log configuration
    2. Preparing YAML files with test commands or configuration
    3. Sending these files to the ut-controller using sendMessage()

    Attributes:
        session (object): Active session object for device communication
        port (int): Port number where ut-controller service is listening (default: 8080)
        log (logModule): Logger instance for recording controller activities and debugging

    Example:
        >>> controller = utPlaneController(session, port=8080)
        >>> controller.sendMessage("/path/on/dut/to/test_config.yaml")
        >>> controller.sendMessage("yaml string directly")
    """

    def __init__(self, session:object, port: int = 8080, log: logModule = None):
        """
        Initializes UT Plane Controller class.

        Args:
            session (class): The session object to communicate with the device
            port (int): The port number for the controller
            log (class, optional): Parent log class. Defaults to None.
        """

        # Validate session
        if session is None:
            raise ValueError("session cannot be None")

        self.log = log
        if log is None:
            self.log = logModule(self.__class__.__name__)
            self.log.setLevel( self.log.INFO )

        self.session = session
        self.port = port

    def sendMessage(self, yamlInput: str, isFile: bool = False) -> bool:
        """
        Sends a command to the ut-controller via curl.

        Args:
            yamlInput (str): Either a YAML string or path to a YAML file.
            isFile (bool): Flag indicating if yamlInput is a file path. Defaults to False.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        try:
            # Validate input
            if not yamlInput or not isinstance(yamlInput, str):
                self.log.error("Invalid input provided")
                return False

            if isFile:
                # It's a file path on target device - use --data-binary with file reference
                yaml_content = yamlInput
                cmd = f'curl -X POST -H "Content-Type: application/x-yaml" --data-binary @"{yaml_content}" "http://localhost:{self.port}/api/postKVP"'
            else:
                # It's a direct YAML string - escape quotes and send inline
                yaml_content = yamlInput.replace('"', '\\"')
                cmd = f'curl -X POST -H "Content-Type: application/x-yaml" --data-binary "{yaml_content}" "http://localhost:{self.port}/api/postKVP"'

            result = True

            # Send command
            result = self.session.write(cmd)

            self.log.info(f"Message sent successfully to ut-controller on port {self.port}")
            return result

        except Exception as e:
            self.log.error(f"Failed to send message to ut-controller: {str(e)}")
            return False
