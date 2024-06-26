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