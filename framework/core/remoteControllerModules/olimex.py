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

