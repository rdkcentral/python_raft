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


class consoleInterface(metaclass=ABCMeta):

    @abstractmethod
    def write(self, message:list|str, lineFeed:str="\n"):
        """Abstract method. Define how to write to the console.
        This method by default is to always send newLine

        Args:
            message (list|str): String or list to write into the console.
            lineFeed (str): Linefeed extension
        """
        raise NotImplementedError('users must define write() to use this base class')

    @abstractmethod
    def open(self):
        """Abstract method. Define how to open the console session.
        """
        raise NotImplementedError('users must define open() to use this base class')

    @abstractmethod
    def read_all(self):
        """Abstract method. Define how to read all information displayed in the console.
            Should return the data read.
        """
        raise NotImplementedError('users must define read_all() to use this base class')

    @abstractmethod
    def read_until(self, value):
        """Abstract method. Define how to read all the information displayed in the console,
            upto the point a defined string appears.
            Should return the data read.

        Args:
            value (str): Message to wait for in the console.
        """
        raise NotImplementedError('users must define read_until() to use this base class')

    @abstractmethod
    def close(self):
        """Close the console session.
        """
        raise NotImplementedError('users must define close() to use this base class')