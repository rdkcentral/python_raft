#! /bin/python3
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
#*   ** @date        : 20/11/2021
#*   **
#*   ** @brief : wrapper for powerSwitch None
#*   **
#/* ******************************************************************************
import time

class powerNone():
    
    def __init__(self, log):
        """
        Initialize the PowerSwitchNone instance.

        Args:
            log: The log module.
        """
        self.log = log
        self.log.info("PowerSwitchNone()")
        pass

    def powerOn(self):
        """
        Turn on the power.

        Returns:
            bool: Always returns True.
        """
        self.log.info("powerSwitchNone().powerOn")
        return True

    def powerOff(self):
        """
        Turn off the power.

        Returns:
            bool: Always returns True.
        """
        self.log.info("powerSwitchNone().powerOff")
        return True

    def reboot(self):
        """
        Reboot the device.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        result = self.powerOff()
        if result != True:
            self.log.error(" Power Failed off")
        time.sleep(1)
        result = self.powerOn()
        if result != True:
            self.log.error(" Power Failed on")
        return result