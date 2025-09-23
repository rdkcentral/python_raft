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
#*   ** @brief : AV Sync module interface
#*   **
#* ******************************************************************************

import abc


class AVSyncInterface(metaclass=abc.ABCMeta):

    def __init__(self):
        self._measuring = False

    @abc.abstractmethod
    def get_audio_trigger_level(self) -> int:
        """Return the AVSync devices audio sensitivity level.

        Returns:
            level (int): Audio sensitivity level.
        """
        pass

    @abc.abstractmethod
    def set_audio_trigger_level(self, trigger_level:int):
        """Set the AVSync devices audio sensitivity level.

        Args:
            trigger_level (int): Arbitrary sensitivity level.
        """
        pass

    @abc.abstractmethod
    def get_frame_rate(self) -> int:
        """Return the current frame rate set in the AVSync device.

        Returns:
            frame_rate (int): The current frame rate set in the current device.
        """
        pass

    @abc.abstractmethod
    def set_frame_rate(self, frame_rate:int):
        """Set the frame rate in the AVSync device.

        The AVSync device will use the framerate set to calculate frame based stats.

        Args:
            frame_rate (int): Frame rate to set.
        """
        pass

    @abc.abstractmethod
    def get_mask_len(self) -> int:
        """Return the current length of mask time set in the AVSync device,
        in milliseconds.

        The mask time is the length of time the AVSync device will wait between measurements.

        Returns:
            mask_length(int): The length of time between measurements in milliseconds.
        """
        pass

    @abc.abstractmethod
    def set_mask_len(self, mask_length: int):
        """Set the length of mask time in the AVSync device.

        The mask time is the length of time the AVSync device will wait between measurements.

        Args:
            mask_length (int): The length of time between measurements in milliseconds.
        """
        pass

    @abc.abstractmethod
    def get_offset(self) -> int:
        """Manual offset in milliseconds set inside the AVSync device.

        This manual offset can be used where equipment delays are known.

        Returns:
            offset (int): Manual offset in milliseconds.
        """
        pass

    @abc.abstractmethod
    def set_offset(self, offset: int):
        """Set the manual offset in milliseconds inside the AVSync device.

        This manual offset can be used where equipment delays are known.

        Args:
            offset (int): Manual offset in milliseconds
        """
        pass

    @abc.abstractmethod
    def get_video_trigger_level(self) -> int:
        """Return the AVSync devices video sensitivity level.

        Returns:
            level (int): Video sensitivity level.
        """
        pass

    @abc.abstractmethod
    def set_video_trigger_level(self, trigger_level:int):
        """Set the AVSync devices video sensitivity level.

        Args:
            trigger_level (int): Arbitrary sensitivity level.
        """
        pass

    @abc.abstractmethod
    def get_results(self) -> list[dict]:
        """Return the results of measurement taken, stored in the AVSync device.

        Returns:
            results (list[dict]): list containing dictionary of each measurement recorded,
                        with the following keys:
                        {'milliseconds',
                        'frames',
                        'avg_milliseconds',
                        'avg_frames',
                        'span_milliseconds',
                        'span_frames'}
        """
        pass

    @abc.abstractmethod
    def clear_results(self):
        """Clear the current results stored in the AVSync device.
        """
        pass

    @abc.abstractmethod
    def start_measuring(self):
        """Start the AVSync device taking measurements.

        This is blocking. No other methods can be called while measurements are being
        taken, except stop_measuring.
        """
        self._measuring = True

    @abc.abstractmethod
    def stop_measuring(self):
        """Stop the AVSync device taking measurements.
        """
        self._measuring = False

    @abc.abstractmethod
    def calibrate(self):
        """Run calibration on the AVSync device.
        """
        pass