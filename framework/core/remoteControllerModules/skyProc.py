#!/usr/bin/env python3
#** *****************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core.remoteControllerModules
#*   ** @date        : 22/11/2021
#*   **
#*   ** @brief : remote sky proc
#*   **
#* ******************************************************************************

import time
from framework.core.commandModules.telnetClass import telnet

class remoteSkyProc():
    
    def __init__( self, log, remoteController):
        self.log = log
        self.ip = remoteController["ip"]
        self.port = remoteController["port"]

    def command(self, cmd):
        self.telnet=telnet(self.log, '{}:{}'.format( self.ip, self.port ), None, None)
        if False==self.telnet.connect():
            return False
        self.telnet.read_very_eager()
        if False==self.telnet.write(cmd):
            return False
        if not b"(OK)" in self.telnet.read_until("(OK)"):
            return False
        self.telnet.disconnect()
        return True
  
    def sendKey(self, code, repeat, delay ):

        # Run the key sendKey via the terminal
        command="echo " + str(code) + " > /proc/cdi_ir"
        for _ in range(repeat):
            self.session.runTargetCommand(command, delay)
        return True