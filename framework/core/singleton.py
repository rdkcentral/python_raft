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
#*   ** @file        : singleton.py
#*   ** @date        : 05/08/2024
#*   **
#*   ** @brief : Singleton class.
#*   **
#* ******************************************************************************

import datetime
import os

from framework.core.decodeParams import decodeParams
from framework.core.deviceManager import deviceManager
from framework.core.rackController import rackController
from framework.core.configParser import configParser
from framework.core.logModule import logModule

class Singleton:
    """Singleton class to contain all core functionality for the
        RAFT framework, that can be shared among all tests and suites.

    Attributes:
        _instance (bool): True when Singleton object already exists.
        summaryLog (logModule): summary logger for test case/suite.
        logPath (str): Path to store summary logs for current test case/suite.
        testLog (logModule): Detailed logger for the current test case/suite.
        testLogPath (str): Path to store detailed logs for current test case/suite.
        config (decodeParams): Object containing data of args passed to the test and configs.
        _rackController (rackController): Object with information of racks.
        deviceConfig (configParser): Object with information contained in deviceConfig.
        rack (rack): Object with information of the rack in use.
        slotInfo (slot): Object with information of the slot in use.
        logConfig (dict): Configuration data for logging.
        _verbosity (int): Verbosity level to use for current test case/suite.
    """

    _instance = False

    def __new__(cls, log):
        """Method to create new instance of a singleton object.

        It checks if an instance of the Singleton class already exists.
        If not, it creates a new instance, initializes its attributes, and sets the class variable
        `_instance` to True to prevent further instantiation.

        Args:
            log (logModule, optional): An instance of the logModule class (used internally). Defaults to None.

        Returns:
            Singleton: The single instance of the Singleton class.
        """

        if cls._instance is False:
            cls._instance = True
            cls._verbosity = 1
            cls.summaryLog = None
            cls.logPath =None
            cls.testLog = None
            cls.testLogPath = None
            cls.devices = None
            cls.config = decodeParams(log)
            cls._rackController = rackController(cls.config.rackConfig)
            cls.deviceConfig = configParser(cls.config.deviceConfig)
            cls.deviceConfig.decodeConfig(cls.config.rackConfig)
            cls.rack = cls._get_rack()
            cls.slotInfo = cls._getSlotInfo()
            cls.logConfig = cls.config.rackConfig.get("local").get("log")
        return cls

    @classmethod
    def _get_rack(cls):
        """Set up the rack object for the selected rack.

        Retreives the rack object for the rack selected in decodeParams.
        The object contains the information for the rack from the rack config.

        Returns:
            rack (rack): Rack object containing information about the rack selected.
        """
        rackName = cls.config.args.rackName
        if rackName == None:
            rack = cls._rackController.getRackByIndex(0)
        else:
            rack = cls._rackController.getRackByName(rackName)
        return rack

    @classmethod
    def _getSlotInfo(cls):
        """Get the information for the slot selected.

        Gets the information for the selected slot,
         based on the arguments parsed by decodeParams.

        Returns:
            slot (rackSlot): Object containing the information of the slot
                             from the rack config.
        """
        #Determine the slot to use
        if cls.config.args.slotNumber != None:
            slot = cls.rack.getSlot(cls.config.args.slotNumber)
        else:
            slotName = cls.config.args.slotName
            if slotName == None:
                slot = cls.rack.getSlot(1)
            else:
                slot = cls.rack.getSlotByName(slotName)
        return slot

    @classmethod
    def setVerbosity(cls,verbosity:int):
        """Set the verbosity level.

        A numerical system of 0-2 is used for the verbosity.
        With 0 being the lowest level and 2 being the highest.

        Args:
            verbosity (int): Verbosity level to use.
        """
        if verbosity > 2:
            verbosity = 2
        elif verbosity < 0:
            verbosity = 0
        cls._verbosity = verbosity

    @classmethod
    def getVerbosity(cls):
        """Get the verbostity level.

        Returns:
            cls.verbosity (int): Verbosity level.
        """
        return cls._verbosity

    @classmethod
    def constructLogPath(cls):
        """Construct the path required for all logs.

        Returns:
            str: Constructed log path.
        """
        #Check if the summary path was previous set, if so then we take that one instead of our new one
        if cls.summaryLog.path != None:
            logPath = cls.summaryLog.path
            return logPath

        time = datetime.datetime.now().strftime("%Y%m%d-%H-%M-%S")

        logPath = cls.addDelimiter(cls.logConfig.get("directory"))
        logPath += cls.addDelimiter(cls.rack.name)
        logPath += cls.addDelimiter(cls.slotInfo.config.get("name"))
        logPath = cls.addDelimiter(logPath + time )
        cls.summaryLog.path = logPath

        try:
            os.makedirs(logPath, exist_ok = True)
            cls.summaryLog.debug("Directory '{}' created successfully".format(logPath))
        except OSError as error:
            cls.summaryLog.error("Directory '{}' can not be created".format(logPath))
        return logPath

    @classmethod
    def constructTestPath(cls, testName:str, qcId:str):
        """Construct the path required for all test logs.

        Args:
            testName (str): Name of the currently running test case/suite.
            qcId (str, Optional): Quality control ID of the currently running test case/suite.

        Returns:
            str: Constructed test log path.
        """
        testPath = cls.addDelimiter( cls.logPath + testName + "-" + qcId )
        try:
            os.makedirs(testPath, exist_ok = True )
            cls.testLog.debug("Directory '{}' created successfully".format(testPath))
            screenImagesPath = cls.addDelimiter( testPath + "screenImages")
            os.makedirs(screenImagesPath, exist_ok = True )
        except OSError as error:
            cls.testLog.error("Directory '{}' can not be created".format(testPath))
        return testPath

    @classmethod
    def addDelimiter(cls, path):
        """Add delimiter to the path if required.

        Args:
            path (str): Path to add delimiter.

        Returns:
            str: Path with added delimiter if required.
        """
        delimiter = cls.logConfig.get("delimiter")
        if path[-1] == delimiter:
            return path
        path += delimiter
        return path

    @classmethod
    def setSummaryLog(cls, testName:str, qcId:str=''):
        """Set up the summary logger

        Args:
            testName (str): Name of the test or test suite starting the logger.
            qcId (str, Optional): QC ID of the test or test suite starting the logger.
        """
        if cls.summaryLog == None:
            cls.summaryLog = logModule(testName+"-summary" )
            # Setup logging
            cls.testLog = logModule(testName)
            cls.logPath = cls.constructLogPath()
            cls.testLogPath = cls.constructTestPath(testName, qcId)
            logFilename = "test-{}.log".format(cls.summaryLog.summaryTestTotal)
            cls.testLog.setFilename(cls.testLogPath, logFilename)

    @classmethod
    def setupDevices(cls, log: logModule, logPath:str):
        """Setup the deviceManager for the devices in the current slot under test.

        Args:
            log (logModule): Log Module for the current test.
            logPath (str): Path of logging output for the current test.

        Returns:
            deviceManager : deviceManager object for all devices in the slot in use by the
                            current test.
        """
        if cls.devices is None:
            cls.devices = deviceManager(cls.slotInfo.config.get("devices"), log, logPath)
        return cls.devices

    @classmethod
    def getCPEInfo(cls):
        """Get the device config information for the current CPE device.

        Returns:
            dict: Dictionary of information for the current CPE device.
        """
        cpePlatform = cls.slotInfo.getPlatform()
        return cls.deviceConfig.getCPEEntryViaPlatform(cpePlatform)

SINGLETON = Singleton(log=None)
