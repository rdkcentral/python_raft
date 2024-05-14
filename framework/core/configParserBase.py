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
#*   ** @file        : configParserBase.py
#*   ** @date        : 19/12/2018
#*   **
#*   ** @brief : Rack Testing Definition
#*   **
#* ******************************************************************************

from framework.core.logModule import logModule

class configParserBase():
    
    def __init__(self, config, log=None ):
        """Initialize the configParser class.

        Args:
            config (dict): Dictionary of the decoded class.
            log (class, optional): Parent log class if required. Defaults to None.
        """
        self.log = log
        if log == None:
            self.log = logModule( "configParserBase" )

    def decodeTable(self, parent, config):
        """Decode parent table.

        Args:
            parent (dict): Parent dictionary.
            config (dict): Config to decode.
        """
        for x in config:
            self.decodeParam( parent, x, config[x] )

    def decodeParam(self, parent, name, value ):
        """Decode a single parameter.

        Args:
            parent (dict): Parent dictionary to fill out.
            name (str): Name of the parameter.
            value (str): Value of the parameter.
        """
        parent[name] = value
        self.log.debug("["+str(name)+"]:["+str(value)+"]")
   
    def __getFieldValue__( self, fieldDict, fieldName ):
        """Get the value from the group field, also confirm.

        Args:
            fieldDict (object): Field dictionary.
            fieldName (str): Field name.

        Returns:
            str: Field value if present, otherwise None.
        """
        try:
            value = fieldDict[fieldName]
        except:
            self.log.error("Field [{}] Not found".format(fieldName))
            return None
        return value

