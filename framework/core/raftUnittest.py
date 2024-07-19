#!/usr/bin/env python3

import os
import sys
import unittest

# Add the directory containing the framework package to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

from framework.core.singleton import SINGLETON

class RAFTUnitTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self._singleton = SINGLETON
        super().__init__(*args, **kwargs)        


class RAFTUnitTestSuite(unittest.TestSuite):
    def __init__(self, tests=()):
        self._singleton = SINGLETON
        super().__init__(tests)
    

def RAFTUnitTestMain():

    print(f"Using config file: {SINGLETON.params.deviceConfig}\n")
    
    unittest.main(argv=[sys.argv[0]], exit=False)