from ctypes import sizeof
import logging
logger = logging.getLogger(__name__)

import asyncio

import tglib as tg
import tg_bringup

msleep = lambda t: asyncio.sleep(t / 1000.0)


def __init_xx_ring(mm, bdtype):
    ring_len = min(mm.page_sz // sizeof(bdtype), 512)

    for i in range(4):
        ring_len |= (ring_len >> (2 ** i))
    ring_len = ring_len - (ring_len >> 1)

    va = mm.alloc(ring_len * sizeof(bdtype))
    return (va, ring_len)


async def _rx_ring_setup(driver):
    mm = driver.device.interface.mm

    rx_ring_va, rx_ring_size = __init_xx_ring(mm, tg.rbd)
    rx_ring_pa = mm.get_paddr(rx_ring_va)
    logger.debug('allocated std rx ring of length %d at %x',
                 rx_ring_size, rx_ring_va)

    regflags = {
        'mini_rcb': {'disable_ring': 1},
        'std_rcb': {
            'host_addr_hi': (rx_ring_pa >> 32),
            'host_addr_low': (rx_ring_pa & 0xffffffff),
            'ring_size': rx_ring_size,
            'max_frame_len': 0x600,
            'nic_addr': 0x6000,
            'disable_ring': 0,
        },
        'jumbo_rcb': {'disable_ring': 1},
    }
    tg_bringup.prepare_block(driver.device.rdi, regflags)


async def arrive_device(driver, dev):
    logger.info("device arrival initiated")

    driver.device = dev

    dev.init()
    dev.nvram.acquire_lock()
    dev.reset()
    await msleep(0.5)

    tg_bringup.configure_device(dev, driver)
    await _rx_ring_setup(driver)

    logger.info("device arrival concluded")
