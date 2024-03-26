#! /bin/python3
#/* *****************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
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

from framework.core.commandModules.consoleInterface import consoleInterface

class telnet(consoleInterface):

    def __init__(self,log, workspacePath, host, username, password, port=23):
        self.tn = None
        self.username = username
        self.password = password
        self.type="telnet"

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

    def open(self):
        self.connect()

    def close(self):
        self.disconnect()

    def connect(self, username_prompt = "login: ", password_prompt = "Password: "):
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

    def disconnect(self):
        self.tn.close()
        return True

    def write(self,message):
        message = message.encode()
        try:
            self.tn.write(message + b"\r\n")
        except socket.error:
            self.log.error("telnet.write() socket.error")
            return False
        return True

    def read_until(self,value):
        message = value.encode()
        result = self.tn.read_until(message,self.timeout)
        return result.decode()

    def read_eager(self):
        result=self.tn.read_eager()
        return result.decode()

    def read_very_eager(self):
        result=self.tn.read_very_eager()
        return result.decode()

    def read_some(self):
        result=self.tn.read_some()
        return result.decode()

    def message(self, message):
        result=self.tn.message(message)
        return result.decode()

    def read_all(self):
        result=self.tn.read_eager()
        return result.decode()
