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

from framework.core.logModule import logModule
from framework.core.audioAmplifier.denon_controller import DenonAVRController

class audioAmplifierController():
    
    def __init__(self, log:logModule, config:dict):
        self._log = log
        self.controllerType = config.get("type")
        self.host = config.get("host")
        
        if self.controllerType == "denon":
            self.audioAmplifier = DenonAVRController(self.host)

    def power_on(self):
        self._log.info("Powering ON audio amplifier")
        self.audioAmplifier.power_on()

    def power_off(self):
        self._log.info("Powering OFF audio amplifier")
        self.audioAmplifier.power_off()

    def set_volume(self, volume: float):
        self._log.info("Setting audio amplifier volume")
        self.audioAmplifier.set_volume(volume)

    def mute(self, state: bool):
        self._log.info("Muting audio amplifier")
        self.audioAmplifier.mute(state)

    def list_inputs(self) -> list[str]:
        self._log.info("Listing the audio amplifier available inputs")
        return self.audioAmplifier.list_inputs()

    def list_sound_modes(self) -> list[str]:
        self._log.info("Listing the audio amplifier available sound modes")
        return self.audioAmplifier.list_sound_modes()

    def set_input(self, input_name: str):
        self._log.info("Setting audio amplifier input")
        self.audioAmplifier.set_input(input_name)

    def set_sound_mode(self, mode: str):
        self.audioAmplifier.set_sound_mode(mode)

    def get_power(self) -> str:
        self._log.info("Getting audio amplifier power")
        return self.audioAmplifier.get_power()

    def get_volume(self) -> float:
        self._log.info("Getting audio amplifier volume")
        return self.audioAmplifier.get_volume()

    def is_muted(self) -> bool:
        self._log.info("Getting audio amplifier mute state")
        return self.audioAmplifier.is_muted()
    
    def get_input(self) -> str:
        self._log.info("Getting audio amplifier input")
        return self.audioAmplifier.get_input()
    
    def get_sound_mode(self) -> str:
        self._log.info("Getting audio amplifier sound mode")
        return self.audioAmplifier.get_sound_mode()

    def get_status(self):
        self._log.info("Getting audio amplifier status")
        return self.audioAmplifier.get_status()
