import asyncio
import os
import sys

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")

from framework.core.denon_controller import DenonAVRController

if __name__ == "__main__":
    controller = DenonAVRController("10.242.30.236")
    controller.setup()

    # Power ON test
    try:
        controller.power_on()
        controller.update_state() 
        power = controller.get_power()
        assert power == "ON"
        print("PASSED: Power ON")
    except:
        print("FAILED: Power ON")

    # Volume test
    try:
        volume = -45
        controller.set_volume(volume)
        controller.update_state()
        updated_volume = controller.get_volume()
        assert updated_volume == volume
        print("PASSED: Volume change")
    except:
        print(f"FAILED: Volume change. Expected: {volume}, actual {updated_volume}")

    # Mute test
    try:
        controller.mute(True)
        controller.update_state()
        muted = controller.is_muted()
        assert muted is True
        print("PASSED: Mute")
    except: 
        print("FAILED: Mute")

    try:
        controller.mute(False)
        controller.update_state()
        muted = controller.is_muted()
        assert muted is False
        print("PASSED: Unmute")
    except: 
        print("FAILED: Unmute")

    # Input test
    try:
        print("Available inputs:", controller.get_available_inputs())
        input = "AUX2"
        controller.set_input(input)
        controller.update_state()
        updated_input = controller.get_input()
        assert updated_input == input
        print("PASSED: Input source set correctly.")
    except:
        print(f"FAILED: Input source not set correctly. Expected: {input}, actual: {updated_input}")

    # Sound Mode test
    try:
        print("Available sound modes:", controller.get_available_sound_modes())
        sound_mode = "MOVIE"
        controller.set_sound_mode(sound_mode)
        controller.update_state()
        updated_sound_mode = controller.get_sound_mode()
        assert updated_sound_mode == sound_mode
        print("PASSED: Sound mode set correctly")
    except:
        print(f"FAILED: Sound mode not set correctly. Expected: {sound_mode}, actual: {updated_sound_mode}")

    # Power OFF test
    try:
        controller.power_off()
        controller.update_state()
        power = controller.get_power()
        assert power.upper() == "OFF"
        print("PASSED: Power OFF")
    except:
        print("FAILED: Power OFF")
