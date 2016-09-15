import sys
import termios

import trollius as asyncio

def platform_setup(driver):
    driver.loop = asyncio.get_event_loop()
    driver.kbd_h = sys.stdin.fileno()

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
