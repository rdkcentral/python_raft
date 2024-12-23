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
#*   ** @addtogroup  : core
#*   ** @date        : 02/10/2024
#*   **
#*   ** @brief : Abstract class for CEC controller types.
#*   **
#* ******************************************************************************

import re

from framework.core.logModule import logModule
from framework.core.streamToFile import StreamToFile
from framework.core.commandModules.sshConsole import sshConsole
from .abstractCECController import CECInterface
from .cecTypes import CECDeviceType

class RemoteCECClient(CECInterface):

    def __init__(self, adaptor: str,logger: logModule, streamLogger: StreamToFile, address: str, port: int = 22, username: str = '', password: str = '', prompt = ':~'):
        super().__init__(adaptor, logger, streamLogger)
        self._console = sshConsole(self._log,address, username, password, port=port, prompt=prompt)
        self._log.debug('Initialising RemoteCECClient controller')
        try:
            self._console.open()
        except:
            self._log.critical('Could not open connection to RemoteCECClient controller')
            raise
        if self.adaptor not in map(lambda x: x.get('com port'),self._getAdaptors()):
            raise AttributeError('CEC Adaptor specified not found')
        self.start()

    def start(self):
        self._console.write(f'cec-client {self.adaptor}')
        self._stream.writeStreamToFile(self._console.shell.makefile())

    def stop(self):
        self._console.write('q')
        self._stream.stopStreamedLog()

    def _getAdaptors(self) -> list:
        """
        Retrieves a list of available CEC adaptors using `cec-client`.

        Returns:
            list: A list of dictionaries representing available adaptors with details like COM port.
        """
        self._console.write(f'cec-client -l')
        stdout = self._console.read()
        stdout = stdout.replace('\r\n','\n')
        adaptor_count = re.search(r'Found devices: ([0-9]+)',stdout, re.M).group(1)
        adaptors = self._splitDeviceSectionsToDicts(stdout)
        return adaptors

    def sendMessage(self, sourceAddress: str, destAddress: str, opCode: str, payload: list = None) -> None:
        message = self.formatMessage(sourceAddress, destAddress, opCode, payload=payload)
        self._console.write(f'tx {message}')

    def listDevices(self) -> list:
        self._console.write(f'scan')
        output = self._stream.readUntil('currently active source',30)
        devices = []
        if len(output) > 0:
            output = '\n'.join(output)
            devices = self._splitDeviceSectionsToDicts(output)
        for device in devices:
            device['physical address'] = device.pop('address')
            device['name'] = device.get('osd string')
            for key in device.keys():
                if 'device' in key.lower():
                    device['logical address'] = key.rsplit('#')[-1]
                    device.pop(key)
                    break
            if device.get('active source') == 'yes':
                device['active source'] = True
            else:
                device['active source'] = False
        return devices

    def _splitDeviceSectionsToDicts(self,command_output:str) -> list:
            """
            Splits the output of a `cec-client` command into individual device sections and parses them into dictionaries.

            Args:
                command_output (str): The output string from the `cec-client` command.

            Returns:
                list: A list of dictionaries, each representing a single CEC device with its attributes.
            """
            devices = []
            device_sections = re.findall(r'^device[ #0-9A-F]{0,}:[\s\S]+?(?:type|language): +[\S ]+$',
                                        command_output,
                                        re.M)
            if device_sections:
                for section in device_sections:
                    device_dict = {}
                    for line in section.split('\n'):
                        line_split = re.search(r'^([\w #]+): +?(\S[\S ]{0,})$',line)
                        if line_split:
                            device_dict[line_split.group(1)] = line_split.group(2)
                    devices.append(device_dict)
            return devices

    def formatMessage(self, sourceAddress, destAddress, opCode, payload = None):
        message_string = f'{sourceAddress}{destAddress}:{opCode[2:]}'
        if payload:
            payload_string = ':'.join(map(lambda x: x[2:], payload))
            message_string += ':' + payload_string
        return message_string.lower()