
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
