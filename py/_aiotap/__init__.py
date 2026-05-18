"""Asyncio rework of _tap's TapDriver with a macOS feth/BPF/NDRV backend.
Linux, Windows and macOS; the default `main.py -d` driver on macOS."""

from .driver import TapDriver


def run(dev):
    with TapDriver(dev) as tap:
        return tap.run()
