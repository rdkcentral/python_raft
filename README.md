<div style="text-align:center"><img src="./docs/images/RAFT_Logo_250.png"/></div>

# Rapid Application Framework for Test (RAFT)

The RAFT framework provides a flexible environment for engineering-level device testing, empowering developers to thoroughly validate code changes before commits, promoting code quality and enabling the testing of multiple commits simultaneously.


<details>
  <summary id=toc>Contents </summary>
  
  * [Features](#features)
  * [Why Use This System](#why-use-this-system)
  * [Installation](#installation)
    * [Requirements](#requirements)
    * [User Installation](#user-installation)
  * [Getting Started](#getting-started)
    * [Running Your First Test](#running-your-first-test)
    * [How it works?](#how-it-works)
    * [The Logs](#the-logs)
  * [Documentation](#documentation)
  * [Contributing](#contributing)
  * [License](#license)
</details>

---

## Features:

### Configuration Management

The system includes a flexible parsing mechanism for configuration. This allows simple environment configuration for describing racks, the devices within them, network settings and other essential test parameters. Providing ultimate flexibility in testing setup, without needing to modify the test.

### Command-Line Customisation

Test runs can be customised by providing dynamic command-line arguments. These arguments might specify which rack to use, device slots to target, debug mode, and other runtime settings. The system intelligently combines these arguments with your pre-defined configurations.

### Device Control and Management

**Centralized Device Management**: The core of the system is a device manager that provides a centralized way to organize and control multiple devices in the testing setup. 

It understands how to:
- **Model Devices**: Representing each device as an object, encapsulating its configuration details.
- **Establish Consoles**: Establishing different types of communication channels with devices, supporting protocols like SSH, Telnet, or Serial for management and control.
- **Manage Power**: Integrates with power control mechanisms to cycle the power state of devices as needed during testing.
- **Handle Inbound/Outbound Connections**: Configures devices to initiate inbound/outbound connections if required by your test scenarios.
- **Remote Control**: Provides a unified interface for sending remote control commands to your devices, abstracting differences between remote types.


## Why Use This System

- **Minimal Infrastructure**: Adaptive minimal testing infrastructure requiring no specialised hardware.
- **Quick setup**: With python and some pip packages installed, testing can begin.
- **Flexibility**: Supports various devices, communication protocols, and integrates with different power control systems.
- **Ease of Use**: Provides a clear interface to interact with devices, simplifying your test scripts and focusing on the test logic itself.
- **Organization**: Introduces structure to your test environment, making it easier to manage test cases and scenarios.

## Installation

### Requirements

- Python (=3.11.8)
    - Pyenv can be used to manage multiple versions of Python (please refer to the [documentation](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)).

- All the packages listed in requirements.txt
    - Can be installed using `$ pip install -r requirements.txt`

### User Installation

Clone the repository and ensure that all requirements are met.

## Getting Started

### Running Your First Test

For our first test script we will be using the [example_test.py](examples/code/example_ssh.py). There are extensive comments in the test files to explain what it does.

Before this test script can be run the `prompt` line in the [device_config](examples/configs/example_device_config.yml) must be replaced with the prompt of the PC running the script.

This test script can be run with the below command:
`./example_test.py --config ../configs/getting_started_rack_config.yml`

### How it works?

Two config files are used for running this test. They are:

- The Rack config
  - This yaml file is used to define the setup your DUT (**D**evice **U**nder **T**est). In this file the connections, IP addresses and controllers connected to the device are listed.
  - For first test we used the [getting_started_rack_config.yml](examples/configs/getting_started_rack_config.yml) from the docs directory.
  - For further information on the rack config see the [example_rack_config.yml](examples/configs/example_rack_config.yml)
- The device config
  - This yaml file is used to define device types. The information defined in this config is consistent across all devices of a type.
  - For of our first test we will use the [example_device_config.yml](examples/configs/example_device_config.yml)

### The Logs

After running your test you should find a new folder has been created called `logs`. This should contain test logs in both text and `.csv` format.

The summary files in this directory show the results of all tests that ran.

*If multiple instances of our test class had been created they would each get a `test-<index>.log` and corresponding `.csv`, with all their results being collated into the summary files.*


## Documentation

- [Module documentation](docs/modules/interfaces.md)

## Contributing

See contributing file: [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

See license file: [LICENSE](./LICENSE)



<style>
    #toc {
        font-size: 1.5em;
        font-weight: 500;
    }
</style>
