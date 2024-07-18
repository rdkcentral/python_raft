#!/usr/bin/env python3

import sys
import unittest

from framework.core.singleton import SINGLETON
from framework.core.decodeParams import decodeParams


class RAFTUnitTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self._singleton = SINGLETON
        super().__init__(*args, **kwargs)        

def RAFTUnitTestMain():

    if SINGLETON.config:
        print(f"Using config file: {SINGLETON.config}\n")
    
    unittest.main(argv=[sys.argv[0]], exit=False)
    