#!/usr/bin/env python3

import sys
import argparse
import unittest

from framework.core.singleton import Singleton
from framework.core.decodeParams import decodeParams


SINGLETON = Singleton(log=None)

class RAFTUnitTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deviceManager = SINGLETON.deviceManager

    def main():    
        parser = argparse.ArgumentParser(description="Run RAFT unit tests.")
        parser.add_argument('--config', type=str, help='Path to the configuration file')
        args, remaining_args = parser.parse_known_args()

        if args.config:
            print(f"Using config file: {args.config}")
            # Load and set the configuration in the singleton
            singleton_instance = Singleton(args.config)
            singleton_instance.config = decodeParams(args.config)

        # Run unit tests 
        unittest.main(argv=[sys.argv[0]] + remaining_args, exit=False)


class RAFTUnitTestMain(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deviceManager = SINGLETON.deviceManager
