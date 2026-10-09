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
#*   ** @brief : Automated unit tests for the network/wake controller (WoL).
#*   **          Runs under `python3 -m unittest` -- no device/rack config
#*   **          required (the WoL logic is exercised over loopback).
#* ******************************************************************************

import os
import sys
import socket
import unittest

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../")

from framework.core.networkControl import networkControlClass
from framework.core.networkModules.wol import networkWol
from framework.core.logModule import logModule

MAC = "aa:bb:cc:dd:ee:ff"
EXPECTED = b"\xff" * 6 + bytes.fromhex("aabbccddeeff") * 16


class TestNetworkWol(unittest.TestCase):
    """Unit tests for the Wake-on-LAN network module and controller."""

    @classmethod
    def setUpClass(cls):
        cls.log = logModule("networkControlTest")
        cls.log.setLevel(cls.log.CRITICAL)

    def test_magic_packet(self):
        """Magic packet is 6x0xFF followed by the MAC x16 (102 bytes)."""
        packet = networkWol(self.log, MAC)._magic_packet()
        self.assertEqual(packet, EXPECTED)
        self.assertEqual(len(packet), 102)

    def test_mac_normalisation(self):
        """Separators and surrounding whitespace are accepted."""
        for mac in ("aa:bb:cc:dd:ee:ff", "aa-bb-cc-dd-ee-ff", "  aabbccddeeff  "):
            self.assertEqual(networkWol(self.log, mac)._magic_packet(), EXPECTED)

    def test_invalid_mac_rejected_at_construction(self):
        """A bad MAC fails fast with a clear ValueError, not at wake() time."""
        for bad in ("", "aa:bb:cc", "zz:bb:cc:dd:ee:ff"):
            with self.assertRaises(ValueError):
                networkWol(self.log, bad)

    def test_wake_sends_magic_packet(self):
        """wake() sends the magic packet to the configured broadcast:port."""
        rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        rx.bind(("127.0.0.1", 0))
        port = rx.getsockname()[1]
        rx.settimeout(2)
        try:
            control = networkControlClass(
                self.log, {"type": "wol", "mac": MAC, "broadcast": "127.0.0.1", "port": port})
            self.assertTrue(control.wake())
            received, _ = rx.recvfrom(1024)
            self.assertEqual(received, EXPECTED)
        finally:
            rx.close()

    def test_unknown_type_does_not_crash(self):
        """An unknown type yields no module and wake() returns False (no AttributeError)."""
        control = networkControlClass(self.log, {"type": "nope"})
        self.assertIsNone(control.networkModule)
        self.assertFalse(control.wake())

    def test_retry_on_failure(self):
        """networkRetry retries on a falsy result up to retryCount, then gives up."""
        control = networkControlClass(self.log, {"type": "wol", "mac": MAC})
        control.retryCount = 2
        control.retryDelay = 0
        self.calls = 0

        def always_fail():
            self.calls += 1
            return False

        self.assertFalse(control.networkRetry(always_fail))
        self.assertEqual(self.calls, 3)  # initial attempt + 2 retries


if __name__ == "__main__":
    unittest.main()
