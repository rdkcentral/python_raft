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
#*   ** @addtogroup  : core.powerModules
#*   ** @date        : 14/01/2025
#*   **
#*   ** @brief : Abstract Power Module
#*   **
#* *****************************************************************************

from abc import ABCMeta, abstractmethod
import time

from framework.core.logModule import logModule


class PowerModuleInterface(metaclass=ABCMeta):

    def __init__(cls,logger: logModule):
        cls._log = logger
        cls._is_on = False

    @property
    def is_on(cls):
        """Boolean for the current power state of the powerswitch/outlet
        True if the powerswitch/outlet is powered on.
        """
        return cls._is_on

    @property
    def is_off(cls):
        """Boolean for the current power state of the powerswitch/outlet
        True if the powerswitch/outlet is powered off.
        """
        if cls.is_on:
            return False
        return True

    @abstractmethod
    def powerOn(cls) -> bool:
        """Turn on the powerswitch/outlet.

        Returns:
            bool: True if successfully switched on.
        """
        pass

    @abstractmethod
    def powerOff(cls) -> bool:
        """Turn off the powerswitch/outlet.

        Returns:
            bool: True if successfully switched off.
        """
        pass

    def reboot(self) -> bool:
        """Power cycle the powerswitch/outlet.

        Returns:
            bool: True if successfully turned back on.
        """
        if self.is_on:
            self.powerOff()
            time.sleep(1)
        self.powerOn()
        return self.is_on

    def getPowerLevel(cls) -> float:
        """Retrieve the current power draw from the powerswitch/outlet.

        Returns:
            float: Power level in Watts.

        Raises:
            RuntimeError: When method cannot be implemented for the powerswitch type.
        """
        raise RuntimeError('Power monitoring is not supported by this power module: [{}]'.format(cls.__class__.__name__))
    
    def getVoltageLevel(cls) -> float:
        """Retrieve the current Voltage draw from the powerswitch/outlet.

        Returns:
            float: Voltage level in Volts.

        Raises:
            RuntimeError: When method cannot be implemented for the powerswitch type.
        """
        raise RuntimeError('Voltage monitoring is not supported by this power module: [{}]'.format(cls.__class__.__name__))
    
    def getCurrentLevel(cls) -> float:
        """Retrieve the current power draw from the powerswitch/outlet.

        Returns:
            float: Current level in Amps.

        Raises:
            RuntimeError: When method cannot be implemented for the powerswitch type.
        """
        raise RuntimeError('Current monitoring is not supported by this power module: [{}]'.format(cls.__class__.__name__))