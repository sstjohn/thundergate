"""Asyncio TAP driver, built as a Driver object running cooperative tasks.
Linux and Windows; the default `main.py -d` driver there."""

from .main_loop import run
