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

import asyncio
import logging

import tg_bringup
from .ring import init_rr_rings, init_rx_rings, init_tx_rings

logger = logging.getLogger(__name__)

msleep = lambda t: asyncio.sleep(t / 1000.0)


async def _device_setup(self):
    dev = self.dev
    dev.drv = self
    logger.info("initializing device")
    dev.init()
    logger.info("resetting device")
    dev.reset()
    await msleep(0.5)
    tg_bringup.configure_device(dev, self)


async def enable_tx_mac(self):
    logger.info("enabling transmit mac")
    tg_bringup.enable_tx_mac(self.dev)
    await msleep(100)


async def enable_rx_mac(self):
    logger.info("enabling receive mac")
    tg_bringup.enable_rx_mac(self.dev)
    await msleep(100)


async def _enable_rx(self):
    await init_rr_rings(self)
    await init_rx_rings(self)
    await enable_rx_mac(self)


async def _enable_tx(self):
    await init_tx_rings(self)
    await enable_tx_mac(self)
