import logging
logger = logging.getLogger(__name__)

import sys

import trollius as asyncio
from trollius import coroutine, From

from platform_fun import wait_for_keypress

@coroutine
def gui_handler(driver):
    '''launch wxwidgets gui'''
    if driver.device is not None:
        import gui
        gui.run(driver.device)
    else:
        logger.warn("can't launch gui without arrived device")

@coroutine
def help_handler(driver):
    '''display keypress bindings'''
    print
    for key in KEYPRESS_HANDLERS:
        print "%s - %s" % (key, KEYPRESS_HANDLERS[key].__doc__)
    print

@coroutine
def verbosity_handler(driver):
    '''toggle tap driver verbosity'''
    driver.verbose = not driver.verbose
    print "tap driver verbosity %s" % (
            "enabled" if driver.verbose else "disabled")

@coroutine
def quit_handler(driver):
    '''terminate tap driver execution and close device'''
    driver.running = False
    driver.loop.stop()

@coroutine
def unknown_keypress_handler(key):
    print "read unknown keypress '%s'" % key

KEYPRESS_HANDLERS = {
    'g': gui_handler,
    'h': help_handler,
    'q': quit_handler,
    'v': verbosity_handler,
}

@coroutine
def keypress_dispatch(driver):
    key = yield From(driver.loop.run_in_executor(None, wait_for_keypress, driver))
    if key in KEYPRESS_HANDLERS:
        asyncio.ensure_future(KEYPRESS_HANDLERS[key](driver))
    else:
        asyncio.ensure_future(unknown_keypress_handler(key))
    asyncio.ensure_future(keypress_dispatch(driver))

