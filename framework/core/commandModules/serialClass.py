#! /bin/python3
#/* *****************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
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
    """
  
    def __init__(self, log, workspacePath, serialPort, baudRate=115200):
        self.log = log
        self.workspacePath = workspacePath
        self.serialPort = serialPort
        self.serialFile = workspacePath + "session.log"
        self.timeout = 5
        self.baudRate = baudRate
        self.type="serial"

        # TODO: Pass in the rest of the serial configuration

        # Initiate serial session , parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, xonxoff=False,
        try:
            self.serialCon = serial.Serial(self.serialPort, self.baudRate, timeout=300)
        except Exception as e:
            self.log.error('Failed to start serial connection - {}'.format(e))
            raise Exception('Failed to start Serial Connection. Check the COM port settings')

    def open(self):
        """Starts serial session and serial file logger
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
        return isOpen

    def close(self):
        """Closes the serial session and serial file logger
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
        return True

    def write(self, message):
        """Write to serial console

        Args:
            message (Str) - message to write to serial console
        """
        self.log.debug("Writing to Serial [{}]".format(message.strip()))
        try:
            self.serialCon.write(message.encode('utf-8'))
        except Exception as e:
            self.log.error('Failed to write to serial - %s' % e)
            return False
        return True
    
    def writeLines(self, message):
        """Write to serial console

        Args:
            message (Str) - message to write to serial console
        """
        try:
            self.serialCon.writelines(message.encode('utf-8'))
        except Exception as e:
            self.log.error('Failed to write to Serial log file - %s' % e)
        return True

    def read_until(self, value):
        """Read serial output until a specified value is found
        """
        message = bytes(value,encoding='utf-8')
        serialStr = self.serialCon.read_until( message )
        writeString = serialStr.decode("utf-8", errors='ignore')
        try:
            self.serialFileHandler.writelines(writeString)
        except Exception as e:
            self.log.error('Failed to decode to Serial log  - %s' % e)
        return writeString

    def read_all(self):
        """Read all lines from serial output available in the buffer
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

    def flush(self):
        self.log.info("Clearing Serial console log")
        self.serialCon.flushInput()
        return True
