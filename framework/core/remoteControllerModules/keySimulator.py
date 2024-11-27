import os
import time
import subprocess
from framework.core.logModule import logModule
from framework.core.commandModules.sshConsole import sshConsole


class KeySimulator:

    def __init__(self, log: logModule, remoteConfig: dict):
        """Initialize the KeySimulator class.

        Args:
            log (logModule): Logging module instance.
            remoteConfig (dict): Key simulator configuration.
        """
        self.log = log
        self.remoteConfig = remoteConfig
        self.prompt = r"\$ "

        # Initialize SSH session
        self.session = sshConsole(
            address=self.remoteConfig.get("ip"),
            username=self.remoteConfig.get("username"),
            password=self.remoteConfig.get("password"),
            known_hosts=self.remoteConfig.get("known_hosts"),
            port=int(self.remoteConfig.get("port")),
        )

        self.firstKeyPressInTc = True

    def sendKey(self, key: str, repeat: int = 1, delay: int = 0) -> bool:
        """Send a key command with specified repeats and interval.

        Args:
            key (str): The key to send.
            repeat (int): Number of times to send the key.
            delay (int): Delay between key presses in seconds.

        Returns:
            bool: Result of the command verification.
        """
        result = False
        keyword = "term start init 1"

        # Send the key command
        for _ in range(repeat):
            self.session.write(f"{key}")
            time.sleep(delay)

        # Read output after sending keys
        output = self.session.read_until(self.prompt)

        # Check for the presence of a keyword in the output
        if keyword in output:
            result = True

        return result
