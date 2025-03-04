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

class sendAllKeysTest(testController):

    def __init__(self):
        super().__init__("commonRemote sendAllKeysTest", level=logModule.DEBUG)

    def testFunction(self):
        map_keys = list(self.commonRemote.remoteMap.currentMap.get("codes", {}).keys())
        for key in map_keys:
            self.log.stepStart(f"Testing key: [{key}]")
            code = rc[key]
            res = self.commonRemote.sendKey(code)
            self.log.stepResult(res, "Result of sendKey")

    def testEndFunction(self, powerOff=True):
        return super().testEndFunction(powerOff=False)



if __name__ == "__main__":
    sendAllKeysTest().run()