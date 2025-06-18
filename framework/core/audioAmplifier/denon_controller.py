from denonavr import DenonAVR
from .base import AudioAmplifier

class DenonAVRController(AudioAmplifier):
    def __init__(self, host: str):
        self.receiver = DenonAVR(host)
        self._init = False

    async def _ensure_setup(self):
        if not self._init:
            await self.receiver.async_setup()
            self._init = True

    async def power_on(self):
        await self._ensure_setup()
        await self.receiver.async_power_on()

    async def power_off(self):
        await self._ensure_setup()
        await self.receiver.async_power_off()

    async def set_volume(self, volume: float):
        await self._ensure_setup()
        await self.receiver.async_set_volume(volume)

    async def mute(self, state: bool):
        await self._ensure_setup()
        await self.receiver.async_mute(state)

    async def set_input(self, input_name: str):
        await self._ensure_setup()
        await self.receiver.async_set_input_func(input_name)

    async def update_state(self):
        await self._ensure_setup()
        await self.receiver.async_update()

    def get_status(self):
        return {
            "power": self.receiver.power,
            "volume": self.receiver.volume,
            "input": self.receiver.input_func,
            "muted": self.receiver.muted,
        }
