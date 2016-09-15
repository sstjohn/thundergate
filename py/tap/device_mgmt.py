from ctypes import cast, POINTER, sizeof
import logging
logger = logging.getLogger(__name__)

import trollius as asyncio
from trollius import coroutine, From

import tglib as tg

msleep = lambda t: asyncio.sleep(t / 1000.0)

def prepare_block(block, registerflags, silent=False):
    bname = block.block_name
    for register in registerflags:
        flags = registerflags[register]
        oreg = getattr(block, register)
        if isinstance(flags, dict):
            for flag in flags:
                ival = flags[flag]
                cval = getattr(oreg, flag)
                if cval != ival:
                    if not silent:
                        if ival > 1:
                            verb = "configuring"
                        elif ival:
                            verb = "setting"
                        else:
                            verb = "clearing"
                        logger.debug("%s %s in %s.%s",
                                     verb, flag, bname, register)
                    setattr(oreg, flag, ival)
        else:
            if not silent:
                logger.debug("configuring %s.%s", bname, register)
            setattr(block, register, flags)

@coroutine
def _pci_setup(driver):
    dma_wmm = 6
    try:
        if driver.device.config.caps['pcie'].max_payload_size > 0:
            dma_wmm += 1
    except KeyError:
        pass

    regflags = {
        'misc_host_ctrl': {
            'enable_tagged_status_mode': 1,
        },
        'dma_rw_ctrl': {
            'dma_write_watermark': dma_wmm,
            'disable_cache_alignment': 1,
        },
    }
    prepare_block(driver.device.pci, regflags)

@coroutine
def _msi_setup(driver):
    regflags = {'mode': {'msix_multi_vector_mode': 0}}
    prepare_block(driver.device.msi, regflags)

@coroutine
def _hc_setup(driver):
    mm = driver.device.interface.mm
    driver.device.hc.block_disable()

    status_block_va = mm.alloc(sizeof(tg.status_block))
    driver.status_block = cast(status_block_va, POINTER(tg.status_block))[0]
    status_block_pa = mm.get_paddr(status_block_va)

    regflags = {
        'rx_coal_ticks': 0x48,
        'tx_coal_ticks': 0x14,
        'rx_max_coal_bds': 0x05,
        'tx_max_coal_bds': 0x35,
        'rx_max_coal_bds_in_int': 0x05,
        'tx_max_coal_bds_in_int': 0x05,
    }
    
    driver.device.hc.status_block_host_addr_hi = status_block_pa >> 32
    driver.device.hc.status_block_host_addr_low = status_block_pa & 0xffffffff

    prepare_block(driver.device.hc, regflags)

    logger.debug("status block initialized at %x", status_block_va)

@coroutine
def _grc_setup(driver):
    regflags = {
        'misc_local_control': {
            'interrupt_on_attention': 1,
            'auto_seeprom': 1,
        },
        'misc_config': {'timer_prescaler': 0x41},
        'mode': {
            'host_send_bds': 1,
            'send_no_pseudo_header_cksum': 1,
            'host_stack_up': 1,
        },
    }
    prepare_block(driver.device.grc, regflags)

@coroutine
def _bufman_setup(driver):
    regflags = {
        'dma_mbuf_low_watermark': {'count': 0x2a},
        'mbuf_high_watermark': {'count': 0xa0},
        'mode': {'attention_enable': 1},
    }
    prepare_block(driver.device.bufman, regflags)

@coroutine
def _emac_setup(driver):
    regflags = {
        'mode': {'port_mode': 2},
        'low_watermark_max_receive_frame': { 'count': 1},
    }
    prepare_block(driver.device.emac, regflags)

@coroutine
def _rbdi_setup(driver):
    regflags = {
        'std_ring_replenish_threshold': {'count': 0x19},
    }
    prepare_block(driver.device.rbdi, regflags)

def __init_xx_ring(mm, bdtype):
    ring_len = min(mm.page_sz / sizeof(bdtype), 512)

    for i in range(4):
        ring_len |= (ring_len >> (2 ** i))
    ring_len = ring_len - (ring_len >> 1)

    va = mm.alloc(ring_len * sizeof(bdtype))
    return (va, ring_len)

@coroutine
def _rx_ring_setup(driver):
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
    prepare_block(driver.device.rdi, regflags)

@coroutine
def arrive_device(driver, dev):
    logger.info("device arrival initiated")
    
    driver.device = dev

    dev.init()
    dev.nvram.acquire_lock()
    dev.reset()
    yield From(msleep(0.5))

    setup_steps = [
        _pci_setup,
        _msi_setup,
        _hc_setup,
        _grc_setup,
        _bufman_setup,
        _emac_setup,
        _rbdi_setup,
        _rx_ring_setup,
    ]

    tasks = []
    for step in setup_steps:
        tasks += [asyncio.ensure_future(step(driver))]

    try:
        asyncio.wait(tasks)
    except Exception:
        print "there was an exception!"
    logger.info("device arrival concluded")
