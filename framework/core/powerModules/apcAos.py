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
        self.hostName = hostName
        self.userName = userName
        self.password = password
        self.port = port
        self.outletNumber = outletNumber
        self.log = log
        self.telnet = None

    def open(self):
        self.telnet = telnet(self.log, "", self.hostName, self.userName, self.password, self.port)
        self.telnet.connect("User Name :", "Password  :")
        self.waitForPrompt()

    def close(self):
        self.telnet.disconnect()

    def waitForPrompt(self):
        data = self.telnet.read_until(CMD_PROMPT)
        self.log.info(data)

    def sendCommand(self, cmd):
        self.open()
        self.telnet.write(cmd)
        self.waitForPrompt()
        self.close()

    def powerOn(self):
        self.log.debug("powerApcAos().powerOn")
        self.sendCommand(POWER_ON + " " + str(self.outletNumber))
        return True

    def powerOff(self):
        self.log.debug("powerApcAos().powerOff")
        self.sendCommand(POWER_OFF + " " + str(self.outletNumber))
        return True
        
    def reboot(self):
        result = self.powerOff()
        if result != True:
            self.log.error(" Power Failed off")
        time.sleep(1)
        result = self.powerOn()
        if result != True:
            self.log.error(" Power Failed on")
        return result
