
#! /bin/python3
#/* ******************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core.commandModules
#*   ** @date        : 20/11/2021
#*   **
#*   ** @brief : wrapper for sshConsole None
#*   **
#/* ******************************************************************************

from paramiko import SSHClient


from framework.core.commandModules.consoleInterface import consoleInterface


class sshConsole(consoleInterface):

    def __init__(self, address, username, password, key=None, known_hosts=None) -> None:
        self.address = address
        self.username = username
        self.password = password
        self.key = key
        self.console = SSHClient()
        self.console.load_system_host_keys(known_hosts)
        self.buffer = []
        self.stdout = None
        self.type="ssh"

    def open(self):
        self.console.connect(self.address, username = self.username, password = self.password, key_filename=self.key)

    def write(self, message):
        if self.stdout:
            self.buffer.extend(self.stdout.readlines())
        self.stdin, self.stdout, self.stderr = self.console.exec_command(message, get_pty=True)

    def read_all(self):
        data = ""
        self.buffer.extend(self.stdout.readlines())
        self.stdout = None
        while self.buffer.__len__() > 0:
            data = data + self.buffer.pop(0)
        return data

    def read_until(self, value):
        data = ""
        self.buffer.extend(self.stdout.readlines())
        self.stdout = None
        while self.buffer.__len__() > 0:
            data = data + self.buffer.pop(0)
            if value in data:
                break
        return data

    def close(self):
        self.console.close()
