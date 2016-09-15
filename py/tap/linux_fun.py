from contextlib import closing
import fcntl
import logging
import os
import socket
import struct
import sys
import termios

import trollius as asyncio

from tunlib import IFF_TAP, IFF_NO_PI, TUNSETIFF

logger = logging.getLogger(__name__)

def platform_setup(driver):
    driver.loop = asyncio.get_event_loop()
    driver.kbd_h = sys.stdin.fileno()

def create_tap(driver):
    fd = os.open("/dev/net/tun", os.O_RDWR)
    ifr = struct.pack('16sH', '', IFF_TAP | IFF_NO_PI)
    name = struct.unpack('16sH', fcntl.ioctl(fd, TUNSETIFF, ifr))[0]
    logger.info("tap device name: %s", name)
    driver.tap_h, driver.tap_name = fd, name

def wait_for_keypress(driver):
    if not driver.running:
        return
    orig_term = termios.tcgetattr(driver.kbd_h)
    new_term = orig_term[:]
    new_term[3] &= ~(termios.ICANON | termios.ECHO)
    termios.tcsetattr(driver.kbd_h, termios.TCSANOW, new_term)
    try:
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(driver.kbd_h, termios.TCSANOW, orig_term)

def _register_fd_callback(handle, driver, callback):
    if not driver.running:
        return
    driver.loop.add_reader(handle, callback, driver)

def register_interrupt_callback(driver, callback):
    if not hasattr(driver.device.interface.eventfd):
        raise NotImplementedError
    _register_fd_callback(driver.device.interface.eventfd, driver, callback)

def register_tapin_callback(driver, callback):
    _register_fd_callback(driver.tap_h, driver, callback)

def update_tapdev_status(driver):
    with closing(socket.socket()) as s:
        ifr = struct.pack('16sH', driver.tap_name, 0)
        r = fcntl.ioctl(s, SIOCGIFFLAGS, ifr)
        flags = struct.unpack('16sH', r)[1]

        if driver.connected:
            flags |= IFF_UP
        else:
            flags &= ~IFF_UP

        ifr = struct.flags('16sH', driver.tap_name, flags)
        fcntl.ioctl(s, SIOCSIFFLAGS, ifr)

