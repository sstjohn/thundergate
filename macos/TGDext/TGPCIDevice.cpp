/*
 *  ThunderGate - an open source toolkit for PCI bus exploration
 *  Copyright (C) 2015-2026  Saul St. John
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <string.h>
#include <os/log.h>

#include <DriverKit/IOLib.h>
#include <DriverKit/IOUserClient.h>
#include <DriverKit/IOMemoryDescriptor.h>
#include <DriverKit/IOBufferMemoryDescriptor.h>
#include <DriverKit/IODMACommand.h>
#include <DriverKit/IODispatchQueue.h>
#include <DriverKit/IOInterruptDispatchSource.h>
#include <DriverKit/OSAction.h>
#include <PCIDriverKit/PCIDriverKit.h>

#include "TGPCIDevice.h"
#include "TGUserClient.h"
#include "tg_dext.h"

#define TGLog(fmt, ...)  os_log(OS_LOG_DEFAULT, "TGDext: " fmt, ##__VA_ARGS__)

/* PCI command register (config offset 0x04). */
#define kPCICommandOffset       0x04
#define kPCICommandMemorySpace  0x0002
#define kPCICommandBusMaster    0x0004

struct TGDMASlot
{
    IOBufferMemoryDescriptor * buffer;
    IODMACommand             * dma;
    uint64_t                   iova;
    uint64_t                   size;
};

struct TGPCIDevice_IVars
{
    IOPCIDevice               * pci;
    IOMemoryDescriptor        * regBar;
    uint64_t                    regBarSize;
    uint8_t                     regBarIndex;

    /* MSI interrupt -> the registered user client. */
    IOInterruptDispatchSource * intSource;
    OSAction                  * intAction;
    IOUserClient              * client;
    uint64_t                    intCount;

    TGDMASlot                   dmaSlots[kTGMaxDMABuffers];
};

bool
TGPCIDevice::init()
{
    if (!super::init())
        return false;
    ivars = IONewZero(TGPCIDevice_IVars, 1);
    return ivars != nullptr;
}

void
TGPCIDevice::free()
{
    if (ivars != nullptr)
        IOSafeDeleteNULL(ivars, TGPCIDevice_IVars, 1);
    super::free();
}

/* ====================================================================== */
/* lifecycle                                                              */
/* ====================================================================== */

kern_return_t
IMPL(TGPCIDevice, Start)
{
    kern_return_t     ret;
    uint16_t          command = 0;
    IODispatchQueue * queue   = nullptr;

    ret = Start(provider, SUPERDISPATCH);
    if (ret != kIOReturnSuccess)
        return ret;

    ivars->pci = OSDynamicCast(IOPCIDevice, provider);
    if (ivars->pci == nullptr) {
        TGLog("Start: provider is not an IOPCIDevice");
        Stop(provider, SUPERDISPATCH);
        return kIOReturnNoDevice;
    }
    ivars->pci->retain();

    ret = ivars->pci->Open(this, 0);
    if (ret != kIOReturnSuccess) {
        TGLog("Start: Open() failed 0x%x", ret);
        OSSafeReleaseNULL(ivars->pci);
        Stop(provider, SUPERDISPATCH);
        return ret;
    }

    /* Enable memory-space decoding and bus mastering. */
    ivars->pci->ConfigurationRead16(kPCICommandOffset, &command);
    command |= (kPCICommandMemorySpace | kPCICommandBusMaster);
    ivars->pci->ConfigurationWrite16(kPCICommandOffset, command);

    /* Locate the register BAR and keep an IOMemoryDescriptor for it.
       The Tigon3's register block is NOT always at BAR index 0 -- a
       stock Apple Thunderbolt-Ethernet adapter presents it at BAR 2
       (our own firmware enables BAR 0, but the stock one does not). So
       scan BAR0..BAR5 for the first memory BAR of non-zero size,
       rather than assuming index 0. A 64-bit BAR's high half
       reports size 0 and is skipped. */
    ret = kIOReturnNotFound;
    for (uint8_t bar = 0; bar < 6; bar++) {     /* BAR0..BAR5, no expansion ROM */
        uint8_t  mIndex = 0;
        uint64_t mSize  = 0;
        uint8_t  bType  = 0;
        if (ivars->pci->GetBARInfo(bar, &mIndex, &mSize, &bType)
                != kIOReturnSuccess || mSize == 0)
            continue;
        /* must be an MMIO BAR: bit 0 of the BAR type is the PCI
           I/O-space indicator (1 = I/O port, 0 = memory). */
        if (bType & 1)
            continue;
        ivars->regBarIndex = mIndex;
        ivars->regBarSize  = mSize;
        ret = kIOReturnSuccess;
        TGLog("Start: register BAR %u -> memory index %u, %llu bytes",
              bar, mIndex, mSize);
        break;
    }
    if (ret != kIOReturnSuccess) {
        TGLog("Start: no usable memory BAR found");
        goto fail;
    }
    ret = ivars->pci->_CopyDeviceMemoryWithIndex(ivars->regBarIndex,
                                                 &ivars->regBar, this);
    if (ret != kIOReturnSuccess) {
        TGLog("Start: copying BAR memory failed 0x%x", ret);
        goto fail;
    }

    /*
     * Route the device's (MSI) interrupt through a dispatch source.
     * interruptIndex 0 is the device's first message-signalled
     * interrupt; PCIDriverKit allocates it.
     */
    ret = CopyDispatchQueue("Default", &queue);
    if (ret == kIOReturnSuccess && queue != nullptr) {
        ret = IOInterruptDispatchSource::Create(ivars->pci, 0, queue,
                                                &ivars->intSource);
        OSSafeReleaseNULL(queue);
        if (ret == kIOReturnSuccess) {
            ret = CreateActionInterruptOccurred(0, &ivars->intAction);
            if (ret == kIOReturnSuccess) {
                ivars->intSource->SetHandler(ivars->intAction);
                ivars->intSource->SetEnable(true);
            }
        }
    }
    if (ret != kIOReturnSuccess) {
        /* The flash path does not need interrupts -- warn, don't fail. */
        TGLog("Start: interrupt setup failed 0x%x (flashing still works)",
              ret);
        OSSafeReleaseNULL(ivars->intAction);
        OSSafeReleaseNULL(ivars->intSource);
    }

    TGLog("Start: ok -- register BAR is %llu bytes", ivars->regBarSize);
    RegisterService();
    return kIOReturnSuccess;

fail:
    ivars->pci->Close(this, 0);
    OSSafeReleaseNULL(ivars->pci);
    Stop(provider, SUPERDISPATCH);
    return ret;
}

kern_return_t
IMPL(TGPCIDevice, Stop)
{
    if (ivars->intSource != nullptr) {
        ivars->intSource->SetEnable(false);
        OSSafeReleaseNULL(ivars->intSource);
    }
    OSSafeReleaseNULL(ivars->intAction);
    OSSafeReleaseNULL(ivars->client);

    for (int i = 0; i < kTGMaxDMABuffers; i++)
        FreeDMA((uint64_t)i);

    OSSafeReleaseNULL(ivars->regBar);
    if (ivars->pci != nullptr) {
        ivars->pci->Close(this, 0);
        OSSafeReleaseNULL(ivars->pci);
    }
    return Stop(provider, SUPERDISPATCH);
}

kern_return_t
IMPL(TGPCIDevice, NewUserClient)
{
    kern_return_t ret;
    IOService *   created = nullptr;

    (void)type;

    ret = Create(this, "UserClientProperties", &created);
    if (ret != kIOReturnSuccess) {
        TGLog("NewUserClient: Create() failed 0x%x", ret);
        return ret;
    }

    *userClient = OSDynamicCast(IOUserClient, created);
    if (*userClient == nullptr) {
        TGLog("NewUserClient: created object is not an IOUserClient");
        OSSafeReleaseNULL(created);
        return kIOReturnError;
    }
    return kIOReturnSuccess;
}

/* ====================================================================== */
/* config space + register BAR                                            */
/* ====================================================================== */

kern_return_t
IMPL(TGPCIDevice, ConfigRead32)
{
    if (ivars->pci == nullptr)
        return kIOReturnNotReady;
    ivars->pci->ConfigurationRead32(offset, value);   /* returns void */
    return kIOReturnSuccess;
}

kern_return_t
IMPL(TGPCIDevice, ConfigWrite32)
{
    if (ivars->pci == nullptr)
        return kIOReturnNotReady;
    ivars->pci->ConfigurationWrite32(offset, value);  /* returns void */
    return kIOReturnSuccess;
}

kern_return_t
IMPL(TGPCIDevice, GetRegBarSize)
{
    *size = ivars->regBarSize;
    return kIOReturnSuccess;
}

kern_return_t
IMPL(TGPCIDevice, CopyRegBarMemory)
{
    if (ivars->regBar == nullptr)
        return kIOReturnNotReady;
    ivars->regBar->retain();          /* balanced by the caller's release */
    *memory = ivars->regBar;
    return kIOReturnSuccess;
}

/* ====================================================================== */
/* DMA buffers                                                  */
/* ====================================================================== */

kern_return_t
IMPL(TGPCIDevice, AllocDMA)
{
    kern_return_t            ret;
    int                      slot = -1;
    IOBufferMemoryDescriptor * buf = nullptr;
    IODMACommand             * dma = nullptr;
    IODMACommandSpecification  spec;
    IOAddressSegment           seg[32];   /* PrepareForDMA writes up to 32 */
    uint64_t                   dmaFlags = 0;
    uint32_t                   segCount = 32;

    for (int i = 0; i < kTGMaxDMABuffers; i++) {
        if (ivars->dmaSlots[i].buffer == nullptr) { slot = i; break; }
    }
    if (slot < 0)
        return kIOReturnNoResources;

    /* A DMA-capable, page-aligned buffer. */
    ret = IOBufferMemoryDescriptor::Create(kIOMemoryDirectionInOut, size,
                                           4096, &buf);
    if (ret != kIOReturnSuccess || buf == nullptr)
        return (ret != kIOReturnSuccess) ? ret : kIOReturnNoMemory;

    /* Map it for the device and obtain a single contiguous IOVA. */
    memset(&spec, 0, sizeof(spec));
    spec.maxAddressBits = 64;
    ret = IODMACommand::Create(ivars->pci, 0, &spec, &dma);
    if (ret != kIOReturnSuccess) {
        OSSafeReleaseNULL(buf);
        return ret;
    }

    memset(seg, 0, sizeof(seg));
    ret = dma->PrepareForDMA(0, buf, 0, size, &dmaFlags, &segCount, seg);
    if (ret != kIOReturnSuccess || segCount != 1) {
        TGLog("AllocDMA: PrepareForDMA failed 0x%x segs=%u", ret, segCount);
        OSSafeReleaseNULL(dma);
        OSSafeReleaseNULL(buf);
        return (ret != kIOReturnSuccess) ? ret : kIOReturnNotAligned;
    }

    ivars->dmaSlots[slot].buffer = buf;
    ivars->dmaSlots[slot].dma    = dma;
    ivars->dmaSlots[slot].iova   = seg[0].address;
    ivars->dmaSlots[slot].size   = size;

    *handle = (uint64_t)slot;
    *iova   = seg[0].address;
    return kIOReturnSuccess;
}

kern_return_t
IMPL(TGPCIDevice, FreeDMA)
{
    if (handle >= kTGMaxDMABuffers)
        return kIOReturnBadArgument;

    TGDMASlot * s = &ivars->dmaSlots[handle];
    if (s->buffer == nullptr)
        return kIOReturnSuccess;        /* already free -- idempotent */

    if (s->dma != nullptr) {
        s->dma->CompleteDMA(kIODMACommandCompleteDMANoOptions);
        OSSafeReleaseNULL(s->dma);
    }
    OSSafeReleaseNULL(s->buffer);
    s->iova = 0;
    s->size = 0;
    return kIOReturnSuccess;
}

kern_return_t
IMPL(TGPCIDevice, CopyDMAMemory)
{
    if (handle >= kTGMaxDMABuffers)
        return kIOReturnBadArgument;

    IOBufferMemoryDescriptor * buf = ivars->dmaSlots[handle].buffer;
    if (buf == nullptr)
        return kIOReturnNotFound;

    buf->retain();                      /* balanced by the caller's release */
    *memory = buf;
    return kIOReturnSuccess;
}

/* ====================================================================== */
/* interrupts                                                   */
/* ====================================================================== */

kern_return_t
IMPL(TGPCIDevice, RegisterClient)
{
    OSSafeReleaseNULL(ivars->client);
    ivars->client = client;
    if (ivars->client != nullptr)
        ivars->client->retain();
    return kIOReturnSuccess;
}

kern_return_t
IMPL(TGPCIDevice, UnregisterClient)
{
    OSSafeReleaseNULL(ivars->client);
    return kIOReturnSuccess;
}

void
IMPL(TGPCIDevice, InterruptOccurred)
{
    (void)action;
    (void)count;
    (void)time;

    ivars->intCount++;
    if (ivars->client != nullptr) {
        TGUserClient * uc = OSDynamicCast(TGUserClient, ivars->client);
        if (uc != nullptr)
            uc->NotifyInterrupt();
    }
}
