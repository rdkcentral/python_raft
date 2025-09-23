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
#*   ** @brief : AV Sync module for Sync-One2 device
#*   **
#* ******************************************************************************

import serial


from .avSyncInterface import AVSyncInterface

class SyncOne2(AVSyncInterface):

    def __init__(self, port:str,
                 audio_input:str='AUTO',
                 extended_mode:bool=False,
                 speaker_dist: float|None=None):
        self._serial = serial.Serial(port,
                                     baudrate=115200,
                                     bytesize=8,
                                     timeout=5)
        super().__init__()
        self._audio_input = audio_input.upper()
        self._extended_mode = extended_mode
        self._speaker_dist = speaker_dist
        self._start_connection()
        self._set_custom_settings()
        

    def _start_connection(self):
        """Connect to the SyncOne2 device and
         set it in API mode.

        Raises:
            ConnectionError: When the SyncOne2 device does not respond as expected.
        """
        self._serial.write(b'api\n')
        self._serial.flush()
        connection_res = self._serial.read_until(b'OK')
        if connection_res:
            if 'OK' in connection_res.decode():
                return
        # If the return above isn't hit, the connection didn't work.
        raise ConnectionError(f'Could not start serial connection with SyncOne2 on port')

    def _set_custom_settings(self):
        """Configure the SyncOne2 device with custom settings.

        These custom settings are passed from the rack config.
        They include:
            - audio_input
            - extended_mode
            - speaker_distance
        """
        audio_input_settings = self.get_audio_input()
        if self._audio_input != audio_input_settings:
            self.set_audio_input(self._audio_input)
        extended_mode = self.get_extended_mode()
        if extended_mode != self._extended_mode:
            self.set_extended_mode(self._extended_mode)
        if self._speaker_dist is not None:
            speaker_dist = self.get_speaker_dist()
            if speaker_dist != self._speaker_dist:
                self.set_speaker_dist(self._speaker_dist)

    def _send_cmd_wait_for_resp(self,command: str, override_measuring_block: bool=False) -> str:
        """Send a message to the SyncOne2 device.

        Args:
            command (str): Command to be sent to the SyncOne2 device.
            override_measuring_block (bool, optional): Allows commands to be while the device is taking measurements.
                                                       Overide active when set to True. Defaults to False. 

        Raises:
            RuntimeError: If measurements are being taken when command is sent, without the overide set to True.

        Returns:
            resp (str): Decoded response from the SyncOne2 device.
        """
        if self._measuring is True and override_measuring_block is False:
            raise RuntimeError('Cannot send command to SyncOne2 while it is measuring.')
        if '\n' not in command:
            command += '\n'
        self._serial.write(command.encode())
        self._serial.flush()
        resp = self._serial.read_until().decode().strip()
        return resp

    def _process_readings(self, readings_list: list[bytes]) -> list[dict]:
        """Process list of bytes returned from SyncOne2 devices stats, into 
        list of dictionaries with defined fields.

        The stats api from the SyncOne2 device returns a list of bytes objects.
        These are decoded to a CSV which is process into a list of dictionaries,
        with the fields defined.

        Args:
            readings_list (list[bytes]): List of bytes objects from SyncOne2's stats api.

        Returns:
            processed_readings(list[dict]): List of dictionaries with defined fields:
                                            {'milliseconds',
                                            'frames',
                                            'avg_milliseconds',
                                            'avg_frames',
                                            'span_milliseconds',
                                            'span_frames'}
        """
        fields = ('milliseconds',
                  'frames',
                  'avg_milliseconds',
                  'avg_frames',
                  'span_milliseconds',
                  'span_frames')
        processed_readings = []
        for line in readings_list:
            line_fields = line.split(',')
            readings_dict = {}
            for index, field in enumerate(fields):
                readings_dict[field] = line_fields[index]
            processed_readings.append(readings_dict)
        return processed_readings

    def get_audio_input(self) -> str:
        """Return the current audio input set to be used on the SyncOne2 device.

        Raises:
            ConnectionError: When the response from the SyncOne2 device is not as expected.

        Returns:
            response(str): Fixed string response from the SyncOne2 device.
                           Options:
                            - AUTO
                            - EXTERNAL
                            - INTERNAL
        """
        response = self._send_cmd_wait_for_resp('AUDIO IN\n')
        if response not in ('AUTO', 'EXTERNAL', 'INTERNAL'):
            raise ConnectionError('Did not receive expected response from SyncOne2')
        return response

    def set_audio_input(self,input:str):
        """Set the audio input for the SyncOne2 device to use.

        Args:
            input (str): Fixed string.
                         Options:
                            - AUTO
                            - EXTERNAL
                            - INTERNAL

        Raises:
            ValueError: When the string argument given isn't one of the listed options.
            ConnectionError: When the response from the SyncOne2 device is not as expected.
        """
        if input.upper() not in ('AUTO', 'EXTERNAL', 'INTERNAL'):
            raise ValueError('SyncOne2 only accepts AUTO, EXTERNAL or INTERNAL for audio input.')
        response = self._send_cmd_wait_for_resp(f'SET AUDIO IN {input.upper()}\n')
        if 'OK' not in response:
            raise ConnectionError('Did not receive expected response from SyncOne2')

    def get_audio_trigger_level(self) -> int:
        response = self._send_cmd_wait_for_resp('AUDIO TRIGGER LEVEL\n')
        if response not in ('0', '1', '2', '3', '4'):
            raise ConnectionError('Did not receive expected response from SyncOne2')
        return int(response)

    def set_audio_trigger_level(self, trigger_level:int):
        if trigger_level > 4 or trigger_level < 0:
            raise ValueError('The trigger level must be between 0 and 4 for the SyncOne2 device.')
        response = self._send_cmd_wait_for_resp(f'SET AUDIO TRIGGER LEVEL {trigger_level}\n')
        if 'OK' not in response:
            raise ConnectionError('Did not receive expected response from SyncOne2')

    def get_extended_mode(self) -> bool:
        """Return the on/off state of the SyncOne2 devices extended mode.

        Raises:
            ConnectionError: When the response from the SyncOne2 device is not as expected.

        Returns:
            state (bool): On/Off state of extended mode. True when extended mode is on.
        """
        state = False
        response = self._send_cmd_wait_for_resp('EXTENDED MODE\n')
        if response not in ('on', 'off'):
            raise ConnectionError('Did not receive expected response from SyncOne2')
        if response.lower() == 'on':
            state = True
        return state

    def set_extended_mode(self, state:bool):
        """Set the on/off state of the SyncOne2 devices extended mode.

        Args:
            state (bool): True to set extended mode on. False to set extended more off.

        Raises:
            ConnectionError: When the response from the SyncOne2 device is not as expected.
        """
        if state is True:
            ext_state = 'ON'
        else:
            ext_state = 'OFF'
        response = self._send_cmd_wait_for_resp(f'SET EXTENDED MODE {ext_state}\n')
        if 'OK' not in response:
            raise ConnectionError('Did not receive expected response from SyncOne2')

    def get_frame_rate(self) -> int:
        response = self._send_cmd_wait_for_resp('FRAME RATE\n')
        if response.isnumeric():
            return int(response)
        raise ConnectionError('Did not receive expected response from SyncOne2')

    def set_frame_rate(self, frame_rate:int):
        if frame_rate > 120 or frame_rate < 0:
            raise ValueError('The SyncOne2 device can only work with frame rate between 0 and 120.')
        response = self._send_cmd_wait_for_resp(f'SET FRAME RATE {frame_rate}\n')
        if 'OK' not in response:
            raise ConnectionError('Did not receive expected response from SyncOne2')

    def get_mask_len(self) -> int:
        response = self._send_cmd_wait_for_resp('MASK LEN\n')
        if response.isnumeric():
            return int(response)
        raise ConnectionError('Did not receive expected response from SyncOne2')

    def set_mask_len(self, mask_length: int):
        permitted_lengths = (150, 300, 450, 600, 750, 900)
        if mask_length not in permitted_lengths:
            raise ValueError(f'The SyncOne2 device can only with fixed mask lengths:[{" ,".join(permitted_lengths)}]')
        response = self._send_cmd_wait_for_resp(f'SET MASK LEN {mask_length}\n')
        if 'OK' not in response:
            raise ConnectionError('Did not receive expected response from SyncOne2')

    def get_offset(self) -> int:
        response = self._send_cmd_wait_for_resp('OFFSET\n')
        if response.lstrip('-').isnumeric():
            return int(response)
        raise ConnectionError('Did not receive expected response from SyncOne2')

    def set_offset(self, offset: int):
        if offset > 99 or offset < -99:
            raise ValueError('The SyncOne2 device can only work with an offset between -99 and 99.')
        response = self._send_cmd_wait_for_resp(f'SET OFFSET {offset}\n')
        if 'OK' not in response:
            raise ConnectionError('Did not receive expected response from SyncOne2')

    def get_speaker_dist(self) -> float:
        """Get the speaker distance currently set in the SyncOne2 Device.

        Raises:
            ConnectionError: When the response from the SyncOne2 device is not as expected.

        Returns:
            response(float): The speaker distance currently set in the SyncOne2 device.
        """
        response = self._send_cmd_wait_for_resp(f'SPEAKER DIST\n')
        if response.isnumeric():
            return float(response)
        raise ConnectionError('Did not receive expected response from SyncOne2')

    def set_speaker_dist(self, speaker_distance: float):
        """Set the speaker distance in the SyncOne2 device.
        Maximum of 20, minimum of 0. In increments of 0.5.

        Args:
            speaker_distance (float): Speaker distance to set in the SyncOne2 device.

        Raises:
            ValueError: When the value given is not an increment of 0.5 or outside the permitted range.
            ConnectionError: When the response from the SyncOne2 device is not as expected.
        """
        if (speaker_distance % 0.5) != 0 or speaker_distance > 20 or speaker_distance < 0:
            raise ValueError('The SyncOne2 device can only work with a speaker distance between 0 and 20 in increment of 0.5.')
        response = self._send_cmd_wait_for_resp(f'SET SPEAKER DIST {speaker_distance}\n')
        if 'OK' not in response:
            raise ConnectionError('Did not receive expected response from SyncOne2')

    def get_video_trigger_level(self) -> int:
        response = self._send_cmd_wait_for_resp('VIDEO TRIGGER LEVEL\n')
        if response not in ('0', '1', '2', '3', '4'):
            raise ConnectionError('Did not receive expected response from SyncOne2')
        return int(response)

    def set_video_trigger_level(self, trigger_level:int):
        if trigger_level > 4 or trigger_level < 0:
            raise ValueError('The trigger level must be between 0 and 4 for the SyncOne2 device.')
        response = self._send_cmd_wait_for_resp(f'SET VIDEO TRIGGER LEVEL {trigger_level}\n')
        if 'OK' not in response:
            raise ConnectionError('Did not receive expected response from SyncOne2')

    def get_results(self):
        response = self._send_cmd_wait_for_resp(f'STATS COUNT\n')
        if response.isnumeric():
            self._serial.flush()
            readings_lines = self._send_cmd_wait_for_resp('STATS\n').split('\r')
            if len(readings_lines) < int(response):
                raise ConnectionError('Did not receive expected response from SyncOne2')
            return self._process_readings(readings_lines)
        raise ConnectionError('Did not receive expected response from SyncOne2')

    def calibrate(self):
        response = self._send_cmd_wait_for_resp('CALIBRATE\n')
        if 'OK' not in response:
            raise ConnectionError('Did not receive expected response from SyncOne2')

    def clear_results(self):
        response = self._send_cmd_wait_for_resp('CLEAR STATS\n')
        if 'OK' not in response:
            raise ConnectionError('Did not receive expected response from SyncOne2')

    def start_measuring(self):
        response = self._send_cmd_wait_for_resp(f'START\n')
        if 'OK' not in response:
            raise ConnectionError('Did not receive expected response from SyncOne2')
        super().start_measuring()

    def stop_measuring(self):
        response = self._send_cmd_wait_for_resp(f'STOP\n',override_measuring_block=True)
        if 'OK' not in response:
            raise ConnectionError('Did not receive expected response from SyncOne2')
        super().stop_measuring()

    def enter_feature_code(self, feature_code: str):
        """Enter a feature code in the SyncOne2 device.

        Feature codes can be used in certain SyncOne2 devices to enable
        extra functionality or run extra actions.

        **This method is currently unreachable from RAFT tests**

        Args:
            feature_code (str): Feature code to send to the SyncOne2 device.

        Raises:
            RuntimeError: When the feature code is not possible on the specific SyncOne2 device.
            RuntimeError: When the feature code is unknown to the SyncOne2 device.
            ConnectionError: When the response from the SyncOne2 device is not as expected.
        """
        response = self._send_cmd_wait_for_resp(f'FEATURE CODE {feature_code}\n')
        if 'OK' not in response:
            if 'ERR invalid feature code' in response:
                raise RuntimeError('Feature code is not for the correct serial number of SyncOne2.')
            elif 'ERR unknown feature code' in response:
                raise RuntimeError('Feature code action requested is unknown to SyncOne2.')
            else:
                raise ConnectionError('Did not receive expected response from SyncOne2')

    def __del__(self):
        self._serial.write(b'EXIT\n')
        self._serial.close()
