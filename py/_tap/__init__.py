"""Synchronous TAP driver: a select() loop around a TapDriver with per-OS
backends. Linux and Windows. `testdrv.py` (`main.py -t`) also uses it."""

from .driver import TapDriver


def run(dev):
    with TapDriver(dev) as tap:
        return tap.run()
