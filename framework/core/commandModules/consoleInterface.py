
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
        raise NotImplementedError('users must define write() to use this base class')

    @abstractmethod
    def open(self):
        raise NotImplementedError('users must define open() to use this base class')

    @abstractmethod
    def read_all(self):
        raise NotImplementedError('users must define read_all() to use this base class')

    @abstractmethod
    def read_until(self, value):
        raise NotImplementedError('users must define read_until() to use this base class')

    @abstractmethod
    def close(self):
        raise NotImplementedError('users must define close() to use this base class')