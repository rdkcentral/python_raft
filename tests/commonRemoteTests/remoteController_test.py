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

import os
import sys

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../../")

from framework.core.rcCodes import rcCode as rc
from framework.core.logModule import logModule
from framework.core.testControl import testController

class demoClass(testController):
    pass

if __name__ == "__main__":
    # Olimex ESP32-EVB as a RC transmitter. Telnet operated.
    demo = demoClass( testName = "remoteDemo", level=logModule.INFO )
    demo.log.info("Testing Power On")
    demo.powerControl.powerOn()
    demo.utils.wait(1)
    demo.log.info("Testing Power Off")
    demo.powerControl.powerOff()
    demo.log.info("Testing remote LLAMA RC6")
    demo.commonRemote.setKeyMap("llama_rc6")
    demo.commonRemote.sendKey( rc.POWER )
    demo.commonRemote.sendKey( rc.MUTE )
    demo.commonRemote.sendKey( rc.MUTE )
    demo.commonRemote.sendKey( rc.VOL_DOWN )
    demo.commonRemote.sendKey( rc.VOL_UP )
    demo.commonRemote.setKeyMap("llama_tpv")
    demo.log.info("Testing remote LLAMA TPV")
    demo.commonRemote.sendKey( rc.MUTE )
    demo.commonRemote.sendKey( rc.MUTE )
    demo.commonRemote.sendKey( rc.CHANNEL_DOWN )
    demo.commonRemote.sendKey( rc.CHANNEL_UP )

