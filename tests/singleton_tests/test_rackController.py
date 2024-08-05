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
#*   ** @file        : test_decodeParams.py
#*   ** @date        : 31/07/20224
#*   **
#*   ** @brief : Tests the rackController is working correctly as part of the
#*   ** singlton.
#*   **
#*   ** The positive path for this test is to run it with the below arguments:
#*   ** --config examples/configs/getting_started_rack_config.yml
#* ******************************************************************************

import os
import sys

# Add the directory containing the framework package to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(path)

from framework.core.raftUnittest import RAFTUnitTestCase, RAFTUnitTestMain

class TestRackController(RAFTUnitTestCase):

    def setUp(self):
        self.rackController = self._singleton._rackController

    def test_number_racks(self):
        """
        Test the number of racks is the
        same as the expected number from the config.
        """
        expected_rack_count = 1
        self.assertEqual(len(self.rackController.racks),
                             expected_rack_count,
                             f"Expected 1 rack in rackController got: [{len(self.rackController.racks)}]")

    def test_rack_information(self):
        """
        Test the name and number of the slots is the
        same as the expected information from the config.
        """
        rack = self.rackController.racks[0]
        expected_name = 'rack1'
        expected_slot_count = 1
        self.assertEqual(expected_name,
                         rack.name,
                         f"Expected the rack name to be rack1. Got: {rack.name}")
        self.assertEqual(expected_slot_count,
                         len(rack.slot),
                         f"Expected one slot in rack1. Got {len(rack.slot)}")

    def test_raw_config(self):
        """
        Test that the config in the rack object is the
        same as the expected information from the config.
        """
        rack = self.rackController.racks[0]
        raw_config = rack.rawConfig
        expected_config = self._singleton.config.rackConfig.get('rack1')
        self.assertEqual(expected_config,
                         raw_config,
                         "Raw config of rack controller does not match expected rack config.")

    
    def test_slot_info(self):
        """
        Test that the slot information in the slot object is the
        same as the expected information from the config.
        """
        slot = self.rackController.racks[0].slot[0]
        rack_config = self._singleton.config.rackConfig.get('rack1')
        expected_config = rack_config.get('slot1')
        self.assertEqual(expected_config,
                         slot.config,
                         'Slot config for slot1 does not match expected config.')


if __name__ == "__main__":
    RAFTUnitTestMain()