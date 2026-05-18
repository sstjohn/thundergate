'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2026  Saul St. John

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

from time import sleep

import tg_bringup
import tglib as tg

usleep = lambda x: sleep(x / 1000000.0)


def device_setup(self):
    dev = self.dev
    dev.drv = self
    print("[+] initializing device")
    dev.init()
    print("[+] resetting device")
    dev.reset()
    sleep(0.5)

    tg_bringup.configure_device(dev, self)

    self._init_rx_rings()
    dev.hpmb.box[tg.mb_rbd_standard_producer].low = 0
    self._init_tx_rings()
    dev.hpmb.box[tg.mb_sbd_host_producer].low = 0
    self._init_rr_rings()
    self._populate_rx_ring()

    print("[+] enabling transmit mac")
    tg_bringup.enable_tx_mac(dev)
    usleep(100)

    print("[+] enabling receive mac")
    tg_bringup.enable_rx_mac(dev)
    usleep(100)
