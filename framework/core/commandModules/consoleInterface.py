#!/usr/bin/env python3
#/* *****************************************************************************
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
#*   ** @addtogroup  : core.commandModules
#*   ** @date        : 20/11/2021
#*   **
#*   ** @brief : wrapper for consoleInterface None
#*   **
#/* ******************************************************************************

from abc import ABCMeta, abstractmethod


from os import path
import sys
MY_PATH = path.realpath(__file__)
MY_DIR = path.dirname(MY_PATH)
sys.path.append(path.join(MY_DIR, '../../../'))
from framework.core.logModule import logModule


class consoleInterface(metaclass=ABCMeta):

    def __init__(self, log: logModule, prompt:str=None):
        self.log = log
        self.prompt = prompt
        self._timeout = 10

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, new_timeout):
        self._timeout = new_timeout

    @abstractmethod
    def open(self) -> bool:
        """Abstract method. Define how to open the console session.
        
        Returns:
            bool: True if the console session opened successfully, False otherwise.
        """
        raise NotImplementedError('users must define open() to use this base class')

    @abstractmethod
    def close(self) -> bool:
        """Close the console session.

        Returns:
            bool: True if the console session was closed successfully, False otherwise.
        """
        raise NotImplementedError('users must define close() to use this base class')

    @abstractmethod
    def read_until(self, value, timeout: int = 10) -> str:
        """Abstract method. Define how to read all the information displayed in the console,
            upto the point a defined string appears.

        Args:
            value (str): Message to wait for in the console.
            timeout (int): Time limit before timing out, in seconds. Defaults to 10.

        Returns:
            str: The data read up to the specified value.
        """
        raise NotImplementedError('users must define read_until() to use this base class')

    @abstractmethod
    def read_all(self) -> str:
        """Abstract method. Define how to read all information displayed in the console.
        
        Returns:
            str: The data read from the console.
        """
        raise NotImplementedError('users must define read_all() to use this base class')
   
    @abstractmethod
    def write(self, message:list|str, lineFeed: str="\n", wait_for_prompt:bool=False) -> bool:
        """Abstract method. Define how to write to the console.
        This method by default is to always send newLine

        Args:
            message (list|str): String or list to write into the console.
            lineFeed (str): Linefeed extension
            wait_for_prompt (bool): If True, waits for the prompt before writing.
        Returns:
            bool: True if the message was written successfully, False otherwise.
        """
        raise NotImplementedError('users must define write() to use this base class')

    def waitForPrompt(self, prompt:str=None, timeout:int=10) -> bool:
        """Wait for a specific prompt to appear in the console.
        
        Args:
            prompt (str, optional): The prompt to wait for. Defaults to the instance's prompt.
            timeout (int): Time limit before timing out, in seconds. Defaults to 10.

        Returns:
            bool: True if the prompt was found, False otherwise.
        """
        prompt = prompt or self.prompt
        if not prompt:
            self.log.error('No prompt specified for waitForPrompt.')
            return False
        output = self.read_until(prompt, timeout)
        return prompt in output