#!/usr/bin/env python3
#** *****************************************************************************
#* Copyright (C) 2019 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core
#*   ** @file        : racks.py
#*   ** @date        : 19/12/2018
#*   **
#*   ** @brief : Rack Testing Definition
#*   **
#* ******************************************************************************

from enum import Enum
from logging import exception
import sys

from framework.core.logModule import logModule as logModule

class configDecoderClass():

    def __init__( self ):
        """Initialize the configDecoderClass."""
        pass

    def checkRequiredField(self, config, name ):
        """Check if a required field is present in the configuration.

        Args:
            config (dict): Configuration dictionary.
            name (str): Name of the field to check.

        Raises:
            KeyError: If the required field is not found.
        """
        try:
            if config[name] != "":
                return
        except:
            self.log.error("Field ["+str(name)+"] - Must be defined")
            sys.exit(1)

    def decodeConfigItem( self, config, value, nameTable ):
        """Decode a configuration item based on a name table.

        Args:
            config (str): Configuration item to decode.
            value: Value of the configuration item.
            nameTable (dict): Name table for decoding.

        Raises:
            KeyError: If the configuration item is not handled.
        """
        func = nameTable.get( config, "nothandled")
        if func == "nothandled":
            string = "Not handled:[",str(config),"]"
            self.log.error(string)
            return
        func( config, value )

    def setConfigValue(self, name, value ):
        """Set a configuration value.

        Args:
            name (str): Name of the configuration.
            value: Value to set.

        Returns:
            None
        """
        self.config[name] = value
        self.log.debug("["+str(name)+"]:["+str(value)+"]")

    def dumpValue(self, x ):
        """Dump a value.

        Args:
            x: Value to dump.

        Returns:
            None
        """
        string = "["+x+"]:["+str(x.value)+"]"
        self.log.info( string )

class rackSlot(configDecoderClass):

    config = dict()

    def __init__(self, config:dict, log:logModule=None ):
        """Initialize the rackSlot.

        Args:
            config (dict): Configuration dictionary.
            log (logModule, optional): Log module. Defaults to None.
        """
        if ( log == None ):
            log = logModule("RackSlot")
        self.log = log
        self.config = config
        super().__init__()

    def getDevice( self, deviceName ):
        """Get a device from the slot.

        Args:
            deviceName (str): Name of the device.

        Returns:
            Any: Device information.
        """
        return self.find_name( self.config.get("devices"), deviceName )

    def find_name(self, table, name):
        """Find a name in a table.

        Args:
            table (list): List of dictionaries.
            name (str): Name to find in the dictionaries.

        Returns:
            Any: Value associated with the name if found, otherwise None.
        """
        for x in table:
            try:
                if x[name]:
                    return x[name]
            except:
                continue
        return None

# Get functions
    def get(self):
        """Get the rackSlot.

        Returns:
            rackSlot: The rackSlot.
        """
        return self

    def getName(self):
        """Get the name of the rackSlot.

        Returns:
            str: Name of the rackSlot.
        """
        return self.config.get("name")

    def getRackName(self):
        """Get the name of the rack.

        Returns:
            str: Name of the rack.
        """
        return self.config.get("rackName")

    def setRackName( self, rackName ):
        """Set the name of the rack.

        Args:
            rackName (str): Name of the rack.
        """
        self.config[ "rackName" ] = rackName

    def getRemoteKeyType(self, deviceName = "dut"):
        """Get the remote key type.

        Args: 
            deviceName (str): Name of the device. Defaults to "dut".

        Returns:
            str: Name of the remote key type.
        """
        myDevice = self.getDevice( deviceName )
        remoteController = myDevice.get("remoteController")
        remoteType = remoteController.get("type")
        return remoteType

    def getDeviceAddress(self, deviceName = "dut"):
        """Get the device address.

        Args: 
            deviceName (str): Name of the device. Defaults to "dut".
            
        Returns:
            str: Name of the device address.
        """
        myDevice = self.getDevice( deviceName )
        deviceAddress = myDevice.get("address")
        if deviceAddress == None:
            deviceAddress = myDevice.get("ip")
        return deviceAddress

    def getDeviceIp(self, deviceName = "dut"):
        """Get the device ip.

        Args: 
            deviceName (str): Name of the device. Defaults to "dut".
            
        Returns:
            str: The device ip.
        """
        myDevice = self.getDevice( deviceName )
        ip = myDevice.get("ip")
        return ip

    def getPlatform(self, deviceName = "dut"):
        """Get the device platform.

        Args: 
            deviceName (str): Name of the device. Defaults to "dut".
            
        Returns:
            str: Name of the device platform.
        """
        myDevice = self.getDevice( deviceName )
        result = myDevice.get("platform")
        return result
    
    def getOutboundUploadDirectory(self, deviceName="dut"):
        """Get the outbound upload directory.

        Args: 
            deviceName (str): Name of the device. Defaults to "dut".
            
        Returns:
            str: Name of the outbound upload directory.
        """
        myDevice = self.getDevice( deviceName )
        result = myDevice.get("outbound").get("upload_url")
        return result

    def getOutboundDownloadDirectory(self, deviceName="dut"):
        """Get the outbound download directory.

        Args: 
            deviceName (str): Name of the device. Defaults to "dut".
            
        Returns:
            str: Name of the outbound download directory.
        """
        myDevice = self.getDevice( deviceName )
        result = myDevice.get("outbound").get("download_url")
        return result

    def show( self):
        """Show the configuration of the rackSlot.
        """
        self.log.info("config[ {} ]".format(self.config))

class rack(configDecoderClass):

    slot = []

    def __init__(self, log=None):
        """Initialize the rack.

        Args:
            log (logModule, optional): Log module. Defaults to None.
        """
        if ( log == None ):
            log = logModule("rack")
        self.log = log
        super().__init__()

    def addSlot( self, rackSlot ):
        """Add a slot to the rack.

        Args:
            rackSlot (rackSlot): Rack slot to add.

        Returns:
            None
        """
        self.slot.append( rackSlot )

    def getSlot( self, slotIndex ):
        """Get a slot from the rack.

        Args:
            slotIndex (int): Index of the slot.

        Returns:
            rackSlot: The requested rack slot.
        """
        if slotIndex == 0:
            self.log.error("Slot Index 1-x")
            sys.exit(1)
        try:
            return self.slot[slotIndex-1]
        except IndexError:
            self.log.error( "getSlot("+str(slotIndex)+") - Index Error")
            return None

    def getSlotByName( self, slotName ):
        """Get a slot from the rack by name.

        Args:
            slotName (str): Name of the slot.

        Returns:
            rackSlot: The requested rack slot.
        """
        for x in self.slots:
            if x.getName == slotName:
                return x
        self.log.error( "getSlot("+slotName+") - Not Found")
        return None
       
class rackController:
    racks = []
    description = ""

    def decodeRackConfig( self, rackConfig ):
        """Decode the rack configuration.

        Args:
            rackConfig (dict): Rack configuration.

        Returns:
            rack: The decoded rack.
        """
        # Setup a new rack
        newRack = rack(self.log)
        newRack.rawConfig = rackConfig
        rackName = rackConfig.get("name")
        newRack.name = rackName

        # TODO: Clean this up, don't think it's required if we just assign the dictionary to it.
        # Setup the slot configuration
        for x in rackConfig:
            if x.startswith("slot"):
                slotConfig = rackConfig[x]
                newSlot = rackSlot(slotConfig,self.log)
                #Add the slot to the list
                newRack.addSlot(newSlot)
        return newRack

    def __init__(self, config ):
        """Initialize the rack controller.

        Args:
            config: Configuration.
        """
        self.log = logModule( "rackController" )
        #self.log.setLevel( self.log.DEBUG )

        # Setup our new rack
        for x in config:
            if x.startswith("rack"):
                rack = self.decodeRackConfig( config[x] )
                self.racks.append( rack )

    def getRackByName(self, rackName):
        """Get a rack by name.

        Args:
            rackName (str): Name of the rack.

        Returns:
            rack: The requested rack.
        """
        for element in self.racks:
            if ( element.config ["name"] == rackName ):
                return element
        self.log.error( "getRack("+str(rackName)+") - Invalid name")
        return None

    def getRackByIndex(self, rackIndex):
        """Get a rack by index.

        Args:
            rackIndex (int): Index of the rack.

        Returns:
            rack: The requested rack.
        """
        try:
            rack = self.racks[rackIndex]
        except:
            self.log.error("Rack Not found")
            self.log.error( "getRackByIndex("+str(rackIndex)+") - Invalid name")
            sys.exit(1)
        return rack

    def getRackServerHostname( self, name ):
        """Get the server hostname of a rack.

        Args:
            name (str): Name of the rack.

        Returns:
            str: Server hostname of the rack.
        """
        for element in self.racks:
            if ( element.name == name ):
                return element.getServerHostname()
        return None

    def getRackDescription( self, name ):
        """Get the description of a rack.

        Args:
            name (str): Name of the rack.

        Returns:
            str: Description of the rack.
        """
        for element in self.racks:
            if ( element.name == name ):
                return element.description
        return None


           
