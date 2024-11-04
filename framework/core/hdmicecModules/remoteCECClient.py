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
from framework.core.commandModules.sshConsole import sshConsole
from .abstractCECController import CECInterface
from .cecTypes import MonitoringType

class RemoteCECClient(CECInterface):

    def __init__(self, adaptor: str,logger: logModule, address: str, port: int = 22, username: str = '', password: str = ''):
        super().__init__(adaptor, logger)
        self._console = sshConsole(self._log,address, username, password, port=port)
        self._log.debug('Initialising RemoteCECClient controller')
        try:
            self._console.open()
        except:
            self._log.critical('Could not open connection to RemoteCECClient controller')
            raise
        if self.adaptor not in map(lambda x: x.get('com port'),self._getAdaptors()):
            raise AttributeError('CEC Adaptor specified not found')
        self._monitoringLog = None

    @property
    def monitoring(self) -> bool:
        return self._monitoring
    
    def _getAdaptors(self) -> list:
        """
        Retrieves a list of available CEC adaptors using `cec-client`.

        Returns:
            list: A list of dictionaries representing available adaptors with details like COM port.
        """
        self._console.write(f'cec-client -l')
        stdout = self._console.read_until('currently active source')
        stdout = stdout.replace('\r\n','\n')
        adaptor_count = re.search(r'Found devices: ([0-9]+)',stdout, re.M).group(1)
        adaptors = self._splitDeviceSectionsToDicts(stdout)
        return adaptors

    def sendMessage(self, message:str) -> bool:
        """
        Send a CEC message to the CEC network.

        Args:
            message (str): The CEC message to be sent.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        return self._console.write(f'echo "{message}" | cec-client {self.adaptor}')

    def listDevices(self) -> list:
        """
        List CEC devices on CEC network.

        The list returned contains dicts in the following format:
            {
            'name': 'TV'
            'address': '0.0.0.0',
            'active source': True,
            'vendor': 'Unknown',
            'osd string': 'TV', 
            'CEC version': '1.3a', 
            'power status': 'on', 
            'language': 'eng', 
            }
        Returns:
            list: A list of dictionaries representing discovered devices.
        """
        self.sendMessage('scan')
        output = self._console.read_until('currently active source')
        devices = self._splitDeviceSectionsToDicts(output.replace('\r\n','\n'))
        for device in devices:
            device['name'] = device.get('osd string')
            if device.get('active source') == 'yes':
                device['active source'] = True
            else:
                device['active source'] = False
        return devices

    def startMonitoring(self, monitoringLog: str, deviceType: MonitoringType=MonitoringType.RECORDER) -> None:
        """
        Starts monitoring CEC messages with a specified device type.

        Args:
            deviceType (MonitoringType, optional): The type of device to monitor (default: MonitoringType.RECORDER).
            monitoringLog (str) : Path to write the monitoring log out
        """
        self._monitoringLog = monitoringLog
        self._console.write(f'cec-client -m -t{deviceType.value}')
        self._console.shell.set_combine_stderr(True)
        self._log.logStreamToFile(self._console.shell.makefile(), self._monitoringLog)
        self._monitoring = True

    def stopMonitoring(self) -> None:
        """
        Stops the CEC monitoring process.
        """
        if self.monitoring is False:
            return
        self._console.write('\x03')
        self._log.stopStreamedLog(self._monitoringLog)

    def _splitDeviceSectionsToDicts(self,command_output:str) -> list:
            """
            Splits the output of a `cec-client` command into individual device sections and parses them into dictionaries.

            Args:
                command_output (str): The output string from the `cec-client` command.

            Returns:
                list: A list of dictionaries, each representing a single CEC device with its attributes.
            """
            devices = []
            device_sections = re.findall(r'^device[ #0-9]{0,}:[\s\S]+?(?:type|language): +[\S ]+$',
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