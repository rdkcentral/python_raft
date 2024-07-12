#!/usr/bin/env python3

import sys
import os
import unittest

# Add the directory containing the framework package to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

from framework.core.singleton import Singleton, RAFTUnitTestCase

SINGLETON = Singleton(log=None)


class TestDecodeParams(RAFTUnitTestCase):
    
    def test_decodeParams(self):   
        print("Hello World")


if __name__ == "__main__":
   RAFTUnitTestCase.main()

