#! /bin/python3
#/* *****************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core.powerModules
#*   ** @date        : 08/03/2022
#*   **
#*   ** @brief : wrapper for apcAos power
#*   **
#* *****************************************************************************

import time
from framework.core.commandModules.telnetClass import telnet

CMD_PROMPT = "apc>"
POWER_ON = "olOn"
POWER_OFF = "olOff"
REBOOT = "olReboot"
REBOOT_WAIT = 60

class powerApcAos():
    
    """Power Control module for the APC power switches
    """

    def __init__(self, log, hostName, userName, password, port=23, outletNumber=1):
        """
        Initialize the powerAPCAOS object.

        Args:
            log: Logger object for logging messages.
            hostName (str): Hostname or IP address of the APC power switch.
            userName (str): Username for accessing the APC power switch.
            password (str): Password for accessing the APC power switch.
            port (int): Port number for the Telnet connection (default is 23).
            outletNumber (int): Outlet number to control (default is 1).
        """
        self.hostName = hostName
        self.userName = userName
        self.password = password
        self.port = port
        self.outletNumber = outletNumber
        self.log = log
        self.telnet = None

    def open(self):
        """Open a Telnet connection to the APC power switch.
        """
        self.telnet = telnet(self.log, "", self.hostName, self.userName, self.password, self.port)
        self.telnet.connect("User Name :", "Password  :")
        self.waitForPrompt()

    def close(self):
        """Close the Telnet connection to the APC power switch.
        """
        self.telnet.disconnect()

    def waitForPrompt(self):
        """Wait for the command prompt from the APC power switch.
        """
        data = self.telnet.read_until(CMD_PROMPT)
        self.log.info(data)

    def sendCommand(self, cmd):
        """
        Send a command to the APC power switch.

        Args:
            cmd (str): Command to send.
        """
        self.open()
        self.telnet.write(cmd)
        self.waitForPrompt()
        self.close()

    def powerOn(self):
        """
        Turn on the outlet specified by the outletNumber.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        self.log.debug("powerApcAos().powerOn")
        self.sendCommand(POWER_ON + " " + str(self.outletNumber))
        return True

    def powerOff(self):
        """
        Turn off the outlet specified by the outletNumber.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        self.log.debug("powerApcAos().powerOff")
        self.sendCommand(POWER_OFF + " " + str(self.outletNumber))
        return True
        
    def reboot(self):
        """
        Reboot the outlet specified by the outletNumber.

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
