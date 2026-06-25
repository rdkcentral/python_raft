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
    
    def setHDCPVersion(self, port: int, hdcp_version: str):
        """
        Set the HDCP version for the HDMI input port.

        Args:
            port (int): HDMI input port number.
            hdcp_version (str): HDCP version string. (VERSION_1_X, VERSION_2_X, UNDEFINED)
        Returns:
            bool: True if HDCP version set successfully.
        """
        results = self.testUserResponse.getUserYN(f"Set HDCP version '{hdcp_version}' for HDMI input port {port}? (Y/N):")
        return results

    def validateEdid(self, port: int, expected_edid: list):
        """
        Validate the EDID data for the HDMI input port.

        Args:
            port (int): HDMI input port number.
            expected_edid (list): Expected EDID data bytes.
        Returns:
            bool: True if EDID data matches expected values.
        """
        results = self.testUserResponse.getUserYN(f"Validate EDID data for HDMI input port {port} against expected data {expected_edid}? (Y/N):")
        return results

    def sendAudioInfoFrame(self, port: int, data: list):
        """
        Ask user to manually set Audio Info Frame for the HDMI input port and confirm.
        """
        results = self.testUserResponse.getUserYN(f"Set Audio Info Frame for HDMI input port {port} with data {data}? (Y/N):")
        return results

    def sendAVIInfoFrame(self, port: int, data: list):
        """
        Ask user to manually set AVI Info Frame for the HDMI input port and confirm.
        """
        results = self.testUserResponse.getUserYN(f"Set AVI Info Frame for HDMI input port {port} with data {data}? (Y/N):")
        return results

    def sendDRMInfoFrame(self, port: int, data: list):
        """
        Ask user to manually set DRM Info Frame for the HDMI input port and confirm.
        """
        results = self.testUserResponse.getUserYN(f"Set DRM Info Frame for HDMI input port {port} with data {data}? (Y/N):")
        return results

    def setHotplugState(self, port: int, connected: bool, version: str):
        if connected == False:
                result = self.testUserResponse.getUserYN(f"UnPlug the HDMI device of HDCP version {version} and press Y:")
        else :
                result = self.testUserResponse.getUserYN(f"Plug the HDMI device of HDCP version {version} and press Y:")
        return result

    def setHDCPStatus(self, port: int, hdcp_version: str, status: str):
        """
        Ask user to manually set HDCP status for the HDMI input port and confirm.
        """
        results = self.testUserResponse.getUserYN(f"Set HDCP status '{status}' (version: {hdcp_version}) for HDMI input port {port}? (Y/N):")
        return results

    def setSignalStatus(self, port: int, signal_state: str):
        """
        Ask user to manually set signal status for the HDMI input port and confirm.
        """
        results = self.testUserResponse.getUserYN(f"Set signal status '{signal_state}' for HDMI input port {port}? (Y/N):")
        return results

    def sendSPDInfoFrame(self, port: int, data: list):
        """
        Ask user to manually set SPD Info Frame for the HDMI input port and confirm.
        """
        results = self.testUserResponse.getUserYN(f"Set SPD Info Frame for HDMI input port {port} with data {data}? (Y/N):")
        return results

    def sendVSIFInfoFrame(self, port: int, data: list):
        """
        Ask user to manually set Vendor Specific Info Frame for the HDMI input port and confirm.
        """
        results = self.testUserResponse.getUserYN(f"Set Vendor Specific Info Frame for HDMI input port {port} with data {data}? (Y/N):")
        return results

    def SetVIC(self, port: int, vic: str):
        """
        Ask user to manually set VIC for the HDMI input port and confirm.
        """
        results = self.testUserResponse.getUserYN(f"Set VIC '{vic}' for HDMI input port {port}? (Y/N):")
        return results

    def setVRRStatus(self, port: int, vrrActive: bool, M_CONST: bool, fastVActive: bool, frameRate: float):
        """
        Ask user to manually set VRR status for the HDMI input port and confirm.
        """
        results = self.testUserResponse.getUserYN(f"Set VRR status for HDMI input port {port} with vrrActive={vrrActive}, M_CONST={M_CONST}, fastVActive={fastVActive}, frameRate={frameRate}? (Y/N):")
        return results

    def start(self):
        """
        Start the virtual HDMI controller (stub).

        Returns:
            None
        """
        pass

    def stop(self):
        """
        Stop the virtual HDMI controller (stub).

        Returns:
            None
        """
        pass

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