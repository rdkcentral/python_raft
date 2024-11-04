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

from abc import ABCMeta, abstractmethod

from framework.core.logModule import logModule
from .cecTypes import MonitoringType

class CECInterface(metaclass=ABCMeta):

    def __init__(self, adaptor_path:str, logger:logModule):
        self.adaptor = adaptor_path
        self._log = logger
        self._monitoring = False
        self._monitoring_log = None

    @property
    def monitoring(self) -> bool:
        return self._monitoring

    @abstractmethod
    def sendMessage(cls, message:str) -> bool:
        """
        Send a CEC message to the CEC network.

        Args:
            message (str): The CEC message to be sent.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        pass

    @abstractmethod
    def listDevices(cls) -> list:
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
        pass

    @abstractmethod
    def startMonitoring(cls, monitoringLog: str, deviceType: MonitoringType=MonitoringType.RECORDER) -> None:
        """
        Starts monitoring CEC messages with a specified device type.

        Args:
            deviceType (MonitoringType, optional): The type of device to monitor (default: MonitoringType.RECORDER).
            monitoringLog (str) : Path to write the monitoring log out
        """
        pass

    @abstractmethod
    def stopMonitoring(cls) -> None:
        """
        Stops the CEC monitoring process.
        """
        pass
