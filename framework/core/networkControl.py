#!/usr/bin/env python3
#** *****************************************************************************
# *
# * If not stated otherwise in this file or this component's LICENSE file the
# * following copyright and licenses apply:
# *
# * Copyright 2026 RDK Management
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
#*   ** @file        : networkControl.py
#*   **
#*   ** @brief : Network-level device control (e.g. Wake-on-LAN wake) for a DUT.
#*   **
#* ******************************************************************************

from framework.core.networkModules.wol import networkWol
from framework.core.utilities import utilities

from framework.core.logModule import logModule

class networkControlClass():

    def __init__(self, log:logModule, config:dict):
        """Initialise the network controller.

        Args:
            log (logModule): log module class
            config (dict): configuration from the .yml file (a device ``network:`` block)
        """
        self.log = log
        self.utils = utilities(log)
        self.name = config.get("name")

        # If variables are not passed in the config they will be defaulted to retryCount: [1], retryDelay: [30]
        self.retryCount = config.get("retryCount", 1)
        self.retryDelay = config.get("retryDelay", 30)

        self.networkModule = None
        type = config.get("type")
        if type == "wol":
            self.networkModule = networkWol(log, config.get("mac"), config.get("broadcast", "255.255.255.255"), config.get("port", 9))
        else:
            self.log.error("Network controller type [{}] unknown".format(type))
        return

    def wake(self):
        """Wake the device over the network (e.g. Wake-on-LAN magic packet).

        Returns:
            bool: True if the wake was successfully sent.
        """
        if self.networkModule is None:
            self.log.error("wake ({}): no network module configured (check 'type')".format(self.name))
            return False
        self.log.info("wake ({})".format(self.name))
        return self.networkRetry(self.networkModule.wake)

    def networkRetry(self, networkMethod):
        """Perform the passed networkMethod and retry it if it fails.

        Args:
            networkMethod (Method): The networkMethod to perform.

        Raises:
            e: Exception if the networkMethod fails after all of the retries.

        Returns:
            boolean: Whether the networkMethod was successfully performed.
        """
        for x in range(self.retryCount+1):
            try:
                result = networkMethod()
                break
            except Exception as e:
                self.log.info(f"Could not perform {[networkMethod.__name__]}. Retry count: [{x}] of [{self.retryCount}], delay is [{self.retryDelay}]")
                if x == self.retryCount:
                    raise e
                self.utils.wait(self.retryDelay)
        return result
