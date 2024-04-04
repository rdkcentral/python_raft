
#! /bin/python3
#/* *****************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
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
    def write(self, message):
        """Abstract method. Define how to write to the console.

        Args:
            message (str): Message to write into the console.
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