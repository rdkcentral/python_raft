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
#*   ** @file        : test_config_parsing.py
#*   ** @date        : 31/07/2024
#*   **
#*   ** @brief : Test the argument parsing that happens in decodeParams.py
#*   **
#*   ** The positive path for this test is to run it with the below arguments:
#*   ** --config examples/configs/getting_started_rack_config.yml
#*   ** --deviceConfig examples/configs/example_device_config.yml 
#*   ** --buildInfo info 
#*   ** --overrideDeviceConfig config 
#*   ** --rack rack1
#*   ** --slot 1 
#*   ** --slotName slot1 
#*   ** --job_id 1 
#*   ** --rack_job_execution 1 
#*   ** --loop 1 
#*   ** --test
#*   ** --debug
#* ******************************************************************************

import sys
import os
import unittest

# Add the directory containing the framework package to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(path)

from framework.core.singleton import SINGLETON

class TestArgumentParser(unittest.TestCase):
    """
    Test case for testing the argument parser in decodeParams
    """
    def setUp(self):
        self.params = SINGLETON.config.args

    def test_config_arg(self):
        """
        Test the --config option is parsed correctly.
        """
        expected_config = "examples/configs/getting_started_rack_config.yml"
        self.assertIn(expected_config, self.params.configFile, f"configFile does not match the expected value. Got: {self.params.configFile}")
    
    def test_device_config_arg(self):
        """
        Test the --deviceConfig option is parsed correctly.
        """
        expected_device_config = "examples/configs/example_device_config.yml"
        self.assertIn(expected_device_config, self.params.deviceConfigFile, f"deviceConfigFile does not match the expected value. Got: {self.params.deviceConfigFile}")

    def test_build_info_arg(self):
        """
        Test the --buildInfo option is parsed correctly.
        """
        expected_build_info = "info"
        self.assertEqual(self.params.buildInfo, expected_build_info, f"buildInfo does not match the expected value. Got: {self.params.buildInfo}" )

    def test_override_device_config_arg(self):
        """
        Test --overrideDeviceConfig option is parsed correctly.
        """
        expected_override_device_config = "config"
        self.assertEqual(self.params.overrideCpeConfig, expected_override_device_config, f"overrideCpeConfig does not match the expected value. Got: {self.params.overrideCpeConfig}" )

    def test_rack_arg(self):
        """
        Test --rack option is parsed correctly.
        """
        expected_rack_name = "rack1"
        self.assertEqual(self.params.rackName, expected_rack_name, f"rackName does not match the expected value. Got: {self.params.rackName}")

    def test_slot_arg(self):
        """
        Test --slot option is parsed corectly.
        """
        expected_slot = 1
        self.assertEqual(self.params.slotNumber, expected_slot, f"slotNumber does not match the expected value. Got: {self.params.slotNumber}")

    def test_slot_name_arg(self):
        """
        Test --slotName option is parsed correctly.
        """
        expected_slot_name = "slot1"
        self.assertEqual(self.params.slotName, expected_slot_name, f"slotName does not match the expected value. Got: {self.params.slotName}")

    def test_job_id_arg(self):
        """
        Test --jobId option is parsed correctly.
        """
        expected_job_id = "1"
        self.assertEqual(self.params.jobId, expected_job_id, f"jobId does not match the expected value. Got: {self.params.jobId}")

    def test_rack_job_execution_arg(self):
        """
        Test --rack_job_execution option is parsed correctly.
        """
        expected_rack_job_execution_id = "1"
        self.assertEqual(self.params.rackJobExecutionId, expected_rack_job_execution_id, f"rackJobExecutionId does not match the expected value. Got: {self.params.rackJobExecutionId}")

    def test_loop_arg(self):
        """
        Test --loop option is parsed correctly.
        """
        expected_loop = "1"
        self.assertEqual(self.params.loop, expected_loop, f"loop does not match the expected value. Got: {self.params.loop}")

    def test_testmode_arg(self):
        """
        Test --test option is parsed correctly.
        """
        self.assertTrue(self.params.testMode, f"testMode does not match the expected value. Got: {self.params.testMode}")

    def test_debug_arg(self):
        """
        Test --debug option is parsed correctly.
        """
        self.assertTrue(self.params.debug, f"debug does not match the expected value. Got: {self.params.testMode}")


if __name__ == "__main__":
   unittest.main(argv=[])

