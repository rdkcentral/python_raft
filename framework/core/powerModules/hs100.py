#! /bin/python3
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
#*   ** @file        : hs100.py
#*   ** @date        : 15/08/2020
#*   **
#*   ** @brief : This module supports the hs100 power switch
#*   **
#* ******************************************************************************

import socket
import time
import struct
from struct import pack

import framework.core.logModule

class powerHS100():
    
    def __init__( self, log, ip, port ):
        """
        Initialize the SmartPlug object.

        Args:
            log: Logger object for logging messages.
            ip (str): IP address of the TP-Link Smart Plug.
            port (int): Port number for the connection.
        """
        self.ip = ip
        if port is None:
            port = 9999
        self.port = int(port)
        self.log = log

        # Predefined Smart Plug Commands
        self.commands = {'info'     : '{"system":{"get_sysinfo":{}}}',
                         'on'       : '{"system":{"set_relay_state":{"state":1}}}',
                         'off'      : '{"system":{"set_relay_state":{"state":0}}}',
                         'ledoff'   : '{"system":{"set_led_off":{"off":1}}}',
                         'ledon'    : '{"system":{"set_led_off":{"off":0}}}',
                         'cloudinfo': '{"cnCloud":{"get_info":{}}}',
                         'wlanscan' : '{"netif":{"get_scaninfo":{"refresh":0}}}',
                         'time'     : '{"time":{"get_time":{}}}',
                         'schedule' : '{"schedule":{"get_rules":{}}}',
                         'countdown': '{"count_down":{"get_rules":{}}}',
                         'antitheft': '{"anti_theft":{"get_rules":{}}}',
                         'reboot'   : '{"system":{"reboot":{"delay":1}}}',
                         'reset'    : '{"system":{"reset":{"delay":1}}}',
                         'energy'   : '{"emeter":{"get_realtime":{}}}'
                         }

    def encrypt(self, string):
        """
        Encrypt a string using XOR Autokey Cipher with starting key = 171.

        Args:
            string (str): The string to encrypt.

        Returns:
            bytes: The encrypted bytes.
        """
        key = 171
        result = pack('>I', len(string))
        for i in string:
            a = key ^ ord(i)
            key = a
            result += bytes([a])
        return result

    def decrypt(self, string):
        """
        Decrypt a string using XOR Autokey Cipher with starting key = 171.

        Args:
            string (bytes): The encrypted bytes to decrypt.

        Returns:
            str: The decrypted string.
        """
        key = 171
        result = ""
        for i in string:
            a = key ^ i
            key = i
            result += chr(a)
        return result

    def switchCommand(self, key):
        """
        Send a command to the switch.

        Args:
            key (str): The command key. Refer to self.commands for available keys.

        Returns:
            bool: True if the command is successful, False otherwise.
        """
        result = False
        counter = 0
        while counter < 5:
            try:
                counter += 1
                sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_tcp.settimeout(5)
                sock_tcp.connect((self.ip, self.port))
                sock_tcp.settimeout(None)
                sock_tcp.send(self.encrypt(self.commands[key]))
                data = sock_tcp.recv(2048)
                sock_tcp.close()
                decrypted = self.decrypt(data[4:])
                self.log.debug("Sent:     {}".format(key))
                self.log.debug("Received: {}".format(decrypted))
                if key == 'on':
                    self.powerOnState = True
                result = True
                break
            except socket.error as message:
                #quit("Could not connect to host " + self.powerSwitchIp + ":" + str(self.powerSwitchPort))
                self.log.error("PowerControl Socket Error: %s" % message)
                time.sleep(1)
        return result

    def powerOff(self):
        """
        Turn off the Smart Plug.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        result = self.switchCommand('off')
        return result

    def powerOn(self):
        """
        Turn on the Smart Plug.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        result = self.switchCommand('on')
        return result

    def switchReboot(self):
        """
        Reboot the Smart Plug.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        result = self.switchCommand('reboot')
        return result

    def reboot(self):
        """
        Reboot the Smart Plug.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        result = self.powerOff()
        if result != True:
            self.log.error(" Power Failed off")
        time.sleep(1)
        result = self.powerOn()
        if result != True:
            self.log.error(" Power Failed on")
        return result