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
#*   ** @brief : Abstract interface for HDMI Analyser controllers
#*   **
#* ******************************************************************************

from abc import ABC, abstractmethod


class HDMIAnalyserInterface(ABC):
    """Abstract base class defining the interface for an HDMI Analyser/Generator controller.

    Implementations must provide methods for controlling the analyser in both
    source (generator) and sink (analyser) modes. This covers capabilities
    required by dsHdmiIn and dsVideoPort L3 test procedures.
    """

    # ── Connection / lifecycle ──────────────────────────────────────────

    @abstractmethod
    def connect(self):
        """Establish a connection to the analyser instrument."""
        pass

    @abstractmethod
    def disconnect(self):
        """Close the connection to the analyser instrument."""
        pass

    # ── Port selection ──────────────────────────────────────────────────

    @abstractmethod
    def select_port(self, port):
        """Select the active HDMI port on the analyser.

        Args:
            port: Port number or identifier.
        """
        pass

    # ── Hot-plug control ────────────────────────────────────────────────

    @abstractmethod
    def set_hpd(self, state: bool, duration: int = 100):
        """Assert or de-assert the Hot Plug Detect signal.

        Args:
            state: ``True`` to assert HPD (simulate connect),
                   ``False`` to de-assert (simulate disconnect).
            duration: Hot-plug duration in milliseconds.
        """
        pass

    # ── Generator (source) operations ───────────────────────────────────

    @abstractmethod
    def set_video_format(self, format_name: str, colour_space: str = None,
                         subsampling: str = None, bit_depth: int = None,
                         vic: int = None):
        """Configure the video generator output format.

        Args:
            format_name: Format name string (e.g. ``"1080p60"``, ``"2160p60"``).
            colour_space: Colour space (e.g. ``"RGB"``, ``"YCbCr709"``).
            subsampling: Sub-sampling (e.g. ``"444"``, ``"422"``, ``"420"``).
            bit_depth: Bits per component (8, 10, 12).
            vic: Video Identification Code (optional).
        """
        pass

    @abstractmethod
    def set_hdr_mode(self, mode: str):
        """Set the HDR signalling mode on the generator output.

        Args:
            mode: HDR standard (e.g. ``"SDR"``, ``"HDR10"``, ``"HLG"``,
                  ``"DolbyVision"``, ``"HDR10PLUS"``).
        """
        pass

    @abstractmethod
    def set_allm(self, enabled: bool):
        """Enable or disable Auto Low Latency Mode on the generator.

        Args:
            enabled: ``True`` to enable ALLM, ``False`` to disable.
        """
        pass

    @abstractmethod
    def set_vrr(self, enabled: bool, base_refresh_rate: int = None):
        """Enable or disable Variable Refresh Rate on the generator.

        Args:
            enabled:  ``True`` to enable VRR, ``False`` to disable.
            base_refresh_rate: Base refresh rate for VTEM (optional).
        """
        pass

    @abstractmethod
    def set_avi_content_type(self, content_type: str):
        """Set the AVI InfoFrame content type on the generator.

        Args:
            content_type: Content type (e.g. ``"Graphics"``, ``"Cinema"``,
                          ``"Photo"``, ``"Game"``).
        """
        pass

    @abstractmethod
    def set_spd_info(self, vendor: str, description: str):
        """Set the Source Product Descriptor InfoFrame on the generator.

        Args:
            vendor:      Vendor name string.
            description: Product description string.
        """
        pass

    @abstractmethod
    def start_output(self):
        """Start the video generator output."""
        pass

    @abstractmethod
    def stop_output(self):
        """Stop the video generator output."""
        pass

    # ── EDID operations ─────────────────────────────────────────────────

    @abstractmethod
    def get_edid(self, port: str = "") -> bytes:
        """Read the EDID currently presented on the specified port.

        Args:
            port: Port identifier. If empty, uses the currently selected port.

        Returns:
            Raw EDID bytes.
        """
        pass

    @abstractmethod
    def set_edid(self, edid_data: str, hp_duration_ms: int = 100):
        """Load a custom EDID onto the analyser sink port.

        Args:
            edid_data: EDID data as hex string (e.g. ``"00FFFFFFFFFFFF00..."``).
            hp_duration_ms: Hot-plug duration in milliseconds (0=no HP).
        """
        pass

    @abstractmethod
    def restore_default_edid(self, port: str = ""):
        """Restore the factory-default EDID on a port.

        Args:
            port: Port identifier.
        """
        pass

    # ── Analyser (sink) read-back ───────────────────────────────────────

    @abstractmethod
    def get_video_status(self) -> dict:
        """Read the current video status from the analyser input.

        Returns:
            dict with video format parameters from the received signal.
        """
        pass

    @abstractmethod
    def get_audio_status(self) -> dict:
        """Read the current audio status from the analyser input.

        Returns:
            dict with keys: ``sampling``, ``bit_size``, ``channels``.
        """
        pass

    @abstractmethod
    def get_hdcp_status(self) -> dict:
        """Read the current HDCP status from the analyser input.

        Returns:
            dict with keys: ``status``, ``key``.
        """
        pass

    @abstractmethod
    def get_link_status(self) -> dict:
        """Read the link status.

        Returns:
            dict with link status information.
        """
        pass

    @abstractmethod
    def get_avi_info(self) -> dict:
        """Read the AVI InfoFrame data from the analyser input.

        Returns:
            dict with keys: ``valid``, ``info``, ``octets``.
        """
        pass

    @abstractmethod
    def get_spd_info(self) -> dict:
        """Read the SPD InfoFrame data from the analyser input.

        Returns:
            dict with keys: ``valid``, ``info``, ``octets``.
        """
        pass

    @abstractmethod
    def get_background_color(self) -> str:
        """Read the current background colour from the analyser input.

        Returns:
            Pixel colour string (e.g. ``"(R,G,B)"``).
        """
        pass

    # ── HDCP control ────────────────────────────────────────────────────

    @abstractmethod
    def set_hdcp_mode(self, mode: str):
        """Set the HDCP mode advertised by the analyser.

        Args:
            mode: ``"none"``, ``"1.4"``, ``"2.3"``.
        """
        pass

    # ── Snapshot / combined status ──────────────────────────────────────

    @abstractmethod
    def snapshot(self) -> dict:
        """Collect a combined status snapshot from the analyser.

        Returns:
            dict containing ``video``, ``audio``, ``hdcp``, ``link``,
            ``avi`` sub-dicts.
        """
        pass
