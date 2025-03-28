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
#*   ** @file        : rcCodes.py
#*   ** @date        : 17/01/2019
#*   **
#*   ** @brief : Remote Control Code Wrapper class
#*   **
#* ******************************************************************************

from enum import Enum

class rcCode(Enum):
    THREE_D = "3d"
    A = "A"
    ANTENNA = "ANTENNA"
    APPS = "APPS"
    ARC = "ARC"
    ARROW_UP = "ARROW_UP"
    ARROW_DOWN = "ARROW_DOWN"
    ARROW_LEFT = "ARROW_LEFT"
    ARROW_RIGHT = "ARROW_RIGHT"
    AUDIO = "AUDIO"
    AUD_DESC = "AUD_DESC"
    AUX = "AUX"
    B = "B"
    BI = "BI"
    BACK = "BACK"
    BAND = "BAND"
    BLK = "BLK"
    BLUE = "BLUE"
    BLUETOOTH = "BLUETOOTH"
    BLURAY = "BLURAY"
    C = "C"
    CANCEL = "CANCEL"
    CBL_SAT = "CBL_SAT"
    CCTT = "CCTT"
    CH_SCAN = "CH_SCAN"
    CHANNEL_UP = "CHANNEL_UP"
    CHANNEL_DOWN = "CHANNEL_DOWN"
    CI_PLUS = "CI+"
    CLONE = "CLONE"
    CROSS = "CROSS"
    CSM = "CSM"
    CTC = "CTC"
    CVBS = "CVBS"
    D = "D"
    D2D3 = "D2D3"
    DCR = "DCR"
    DISC_MENU = "DISC_MENU"
    DISNEY = "DISNEY"
    DISPLAY = "DISPLAY"
    DVD = "DVD"
    ECO = "ECO"
    ELLIPSIS = "ELLIPSIS"
    EJECT = "EJECT"
    ENHANCER = "ENHANCER"
    EXIT = "EXIT"
    FAC = "FAC"
    FFORWARD = "FFORWARD"
    GREEN = "GREEN"
    GUIDE = "GUIDE"
    HDMI = "HDMI"
    HEART = "HEART"
    HELP = "HELP"
    HOME = "HOME"
    INFO = "INFO"
    INTERNET = "INTERNET"
    INTERNET_RADIO = "INTERNET_RADIO"
    LAST = "LAST"
    LIGHT_SENSOR = "LIGHT_SENSOR"
    LOBATT = "LOBATT"
    LOG_LED = "LOG_LED"
    MEDIA_PLAYER = "MEDIA_PLAYER"
    MENU = "MENU"
    MIC = "MIC"
    MIRACAST = "MIRACAST"
    MODE = "MODE"
    MORE = "MORE"
    MOVIE = "MOVIE"
    MUSIC = "MUSIC"
    MUTE = "MUTE"
    NETFLIX = "NETFLIX"
    NUM_0 = "NUM_0"
    NUM_1 = "NUM_1"
    NUM_2 = "NUM_2"
    NUM_3 = "NUM_3"
    NUM_4 = "NUM_4"
    NUM_5 = "NUM_5"
    NUM_6 = "NUM_6"
    NUM_7 = "NUM_7"
    NUM_8 = "NUM_8"
    NUM_9 = "NUM_9"
    OPTIONS = "OPTIONS"
    PAGE_DOWN = "PAGE_DOWN"
    PAGE_UP = "PAGE_UP"
    PARENT = "PARENT"
    PARTY = "PARTY"
    PASSTHROUGH = "PASSTHROUGH"
    PATTERN = "PATTERN"
    PAUSE = "PAUSE"
    PEACOCK = "PEACOCK"
    PHONO = "PHONO"
    PIC = "PIC"
    PICK_UP = "PICK_UP"
    PLAY = "PLAY"
    POPUP_MENU = "POPUP_MENU"
    POWER = "POWER"
    PRESET_LEFT = "PRESET_LEFT"
    PRESET_RIGHT = "PRESET_RIGHT"
    PREV_CH = "PREV_CH"
    PROG_LEFT = "PROG_LEFT"
    PROG_RIGHT = "PROG_RIGHT"
    PRIME_VIDEO = "PRIME_VIDEO"
    QUESTION = "QUESTION"
    RECORD = "RECORD"
    RED = "RED"
    REGIN = "REGIN"
    REPLAY = "REPLAY"
    RESERVE1 = "RESERVE1"
    RESERVE2 = "RESERVE2"
    REWIND = "REWIND"
    RGYB = "RGYB"
    RJ45 = "RJ45"
    RS232 = "RS232"
    RESET = "RESET"
    SEARCH = "SEARCH"
    SEARCH_BACK = "SEARCH_BACK"
    SEARCH_FWD = "SEARCH_FWD"
    SELECT = "SELECT"
    SETUP = "SETUP"
    SKY = "SKY"
    SOURCE = "SOURCE"
    STANDBY = "STANDBY"
    STATUS = "STATUS"
    STOP = "STOP"
    STRAIGHT = "STRAIGHT"
    SUBTITLE = "SUBTITLE"
    SURROUND = "SURROUND"
    SUR_DECODE = "SUR_DECODE"
    TEST = "TEST"
    TEXT = "TEXT"
    TOOLS = "TOOLS"
    TUNER = "TUNER"
    USB = "USB"
    VGA = "VGA"
    VIRGIN = "VIRGIN"
    VOL_DOWN = "VOL_DOWN"
    VOL_UP = "VOL_UP"
    WIFI_SSID = "WIFI_SSID"
    WP = "WP"
    XFINITY = "XFINITY"
    XUMO = "XUMO"
    YELLOW = "YELLOW"
    YPBPR_SCART = "YPBPR_SCART"
