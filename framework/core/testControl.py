#!/usr/bin/env python3
#** ******************************************************************************
#* Copyright (C) 2019 Sky group of companies, All Rights Reserved
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
        delimiter = self.logConfig.get("delimiter")
        if path[-1] == delimiter:
            return path
        path += delimiter
        return path

    def constructLogPath(self, rackName, slotName):
        """Construct the path required for all Logs

            localLogs/
            └── rackName
                └── slotName 
                    └── 210629-10:00:00.0000 -> logPath
            since the directory has the time in it to the second it's unique  

        Args:
        Returns:
            [string]: [string with added delimiter if required]
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
        """Construst the path required for all Logs

            localLogs/
            └── rackName
                └── slotName -> logPath
                    └── 210629-10:00:00.0000 -> logPath
                        └── testName:xx-testId:xx -> testPath
                            ├── serial.log
                            └── test.log
            since the directory has the time in it to the second it's unique  

        Args:
        Returns:
            [string]: [string with added delimiter if required]
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
        """[wait for the system to boot]
            Actual functionality is depending on the parent class 
        Returns:
            [bool]: [True if system booted]
        """
        return True
    
    def testFunction(self):
        """Executes the main actions for performing the test.

        Should be overloaded in the test script to contain the main actions executed during the rest. Is run in stressTest.run()
        
        Returns:
            True / False 
        """ 
        return True

    def testPrepareFunction(self):
        """Executes the pre-test setup

        Should be overloaded in the test scrip to execute all necessary pre-test setup. Is run in stressTest.run() and is not part of the main test loop.
        
        Returns:
            True / False
        """
        return True
    
    def testEndFunction(self, powerOff=True):
        """Close device sessions and release the resources used for test execution
        Args:
            powerOff( bool ): Default True, power off after test
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
        """Cleans up a test if required by the test
        """
        return

    def waitSeconds(self, seconds, startMessage=True, endMessage=False):
        """Sleep the test for a number of seconds

        Args:
            seconds (_type_): number of sections to wait
            startMessage (bool, optional): display a start message. Defaults to False.
            endMessage (bool, optional): display an end message. Defaults to False.
        """
        if ( True == startMessage ):
            self.log.info("waitSeconds["+str(seconds)+"]")
        if ( 0 != seconds ):
            time.sleep(seconds)
        if ( True == endMessage ):
            self.log.info("Waited:[" + str(seconds) + "]")    

    def waitForSessionMessage(self, message):
        """User friendly function to Wait for the given message or timeout as required

        Args:
            message ([string): [message to wait for]

        Returns:
            result (boolean)
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
        """User friendly function to write a message to the current session

        Args:
            message ([string]): [Write to the session]
        """
        self.log.step( "testControl.writeMessageToSession({})".format(message.strip()) )
        self.session.write(message)

    def programOutboundWithValidImage( self, sourceImageType,  destinationImageType = None ):
        """program an image from the valid list based on platform

        Args:
            sourceImageType ([string]): [PCI1, PCI2, PDRI, BDRI etc. based on test_config.yml image types ]
            destinationImageType ([string]): [PCI1, PCI2, PDRI, BDRI etc.]
        """
        platform = self.slotInfo.getPlatform()
        if destinationImageType == None: 
            destinationImageType = sourceImageType
        url = self.deviceConfig.getValidImageUrlViaPlatform( sourceImageType, platform )
        result = self.outboundClient.prepareOutboundWithImageFromUrl( destinationImageType, url )
        return result

    def processBuildConfiguration(self, inputUrl):
        """Downloads and retrives information from config file at inputUrl

        Args:
            inputUrl (url) - location of config file

        Returns:
            outputDict (dict) - dictionary decoded from config file
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
        """Validate the platform by comparing it against platform and alternative platform

        Args:
            platform (str)

        Returns:
            result (boolean)
        """
        self.log.info("validatePlatform - {}".format(platform))
        if platform == self.buildConfig['platform']:
            return True
        alternativePlatform = self.deviceConfig.getAlternativePlatform()
        if platform in alternativePlatform:
            return True
        return False
 
    def run(self, powerOff=True):
        """
        Run the test
        Check if the box is alive, before we start our testing. If the box hasn't responded at this point we, cannot run the test.
        Args:
            powerOff (bool, optional): don't turn off the power after the test completes. Defaults to True.

        Returns:
            _type_: TRUE - on test pass, otherwise failure
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
        """Parses an exception into the a dictionary to get the, exception thrown and the file, line and method it was thrown on

        Args:
            exception (String): An exception as generated by traceback.format_exc()

        Returns:
            dict: _description_
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
        """Signal handler support for CTRL-C

        Args:
            signal (_type_): signal input
            frame (_type_): signal frame
        """
        #result = True
        self.log.info( "signal_handler [{}]".format(frame) )
        self.testEndFunction()
        sys.exit(1)

    def runHostCommand(self, command, supressErrors=False, supressOutput=False, supress=False):
        """Run a host command

        Args:
            command (_type_): command to run
            supressErrors (bool, optional): suppress all errors. Defaults to False.
            supressOutput (bool, optional): suppress the output. Defaults to False.
            supress (bool, optional): suppre. Defaults to False.

        Returns:
            _type_: anyh errors listed
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
        """ Runs a command on the system, waits for the command to finish, and then
            returns the text output of the command. If the command produces no text
            output, the command's return code will be returned instead.

        Args:
            cmd (string): command 
            encoding (str, optional): encoding required. Defaults to ''.
            returnCode (bool, optional): check for return codes. Defaults to False.

        Returns:
            string: command result
        """
        self.log.debug( "command: ["+str(cmd)+"]")
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,close_fds=True)
        p.wait()
        self.output = p.stdout.read()
        if ( True == returnCode ):
            if len(self.output) > 1:
                self.log.debug( "command: output:["+str(self.output)+"], returnCode:["+str(p.returncode)+"]")
            return p.returncode
        if len(self.output) > 1:
            if encoding: 
                return self.output.decode(encoding)
            else: 
                return self.output
        return p.returncode
    

    def pingTest(self, deviceName="dut", logPingTime=False):
    #Ping the box till the box responds after the boot
        if(logPingTime):
            self.log.step("waitForBoot( {} )".format(self.slotInfo.getDeviceAddress()))
            pingStartTime = time.time()
            timeString = time.strftime("%H:%M:%S",time.gmtime(pingStartTime))
            self.log.step("ping start time: [{}]".format(timeString) )
        self.alive = self._pingTestOnly(deviceName)
        if(logPingTime):
            elapsed_time = time.time() - pingStartTime
            timeString = time.strftime("%H:%M:%S",time.gmtime(time.time()))
            self.log.step("ping response time: [{}]".format(timeString) )
            elasped_string = time.strftime( "%H:%M:%S", time.gmtime(elapsed_time))              
            self.log.step("Time taken to get ping response: ["+elasped_string+"]")
        # We've not be able to ping the box, return an error
        if ( False == self.alive ):
            self.log.critical( "ping Up Check:[Box is not responding to ping within:"+elasped_string+"]")
            raise Exception(" ping failed")           
        return self.alive

    def _pingTestOnly(self, deviceName="dut"):
        """perform a ping test against the given device

        Args:
            deviceName (string): device from the configuration to ping 

        Returns:
            bool: TRUE - host is up, otherwise host is down
        """
        hostIsUp = False
        ip = self.slotInfo.getDeviceAddress( deviceName )
        if (platform.system().lower() == 'windows') or ('cygwin' in platform.system().lower()):
            ping_param_amount = " -n "
            ping_param_quiet = " "
        else:
            ping_param_amount = " -c "
            ping_param_quiet = " -q "
        # Quick check for ping working first time round
        command  = "ping" + ping_param_amount + "1" + ping_param_quiet + ip
        result = self.syscmd( command, returnCode=True )
        if ( 0 == result ):
            self.log.debug("ping response 1 - Host Up")
            return True
        #Host is currently down, we need to loop
        for x in range( 0, 15 ):
            self.log.debug("pingTest Inner Loop["+str(x)+"]")
            self.waitSeconds(5) # Wait 5 seconds before trying constant ping
            result = self.syscmd( "ping" + ping_param_amount + "10" + ping_param_quiet + ip, returnCode=True )
            if ( 0 == result ):
                # Check for 0% packet loss, otherwise reject it
                outputString = str(self.output)
                if ( ", 0% packet loss" in outputString ):
                    hostIsUp = True
                    self.log.debug("pingTest hostIsUp")
                    break
            self.log.debug("pingTest hostIsDown")
    
        return hostIsUp

    def waitForPrompt(self, prompt=None):
        """
           This function must wait for the first log prompt to denote that the target is booted.
           Try for every 10 seconds and read the console for the prompt. If a prompt presents, the box booted successfully, if not retry
           maximum time limit is 2 minutes and the reports box is not in proper state.
        """
        if prompt == None:
            prompt = self.getCPEFieldValue("prompt")
        self.writeMessageToSession("\n")
        result = self.waitForSessionMessage(prompt)
        return result
