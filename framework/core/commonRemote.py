#!/usr/bin/env python3
#** *****************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core
#*   ** @date        : 22/11/2021
#*   **
#*   ** @brief : commonRemote with key mapping
#*   **
#* ******************************************************************************

import time
import yaml
import os
from framework.core.logModule import logModule
from framework.core.rcCodes import rcCode as rc
from framework.core.remoteControllerModules.olimex import remoteOlimex
from framework.core.remoteControllerModules.skyProc import remoteSkyProc
from framework.core.remoteControllerModules.arduino import remoteArduino
from framework.core.remoteControllerModules.none import remoteNone

class remoteControllerMapping():
    def __init__(self, log:logModule, mappingConfig:dict):
        """Initialise the remote controller key mapping class

        Args:
            log (logModule): log class
            mappingConfig (dict): mapping dictionary
        """
        self.log = log
        self.currentMap = None
        self.maps = mappingConfig
        try:
            defaultMap = mappingConfig[0]["name"]
        except:
            defaultMap = None
        self.setKeyMap( defaultMap )

    def getMappedKey(self, key:str):
        """Get the mapped key

        Args:
            key (str): Key to translate

        Returns:
            str: Translated key via map or None on failure
        """
        if self.currentMap == None:
            #self.log.info("No map defined")
            return key
        if not key in self.currentMap["codes"]:
            self.log.error("remoteControllerMapping.get() map=[{}] not found".format(self.currentMap["name"]))
            return None
            
        prefix = self.currentMap.get("prefix")
        returnedKey=self.currentMap["codes"].get(key)
        if prefix:
            returnedKey = prefix+key
        return returnedKey

    def getKeyMap(self):
        """Get key Map

        Returns:
            dict: Active key map
        """
        return self.currentMap
    
    def setKeyMap(self, newMapName:dict ):
        """Set the key map

        Args:
            newMapName (dict): Key map dictionary

        Returns:
            bool: True on success, or False if failure
        """
        if newMapName == None:
            return False
        if self.maps == None:
            self.log.error("RemoteController keyMap [{}] not found".format(newMapName))
            return False
        found = False
        for x in self.maps:
            if x["name"] == newMapName:
                self.currentMap = x
                found = True
                break
        if found == False:
            self.log.warn(" Map [{}] not found".format(newMapName))
            return False
        return True

class commonRemoteClass():
    def __init__(self, log:logModule, remoteConfig:dict, **kwargs:dict):
        """Intialise a commonRemote

        Args:
            log (logModule): log module.
            remoteConfig (dict): configuration file
        """
        self.log = log
        self.remoteConfig = remoteConfig
        rcMappingConfig = self.__decodeRemoteMapConfig()
        keyMap = remoteConfig.get("map")
        self.remoteMap = remoteControllerMapping( log, rcMappingConfig )
        self.setKeyMap( keyMap )
        self.type = remoteConfig.get("type")
        if self.type == "olimex":
            self.remoteController = remoteOlimex( self.log, remoteConfig )
        elif self.type == "sky_proc":
            self.remoteController = remoteSkyProc( self.log, remoteConfig )
        elif self.type == "arduino":
            self.remoteController = remoteArduino (self.log, remoteConfig)
        else:   # remoteNone otherwise
            self.remoteController = remoteNone( self.log, remoteConfig )

    def __decodeRemoteMapConfig(self):
        """Decode the remote map configuration file
        """
        configFile = self.remoteConfig.get("config")
        if configFile == None:
            return
        fullPath = configFile
        if fullPath.startswith("."):
            fullPath = os.path.abspath(configFile)
        if os.path.exists(fullPath) == False:
            print("config: file is required to run: ERROR, missing url=[{}]".format(fullPath))
            os._exit(1)
        with open(configFile) as inputFile:
            inputFile.seek(0, os.SEEK_SET)
            config = yaml.full_load(inputFile)
        keyDictionary = {}
        for key, val in config.items():
            if isinstance(val, dict):
                for k, v in val.items():
                    keyDictionary[k] = v 
            else:
                keyDictionary[key] = val
        return keyDictionary

    def sendKey(self, keycode:dict, delay:int=1, repeat:int=1, randomRepeat:int=0):
        """Send a key to the remoteCommander

        Args:
            keycode (dict): Key value pair
            delay (int, optional): Delay in seconds between repeats. Defaults to 1.
            repeat (int, optional): How many key repeats. Defaults to 1.
            randomRepeat (int, optional): Random Key repeat value. Defaults to 0.
        """
        if (randomRepeat != 0):
            import random
            repeat=random.randint(0, randomRepeat)
            self.log.info( "sendKey[" + keycode.name + "] delay:[" +str(delay)+"] randomRepeat:["+str(randomRepeat)+"] -> repeat:["+str(repeat)+"]" )
        else:
            if (repeat != 1):
                self.log.info( "sendKey[" + keycode.name + "] delay:[" +str(delay)+"] repeat:["+str(repeat)+"]" )
            else:            
                self.log.info( "sendKey[" + keycode.name + "] delay:[" +str(delay)+"]" )

        mappedCode = self.remoteMap.getMappedKey( keycode.name )
        result = self.remoteController.sendKey( mappedCode, repeat, delay)

    def setKeyMap( self, name:dict ):
        """Set the Key Translation Map

        Args:
            name (dict): Translation dictionary
        """
        self.remoteMap.setKeyMap( name )

    def getKeyMap( self ):
        """Get the Key Translation Map
        """
        self.remoteMap.getKeyMap()
