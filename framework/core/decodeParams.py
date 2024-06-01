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
#*   ** @file        : decodeParams.py
#*   ** @date        : 01/07/2021
#*   **
#*   ** @brief : decodeParams class
#*   **
#* ******************************************************************************

import os
import logging
from datetime import datetime
from os import path
import argparse
import yaml
import os
class FlexibleObject:
    def __getattr__(self, name):
        # Return None if the attribute is not found
        return None
class decodeParams():
    """Decodes the input arguments and sets the slot details
    """
    
    def __init__(self, log):
        """
        Initialises a DecodeParams instance based on the parameters.

        Args:
            log (logModule): Log module instance.
        """
        self.jobId = None
        self.rackJobExecutionId = None
        self.testMode = False
        self.debug = False
        self.loop = None
        self.log = log
        self.buildConfig = None
        self.overrideCpeConfig = None

        parser = argparse.ArgumentParser()
        config=os.environ.get('CONFIG')
        # Switches with a 2nd parameter
        parser.add_argument('--config', '-config', help="config file", action="store", dest="configFile")
        parser.add_argument('--deviceConfig', '-deviceConfig', '--deviceConfig', '-testConfig', "--testConfig", help="testconfig file", action="store", dest="deviceConfigFile")
        parser.add_argument('--buildInfo', help='Build info file', action='store', dest='buildInfo')
        parser.add_argument('--overrideDeviceConfig', help='cpe config override', action='store', dest='overrideCpeConfig')
        parser.add_argument('--rack', help="rack name", action="store", dest="rackName")
        parser.add_argument('--slot', help="slot number", action="store", dest="slotNumber", type=int)
        parser.add_argument('--slotName', help="slot number", action="store", dest="slotName")
        parser.add_argument('--job_id', help="job Id (optional)", action="store", dest="jobId")
        parser.add_argument('--rack_job_execution_id', help="rack job id (optional)", action="store", dest="rackJobExecutionId")
        parser.add_argument('--loop', help="device ip", action="store", dest="loop")
        
        # Single switches
        parser.add_argument('--test', '-test', help="test Mode enabled", action="store_const", dest="testMode", const=True)
        parser.add_argument('--debug', '-debug', help="set debug level", action="store_const", dest="debug", const=True)

        try:
            self.args = parser.parse_args()
        except SystemExit:
            self.log.error("Failed to parse command-line arguments.")
            self.args = FlexibleObject()
        if self.args.configFile == None:
            print("Config file is required to run: ERROR, missing --config <url> argument")
            os._exit(1)

        #Decode the configuration
        self.rackConfig = self.decodeConfigIntoDictionary( self.args.configFile )
        self.decodeDeviceConfig()

        # Check for build_info and overrideDeviceConfig yaml files
        if getattr(self.args, 'buildInfo', None):
            self.buildConfig = self.args.buildInfo
        
        if getattr(self.args, 'overrideCpeConfig', None):
            self.overrideCpeConfig = self.args.overrideCpeConfig

         # Setup the debug mode
        if self.args.debug != None:
            self.debug = True

         # Setup the test mode
        if (self.args.testMode != None):
            self.testMode = True

        # Setup the loop override
        if (self.args.loop != None):
            self.loop = self.args.loop

    def decodeDeviceConfig( self ):
        """Decodes the device configuration.
        """
        self.deviceConfig = None
        deviceConfigFile = self.args.deviceConfigFile
        if deviceConfigFile == None:
            try:
                deviceConfigFile = self.rackConfig.get("includes").get("deviceConfig")
            except:
                self.log.warn("No deviceConfig: [filename.yml] specified")
                return
                #print("deviceConfig: file is required to run: ERROR deviceConfig: location: <url> not specified")
                #os._exit(1)

        # Convert the ./test_config, to a full path if required.
        self.deviceConfig = self.decodeConfigIntoDictionary(deviceConfigFile)

    def decodeConfigIntoDictionary(self, configFile):
        """
        Decodes the configuration file into a dictionary.

        Args:
            configFile (str): Path to the configuration file.

        Returns:
            dict: The decoded configuration.
        """
        fullPath = configFile
        if fullPath.startswith("."):
            fullPath = os.path.abspath(configFile)
        if os.path.exists(fullPath) == False:
            print("config: file is required to run: ERROR, missing url=[{}]".format(fullPath))
            os._exit(1)
        with open(configFile) as inputFile:
            inputFile.seek(0, os.SEEK_SET)
            config = yaml.full_load(inputFile)
        
        keyDictionary = {}
        for key, val in config.items():
            if isinstance(val, dict):
                for k, v in val.items():
                    keyDictionary[k] = v 
            else:
                keyDictionary[key] = val
        return keyDictionary
