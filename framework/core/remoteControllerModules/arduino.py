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
#*   ** @date        : 25/02/2022
#*   **
#*   ** @brief : remote arduino uno IR transmitter
#*   **
#* ******************************************************************************

import time
import serial

from framework.core.logModule import logModule

class remoteArduino():

    def __init__( self, log:logModule, remoteConfig:dict() ):
        """intialise the arduino module

        Args:
            log (logModule): log class
            remoteConfig (dict): remote configuration
        """
        self.log = log
        self.remoteConfig = remoteConfig
        self.arduino = serial.Serial(port=self.remoteConfig.get("port"), baudrate=self.remoteConfig.get("baudrate"), timeout=300)
        self.firstKeyPressInTc = True

    def sendKey(self, key, repeat=1, delay=1):
        """Send IR key using arduino module

        Args:
            key (str) - Key to be sent to device#
            repeat (int) - Number of times the key has to be pressed. Defaults to 1
            delay (int) - wait time after pressing the key
        """
        if self.firstKeyPressInTc:
            time.sleep(5)
            self.firstKeyPressInTc = False

        for _ in range(repeat):
            self.arduino.write(key.encode())
            time.sleep(delay)
        return True
