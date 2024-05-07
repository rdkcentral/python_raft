![LOGO](docs/images/RAFT_Logo_250.png)

# RAFT

**R**apid **A**pplication **F**ramework for **T**esting.<br>

The RAFT framework provides a flexible environment for engineering-level device testing<br>
RAFT’s primary focus is to provide engineering teams a modular, config driven, low level testing framework.

## Contents

* [Why use RAFT?](#why-use-raft)
* [Features](#features)
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

---

## Why use RAFT?

Engineering tests are used by developers ensure each component of a software stack meets its requirements, without any unwanted behaviour. This is usually done through a combination of unit and functional testing.

While some engineering tests can be run without their target device. At some point the component will need to be tested within the context of the device.


***Thats where RAFT comes in.***

## Features

- Simple config driven interfaces, allowing for cross-platform tests.
- Many predefined control modules including:
  - Power control modules.
  - [Console modules](docs/modules/command_modules).
  - [Uploading and Downloading files](docs/modules/outbound_client.md).
  - [Controlling remote controls](docs/modules/common_remote.md).
- Out of the box standardised and consistent [logging](docs/modules/log_module.md).
- Straight-forward, Pythonic implementation.

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

For our first test script we will be using the [example_test.py](example_test.py). There are extensive comments in the test files to explain what it does.

This test script can be run with the below command:
`./example_test.py --config ./docs/getting_started_rack_config.yml`

### How it works?

Two config files are used for running this test. They are:

- The Rack config
  - This yaml file is used to define the setup your DUT (**D**evice **U**nder **T**est). In this file the connections, IP addresses and controllers connected to the device are listed.
  - For first test we used the [getting_started_rack_config.yml](docs/getting_started_rack_config.yml) from the docs directory.
  - For further information on the rack config see the [example_rack_config.yml](docs/example_rack_config.yml)
- The device config
  - This yaml file is used to define device types. The information defined in this config is consistent across all devices of a type.
  - For of our first test we will use the [example_device_config.yml](docs/example_device_config.yml)

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
