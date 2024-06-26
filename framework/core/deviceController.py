#!/usr/bin/env python3
#** ******************************************************************************
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
#*   ** @addtogroup  : core
#*   ** @file        : testControl.py
#*   ** @brief : Test Control Module for running rack Testing
#*   **
#* ******************************************************************************
# System
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


framework_path = '/home/FKC01/python_raft/framework/core'
sys.path.append(framework_path)


from framework.core.rackController import rackController
from framework.core.configParser import configParser
from framework.core.utilities import utilities
from framework.core.decodeParams import decodeParams
from framework.core.capture import capture
from framework.core.webpageController import webpageController
from framework.core.deviceManager import deviceManager

class deviceController():

    def __init__(self):
        
        self.devices = deviceManager(self.slotInfo.config.get("devices"), self.log, self.testLogPath)
        self.dut = self.devices.getDevice( "dut" )
        self.session = self.dut.getConsoleSession()
        self.powerControl = self.dut.powerControl

    
    def powerOn(self):
        self.powerControl.powerOn()
    