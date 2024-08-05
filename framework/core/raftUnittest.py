#!/usr/bin/env python3
#** ******************************************************************************
# *
# * If not stated otherwise in this file or this component's LICENSE file the
# * following copyright and licenses apply:
# *
# * Copyright 2023 RDK Management
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *
# http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core
#*   ** @file        : raftUnittest.py
#*   ** @date        : 05/08/2024
#*   **
#*   ** @brief : RAFTUnitTestCase class, RAFTUnitTestSuite class 
#*   **          and RAFTUnitTestMain function .
#*   **
#* ******************************************************************************

import os
import sys
import unittest

# Add the directory containing the framework package to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

from framework.core.singleton import SINGLETON
from framework.core.logModule import logModule

class RAFTUnitTestCase(unittest.TestCase):
    """
    A custom unittest.TestCase subclass for RAFT framework.

    This class provides a base for test cases within the RAFT framework. It initializes
    a singleton instance and sets up summary logging for the test case. Verbosity
    can be accessed and set through properties.

    Attributes:
        testName (str): The name of the test class.
        qcId (str): The quality center ID.
        verbosity (int): The verbosity level for test output.

    Args:
        *args: Arguments passed to the base class.
        **kwargs: Keyword arguments passed to the base class.
            - qcId (str, optional): The quality center ID. Defaults to ''.
    """

    def __init__(self, *args, **kwargs):
        """Initializes the test case."""
        self._singleton = SINGLETON
        self.testName = self.__class__.__name__
        self.qcId = kwargs.get('qcId', '')
        self._singleton.setSummaryLog(self.testName, self.qcId)
        super().__init__(*args, **kwargs)

    @property
    def verbosity(self):
        return self._singleton.getVerbosity()

    @verbosity.setter
    def verbosity(self, verbosity:int):
        self._singleton.setVerbosity(verbosity)


class RAFTUnitTestSuite(unittest.TestSuite):
    """
    A custom unittest.TestSuite subclass for RAFT framework.

    This class provides a base for test suites within the RAFT framework. It initializes
    a singleton instance and sets up summary logging for the test suite. Verbosity
    can be accessed and set through properties.

    Attributes:
        verbosity (int): The verbosity level for test output.
    Args:
        testName (str): The name of the test suite.
        tests (tuple, optional): A sequence of test cases to add. Defaults to an empty tuple.
    """
    def __init__(self, testName:str , tests=()):
        """Initializes the test suite."""
        self._singleton = SINGLETON
        self._testName = testName
        self._singleton.setSummaryLog(self._testName)
        super().__init__(tests)

    @property
    def verbosity(self):
        return self._singleton.getVerbosity()

    @verbosity.setter
    def verbosity(self, verbosity:int):
        self._singleton.setVerbosity(verbosity)

def RAFTUnitTestMain():
    """
    Runs the unit tests.
    """
    verb = SINGLETON.getVerbosity()
    unittest.main(argv=[sys.argv[0]], verbosity=SINGLETON.getVerbosity())