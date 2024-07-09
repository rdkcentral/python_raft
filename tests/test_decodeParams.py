#!/usr/bin/env python3

import sys
import os
import unittest
import argparse

# Add the directory containing the framework package to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

from framework.core.singleton import Singleton, RAFTUnitTestCase

singleton = Singleton(log=None)


class TestDecodeParams(RAFTUnitTestCase):
    
    def test_decodeParams(self):   
        print("Hello World")

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

