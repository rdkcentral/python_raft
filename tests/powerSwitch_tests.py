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
sys.path.append(dir_path+"/../")

from framework.core.powerControl import powerControlClass
from framework.core.rackController import rackController
from framework.core.logModule import logModule
from framework.core.utilities import utilities
from framework.core.decodeParams import decodeParams
from framework.core.deviceManager import deviceManager

if __name__ == "__main__":
    # Read configuration file, and run power switch test based on that
    log = logModule("powerSwitchTest")
    log.setLevel( log.INFO )

    utils = utilities( log )

    config = decodeParams(log)
    rackControl = rackController( config.rackConfig )

    # Just choose rack 0, slot 0
    rack = rackControl.getRackByIndex( 0 )
    if config.args.slotNumber != None:
        slot = rack.getSlot(config.args.slotNumber )
    else:
        slot = rack.getSlot(1)

    devices = deviceManager( slot.config.get("devices"), log, "./logs" )
    dut = devices.getDevice("dut")
    power = dut.powerControl

    log.info("Testing Power on")
    power.powerOn()

    utils.wait(5)

    log.info("Testing Power ON Reboot")
    power.reboot()

    utils.wait(5)

    log.info("Testing Power Off")
    power.powerOff()

    utils.wait(5)

    log.info("Testing Power Off Reboot")
    power.reboot()

    utils.wait(5)

    log.info("Testing Power Off")
    power.powerOff()

    log.info("Test complete")

