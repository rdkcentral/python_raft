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
#*   ** @date        : 20/11/2021
#*   **
#*   ** @brief : wrapper for telnet
#*   **
#* *****************************************************************************


import time
from framework.core.commandModules.telnetClass import telnet
import re

CONNECT_MSG = "Communication Established"
POWER_ON = "1"
POWER_OFF = "2"
REBOOT = "3"
REBOOT_WAIT = 60

class powerAPC():
    
    """Power Control module for the APC power switches
    """

    def __init__(self, log, hostName, userName, password, outletNumber=1):
        """
        Initializes the PDU Controller class.

        Args:
            log (logging object): A logging object used for logging messages.
            hostName (str): The hostname or IP address of the PDU.
            userName (str): The username for the PDU web interface.
            password (str): The password for the PDU web interface.
            outletNumber (int, optional): The outlet number on the PDU. Defaults to 1.
        """
        self.hostName = hostName
        self.userName = userName
        self.password = password
        self.outletNumber = outletNumber
        self.log = log
        self.telnet = None

    def pduPowerSetting(self, powerMode):
        """
        Control the power mode of the outlet.

        Args:
            powerMode (str): The desired power mode ('POWER_ON', 'POWER_OFF', or 'REBOOT').

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        if not self.open():
            self.log.error("Unable to open PDU")
            return False

        if not self.configurePDU():
            self.log.error("Unable to configure PDU")
            return False

        self.selectPDUOutlet(self.outletNumber)

        if POWER_ON == powerMode:
            self.log.info("Powering ON the device")
            self.sendPowerON()
        elif POWER_OFF == powerMode:
            self.log.info("Powering OFF the device")
            self.sendPowerOFF()
        elif REBOOT == powerMode:
            self.log.info("Rebooting the device")
            self.sendPowerOFF()
            time.sleep(REBOOT_WAIT)
            self.sendPowerON()
        else:
            self.log.info("Invalid Power Mode")
            return False

        self.close()
        return True

    def checkConnection(self):
        """
        Check the connection status with the APC power switch.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        self.log.info("Checking for " + CONNECT_MSG)
        data = self.telnet.read_until(CONNECT_MSG)
        if re.search(CONNECT_MSG, data, re.IGNORECASE):
            return True
        else:
            self.log.error(str(data))
            return False

    def open(self):
        """
        Open a Telnet connection to the APC power switch.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        self.telnet = telnet(self.log, "", self.hostName, self.userName, self.password)
        self.telnet.connect(username_prompt="User Name :", password_prompt="Password  :")

        if self.checkConnection():
            self.log.info("Successfully connected to PDU")
            return True

        self.log.error("Failed to connect PDU")
        return False

    def close(self):
        """Close a Telnet connection to the APC power switch.
        """
        # Keeping sending ECS make us reach top directory
        self.telnet.write(chr(27))
        self.telnet.write(chr(27))
        self.telnet.write(chr(27))
        self.telnet.write(chr(27))
        self.telnet.write(chr(27))

        self.telnet.read_very_eager()
        self.telnet.write("4")
        self.telnet.read_some()
        self.telnet.write("")
        self.log.info("Disconnected from PDU")

    def waitAPCNextline(self):
        """Wait for the next line from the APC power switch.
        """
        data = self.telnet.read_until('> ')
        self.log.debug(data)
        self.telnet.read_eager()

    def configurePDU(self):
        """Configure the APC power switch for outlet control.
        """
        self.log.info("configuring PDU")
        data = self.telnet.read_until('Console')
        if not re.search("Console", data, re.IGNORECASE):
            self.log.info('Failed to configure PDU')
            self.close()
            return False

        self.log.info("PDU Control Console")
        self.waitAPCNextline()
        self.log.info('Opening Device Manager')
        self.telnet.write("1")
        self.waitAPCNextline()
        self.log.info('Opening Outlet Management')
        self.telnet.write("2")
        self.waitAPCNextline()
        self.log.info('Entering Outlet Control')
        self.telnet.write("1")
        self.waitAPCNextline()
        return True

    def selectPDUOutlet(self, outletNumber):
        """
        Select the outlet number on the APC power switch.

        Args:
            outletNumber (int): The number of the outlet to select.
        """
        outletNumber = str(outletNumber)
        self.log.info("Selecting outlet : " + outletNumber)
        self.telnet.write(outletNumber)
        self.telnet.read_until(outletNumber)
        self.waitAPCNextline()

    def sendPowerON(self):
        """Send the command to power ON the selected outlet.
        """
        self.telnet.write(POWER_ON)
        self.log.debug(self.telnet.read_until("Immediate On"))
        self.log.info('Immediate On')
        # Read expected message from AP
        self.log.debug(self.telnet.read_until('cancel'))
        # Type YES
        self.telnet.write("YES")
        self.log.info("Turned ON the STB")
        self.telnet.read_some()
        self.telnet.write("")

    def sendPowerOFF(self):
        """Send the command to power OFF the selected outlet.
        """
        self.telnet.write(POWER_OFF)
        self.log.debug(self.telnet.read_until("Immediate Off"))
        self.log.info("Immediate Off")
        # Read expected message from AP
        self.log.debug(self.telnet.read_until('cancel'))
        # Type YES
        self.telnet.write("YES")
        self.log.info("Turned OFF the STB")
        self.telnet.read_some()
        self.telnet.write("")

    def powerOff(self):
        """
        Power OFF the device connected to the outlet.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        result = self.pduPowerSetting(POWER_OFF)
        return result

    def powerOn(self):
        """
        Power ON the device connected to the outlet.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        result = self.pduPowerSetting(POWER_ON)
        return result

    def reboot(self):
        """
        Reboot the device connected to the outlet.

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
