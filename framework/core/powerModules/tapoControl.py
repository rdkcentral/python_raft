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
#*   ** @date        : 14/01/2025
#*   **
#*   ** @brief : Power On and Off TAPO power switches
#*   **
#
# https://github.com/python-kasa/python-kasa
# # Supported Kasa devices
#     Plugs: EP10, EP251, HS1002, HS103, HS105, HS110, KP100, KP105, KP115, KP125, KP125M1, KP401
#     Power Strips: EP40, EP40M1, HS107, HS300, KP200, KP303, KP400
#     Wall Switches: ES20M, HS2002, HS210, HS2202, KP405, KS200, KS200M, KS2051, KS220, KS220M, KS2251, KS230, KS2401
# Supported Tapo1 devices
#     Plugs: P100, P110, P110M, P115, P125M, P135, TP15
#     Power Strips: P210M, P300, P304M, P306, TP25
#     Wall Switches: S210, S220, S500D, S505, S505D
#
# TODO: Had issues with calling the python library directly it has comms errors
# To get round this issue and to get this in, since kasa command line tool works
# Swap the interface to use that instead
# This implementation is a hack to get TAPO support.
# The kasaControl should be reimplemented to support both Kasa and TAPO
#* ******************************************************************************

import json
import re
import subprocess
import time

from framework.core.logModule import logModule
from framework.core.powerModules.abstractPowerModule import PowerModuleInterface

class powerTapo(PowerModuleInterface):
    
    """Tapo power switch controller supports
    """
    
    def __init__( self, log:logModule, ip:str, outlet:str = None, **kwargs ):
        """
        Tapo module based on kasa library.
        TODO: Reintegrate this with the powerKasa module.

        Args:
            log ([logModule]): [log module]
            ip ([str]): [ip]
            outlet ([int], optional): Outlet number for power strips. Defaults to None.
            kwargs ([dict]): [any other args]
        """
        super().__init__(log)
        self._is_on = False
        self._outlet = None
        self.ip = ip
        self._username = kwargs.get("username", None)
        self._password = kwargs.get("password", None)
        if outlet:
            self._outlet=str(outlet)
        self._device_type = None
        self._encryption_type = None
        self._discover_device()
        self._get_state()

    def _performCommand(self, command, json = False, append_args:list = []):
        """
        Perform a command.

        Args:
            command (str): The command to execute.
            json (bool): Add the --json option to the command.
                         Retrieves the data in json string format.
                         Default is False.
            append_args (list): Extra arguments to add on the end of the command.
                                Defaults to an empty list.
        Returns:
            str: The command output.
        """
        command_list = ["kasa", "--host", self.ip]
        if json:
            command_list.append("--json")
        if self._username:
            command_list.append("--username")
            command_list.append(self._username)
        if self._password:
            command_list.append("--password")
            command_list.append(self._password)
        if self._device_type != "UNKNOWN" and self._encryption_type:
            command_list.append("--device-family")
            command_list.append(self._device_type)
            command_list.append("--encrypt-type")
            command_list.append(self._encryption_type)
        else:
            if self._outlet:
                command_list.append("--type")
                command_list.append("strip")
            else:
                command_list.append("--type")
                command_list.append("plug")
        command_list.append(command)
        for arg in append_args:
            command_list.append(arg)
        self._log.debug( "Command: {}".format(" ".join(command_list)))
        data = subprocess.run(command_list, stdout=subprocess.PIPE, text=True)
        self._log.debug(data.stdout)
        return data.stdout

    def powerOff(self):
        """
        Turn off the device.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        self._get_state()
        if self.is_off:
            return True
        if self._outlet:
            self._performCommand("off", append_args=["--index", str(self._outlet)])
        else:
            self._performCommand("off")
        self._get_state()
        if self.is_off == False:
            self._log.error(" Power Off Failed")
        return self.is_off

    def powerOn(self):
        """
        Turn on the device.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        self._get_state()
        if self.is_on:
            return True
        if self._outlet:
            self._performCommand("on", append_args=["--index", str(self._outlet)])
        self._performCommand("on")
        self._get_state()
        if self.is_on == False:
            self._log.error(" Power On Failed")    
        return self.is_on

    def _get_state(self):
        """Get the state of the device.
        """
        result = self._performCommand("state")
        if self._outlet:
            # We have a strip look at the status of the strip, and check the index and the device state
            #Device state: ON
            #== Plugs ==
            #* Socket 'Plug 1' state: ON on_since: 2022-01-26 12:17:41.423468
	        #* Socket 'Plug 2' state: OFF on_since: None
	        #* Socket 'Plug 3' state: OFF on_since: None
            result = self._performCommand("state", noArgs=True)
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
            # | grep 'Device state' | cut -d ' ' -f 3
            if "Device state: False" in result:
                self._is_on = False
                self._log.debug("Device state: OFF")
            else:
                self._is_on = True
                self._log.debug("Device state: ON")


    def _discover_device(self):
        command = ["kasa", "--json", "--target", str(self.ip)]
        if self._username:
            command.append("--username")
            command.append(self._username)
        if self._password:
            command.append("--password")
            command.append(self._password)
        command.append("discover")
        result = subprocess.run(command,
                                stdout=subprocess.PIPE,
                                check=True,
                                text=True)
        result = json.loads(result.stdout)
        if result.get(self.ip):
            result = result.get(self.ip)
        else:
            self._device_type = "UNKNOWN"

        if result.get("info"):
            info = result.get("info")
            self._device_type = info.get("type", "UNKNOWN")
        elif result.get("system"):
            system = result.get("system")
            if info:=system.get("get_sysinfo"):
                self._device_type = info.get("mic_type", "UNKNOWN")
            else:
                self._device_type = "UNKNOWN"
        else:
            self._device_type = "UNKNOWN"
        self._encryption_type = self._get_encryption_type()

    def _get_encryption_type(self):
        command = ["kasa", "--target", self.ip, "discover"]
        result = subprocess.run(command,
                                check=True,
                                stdout=subprocess.PIPE,
                                text=True)
        found = re.search(r"Encrypt Type:\s+(.*)$", result.stdout,re.M)
        if found:
            return found.group(1)
        return None

    def getPowerLevel(self):
        if self._outlet:
            # TODO: implement this for a powerstrip
            # result = self._performCommand("emeter",
            #                               json=True,
            #                               append_args=["--index", str(self._outlet)])
            raise RuntimeError("Power monitoring is not yet supported for Tapo strips")
        else:
            result = self._performCommand("emeter", json=True)
            result = json.loads(result)
            millewatt = result.get('power_mw')
            if millewatt:
                power = int(millewatt) / 1000
                return power
            raise KeyError("The dictionary return for the Tapo device did is not formed as expected.")
