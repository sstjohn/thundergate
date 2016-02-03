'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2016 Saul St. John

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


def link_detect(self):
    print "[+] detecting link"
    res = self.dev.gphy.autonegotiate()
    if not res & 0x8000:
        print "[-] no link detected"
        self._set_tapdev_status(False)
        self._hcd = 0
    else:
        hcd = (res & 0x700) >> 8
        self._hcd = hcd
        if (hcd & 0x6) == 6:
            txpause = self.dev.gphy.may_send_pause()
            rxpause = self.dev.gphy.may_recv_pause()
            if hcd & 1:
                print "[+] full duplex gige link negotated (res: %08x, txpause: %s, rxpause: %s)" % (res, txpause, rxpause)
                self.dev.emac.mode.half_duplex = 1
            else:
                print "[+] half duplex gige link negotated (res: %08x, txpause: %s, rxpause: %s)" % (res, txpause, rxpause)
                self.dev.emac.mode.half_duplex = 0

            self.dev.emac.mode.port_mode = 2

            self.dev.emac.rx_mac_mode.enable_flow_control = 1 if rxpause else 0
            self.dev.emac.tx_mac_mode.enable_flow_control = 1 if txpause else 0

        elif (hcd > 0):
            if hcd == 5:
                print "[+] full duplex 100base-tx link negotiated"
                self.dev.emac.mode.half_duplex = 0
            elif hcd == 4:
                print "[+] 100base-t4 link negotiated"
                self.dev.emac.mode.half_duplex = 0
            elif hcd == 3:
                print "[+] half duplex 100base-tx link negotiated"
                self.dev.emac.mode.half_duplex = 1
            elif hcd == 2:
                print "[+] full duplex 10base-t link negotiated"
                self.dev.emac.mode.half_duplex = 0
            elif hcd == 1:
                print "[+] half duplex 10base-t link negotiated"
                self.dev.emac.mode.half_duplex = 1

            self.dev.emac.mode.port_mode = 1

            self.dev.emac.rx_mac_mode.enable_flow_control = 0
            self.dev.emac.tx_mac_mode.enable_flow_control = 0

        else:
            raise Exception("autonegotiaton failed, hcd %x" % hcd)
        self._set_tapdev_status(True)
