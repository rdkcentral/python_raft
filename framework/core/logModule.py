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
import logging
import time
import datetime
import sys
import csv
import xml

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

    def __init__(self, moduleName, level=INFO, xml_output=True):
        """
        Initialises the log module.

        Args:
            moduleName (str): Name of the module.
            level (int, optional): Logging level. Defaults to INFO.
        """
        # Initialize python logger
        self.log = logging.getLogger(moduleName)
        self.moduleName = moduleName
        self.xml_output = xml_output

        # Console Handler
        self.format = logging.Formatter('%(asctime)-15s, %(name)s, %(levelname)-12s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S' )
        self.logConsole = logging.StreamHandler()
        self.logConsole.setFormatter( self.format )
        self.log.addHandler( self.logConsole )
        self.log.setLevel(level)
        self.csvLogger = logging.getLogger(self.moduleName+"csv")
        self.csvLogger.setLevel( logging.DEBUG )
        self.xmlLogger = logging.getLogger('xml_logger')
        self.xmlLogger.setLevel( logging.DEBUG )

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
        self.xmlLogFile = None

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

        # Create the XML Logger module
        self.xmlLogFile = logging.FileHandler(logFileName + ".xml")
        self.xmlLogFile.setLevel(logging.INFO)
        formatter = logging.Formatter('<log>%(message)s</log>')  # XML format
        self.xmlLogFile.setFormatter(formatter)
        self.xmlLogger.addHandler(self.xmlLogFile)
        self.xmlLogger.info("QcId, TestName, Result, Failed Step, Failure, Duration [hh:mm:ss]")
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

        if self.totalStepsFailed > 0:
            failed_steps_message = "Failed Steps:"
            for step_num, step_message in self.failedSteps.items():
                failed_steps_message += f"\nStep {step_num}: {step_message}"
            self.log.error(failed_steps_message)

        if self.testCountActive == 0:
            # Cater for the case where there is a test 
            if self.summaryTestsFailed + self.summaryTestsPassed == self.summaryTestTotal-1:
                self.summaryTestTotal -= 1
            message = "testName: [{}], qcId:[{}] Tests: Total:[{}]: Passed:[{}] Failed:[{}] Duration:[{}]".format(self.summaryTestName, self.summaryQcID, self.summaryTestTotal,self.summaryTestsPassed,self.summaryTestsFailed, str(testDuration) )
            self.testSummaryMessage(message)
            self.step("====================End Of Test====================\r\n", showStepNumber=False)
            self.testCountActive = 0
            
            self.csvLogger.info("{},{},{},{},{},{}". format(self.summaryQcID, self.summaryTestName, resultMessage, list(self.failedSteps.keys())[-1], list(self.failedSteps.values())[-1], str(testDuration)) )
        
            if self.xml_output:
                with open(self.xmlLogFile.baseFilename, "a") as xml_file:
                    xml_file.write(f'<testcase classname="{self.moduleName}.{self.summaryTestName}" name="{self.summaryQcID} - {self.summaryTestName}" time="{testDuration.total_seconds()}" >\n')
                    if resultMessage == "FAILED":
                        xml_file.write(f'   <error message="test failure">failure - {self.failedSteps[self.stepNum]}, failure step - {list(self.failedSteps.keys())[-1]}\n</error>\n')
                    xml_file.write('</testcase>\n')

        else:
            self.csvLogger.info("{},{},{},{},{},{}". format(self.qcId, self.testName, resultMessage, list(self.failedSteps.keys())[-1], list(self.failedSteps.values())[-1], str(testDuration)) )
            
            if self.xml_output:
                with open(self.xmlLogFile.baseFilename, "a") as xml_file:
                    xml_file.write(f'<testcase classname="{self.moduleName}.{self.testName}" name="{self.qcId} - {self.testName}" time="{testDuration.total_seconds()}" />\n')

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
            

    # def buildXml(fileName, testSuite=None, xml_output=True):
    #     # log = logModule("buildXml", logModule.INFO, xml_output)  # Initialize logModule for logging

    #     if not fileName.endswith(".xml"):
    #         fileName = fileName + ".xml"
            
    #     fails = 0

        
    #     data = []
    #     with open(fileName, "r") as file:
    #         for line in file:
    #             data.append(line.strip())  #to remove leading/trailing whitespaces
        
    #     for row in data:
    #         if row.get("Result") == "FAILED":
    #             fails += 1 

    #     log.info(f'Writing results to file "{fileName}" in Jenkins XML format')

    #     with open(fileName, 'w') as xmlFile:
    #         xmlFile.write(f'<testsuite name="{testSuite}" failures="{fails}" tests="{len(data)}">\n')
    #     #     xmlFile.write(f"""
    #     # <properties>
    #     #     <property name="TestAgent" value="{testAgent}"/>
    #     # </properties>""")
    #         for row in data:
    #             d = row.get('Duration [hh:mm:ss]')
    #             try:
    #                 h, m, s = d.split(':')
    #                 secs = int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(float(s))).total_seconds()) 
    #             except Exception as e:
    #                 log.error(f'Could not parse time from CSV for test [{row["QcId"]} - {row["TestName"]}]. Error: {e}')
    #                 secs = -1  

    #             xmlFile.write(f'\t<testcase classname="{testSuite}.{row["TestName"]}" name="{row["QcId"]} - {row["TestName"]}" time="{secs}" >\n')
    #             if row["Result"] == "FAILED":
    #                 xmlFile.write('\t<failure message="test failure">')
    #                 xmlFile.write(f'failure - {removeXmlSpecialChars(row["Failure"])}, failure step - {row["Failed Step"]}\n')
    #                 xmlFile.write('\t</failure>\n')
    #             elif row["Result"] in ['pending', 'skipped']:
    #                 xmlFile.write('\t<skipped/>\n')
    #             xmlFile.write('\t</testcase>\n')

    #         xmlFile.write('</testsuite>\n')    
    #         log.info(f'Results written to file "{fileName}"')
        
    #     return fileName

    # def removeXmlSpecialChars(string):
    #     specialChars = ["&", "<", ">", "\"", "'"]
    #     escapeChars = {"<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&apos;", "&": "&amp;"}
    #     for char in specialChars:
    #         string = string.replace(char, escapeChars.get(char))
    #     return string
