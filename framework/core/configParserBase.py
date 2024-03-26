#!/usr/bin/env python3
#** *****************************************************************************
#* Copyright (C) 2019 Sky group of companies, All Rights Reserved
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
        """Class: configParser
        Args:
            config (dict): [dict of the decoded class]
            log ([class], optional): [parent log class if required]. Defaults to None.
        """
        self.log = log
        if log == None:
            self.log = logModule( "configParserBase" )

    def decodeTable(self, parent, config):
        """decode parent table

        Args:
            parent ([dict]): parent]
            config ([dict]): config to decode]
        """
        for x in config:
            self.decodeParam( parent, x, config[x] )

    def decodeParam(self, parent, name, value ):
        """Decode a single param

        Args:
            parent ([dict]): [parent string to fill out]
            name ([string]): [name]
            value ([string]): [value]
        """
        parent[name] = value
        self.log.debug("["+str(name)+"]:["+str(value)+"]")
   
    def __getFieldValue__( self, fieldDict, fieldName ):
        """Get the value from the group field, also confirm

        Args:
            fieldDict ([object]): [field dictionary]
            fieldName ([string]): [field name]

        Returns:
            [string]: [field value if present, otherwise None]
        """
        try:
            value = fieldDict[fieldName]
        except:
            self.log.error("Field [{}] Not found".format(fieldName))
            return None
        return value

