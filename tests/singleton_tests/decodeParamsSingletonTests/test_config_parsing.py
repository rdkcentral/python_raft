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
#*   ** @addtogroup  : tests
#*   ** @file        : test_config_parsing.py
#*   ** @date        : 31/07/2024
#*   **
#*   ** @brief : Test the config parsing that happens as part of decodeParams.py
#*   **
#*   ** The positive path for this test is to run it with the below arguments:
#*   ** --config examples/configs/getting_started_rack_config.yml
#*   ** --deviceConfig examples/configs/example_device_config.yml 
#*   ** --buildInfo info 
#*   ** --overrideDeviceConfig config 
#*   ** --rack rack1
#*   ** --slot 1 
#*   ** --slotName slot1 
#*   ** --job_id 1 
#*   ** --rack_job_execution 1 
#*   ** --loop 1 
#*   ** --test
#*   ** --debug
#* ******************************************************************************

import sys
import os
import unittest

import yaml
try:
    from yaml import SafeLoader as LOADER
except:
    from yaml import CLoader as LOADER

# Add the directory containing the framework package to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(path)

from framework.core.singleton import SINGLETON

MY_PATH = os.path.abspath(__file__)
MY_DIR = os.path.dirname(MY_PATH)

class TestConfigParsing(unittest.TestCase):

    def setUp(self):
        self._decode_params = SINGLETON.config
        self._rack_config = os.path.join(MY_DIR,'../../../examples/configs/example_rack_config.yml')
        self._device_config = os.path.join(MY_DIR,'../../../examples/configs/example_device_config.yml')

    def test_decodeConfigIntoDictionary(self):
        """
        Test the decodeConfigIntoDictionary function works as expected.
        """
        with open(self._rack_config, 'r', encoding='utf-8') as rc:
            expected_dict = yaml.load(rc, Loader=LOADER)
        expected_restructure = expected_dict.get('globalConfig')
        expected_restructure.update(expected_dict.get('rackConfig'))
        result = self._decode_params.decodeConfigIntoDictionary(self._rack_config)
        self.assertEqual(expected_restructure,result,'Config file was not parsed into dictionary correctly')

    def test_decodeDeviceConfig(self):
        """
        Test the decodeDeviceConfig works as expected.
        """
        with open(self._device_config, 'r', encoding='utf-8') as rc:
            expected_dict = yaml.load(rc, Loader=LOADER)
        expected_restructure = expected_dict.get('deviceConfig')
        # SINGLETON.config.args.deviceConfigFile = None
        device_config = SINGLETON.deviceConfig.cpe
        self.assertEqual(expected_restructure,device_config)

if __name__ == "__main__":
   unittest.main(argv=[sys.argv[0]])

    