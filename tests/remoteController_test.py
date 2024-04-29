#! /bin/python3
import os
import sys

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")

from framework.core.rcCodes import rcCode as rc
from framework.core.logModule import logModule
from framework.core.testControl import testController

class demoClass(testController):
    pass

if __name__ == "__main__":
    # Olimex ESP32-EVB as a RC transmitter. Telnet operated.
    demo = demoClass( testName = "remoteDemo", level=logModule.INFO )
    demo.log.info("Testing Power On")
    demo.powerControl.powerOn()
    demo.utils.wait(1)
    demo.log.info("Testing Power Off")
    demo.powerControl.powerOff()
    demo.log.info("Testing remote LLAMA RC6")
    demo.commonRemote.setKeyMap("llama_rc6")
    demo.commonRemote.sendKey( rc.POWER )
    demo.commonRemote.sendKey( rc.MUTE )
    demo.commonRemote.sendKey( rc.MUTE )
    demo.commonRemote.sendKey( rc.VOL_DOWN )
    demo.commonRemote.sendKey( rc.VOL_UP )
    demo.commonRemote.setKeyMap("llama_tpv")
    demo.log.info("Testing remote LLAMA TPV")
    demo.commonRemote.sendKey( rc.MUTE )
    demo.commonRemote.sendKey( rc.MUTE )
    demo.commonRemote.sendKey( rc.CHANNEL_DOWN )
    demo.commonRemote.sendKey( rc.CHANNEL_UP )

