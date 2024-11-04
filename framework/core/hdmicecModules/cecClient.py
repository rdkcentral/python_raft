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

from io import IOBase
import re
import subprocess
from threading import Thread

from framework.core.logModule import logModule
from .abstractCECController import CECInterface
from .cecTypes import MonitoringType


class CECClientController(CECInterface):
    """
    This class provides an interface for controlling Consumer Electronics Control (CEC) 
    devices through the `cec-client` command-line tool.
    """

    def __init__(self, adaptor_path:str, logger:logModule):
        """
        Initializes the CECClientController instance.

        Args:
            adaptor_path (str): Path to the CEC adaptor device.
            logger (logModule): An instance of a logging module for recording messages.

        Raises:
            AttributeError: If the specified CEC adaptor is not found.
        """
        
        super().__init__(adaptor_path=adaptor_path, logger=logger)
        self._log.debug('Initialising CECClientController for [%s]' % self.adaptor)
        if self.adaptor not in map(lambda x: x.get('com port'),self._getAdaptors()):
            raise AttributeError('CEC Adaptor specified not found')
        self._monitoring = False
        self._m_proc = None
        self._m_stdout_thread = None

    def sendMessage(self,message: str) -> bool:
        exit_code, stdout =  self._sendMessage(message, 0)
        self._log.debug('Output of message sent: [%s]' % stdout)
        if exit_code != 0:
            return False
        return True

    def _sendMessage(self, message: str, debug: int = 1) -> tuple:
        """
        Internal method for sending a CEC message using `subprocess`.

        Args:
            message (str): The CEC message to be sent.
            debug (int, optional): Debug level for `cec-client` (default: 1).

        Returns:
            tuple: A tuple containing the exit code of the subprocess call and the standard output.
        """
        result = subprocess.run(f'echo "{message}" | cec-client {self.adaptor} -s -d {debug}',
                                shell=True,
                                check=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')
        exit_code = result.returncode
        return exit_code, stdout

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
        _, result = self._sendMessage('scan')
        self._log.debug('Output of scan on CEC Network: [%s]' % result)
        devicesOnNetwork = self._splitDeviceSectionsToDicts(result)
        return devicesOnNetwork

    def listDevices(self) -> list:
        devices = self._scanCECNetwork()
        for device_dict in devices:
            device_dict['name'] = device_dict.get('osd string')
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

    def startMonitoring(self, monitoringLog: str, device_type: MonitoringType = MonitoringType.RECORDER) -> None:
        self._monitoring = True
        self._monitoring_log = monitoringLog
        try:
            self._m_proc = subprocess.Popen(f'cec-client {self.adaptor} -m -d 0 -t {device_type.value}'.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                text=True)
            self._log.logStreamToFile(self._m_proc.stdout, self._monitoring_log)
        except Exception as e:
            self.stopMonitoring()
            raise

    def stopMonitoring(self) -> None:
        self._log.debug('Stopping monitoring of adaptor [%s]' % self.adaptor)
        if self.monitoring is False:
            return
        self._m_proc.terminate()
        exit_code = self._m_proc.wait()
        self._log.stopStreamedLog(self._monitoring_log)
        self._monitoring_log = None
        self._monitoring = False

    def __del__(self):
        """
        Destructor for the class, ensures monitoring is stopped.
        """
        self.stopMonitoring()
