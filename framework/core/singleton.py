#!/usr/bin/env python3

import sys
import argparse

from framework.core.decodeParams import decodeParams


class Singleton:

    _instance = None
    __initialized = False

    def __new__(cls, log):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._params = decodeParams(log)
                    
        return cls._instance

    def __init__(self, log):
        if self.__initialized:
            return
        self.__initialized = True
        self.config = None
        self.deviceManager = None   
        self.params = self._instance._params  
        

    @property
    def config(self):
        # Return a copy if the config is mutable
        return self._config.copy() if isinstance(self._config, dict) else self._config

    @config.setter
    def config(self, config: dict):
        self._config = config
    

SINGLETON = Singleton(log=None)
