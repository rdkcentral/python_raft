import asyncio
from denonavr import DenonAVR
from .base import AudioAmplifier

class DenonAVRController(AudioAmplifier):
    
    def __init__(self, host: str):
        self.receiver = DenonAVR(host)

    def setup(self):
        asyncio.run(self.receiver.async_setup())

    def power_on(self):
        asyncio.run(self.receiver.async_power_on())

    def power_off(self):
        asyncio.run(self.receiver.async_power_off())

    def set_volume(self, volume: float):
        asyncio.run(self.receiver.async_set_volume(volume))

    def mute(self, state: bool):
        asyncio.run(self.receiver.async_mute(state))

    def get_available_inputs(self) -> list[str]:
        self.update_state()
        return self.receiver.input_func_list

    def get_available_sound_modes(self) -> list[str]:
        self.update_state()
        return self.receiver.sound_mode_list

    def set_input(self, input_name: str):
        available = self.get_available_inputs()
        if input_name not in available:
            raise ValueError(f"Invalid input: {input_name}. Available inputs: {available}")
        asyncio.run(self.receiver.async_set_input_func(input_name))

    def set_sound_mode(self, mode: str):
        available = self.get_available_sound_modes()
        if mode not in available:
            raise ValueError(f"Invalid sound mode: {mode}. Available modes: {available}")
        asyncio.run(self.receiver.async_set_sound_mode(mode))

    def update_state(self):
        asyncio.run(self.receiver.async_update())

    def get_power(self) -> str:
        return self.receiver.power

    def get_volume(self) -> float:
        return self.receiver.volume

    def is_muted(self) -> bool:
        return self.receiver.muted
    
    def get_input(self) -> str:
        return self.receiver.input_func
    
    def get_sound_mode(self) -> str:
        return self.receiver.sound_mode

    def get_status(self):
        return {
            "power": self.get_power(),
            "volume": self.get_volume(),
            "muted": self.is_muted(),
            "input": self.get_input(),
            "sound_mode": self.get_sound_mode(),
        }
