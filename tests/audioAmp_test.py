import asyncio

import os
import sys

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")

from framework.core.audioAmplifier.denon_controller import DenonAVRController

async def main():
    controller = await DenonAVRController.create("10.242.30.236")

    # Power ON test
    try:
        await controller.power_on()
        await controller.update_state() 
        power = await controller.get_power()
        assert power == "ON"
        print("PASSED: Power ON")
    except:
        print("FAILED: Power ON")

    # Volume test
    try:
        volume = -40
        await controller.set_volume(volume)
        await controller.update_state()
        updated_volume = await controller.get_volume()
        assert updated_volume == volume
        print("PASSED: Volume change")
    except:
        print(f"FAILED: Volume change. Expected: {volume}, actual {updated_volume}")

    # Mute test
    try:
        await controller.mute(True)
        await controller.update_state()
        muted = await controller.is_muted()
        assert muted is True
        print("PASSED: Mute")
    except: 
        print("FAILED: Mute")

    try:
        await controller.mute(False)
        await controller.update_state()
        muted = await controller.is_muted()
        assert muted is False
        print("PASSED: Unmute")
    except: 
        print("FAILED: Unmute")

    # Input test
    try:
        print("Available inputs:", await controller.get_available_inputs())
        input = "Game"
        await controller.set_input(input)
        await controller.update_state()
        updated_input = await controller.get_input()
        assert updated_input == input
        print("PASSED: Input source set correctly.")
    except:
        print(f"FAILED: Input source not set correctly. Expected: {input}, actual: {updated_input}")

    # Sound Mode test
    try:
        print("Available sound modes:", await controller.get_available_sound_modes())
        sound_mode = "MUSIC"
        await controller.set_sound_mode(sound_mode)
        await controller.update_state()
        updated_sound_mode = await controller.get_sound_mode()
        assert updated_sound_mode == sound_mode
        print("PASSED: Sound mode set correctly")
    except:
        print(f"FAILED: Sound mode not set correctly. Expected: {sound_mode}, actual: {updated_sound_mode}")

    # Power OFF test
    try:
        await controller.power_off()
        await controller.update_state()
        power = await controller.get_power()
        assert power.upper() == "OFF"
        print("PASSED: Power OFF")
    except:
        print("FAILED: Power OFF")

asyncio.run(main())