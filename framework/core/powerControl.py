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
#*   ** @file        : powerControl.py
#*   ** @date        : 07/03/2019
#*   **
#*   ** @brief : Power On and Off STBs connected using power switch
#*   **
#* ******************************************************************************

#------- Control Outlet -----------------------------------
#
#     Name         : Outlet 8
#     Outlet       : 8
#     State        : ON
#
#     1- Immediate On
#     2- Immediate Off
#     3- Immediate Reboot
#     4- Delayed On
#     5- Delayed Off
#     6- Delayed Reboot
#     7- Cancel
###########################################################

from framework.core.powerModules.S20control import powerOrviboS20
from framework.core.powerModules.apcAos import powerApcAos
from framework.core.powerModules.kasaControl import powerKasa
from framework.core.powerModules.olimex import powerOlimex
from framework.core.powerModules.apc import powerAPC
from framework.core.powerModules.hs100 import powerHS100
from framework.core.powerModules.SLP import powerSLP
from framework.core.powerModules.none import powerNone
from framework.core.utilities import utilities

from framework.core.logModule import logModule

class powerControlClass():
    
    def __init__(self, log:logModule, config:dict):
        """Initalise the power controller 

        Args:
            log (logModule): log module class
            config (dict): configuration from the .yml file
        """
        self.log = log
        self.utils = utilities(log)
        self.ip = config.get("ip")
        self.name = config.get("name")

        # If variables are not passed in the config they will be defaulted to retryCount: [1], retryDelay: [30]
        self.retryCount = config.get("retryCount", 1)
        self.retryDelay = config.get("retryDelay", 30)
        if ( self.name == None ):
            self.name = self.ip
        self.powerOnState = False
        type = config.get("type")
        if type == None:
            self.powerSwitch = powerNone( log )
        elif type == "orviboS20":
            self.powerSwitch = powerOrviboS20( log, ip=self.ip, mac=config.get("mac"), port=config.get("port"))
        elif type == "hs100":
            self.powerSwitch = powerHS100( log, self.ip, config.get("port"))
        elif type == "apc":
            self.powerSwitch = powerAPC( log, self.ip, config.get("username"), config.get("password"), config.get("outlet"))
        elif type == "apcAos":
            self.powerSwitch = powerApcAos( log, self.ip, config.get("username"), config.get("password"), config.get("port",23), config.get("outlet"))
        elif type == "olimex":
            self.powerSwitch = powerOlimex( log, self.ip, config.get("port"), config.get("relay"))
        elif type == "kasa":
            self.powerSwitch = powerKasa( log, **config )
        elif type == "SLP":
            self.powerSwitch = powerSLP(log, self.ip, config.get("username"), config.get("password"), config.get("outlet_id"),config.get('port',23))
        elif type == "none":
            self.powerSwitch = powerNone( log )
        else:
            self.log.error("Power Switch [{}] unknown".format(type))
        return

    def powerOn(self):
        self.log.info("powerOn ({})".format( self.name ))
        result = self.powerRetry(self.powerSwitch.powerOn)
        if result == True:
            self.powerOnState = True
        return result


    def powerOff(self):
        self.log.info("powerOff ({})".format( self.name ))
        result = self.powerRetry(self.powerSwitch.powerOff)
        if result == True: 
            self.powerOnState = False
        return result


    def reboot(self):
        self.log.info("reboot")
        return self.powerRetry(self.powerSwitch.reboot)

    def powerRetry(self, powerMethod):
        """ Performs the passed powerMethod and retries it if it fails

        Args:
            powerMethod (Method): The powerMethod to perform

        Raises:
            e: Exception for if the powerMethod fails after all of the retries

        Returns:
            boolean: Whether the powerMethod was successfully performed
        """
        for x in range(self.retryCount+1):
            try:
                result = powerMethod()
                break
            except Exception as e:
                self.log.info(f"Could not perform {[powerMethod.__name__]}. Retry count: [{x}] of [{self.retryCount}], delay is [{self.retryDelay}]")
                if x == self.retryCount:
                    raise e 
                self.utils.wait(self.retryDelay)
        return result
