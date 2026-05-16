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

#include <os/log.h>

#include <DriverKit/IOLib.h>
#include <DriverKit/IOUserClient.h>
#include <DriverKit/IOMemoryDescriptor.h>
#include <PCIDriverKit/PCIDriverKit.h>

#include "TGPCIDevice.h"

#define TGLog(fmt, ...)  os_log(OS_LOG_DEFAULT, "TGDext: " fmt, ##__VA_ARGS__)

/* PCI command register (config offset 0x04). */
#define kPCICommandOffset       0x04
#define kPCICommandMemorySpace  0x0002
#define kPCICommandBusMaster    0x0004

struct TGPCIDevice_IVars
{
    IOPCIDevice        * pci;
    IOMemoryDescriptor * bar0;
    uint64_t             bar0Size;
    uint8_t              bar0Index;
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

kern_return_t
IMPL(TGPCIDevice, Start)
{
    kern_return_t ret;
    uint8_t       barType = 0;
    uint16_t      command = 0;

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

    /* Locate BAR 0 and keep an IOMemoryDescriptor for it. */
    ret = ivars->pci->GetBARInfo(0, &ivars->bar0Index, &ivars->bar0Size,
                                 &barType);
    if (ret != kIOReturnSuccess) {
        TGLog("Start: GetBARInfo(0) failed 0x%x", ret);
        goto fail;
    }

    ret = ivars->pci->_CopyDeviceMemoryWithIndex(ivars->bar0Index,
                                                 &ivars->bar0, this);
    if (ret != kIOReturnSuccess) {
        TGLog("Start: copying BAR0 memory failed 0x%x", ret);
        goto fail;
    }

    TGLog("Start: ok -- BAR0 is %llu bytes", ivars->bar0Size);
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
    OSSafeReleaseNULL(ivars->bar0);
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

kern_return_t
IMPL(TGPCIDevice, ConfigRead32)
{
    if (ivars->pci == nullptr)
        return kIOReturnNotReady;
    return ivars->pci->ConfigurationRead32(offset, value);
}

kern_return_t
IMPL(TGPCIDevice, ConfigWrite32)
{
    if (ivars->pci == nullptr)
        return kIOReturnNotReady;
    return ivars->pci->ConfigurationWrite32(offset, value);
}

kern_return_t
IMPL(TGPCIDevice, GetBAR0Size)
{
    *size = ivars->bar0Size;
    return kIOReturnSuccess;
}

kern_return_t
IMPL(TGPCIDevice, CopyBAR0Memory)
{
    if (ivars->bar0 == nullptr)
        return kIOReturnNotReady;
    ivars->bar0->retain();          /* balanced by the caller's release */
    *memory = ivars->bar0;
    return kIOReturnSuccess;
}
