
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


from .consoleInterface import consoleInterface


class sshConsole(consoleInterface):
    """sshConsole is a consoleInterface class to interface with SSH console sessions

    Args:
        address (str): IP address of the host to connect to.
        username (str): Username for logging into the host.
        password (str): Password for logging into the host.
        key (str, optional): Filepath of ssh key to use.
        known_hosts (str, optional): Filepath of known_hosts file to use.
    """

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
        """Open the SSH session.
        """
        self.console.connect(self.address, username = self.username, password = self.password, key_filename=self.key)

    def write(self, message):
        """Write a message into the console.

        Args:
            message (str): String to write into the console.
        """
        if self.stdout:
            self.buffer.extend(self.stdout.readlines())
        self.stdin, self.stdout, self.stderr = self.console.exec_command(message, get_pty=True)

    def read_all(self):
        """Capture all lines that are displayed in the console.

        Returns:
            List: List of strings, with each being a line displayed in the console.
        """
        data = ""
        self.buffer.extend(self.stdout.readlines())
        self.stdout = None
        while self.buffer.__len__() > 0:
            data = data + self.buffer.pop(0)
        return data

    def read_until(self, value):
        """Read the console until a message appears.

        Args:
            value (str): The message to wait for in the console.

        Returns:
            List: List of string, with each being a line displayed in the console up to the value entered.
        """
        data = ""
        self.buffer.extend(self.stdout.readlines())
        self.stdout = None
        while self.buffer.__len__() > 0:
            data = data + self.buffer.pop(0)
            if value in data:
                break
        return data

    def close(self):
        """Close the SSH session
        """
        self.console.close()
