import logging
logger = logging.getLogger(__name__)

import trollius as asyncio
from trollius import coroutine, From

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
                        fname = flag.replace("_", " ")
                        logger.debug("%s %s (%s.%s)",
                                     verb, fname, bname, register)
                    setattr(oreg, flag, ival)
        elif oreg != flags:
            if not silent:
                logger.debug("configuring %s.%s", bname, register)
            setattr(block, register, flags)

@coroutine
def _pci_setup(dev):
    dma_wmm = 6
    try:
        if dev.config.caps['pcie'].max_payload_size > 0:
            dma_wmm += 1
    except KeyError:
        pass

    flags = {
        'misc_host_ctrl': {
            'enable_tagged_status_mode': 1,
        },
        'dma_rw_ctrl': {
            'dma_write_watermark': dma_wmm,
            'disable_cache_alignment': 1,
        },
    }
    prepare_block(dev.pci, flags)

@coroutine
def arrive_device(dev):
    logger.info("device arrived")

    dev.init()
    dev.reset()
    yield From(msleep(0.5))

    asyncio.ensure_future(_pci_setup(dev))

