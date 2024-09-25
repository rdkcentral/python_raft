#!/usr/bin/env python3
#/* ******************************************************************************
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
#*   ** @brief : wrapper for sshConsole None
#*   **
#/* ******************************************************************************

import paramiko
import time

from .consoleInterface import consoleInterface
from paramiko import SSHClient

class sshConsole(consoleInterface):
    """sshConsole is a consoleInterface class to interface with SSH console sessions

    Args:
        address (str): IP address of the host to connect to.
        username (str): Username for logging into the host.
        password (str): Password for logging into the host.
        key (str, optional): Filepath of ssh key to use.
        known_hosts (str, optional): Filepath of known_hosts file to use.
    """

    def __init__(self, address, username, password, key=None, known_hosts=None, port=22) -> None:
        self.address = address
        self.username = username
        self.password = password
        self.key = key
        self.port = port
        self.console = SSHClient()
        #self.console.load_system_host_keys(known_hosts)
        self.console.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        self.buffer = []
        self.stdout = None
        self.type="ssh"
        self.shell = None
        self.full_output = ""
        self.is_open = False

    def open(self):
        """Open the SSH session.
        """
        self.console.connect(self.address, username = self.username, password = self.password, key_filename=self.key, port=self.port)
        self.is_open = True

    def open_interactive_shell(self):
        """Open an interactive shell session."""
        # Open an interactive shell
        self.shell = self.console.invoke_shell()

        # Ensure the shell is ready
        while not self.shell.send_ready():
            time.sleep(1)

    def write(self, message:list|str, lineFeed="\n"):
        """Write a message into the console.

        Args:
            message (str): String to write into the console.
            lineFeed (str): Linefeed extension
        """
        
        if self.shell is None:
            self.open()
            self.open_interactive_shell()

        if isinstance( message, str ):
            message = [message]
        for msg in message:
            msg += lineFeed
            self.shell.send(msg)

       # output = self.read()
       # self.full_output += output

        return True
    
    def read(self, timeout=10):
        """Read the output from the shell with a timeout.

        Args:
            timeout (int): The maximum time to wait for in the message in seconds. Defaults to 10. 
        """
        output = ""
        
        # Set a timeout period
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            if self.shell.recv_ready():
                output += self.shell.recv(4096).decode('utf-8')
                # Reset the timeout when new data arrives
                end_time = time.time() + timeout
            else:
                # Small delay to prevent busy waiting
                time.sleep(0.1)

        return output
    
    def read_all(self):
        """Retrieve the accumulated output in the console.

        Returns:
            Str: A single string containing all the accumulated output in the console.
        """
        return self.full_output

    def read_until(self, value, timeout=10):
        """Read the console output until a specific message appears.

        Args:
            value (str): The message to wait for in the console.
            timeout (int): The maximum time to wait for in the message in seconds. Defaults to 10. 

        Returns:
            Str: The console output up to the specified value.

        """
        output = ""
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            if self.shell.recv_ready():
                output += self.shell.recv(4096).decode('utf-8')
                # Reset the timeout if new data is received
                end_time = time.time() + timeout

                # Check if the target value is in the current output
                if value in output:
                    break
            else:
                # Small delay to prevent busy waiting
                time.sleep(0.1)

        return output

    def close(self):
        """Close the SSH session
        """
        self.console.close()
        self.is_open = False
