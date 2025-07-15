
import os
import sys
import json

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")

from framework.core.logModule import logModule
from framework.core.audioAmplifierController import audioAmplifierController

if __name__ == "__main__":

    LOG = logModule("audio amplifier test", logModule.DEBUG)
    CONFIGS = [
        {
            'type': 'denon',
            'host': '10.242.30.236'
        }]
    
    for config in CONFIGS:
        
        LOG.setFilename(os.path.abspath('./logs/'),'audioAmplifier-%sTest.log' % config.get('type'))
        LOG.stepStart('Testing with %s' % json.dumps(config))
        
        controller = audioAmplifierController(LOG, config)

        # Power ON test
        try:
            controller.power_on()
            power = controller.get_power()
            assert power == "ON"
            print("PASSED: Power ON")
        except:
            print("FAILED: Power ON")

        # Volume test
        try:
            volume = -51
            controller.set_volume(volume)
            updated_volume = controller.get_volume()
            assert updated_volume == volume
            print("PASSED: Volume change")
        except:
            print(f"FAILED: Volume change. Expected: {volume}, actual {updated_volume}")

        # Mute test
        try:
            controller.mute(True)
            muted = controller.is_muted()
            assert muted is True
            print("PASSED: Mute")
        except: 
            print("FAILED: Mute")

        try:
            controller.mute(False)
            muted = controller.is_muted()
            assert muted is False
            print("PASSED: Unmute")
        except: 
            print("FAILED: Unmute")

        # Input test
        try:
            print("Available inputs:", controller.list_inputs())
            input = "AUX2"
            controller.set_input(input)
            updated_input = controller.get_input()
            assert updated_input == input
            print("PASSED: Input source set correctly.")
        except:
            print(f"FAILED: Input source not set correctly. Expected: {input}, actual: {updated_input}")

        # Sound Mode test
        try:
            print("Available sound modes:", controller.list_sound_modes())
            sound_mode = "MOVIE"
            controller.set_sound_mode(sound_mode)
            updated_sound_mode = controller.get_sound_mode()
            assert updated_sound_mode == sound_mode
            print("PASSED: Sound mode set correctly")
        except:
            print(f"FAILED: Sound mode not set correctly. Expected: {sound_mode}, actual: {updated_sound_mode}")

        # Power OFF test
        try:
            controller.power_off()
            power = controller.get_power()
            assert power.upper() == "OFF"
            print("PASSED: Power OFF")
        except:
            print("FAILED: Power OFF")
