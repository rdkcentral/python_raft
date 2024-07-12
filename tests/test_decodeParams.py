#!/usr/bin/env python3

import sys
import os
import unittest

# Add the directory containing the framework package to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

from framework.core.singleton import Singleton
from framework.core.raftUnittest import RAFTUnitTestCase

SINGLETON = Singleton(log=None)


class TestDecodeParams(RAFTUnitTestCase):
    
    def test_decodeParams(self):   
        print("Hello World")
        
        params = SINGLETON.params.args
        
        if params.rackName:
            print(params.rackName)
        else:
            print("No rack name provided")

        if params.slotName:
            print(params.slotName)
        else:
            print("No slot name provided")

        if params.loop:
            print(params.loop)
        else:
            print("No loop provided")


if __name__ == "__main__":
   RAFTUnitTestCase.main()

