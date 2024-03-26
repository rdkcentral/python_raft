#! /bin/python3

#** *****************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
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
        """Encryption of TP-Link Smart Home Protocol. XOR Autokey Cipher with starting key = 171"""
        key = 171
        result = pack('>I', len(string))
        for i in string:
            a = key ^ ord(i)
            key = a
            result += bytes([a])
        return result

    def decrypt(self, string):
        """Decryption of TP-Link Smart Home Protocol. XOR Autokey Cipher with starting key = 171"""
        key = 171
        result = ""
        for i in string:
            a = key ^ i
            key = i
            result += chr(a)
        return result

    def switchCommand(self, key):
        """send key command to switch

        Args:
            key (str) - 'on'\'off'\'reboot'. Refer self.commands
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
        result = self.switchCommand('off')
        return result

    def powerOn(self):
        result = self.switchCommand('on')
        return result

    def switchReboot(self):
        result = self.switchCommand('reboot')
        return result

    def reboot(self):
        result = self.powerOff()
        if result != True:
            self.log.error(" Power Failed off")
        time.sleep(1)
        result = self.powerOn()
        if result != True:
            self.log.error(" Power Failed on")
        return result