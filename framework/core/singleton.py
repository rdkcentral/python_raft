#!/usr/bin/env python3

import argparse
import sys
import unittest
from framework.core.decodeParams import decodeParams
from framework.core.deviceManager import deviceManager


class Singleton:

    _instance = None
    __initialized = False

    def __new__(cls, log):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.config = decodeParams(log)
        return cls._instance

    def __init__(self, log):
        if self.__initialized:
            return
        self.__initialized = True
        self.config = None
        self.deviceManager = None
        self.setup()

    def setup(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', type=str, help='Path to the configuration file')
        args, remaining_args = parser.parse_known_args()

        if args.config:
            self.set_config(args.config)
            self.config = decodeParams.decodeConfigIntoDictionary(self, self.config) # ---- need to get the device not the whole config
        #     self.config.devices.get("dut") ###

        # self.deviceManager = deviceManager(self.config, log=None)
        # if self.deviceManager:
        #     print("deviceManager initialised succesfully")
        # else:
        #     print("failed to initialise deviceManager")

    def set_config(self, config):
        self.config = config

    def get_config(self):
        return self.config
    
    # def get_config(self):
    #     return self._instance.config


singleton = Singleton(log=None)

class RAFTUnitTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deviceManager = singleton.deviceManager
        # print("Here_1, Config:", self.deviceManager.get_config())


class RAFTUnitTestMain(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deviceManager = singleton.deviceManager
        # print("Here_2, Config:", self.raft.get_config())

