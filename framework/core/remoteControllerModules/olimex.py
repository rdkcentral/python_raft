#!/usr/bin/env python3
#** *****************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core.remoteControllerModules
#*   ** @date        : 22/11/2021
#*   **
#*   ** @brief : remote Olimex
#*   **
#* ******************************************************************************

import time
from framework.core.rcCodes import rcCode as rc
from framework.core.logModule import logModule
from framework.core.commandModules.telnetClass import telnet
import framework.core

class remoteOlimex():

    def __init__( self, log:logModule, remoteController:dict ):
        self.log = log
        self.remoteController = remoteController

    def command(self, cmd:str):
        self.telnet=telnet(self.log, '{}:{}'.format( self.remoteController["ip"], self.remoteController["port"] ), None, None)
        if False==self.telnet.connect():
            return False
        self.telnet.read_very_eager()
        if False==self.telnet.write(cmd):
            return False
        if not b"(OK)" in self.telnet.read_until("(OK)"):
            return False
        self.telnet.disconnect()
        return True
    
    def sendKey(self, code:str, repeat:int, delay:int ):
        if code == None:
            return False

        for _ in range(repeat):
            if True != self.command('{}\n'.format( code )):
                self.log.error("sendKey(), Command [{}] failed.".format( code ) )
                return False
            time.sleep( delay )
            
        return True

