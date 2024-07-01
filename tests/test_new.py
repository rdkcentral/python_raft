#!/usr/bin/env python3

import sys
import os
import unittest
import argparse

# Add the directory containing the framework package to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

print("Here_0, sys.path:", sys.path)

from framework.core.decodeParams import decodeParams
from framework.core.deviceManager import deviceManager
from framework.core.deviceController import deviceController

from framework.core.singleton_module import Singleton

singleton = Singleton()

class RAFTUnitTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raft = singleton
        print("Here_1, Config:", self.raft.get_config())


# ERROR: module() takes at most 2 arguments (3 given) 
# The error you're encountering is because you are attempting to subclass unittest directly, 
# but unittest is a module, not a class. You should be subclassing unittest.TestCase instead.
class RAFTUnitTestMain(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raft = singleton
        print("Here_2, Config:", self.raft.get_config())

class TestNew(RAFTUnitTestCase):
    
    def test_new(self):   
        print("Here_3")
        self.dut = deviceController()
        self.dut.powerOn()
        self.assertTrue(deviceController.power)


def main():
    parser = argparse.ArgumentParser(description="Run RAFT unit tests.")
    parser.add_argument('--config', type=str, help='Path to the configuration file')
    args, remaining_args = parser.parse_known_args()

    if args.config:
        print(f"Using config file: {args.config}")
        # Load and set the configuration in the singleton
        singleton.set_config(args.config)
        # Load and process the config file if needed

    # Run unit tests
    unittest.main(argv=[sys.argv[0]] + remaining_args, exit=False)

if __name__ == "__main__":
    main()


