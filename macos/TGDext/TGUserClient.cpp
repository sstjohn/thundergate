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
#include <DriverKit/OSAction.h>

#include "TGUserClient.h"
#include "TGPCIDevice.h"
#include "tg_dext.h"

#define TGLog(fmt, ...)  os_log(OS_LOG_DEFAULT, "TGDext: " fmt, ##__VA_ARGS__)

struct TGUserClient_IVars
{
    TGPCIDevice * owner;
    OSAction    * intCompletion;    /* pending kTGWaitInterrupt, if any */
};

bool
TGUserClient::init()
{
    if (!super::init())
        return false;
    ivars = IONewZero(TGUserClient_IVars, 1);
    return ivars != nullptr;
}

void
TGUserClient::free()
{
    if (ivars != nullptr)
        IOSafeDeleteNULL(ivars, TGUserClient_IVars, 1);
    super::free();
}

kern_return_t
IMPL(TGUserClient, Start)
{
    kern_return_t ret = Start(provider, SUPERDISPATCH);
    if (ret != kIOReturnSuccess)
        return ret;

    /* The provider is the TGPCIDevice that created us via Create(). */
    ivars->owner = OSDynamicCast(TGPCIDevice, provider);
    if (ivars->owner == nullptr) {
        TGLog("UserClient Start: provider is not a TGPCIDevice");
        return kIOReturnNoDevice;
    }
    ivars->owner->retain();
    ivars->owner->RegisterClient(this);
    return kIOReturnSuccess;
}

kern_return_t
IMPL(TGUserClient, Stop)
{
    if (ivars->owner != nullptr)
        ivars->owner->UnregisterClient();

    /* Fail any wait that was still outstanding. */
    if (ivars->intCompletion != nullptr) {
        AsyncCompletion(ivars->intCompletion, kIOReturnAborted, nullptr, 0);
        OSSafeReleaseNULL(ivars->intCompletion);
    }
    OSSafeReleaseNULL(ivars->owner);
    return Stop(provider, SUPERDISPATCH);
}

/*
 * ExternalMethod handles the dispatch inline: it is itself a dispatched
 * override, so `ivars` (hence `owner`) is in scope here -- no separate
 * static handler table is needed. Scalar argument counts are validated
 * by hand. Selectors are defined in tg_dext.h.
 */
/* ExternalMethod is declared LOCALONLY in IOUserClient.iig -- it is a
   plain virtual override, not an iig-dispatched (IMPL) method. */
kern_return_t
TGUserClient::ExternalMethod(uint64_t selector,
                             IOUserClientMethodArguments * arguments,
                             const IOUserClientMethodDispatch * dispatch,
                             OSObject * target,
                             void * reference)
{
    if (ivars->owner == nullptr)
        return kIOReturnNotReady;

    switch (selector) {
    case kTGConfigRead: {
        if (arguments->scalarInputCount < 1)
            return kIOReturnBadArgument;
        uint32_t value = 0;
        kern_return_t ret = ivars->owner->ConfigRead32(
            arguments->scalarInput[0], &value);
        if (ret != kIOReturnSuccess)
            return ret;
        arguments->scalarOutput[0] = value;
        arguments->scalarOutputCount = 1;
        return kIOReturnSuccess;
    }

    case kTGConfigWrite: {
        if (arguments->scalarInputCount < 2)
            return kIOReturnBadArgument;
        arguments->scalarOutputCount = 0;
        return ivars->owner->ConfigWrite32(
            arguments->scalarInput[0],
            (uint32_t)arguments->scalarInput[1]);
    }

    case kTGGetBar0Info: {
        uint64_t size = 0;
        kern_return_t ret = ivars->owner->GetRegBarSize(&size);
        if (ret != kIOReturnSuccess)
            return ret;
        arguments->scalarOutput[0] = size;
        arguments->scalarOutputCount = 1;
        return kIOReturnSuccess;
    }

    case kTGAllocDMA: {
        if (arguments->scalarInputCount < 1)
            return kIOReturnBadArgument;
        uint64_t handle = 0, iova = 0;
        kern_return_t ret = ivars->owner->AllocDMA(
            arguments->scalarInput[0], &handle, &iova);
        if (ret != kIOReturnSuccess)
            return ret;
        arguments->scalarOutput[0] = handle;
        arguments->scalarOutput[1] = iova;
        arguments->scalarOutputCount = 2;
        return kIOReturnSuccess;
    }

    case kTGFreeDMA: {
        if (arguments->scalarInputCount < 1)
            return kIOReturnBadArgument;
        arguments->scalarOutputCount = 0;
        return ivars->owner->FreeDMA(arguments->scalarInput[0]);
    }

    case kTGWaitInterrupt: {
        /*
         * Async method: the caller (IOConnectCallAsyncScalarMethod)
         * supplies a completion. Stash it; NotifyInterrupt() fires it
         * when the device next interrupts. One wait outstanding at a
         * time.
         */
        if (arguments->completion == nullptr)
            return kIOReturnBadArgument;
        if (ivars->intCompletion != nullptr)
            return kIOReturnBusy;
        ivars->intCompletion = arguments->completion;
        ivars->intCompletion->retain();
        return kIOReturnSuccess;
    }

    default:
        return super::ExternalMethod(selector, arguments, dispatch,
                                     target, reference);
    }
}

/*
 * Hands a region to the user-space IOConnectMapMemory() call:
 *   kTGMemoryBar0            -> PCI BAR 0
 *   kTGMemoryDMA + <handle>  -> the DMA buffer with that handle
 */
kern_return_t
IMPL(TGUserClient, CopyClientMemoryForType)
{
    if (ivars->owner == nullptr)
        return kIOReturnNotReady;

    if (type == kTGMemoryBar0)
        return ivars->owner->CopyRegBarMemory(memory);

    if (type >= kTGMemoryDMA && type < kTGMemoryDMA + kTGMaxDMABuffers)
        return ivars->owner->CopyDMAMemory(type - kTGMemoryDMA, memory);

    return super::CopyClientMemoryForType(type, options, memory);
}

/*
 * Invoked by TGPCIDevice on each device interrupt. Completes the pending
 * asynchronous kTGWaitInterrupt call, which wakes the TAP driver's wait
 * loop in py/interfaces/macos.py.
 */
void
IMPL(TGUserClient, NotifyInterrupt)
{
    if (ivars->intCompletion != nullptr) {
        AsyncCompletion(ivars->intCompletion, kIOReturnSuccess, nullptr, 0);
        OSSafeReleaseNULL(ivars->intCompletion);
    }
}
