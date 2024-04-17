# Getting Started

This document will guide you through the process of creating your first test with the RAFT framework. 

---
* [Requirements](#requirements)
* [Installation](#installation)
* [Directory Structure](#directory-structure)
  * [Alternative Structure](#alternative-structure)
* [Config File Setup](#config-file-setup)
  * [The Rack Config](#the-rack-config)
    * [The Global Section](#the-global-section)
    * [Example of the global section](#example-of-the-global-section)
    * [The Rack Section](#the-rack-section)
    * [Example of the rack section](#example-of-the-rack-section)
    * [Example Rack Config](#example-rack-config)
  * [The Device Config](#the-device-config)
    * [Example Device Config](#example-device-config)
* [Writing Your First Test](#writing-your-first-test)
  * [Import and subclass the testController](#import-and-subclass-the-testcontroller)
  * [Setup the environment for your test](#setup-the-environment-for-your-test)
  * [The main test function](#the-main-test-function)
  * [Clean up after your test](#clean-up-after-your-test)
  * [Create the main function for your test script](#create-the-main-function-for-your-test-script)
  * [Example Test script](#example-test-script)
  * [Run the test script](#run-the-test-script)
* [The Logs](#the-logs)
  * [Explaination of the log files](#explaination-of-the-log-files)
---

## Requirements

- A Linux based OS
- SSH Server installed and configured

## Installation

Follow the installation guide [here](../README.md) to begin

## Directory Structure

The simplest way to get a test to work with the RAFT framework is to create your test file inside the python_raft folder after you've cloned the repository.
```sh
python_raft/
├── CONTRIBUTING.md
├── COPYING -> LICENSE
├── docs
├── framework
├── GETTING_STARTED_TEST.py
├── installation
├── LICENSE
├── NOTICE
├── README.md
├── requirements.txt
└── unitTests
```

### Alternative Structure
Should you wish to use to keep your test script in a different folder you will need to add the following line to the top of your test script for it to work.
```py
import sys
sys.path.append('<path to framework directory in python_raft clone>')
```

## Config File Setup

There are two very important yaml config files used with the RAFT framework. These are:
- The rack config
- The device config.
Both these files should be create inside the top level python_raft folder, with the names `rack_config.yml` & `device_config.yml`.

### The Rack Config

This yaml file is used to define the setup your DUT (**D**evice **U**nder **T**est). In this file the connections, IP addresses and controllers connected to the device are listed.

For the purposes of the first test we will create from this document, we will fill out the rack config with the information of the PC you are current running the tests on.

#### The Global Section

To begin the rack config we define the `globalConfig` section. In this section we define data that is global to all tests.

In the global section we will define the included config, using the includes field. For the purpose of this guide we need to add the `deviceConfig` key to this, with it's value set to the path of the device config file.

We also need to defile the local field, with the log key. This will tell the test where to put the logs from the tests.

#### Example of the global section
```yaml
globalConfig:
    includes:
        deviceConfig: "./device_config.yml"
    local:
        log:
            directory: "./logs"
            delimiter: "/"
```

#### The Rack Section

In the `rackConfig` section, we define our racks, their slots and the devices in them. *These are not always physical racks and slots*.

First we start off by defining a rack with a name and a description.
Then we define the slots in it, with their own name and description.
A slot can contain multiple devices, but must contain a dut (Device Under Test). Other devices could be defined here would be devices to interact with the dut.
As part of the device field we must define the consoles we can use to interact with it. We must also define the devices platform, this platform must correspond to a device type in the device config.

#### Example of the rack section

```yaml
rackConfig:
    rack1:
        name: "rack1"
        description: "example config at my desk"
        slot1:
            name: "slot1"
            devices:
                - dut:
                    ip: "127.0.0.1"  
                    description: "local pc"
                    platform: "linux"
                    consoles:
                        - default:
                            type: "ssh"
                            port: "22"
                            ip: "127.0.0.1"
```

#### Example Rack Config
```yaml
globalConfig:
    includes:
        deviceConfig: "./device_config.yml"
    local:
        log:
            directory: "./logs"
            delimiter: "/"
        
rackConfig:
    rack1:
        name: "rack1"
        description: "example config at my desk"
        slot1:
            name: "slot1"
            devices:
                - dut:
                    ip: "127.0.0.1"  
                    description: "local pc"
                    platform: "linux"
                    consoles:
                        - default:
                            type: "ssh"
                            port: "22"
                            ip: "127.0.0.1"
```

### The Device Config

The Device Config is used to define device types. The information defined in this config is consistent across all devices of a type.

Here we are simple defining a linux type, with the model identity as `PC`.

#### Example Device Config
```yaml
deviceConfig:
    cpe1:
        platform:   "linux"
        model:      "PC"

```

## Writing Your First Test

For our first test script we will simply write a test that does the following:
1. SSH's into our local PC
2. Creates a folder called RAFT_test_files
3. Creates a file in that folder called RAFT_Test_File
4. Lists the contents of the RAFT_test_files directory to check that the RAFT_Test_File has been created
5. Exits with test success if the file is created, failure when the file is no created.

### Import and subclass the testController

At the heart of all tests is the testController. This class contains methods for you to fill out to set up and tear down the environment for your test and to actually run the steps of your test.

The first step of any test is to import the testController into your test script and subclass it. This will allow you to fill out the predefined functions to run your test.

*We've also defined some global variables here to use a constants for the file paths we need for testing.*

```python

from framework.core.testControl import testController

TEST_FILE = 'RAFT_Test_File'
TEST_DIRECTORY = '~/RAFT_test_files'

class FirstTest(testController):

    def __init__(self):
        super().__init__(testName='My first test', qcId='1')
```

### Setup the environment for your test

To ensure our test can run correctly, we need to setup the testing environment correct.
For the purpose of this test we will fillout the testPrepareFunction(). This function will need to do the following:
- Ensure the `TEST_DIRECTORY` is created on our local PC.
- Ensure it doesn't already contain a file with the same name as the `TEST_FILE`.
	- Removing any files that already exist in the directory that have the same name.
- Return a boolean, set to `True` when the environment has been set up correctly.
	- Set the boolean to `False` when the environtment could not be set up correct. This will allow the test to abort and prevent erroneous results.

```python
#!/usr/bin/env python3

from framework.core.testControl import testController

# Globals to keep the filepaths we're using constant
TEST_FILE = 'RAFT_Test_File'
TEST_DIRECTORY = '~/RAFT_test_files'

class FirstTest(testController):

    def __init__(self):
        super().__init__(testName='My first test', qcId='1')

    def testPrepareFunction(self, recursive_stop=False):
        """This function runs before the test to prepare the environment.

        Args:
            recursive_stop (bool, optional): Hacky way to stop infinite recursive loop. Defaults to False.

        Returns:
            bool: True when environment setup successful.
        """
        result = True
        self.log.info('Pre-test check')
        self.log.info('Make the test directory')
        # Create test directory if if doesn't already exist
        self.session.write(f'mkdir -p {TEST_DIRECTORY}')
        # List the files in the test directory
        self.session.write(f'ls {TEST_DIRECTORY}')
        file_list = self.session.read_all()
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
```

### The main test function

We're now ready to fill out the `testFunction()` method. This function is the main body of the test. 

```python
#!/usr/bin/env python3

from framework.core.testControl import testController

# Globals to keep the filepaths we're using constant
TEST_FILE = 'RAFT_Test_File'
TEST_DIRECTORY = '~/RAFT_test_files'

class FirstTest(testController):

    def __init__(self):
        super().__init__(testName='My first test', qcId='1')

    def testPrepareFunction(self, recursive_stop=False):
        """This function runs before the test to prepare the environment.

        Args:
            recursive_stop (bool, optional): Hacky way to stop infinite recursive loop. Defaults to False.

        Returns:
            bool: True when environment setup successful.
        """
        result = True
        self.log.info('Pre-test check')
        self.log.info('Make the test directory')
        # Create test directory if if doesn't already exist
        self.session.write(f'mkdir -p {TEST_DIRECTORY}')
        # List the files in the test directory
        self.session.write(f'ls {TEST_DIRECTORY}')
        file_list = self.session.read_all()
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
        result = False
        self.log.stepStart(f'Creating {TEST_FILE} in {TEST_DIRECTORY}')
        # Create the test file in the test directory
        self.session.write(f'touch {TEST_DIRECTORY}/{TEST_FILE}')
        self.log.step(f'Running ls in {TEST_DIRECTORY}')
        # List the contents of the test directory
        self.session.write(f'ls {TEST_DIRECTORY}')
        file_list = self.session.read_all()
        if TEST_FILE in file_list:
            result = True
        self.log.stepResult(result, 'Test for file')
        return result
```

### Clean up after your test

To clean up after a test has run we use the `testEndFunction()`. This function will always run after the test to clean up any mess made by the test. In this case we are using it to remove the `TEST_DIRECTORY` and it's contents

```python
#!/usr/bin/env python3

from framework.core.testControl import testController

# Globals to keep the filepaths we're using constant
TEST_FILE = 'RAFT_Test_File'
TEST_DIRECTORY = '~/RAFT_test_files'

class FirstTest(testController):

    def __init__(self):
        super().__init__(testName='My first test', qcId='1')

    def testPrepareFunction(self, recursive_stop=False):
        """This function runs before the test to prepare the environment.

        Args:
            recursive_stop (bool, optional): Hacky way to stop infinite recursive loop. Defaults to False.

        Returns:
            bool: True when environment setup successful.
        """
        result = True
        self.log.info('Pre-test check')
        self.log.info('Make the test directory')
        # Create test directory if if doesn't already exist
        self.session.write(f'mkdir -p {TEST_DIRECTORY}')
        # List the files in the test directory
        self.session.write(f'ls {TEST_DIRECTORY}')
        file_list = self.session.read_all()
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
        result = False
        self.log.stepStart(f'Creating {TEST_FILE} in {TEST_DIRECTORY}')
        # Create the test file in the test directory
        self.session.write(f'touch {TEST_DIRECTORY}/{TEST_FILE}')
        self.log.step(f'Running ls in {TEST_DIRECTORY}')
        # List the contents of the test directory
        self.session.write(f'ls {TEST_DIRECTORY}')
        file_list = self.session.read_all()
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
```

### Create the main function for your test script

The final step to creating your test script is to add a main function to the bottom of the script. This is what the script will run when executed.

In our main we are simply creating an instace of our test and calling it's `run()` function.

```python
if __name__ == '__main__':
    TEST = FirstTest()
    TEST.run()
```

### Example Test script

```python

#!/usr/bin/env python3

from framework.core.testControl import testController


TEST_FILE = 'RAFT_Test_File'
TEST_DIRECTORY = '~/RAFT_test_files'

class FirstTest(testController):

    def __init__(self):
        super().__init__(testName='My first test', qcId='1')

    def testPrepareFunction(self, recursive_stop=False):
        """This function runs before the test to prepare the environment.

        Args:
            recursive_stop (bool, optional): Hacky way to stop infinite recursive loop. Defaults to False.

        Returns:
            bool: True when environment setup successful.
        """
        result = True
        self.log.info('Pre-test check')
        self.log.info('Make the test directory')
        # Create test directory if if doesn't already exist
        self.session.write(f'mkdir -p {TEST_DIRECTORY}')
        # List the files in the test directory
        self.session.write(f'ls {TEST_DIRECTORY}')
        file_list = self.session.read_all()
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
        result = False
        self.log.stepStart(f'Creating {TEST_FILE} in {TEST_DIRECTORY}')
        # Create the test file in the test directory
        self.session.write(f'touch {TEST_DIRECTORY}/{TEST_FILE}')
        self.log.step(f'Running ls in {TEST_DIRECTORY}')
        # List the contents of the test directory
        self.session.write(f'ls {TEST_DIRECTORY}')
        file_list = self.session.read_all()
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

if __name__ == '__main__':
    TEST = FirstTest()
    TEST.run()
```

### Run the test script

This test script can be run with the below command:
`python3 my_first_test.py --config rack_config.yml`

## The Logs

After running your test you should find a new folder has been created called `logs`. In this folder you will sub directories for the racks and slots listed in your rack config. In each slot directory you will find directories, with the time and date. Each of these corresponds to a test run. In these you will find the logs for your tests.

```sh
python_raft/logs/
└── rack1
    └── slot1
        └── 20240417-15-39-22
            └── My first test-1
                ├── screenImages
                ├── test-0.log
                ├── test-0.log.csv
                ├── test_summary.log
                └── test_summary.log.csv
```

### Explaination of the log files

The `.log` files in this directory are text files that detail the running and results of the test and it's steps.
The `.csv` files in the directory are show the results of the test steps as a simple pass fail, in a standard csv format.
The summary files in this directory show the results of all tests that ran.
*If multiple instances of our test class had been created they would each get a `test-<index>.log` and corresponding `.csv`, with all their results being collated into the summary files.*

