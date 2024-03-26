#! /bin/python3

#** *****************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core.powerModules
#*   ** @date        : 18/11/2021
#*   **
#*   ** @brief : power module to support olimex hardware
#*   **
#* ******************************************************************************

from framework.core.commandModules.telnetClass import telnet

class powerOlimex():
    
    def __init__( self, log, ip, port, relay ):
        self.log = log
        self.ip = ip
        self.port = port
        if port is None:
            self.port = int(9999)   #TODO: Set the default port here
        self.relay = relay
        self.telnet = None

    def command(self, cmd):
        self.telnet=telnet(self.log, '{}:{}'.format(self.ip,self.port), None, None)
        if False==self.telnet.connect():
            return False
        self.telnet.read_very_eager()
        if False==self.telnet.write(cmd):
            return False
        if not b"(OK)" in self.telnet.read_until("(OK)"):
            return False
        self.telnet.disconnect()
        return True

    def powerOff(self):
        result = self.command('REL{}=0\n'.format(self.relay))
        if result != True:
            self.log.error(" Power Failed off")
        return result

    def powerOn(self):
        result = self.command('REL{}=1\n'.format(self.relay))
        if result != True:
            self.log.error(" Power Failed on")
        return result

    def reboot(self):
        result = self.powerOff()
        if result != True:
            result = self.powerOn()
        return result
