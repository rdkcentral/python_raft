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
#*   ** @addtogroup  : tests
#*   ** @file        : test_deviceManager.py
#*   ** @date        : 07/08/20224
#*   **
#*   ** @brief : Tests the decodeManager class as part of the singleton.
#*   **
#*   ** The positive path for this test is to run it with the below arguments:
#*   ** --config examples/configs/getting_started_rack_config.yml
#* ******************************************************************************
import os
import sys

try:
    from yaml import load, SafeLoader as Loader
except:
    from yaml import load, CLoader as Loader

# Add the directory containing the framework package to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(path)

from framework.core.raftUnittest import RAFTUnitTestCase, RAFTUnitTestMain
from framework.core.commandModules.consoleInterface import consoleInterface

class TestDeviceManager(RAFTUnitTestCase):

    def test_devicesList(self):
        """
        Test the list of devices set up in the device manager is correct.
        """
        device_list = list(self.devices.devices.keys())
        expected_device_list_dicts = self._singleton.slotInfo.config.get('devices',[])
        expected_device_list = []
        for device_dict in expected_device_list_dicts:
            expected_device_list += device_dict.keys()
        self.assertEqual(expected_device_list, device_list,f'Expected to find dut in device list. Device list contains: [{", ".join(device_list)}]')

    def test_DUTInfo(self):
        """
        Test the information of the dut in the slot is correct.
        """
        expectedName = 'dut'
        self.assertEqual(self.dut.deviceName, expectedName, f'Expected device name to be {expectedName}. Got [{self.dut.deviceName}]')
        expectedConfig = self._singleton.slotInfo.config.get('devices',[{'dut':{}}])[0]
        self.assertEqual(expectedConfig, self.dut.rawConfig, 'DUT device config does not match expected config.')

    def test_getSessionForDUT(self):
        """
        Test the console session for the dut has been instantiated.
        """
        session = self.dut.getConsoleSession()
        self.assertIsInstance(session,consoleInterface)


if __name__ == '__main__':
    RAFTUnitTestMain()