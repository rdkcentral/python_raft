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
#*   ** Project      : RAFT
#*   ** @addtogroup  : core.networkModules
#*   ** @file        : wol.py
#*   ** @brief : Wake-on-LAN network module. wake() sends a magic packet to
#*   **          wake a sleeping / soft-off device on the same broadcast domain.
#*   **
#* ******************************************************************************

import socket


class networkWol():
    """Wake-on-LAN network module.

    A magic packet wakes a device that is asleep or in a Wake-on-LAN soft-off
    state, provided the host sending it shares the target's layer-2 broadcast
    domain (or a directed subnet broadcast reaches it). Wake-on-LAN is a
    network (layer-2) action, not a power action: it can only wake a device, so
    the module exposes a single ``wake()`` verb.

    Rack-config fields (under a device's ``network:``)::

        network:
            type: "wol"
            mac: "b0:3e:51:ff:f6:bc"       # required - target NIC MAC
            broadcast: "255.255.255.255"   # optional - subnet broadcast for directed WoL
            port: 9                        # optional - 9 (default) or 7
    """

    def __init__(self, log, mac, broadcast="255.255.255.255", port=9):
        """
        Args:
            log: The log module.
            mac (str): Target NIC MAC address (":" / "-" separated or bare hex).
            broadcast (str): Broadcast address the magic packet is sent to.
            port (int): UDP port for the magic packet (typically 7 or 9).
        """
        self.log = log
        if not mac:
            raise ValueError("networkWol requires a 'mac' address")
        self.mac = mac
        self.broadcast = broadcast or "255.255.255.255"
        self.port = int(port) if port else 9
        self.log.info("networkWol(mac={}, broadcast={}, port={})".format(
            self.mac, self.broadcast, self.port))

    def _magicPacket(self):
        """Build the Wake-on-LAN magic packet: 6x 0xFF followed by the MAC x16."""
        hexMac = self.mac.replace(":", "").replace("-", "").replace(".", "")
        if len(hexMac) != 12:
            raise ValueError("Invalid MAC address: {}".format(self.mac))
        return b"\xff" * 6 + bytes.fromhex(hexMac) * 16

    def wake(self):
        """Send the Wake-on-LAN magic packet.

        Returns:
            bool: True if the packet was sent, False on error.
        """
        try:
            packet = self._magicPacket()
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(packet, (self.broadcast, self.port))
            self.log.info("networkWol().wake: magic packet sent to {}".format(self.mac))
            return True
        except Exception as error:
            self.log.error("networkWol().wake failed: {}".format(error))
            return False
