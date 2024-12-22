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
from datetime import datetime
import os

from framework.core.logModule import logModule
from framework.core.streamToFile import StreamToFile
from .cecTypes import CECDeviceType

class CECInterface(metaclass=ABCMeta):

    def __init__(self, adaptor_path:str, logger:logModule, streamLogger: StreamToFile):
        self.adaptor = adaptor_path
        self._log = logger
        self._console = None
        self._stream = streamLogger

    @abstractmethod
    def sendMessage(cls, sourceAddress: str, destAddress: str, opCode: str, payload: list = None, deviceType: CECDeviceType=None) -> None:
        """
        Sends an opCode from a specified source and to a specified destination.
        
        Args:
          sourceAddress (str): The logical address of the source device (0-9 or A-F).
          destAddress (str): The logical address of the destination device (0-9 or A-F).
          opCode (str): Operation code to send as an hexidecimal string e.g 0x81.
          payload (list): List of hexidecimal strings to be sent with the opCode. Optional.
        """
        pass

    @abstractmethod
    def listDevices(cls) -> list:
        """
        List CEC devices on CEC network.

        The list returned contains dicts in the following format:
            {'active source': False,
             'vendor': 'Unknown',
             'osd string': 'TV',
             'CEC version': '1.3a',
             'power status': 'on',
             'language': 'eng',
             'physical address': '0.0.0.0',
             'name': 'TV',
             'logical address': '0'}
        Returns:
            list: A list of dictionaries representing discovered devices.
        """
        pass

    @abstractmethod
    def start(cls):
        """Start the CECContoller.
        """
        pass

    @abstractmethod
    def stop(cls):
        """Stop the CECController.
        """
        pass

    def formatMessage(cls, sourceAddress: str, destAddress: str, opCode:str, payload: list = None) -> str:
        """Format the input information into the required message string
            for the CECController.

        Args:
          sourceAddress (str): The logical address of the source device (0-9 or A-F).
          destAddress (str): The logical address of the destination device (0-9 or A-F).
          opCode (str): Operation code to send as an hexidecimal string e.g 0x81.
          payload (list): List of hexidecimal strings to be sent with the opCode. Optional

        Returns:
            str: Formatted message for CECController.
        """
        pass

    def receiveMessage(self,sourceAddress: str, destAddress: str, opCode: str, timeout: int = 10, payload: list = None) -> bool:
        """
        This function checks to see if a specified opCode has been received.

        Args:
          sourceAddress (str): The logical address of the source device (0-9 or A-F).
          destAddress (str): The logical address of the destination device (0-9 or A-F).
          opCode (str): Operation code to send as an hexidecimal string e.g 0x81.
          timeout (int): The maximum amount of time, in seconds, that the method will
                           wait for the message to be received. Defaults to 10.
          payload (list): List of hexidecimal strings to be sent with the opCode. Optional.

        Returns:
            boolean: True if message is received. False otherwise.
        """
        result = False
        message = self.formatMessage(sourceAddress, destAddress, opCode, payload)
        output = self._stream.readUntil(message, timeout)
        if len(output) > 0:
                result = True
        return result
