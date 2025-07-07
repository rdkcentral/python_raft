#!/usr/bin/env python3
#** *****************************************************************************
# *
# * If not stated otherwise in this file or this component's LICENSE file the
# * following copyright and licenses apply:
# *
# * Copyright 2023 RDK Management
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *
# http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : core
#*   ** @date        : 01/07/2025
#*   **
#*   ** @brief : audio amplifier controller
#*   **
#* ******************************************************************************

import asyncio
from denonavr import DenonAVR

from framework.core.logModule import logModule
from framework.core.audioAmplifier.base import AudioAmplifier

class DenonAVRController(AudioAmplifier):
    
    def __init__(self, host: str):
        self.receiver = DenonAVR(host)
        self._log = logModule("DenonAVRController")

    def setup(self):
        self._log.info("Setting up receiver")
        asyncio.run(self.receiver.async_setup())

    def power_on(self):
        self._log.info("Powering ON receiver")
        asyncio.run(self.receiver.async_power_on())

    def power_off(self):
        self._log.info("Powering OFF receiver")
        asyncio.run(self.receiver.async_power_off())

    def set_volume(self, volume: float):
        self._log.info("Setting receiver volume")
        asyncio.run(self.receiver.async_set_volume(volume))

    def mute(self, state: bool):
        self._log.info("Muting receiver")
        asyncio.run(self.receiver.async_mute(state))

    def get_available_inputs(self) -> list[str]:
        self._log.info("Getting receiver available inputs")
        self.update_state()
        return self.receiver.input_func_list

    def get_available_sound_modes(self) -> list[str]:
        self._log.info("Getting receiver available sound modes")
        self.update_state()
        return self.receiver.sound_mode_list

    def set_input(self, input_name: str):
        self._log.info("Setting receiver input")
        available = self.get_available_inputs()
        if input_name not in available:
            raise ValueError(f"Invalid input: {input_name}. Available inputs: {available}")
        asyncio.run(self.receiver.async_set_input_func(input_name))

    def set_sound_mode(self, mode: str):
        self._log.info("Setting receiver sound mode")
        available = self.get_available_sound_modes()
        if mode not in available:
            raise ValueError(f"Invalid sound mode: {mode}. Available modes: {available}")
        asyncio.run(self.receiver.async_set_sound_mode(mode))

    def update_state(self):
        self._log.info("Updating receiver state")
        asyncio.run(self.receiver.async_update())

    def get_power(self) -> str:
        self._log.info("Getting receiver power")
        return self.receiver.power

    def get_volume(self) -> float:
        self._log.info("Getting receiver volume")
        return self.receiver.volume

    def is_muted(self) -> bool:
        self._log.info("Getting receiver mute state")
        return self.receiver.muted
    
    def get_input(self) -> str:
        self._log.info("Getting receiver input")
        return self.receiver.input_func
    
    def get_sound_mode(self) -> str:
        self._log.info("Getting receiver sound mode")
        return self.receiver.sound_mode

    def get_status(self):
        self._log.info("Getting receiver status")
        return {
            "power": self.get_power(),
            "volume": self.get_volume(),
            "muted": self.is_muted(),
            "input": self.get_input(),
            "sound_mode": self.get_sound_mode(),
        }
