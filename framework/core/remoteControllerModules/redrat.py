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

    def start(self, ip: str, port: int = 5248):
        self._socket.connect((ip, port))
        self._is_open = True

    def stop(self):
        if self._is_open:
            self._socket.close()
            self._is_open = False

    def send_message(self, message):
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
        self._client.start(self._hub_ip, self._hub_port)
        self._netbox_ip = config.get('netbox_ip')
        self._output = config.get('output', 1)

    def sendKey(self, code, repeat, delay):
        msg = f'ip="{self._netbox_ip}" {code} output="{self._output}"'
        for _ in range(repeat):
            if 'OK' not in self._client.send_message(msg):
                self.log.error("sendKey(), Command [{}] failed.".format( code ) )
                return False
            time.sleep( delay )
        return True


