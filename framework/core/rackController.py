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
        pass

    def checkRequiredField(self, config, name ):
        try:
            if config[name] != "":
                return
        except:
            self.log.error("Field ["+str(name)+"] - Must be defined")
            sys.exit(1)

    def decodeConfigItem( self, config, value, nameTable ):
        func = nameTable.get( config, "nothandled")
        if func == "nothandled":
            string = "Not handled:[",str(config),"]"
            self.log.error(string)
            return
        func( config, value )

    def setConfigValue(self, name, value ):
        self.config[name] = value
        self.log.debug("["+str(name)+"]:["+str(value)+"]")

    def dumpValue(self, x ):
        string = "["+x+"]:["+str(x.value)+"]"
        self.log.info( string )

class rackSlot(configDecoderClass):

    config = dict()

    def __init__(self, config:dict, log:logModule=None ):
        if ( log == None ):
            log = logModule("RackSlot")
        self.log = log
        self.config = config
        super().__init__()

    def getDevice( self, deviceName ):
        return self.find_name( self.config.get("devices"), deviceName )

    def find_name(self, table, name):
        for x in table:
            try:
                if x[name]:
                    return x[name]
            except:
                continue
        return None

# Get functions
    def get(self):
        return self

    def getName(self):
        return self.config.get("name")

    def getRackName(self):
        return self.config.get("rackName")

    def setRackName( self, rackName ):
        self.config[ "rackName" ] = rackName

    def getRemoteKeyType(self, deviceName = "dut"):
        myDevice = self.getDevice( deviceName )
        remoteController = myDevice.get("remoteController")
        remoteType = remoteController.get("type")
        return remoteType

    def getDeviceAddress(self, deviceName = "dut"):
        myDevice = self.getDevice( deviceName )
        deviceAddress = myDevice.get("address")
        if deviceAddress == None:
            deviceAddress = myDevice.get("ip")
        return deviceAddress

    def getDeviceIp(self, deviceName = "dut"):
        myDevice = self.getDevice( deviceName )
        ip = myDevice.get("ip")
        return ip

    def getPlatform(self, deviceName = "dut"):
        myDevice = self.getDevice( deviceName )
        result = myDevice.get("platform")
        return result
    
    def getOutboundUploadDirectory(self, deviceName="dut"):
        myDevice = self.getDevice( deviceName )
        result = myDevice.get("outbound").get("upload_url")
        return result

    def getOutboundDownloadDirectory(self, deviceName="dut"):
        myDevice = self.getDevice( deviceName )
        result = myDevice.get("outbound").get("download_url")
        return result

    def show( self):
        self.log.info("config[ {} ]".format(self.config))

class rack(configDecoderClass):

    slot = []

    def __init__(self, log=None):
        if ( log == None ):
            log = logModule("rack")
        self.log = log
        super().__init__()

    def addSlot( self, rackSlot ):
        self.slot.append( rackSlot )

    def getSlot( self, slotIndex ):
        if slotIndex == 0:
            self.log.error("Slot Index 1-x")
            sys.exit(1)
        try:
            return self.slot[slotIndex-1]
        except IndexError:
            self.log.error( "getSlot("+str(slotIndex)+") - Index Error")
            return None

    def getSlotByName( self, slotName ):
        for x in self.slots:
            if x.getName == slotName:
                return x
        self.log.error( "getSlot("+slotName+") - Not Found")
        return None
       
class rackController:
    racks = []
    description = ""

    def decodeRackConfig( self, rackConfig ):
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
        self.log = logModule( "rackController" )
        #self.log.setLevel( self.log.DEBUG )

        # Setup our new rack
        for x in config:
            if x.startswith("rack"):
                rack = self.decodeRackConfig( config[x] )
                self.racks.append( rack )

    def getRackByName(self, rackName):
        for element in self.racks:
            if ( element.config ["name"] == rackName ):
                return element
        self.log.error( "getRack("+str(rackName)+") - Invalid name")
        return None

    def getRackByIndex(self, rackIndex):
        try:
            rack = self.racks[rackIndex]
        except:
            self.log.error("Rack Not found")
            self.log.error( "getRackByIndex("+str(rackIndex)+") - Invalid name")
            sys.exit(1)
        return rack

    def getRackServerHostname( self, name ):
        for element in self.racks:
            if ( element.name == name ):
                return element.getServerHostname()
        return None

    def getRackDescription( self, name ):
        for element in self.racks:
            if ( element.name == name ):
                return element.description
        return None


           
