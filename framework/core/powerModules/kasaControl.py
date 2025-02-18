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
#*   ** @addtogroup  : core.powerModules
#*   ** @date        : 15/11/2021
#*   **
#*   ** @brief : Power On and Off Kasa power switches
#*   **
#
# https://github.com/python-kasa/python-kasa
# Plugs:
#
#    HS100, HS103, HS105, HS107, HS110, KP105, KP115, KP401
#
# Power Strips:
#
#    EP40, HS300, KP303, KP400
#
# Wall switches:
#
#   HS200, HS210, HS220
#
# Bulbs:
#
#    EP40, LB100, LB110, LB120, LB130, LB230, KL50, KL60, KL110, KL120, KL125, KL130
#
# Light strips:
#
#   KL400, KL430
#
# @Note: Had issues with calling the python library directly it has comms errors
# To get round this issue and to get this in, since kasa command line tool works
# Swap the interface to use that instead
#* ******************************************************************************

import os
import time
import subprocess

from framework.core.logModule import logModule
from framework.core.powerModules.abstractPowerModule import PowerModuleInterface

class powerKasa(PowerModuleInterface):
    
    """Kasa power switch controller supports
    """
    
    def __init__( self, log:logModule, ip:str, args:str=None, options:str=None, **kwargs ):
        """[init the kasa module]

            kasa [OPTIONS] COMMAND [ARGS]...\n
            Examples:-\n
            kasa --strip --host 192.168.88.39 on --name "Plug 3"\n
            kasa --strip --host 192.168.88.39 on --index 0 # Complete strip overall, index 1 is the first socket\n
            kasa --plug --host 192.168.88.39 on\n

        Args:
            log ([logModule]): [log module]
            ip ([str]): [ip]
            args ([str], optional): [args]. Defaults to None.
            options ([str], optional): [options]. Defaults to None, which translates to "--plug"
            kwargs ([dict]): [any other args]
        """
        super().__init__(log)
        self.slotIndex=0
        self.ip = ip
        #config.get("ip")
        #args = config.get("args")
        #options = config.get("options")
        if options == None:
            options = "--type plug"
        if args == None:
            args = ""
        else:
            self.slotIndex=int(args.split("--index ")[1])
        self.options = options
        self.args = args

    def split_with_quotes(self, inputString):
        """
        Split a string considering quotes.

        Args:
            inputString (str): The input string to split.

        Returns:
            list: The list of substrings.
        """
        result = []
        quotes = False
        for substring in inputString.split('"'):
            if not quotes:
                result.extend(substring.split())
            else:
                result.append(substring)
            quotes = not quotes
        return result

    def remove_empty_strings(self, inputList):
        """
        Remove empty strings from a list.

        Args:
            inputList (list): The list to clean.

        Returns:
            list: The cleaned list.
        """
        empty_strings = []
        for string in inputList:
            if (string != ""):
                empty_strings.append(string)
        return empty_strings;

    def performCommand(self, command, noOptions = False, noArgs = False):
        """
        Perform a command.

        Args:
            command (str): The command to execute.
            noOptions (bool, optional): Whether to exclude options. Defaults to False.
            noArgs (bool, optional): Whether to exclude arguments. Defaults to False.

        Returns:
            str: The command output.
        """
        extension = ""
        extension += "--host {} ".format(self.ip)
        if noOptions == False:
            extension += "{} ".format( self.options )
        extension += "{}".format(command)
        if noArgs == False:
            extension += " {}".format(self.args)
        # kasa [OPTIONS] COMMAND [ARGS]...
        command = self.split_with_quotes( "kasa " + extension )
        self._log.debug( "Command: {}".format(command))
        data = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        self._log.debug(data.stdout)
        return data.stdout

    def powerOff(self):
        """
        Turn off the device.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        self.__getstate__()
        if self.is_off:
            return True
        self.performCommand("off")
        self.__getstate__()
        if self.is_off == False:
            self._log.error(" Power Off Failed")
        return self.is_off

    def powerOn(self):
        """
        Turn on the device.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        self.__getstate__()
        if self.is_on:
            return True
        self.performCommand("on")
        self.__getstate__()
        if self.is_on == False:
            self._log.error(" Power On Failed")    
        return self.is_on

    def __getstate__(self):
        """Get the state of the device.
        """
        if "strip" in self.options:
            # We have a strip look at the status of the strip, and check the index and the device state
            #Device state: ON
            #== Plugs ==
            #* Socket 'Plug 1' state: ON on_since: 2022-01-26 12:17:41.423468
	        #* Socket 'Plug 2' state: OFF on_since: None
	        #* Socket 'Plug 3' state: OFF on_since: None
            result = self.performCommand("state", noArgs=True)
            state = result.split("state: ")
            powerState = []
            for line in state:
                if line[:2] == "ON":
                    powerState.append("ON")
                elif line[:3] == "OFF":
                    powerState.append("OFF")
            if len(powerState) != 0:
                self._log.debug(powerState)
                # Check if this strip is off
                if powerState[0] == "OFF":
                    self._is_on = False
                    self._log.debug("Device state: OFF")
                    return
                # Check if the this socket is off.
                if powerState[self.slotIndex+1] == "OFF":
                    self._is_on = False
                    self._log.debug("Slot state: OFF")
                else:
                    self._is_on = True
                    self._log.debug("Slot state: ON")
        else:
            result = self.performCommand("state")
            # | grep 'Device state' | cut -d ' ' -f 3
            if "Device state: False" in result:
                self._is_on = False
                self._log.debug("Device state: OFF")
            else:
                self._is_on = True
                self._log.debug("Device state: ON")

    def reboot(self):
        """
        Reboot the device.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        result = self.powerOff()
        if result == True:
            time.sleep(1)
            result = self.powerOn()
        return result

