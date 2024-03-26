#! /bin/python3

#** *****************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
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
        result = self.command('OFF {}\n'.format(self.outlet))
        if result != True:
            self.log.error(" Power Failed off")
        return result

    def powerOn(self):
        result = self.command('ON {}\n'.format(self.outlet))
        if result != True:
            self.log.error(" Power Failed on")
        return result

    def reboot(self):
        result = self.powerOff()
        if result is True:
            result = self.powerOn()
        return result
