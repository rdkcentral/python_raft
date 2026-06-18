#!/usr/bin/env python3
#** *****************************************************************************
# *
# * If not stated otherwise in this file or this component's LICENSE file the
# * following copyright and licenses apply:
# *
# * Copyright 2026 RDK Management
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *
# * http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *
#* ******************************************************************************
from .hdmiAnalyserInterface import HDMIAnalyserInterface

class manualHdmiController(HDMIAnalyserInterface):
    def __init__(self, logger, host, user, passwd, port:int=22, prompt:str='~#', control_port:int=8080, device:str=""):
        #super().__init__(logger, address, username, password, port, prompt, control_port, device)
        self._log = logger
        self.address = host
        self.username = user
        self.password = passwd
        self.port = port
        self.prompt = prompt
        self.control_port = control_port
        self.device = device
    def sendEDIDRead(self, port: int, data: list):
        return True

    def sendFrameRateChanged(self, port: int):
        return True

    def setHDCPStatus(self, port: int, status: str, version: str):
        return True

    def setHotplugState(self, port: int, connected: bool, version: str):
        if connected == False:
                result = self.testUserResponse.getUserYN(f"UnPlug the HDMI device of HDCP version {version} and press Y:")
        else :
                result = self.testUserResponse.getUserYN(f"Plug the HDMI device of HDCP version {version} and press Y:")
        return result

    # ── Connection / lifecycle ──────────────────────────────────────────

    def connect(self):
        return True

    def disconnect(self):
        return True

    # ── Port selection ──────────────────────────────────────────────────

    def select_port(self, port):
        return True

    # ── Hot-plug control ────────────────────────────────────────────────

    def set_hpd(self, state: bool, duration: int = 100):
        return True

    # ── Generator (source) operations ───────────────────────────────────

    def set_video_format(self, format_name: str, colour_space: str = None,
                         subsampling: str = None, bit_depth: int = None,
                         vic: int = None):
        return True

    def set_hdr_mode(self, mode: str):
        # HDR is signalled via the DRM InfoFrame; configure via InfoFrame
        # type control.  The caller is expected to use configInfoFrame and
        # updateFormatParameters for full DRM control.  This helper enables
        # or disables the HDR InfoFrame packet.
        return True

    def set_allm(self, enabled: bool):
        # ALLM is signalled via the HDMI Forum VSIF (ALLM bit).
        # Toggle the HDMI Forum VS InfoFrame accordingly.
        return True

    def set_vrr(self, enabled: bool, base_refresh_rate: int = None):
        # VRR is signalled via the Video Timing Extended Metadata (VTEM)
        # packet on the generator side.
        return True

    def set_avi_content_type(self, content_type: str):
        # Content type is part of the AVI InfoFrame (ITC/CN fields).
        # Update via format parameters.
        pass

    def set_spd_info(self, vendor: str, description: str):
        # SPD InfoFrame configuration.
        return True

    def start_output(self):
        return True

    def stop_output(self):
        return True

    # ── EDID operations ─────────────────────────────────────────────────

    def get_edid(self, port: str = "") -> bytes:
        # The ATP API does not expose a direct "read-back EDID bytes"
        # from the sink side in a simple getter.  The EDID read-back
        # typically occurs through the compliance test infrastructure.
        # Return empty bytes as placeholder.
        return b""

    def set_edid(self, edid_data: str, hp_duration_ms: int = 100):
        return True


    def restore_default_edid(self, port: str = ""):
        # Re-apply hot-plug with no custom EDID to revert to built-in EDID.
        return True

    # ── Analyser (sink) read-back ───────────────────────────────────────

    def get_video_status(self) -> dict:
        result = {}
        return result

    def get_audio_status(self) -> dict:
        return {}

    def get_hdcp_status(self) -> dict:
        # Attempt to read HDCP for both modes and return whichever is active.
        return {}

    def get_link_status(self) -> dict:
        return {}

    def get_avi_info(self) -> dict:
        return {}

    def get_spd_info(self) -> dict:
        return {}

    def get_background_color(self) -> str:
        return ""

    # ── HDCP control ────────────────────────────────────────────────────

    def set_hdcp_mode(self, mode: str):
        pass

    # ── Snapshot / combined status ──────────────────────────────────────

    def snapshot(self) -> dict:
        return {}
