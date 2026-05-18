import sys
import asyncio

from .platform_fun import platform_setup

from .device_mgmt import arrive_device
from .kbd_mgmt import keypress_dispatch

DRIVER_PROPERTIES = {
    "running": False,
    "device": None,
    "loop": None,
    "kbd_h": None,
    "status_block": None,
    "status_block_vaddr": None,
    "status_block_paddr": None,
    "mac_addr": None,
    "tap_h": None,
    "tap_name": None,
    "verbose": False,
}

class Driver(object):
    __slots__ = list(DRIVER_PROPERTIES.keys())
    def __init__(self):
        for prop in DRIVER_PROPERTIES:
            setattr(self, prop, DRIVER_PROPERTIES[prop])

def run(dev=None):
    driver = Driver()
    platform_setup(driver)
    if dev is not None:
        driver.loop.create_task(arrive_device(driver, dev))
    driver.loop.create_task(keypress_dispatch(driver))
    driver.running = True
    #driver.loop.set_debug(True)
    driver.loop.run_forever()
    driver.loop.close()
