from abc import ABC, abstractmethod

class AudioAmplifier(ABC):
    """
    Abstract base class defining the interface for an audio amplifier controller.

    Implementations must provide methods for controlling power, volume,
    input source, mute state, sound mode, and retrieving status information.
    """

    @abstractmethod
    def power_on(self):
        """Power on the amplifier."""
        pass

    @abstractmethod
    def power_off(self):
        """Power off the amplifier."""
        pass

    @abstractmethod
    def set_volume(self, volume: float):
        """
        Set the amplifier volume.

        :param volume: Desired volume level.
        """
        pass

    @abstractmethod
    def mute(self, state: bool):
        """
        Mute or unmute the amplifier.

        :param state: True to mute, False to unmute.
        """
        pass

    @abstractmethod
    def list_inputs(self) -> list[str]:
        """
        Get the list of available input sources supported by the amplifier.
        """
        pass

    @abstractmethod
    def list_sound_modes(self) -> list[str]:
        """
        Get the list of available sound modes supported by the amplifier.
        """
        pass

    @abstractmethod
    def set_input(self, input_name: str):
        """
        Set the input source of the amplifier.

        :param input_name: Name of the input source (e.g., "TV", "CD").
        """
        pass

    @abstractmethod
    def set_sound_mode(self, input_name: str):
        """
        Set the sound mode of the amplifier.

        :param input_name: Name of the sound mode (e.g., "TV", "CD").
        """
        pass

    @abstractmethod
    def update_state(self):
        """
        Refresh the internal state from the amplifier.

        Typically required before retrieving status properties.
        """
        pass

    @abstractmethod
    def get_power(self) -> str:
        """Get the current power state (e.g., "ON", "OFF")."""
        pass

    @abstractmethod
    def get_volume(self) -> float:
        """Get the current volume level."""
        pass

    @abstractmethod
    def get_input(self) -> str:
        """Get the currently selected input source."""
        pass

    @abstractmethod
    def is_muted(self) -> bool:
        """Check whether the amplifier is muted."""
        pass

    @abstractmethod
    def get_status(self) -> dict:
        """
        Get a dictionary of key status information (power, volume, input, mute).

        :return: Dictionary of current amplifier state.
        """
        pass
