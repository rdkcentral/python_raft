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
#*   ** @addtogroup  : core.powerModules
#*   ** @date        : 16/12/2021
#*   **
#*   ** @brief : power module to support Lantronix SecureLinx SLP Remote Power Manager hardware
#*   **
#* ******************************************************************************

from framework.core.commandModules.telnetClass import telnet


class powerSLP():

    def __init__(self, log, ip, username, password, outlet_id, port=None):
        """
        Initializes the PDU control object.

        Args:
            log: The logger object for logging messages.
            ip (str): The IP address of the Power Distribution Unit (PDU).
            username (str): The username for authentication.
            password (str): The password for authentication.
            outlet_id (int): The ID of the outlet to control.
            port (int, optional): The port for Telnet connection. Defaults to 23.
        """
        self.log = log
        self.ip = ip
        self.username = username
        self.password = password
        self.outlet = outlet_id
        self.port = 23
        if port:
            self.port = port
        self.telnet = telnet(self.log, '{}:{}'.format(self.ip, self.port),
                             self.username, self.password)

    def command(self, cmd):
        """
        Send a command to the Power Distribution Unit (PDU) via Telnet.

        Args:
            cmd (str): The command to be executed.

        Returns:
            bool: True if the command was successful, False otherwise.
        """
        result = True
        if self.telnet.connect(username_prompt='Username: ',
                               password_prompt='Password: ') is False:
            raise RuntimeError('Cannot connect to PDU via telnet')
        self.telnet.read_very_eager()
        if self.telnet.write(cmd):
            if b"Command successful" not in self.telnet.read_until(
                    "Command successful"):
                result = False
        else:
            result = False
        self.telnet.disconnect()
        return result

    def powerOff(self):
        """
        Turn off the outlet.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        result = self.command('OFF {}\n'.format(self.outlet))
        if result != True:
            self.log.error(" Power Failed off")
        return result

    def powerOn(self):
        """
        Turn on the outlet.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        result = self.command('ON {}\n'.format(self.outlet))
        if result != True:
            self.log.error(" Power Failed on")
        return result

    def reboot(self):
        """
        Reboot the outlet by powering it off and then on.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        result = self.powerOff()
        if result is True:
            result = self.powerOn()
        return result
