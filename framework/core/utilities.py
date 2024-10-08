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
#*   ** @file        : powerControl.py
#*   ** @date        : 26/05/2021
#*   **
#*   ** @brief : Common utils to support core framework
#*   **
#* ******************************************************************************

import re
import subprocess
import time

class utilities():
    def __init__(self, log):
        """
        Initializes the utilities class.

        Args:
            log (logger object): Logger object for logging messages.
        """
        self.log = log

    def wait(self, seconds, minutes=0, hours=0):        
        """
        Pause the program execution for a specified duration.

        Args:
            seconds (int): Number of seconds to wait.
            minutes (int, optional): Number of minutes to wait. Defaults to 0.
            hours (int, optional): Number of hours to wait. Defaults to 0.

        Returns:
            None
        """
        self.log.info("Wait for [{}] seconds [{}] mins [{}] Hours".format(seconds, minutes, hours))
        waitTime = seconds
        if hours:
            waitTime += hours*60*60
        
        if minutes:
            waitTime += minutes*60

        time.sleep(waitTime)
        self.log.info('Wait over')
        return

    def fuzzyCompareText(self, expText, actualText, exactMatch=False):        
        """
        Compare two strings with possible variations.

        Args:
            expText (str): The expected text.
            actualText (str): The actual text to compare.
            exactMatch (bool, optional): If True, perform an exact match. Defaults to False.

        Returns:
            bool: True if the texts match, False otherwise.
        """
        self.log.info('fuzzyCompareText: expText - [{}] actualText - [{}]'.format(expText, actualText))
        
        result = False
        expText = expText.lower().replace(' ', '')
        actualText = actualText.lower().replace(' ', '')

        if exactMatch:
            result = expText == actualText
        else:
            result = True if re.search(expText.replace('*', '.*'), actualText) else False
        
        self.log.info('fuzzyCompareText returns - [{}]'.format(result))
        return result

    def value1HigherThanValue2(self, value1, value2):
        """Compares two version numbers and returns True if value1 is higher than value2.

        Args:
            value1 (str): First version number to compare.
            value2 (str): Second version number to compare.

        Returns:
            bool: True if value1 is higher than value2, False otherwise.
        """
        self.log.info('utils.value1HigherThanValue2 - value1 ({}), value2 ({})'.format(value1, value2))
        value1 = value1.split('.')
        value2 = value2.split('.')

        intValuesOfValue1 = [int(value) for value in value1]
        intValuesOfValue2 = [int(value) for value in value2]

        if intValuesOfValue1[0] > intValuesOfValue2[0]:
            return True
        
        if intValuesOfValue1[0] == intValuesOfValue2[0]:
            if intValuesOfValue1 [1] > intValuesOfValue2[1]:
                return True
            
            if intValuesOfValue1 [1] == intValuesOfValue2[1]:
                if intValuesOfValue1[2] > intValuesOfValue2[2]:
                    return True
        return False
    
    def syscmd(self, cmd, encoding=''):
        """Run a command on the system.

        Args:
            cmd (str): Command to run.
            encoding (str, optional): Encoding required. Defaults to ''.
            returnCode (bool, optional): Check for return codes. Defaults to False.

        Returns:
            str or int: Command result or return code.
        """
        self.log.debug( "command: ["+str(cmd)+"]")
        p = subprocess.run(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,close_fds=True)
        output = p.stdout
        resultCodeReturn = p.returncode
        if len(output) > 1:
            self.log.debug( "command: output:["+str(output.decode('utf-8'))+"], returnCode:["+str(resultCodeReturn)+"]")
            if encoding: 
                output = output.decode(encoding)
        return output, resultCodeReturn
    
    def strip_ansi_escapes(line):
        """Removes ansi escape sequences from strings.

        Args:
            line (str): String to remove ansi escape sequences from.

        Returns:
            str: The input string with all ansi escape sequences removed.
        """
        ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', line)
