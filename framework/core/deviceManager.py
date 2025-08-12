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
#*   ** @date        : 05/07/2022
#*   ** @brief : Device Manager to control rack devices
#*   **
#* ******************************************************************************

from logging import exception
import time
import platform
import os

from framework.core.commandModules.sshConsole import sshConsole
from framework.core.commandModules.serialClass import serialSession
from framework.core.commandModules.telnetClass import telnet
from framework.core.logModule import logModule
from framework.core.powerControl import powerControlClass
from framework.core.outboundClient import outboundClientClass
from framework.core.commonRemote import commonRemoteClass
from framework.core.hdmiCECController import HDMICECController
from framework.core.utilities import utilities

dir_path = os.path.dirname(os.path.realpath(__file__))

class consoleClass():
    """Represents a console for interacting with a device.
    """
    session = None

    def __init__(self, log:logModule, logPath:str, configElements:dict):
        """
        Initialises a console instance based on the parameters.

        If a console is already active for the same device, it will be returned.

        Args:
            log (logModule): Log module instance.
            logPath (str): Path to write workspace files.
            configElements (dict): Dictionary for configuration.

        Returns:
            class: Console class instance.
        """
        for element in configElements:
            config = configElements.get(element)
        self.type = config.get("type")
        self.prompt = config.get("prompt")
        # Create a new console since it hasn't been created
        if self.type == "ssh":
            address = config.get("address")
            if ( address == None ):
                address = config.get("ip")
            username = config.get("username")
            password = config.get("password")
            known_hosts = config.get("known_hosts")
            port = int(config.get("port",22))
            if not address:
                log.error("ssh console config has not been provided an [ip/address]")
            if not username:
                log.error("ssh console config has not been provided an [username]")
            self.session = sshConsole(log, address, username, password, known_hosts=known_hosts, port=port, prompt=self.prompt)
        elif self.type == "serial":
            port = config.get("port")
            baudRate = config.get("baudRate")
            parity = config.get("parity")
            dataBits = config.get("dataBits")
            stopBits = config.get("stopBits")
            flowControl = config.get("flowControl")
            if not port:
                log.error( "Serial console config has not been provided a port")
            if not baudRate:
                baudRate = 115200
            if not dataBits:
                dataBits = 8
            if not parity:
                parity = "None"
            if not stopBits:
                stopBits = 1
            if not flowControl:
                flowControl = False

            #TODO: Pass more params to the serial session
            self.session = serialSession(log, logPath, port, baudRate, prompt=self.prompt)
        elif self.type == "telnet":
            address = config.get("address")
            if ( address == None ):
                address = config.get("ip")
            username = config.get("username")
            password = config.get("password")
            port =  config.get("port",23)
            username_prompt = config.get("username_prompt")
            password_prompt = config.get("password_prompt")
            if not address:
                log.error("Telnet console config has not been provided an [addres/ip]")
            if not username:
                log.error("Telnet console config has not been provided a [username]")
            if not password:
                log.error("Telnet console config has not been provided a [password]")
            self.session = telnet(log, "",
                                  address,
                                  username,
                                  password,
                                  port,
                                  prompt=self.prompt,
                                  username_prompt=username_prompt,
                                  password_prompt=password_prompt)
        else:
            raise exception ("Unknown console type".format(self.type))

class deviceClass():
    """Represents a single device with all controllers
    """

    def __init__(self, log:logModule, logPath:str, devices:dict):
        """
        Initialises a single device from the config.

        Args:
            log (logModule): Log module class.
            logPath (str): Path to write workspace files.
            devices (dict): Devices to initialize.
        """
        #     # powerControl 
        #     # consoles
        #         # Serial
        #         # SSH
        #         # Telnet
        #     # outbound
        #     # remoteController
        #     # hdmiCECController
        self.log = log
        self.consoles = dict()
        self.powerControl = None
        self.outBoundClient = None
        self.remoteController = None
        self.hdmiCECController = None
        self.session = None
        self.alive = False

        self.rawConfig = devices
        for element in devices:
            self.deviceName = element
            device = devices[element]
            config = device.get("powerSwitch")
            if config != None:
                self.powerControl = powerControlClass( log, config )
            consoles = device.get("consoles")
            for element in consoles:
                for name in element:
                    self.consoles[name] = consoleClass(log, logPath, element )
            config = device.get("outbound")
            if config != None:
                self.outBoundClient = outboundClientClass(log, **config)
            config = device.get("remoteController")
            if config != None:
                self.remoteController = commonRemoteClass(log, config)
            config = device.get("hdmiCECController")
            if config != None:
                self.hdmiCECController = HDMICECController(log, config)
        self.session = self.getConsoleSession()

    def getField(self, fieldName:str, itemsList:dict = None):
        """Gets a named field from the device

        Args:
            fieldName (str): name of the field to return
            itemsList (dict): gets field from the items list, or None to start at the top

        Returns:
            str: field value, None on error
        """
        if itemsList == None:
            itemsList = self.rawConfig
        for k, v in itemsList.items():
            if isinstance(v,dict):
                result = self.getField( fieldName, v)
                if result != None:
                    return result
            else:
                if k == fieldName:
                    return v
        return None

    def getConsoleSession(self, consoleName:str="default" ):
        """Gets the device console

        Args:
            consoleName (str, optional): console name. Defaults to "default".

        Returns:
            consoleClass: Console class, or None on failure
        """
        console = self.consoles[consoleName]
        if console == None:
            self.log.error("Invalid consoleName [{}]".format(consoleName))
        return console.session
    
    def pingTest(self, logPingTime=False):
        """Perform a ping test against the given device.

        Args:
            logPingTime (bool, optional): Log ping time. Defaults to False.

        Returns:
            bool: True if host is up, False otherwise.
        """
        #Ping the box till the box responds after the boot

        elapsed_string = "unknown"

        if logPingTime:
            pingStartTime = time.time()
            timeString = time.strftime("%H:%M:%S",time.gmtime(pingStartTime))
            self.log.step("ping start time: [{}]".format(timeString) )
        
        self.alive = self._pingTestOnly()
        
        if logPingTime:
            elapsed_time = time.time() - pingStartTime
            timeString = time.strftime("%H:%M:%S",time.gmtime(time.time()))
            self.log.step("ping response time: [{}]".format(timeString) )
            elapsed_string = time.strftime( "%H:%M:%S", time.gmtime(elapsed_time))              
            self.log.step("Time taken to get ping response: ["+elapsed_string+"]")
        # We've not be able to ping the box, return an error
        
        if not self.alive:
            self.log.critical( "ping Up Check:[Box is not responding to ping within:"+elapsed_string+"]")
            raise Exception(" ping failed")           
        
        return self.alive

    def _pingTestOnly(self):
        """Perform a ping test against the given device.

        Returns:
            bool: True if host is up, False otherwise.
        """
        hostIsUp = False
        ip = self.getField("ip")
        
        if platform.system().lower() == 'windows' or 'cygwin' in platform.system().lower():
            ping_param_amount = " -n "
            ping_param_quiet = " "
        else:
            ping_param_amount = " -c "
            ping_param_quiet = " -q "
        
        # Quick check for ping working first time round
        command  = "ping" + ping_param_amount + "1" + ping_param_quiet + ip
        result = utilities(self.log).syscmd(command)
        
        if result[1] == 0:
            self.log.debug("ping response 1 - Host Up")
            return True
        
        #Host is currently down, we need to loop
        for x in range( 0, 15 ):
            self.log.debug("pingTest Inner Loop["+str(x)+"]")
            utilities(self.log).wait(5) # Wait 5 seconds before trying constant ping
            result = utilities(self.log).syscmd( "ping" + ping_param_amount + "10" + ping_param_quiet + ip)
            
            if result[1] == 0:
                # Check for 0% packet loss, otherwise reject it
                outputString = str(result[0])
                if ", 0% packet loss" in outputString:
                    hostIsUp = True
                    self.log.debug("pingTest hostIsUp")
                    break
            self.log.debug("pingTest hostIsDown")
        
        return hostIsUp

class deviceManager():
    """Manages device configurations.
    """
    
    rawConfig = dict()
    devices = dict()

    def __init__(self, deviceConfig:dict, log:logModule, logPath:str=""):
        """Initalises the device managers

        Args:
            deviceConfig (dict): Device list.
            log (logModule): Upper device module class.
            logPath (str, optional): Path to write log files. Defaults to "".
        """
        self.log = log
        self.logPath = logPath
        self.rawConfig = deviceConfig
        for x in deviceConfig:
            for name in x:
                self.devices[name] = deviceClass( log, logPath, x )

    def getDevice(self, deviceName:str="dut"):
        """Gets an individual device configuration

        Args:
            deviceName (str, optional): Device name. Defaults to "dut".

        Returns:
            dict: Device dictionary, or None on failure
        """
        device = self.devices.get(deviceName)
        if device == None:
            self.log.error("Invalid deviceName [{}]".format(deviceName))
        return device

