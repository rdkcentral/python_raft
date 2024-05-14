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
#*   ** @brief : remote none
#*   **
#* ******************************************************************************

import time
from framework.core.logModule import logModule

class remoteNone():
    
    def __init__( self, log:logModule, remoteConfig:dict):
        """Initalise a remoteNone class

        Args:
            log (logModule): logging module
            remoteConfig (dict): remote controller configuration
        """
        self.log = log
  
    def sendKey(self, code:str, repeat:int, delay:int ):
        """Send a key

        Args:
            code (str): keycode
            repeat (int): number of repeats required
            delay (int): delay in seconds between repeats

        Returns:
            bool: true on success otherwise failure
        """
        if code == None:
            return False

        for _ in range(repeat):
            self.log.info("remoteNone: sendKey( code=[{}] repeat=[{}] delay=[{}] )".format( code, repeat, delay ) )
            time.sleep( delay )

        return True