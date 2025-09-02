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
#*   ** @date        : 28/08/2025
#*   **
#*   ** @brief : AV Sync controller
#*   **
#* ******************************************************************************
import json
from os import path

import sys
MY_PATH = path.realpath(__file__)
MY_DIR = path.dirname(MY_PATH)
sys.path.append(path.join(MY_DIR,'../../'))
from framework.core.logModule import logModule
from framework.core.avSyncModules import SyncOne2

class AVSyncController():

    def __init__(self, log: logModule, config: dict):
        self._log = log
        self.controllerType = config.get('type')
        if self.controllerType.lower() == 'syncone2':
            port = config.get('port')
            input = config.get('audio_input','AUTO')
            extended_mode = config.get('extended_mode',False)
            speaker_distance = config.get('speaker_distance', None)
            if port is None:
                raise AttributeError('Cannot initialise SyncOne2 without port set in the rackConfig.')
            self.controller = SyncOne2(port,
                                       audio_input=input,
                                       extended_mode=extended_mode,
                                       speaker_dist=speaker_distance)
    @property
    def audio_trigger_level(self) -> int:
        """Audio Sensor Sensitivity Level.

        The higher the level the easier the sensor will trigger.
        """
        return self.controller.get_audio_trigger_level()

    @audio_trigger_level.setter
    def audio_trigger_level(self, audio_trigger_level: int):
        self.controller.set_audio_trigger_level(audio_trigger_level)

    @property
    def frame_rate(self) -> int:
        """Frame rate used in statistics calculations.
        """
        return self.controller.get_frame_rate()

    @frame_rate.setter
    def frame_rate(self, frame_rate: int):
        self.controller.set_frame_rate(frame_rate)

    @property
    def mask_length(self) -> int:
        """Mask time length in milliseconds.

        The time AVSync controller will wait after taking a measurement
        before re-arming to take the next measurement.
        """
        return self.controller.get_mask_len()

    @mask_length.setter
    def mask_length(self, mask_length: int):
        self.controller.set_mask_len(mask_length)

    @property
    def offset(self) -> int:
        """Manual offset in milliseconds.
        
        This manual offset can be used where equipment delays are known.
        """
        return self.controller.get_offset()

    @offset.setter
    def offset(self, offset: int):
        self.controller.set_offset(offset)

    @property
    def video_trigger_level(self) -> int:
        """Video Sensor Sensitivity Level.

        The higher the level the easier the sensor will trigger.
        """
        return self.controller.get_audio_trigger_level()

    @video_trigger_level.setter
    def video_trigger_level(self, video_trigger_level: int):
        self.controller.set_audio_trigger_level(video_trigger_level)

    def calibrate(self):
        """Calibrate the AVSync controller.
        """
        self._log.info('Calibrating AVSync controller.')
        self.controller.calibrate()

    def start_measurements(self):
        """Start recording measurements.

        The current measurement held in the buffer of the AVSync controller will
        be cleared before more measurements start being captured.
        """
        self._log.info('Starting measurement collection from AVSync controller.')
        # Clear the measurements before we start taking more measurments.
        self.controller.clear_results()
        self.controller.start_measuring()

    def stop_measurements(self):
        """Stop recording measurements
        """
        self._log.info('Stopping measurement collection from AVSync controller.')
        self.controller.stop_measuring()

    def clear_results(self):
        """Clear store results.
        """
        self._log.info('Clearing stored results from AVSync controller.')
        self.controller.clear_results()

    def get_results(self) -> list[dict]:
        """Return the results of the most recent measurements.

        Returns:
            results (list[dict]): list containing dictionary of each measurment recorded,
                        with the following keys:
                        {'milleseconds',
                        'frames',
                        'avg_milleseconds',
                        'avg_frames',
                        'span_milleseconds',
                        'span_frames'}
        """
        self._log.debug('Retrieving results from AVSync controller.')
        results = self.controller.get_results()
        self._log.debug(json.dumps(results))
        return results

### MAIN ###
if __name__ == '__main__':
    import time
    CONFIG = {
        'type': 'SyncONE2',
        'port': '/dev/ttyACM0',
        'extended_mode': False,
        'audio_input': 'EXTERNAL'
    }
    LOG = logModule('AVSync Logger')
    CONTROLLER = AVSyncController(LOG, CONFIG)

    # Test Audio Trigger Level
    CONTROLLER.audio_trigger_level = 2
    res = CONTROLLER.audio_trigger_level
    print(res)

    # Test Frame Rate
    CONTROLLER.frame_rate = 30
    print(CONTROLLER.frame_rate)

    # Test Mask Length
    CONTROLLER.mask_length = 300
    print(CONTROLLER.mask_length)

    # Test offset
    CONTROLLER.offset = -10
    print(CONTROLLER.offset)

    # Test Video Trigger Level
    CONTROLLER.video_trigger_level = 3
    print(CONTROLLER.video_trigger_level)

    # Test capturing measurements
    # CONTROLLER.start_measurements()
    # time.sleep(5)
    # CONTROLLER.stop_measurements()
    print(json.dumps(CONTROLLER.get_results()))

