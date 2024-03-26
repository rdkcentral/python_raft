#!/usr/bin/env python3
#** *****************************************************************************
#* Copyright (C) 2019 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core
#*   ** @file        : rcCodes.py
#*   ** @date        : 17/01/2019
#*   **
#*   ** @brief : Remote Control Code Wrapper class
#*   **
#* ******************************************************************************

from enum import Enum

class rcCode(Enum):
    #------ PORTABLE FOR /proc ----------
    NUM_0    = "0x00"
    NUM_1    = "0x01"
    NUM_2    = "0x02"
    NUM_3    = "0x03"
    NUM_4    = "0x04"
    NUM_5    = "0x05"
    NUM_6    = "0x06"
    NUM_7    = "0x07"
    NUM_8    = "0x08"
    NUM_9    = "0x09"
    # PREVPROG = "0x0A" # No action
    POWER    = "0x0C"
    MUTE     = "0x0D"
    VOL_UP   = "0x10"   # No actionon the TV with IR, may work via bluetooth
    VOL_DOWN  = "0x11" # No actionon the TV with IR, may work via bluetooth
    CHANNEL_UP  = "0x20"
    CHANNEL_DOWN = "0x21"
    PAUSE    = "0x24"
    FFWD     = "0x28"
    FORWARD  = "0x28"
    FFORWARD = "0x28"
    #HELP     = "0x29" # just brings up home screen and no action
    #UNPAIRED = "0x2A" # no visible action
    #POWERON  = "0x2B" # No action 
    #POWEROFF = "0x2C" # No action
    AUDDESC  = "0x2D"
    SUBT     = "0x2E" # Subtitle section via ?
    #TEXT     = "0x3C" # No visible action
    REWIND   = "0x3D"
    PLAY     = "0x3E"
    STOP     = "0x3F"
    RECORD   = "0x40"
    LOBATT   = "0x47" # displays popup for battery
    UP       = "0x58"
    DOWN     = "0x59"
    LEFT     = "0x5A"
    RIGHT    = "0x5B"
    SELECT   = "0x5C"
    RED      = "0x6D"
    GREEN    = "0x6E"
    YELLOW   = "0x6F"
    BLUE     = "0x70"
    #BOXOFF   = "0x7D" # no action
    SEARCH   = "0x7E" # Search Key
    #PARENT   = "0x7F" # No action
    SKY      = "0x80"
    HELP     = "0x81" # ? Key
    BACKUP   = "0x83"
    EXIT     = "0xCE"
    #TV      = "0x84" # No action
    #MORE    = "0xCB" # No Action
    HOME     = "0xCC" # Previously TVGuide
    APPS     = "0xF5" # ... Key
    #------ PRIVATE FOR LLAMA-USER ------
    BACK = "BACK"
    CROSS = "CROSS"
    MIC = "MIC"
    RGYB = "RGYB"
    PICK_UP = "PICK_UP"
    #------ PRIVATE FOR TPV-006 ---------
    TEST = "TEST"
    RST = "RST"
    FAC = "FAC"
    CSM = "CSM"
    PATTERN = "PATTERN"
    ANTENNA_CABLE = "ANTENNA_CABLE"
    PRE_CH = "PRE_CH"
    VOL_MAX = "VOL_MAX"
    CTC = "CTC"
    VOL_BUZZ = "VOL_BUZZ"
    MENU = "MENU"
    BI = "BI"
    CH_SCAN = "CH_SCAN"
    CCTT = "CCTT"
    PIC = "PIC"
    LOG_LED = "LOG_LED"
    AUDIO = "AUDIO"
    D2D3 = "D2D3"
    ARC = "ARC"
    CIP = "CIP"
    VIRGIN = "VIRGIN"
    CVBS = "CVBS"
    YPBPR_SCART = "YPBPR_SCART"
    HDMI = "HDMI"
    VGA = "VGA"
    REGIN = "REGIN"
    CLONE = "CLONE"
    RESERVE1 = "RESERVE1"
    DCR = "DCR"
    WIFI_SSID = "WIFI_SSID"
    BLK = "BLK"
    WP = "WP"
    LIGHT_SENSOR = "LIGHT_SENSOR"
    USB = "USB"
    RJ45 = "RJ45"
    RS232 = "RS232"
    RESERVE2 = "RESERVE2"
    #------------------------------------

