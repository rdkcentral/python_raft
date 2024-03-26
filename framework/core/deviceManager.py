#!/usr/bin/env python3
#** *****************************************************************************
#* Copyright (C) 2022 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core
#*   ** @date        : 05/07/2022
#*   ** @brief : Device Manager to control rack devices
#*   **
#* ******************************************************************************

from logging import exception
import os

from framework.core.commandModules.sshConsole import sshConsole
from framework.core.commandModules.serialClass import serialSession
from framework.core.commandModules.telnetClass import telnet
from framework.core.logModule import logModule
from framework.core.powerControl import powerControlClass
from framework.core.outboundClient import outboundClientClass
from framework.core.commonRemote import commonRemoteClass

dir_path = os.path.dirname(os.path.realpath(__file__))

class consoleClass():

    session = None

    def __init__(self, log:logModule, logPath:str, configElements:dict):
        """createConsole instance based on the params

        if a console is already active for the same device, it will be returned

        Args:
            log (logModule): console name
            logPath (str): path to write workspace files
            configElements (dict): dictionary for configuration

        Returns:
            class: console class
        """
        for element in configElements:
            config = configElements.get(element)
        self.type = config.get("type")
        # Create a new console since it hasn't been created
        if self.type == "ssh":
            address = config.get("address")
            if ( address == None ):
                address = config.get("ip")
            username = config.get("username")
            password = config.get("password")
            known_hosts = config.get("known_hosts")
            if not address:
                log.error("ssh console config has not been provided an [ip/address]")
            if not username:
                log.error("ssh console config has not been provided an [username]")
            self.session = sshConsole(address, username, password, known_hosts=known_hosts)
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
            self.session = serialSession(log, logPath, port, baudRate)
        elif self.type == "telnet":
            address = config.get("address")
            if ( address == None ):
                address = config.get("ip")
            username = config.get("username")
            password = config.get("password")
            port =  config.get("port",23)
            if not address:
                log.error("Telnet console config has not been provided an [addres/ip]")
            if not username:
                log.error("Telnet console config has not been provided a [username]")
            if not password:
                log.error("Telnet console config has not been provided a [password]")
            self.session = telnet(log, "", address, username, password, port)
        else:
            raise exception ("Unknown console type".format(self.type))
class deviceClass():
    """Single device with all controllers

    Raises:
        exception: none

    Returns:
        class: device class
    """

    def __init__(self, log:logModule, logPath:str, devices:dict):
        """Intialise a single decode from the config

        Args:
            log (logModule): log Module class
            logPath (str): path to write workspace files
            devices (dict): devices to initialise
        """
        #     # powerControl 
        #     # consoles
        #         # Serial
        #         # SSH
        #         # Telnet
        #     # outbound
        #     # remoteController
        self.consoles = dict()
        self.powerControl = None
        self.outBoundClient = None
        self.remoteController = None

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

    def getField(self, fieldName:str, itemsList:dict = None):
        """get a named field from the device

        Args:
            fieldName (str): name of the field to return
            itemsList (dict): get field from the items list, or None to start at the top

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
        """get the device console

        Args:
            consoleName (str, optional): console name. Defaults to "default".

        Returns:
            consoleClass: console class, or None on failure
        """
        console = self.consoles[consoleName]
        if console == None:
            self.log.error("Invalid consoleName [{}]".format(consoleName))
        return console.session

class deviceManager():

    rawConfig = dict()
    devices = dict()

    def __init__(self, deviceConfig:dict, log:logModule, logPath:str=""):
        """Initalise the device Managers

        Args:
            deviceConfig (dict): device list
            log (logModule): upper device module class
        """
        self.log = log
        self.logPath = logPath
        self.rawConfig = deviceConfig
        for x in deviceConfig:
            for name in x:
                self.devices[name] = deviceClass( log, logPath, x )

    def getDevice(self, deviceName:str="dut"):
        """Get an individual device configuration

        Args:
            deviceName (str, optional): device name. Defaults to "dut".

        Returns:
            dict: device dictionary, or None on failure
        """
        device = self.devices.get(deviceName)
        if device == None:
            self.log.error("Invalid deviceName [{}]".format(deviceName))
        return device

