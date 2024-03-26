#!/usr/bin/env python3
#** *****************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core.remoteControllerModules
#*   ** @date        : 22/11/2021
#*   **
#*   ** @brief : remote none
#*   **
#* ******************************************************************************

import time
from framework.core.logModule import logModule

class remoteNone():
    
    def __init__( self, log:logModule, remoteConfig:dict):
        """Initalise a remoteNone class

        Args:
            log (logModule): logging module
            remoteConfig (dict): remote controller configuration
        """
        self.log = log
  
    def sendKey(self, code:str, repeat:int, delay:int ):
        """Send a key

        Args:
            code (str): keycode
            repeat (int): number of repeats required
            delay (int): delay in seconds between repeats

        Returns:
            bool: true on success otherwise failure
        """
        if code == None:
            return False

        for _ in range(repeat):
            self.log.info("remoteNone: sendKey( code=[{}] repeat=[{}] delay=[{}] )".format( code, repeat, delay ) )
            time.sleep( delay )

        return True