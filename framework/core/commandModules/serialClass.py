#!/usr/bin/env python3
#/* *****************************************************************************
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
#*   ** @addtogroup  : core.commandModules
#*   ** @date        : 20/11/2021
#*   **
#*   ** @brief : wrapper for serial
#*   **
#/* *****************************************************************************


import serial as serial

from framework.core.commandModules.consoleInterface import consoleInterface

class serialSession(consoleInterface):
    """Handle device serial connection operation

    Args:
        log (logModule): Log module to be used.
        workspacePath (str): Path of the tests workspace to create the session.log file.
        serialPort (str): Serial port to use.
        baudRate (int, option): Baud rate to use. Default's to 115200.

    """
  
    def __init__(self, log, workspacePath, serialPort, baudRate=115200, prompt=None) -> None:
        super().__init__(prompt)
        self.log = log
        self.workspacePath = workspacePath
        self.serialPort = serialPort
        self.serialFile = workspacePath + "session.log"
        self.timeout = 5
        self.baudRate = baudRate
        self.type="serial"
        self.is_open = False

        # TODO: Pass in the rest of the serial configuration

        # Initiate serial session , parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, xonxoff=False,
        try:
            self.serialCon = serial.Serial(self.serialPort, self.baudRate, timeout=300)
        except Exception as e:
            self.log.error('Failed to start serial connection - {}'.format(e))
            raise Exception('Failed to start Serial Connection. Check the COM port settings')

    def open(self) -> bool:
        """Start serial session and serial file logger.

        Returns:
            bool: True if serial session opened successfully.
        """        
        try:
            if not self.serialCon.is_open:
                self.serialCon.open()
        except (serial.SerialException, serial.SerialTimeoutException) as e:
            self.log.error('Failed to open serial connection - %s' % e)
        try:
            self.serialFileHandler = open(self.serialFile, "w+")
        except (OSError, IOError) as e:
            self.log.error('Failed to initiate Serial log file - %s' % e)
        isOpen = self.serialCon.is_open
        self.is_open = True
        return isOpen

    def close(self) -> bool:
        """Close the serial session and serial file logger.

        Returns:
            bool: True if serial session closed successfully.
        """
        if self.serialFileHandler:
            self.log.debug("Successfully closed Serial log file")
            try:
                self.serialFileHandler.close()        
            except (OSError, IOError) as e:
                self.log.error('Failed to close serial log file')
                self.log.error(e)
            self.log.debug("Successfully closed Serial session and log file")
        try:
            self.serialCon.close()
        except  serial.SerialException as e:
            self.log.error('Failed to close serial connection or file')
            self.log.error(e)
        self.is_open = False
        return True

    def read_until(self, value) -> str:
        """Read serial output until a specified value is found.

        Args:
            value (str): The message to wait for in the console.

        Returns:
            str: Information displayed in the console up to the value entered.
        """
        message = bytes(value,encoding='utf-8')
        serialStr = self.serialCon.read_until( message )
        writeString = serialStr.decode("utf-8", errors='ignore')
        try:
            self.serialFileHandler.writelines(writeString)
        except Exception as e:
            self.log.error('Failed to decode to Serial log  - %s' % e)
        return writeString

    def read_all(self) -> str:
        """Read all lines from serial output available in the buffer.

        Returns:
           str: Information currently displayed in the console.
        """
        serialStr = self.serialCon.read_all()
        if serialStr == b'':
            return ""
        writeString = serialStr.decode("utf-8", errors='ignore')
        try:
            self.serialFileHandler.writelines(writeString)
        except Exception as e:
            self.log.error('Failed to writelines from Serial log  - %s' % e)
        return writeString
    
    def write(self, message:list|str, lineFeed:str="\n", wait_for_prompt:bool=False) -> bool:
        """Write to serial console.
        Optional: waits for prompt.

        Args:
            message (Str) - message to write to serial console.
            lineFeed (str): Linefeed extension.
            wait_for_prompt (bool): If True, waits for the prompt before writing.

        Returns:
            bool: True if can successfully write to serial console.
        """
        if not self.is_open:
            self.open()
        self.log.debug("Writing to Serial [{}]".format(message.strip()))
        if wait_for_prompt:
            if not self.waitForPrompt():
                return False
        if isinstance( message, str ):
            message = [message]
        for msg in message:
            msg += lineFeed
            outputMessage = msg.encode('utf-8')
            try:
                self.serialCon.write(outputMessage)
            except Exception as e:
                self.log.error('Failed to write to serial - %s' % e)
                return False
        return True
    
    def writeLines(self, message):
        """Write to serial console.

        Args:
            message (Str) - message to write to serial console.

        Returns:
            bool: True if can successfully write to serial console.
        """
        try:
            self.serialCon.writelines(message.encode('utf-8'))
        except Exception as e:
            self.log.error('Failed to write to Serial log file - %s' % e)
        return True

    def flush(self) -> bool:
        """Clear the console.

        Returns:
            True if can successfully clear the serial console.
        """
        self.log.info("Clearing Serial console log")
        self.serialCon.flushInput()
        return True
