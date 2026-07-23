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
#*   ** @date        : 13/04/2026
#*   **
#*   ** @brief : HDMI Analyser controller facade
#*   **
#* ******************************************************************************

from framework.core.logModule import logModule
from framework.core.hdmiAnalyserModules.m42h import M42hController


class HDMIAnalyserController():
    """Facade controller for HDMI Analyser/Generator instruments.

    Selects a concrete backend based on the ``type`` key in *config* and
    delegates all operations, following the same pattern used by
    :class:`audioAmplifierController`, :class:`HDMICECController`, and
    :class:`AVSyncController`.

    Supported types:
        ``m42h`` – Teledyne LeCroy Quantumdata M42h 96G Video Analyser/Generator.

    Rack-config example::

        hdmiAnalyserController:
            type: "m42h"
            host: "192.168.0.50"
            port: 22             # optional SSH port
            user: "qd"           # optional, defaults to "qd"
            passwd: "qd"         # optional, defaults to "qd"
            card: 4              # optional card number
    """

    def __init__(self, log: logModule, config: dict):
        self._log = log
        self.controllerType = config.get("type")
        self.host = config.get("host")

        if self.controllerType == "m42h":
            self.hdmiAnalyser = M42hController(
                host=self.host,
                port=config.get("port"),
                user=config.get("user", "qd"),
                passwd=config.get("passwd", "qd"),
                card=config.get("card"),
            )
        else:
            raise ValueError(
                f"Unsupported hdmiAnalyserController type: '{self.controllerType}'"
            )

    # ── Connection / lifecycle ──────────────────────────────────────────

    def connect(self):
        self._log.info("Connecting to HDMI analyser")
        self.hdmiAnalyser.connect()

    def disconnect(self):
        self._log.info("Disconnecting from HDMI analyser")
        self.hdmiAnalyser.disconnect()

    # ── Port selection ──────────────────────────────────────────────────

    def select_port(self, port):
        self._log.info(f"Selecting HDMI analyser port: {port}")
        self.hdmiAnalyser.select_port(port)

    # ── Hot-plug control ────────────────────────────────────────────────

    def set_hpd(self, state: bool, duration: int = 100):
        self._log.info(f"Setting HPD state: {state} duration: {duration}ms")
        self.hdmiAnalyser.set_hpd(state, duration)

    # ── Generator (source) operations ───────────────────────────────────

    def set_video_format(self, format_name: str, colour_space: str = None,
                         subsampling: str = None, bit_depth: int = None,
                         vic: int = None):
        self._log.info(f"Setting video format: {format_name} "
                       f"cs={colour_space} ss={subsampling} "
                       f"depth={bit_depth} vic={vic}")
        self.hdmiAnalyser.set_video_format(
            format_name, colour_space, subsampling, bit_depth, vic
        )

    def set_hdr_mode(self, mode: str):
        self._log.info(f"Setting HDR mode: {mode}")
        self.hdmiAnalyser.set_hdr_mode(mode)

    def set_allm(self, enabled: bool):
        self._log.info(f"Setting ALLM: {'enabled' if enabled else 'disabled'}")
        self.hdmiAnalyser.set_allm(enabled)

    def set_vrr(self, enabled: bool, base_refresh_rate: int = None):
        self._log.info(f"Setting VRR: {'enabled' if enabled else 'disabled'}"
                       f"{f' base_rate={base_refresh_rate}' if base_refresh_rate else ''}")
        self.hdmiAnalyser.set_vrr(enabled, base_refresh_rate)

    def set_avi_content_type(self, content_type: str):
        self._log.info(f"Setting AVI content type: {content_type}")
        self.hdmiAnalyser.set_avi_content_type(content_type)

    def set_spd_info(self, vendor: str, description: str):
        self._log.info(f"Setting SPD info: vendor={vendor}, desc={description}")
        self.hdmiAnalyser.set_spd_info(vendor, description)

    def start_output(self):
        self._log.info("Starting HDMI generator output")
        self.hdmiAnalyser.start_output()

    def stop_output(self):
        self._log.info("Stopping HDMI generator output")
        self.hdmiAnalyser.stop_output()

    # ── EDID operations ─────────────────────────────────────────────────

    def get_edid(self, port: str = "") -> bytes:
        self._log.info("Reading EDID")
        return self.hdmiAnalyser.get_edid(port)

    def set_edid(self, edid_data: str, hp_duration_ms: int = 100):
        self._log.info("Loading custom EDID")
        self.hdmiAnalyser.set_edid(edid_data, hp_duration_ms)

    def restore_default_edid(self, port: str = ""):
        self._log.info("Restoring default EDID")
        self.hdmiAnalyser.restore_default_edid(port)

    # ── Analyser (sink) read-back ───────────────────────────────────────

    def get_video_status(self) -> dict:
        self._log.info("Getting video status from analyser")
        return self.hdmiAnalyser.get_video_status()

    def get_audio_status(self) -> dict:
        self._log.info("Getting audio status from analyser")
        return self.hdmiAnalyser.get_audio_status()

    def get_hdcp_status(self) -> dict:
        self._log.info("Getting HDCP status from analyser")
        return self.hdmiAnalyser.get_hdcp_status()

    def get_link_status(self) -> dict:
        self._log.info("Getting link status from analyser")
        return self.hdmiAnalyser.get_link_status()

    def get_avi_info(self) -> dict:
        self._log.info("Getting AVI InfoFrame from analyser")
        return self.hdmiAnalyser.get_avi_info()

    def get_spd_info(self) -> dict:
        self._log.info("Getting SPD InfoFrame from analyser")
        return self.hdmiAnalyser.get_spd_info()

    def get_background_color(self) -> str:
        self._log.info("Getting background colour from analyser")
        return self.hdmiAnalyser.get_background_color()

    # ── HDCP control ────────────────────────────────────────────────────

    def set_hdcp_mode(self, mode: str):
        self._log.info(f"Setting HDCP mode: {mode}")
        self.hdmiAnalyser.set_hdcp_mode(mode)

    # ── Snapshot / combined status ──────────────────────────────────────

    def snapshot(self) -> dict:
        self._log.info("Taking analyser snapshot")
        return self.hdmiAnalyser.snapshot()
