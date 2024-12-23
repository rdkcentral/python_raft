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
#*   ** @brief : cecClient controller. Class for running cec-client commands on
#*   **          the host PC. This requires the cec-utils package to be installed
#*   **          on the host.
#*   **
#* ******************************************************************************

from datetime import datetime
from io import IOBase
import re
import subprocess
from threading import Thread

from framework.core.logModule import logModule
from framework.core.streamToFile import StreamToFile
from .abstractCECController import CECInterface
from .cecTypes import CECDeviceType


class CECClientController(CECInterface):
    """
    This class provides an interface for controlling Consumer Electronics Control (CEC)
    devices through the `cec-client` command-line tool.
    """

    def __init__(self, adaptor_path:str, logger:logModule, streamLogger: StreamToFile):
        """
        Initializes the CECClientController instance.

        Args:
            adaptor_path (str): Path to the CEC adaptor device.
            logger (logModule): An instance of a logging module for recording messages.

        Raises:
            AttributeError: If the specified CEC adaptor is not found.
        """

        super().__init__(adaptor_path=adaptor_path, logger=logger, streamLogger=streamLogger)
        self._log.debug('Initialising CECClientController for [%s]' % self.adaptor)
        if self.adaptor not in map(lambda x: x.get('com port'),self._getAdaptors()):
            raise AttributeError('CEC Adaptor specified not found')
        self.start()

    def start(self):
        self._console = subprocess.Popen(f'cec-client {self.adaptor}'.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                stdin=subprocess.PIPE,
                                text=True)
        self._stream.writeStreamToFile(self._console.stdout)

    def stop(self):
        self._console.stdin.write('q\n')
        self._console.stdin.flush()
        try:
            self._console.wait()
        except subprocess.CalledProcessError:
            self._console.terminate()
        self._stream.stopStreamedLog()

    def sendMessage(self, sourceAddress: str, destAddress: str, opCode: str, payload: list = None) -> None:
        message = self.formatMessage(sourceAddress, destAddress, opCode, payload=payload)
        self._console.stdin.write(f'tx {message}\n')
        self._console.stdin.flush()

    def _getAdaptors(self) -> list:
        """
        Retrieves a list of available CEC adaptors using `cec-client`.

        Returns:
            list: A list of dictionaries representing available adaptors with details like COM port.
        """
        result = subprocess.run(f'cec-client -l',
                                shell=True,
                                text=True,
                                capture_output=True,
                                check=True)
        stdout = result.stdout
        adaptor_count = re.search(r'Found devices: ([0-9]+)',stdout, re.M).group(1)
        adaptors = self._splitDeviceSectionsToDicts(stdout)
        return adaptors

    def _scanCECNetwork(self) -> list:
        """
        Scans the CEC network for connected devices using `cec-client`.

        Sends a "scan" message and parses the response to identify connected devices.

        Returns:
            list: A list of dictionaries representing discovered devices with details.
        """
        devicesOnNetwork = []
        self._console.stdin.write('scan')
        self._console.stdin.flush()
        output = self._stream.readUntil('currently active source',30)
        if len(output) > 0:
            output = '\n'.join(output)
            self._log.debug('Output of scan on CEC Network: [%s]' % output)
            devicesOnNetwork = self._splitDeviceSectionsToDicts(output)
        return devicesOnNetwork

    def listDevices(self) -> list:
        devices = self._scanCECNetwork()
        for device_dict in devices:
            # Remove the 'address' from the dict and change it to 'physical address'
            device_dict['physical address'] = device_dict.pop('address')
            device_dict['name'] = device_dict.get('osd string')
            for key in device_dict.keys():
                if 'device' in key.lower():
                    device_dict['logical address'] = key.rsplit('#')[-1]
                    device_dict.pop(key)
                    break
            if device_dict.get('active source') == 'yes':
                device_dict['active source'] = True
            else:
                device_dict['active source'] = False
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

    def formatMessage(self, sourceAddress: str, destAddress: str, opCode:str, payload: list = None) -> str:
        message_string = f'{sourceAddress}{destAddress}:{opCode[2:]}'
        if payload:
            payload_string = ':'.join(map(lambda x: x[2:], payload))
            message_string += ':' + payload_string
        return message_string.lower()

    def __del__(self):
        """
        Destructor for the class, ensures monitoring is stopped.
        """
        self.stop()
