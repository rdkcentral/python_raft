#! /bin/python3
#/* *****************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core.powerModules
#*   ** @date        : 20/11/2021
#*   **
#*   ** @brief : wrapper for powerSwitch None
#*   **
#/* ******************************************************************************
import time

class powerNone():
    
    def __init__(self, log):
        """
        Initialize the PowerSwitchNone instance.

        Args:
            log: The log module.
        """
        self.log = log
        self.log.info("PowerSwitchNone()")
        pass

    def powerOn(self):
        """
        Turn on the power.

        Returns:
            bool: Always returns True.
        """
        self.log.info("powerSwitchNone().powerOn")
        return True

    def powerOff(self):
        """
        Turn off the power.

        Returns:
            bool: Always returns True.
        """
        self.log.info("powerSwitchNone().powerOff")
        return True

    def reboot(self):
        """
        Reboot the device.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        result = self.powerOff()
        if result != True:
            self.log.error(" Power Failed off")
        time.sleep(1)
        result = self.powerOn()
        if result != True:
            self.log.error(" Power Failed on")
        return result