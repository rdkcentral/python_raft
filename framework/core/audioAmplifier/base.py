from abc import ABC, abstractmethod

class AudioAmplifier(ABC):
    @abstractmethod
    async def power_on(self): pass

    @abstractmethod
    async def power_off(self): pass

    @abstractmethod
    async def set_volume(self, volume: float): pass

    @abstractmethod
    async def mute(self, state: bool): pass

    @abstractmethod
    async def set_input(self, input_name: str): pass

    @abstractmethod
    async def update_state(self): pass

    @abstractmethod
    def get_status(self) -> dict: pass
