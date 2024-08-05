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
#*   ** @file        : test_decodeParams.py
#*   ** @date        : 31/07/20224
#*   **
#*   ** @brief : Tests the decodeParams class as part of the singleton.
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

# Add the directory containing the framework package to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(path)

from framework.core.raftUnittest import RAFTUnitTestSuite, RAFTUnitTestMain
from decodeParamsSingletonTests.test_argument_parser import TestArgumentParser
from decodeParamsSingletonTests.test_config_parsing import TestConfigParsing

if __name__ == "__main__":
    TestDecodeParams = RAFTUnitTestSuite('TestDecodeParams')
    TestDecodeParams.addTest(TestArgumentParser())
    TestDecodeParams.addTest(TestConfigParsing())
    TestDecodeParams.verbosity = 2
    RAFTUnitTestMain()

