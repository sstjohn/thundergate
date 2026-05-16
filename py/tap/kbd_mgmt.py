import logging
logger = logging.getLogger(__name__)

import sys

import asyncio

from .platform_fun import wait_for_keypress

async def gui_handler(driver):
    '''launch wxwidgets gui'''
    if driver.device is not None:
        import gui
        gui.run(driver.device)
    else:
        logger.warning("can't launch gui without arrived device")

async def help_handler(driver):
    '''display keypress bindings'''
    print()
    for key in KEYPRESS_HANDLERS:
        print("%s - %s" % (key, KEYPRESS_HANDLERS[key].__doc__))
    print()

async def verbosity_handler(driver):
    '''toggle tap driver verbosity'''
    driver.verbose = not driver.verbose
    print("tap driver verbosity %s" % (
            "enabled" if driver.verbose else "disabled"))

async def quit_handler(driver):
    '''terminate tap driver execution and close device'''
    driver.running = False
    driver.loop.stop()

async def unknown_keypress_handler(key):
    print("read unknown keypress '%s'" % key)

KEYPRESS_HANDLERS = {
    'g': gui_handler,
    'h': help_handler,
    'q': quit_handler,
    'v': verbosity_handler,
}

async def keypress_dispatch(driver):
    key = await (driver.loop.run_in_executor(None, wait_for_keypress, driver))
    if key in KEYPRESS_HANDLERS:
        asyncio.ensure_future(KEYPRESS_HANDLERS[key](driver))
    else:
        asyncio.ensure_future(unknown_keypress_handler(key))
    asyncio.ensure_future(keypress_dispatch(driver))

