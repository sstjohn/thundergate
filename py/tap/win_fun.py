import logging
logger = logging.getLogger(__name__)

import trollius as asyncio

from winlib import INPUT_RECORD, DWORD, ReadConsoleInput, pointer, WinError

def platform_setup(driver):
    driver.loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(driver.loop)
    driver.kbd_h = ??

def wait_for_keypress(driver):
    input_rec = INPUT_RECORD()
    rec_count = DWORD(0)
    while (driver.running and
           (input_rec.EventType != 1 or
            not input_rec.Event.KeyEvent.bKeyDown)):
        if not ReadConsoleInput(driver.kbd_h,
                                pointer(input_rec),
                                1,
                                pointer(rec_count)):
            raise WinError()
    return input_rec.Event.KeyEvent.uChar.AsciiChar

