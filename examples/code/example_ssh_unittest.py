#!/usr/bin/env python3
#** *****************************************************************************
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
"""A simple test that does the following:
1. SSH's into our dut (with the getting_started_rack_config.yml this is our local PC)
2. Creates a folder called RAFT_test_files
3. Creates a file in that folder called RAFT_Test_File
4. Lists the contents of the RAFT_test_files directory to check that the RAFT_Test_File has been created
5. Cleans up after itself and removes the RAFT_test_files folder
6. Exits with test success if the file is created, failure when the file is not created.
"""

import sys
from os import path
import re

# Since this test is in a sub-directory we need to add the directory above
# so we can import the framework correctly
MY_PATH = path.abspath(__file__)
MY_DIR = path.dirname(MY_PATH)
sys.path.append(path.join(MY_DIR,'../../'))
from framework.core.raftUnittest import RAFTUnitTestCase, RAFTUnitTestMain
from framework.core.singleton import SINGLETON
from framework.core.utilities import utilities
# Constants for the file paths we need for testing
TEST_FILE = 'RAFT_Test_File'
TEST_DIRECTORY = '~/RAFT_test_files'

class TestExampleSSH(RAFTUnitTestCase):
    """
    A test class for verifying file creation on the DUT via SSH.
    """

    def _list_files(self,directory:str):
        """List the files in the given directory.

        Args:
            directory (str): Path of directory to list files in.

        Returns:
            str: Space separated list of files from the directory.
        """
        # List the files in the test directory
        self.dut.session.write(f'ls {directory}')
        file_list = utilities.strip_ansi_escapes(self.dut.session.read_all())
        # Clear the session buffer now we've capured its contents
        self.dut.session.write('clear')
        self.log.info(f'Current file list: [{file_list}]')
        return file_list

    def setUp(self):
        """
        Perform pre-test setup tasks.

        This method will run before each test method.
        """
        self.log.info('Pre-test check')
        self.log.info('Make the test directory')
        # Ping Test to check Box alive
        if self.dut.pingTest() is False:
            raise ConnectionError('Cannot reach dut')
        # Open the console session
        self.dut.session.open()
        # Create test directory if if doesn't already exist
        self.dut.session.write(f'mkdir -p {TEST_DIRECTORY}')
        file_list = self._list_files(TEST_DIRECTORY)
        if TEST_FILE in file_list:
            self.log.info(f'{TEST_FILE} found in testing directory')
            self.dut.session.write(f'rm {TEST_DIRECTORY}/{TEST_FILE}')
            self.log.info('Rerunning pre-test check to ensure file has been removed')

    def test_fileCreation(self):
        """
        The main test method that verifies file creation on the DUT

        Any method starting with the word test at the start of it name,
        will run as an individual test method.
        """
        self.log.stepStart(f'Creating {TEST_FILE} in {TEST_DIRECTORY}')
        # Create the test file in the test directory
        self.dut.session.write(f'touch {TEST_DIRECTORY}/{TEST_FILE}')
        file_list = self._list_files(TEST_DIRECTORY)
        # Test that the file is in the list object
        self.assertIn(TEST_FILE, file_list)

    def tearDown(self):
        """
        Performs post-test cleanup tasks:

        This method will run after each test method.
        """
        self.log.info(f'Removing {TEST_DIRECTORY}')
        self.dut.session.write(f'rm -rf {TEST_DIRECTORY}')

if __name__ == '__main__':
    RAFTUnitTestMain()
