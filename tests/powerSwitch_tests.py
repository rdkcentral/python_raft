#! /bin/python3
import os
import sys

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")

from framework.core.powerControl import powerControlClass
from framework.core.rackController import rackController
from framework.core.logModule import logModule
from framework.core.utilities import utilities
from framework.core.decodeParams import decodeParams
from framework.core.deviceManager import deviceManager

if __name__ == "__main__":
    # Read configuration file, and run power switch test based on that
    log = logModule("powerSwitchTest")
    log.setLevel( log.INFO )

    utils = utilities( log )

    config = decodeParams(log)
    rackControl = rackController( config.rackConfig )

    # Just choose rack 0, slot 0
    rack = rackControl.getRackByIndex( 0 )
    if config.args.slotNumber != None:
        slot = rack.getSlot(config.args.slotNumber )
    else:
        slot = rack.getSlot(1)

    devices = deviceManager( slot.config.get("devices"), log, "./logs" )
    dut = devices.getDevice("dut")
    power = dut.powerControl

    log.info("Testing Power on")
    power.powerOn()

    utils.wait(5)

    log.info("Testing Power ON Reboot")
    power.reboot()

    utils.wait(5)

    log.info("Testing Power Off")
    power.powerOff()

    utils.wait(5)

    log.info("Testing Power Off Reboot")
    power.reboot()

    utils.wait(5)

    log.info("Testing Power Off")
    power.powerOff()

    log.info("Test complete")

