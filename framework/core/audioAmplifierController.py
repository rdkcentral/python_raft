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

class audioAmplifierController(AudioAmplifier):
    
    def __init__(self, config:dict):
        self._log = logModule("DenonAVRController")
        self.controllerType = config.get("type")
        self.host = config.get("host")
        
        self.audioAmplifier = DenonAVR(self.host)

    def setup(self):
        self._log.info("Setting up audio amplifier")
        asyncio.run(self.audioAmplifier.async_setup())

    def power_on(self):
        self._log.info("Powering ON audio amplifier")
        asyncio.run(self.audioAmplifier.async_power_on())

    def power_off(self):
        self._log.info("Powering OFF audio amplifier")
        asyncio.run(self.audioAmplifier.async_power_off())

    def set_volume(self, volume: float):
        self._log.info("Setting audio amplifier volume")
        asyncio.run(self.audioAmplifier.async_set_volume(volume))

    def mute(self, state: bool):
        self._log.info("Muting audio amplifier")
        asyncio.run(self.audioAmplifier.async_mute(state))

    def get_available_inputs(self) -> list[str]:
        self._log.info("Getting audio amplifier available inputs")
        self.update_state()
        return self.audioAmplifier.input_func_list

    def get_available_sound_modes(self) -> list[str]:
        self._log.info("Getting audio amplifier available sound modes")
        self.update_state()
        return self.audioAmplifier.sound_mode_list

    def set_input(self, input_name: str):
        self._log.info("Setting audio amplifier input")
        available = self.get_available_inputs()
        if input_name not in available:
            raise ValueError(f"Invalid input: {input_name}. Available inputs: {available}")
        asyncio.run(self.audioAmplifier.async_set_input_func(input_name))

    def set_sound_mode(self, mode: str):
        self._log.info("Setting audio amplifier sound mode")
        available = self.get_available_sound_modes()
        if mode not in available:
            raise ValueError(f"Invalid sound mode: {mode}. Available modes: {available}")
        asyncio.run(self.audioAmplifier.async_set_sound_mode(mode))

    def update_state(self):
        self._log.info("Updating audio amplifier state")
        asyncio.run(self.audioAmplifier.async_update())

    def get_power(self) -> str:
        self._log.info("Getting audio amplifier power")
        return self.audioAmplifier.power

    def get_volume(self) -> float:
        self._log.info("Getting audio amplifier volume")
        return self.audioAmplifier.volume

    def is_muted(self) -> bool:
        self._log.info("Getting audio amplifier mute state")
        return self.audioAmplifier.muted
    
    def get_input(self) -> str:
        self._log.info("Getting audio amplifier input")
        return self.audioAmplifier.input_func
    
    def get_sound_mode(self) -> str:
        self._log.info("Getting audio amplifier sound mode")
        return self.audioAmplifier.sound_mode

    def get_status(self):
        self._log.info("Getting audio amplifier status")
        return {
            "power": self.get_power(),
            "volume": self.get_volume(),
            "muted": self.is_muted(),
            "input": self.get_input(),
            "sound_mode": self.get_sound_mode(),
        }
