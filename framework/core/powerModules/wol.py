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
#*   ** @addtogroup  : core.powerModules
#*   ** @file        : wol.py
#*   ** @brief : Wake-on-LAN power module. powerOn() sends a magic packet to
#*   **          wake a sleeping / soft-off device on the same broadcast domain.
#*   **
#* ******************************************************************************

import socket


class powerWol():
    """Wake-on-LAN "power switch".

    A magic packet wakes a device that is asleep or in a Wake-on-LAN soft-off
    state, provided the host sending it shares the target's layer-2 broadcast
    domain (or a directed subnet broadcast reaches it). Wake-on-LAN is
    wake-only: it cannot power a device off, so powerOff() is a logged no-op and
    reboot() is a best-effort wake.

    Rack-config fields (under a device's ``powerSwitch:``)::

        powerSwitch:
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
            raise ValueError("powerWol requires a 'mac' address")
        self.mac = mac
        self.broadcast = broadcast or "255.255.255.255"
        self.port = int(port) if port else 9
        self.log.info("powerWol(mac={}, broadcast={}, port={})".format(
            self.mac, self.broadcast, self.port))

    def _magicPacket(self):
        """Build the Wake-on-LAN magic packet: 6x 0xFF followed by the MAC x16."""
        hexMac = self.mac.replace(":", "").replace("-", "").replace(".", "")
        if len(hexMac) != 12:
            raise ValueError("Invalid MAC address: {}".format(self.mac))
        return b"\xff" * 6 + bytes.fromhex(hexMac) * 16

    def powerOn(self):
        """Send the Wake-on-LAN magic packet.

        Returns:
            bool: True if the packet was sent, False on error.
        """
        try:
            packet = self._magicPacket()
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(packet, (self.broadcast, self.port))
            self.log.info("powerWol().powerOn: magic packet sent to {}".format(self.mac))
            return True
        except Exception as error:
            self.log.error("powerWol().powerOn failed: {}".format(error))
            return False

    def powerOff(self):
        """Wake-on-LAN cannot power a device off; logged no-op.

        Returns:
            bool: Always True (nothing to do).
        """
        self.log.info("powerWol().powerOff: Wake-on-LAN is wake-only; no power-off performed")
        return True

    def reboot(self):
        """No hard power cycle over Wake-on-LAN; best-effort wake.

        Returns:
            bool: Result of powerOn().
        """
        self.log.info("powerWol().reboot: Wake-on-LAN is wake-only; sending wake")
        return self.powerOn()
