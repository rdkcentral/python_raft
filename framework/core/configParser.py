#!/usr/bin/env python3
#** *****************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core
#*   ** @date        : 19/12/2018
#*   **
#*   ** @brief : global test config, for ALL platforms, no platform specific code in here
#*   **
#* ******************************************************************************
import os
from urllib.parse import urlparse
from framework.core.logModule import logModule as logModule
from framework.core.configParserBase import configParserBase

class configParser(configParserBase):

    def __init__(self, config=None, log=None ):
        """Class: configParser
        Args:
            config (dict): [dict of the decoded class]
            log ([class], optional): [parent log class if required]. Defaults to None.
        """
        self.log = log
        if log == None:
            self.log = logModule( "configParser" )
            #self.log.setLevel( self.log.DEBUG )

        self.local = dict()
        self.cpe = dict()
        self.memoryMap = dict()
        self.validImages = dict()
        if config is not None:
            self.decodeConfig( config )

    def decodeConfig(self, config ):
        """decode the test config section top level
            local:      -   Local config
            cpe:        -   cpe device configuration
            memoryMap:  -   memoryMap configuration

        Args:
            config ([dict]): [config dictionary]
        """
        for x in config:
            # Items from rack config
            if x.startswith("local"):
                self.decodeTable( self.local, config[x] )
            # CPE Config
            if x.startswith("cpe"):
                self.__decodeCPEConfig__( x, config[x] )
            if x.startswith('memoryMap'):
                self.__decodeMemoryMapConfig__( x, config[x] )

    def __decodeMemoryMapConfig__(self, parent, config):
        """decode the memory map config

        Args:
            config ([dict]): [config for the memory map sections]
        """
        self.memoryMap[parent] = dict()
        parent = self.memoryMap[parent]
        for x in config:
            if x.startswith("offsets"):
                self.decodeTable( parent, config )
            else:
                self.decodeParam( parent, x, config[x] )
    
    def updateCPEConfig(self, config):
        """update the CPE config

        Args:
            config ([dict]): [config for the cpe section]
        """
        # Find the config that has the same cpe.platform, this will be the override
        for x in self.cpe:
            cpePlatform = self.cpe[x]["platform"]
            if config["platform"] == cpePlatform:
                parent=self.cpe[x]
                for x in config:
                    if x.startswith("validImage"):
                        self.decodeTable( parent["validImage"], config["validImage"] )
                    else:
                        self.decodeParam( parent, x, config[x] )
                break

    def createCpeConfig(self, imageLocationDict, platform):
        """Creates template of deviceConfig cpe entry

        Args:
            imageLocationDict (dict) 
            Ex: {PCI1: "http://testwebsite.com/image.bin"}

            platform (str) - platorm of the device (Ex: ada.sr300)

        Returns:
            cpeConfig (dict)
            Ex:{
                    {platform: "test_platform",
                    validImage:
                        {PCI1: "http://testwebsite.com/image.bin"}
                    }
                }                
        """
        # TODO: Cover more params in future
        cpeConfig = {
            'platform': platform,
            'validImage': imageLocationDict
        }
        return cpeConfig

    def __decodeCPEConfig__(self, parent, config):
        """decode the CPE config

        Args:
            config ([dict]): [config for the cpe section]
        """
        self.cpe[parent] = dict()
        parent = self.cpe[parent]
        for x in config:
            if x.startswith("validImage"):
                self.decodeTable( parent, config )
            else:
                self.decodeParam( parent, x, config[x] )

    def getCPEEntryViaPlatform(self, platform):
        """[find the cpe entry via the platform ]

        Args:
            platform ([string]): [platform name e.g. "xione.de"]

        Returns:
            [dict]: [cpe dict entry, or None if not found]
        """
        for cpeParent in self.cpe:
            cpeEntry = self.cpe[cpeParent]
            if cpeEntry["platform"] == platform:
                return cpeEntry
        self.log.error("CPE Entry Not found for [{}]".format(platform))
        return None

    def getCPEFieldViaPlatform(self, platform, field):
        """[find the cpe entry via the platform ]

        Args:
            platform ([string]): [platform name e.g. "xione.de"]

        Returns:
            [dict]: [cpe dict entry, or None if not found]
        """
        self.log.debug("configParser.getCPEFieldViaPlatform([{}][{}])".format(platform,field))
        for cpeParent in self.cpe:
            cpeEntry = self.cpe[cpeParent]
            if cpeEntry["platform"] == platform:
                try:
                    value = cpeEntry[field]
                except:
                    raise Exception ("CPE Entry Not found for [{}][{}]".format(platform,field))
                    return None
                return value
        self.log.error("CPE Entry Not found for [{}][{}]".format(platform,field))
        return None

    def getMemoryMapViaPlatform(self, platform):
        """[find the Memory Map entry via the platform ]

        Args:
            platform ([string]): [platform name e.g. "xione.de"]

        Returns:
            [dict]: [memory map dict entry, or None if not found]
        """
        cpe = self.getCPEEntryViaPlatform( platform )
        if cpe == None:
            return None
        requiredMap = self.__getFieldValue__( cpe, "memoryMap")
        if requiredMap == None:
            return None
        for x in self.memoryMap:
            map = self.memoryMap[x]
            if map["platform"] == requiredMap:
                return map
        self.log.error("Memory Map not found [{}]".format(platform))
        return None

    def getMemoryMapValueViaPlatform(self, platform, name ):
        """[find the Memory Map item via the platform ]

        Args:
            platform ([string]): [platform name e.g. "xione.de"]
            name ([string]): [name of the section like "BL1Offset"]

        Returns:
            [dict]: [memory map dict entry, or None if not found]
        """
        map = self.getMemoryMapViaPlatform( platform )
        try:
            data = map["offsets"][name]
        except:
            raise Exception ("getMemoryMapValue[{}] Not Found".format(name))
            return None
        return data

    def getWorkspaceDirectory(self):
        """[get the workspace directory]

        Returns:
            [string]: [workspace directory]
        """
        result = self.__getFieldValue__( self.local, "workspaceDirectory" )
        if result is None:
            raise Exception ("[workspaceDirectory] Not found")
            return None
        if len(result)<2:
            return result
        if result[0]=='~' and result[1]=='/':
            result = os.path.expanduser(result) 
        return result

    def getAlternativePlatform(self, platform):
        """Get the alternative platform from device config
        """
        cpe = self.getCPEEntryViaPlatform( platform )
        if cpe == None:
            return None
        alternative_platform = self.__getFieldValue__( cpe, "alternative_platform")
        return alternative_platform

## Debate on these functions should they 

    def getImageField( self, imageName, fieldName, fieldValue ):
        """Search and return the image field specified

        Args:
            imageName ([string]): [image name to search for]
            fieldName ([string]): [field to search for]
            fieldValue ([string]): [pattern to match the field]

        Returns:
            [string]: [url]
        """
        self.log.debug("getImageField([{}] [{}] [{}])".format( imageName, fieldName, fieldValue ))
        for cpeParent in self.cpe:
            cpeEntry = self.cpe[cpeParent]
            if cpeEntry[fieldName] == fieldValue:
                try:
                    parent = cpeEntry["validImage"]
                except:
                    self.log.error("validImage field not found")
                    return None
                for imageNameEntry in parent:
                    if imageNameEntry == imageName:
                        location = parent[imageNameEntry]
                        try:
                            baseUrl = parent["baseLocation"]
                        except:
                            baseUrl = ""
                        # If we don't have our own scheme, then we need to add the base URL
                        if isinstance(location, list):
                            newList = []
                            for eachLocation in location:
                                url = urlparse( eachLocation )
                                if url.scheme == "":
                                    newList.append(baseUrl + eachLocation)
                                else:
                                    newList.append(eachLocation)
                            location = newList
                        else:
                            url = urlparse( location )
                            if url.scheme == "":
                                location = baseUrl + location
                        return location
        return None

    def getNegativeImageUrlViaPlatform(self, platform):
        """Get the negative image location via the platform

        Args:
            platform ([string]): [platform string e.g. xione.de, llama.uk]
        Returns:
            [string]: [url or none if not found]
        """
        value = self.getCPEFieldViaPlatform( platform, "negativeImageLocation" )
        return value

    def getValidImageUrlViaPlatform(self, imageName, platform ):
        """[gets a valid image from the specified platform name]

        Args:
            imageName ([string]): [image name , "PCI1, PCI2, PDRI, BDRI etc" from the config]
            platform ([string]): [platform name e.g. "xione.de"]
        Returns:
            [string]: [url]
        """
        self.log.debug("getValidImageUrlViaPlatform([{}] [{}] [{}])".format( imageName, "platform", platform ))
        return self.getImageField( imageName, "platform", platform )

    def getValidImages(self, platform, filterString):
        """For the given platform, gets valid image names for the imageType in the testConfig

        Args:
            filterString (str) - To filter the matching valid image names Ex: PCI \ DRI etc.,
            platform (str) - device platform. Ex: ada.sr300 or xione.de etc.,

        Returns:
            validNames (list) - List of matching image names in testConfig (Ex: For DRI, it returns BDRI\PDRI)
        """
        validNames = []
        for cpeParent in self.cpe:
            cpeEntry = self.cpe[cpeParent]
            if cpeEntry['platform'] == platform:
                try:
                    parent = cpeEntry["validImage"]
                except:
                    self.log.error("validImage field not found")
                    return None
                for imageNameEntry in parent:
                    if filterString in imageNameEntry and "_" not in imageNameEntry:
                        validNames.append(imageNameEntry)
        return validNames
