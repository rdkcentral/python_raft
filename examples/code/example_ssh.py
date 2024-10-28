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

# Since this test is in a sub-directory we need to add the directory above
# so we can import the framework correctly
MY_PATH = path.abspath(__file__)
MY_DIR = path.dirname(MY_PATH)
sys.path.append(path.join(MY_DIR,'../../'))
from framework.core.testControl import testController


# Constants for the file paths we need for testing
TEST_FILE = 'RAFT_Test_File'
TEST_DIRECTORY = '~/RAFT_test_files'


# The heart of all tests is the testController
class FirstTest(testController):

    def __init__(self):
        super().__init__(testName='example_test', qcId='1')

    def testPrepareFunction(self, recursive_stop=False):
        """This function runs before the test to prepare the environment.
        We are overriding this function from the testController class.

        Args:
            recursive_stop (bool, optional): Hacky way to stop infinite recursive loop. Defaults to False.

        Returns:
            bool: True when environment setup successful.
        """
        result = True
        self.log.info('Pre-test check')
        self.log.info('Make the test directory')
        # For this to work the prompt entry in the example_device_config.yml
        # must be set to the prompt of the test device
        self.session.prompt = self.cpe.get('prompt')
        # Create test directory if if doesn't already exist
        self.session.write(f'mkdir -p {TEST_DIRECTORY}')
        # List the files in the test directory
        self.session.write(f'ls {TEST_DIRECTORY}')
        file_list = self.session.read_until(self.session.prompt)
        # Clear the session buffer now we've capured its contents
        self.session.write('clear')
        self.log.info(f'Current file list: {file_list}')
        if TEST_FILE in file_list:
            self.log.info(f'{TEST_FILE} found in testing directory')
            self.session.write(f'rm {TEST_DIRECTORY}/{TEST_FILE}')
            self.log.info('Rerunning pre-test check to ensure file has been removed')
            # If this is true, we've tried to remove the file before and it didn't work
            if recursive_stop:
                # Rather than going in an endless loop of trying to remove the file
                # Return false to signal the prepare failed 
                return False
            else:
                # Rerun the prepare function to ensure the test file has been removed
                result = self.testPrepareFunction(recursive_stop=True)
        return result


    def testFunction(self):
        """This is the main test function of the test controller.
        It is being overridden to perform an actual test.

        Returns:
            bool: True if test is successful. False if the test result is a failure.
        """
        result = False
        self.log.stepStart(f'Creating {TEST_FILE} in {TEST_DIRECTORY}')
        # Create the test file in the test directory
        self.session.write(f'touch {TEST_DIRECTORY}/{TEST_FILE}')
        self.log.step(f'Running ls in {TEST_DIRECTORY}')
        # List the contents of the test directory
        self.session.write(f'ls {TEST_DIRECTORY}')
        file_list = self.session.read_until(self.session.prompt)
        if TEST_FILE in file_list:
            result = True
        self.log.stepResult(result, 'Test for file')
        return result

    def testEndFunction(self, powerOff=False):
        """This function alway runs after the test has finished.
        It is used to reset the test environment.

        Args:
            powerOff (bool, optional): This variable tells the test whether to turn off the power of the dut when it is finished. Defaults to False.

        Returns:
            bool: True when test exits successfully.
        """
        # A Bug is currently causing powerOff to always be true
        powerOff = False
        self.log.info(f'Removing {TEST_DIRECTORY}')
        self.session.write(f'rm -rf {TEST_DIRECTORY}')
        return super().testEndFunction(powerOff)

# This is what the script will run when executed
if __name__ == '__main__':
    TEST = FirstTest()
    TEST.run()