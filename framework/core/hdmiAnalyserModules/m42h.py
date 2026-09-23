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
#*   ** @addtogroup  : core.hdmiAnalyserModules
#*   ** @date        : 13/04/2026
#*   **
#*   ** @brief : Teledyne LeCroy Quantumdata M42h HDMI Analyser/Generator driver
#*   **
#*   ** This module communicates with the M42h instrument via its
#*   ** Advanced Test Platform (ATP) Python API (``tlqd`` package).
#*   **
#* ******************************************************************************

from .hdmiAnalyserInterface import HDMIAnalyserInterface

try:
    from tlqd import (
        TLqdInstrument,
        TLqdConnectSsh,
        TLqdUse,
        TLqdSetFormat,
        TLqdGetFormat,
        TLqdGetReceivedFormat,
        TLqdGetFormatParameters,
        TLqdUpdateFormatParameters,
        TLqdSetImage,
        TLqdGetImage,
        TLqdSetEdidData,
        TLqdSetEdidFile,
        TLqdEnableOutput,
        TLqdIsOutputEnabled,
        TLqdGetAviInfoframe,
        TLqdSetAudio,
        TLqdGetAudio,
        TLqdTestAudio,
        TLqdGetPixel,
        TLqdGetVideoFrame,
        TLqdCapture,
        TLqdSetScrambling,
        TLqdGetScrambling,
        TLqdSetPort,
        TLqdGetPorts,
        TLqdColorSpace,
        TLqdSubsampling,
        TLqdStatus,
        TLqdHdcpMode,
        TLqdPort,
        TLqdInfoFrameType,
        TLqdHotPlugMode,
        TLqdVideoFormatParameters,
    )
    _TLQD_AVAILABLE = True
except ImportError:
    _TLQD_AVAILABLE = False

# Map user-friendly colour-space strings to TLqdColorSpace enum values.
_COLOUR_SPACE_MAP = {}
if _TLQD_AVAILABLE:
    _COLOUR_SPACE_MAP = {
        "RGB": TLqdColorSpace.RGB,
        "YCbCr601": TLqdColorSpace.YCbCr601,
        "YCbCr709": TLqdColorSpace.YCbCr709,
        "BT2020YCbCr": TLqdColorSpace.BT2020YCbCr,
        "BT2020RGB": TLqdColorSpace.BT2020RGB,
    }

# Map user-friendly sub-sampling strings to TLqdSubsampling enum values.
_SUBSAMPLING_MAP = {}
if _TLQD_AVAILABLE:
    _SUBSAMPLING_MAP = {
        "RGB444": TLqdSubsampling.RGB444,
        "444": TLqdSubsampling.SS444,
        "422": TLqdSubsampling.SS422,
        "420": TLqdSubsampling.SS420,
    }


class M42hController(HDMIAnalyserInterface):
    """Driver for the Teledyne LeCroy Quantumdata M42h 96G Video Analyser/Generator.

    The M42h is controlled through its ATP (Advanced Test Platform) Python API
    exposed by the ``tlqd`` package.  The package is distributed as part of the
    M42h *Application Programming Interface* download available from Teledyne
    LeCroy's software-download portal.

    Configuration keys (passed via *config* dict):
        ``host``  – IP address or hostname of the M42h instrument.
        ``port``  – (optional) SSH port, defaults to 22.
        ``user``  – (optional) SSH user, defaults to ``"qd"``.
        ``passwd`` – (optional) SSH password, defaults to ``"qd"``.
        ``card``  – (optional) Card number to select with ``TLqdUse``.
    """

    def __init__(self, host: str, port: int = None, user: str = "qd",
                 passwd: str = "qd", card: int = None):
        if not _TLQD_AVAILABLE:
            raise ImportError(
                "The 'tlqd' package is required to use M42hController. "
                "Install the Quantumdata ATP API from Teledyne LeCroy."
            )
        self._host = host
        self._port = port
        self._user = user
        self._passwd = passwd
        self._card = card
        self._qdDev = None

    # ── Connection / lifecycle ──────────────────────────────────────────

    def connect(self):
        self._qdDev = TLqdConnectSsh(self._host, user=self._user,
                                     passwd=self._passwd, port=self._port)
        if not self._qdDev.connected:
            raise RuntimeError(
                f"Failed to connect to M42h at {self._host}"
            )
        if self._card is not None:
            TLqdUse(self._qdDev, self._card)

    def disconnect(self):
        if self._qdDev is not None:
            self._qdDev.close()
            self._qdDev = None

    # ── Port selection ──────────────────────────────────────────────────

    def select_port(self, port):
        TLqdSetPort(self._qdDev, port)

    # ── Hot-plug control ────────────────────────────────────────────────

    def set_hpd(self, state: bool, duration: int = 100):
        if state:
            self._qdDev.setHotPlug(duration=duration)
        else:
            self._qdDev.setHotPlug(duration=0)

    # ── Generator (source) operations ───────────────────────────────────

    def set_video_format(self, format_name: str, colour_space: str = None,
                         subsampling: str = None, bit_depth: int = None,
                         vic: int = None):
        kwargs = {}
        if colour_space and colour_space in _COLOUR_SPACE_MAP:
            kwargs["colorSpace"] = _COLOUR_SPACE_MAP[colour_space]
        if subsampling and subsampling in _SUBSAMPLING_MAP:
            kwargs["subsampling"] = _SUBSAMPLING_MAP[subsampling]
        if bit_depth is not None:
            kwargs["bitDepth"] = bit_depth
        if vic is not None:
            kwargs["vic"] = vic
        TLqdSetFormat(self._qdDev, format_name, **kwargs)

    def set_hdr_mode(self, mode: str):
        # HDR is signalled via the DRM InfoFrame; configure via InfoFrame
        # type control.  The caller is expected to use configInfoFrame and
        # updateFormatParameters for full DRM control.  This helper enables
        # or disables the HDR InfoFrame packet.
        if mode.upper() == "SDR":
            self._qdDev.configInfoFrame(type=TLqdInfoFrameType.HDR_IF,
                                        enable=False)
        else:
            self._qdDev.configInfoFrame(type=TLqdInfoFrameType.HDR_IF,
                                        enable=True)

    def set_allm(self, enabled: bool):
        # ALLM is signalled via the HDMI Forum VSIF (ALLM bit).
        # Toggle the HDMI Forum VS InfoFrame accordingly.
        self._qdDev.configInfoFrame(type=TLqdInfoFrameType.HDMI_FORUM_VS_IF,
                                    enable=enabled)

    def set_vrr(self, enabled: bool, base_refresh_rate: int = None):
        # VRR is signalled via the Video Timing Extended Metadata (VTEM)
        # packet on the generator side.
        if enabled:
            kwargs = {"vrrEn": 1}
            if base_refresh_rate is not None:
                kwargs["baseRefreshRate"] = base_refresh_rate
            self._qdDev.updateVtem(**kwargs)
        else:
            self._qdDev.updateVtem(vrrEn=0)

    def set_avi_content_type(self, content_type: str):
        # Content type is part of the AVI InfoFrame (ITC/CN fields).
        # Update via format parameters.
        pass

    def set_spd_info(self, vendor: str, description: str):
        # SPD InfoFrame configuration.
        self._qdDev.configInfoFrame(type=TLqdInfoFrameType.SPD_IF,
                                    enable=True)

    def start_output(self):
        TLqdEnableOutput(self._qdDev, True)

    def stop_output(self):
        TLqdEnableOutput(self._qdDev, False)

    # ── EDID operations ─────────────────────────────────────────────────

    def get_edid(self, port: str = "") -> bytes:
        # The ATP API does not expose a direct "read-back EDID bytes"
        # from the sink side in a simple getter.  The EDID read-back
        # typically occurs through the compliance test infrastructure.
        # Return empty bytes as placeholder.
        return b""

    def set_edid(self, edid_data: str, hp_duration_ms: int = 100):
        TLqdSetEdidData(self._qdDev, edid_data,
                        hpDurationInMs=hp_duration_ms)

    def set_edid_file(self, edid_file: str, hp_duration_ms: int = 100):
        TLqdSetEdidFile(self._qdDev, edid_file,
                        hpDurationInMs=hp_duration_ms)

    def restore_default_edid(self, port: str = ""):
        # Re-apply hot-plug with no custom EDID to revert to built-in EDID.
        self._qdDev.setHotPlug(duration=100)

    # ── Analyser (sink) read-back ───────────────────────────────────────

    def get_video_status(self) -> dict:
        metrics = TLqdGetReceivedFormat(self._qdDev)
        result = {}
        for tag in TLqdVideoFormatParameters.tags:
            value = getattr(metrics, tag.longTag, None)
            if value is not None:
                result[tag.longTag] = str(value)
        return result

    def get_audio_status(self) -> dict:
        audio = TLqdGetAudio(self._qdDev)
        return {
            "sampling": getattr(audio, "sampling", 0),
            "bit_size": getattr(audio, "bitSize", 0),
            "channels": getattr(audio, "channels", []),
        }

    def get_hdcp_status(self) -> dict:
        # Attempt to read HDCP for both modes and return whichever is active.
        try:
            params = self._qdDev.getHdcp(TLqdPort.PortRx,
                                         TLqdHdcpMode.HDCP23Mode)
            return {
                "status": getattr(params, "hdcpStatus", ""),
                "key": getattr(params, "key", ""),
            }
        except Exception:
            return {"status": "", "key": ""}

    def get_link_status(self) -> dict:
        output_enabled = TLqdIsOutputEnabled(self._qdDev)
        return {
            "output_enabled": output_enabled,
        }

    def get_avi_info(self) -> dict:
        result, info, octets = TLqdGetAviInfoframe(self._qdDev)
        return {
            "valid": result,
            "info": info,
            "octets": octets,
        }

    def get_spd_info(self) -> dict:
        result, info, octets = self._qdDev.getInfoframe("SPD")
        return {
            "valid": result,
            "info": info,
            "octets": octets,
        }

    def get_background_color(self) -> str:
        pixel = TLqdGetPixel(self._qdDev, 0, 0)
        if pixel.valid:
            return f"({pixel.red},{pixel.green},{pixel.blue})"
        return ""

    # ── HDCP control ────────────────────────────────────────────────────

    def set_hdcp_mode(self, mode: str):
        mode_map = {
            "none": TLqdHdcpMode.HDCPNone,
            "1.4": TLqdHdcpMode.HDCP13Mode,
            "2.3": TLqdHdcpMode.HDCP23Mode,
        }
        hdcp_mode = mode_map.get(mode.lower(), TLqdHdcpMode.HDCPNone)
        self._qdDev.setHdcp(TLqdPort.PortRx, hdcp_mode)

    # ── Snapshot / combined status ──────────────────────────────────────

    def snapshot(self) -> dict:
        return {
            "video": self.get_video_status(),
            "audio": self.get_audio_status(),
            "hdcp": self.get_hdcp_status(),
            "link": self.get_link_status(),
            "avi": self.get_avi_info(),
        }

    # ── Additional M42h-specific helpers ────────────────────────────────

    @property
    def qdDev(self):
        """Provide direct access to the underlying TLqdInstrument for
        advanced operations not covered by the standard interface."""
        return self._qdDev
