#!/usr/bin/env python3

import argparse
import sys
import argparse
import unittest
from framework.core.decodeParams import decodeParams


class Singleton:

    _instance = None
    __initialized = False

    def __new__(cls, log):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance._config = decodeParams(log)
        return cls._instance

    def __init__(self, log):
        if self.__initialized:
            return
        self.__initialized = True
        self.config = None
        self.deviceManager = None   
        self.params = decodeParams(log=None)   
        self.setup()

    def setup(self):
        deviceConfig = self.params.deviceConfig

        if deviceConfig:
            self.config = deviceConfig
          

    @property
    def config(self):
        # Return a copy if the config is mutable
        return self._config.copy() if isinstance(self._config, dict) else self._config

    @config.setter
    def config(self, config: dict):
        self._config = config
    

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

