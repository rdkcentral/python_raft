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
#*   ** @brief : wrapper for telnet
#*   **
#*
#* ******************************************************************************

import telnetlib
import socket

from .consoleInterface import consoleInterface

class telnet(consoleInterface):

    """telnet is a consoleInterface class to interface with telnet console sessions.

    Args:
        log (logModule): Log module to be used.
        workspacePath (str): Path of the tests workspace to create the session.log file.
        host (str): IP address of the host to open a session with.
        username (str): Username to login to the session with.
        password (str): Password to login to the session with.
        port (int, optional): Listening telnet port on host. Defaults to 23.
    """

    def __init__(self,log, workspacePath, host, username, password, port=23, prompt=None) -> None:
        super().__init__(prompt)
        self.tn = None
        self.username = username
        self.password = password
        self.type="telnet"
        self.is_open = False

        try:
            xhost=host.split(':')
            if len(xhost)==2:
                self.host=xhost[0]
                self.port=xhost[1]
            else:
                raise Exception()
        except:
            self.host = host
            self.port = port
        self.timeout = 5
        self.log = log
        self.sessionLogFile = workspacePath + "session.log"
        try:
            self.sessionLogHand = open(self.sessionLogFile, "w+")
        except (OSError, IOError) as e:
            self.log.error('Failed to initiate session log file - %s' % e)

    def open(self) -> bool:
        """Open the telnet session.
        """
        self.connect()
        self.is_open = True

    def close(self) -> bool:
        """Close the telnet session.
        """
        self.disconnect()
        self.is_open = False

    def connect(self, username_prompt = "login: ", password_prompt = "Password: ") -> bool:
        """Open the telnet session

        Args:
            username_prompt (str, optional): Expected prompt shown for entering the username.
            password_prompt (str, optional): Expected prompt shown for entering the password.

        Returns:
            bool: True if session opened successfully.
        """
        try :
            self.log.info("Host IP : [{}]".format(self.host))
            self.tn = telnetlib.Telnet(self.host, self.port, self.timeout)
        except socket.timeout:
            self.log.error("telnet.connect() socket.timeout")
            return False
        except socket.gaierror:
            self.log.error("telnet.connect() socket.gaierror")
            return False
        if self.username is None:
            return True
        self.log.info( "Username : [{}]".format( self.username))
        readData = self.read_until(username_prompt)
        if len(readData) == 0:
            return False
        self.write(self.username)
        if self.password is None:
            return True
        self.log.info( "Password : [{}]".format( self.password))
        readData = self.read_until(password_prompt)
        if len(readData) == 0:
            return False
        self.write(self.password)
        return True

    def disconnect(self) -> bool:
        """Close the telnet session

        Returns:
            bool: True if session closed successfully.
        """
        self.tn.close()
        return True

    def read_until(self,value) -> str:
        """Read the console until a message appears.

        Args:
            value (str): The message to wait for in the console.

        Returns:
            str: Information displayed in the console up to the value entered.
        """
        message = value.encode()
        result = self.tn.read_until(message,self.timeout)
        return result.decode()
    
    def read_all(self) -> str:
        """Read all readily available information displayed in the console.

        Returns:
            str: Information currently displayed in the console.
        """
        return self.read_eager()
    
    def write(self,message:list|str, lineFeed:str="\r\n", wait_for_prompt:bool=False) -> bool:
        """Write a message into the session console.
        Optional: waits for prompt.

        Args:
            message (list|str): String or list of strings to write to the console.
            lineFeed (str): Linefeed extension.
            wait_for_prompt (bool): If True, waits for the prompt before writing.

        Returns:
            bool: True when the message is successfully written to the console.
        """
        if not self.is_open:
            self.open()
        if wait_for_prompt:
            if not self.waitForPrompt():
                return False
        if isinstance( message, str ):
            message = [message]
        for msg in message:
            msg += lineFeed
            msg = msg.encode()
            try:
                self.tn.write(message)
            except socket.error:
                self.log.error("telnet.write() socket.error")
                return False
        return True

    def read_eager(self) -> str:
        """Read all readily available information displayed in the console.

        Returns:
            str: Information currently displayed in the console.
        """
        result=self.tn.read_eager()
        return result.decode()

    def read_very_eager(self) -> str:
        """Read all readily available information displayed in the console, without blocking I/O.

        Returns:
            str: Information currently displayed in the console.
        """
        result=self.tn.read_very_eager()
        return result.decode()

    def read_some(self) -> str:
        """Read information displayed in the console until EOF hit.

        Returns:
            str: Information currently displayed in the console.
        """
        result=self.tn.read_some()
        return result.decode()
