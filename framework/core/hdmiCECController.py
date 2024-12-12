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
#*   ** @addtogroup  : core
#*   ** @date        : 22/11/2021
#*   **
#*   ** @brief : HDMICECController class to differentiate into the whichever
#*   **          cec controller type is specified.
#*   **
#* ******************************************************************************

from os import path

import sys
MY_PATH = path.realpath(__file__)
MY_DIR = path.dirname(MY_PATH)
sys.path.append(path.join(MY_DIR,'../../'))
from framework.core.logModule import logModule
from framework.core.hdmicecModules import CECClientController, MonitoringType

class HDMICECController():
    """
    This class provides a high-level interface for controlling and monitoring 
    Consumer Electronics Control (CEC) devices.
    """

    def __init__(self, log: logModule, config: dict):
        """
        Initializes the HDMICECController instance.

        Args:
            log (logModule): An instance of a logging module for recording messages.
            config (dict): A dictionary containing configuration options
        """
        self._log = log
        self.controllerType = config.get('type')
        self.cecAdaptor = config.get('adaptor')
        if self.controllerType.lower() == 'cec-client':
            self.controller = CECClientController(self.cecAdaptor, self._log)
        self._read_line = 0
        self._monitoringLog = path.join(self._log.logPath, 'cecMonitor.log')

    def send_message(self, message: str) -> bool:
        """
        Sends a CEC message to connected devices using the configured controller.

        Args:
            message (str): The CEC message to be sent.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        self._log.debug('Sending CEC message: [%s]' % message)
        return self.controller.sendMessage(message)
        
    def startMonitoring(self, deviceType: MonitoringType = MonitoringType.RECORDER) -> None:
        """
        Starts monitoring CEC messages from the adaptor as the specified device type.

        Args:
            deviceType (MonitoringType, optional): The type of device to monitor (default: MonitoringType.RECORDER).

        Raises:
            RuntimeError: If monitoring is already running.
        """
        if self.controller.monitoring is False:
            self._log.debug('Starting monitoring on adaptor: [%s]' % self.cecAdaptor)
            self._log.debug('Monitoring as device type [%s]' % deviceType.name)
            return self.controller.startMonitoring(self._monitoringLog, deviceType)
        else:
            self._log.warn('CEC monitoring is already running')

    def stopMonitoring(self):
        """
        Stops the CEC monitoring process.

        Delegates the stop task to the underlying `CECClientController`.
        """
        return self.controller.stopMonitoring()

    def readUntil(self, message: str, retries: int = 5) -> bool:
        """
        Reads the monitoring log until the specified message is found.

        Opens the monitoring log file and checks for the message within a specified retry limit.

        Args:
            message (str): The message to search for in the monitoring log.
            retries (int, optional): The maximum number of retries before giving up (default: 5).

        Returns:
            bool: True if the message was found, False otherwise.
        """
        self._log.debug('Starting readUntil for message as [%s] with [%s] retries' % (message,retries))
        result = False
        retry = 0
        max_retries = retries
        while retry != max_retries and not result:
            with open(self._monitoringLog, 'r') as logFile:
                logLines = logFile.readlines()
                read_line = self._read_line
                write_line = len(logLines)
                while read_line != write_line:
                    if message in logLines[read_line]:
                        result = True
                        break
                    read_line+=1
            retry += 1
        self._read_line = read_line
        return result

    def listDevices(self) -> list:
        """
        Retrieves a list of discovered CEC devices with their OSD names (if available).

        Returns:
            list: A list of dictionaries representing discovered devices.
        """
        self._log.debug('Listing devices on CEC network')
        return self.controller.listDevices()


if __name__ == "__main__":
    import time
    import json
    LOG = logModule('CECTEST', logModule.DEBUG)
    CONFIGS = [
        {
            'type': 'cec-client',
            'adaptor': '/dev/ttyACM0'
            },
    ]
    for config in CONFIGS:
        LOG.setFilename('./logs/','CECTEST%s.log' % config.get('type'))
        LOG.stepStart('Testing with %s' % json.dumps(config))
        CEC = HDMICECController(LOG, config)
        DEVICES = CEC.listDevices()
        LOG.info(json.dumps(DEVICES))
        # The user will need to check all the devices expected from their 
        # cec network are shown in this output.
        CEC.startMonitoring()
        # It's is expected that a user will send a standby command on their cec
        # network during this 2 minutes.
        time.sleep(120)
        result = CEC.readUntil('standby')
        CEC.stopMonitoring()
        LOG.stepResult(result, 'The readUntil result is: [%s]' % result)
        # The user should check here the monitoring log for thier type contains
        # the expected information.
