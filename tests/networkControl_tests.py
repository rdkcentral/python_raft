#!/usr/bin/env python3
#** *****************************************************************************
# *
# * If not stated otherwise in this file or this component's LICENSE file the
# * following copyright and licenses apply:
# *
# * Copyright 2026 RDK Management
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
sys.path.append(dir_path+"/../")

from framework.core.networkControl import networkControlClass
from framework.core.logModule import logModule

if __name__ == "__main__":
    log = logModule("networkControlTest")
    log.setLevel( log.INFO )

    # Network/wake controller straight from a `network:` config block
    config = { "type": "wol", "mac": "aa:bb:cc:dd:ee:ff" }
    control = networkControlClass( log, config )

    log.info("Testing wake")
    control.wake()

    log.info("Test complete")
