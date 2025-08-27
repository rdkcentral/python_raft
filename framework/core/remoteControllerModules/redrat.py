#!/usr/bin/env python3
#** *****************************************************************************
# *
# * If not stated otherwise in this file or this component's LICENSE file the
# * following copyright and licenses apply:
# *
# * Copyright 2023 RDK Management
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
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core.remoteControllerModules
#*   ** @date        : 22/11/2021
#*   **
#*   ** @brief : remote Redrat
#*   **
#* ******************************************************************************

import socket
import time

from framework.core.logModule import logModule
from .remoteInterface import RemoteInterface

class HubClient():

    def __init__(self):
        self._socket = socket.socket()
        self._is_open = False

    def __del__(self):
        self.stop()

    def start(self, hub_ip: str, hub_port: int = 40000, netbox_ip: None|str=None):
        """Start a socket connection to the RedRat Hub on the given IP and port.
        If the netbox IP address is given, it will check that it's available on the hub.

        Args:
            hub_ip (str): IP address of the RedRat Hub server.
            hub_port (int, optional): Socket port of the RedRat Hub server. Defaults to 40000.
            netbox_ip (None | str, optional): IP address of the IR Netbox expected
                                              to be connected to the RedRat Hub server. Defaults to None.

        Raises:
            ConnectionError: If IR Netbox IP address isn't found on the RedRat Hub.
                             This will also occur if the hub address/port is not actually a
                             RedRat Hub socker server.
        """
        self._socket.connect((hub_ip, hub_port))
        if netbox_ip is not None:
            response = self.send_message('hubquery="list redrats"')
            netbox_on_hub = list(filter(lambda x: netbox_ip in x, response))
            if len(netbox_on_hub) <= 0:
                raise ConnectionError('Could not connect to RedRat Hub. It may be misconfigured.')

        self._is_open = True

    def stop(self):
        if self._is_open:
            self._socket.close()
            self._is_open = False

    def send_message(self, message: str) -> str:
        """Send a message to the RedRatHub via the socket

        Args:
            message (str): The message to send.

        Returns:
            str: The response from the socket.
        """
        self._socket.send(f'{message}\n'.encode())
        response = ''
        timeout = 60
        start_time = time.time()
        while True:
            response += self._socket.recv(64).decode()
            if ('{' in response and '}' in response) or '\n' in response:
                return response
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                return ''

class remoteRedRat(RemoteInterface):

    def __init__(self, log: logModule, config: dict):
        super().__init__(log, config)
        self._hub_ip = config.get('hub_ip')
        self._hub_port = config.get('hub_port',5248)
        self._client = HubClient()
        self._netbox_ip = config.get('netbox_ip')
        self._client.start(self._hub_ip, hub_port=self._hub_port, netbox_ip=self._netbox_ip)
        self._output = config.get('output', 1)

    def sendKey(self, code, repeat, delay):
        msg = f'ip="{self._netbox_ip}" {code} output="{self._output}"'
        for _ in range(repeat):
            if 'OK' not in self._client.send_message(msg):
                self.log.error("sendKey(), Command [{}] failed.".format( code ) )
                return False
            time.sleep( delay )
        return True


