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
from datetime import datetime
from os import path

import sys
MY_PATH = path.realpath(__file__)
MY_DIR = path.dirname(MY_PATH)
sys.path.append(path.join(MY_DIR,'../../'))
from framework.core.logModule import logModule
from framework.core.streamToFile import StreamToFile
from framework.core.hdmicecModules import CECClientController, RemoteCECClient, CECDeviceType

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
        self._streamFile = path.join(self._log.logPath, f'{self.controllerType.lower()}_{str(datetime.now().timestamp())}')
        self._stream = StreamToFile(self._streamFile)
        if self.controllerType.lower() == 'cec-client':
            self.controller = CECClientController(self.cecAdaptor,
                                                  self._log,
                                                  self._stream)
        elif self.controllerType.lower() == 'remote-cec-client':
            self.controller = RemoteCECClient(self.cecAdaptor,
                                              self._log,
                                              self._stream,
                                              config.get('address'),
                                              username=config.get('username',''),
                                              password=config.get('password',''),
                                              port=config.get('port',22),
                                              prompt=config.get('prompt', ':~'))
        self._read_line = 0

    def sendMessage(self, sourceAddress: str, destAddress: str, opCode: str, payload: list = None) -> None:
        """
        Sends an opCode from a specified source and to a specified destination.

        Args:
          sourceAddress (str): The logical address of the source device (0-9 or A-F).
          destAddress (str): The logical address of the destination device (0-9 or A-F).
          opCode (str): Operation code to send as an hexidecimal string e.g 0x81.
          payload (list): List of hexidecimal strings to be sent with the opCode. Optional.
        """
        payload_string = ''
        if isinstance(payload, list):
            payload_string = ' '.join(payload)
        self._log.debug('Sending CEC message: Source=[%s] Dest=[%s] opCode=[%s] payload=[%s]' %
                        (sourceAddress, destAddress, opCode, payload_string))
        self.controller.sendMessage(sourceAddress, destAddress, opCode, payload=payload)

    def checkMessageReceived(self, sourceAddress: str, destAddress: str, opCode: str, timeout: int = 10, payload: list = None) -> bool:
        """
        This function checks to see if a specified opCode has been received.

        Args:
          sourceAddress (str): The logical address of the source device (0-9 or A-F).
          destAddress (str): The logical address of the destination device (0-9 or A-F).
          opCode (str): Operation code to send as an hexidecimal string e.g 0x81.
          timeout (int): The maximum amount of time, in seconds, that the method will
                           wait for the message to be received. Defaults to 10.
          payload (list): List of hexidecimal strings to be sent with the opCode. Optional.

        Returns:
            boolean: True if message is received. False otherwise.
        """
        result = False
        payload_string = ''
        if isinstance(payload, list):
            payload_string = ' '.join(payload)
        self._log.debug('Expecting CEC message: Source=[%s] Dest=[%s] opCode=[%s] payload=[%s]' %
                        (sourceAddress, destAddress, opCode, payload_string))
        received_message = self.controller.receiveMessage(sourceAddress, destAddress, opCode, timeout=timeout, payload=payload)
        if len(received_message) > 0:
            result = True
        return result

    def listDevices(self) -> list:
        """
        List CEC devices on CEC network.

        The list returned contains dicts in the following format:
            {'active source': False,
             'vendor': 'Unknown',
             'osd string': 'TV',
             'CEC version': '1.3a',
             'power status': 'on',
             'language': 'eng',
             'physical address': '0.0.0.0',
             'name': 'TV',
             'logical address': '0'}
        Returns:
            list: A list of dictionaries representing discovered devices.
        """
        self._log.debug('Listing devices on CEC network')
        return self.controller.listDevices()

    def start(self):
        """Start the CECContoller.
        """
        self.controller.start()

    def stop(self):
        """Stop the CECController.
        """
        self.controller.stop()

if __name__ == "__main__":
    import time
    import json
    LOG = logModule('CECTEST', logModule.DEBUG)
    CONFIGS = [
        {
            'type': 'cec-client',
            'adaptor': '/dev/ttyACM0' # This is default for pulse 8
        },
        {
            'type': 'remote-cec-client',
            'adaptor': '/dev/cec0', # This is default for Raspberry Pi
            'address': '', # Needs to be be filled out with IP address
            'username': '', # Needs to be filled out with login username
            'password': '', # Needs to be filled out with login password
            'prompt' : ''
        }
    ]
    for config in CONFIGS:
        LOG.setFilename(path.abspath('./logs/'),'CECTEST%s.log' % config.get('type'))
        LOG.stepStart('Testing with %s' % json.dumps(config))
        CEC = HDMICECController(LOG, config)
        DEVICES = CEC.listDevices()
        LOG.info(json.dumps(DEVICES))
        CEC.sendMessage('0', '2', '0x8f')
        result = CEC.receiveMessage('2', '0', '0x90', payload=['0x00'])
        LOG.stepResult(result, 'The readUntil result is: [%s]' % result)
        CEC.stop()

