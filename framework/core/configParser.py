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
    """ConfigParser is a class designed to parse configuration data.
    """

    def __init__(self, config=None, log=None ):
        """
        Initializes a ConfigParser object.
    
        Args:
            config (dict): A dictionary containing the decoded configuration data.
            log (logModule, optional): The logModule to use for logging. 
                Defaults to None, in which case the ConfigParser starts its own logModule.
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
        """Decodes the top-level test config section.
            local:      -   Local config
            cpe:        -   cpe device configuration
            memoryMap:  -   memoryMap configuration
        
        Args:
            config (dict): The config dictionary.
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
        """Decodes the memory map config.
        
        Args:
            parent (str): The parent key in the config.
            config (dict): The config for the memory map sections.
        """
        self.memoryMap[parent] = dict()
        parent = self.memoryMap[parent]
        for x in config:
            if x.startswith("offsets"):
                self.decodeTable( parent, config )
            else:
                self.decodeParam( parent, x, config[x] )
    
    def updateCPEConfig(self, config):
        """Updates the CPE config.
        
        Args:
            config (dict): The config for the CPE section.
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
        """Creates a template of deviceConfig CPE entry.
        
        Args:
            imageLocationDict (dict): A dictionary containing image locations.
            platform (str): The platform of the device.

        Returns:
            cpeConfig (dict): A dictionary representing the CPE config.
        """             
        # TODO: Cover more params in future
        cpeConfig = {
            'platform': platform,
            'validImage': imageLocationDict
        }
        return cpeConfig

    def __decodeCPEConfig__(self, parent, config):
        """Decodes the CPE config.
        
        Args:
            parent (str): The parent key in the config.
            config (dict): The config for the CPE section.
        """
        self.cpe[parent] = dict()
        parent = self.cpe[parent]
        for x in config:
            if x.startswith("validImage"):
                self.decodeTable( parent, config )
            else:
                self.decodeParam( parent, x, config[x] )

    def getCPEEntryViaPlatform(self, platform):
        """Finds the CPE entry via the platform.
        
        Args:
            platform (str): The platform name.

        Returns:
            dict: The CPE dict entry, or None if not found.
        """
        for cpeParent in self.cpe:
            cpeEntry = self.cpe[cpeParent]
            if cpeEntry["platform"] == platform:
                return cpeEntry
        self.log.error("CPE Entry Not found for [{}]".format(platform))
        return None

    def getCPEFieldViaPlatform(self, platform, field):
        """Finds the CPE field via the platform.
        
        Args:
            platform (str): The platform name.
            field (str): The field to search for.

        Returns:
            dict: The CPE dict entry, or None if not found.
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
        """Finds the Memory Map entry via the platform.
        
        Args:
            platform (str): The platform name.

        Returns:
            dict: The memory map dict entry, or None if not found.
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
        """Finds the Memory Map item via the platform.
        
        Args:
            platform (str): The platform name.
            name (str): The name of the section.

        Returns:
            dict: The memory map dict entry, or None if not found.
        """
        map = self.getMemoryMapViaPlatform( platform )
        try:
            data = map["offsets"][name]
        except:
            raise Exception ("getMemoryMapValue[{}] Not Found".format(name))
            return None
        return data

    def getWorkspaceDirectory(self):
        """Gets the workspace directory.

        Returns:
            str: The workspace directory.
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
        """Gets the alternative platform from device config.
        """
        cpe = self.getCPEEntryViaPlatform( platform )
        if cpe == None:
            return None
        alternative_platform = self.__getFieldValue__( cpe, "alternative_platform")
        return alternative_platform

## Debate on these functions should they 

    def getImageField( self, imageName, fieldName, fieldValue ):
        """Searches and returns the image field specified.
        
        Args:
            imageName (str): The image name to search for.
            fieldName (str): The field to search for.
            fieldValue (str): The pattern to match the field.

        Returns:
            str: The URL.
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
        """Gets the negative image location via the platform.
        
        Args:
            platform (str): The platform string.

        Returns:
            str: The URL, or None if not found.
        """
        value = self.getCPEFieldViaPlatform( platform, "negativeImageLocation" )
        return value

    def getValidImageUrlViaPlatform(self, imageName, platform ):
        """Gets a valid image from the specified platform name.
        
        Args:
            imageName (str): The image name.
            platform (str): The platform name.

        Returns:
            str: The URL.
        """
        self.log.debug("getValidImageUrlViaPlatform([{}] [{}] [{}])".format( imageName, "platform", platform ))
        return self.getImageField( imageName, "platform", platform )

    def getValidImages(self, platform, filterString):
        """For the given platform, gets valid image names for the imageType in the testConfig.
        
        Args:
            platform (str): The device platform.
            filterString (str): The string to filter the matching valid image names.

        Returns:
            list: List of matching image names in testConfig.
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
