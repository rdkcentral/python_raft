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
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core
#*   ** @file        : logModule.py
#*   ** @date        : 17/01/2019
#*   **
#*   ** @brief : Logger wrapper for standing testing output for logging.
#*   **
#* ******************************************************************************

import os
from io import IOBase
import logging
from threading import Thread
import time
import datetime
#from datetime import datetime
from os import path

from enum import Enum

from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, FATAL

class logModule():
    TEST_RESULT = 99
    FATAL = 100
    moduleName = ""
    SEPERATOR=     " ---- "
    SEPERATOR_STAR=" **** "
    LARGE_SEPERATOR = "=================================================="
    INDENT_DEFAULT="  "
    indentString=""
    DEBUG=DEBUG
    INFO=logging.INFO
    WARNING=WARNING
    ERROR=ERROR
    CRITICAL=CRITICAL
    FATAL=FATAL
    STEP=INFO+1
    STEP_START=INFO+2
    TEST_START=INFO+3
    STEP_RESULT=INFO+4  # Here or above you can just display results
    TEST_RESULT=INFO+5
    TEST_SUMMARY=INFO+6
    RESULT = STEP_RESULT

    def __init__(self, moduleName, level=INFO):
        """
        Initialises the log module.

        Args:
            moduleName (str): Name of the module.
            level (int, optional): Logging level. Defaults to INFO.
        """
        # Initialize python logger
        self.log = logging.getLogger(moduleName)
        self.moduleName = moduleName

        # Console Handler
        self.format = logging.Formatter('%(asctime)-15s, %(name)s, %(levelname)-12s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S' )
        self.logConsole = logging.StreamHandler()
        self.logConsole.setFormatter( self.format )
        self.log.addHandler( self.logConsole )
        self.log.setLevel(level)
        self.csvLogger = logging.getLogger(self.moduleName+"csv")
        self.csvLogger.setLevel( logging.DEBUG )

        # Add some extra levels
        logging.addLevelName( self.TEST_START, "TEST_START" )
        logging.addLevelName( self.TEST_RESULT, "TEST_RESULT" )
        logging.addLevelName( self.TEST_SUMMARY, "TEST_SUMMARY" )
        logging.addLevelName( self.STEP, "STEP" )
        logging.addLevelName( self.STEP_START, "STEP_START" )
        logging.addLevelName( self.STEP_RESULT, "STEP_RESULT" )
        logging.addLevelName( self.FATAL, "FATAL" )

        self.log.debug('logModule: '+moduleName)
        self.stepNum = 1
        self.summaryQcID = ""
        self.summaryTestName = ""
        self.summaryTestTotal = 0
        self.summaryTestsFailed = 0
        self.summaryTestsPassed = 0
        self.totalStepsFailed = 0
        self.totalStepsPassed = 0
        self.totalSteps = 0
        self.testDuration = 0
        self.stepNum = 0
        self.testCountActive = 0
        self.path = None
        self.logFile = None
        self.csvLogFile = None
        self._loggingThreads = {}

    def __del__(self):
        """Deletes the logger instance.
        """
        while self.log.hasHandlers():
            self.log.removeHandler(self.log.handlers[0])

    def setFilename( self, logPath, logFileName ):
        """
        Sets the filename for logging.

        Args:
            logPath (str): The path to write log files.
            logFileName (str): The name of the log file.
        """
        if self.logFile != None:
            #Log file already set don't set a new one
            return
        self.logPath = logPath
        logFileName = os.path.join(logPath + logFileName)
        self.logFile = logging.FileHandler(logFileName)
        self.logFile.setFormatter( self.format )
        self.log.addHandler( self.logFile )
        #Create the CSV Logger module
        self.csvLogFile = logging.FileHandler( logFileName+".csv" )
        self.csvLogger.addHandler( self.csvLogFile )
        self.csvLogger.info("QcId, TestName, Result, Failed Step, Failure, Duration [hh:mm:ss]")
        self.log.info( "Log File: [{}]".format(logFileName) )

    def fatal(self, message,*args, **kws):
        """
        Logs a fatal error and exits the program.

        Args:
            message (str): The message to log.
            *args: Additional positional arguments.
            **kws: Additional keyword arguments.
        """
        self.log._log(self.FATAL, self.indentString+str(message), args, **kws)
        os._exit(1)

    def warn(self,message,extra=None):
        """
        Logs a warning message.

        Args:
            message (str): The message to log.
            extra (Any, optional): Additional information to include. Defaults to None.
        """
        self.log.warning(self.indentString+str(message),extra=extra)

    def error(self,message,extra=None):
        """
        Logs an error message.

        Args:
            message (str): The message to log.
            extra (Any, optional): Additional information to include. Defaults to None.
        """
        self.log.error(self.indentString+str(message),extra=extra)

    def critical(self,message,extra=None):
        """
        Logs a critical message.

        Args:
            message (str): The message to log.
            extra (Any, optional): Additional information to include. Defaults to None.
        """
        self.log.critical(self.indentString+str(message),extra=extra)

    def debug(self,message,extra=None):
        """
        Logs a debug message.

        Args:
            message (str): The message to log.
            extra (Any, optional): Additional information to include. Defaults to None.
        """
        self.log.debug(self.indentString+str(message),extra=extra)

    def info(self,message,extra=None):
        """
        Logs an info message.

        Args:
            message (str): The message to log.
            extra (Any, optional): Additional information to include. Defaults to None.
        """
        self.log.info(self.indentString+str(message),extra=extra)

    def stepMessage(self,message,*args, **kws):
        """
        Logs a step message.

        Args:
            message (str): The message to log.
            extra (Any, optional): Additional information to include. Defaults to None.
        """
        self.log._log(self.STEP, message, args, **kws)

    def stepStartMessage(self,message,*args, **kws):
        """
        Logs a step start message.

        Args:
            message (str): The message to log.
            extra (Any, optional): Additional information to include. Defaults to None.
        """
        self.log._log(self.STEP_START, message, args, **kws)

    def stepResultMessage(self,message,*args, **kws):
        """
        Logs a step result message.

        Args:
            message (str): The message to log.
            extra (Any, optional): Additional information to include. Defaults to None.
        """
        self.log._log(self.STEP_RESULT, message, args, **kws)

    def testStartMessage(self,message,*args, **kws):
        """
        Logs a test start message.

        Args:
            message (str): The message to log.
            extra (Any, optional): Additional information to include. Defaults to None.
        """
        self.log._log(self.TEST_START, message, args, **kws)

    def testResultMessage(self,message,*args, **kws):
        """
        Logs a test result message.

        Args:
            message (str): The message to log.
            extra (Any, optional): Additional information to include. Defaults to None.
        """
        self.log._log(self.TEST_RESULT, message, args, **kws)

    def testSummaryMessage(self,message,*args, **kws):
        """
        Logs a test summary message.

        Args:
            message (str): The message to log.
            extra (Any, optional): Additional information to include. Defaults to None.
        """
        self.log._log(self.TEST_SUMMARY, message, args, **kws)

    def setLevel( self, level ):
        """
        Sets the logging level for the logger.

        Args:
            level (int): The logging level to set.
        """
        self.log.setLevel( level )

    def message( self, level, output, extra=None):
        """
        Logs a message with the specified logging level.

        Args:
            level (int): The logging level.
            output (str): The message to log.
            extra (Any, optional): Additional information to include. Defaults to None.
        """
        levelFunctions = {
            DEBUG: self.debug,
            INFO: self.info,
            STEP: self.step, # type: ignore
            WARNING: self.warning,
            ERROR: self.error,
            FATAL: self.fatal,
            CRITICAL: self.critical
        }
        func = levelFunctions.get( level )
        return func( output, extra )

    def indent( self, string=INDENT_DEFAULT):
        """
        Pushes an indentation prefix.

        Args:
            string (str, optional): The string used for indentation. Defaults to INDENT_DEFAULT.

        Returns:
            bool: False
        """
        #indentLength = len(self.indentString)
        self.indentString=self.indentString+string
        #indentLength = len(self.indentString)
        return False

    def outdent(self, string=INDENT_DEFAULT):
        """
        Pops an indentation prefix.

        Args:
            string (str, optional): The string used for indentation. Defaults to INDENT_DEFAULT.

        Returns:
            bool: True if successful, False otherwise.
        """
        indentLength = len(self.indentString)
        stringLength = len(string)
        if ( indentLength <= stringLength):
            self.indentString=""
            return False
        self.indentString=self.indentString[0:indentLength-stringLength]
        indentLength = len(self.indentString)
        return True

    def testStart(self, testName, qcId, loops=1, maxRunTime=(60*24) ):
        """
        Starts a test.

        Args:
            testName (str): The name of the test.
            qcId (str): The QC ID of the test.
            loops (int, optional): The number of loops for the test. Defaults to 1.
            maxRunTime (int, optional): The maximum runtime for the test in minutes. Defaults to 1440.

        Returns:
            datetime: The end time of the test.
        """
        self.testName=testName
        self.qcId = qcId
        self.loopCount = loops
        self.maxRunTime = maxRunTime
        self.stepNum=0
        self.failedSteps = {"":""}

        if self.testCountActive == 0:
            self.summaryTestTotal = 0
            self.summaryTestsPassed = 0
            self.summaryTestsFailed = 0
            self.summaryTestName = testName
            self.summaryQcID = qcId
        self.testCountActive += 1
        self.summaryTestTotal += 1
        self.totalSteps = 0
        self.totalStepsPassed = 0
        self.totalStepsFailed = 0

        self.start_time = datetime.datetime.now()
        self.end_time = self.start_time + datetime.timedelta(minutes=self.maxRunTime)
        durationTime = self.end_time - self.start_time
        self.timeFormat = "%Y-%m-%d %H:%M:%S"

        message = logModule.SEPERATOR + "Run Test [" + self.testName + "], qcId:[" + self.qcId + "] Duration:["+str(self.maxRunTime)+"]:["+str(durationTime)+"], LoopCount:["+str(self.loopCount)+"]"+logModule.SEPERATOR
        self.testStartMessage( message )

        if ( 0 != self.maxRunTime ):
            self.log.info( logModule.SEPERATOR+"Start Time: ["+ self.start_time.strftime(self.timeFormat) + "], Max Run End Time: ["+ self.end_time.strftime(self.timeFormat) + "]"+logModule.SEPERATOR )
        else:
            self.log.info( logModule.SEPERATOR+"Start Time: ["+ self.start_time.strftime(self.timeFormat) + "]"+logModule.SEPERATOR )
        self.testStartTime = datetime.datetime.now()
        self.testActive = True
        return self.end_time

    def testLoop(self, loopIndex):
        """
        Starts a test loop.

        Args:
            loopIndex (int): The index of the test loop.
        """
        self.step(logModule.SEPERATOR_STAR+"Test Loop:[" + str(loopIndex) + "], Start Time: ["+self.testStartTime.strftime(self.timeFormat)+"]" )
        #self.indent()

    def testLoopComplete(self, loopIndex):
        """
        Marks the completion of a test loop.

        Args:
            loopIndex (int): The index of the completed test loop.
        """
        #self.outdent()
        loopEndTime = datetime.datetime.now()
        loopDuration = loopEndTime - self.testStartTime
        message = logModule.SEPERATOR_STAR+"Completed Loop ["+str(loopIndex)+"], End Time:"+ loopEndTime.strftime(self.timeFormat) + "], Duration:["+str(loopDuration)+"]"
        self.step( message )
        self.loopStartTime = None

    def testResult(self, message):
        """
        Logs the result of a test.

        Args:
            message (str): The result message.
        """
        if self.testCountActive >= 1:
            self.testCountActive -= 1

#        if self.testCountActive != 0:
        testEndTime = datetime.datetime.now()
        testDuration = testEndTime - self.testStartTime
        self.testDuration = testDuration
        #message = "loopCount ["+str(self.loopCount)+"], End Time:["+ testEndTime.strftime(self.timeFormat) + "], Duration:["+str(testDuration)+"]"
        #self.step( message )

        self.step("====================Result====================", showStepNumber=False)
        #self.log._log( self.TEST_RESULT, str(result.value) +':('+ result.name + ') '+message, args, **kws )
        if self.totalStepsFailed != 0:
            resultMessage = "FAILED"
            self.summaryTestsFailed += 1
        else:
            resultMessage = "PASSED"
            self.summaryTestsPassed += 1
        message = "[{}]: {}".format(resultMessage,message)

        self.testResultMessage(message)
        if self.testCountActive == 0:
            # Cater for the case where there is a test 
            if self.summaryTestsFailed + self.summaryTestsPassed == self.summaryTestTotal-1:
                self.summaryTestTotal -= 1
            message = "testName: [{}], qcId:[{}] Tests: Total:[{}]: Passed:[{}] Failed:[{}] Duration:[{}]".format(self.summaryTestName, self.summaryQcID, self.summaryTestTotal,self.summaryTestsPassed,self.summaryTestsFailed, str(testDuration) )
            self.testSummaryMessage(message)
            self.step("====================End Of Test====================\r\n", showStepNumber=False)
            self.testCountActive = 0
            self.csvLogger.info("{},{},{},{},{},{}". format(self.summaryQcID, self.summaryTestName, resultMessage, list(self.failedSteps.keys())[-1], list(self.failedSteps.values())[-1], str(testDuration)) )
        else:
            self.csvLogger.info("{},{},{},{},{},{}". format(self.qcId, self.testName, resultMessage, list(self.failedSteps.keys())[-1], list(self.failedSteps.values())[-1], str(testDuration)) )

    def stepStart(self, message, expected=None):
        """
        Starts a step in the test.

        Args:
            message (str): The description of the step.
            expected (Any, optional): The expected outcome of the step. Defaults to None.
        """
        self.totalSteps += 1
        self.stepNum += 1
        self.step("====================Step Start====================", showStepNumber=False)
        self.stepStartMessage("[{}]: DESCRIPTION : {}".format(self.stepNum, message))
        if expected is not None:
            self.step("EXPECTED : {}".format(expected))
        self.step(self.LARGE_SEPERATOR, showStepNumber=False)
        #self.indent()

    def step(self, message, showStepNumber=True):
        """
        Logs a step in the test.

        Args:
            message (str): The message to log.
            showStepNumber (bool, optional): Whether to show the step number. Defaults to True.
        """
        output = "[{}]: {}{}".format(self.stepNum, self.indentString, message)
        if showStepNumber == False:
            output = "{}{}".format(self.indentString,message)
        self.stepMessage( output )

    def stepResult(self, result, message):
        """
        Logs the result of a step in the test.

        Args:
            result (bool): The result of the step.
            message (str): The result message.
        """
        #self.outdent()
        if result == True:
            resultMessage = "PASSED"
            self.totalStepsPassed += 1
        else:
            resultMessage = "FAILED"
            self.totalStepsFailed += 1
            self.failedSteps[self.stepNum] = message
        message = "[{}]: RESULT : [{}]: {}".format(self.stepNum,resultMessage, message)
        self.step("=====================Step End======================",showStepNumber=False)
        self.stepResultMessage(message)

    def logStreamToFile(self, inputStream: IOBase, outFileName: str) -> None:
        """
        Starts a new thread to write the contents of an input stream to a file.

        Args:
            inputStream (IOBase): The input stream to be read from.
            outFileName (str): The path of the output file where the stream data will be written.
                                If only a file name is given, the file will be written in the current tests log directory.
        """
        outPath = path.join(self.logPath,outFileName)
        if path.isabs(outFileName):
            outPath = outFileName
        newThread = Thread(target=self._writeLogFile,
                                        args=[inputStream, outPath],
                                        daemon=True)
        
        self._loggingThreads.update({outFileName: newThread})
        newThread.start()

    def stopStreamedLog(self, outFileName: str) -> None:
        """
        Stops a previously started thread that is writing to a log file.

        Args:
            outFileName (str): The path of the output file associated with the thread to be stopped.

        Raises:
            AttributeError: If the specified thread cannot be found.
        """
        log_thread = self._loggingThreads.get(outFileName)
        if log_thread:
            log_thread.join(timeout=30)
        else:
            raise AttributeError(f'Could not find requested logging thread to stop. [{outFileName}]')

    def _writeLogFile(self,streamIn: IOBase, logFilePath: str) -> None:
        """
        Writes the input stream to a log file.

        Args:
            stream_in (IOBase): The stream from a process.
            logFilePath (str): File path to write the log out to.
        """
        while True:
            chunk = streamIn.readline()
            if chunk == '':
                break
            with open(logFilePath, 'a+',) as out:
                out.write(chunk)

    def __del__(self):
        for thread in self._loggingThreads.values():
            thread.join()