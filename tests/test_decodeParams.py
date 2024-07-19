#!/usr/bin/env python3

import sys
import os
import unittest

# Add the directory containing the framework package to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

from framework.core.raftUnittest import RAFTUnitTestCase, RAFTUnitTestSuite, RAFTUnitTestMain


class TestDecodeParams(RAFTUnitTestCase):
    """
    Test suite for verifying the decodeParams function.
    """
    

    def test_decodeParams(self):   
        
        """
        Test the decodeParams function to ensure that it correctly parses 
        and returns the expected parameters.
        
        This test verifies that:
        - The rackName parameter matches the expected value.
        - The slotName parameter matches the expected value.
        - The loop parameter matches the expected value.
        

        Running the test with the following command should pass:
        $ python tests/test_decodeParams.py \
            --config examples/configs/getting_started_rack_config.yml \
            --deviceConfig examples/configs/getting_started_rack_config.yml \
            --buildInfo info \
            --overrideDeviceConfig config \
            --rack rack1 \
            --slot 1 \
            --slotName slot1 \
            --job_id 1 \
            --rack_job_execution 1 \
            --loop 1
        
        Running the test with any of the following commands should fail:
        $ python tests/test_decodeParams.py \
            --config examples/configs/getting_started_rack_config.yml
        
        $ python tests/test_decodeParams.py \
            --config examples/configs/getting_started_rack_config.yml \
            --deviceConfig examples/configs/getting_started_rack_config.yml \
            --buildInfo info \
            --overrideDeviceConfig config \
            --rack rack2 \
            --slot 2 \
            --slotName slot2 \
            --job_id 2 \
            --rack_job_execution 2 \
            --loop 2
        """
        
        params = self._singleton.params.args

        # Define the expected values
        expected_config = "examples/configs/getting_started_rack_config.yml"
        expected_device_config = "examples/configs/getting_started_rack_config.yml"
        expected_build_info = "info"
        expected_override_device_config = "config"
        expected_rack_name = "rack1"
        expected_slot = 1
        expected_slot_name = "slot1"
        expected_job_id = "1"
        expected_rack_job_execution_id = "1"
        expected_loop = "1"

        # Assert that the actual values match the expected values
        self.assertIn(expected_config, params.configFile, f"configFile does not match the expected value. Got: {params.configFile}")
        self.assertIn(expected_device_config, params.deviceConfigFile, f"deviceConfigFile does not match the expected value. Got: {params.deviceConfigFile}")
        self.assertEqual(params.buildInfo, expected_build_info, f"buildInfo does not match the expected value. Got: {params.buildInfo}" )
        self.assertEqual(params.overrideCpeConfig, expected_override_device_config, f"overrideCpeConfig does not match the expected value. Got: {params.overrideCpeConfig}" )
        self.assertEqual(params.rackName, expected_rack_name, f"rackName does not match the expected value. Got: {params.rackName}")
        self.assertEqual(params.slotNumber, expected_slot, f"slotNumber does not match the expected value. Got: {params.slotNumber}")
        self.assertEqual(params.slotName, expected_slot_name, f"slotName does not match the expected value. Got: {params.slotName}")
        self.assertEqual(params.jobId, expected_job_id, f"jobId does not match the expected value. Got: {params.jobId}")
        self.assertEqual(params.rackJobExecutionId, expected_rack_job_execution_id, f"rackJobExecutionId does not match the expected value. Got: {params.rackJobExecutionId}")
        self.assertEqual(params.loop, expected_loop, f"loop does not match the expected value. Got: {params.loop}")
             
        
if __name__ == "__main__":
   
   testSuite = RAFTUnitTestSuite()
   testSuite.addTest(unittest.makeSuite(TestDecodeParams))

   RAFTUnitTestMain()

