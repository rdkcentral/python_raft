from denonavr import DenonAVR
from .base import AudioAmplifier

class DenonAVRController(AudioAmplifier):
    def __init__(self, receiver: DenonAVR):
        self.receiver = receiver

    @classmethod
    async def create(cls, host: str):
        receiver = DenonAVR(host)
        await receiver.async_setup()
        return cls(receiver)

    async def power_on(self):
        await self.receiver.async_power_on()

    async def power_off(self):
        await self.receiver.async_power_off()

    async def set_volume(self, volume: float):
        await self.receiver.async_set_volume(volume)

    async def mute(self, state: bool):
        await self.receiver.async_mute(state)

    async def get_available_inputs(self) -> list[str]:
        await self.update_state()
        return self.receiver.input_func_list

    async def get_available_sound_modes(self) -> list[str]:
        await self.update_state()
        return self.receiver.sound_mode_list

    async def set_input(self, input_name: str):
        available = await self.get_available_inputs()
        if input_name not in available:
            raise ValueError(f"Invalid input: {input_name}. Available inputs: {available}")
        await self.receiver.async_set_input_func(input_name)

    async def set_sound_mode(self, mode: str):
        available = await self.get_available_sound_modes()
        if mode not in available:
            raise ValueError(f"Invalid sound mode: {mode}. Available modes: {available}")
        await self.receiver.async_set_sound_mode(mode)

    async def update_state(self):
        await self.receiver.async_update()

    async def get_power(self) -> str:
        return self.receiver.power

    async def get_volume(self) -> float:
        return self.receiver.volume

    async def is_muted(self) -> bool:
        return self.receiver.muted
    
    async def get_input(self) -> str:
        return self.receiver.input_func
    
    async def get_sound_mode(self) -> str:
        return self.receiver.sound_mode


    async def get_status(self):
        return {
            "power": self.get_power(),
            "volume": self.get_volume(),
            "muted": self.is_muted(),
            "input": self.get_input(),
            "sound_mode": self.get_sound_mode(),
        }
