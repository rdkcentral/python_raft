#!/usr/bin/env python3
#** *****************************************************************************
#* Copyright (C) 2019 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core
#*   ** @file        : powerControl.py
#*   ** @date        : 26/05/2021
#*   **
#*   ** @brief : Common utils to support core framework
#*   **
#* ******************************************************************************

import re
import time

class utilities():
    def __init__(self, log):
        self.log = log

    def wait(self, seconds, minutes=0, hours=0):        
        self.log.info("Wait for [{}] seconds [{}] mins [{}] Hours".format(seconds, minutes, hours))
        waitTime = seconds
        if hours:
            waitTime += hours*60*60
        
        if minutes:
            waitTime += minutes*60

        time.sleep(waitTime)
        self.log.info('Wait over')
        return

    def fuzzyCompareText(self, expText, actualText, exactMatch=False):        
        self.log.info('fuzzyCompareText: expText - [{}] actualText - [{}]'.format(expText, actualText))
        
        result = False
        expText = expText.lower().replace(' ', '')
        actualText = actualText.lower().replace(' ', '')

        if exactMatch:
            result = expText == actualText
        else:
            result = True if re.search(expText.replace('*', '.*'), actualText) else False
        
        self.log.info('fuzzyCompareText returns - [{}]'.format(result))
        return result

    def value1HigherThanValue2(self, value1, value2):
        """Compares input values and returns result

        Args:
            value1 and value 2 (str) - values to be compared

        Returns:
            result (bool) - True if value1 is higher than value 2 else False
        """
        self.log.info('utils.value1HigherThanValue2 - value1 ({}), value2 ({})'.format(value1, value2))
        value1 = value1.split('.')
        value2 = value2.split('.')

        intValuesOfValue1 = [int(value) for value in value1]
        intValuesOfValue2 = [int(value) for value in value2]

        if intValuesOfValue1[0] > intValuesOfValue2[0]:
            return True
        
        if intValuesOfValue1[0] == intValuesOfValue2[0]:
            if intValuesOfValue1 [1] > intValuesOfValue2[1]:
                return True
            
            if intValuesOfValue1 [1] == intValuesOfValue2[1]:
                if intValuesOfValue1[2] > intValuesOfValue2[2]:
                    return True

        return False
