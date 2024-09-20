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
#*   ** @file        : testControl.py
#*   ** @brief : Test Control Module for running rack Testing
#*   **
#* ******************************************************************************
# System
import sys
import datetime
import time
import signal
import random
import telnetlib
import os
import shlex, subprocess
import traceback
import requests
import platform
import inspect
import csv
import signal

dir_path = os.path.dirname(os.path.realpath(__file__))

from framework.core.logModule import logModule
from . logModule import DEBUG, INFO, WARNING, ERROR, CRITICAL

from framework.core.rackController import rackController
from framework.core.configParser import configParser
from framework.core.utilities import utilities
from framework.core.decodeParams import decodeParams
from framework.core.capture import capture
from framework.core.webpageController import webpageController
from framework.core.deviceManager import deviceManager

class testController():

    slotInfo = None
    log = None
    session = None
    fullPath = None
    testMode = False
    loopCount = 0
    TEST_MAX_RUN_TIME = (60*60*24*30) #  Test all tests max run time to 30 days

    def __init__(self, testName="", qcId="", maxRunTime=TEST_MAX_RUN_TIME, level=logModule.STEP, loop=1, log=None):
        """Initialize the test class.

        Args:
            testName (str, optional): Name of the test. Defaults to "".
            qcId (str, optional): QC ID of the test. Defaults to "".
            maxRunTime (int, optional): Maximum runtime of the test. Defaults to TEST_MAX_RUN_TIME.
            level (int, optional): Log level. Defaults to logModule.STEP.
            loop (int, optional): Number of test loops. Defaults to 1.
            log (class, optional): Parent log class. Defaults to None.
        """
        self.testStartTime = ''
        self.log = logModule(testName)
        self.log.setLevel(level)
        testHasParent = False
        self.summaryLog = log
        if self.summaryLog == None:
            self.summaryLog = logModule( testName+"-summary" )
            self.summaryLogCreated = True
        self.maxRunTime = maxRunTime
        self.loopCount = loop   # Set the loop input from the test
        self.result = False    # Setup the result codes
        self.testName = testName
        self.qcId = qcId
        self.capture = None
        self.webpageController = None
        signal.signal(signal.SIGINT, self.signal_handler)

        # Ensure that decodeParams is after set level to support --debug
        self.config = decodeParams(self.log)

        if self.config.debug == True:
            self.log.setLevel(self.log.DEBUG)

        # Decode the input configuration file
        self.rackControl = rackController( self.config.rackConfig )

        # Let's run the config parse on the deviceConfig + anything in the rackConfig also, so that all the data is in the deviceConfig
        # except for the rack specific section
        self.deviceConfig = configParser( self.config.deviceConfig )
        self.deviceConfig.decodeConfig( self.config.rackConfig )

        # Determine what slot we're going to work with
        rackName = self.config.args.rackName
        if rackName == None:
            rack = self.rackControl.getRackByIndex( 0 )
        else:
            rack = self.rackControl.getRackByName( rackName )

        #Determine the slot to use
        if self.config.args.slotNumber != None:
            slot = rack.getSlot(self.config.args.slotNumber )
        else:
            slotName = self.config.args.slotName
            if slotName == None:
                slot = rack.getSlot( 1 )
            else:
                slot = rack.getSlotByName( slotName )

        self.slotInfo = slot

        if (self.config.testMode != None ):
            self.testMode = self.config.testMode # Override the test mode out of the decodeParams, as required
        if (self.config.loop != None ):
            self.loopCount = int(self.config.loop) # Override the loop count out of the decodeParams

        # Pull the log configuration
        self.logConfig = self.config.rackConfig.get("local").get("log")
        self.logPath = self.constructLogPath(rack.name,self.slotInfo.config[ "name" ] )
        self.testLogPath = self.constructTestPath()

        #Start the logging system
        logFilename = "test-{}.log".format(self.summaryLog.summaryTestTotal)
        self.log.setFilename( self.testLogPath, logFilename )
        summaryPath = self.logPath
        if log==None:
            #We don't have a parent log so we put the summary log inside the test path
            summaryPath = self.testLogPath
        self.summaryLog.setFilename( summaryPath, "test_summary.log")

        #Start the rest of the testControl requirements
        self.devices = deviceManager(self.slotInfo.config.get("devices"), self.log, self.testLogPath)

        # Set up the session from the default console
        self.dut = self.devices.getDevice( "dut" )
        self.session = self.dut.getConsoleSession()
        self.outboundClient = self.dut.outBoundClient
        self.powerControl = self.dut.powerControl
        self.commonRemote = self.dut.remoteController
        self.utils = utilities(self.log)
        # For UI tests Initialising Video capture and decode the screen_regions.yml for the platform
        cpePlatform = self.slotInfo.getPlatform()
        self.cpe = self.deviceConfig.getCPEEntryViaPlatform(cpePlatform)
        if self.cpe == None:
            self.log.warn("CPE device:[{}] not setup".format(cpePlatform))

        # Setup the capture device
        captureConfig = self.config.rackConfig.get("capture")
        if captureConfig != None:
            captureImagesPath = os.path.join(self.testLogPath, "captureImages")
            self.capture = capture(self.log, captureImagesPath, **captureConfig)
            # Start the capture engine
            self.capture.start()
        else:
            self.log.warn("capture Engine not setup")

        # Setup the OCR capture regions if defined, otherwise the test can configure it
        if self.cpe != None and captureConfig != None and 'screenRegions' in self.cpe:
            # Setup the current capture regions
            captureRegionsFile = self.deviceConfig.getCPEFieldViaPlatform(cpePlatform, "screenRegions")
            captureRegions = self.config.decodeConfigIntoDictionary("./{}".format(captureRegionsFile))
            self.capture.setRegions( captureRegions )
        else:
            self.log.warn("screenRegions not setup")

        # Support for webpage control.
        self.webDriverConfig = self.config.rackConfig.get("webpageDriver")
        if self.webDriverConfig != None:
            self.webpageController = webpageController(self.log, self.webDriverConfig)
        else:
            self.log.warn("webpageController not setup")

        # Process the incoming build configurations
        if self.config.buildConfig:
            self.buildConfig = self.processBuildConfiguration(self.config.buildConfig)

        if self.config.overrideCpeConfig:
            self.overrideCpeConfig = self.processBuildConfiguration(self.config.overrideCpeConfig)

    def addDelimiter( self, path ):
        """Add delimiter to the path if required.

        Args:
            path (str): Path to add delimiter.

        Returns:
            str: Path with added delimiter if required.
        """
        delimiter = self.logConfig.get("delimiter")
        if path[-1] == delimiter:
            return path
        path += delimiter
        return path

    def constructLogPath(self, rackName, slotName):
        """Construct the path required for all logs.

        Args:
            rackName (str): Name of the rack.
            slotName (str): Name of the slot.

        Returns:
            str: Constructed log path.
        """
        #Check if the summary path was previous set, if so then we take that one instead of our new one
        if self.summaryLog.path != None:
            logPath = self.summaryLog.path
            return logPath

        time = datetime.datetime.now().strftime("%Y%m%d-%H-%M-%S")

        logPath = self.addDelimiter(  self.logConfig.get("directory") )
        logPath += self.addDelimiter( rackName )
        logPath += self.addDelimiter( slotName )
        logPath = self.addDelimiter( logPath + time )
        self.summaryLog.path = logPath

        try:
            os.makedirs(logPath, exist_ok = True )
            self.log.debug("Directory '{}' created successfully".format(logPath))
        except OSError as error:
            self.log.error("Directory '{}' can not be created".format(logPath))
        return logPath
   
    def constructTestPath(self):
        """Construct the path required for all test logs.

        Returns:
            str: Constructed test log path.
        """
        testPath = self.addDelimiter( self.logPath + self.testName + "-" + self.qcId )
        try:
            os.makedirs(testPath, exist_ok = True )
            self.log.debug("Directory '{}' created successfully".format(testPath))
            screenImagesPath = self.addDelimiter( testPath + "screenImages")
            os.makedirs(screenImagesPath, exist_ok = True )
        except OSError as error:
            self.log.error("Directory '{}' can not be created".format(testPath))
        return testPath
    
    def waitForBoot(self):
        """Wait for the system to boot.

        Returns:
            bool: True if system booted, False otherwise.
        """
        return True
    
    def testFunction(self):
        """Execute the main actions for performing the test.

        Should be overloaded in the test script to contain the main actions executed during the test.

        Returns:
            bool: True if test passes, False otherwise.
        """
        return True

    def testPrepareFunction(self):
        """Execute the pre-test setup.

        Should be overloaded in the test script to execute all necessary pre-test setup.

        Returns:
            bool: True if pre-test setup succeeds, False otherwise.
        """
        return True
    
    def testEndFunction(self, powerOff=True):
        """Close device sessions and release test resources.

        Args:
            powerOff (bool, optional): Whether to power off after the test. Defaults to True.

        Returns:
            bool: True if cleanup succeeds, False otherwise.
        """
        self.session.close()
        if powerOff:
           self.powerControl.powerOff()
        if self.webpageController is not None:
            self.webpageController.closeBrowser()
        if self.capture is not None:
            self.capture.stop()
        return True

    def testExceptionCleanUp(self):
        """Clean up test if required.

        Should be overloaded in the test script.
        """
        return

    def waitSeconds(self, seconds, startMessage=True, endMessage=False):
        """Sleep the test for a number of seconds.

        Args:
            seconds (int): Number of seconds to wait.
            startMessage (bool, optional): Display a start message. Defaults to False.
            endMessage (bool, optional): Display an end message. Defaults to False.
        """
        if ( True == startMessage ):
            self.log.info("waitSeconds["+str(seconds)+"]")
        if ( 0 != seconds ):
            time.sleep(seconds)
        if ( True == endMessage ):
            self.log.info("Waited:[" + str(seconds) + "]")    

    def waitForSessionMessage(self, message):
        """Wait for the given message in the session.

        Args:
            message (str): Message to wait for.

        Returns:
            bool: True if message found, False otherwise.
        """
        self.log.step( "testControl.waitForSessionMessage("+message+")" )
        #return self.session.read_until(message)
        try:
            string = self.session.read_until(message)
            findStringLocation=string.find(message)
            if findStringLocation == -1:
                self.log.error("Could not find string: {} ,raise an exception".format(message))
                raise Exception(" raise an exception")
                return False
        except Exception as e:
            self.log.error(e)
            raise Exception('Waitfor session message - {} failed'.format(message))
        return True

    def writeMessageToSession(self,message):
        """Write a message to the current session.

        Args:
            message (str): Message to write to the session.
        """
        self.log.step( "testControl.writeMessageToSession({})".format(message.strip()) )
        self.session.write(message)

    def programOutboundWithValidImage( self, sourceImageType,  destinationImageType = None ):
        """Program an image from the valid list based on platform.

        Args:
            sourceImageType (str): Source image type.
            destinationImageType (str, optional): Destination image type. Defaults to None.

        Returns:
            bool: True if programming succeeds, False otherwise.
        """
        platform = self.slotInfo.getPlatform()
        if destinationImageType == None: 
            destinationImageType = sourceImageType
        url = self.deviceConfig.getValidImageUrlViaPlatform( sourceImageType, platform )
        result = self.outboundClient.prepareOutboundWithImageFromUrl( destinationImageType, url )
        return result

    def processBuildConfiguration(self, inputUrl):
        """Download and retrieve information from a config file.

        Args:
            inputUrl (str): Location of the config file.

        Returns:
            dict: Decoded dictionary from the config file.
        """
        self.log.step("testControl.processBuildConfiguration")
        try:
            self.outboundClient.downloadFile(inputUrl)
            workspaceFolder = self.deviceConfig.getWorkspaceDirectory()
            fileName = os.path.basename(inputUrl)
            inputPath = os.path.join(workspaceFolder, fileName)
            outputDict = self.config.decodeConfigIntoDictionary(inputPath)
        except Exception as e:
            raise Exception("testControl.processBuildConfiguration returns error - {}".format(e))
        return outputDict

    def validatePlatform(self, platform):
        """Validate the platform against platform and alternative platform.

        Args:
            platform (str): Platform to validate.

        Returns:
            bool: True if platform is valid, False otherwise.
        """
        self.log.info("validatePlatform - {}".format(platform))
        if platform == self.buildConfig['platform']:
            return True
        alternativePlatform = self.deviceConfig.getAlternativePlatform()
        if platform in alternativePlatform:
            return True
        return False
 
    def run(self, powerOff=True):
        """Run the test.

        Args:
            powerOff (bool, optional): Whether to turn off power after the test. Defaults to True.

        Returns:
            bool: True if test passes, False otherwise.
        """
        self.session.open()

        result = self.waitForBoot()
        if ( result == False ):
            self.log.stepResult( result, "could not communicate or start test" )
            return False
        
        end_time = self.summaryLog.testStart( self.testName, self.qcId, self.loopCount, self.maxRunTime )
        self.log.testStart( self.testName, self.qcId, self.loopCount, self.maxRunTime )
        # Run the testPrepare function
        self.log.info( logModule.SEPERATOR+"testPrepareFunction()"+logModule.SEPERATOR )
        self.log.indent()
        iterations = 1
        result = self.testPrepareFunction()
        showLoopCount = True
        if ( self.loopCount == 1 ):
            showLoopCount = False
        self.log.outdent()
        if (result == True):
            # Use "finish" variable in case there are other reasons to quit apart from end of test, although note simple
            #  keyboard polling is troublesome in Python hence the simpler addition of a ^C handler
            finish=False
            
            while finish==False:
                if (0 != self.maxRunTime):
                    if (datetime.datetime.now() >= end_time):
                        break
                if showLoopCount:
                    self.log.testLoop( iterations )
                # Script log file init
                
                try:
                    result = self.testFunction()
                except Exception as e:
                    self.log.step('testControl - Invoking testExceptionCleanUp')
                    self.log.critical(str(e))
                    try:
                        self.testExceptionCleanUp()
                        self.utils.wait(2)
                    except Exception as e:
                        self.log.step('Exception while running testExceptionCleanUp')
                        self.log.critical(str(e))
                    self.log.debug("************************")
                    self.log.debug(str(inspect.stack()))
                    exception = traceback.format_exc()
                    exceptionDict = self.parseException(exception)
                    self.log.stepResult( False, "Exception in stage. '{}' in method '{}' of file {} line {}".format(exceptionDict.get("exception"), exceptionDict.get("method"), exceptionDict.get("file"), exceptionDict.get("line")))
                    break
                if result == False:
                    break
                if showLoopCount:
                    self.log.testLoopComplete( iterations )
                if self.loopCount != 0:
                    if iterations >= self.loopCount:
                        break
                iterations=iterations+1

        self.log.testResult("[{}] : Test Completed".format(self.testName) )
        self.summaryLog.failedSteps = self.log.failedSteps
        self.summaryLog.totalStepsFailed += self.log.totalStepsFailed
        self.summaryLog.totalStepsPassed += self.log.totalStepsPassed
        self.summaryLog.totalSteps += self.log.totalSteps
        self.summaryLog.testResult("[{}] : Test Completed".format(self.testName) )
        self.testEndFunction(powerOff)
        self.utils.wait(2)

        return result

    def parseException(self, exception):
        """Parse an exception into a dictionary.

        Args:
            exception (str): Exception generated by traceback.format_exc().

        Returns:
            dict: Dictionary containing parsed exception information.
        """
        lines = exception.split("\n")
        exceptionInfo = {}
        lastFileIndex = None
        # Finds the last line of the execption that has'File "' in to then parse the information from the following lines
        for index, line in enumerate(lines):
            if "File \"" in line:
                lastFileIndex = index

        exceptionInfo["exception"] = lines[lastFileIndex + 2]
        fileLineWords = lines[lastFileIndex].strip().split(" ")
        try:
            fileIndex = fileLineWords.index('File')+1
            exceptionInfo["file"] = fileLineWords[fileIndex].replace(",", "")
        except IndexError:
            raise ValueError("Incorrect format of exception, expected 'File' on 3rd last line")
        
        try:
            lineNumIndex = fileLineWords.index('line')+1
            exceptionInfo["line"] = fileLineWords[lineNumIndex].replace(",", "")
        except IndexError:
            raise ValueError("Incorrect format of exception, expected 'line' on 3rd last line")

        try:
            methodIndex = fileLineWords.index('in')+1
            exceptionInfo["method"] = fileLineWords[methodIndex]
        except IndexError:
            raise ValueError("Incorrect format of exception, expected 'in' on 3rd last line")

        return exceptionInfo


    
    def signal_handler(self, signal, frame):
        """Signal handler support for CTRL-C.

        Args:
            signal (_type_): Signal input.
            frame (_type_): Signal frame.
        """
        #result = True
        self.log.info( "signal_handler [{}]".format(frame) )
        self.testEndFunction()
        sys.exit(1)

    def runHostCommand(self, command, supressErrors=False, supressOutput=False, supress=False):
        """Run a host command.

        Args:
            command (_type_): Command to run.
            suppressErrors (bool, optional): Suppress all errors. Defaults to False.
            suppressOutput (bool, optional): Suppress the output. Defaults to False.
            suppress (bool, optional): Suppress both errors and output. Defaults to False.

        Returns:
            _type_: Any errors listed.
        """
        self.log.debug( command )
        args = shlex.split( command )
        errors = None
        output = None
        if ( True == supress ):
            supressErrors = True
            supressOutput = True
        if ( True == supressErrors ):
            errors = subprocess.STDOUT
        if ( True == supressOutput ):
            output = subprocess.DEVNULL
        proc = subprocess.Popen( args, stderr=errors, stdout=output )
        try:
            errs = proc.communicate(timeout=15)
        except: 
            proc.kill()
            errs = proc.communicate()
            self.log.fatal( command + " Failed : ["+str(errs)+"]")
        return errs

    def syscmd(self, cmd, encoding='', returnCode=False):
        """Run a command on the system.

        Args:
            cmd (str): Command to run.
            encoding (str, optional): Encoding required. Defaults to ''.
            returnCode (bool, optional): Check for return codes. Defaults to False.

        Returns:
            str or int: Command result or return code.
        """
        stdout, exitCode = utilities(self.log).syscmd(cmd, encoding=encoding)
        self.output = stdout
        if ( True == returnCode ):
            return exitCode
        if len(self.output) > 1:
            if encoding: 
                return self.output.decode(encoding)
            else: 
                return self.output
        return exitCode
    

    def pingTest(self, deviceName="dut", logPingTime=False):
        """Perform a ping test against the given device.

        Args:
            deviceName (str, optional): Device from the configuration to ping. Defaults to "dut".
            logPingTime (bool, optional): Log ping time. Defaults to False.

        Returns:
            bool: True if host is up, False otherwise.
        """
        #Ping the box till the box responds after the boot
        self.alive = self._pingTestOnly(deviceName)
        return self.alive

    def _pingTestOnly(self, deviceName="dut", logPingTime=False):
        """Perform a ping test against the given device.

        Args:
            deviceName (str, optional): Device from the configuration to ping. Defaults to "dut".

        Returns:
            bool: True if host is up, False otherwise.
        """
        device = self.devices.getDevice(deviceName)
        return device.pingTest(logPingTime)

    def waitForPrompt(self, prompt=None):
        """Wait for the prompt to denote that the target is booted.

        Args:
            prompt (str, optional): Prompt to wait for. Defaults to None.

        Returns:
            bool: True if prompt found, False otherwise.
        """
        if prompt == None:
            prompt = self.getCPEFieldValue("prompt")
        self.writeMessageToSession("\n")
        result = self.waitForSessionMessage(prompt)
        return result
