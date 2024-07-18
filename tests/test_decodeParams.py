#!/usr/bin/env python3

import sys
import os
import unittest

# Add the directory containing the framework package to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

from framework.core.raftUnittest import RAFTUnitTestCase, RAFTUnitTestMain


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
        $ python tests/test_decodeParams.py --config examples/configs/getting_started_rack_config.yml --rack rack1 --slotName slot1 --loop 1
        
        Running the test with any of the following commands should fail:
        $ python tests/test_decodeParams.py --config examples/configs/getting_started_rack_config.yml
        $ python tests/test_decodeParams.py --config examples/configs/getting_started_rack_config.yml --rack rack2 --slotName slot3 --loop 1
        """
        
        params = self._singleton.params.args

        # Define the expected values
        expected_rack_name = "rack1"
        expected_slot_name = "slot1"
        expected_loop = "1"

        # Assert that the actual values match the expected values
        self.assertEqual(params.rackName, expected_rack_name, f"rackName does not match the expected value. Got: {params.rackName}")
        if params.rackName:
            print(f"rackName: {params.rackName}")
        else:
            self.fail("No rack name provided")

        self.assertEqual(params.slotName, expected_slot_name, f"slotName does not match the expected value. Got: {params.slotName}")
        if params.slotName:
            print(f"slotName: {params.slotName}")
        else:
            self.fail("No slot name provided")

        self.assertEqual(params.loop, expected_loop, f"loop does not match the expected value. Got: {params.loop}")
        if params.loop:
            print(f"loop: {params.loop}")
        else:
            self.fail("No loop provided")

if __name__ == "__main__":
   RAFTUnitTestMain()

