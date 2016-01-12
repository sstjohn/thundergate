/*
*  ThunderGate - an open source toolkit for PCI bus exploration
*  Copyright (C) 2015-2016 Saul St. John
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

#include "driver.h"

#ifdef ALLOC_PRAGMA
#pragma alloc_text (PAGE, tgwinkQueueInitialize)
#endif

NTSTATUS
tgwinkQueueInitialize(
    _In_ WDFDEVICE Device
    )
{
    NTSTATUS status;
    WDF_IO_QUEUE_CONFIG    queueConfig;
    PDEVICE_CONTEXT deviceContext;
    PAGED_CODE();
    
    WDF_IO_QUEUE_CONFIG_INIT_DEFAULT_QUEUE(
         &queueConfig,
        WdfIoQueueDispatchSequential
        );

    queueConfig.EvtIoDeviceControl = tgwinkEvtIoDeviceControl;
    queueConfig.EvtIoStop = tgwinkEvtIoStop;
    queueConfig.EvtIoRead = tgwinkEvtIoRead;
    queueConfig.EvtIoWrite = tgwinkEvtIoWrite;

    deviceContext = DeviceGetContext(Device);

    status = WdfIoQueueCreate(
                 Device,
                 &queueConfig,
                 WDF_NO_OBJECT_ATTRIBUTES,
                 &deviceContext->IoDefaultQueue
                 );

    WDF_IO_QUEUE_CONFIG_INIT(&queueConfig, WdfIoQueueDispatchManual);
    status = WdfIoQueueCreate(
        Device,
        &queueConfig,
        WDF_NO_OBJECT_ATTRIBUTES,
        &deviceContext->NotificationQueue);

    return status;
}

VOID
tgwinkEvtIoDeviceControl(
    _In_ WDFQUEUE Queue,
    _In_ WDFREQUEST Request,
    _In_ size_t OutputBufferLength,
    _In_ size_t InputBufferLength,
    _In_ ULONG IoControlCode
    )
{
    WDFMEMORY mem;
    NTSTATUS status;
    WDFDEVICE dev;
    PDEVICE_CONTEXT context;
    void *uBase = NULL;
    LARGE_INTEGER offset;
    size_t size;

    dev = WdfIoQueueGetDevice(Queue);
    context = DeviceGetContext(dev);

    switch (IoControlCode) {
    case IOCTL_TGWINK_SAY_HELLO:
        
        if (OutputBufferLength != 4) {
            WdfRequestComplete(Request, STATUS_BAD_DATA);
            break;
        }

        status = WdfRequestRetrieveOutputMemory(Request, &mem);
        if (!NT_SUCCESS(status)) {
            KdPrint("tgwinkEvtIoDeviceControl could not get request memory buffer, status 0x%x\n", status);
            WdfVerifierDbgBreakPoint();
            WdfRequestComplete(Request, status);
            break;
        }

        *((DWORD32 *)(WdfMemoryGetBuffer(mem, NULL))) = 0x5a5aa5a5;
        WdfRequestComplete(Request, STATUS_SUCCESS);
        break;

    case IOCTL_TGWINK_MAP_BAR_0:
        if (sizeof(void *) > OutputBufferLength) {
            KdPrint("tgwinkEvtIoDeviceControl needs a larger buffer (%d > %d)!\n", sizeof(void *), OutputBufferLength);
            WdfRequestComplete(Request, STATUS_BUFFER_TOO_SMALL);
            break;
        }

        offset = context->bar[0].phyAddr;
        size = context->bar[0].length;

        status = ZwMapViewOfSection(context->hMemory, ZwCurrentProcess(), &uBase, 0, 0, &offset, &size, ViewUnmap, 0, PAGE_READWRITE);
        if (!NT_SUCCESS(status)) {

            KdPrint("tgwinkEvtIoDeviceControl could not map view of section, status ");
            switch (status) {
            case STATUS_CONFLICTING_ADDRESSES: 
                KdPrint("STATUS_CONFLICTING_ADDRESSES\n"); 
                break;
            case STATUS_INVALID_PAGE_PROTECTION: 
                KdPrint("STATUS_INVALID_PAGE_PROTECTION\n"); 
                break;
            case STATUS_SECTION_PROTECTION: 
                KdPrint("STATUS_SECTION_PROTECTION\n"); 
                break;
            default: 
                KdPrint("0x % x\n", status); 
                break;
            }
            WdfRequestComplete(Request, status);
            break;
        }

        status = WdfRequestRetrieveOutputMemory(Request, &mem);
        if (!NT_SUCCESS(status)) {
            KdPrint("tgwinkEvtIoDeviceControl could not get request memory buffer, status 0x%x\n", status);
            WdfVerifierDbgBreakPoint();
            WdfRequestComplete(Request, status);
            break;
        }

        *((void **)(WdfMemoryGetBuffer(mem, NULL))) = uBase;

        WdfRequestComplete(Request, STATUS_SUCCESS);
        break;

    case IOCTL_TGWINK_READ_PHYS:
    {
        PVOID buf;
        ULONG_PTR page, ofs, vtgt = 0;
        SIZE_T vsz = 0;

        if (InputBufferLength != sizeof(PVOID)) {
            KdPrint("tgwinkEvtIoDeviceControl requires a %d-byte buffer for this ioctl (got %d)\n", sizeof(PVOID), OutputBufferLength);
            WdfRequestComplete(Request, STATUS_INSUFFICIENT_RESOURCES);
            break;
        }
        
        status = WdfRequestRetrieveInputBuffer(Request, sizeof(PVOID), &buf, NULL);
        if (!NT_SUCCESS(status)) {
            KdPrint("tgwinkEvtIoDeviceControl could not get request memory buffer, status 0x%x\n", status);
            WdfRequestComplete(Request, status);
            break;
        }

        ofs = *((ULONG_PTR *)buf);
        page = ofs & ~0xfff;
        vsz = OutputBufferLength + (page ^ ofs);
        buf = NULL;

        status = WdfRequestRetrieveOutputMemory(Request, &mem);
        if (!NT_SUCCESS(status)) {
            KdPrint("tgwinkEvtIoDeviceControl could not get request memory buffer, status 0x%x\n", status);
            WdfRequestComplete(Request, status);
            break;
        }

        status = ZwMapViewOfSection(context->hMemory, (HANDLE)-1, (PVOID *)&vtgt, 0, 0, (PLARGE_INTEGER)&page, &vsz, ViewUnmap, 0, PAGE_READONLY);
        if (!NT_SUCCESS(status)) {
            KdPrint("tgwinkEvtIoDeviceControl could not map view of physical memory section, status 0x%x\n", status);
            WdfRequestComplete(Request, status);
            break;
        }

        ofs -= page;
        status = WdfMemoryCopyFromBuffer(mem, 0, (PVOID)(vtgt + ofs), OutputBufferLength);
        if (!NT_SUCCESS(status)) {
            KdPrint("tgwinkEvtIoDeviceControl failed to copy data from memory to buffer, status 0x%x\n", status);
            WdfRequestComplete(Request, status);
            break;
        }

        status = ZwUnmapViewOfSection((HANDLE)-1, (PVOID)vtgt);
        if (!NT_SUCCESS(status)) {
            KdPrint("tgwinkEvtIoDeviceControl failed to unmap view of physical memory section, status 0x%x\n", status);
            WdfRequestComplete(Request, status);
            break;
        }
    
        WdfRequestCompleteWithInformation(Request, STATUS_SUCCESS, OutputBufferLength);
    } break;

    case IOCTL_TGWINK_PEND_INTR:
    {
        WdfWaitLockAcquire(context->nnLock, NULL);
        if (context->notifyNext) {
            PINTERRUPT_CONTEXT pCtx = InterruptGetContext(context->hIrq);
            status = WdfRequestRetrieveOutputMemory(Request, &mem);
            if (!NT_SUCCESS(status)) {
                KdPrint("tgwinkEvtIoDeviceControl failed to retrieve output memory, status 0x%x\n", status);
                WdfRequestComplete(Request, status);
            }
            status = WdfMemoryCopyFromBuffer(mem, 0, &pCtx->serial, 8);
            if (!NT_SUCCESS(status)) {
                KdPrint("tgwinkEvtIoDeviceControl failed to copy interrupt number to buffer, status 0x%x\n", status);
                WdfRequestComplete(Request, status);
            }
            WdfRequestCompleteWithInformation(Request, STATUS_SUCCESS, 8);
            context->notifyNext = 0;
            KdPrint("tgwinkEvtIoDeviceControl satisfied interrupt notification request synchronously.\n");
            WdfInterruptEnable(context->hIrq);
        } else {
            KdPrint("tgwinkEvtIoDeviceControl forwarding PEND_INTR request to notification queue\n");
            WdfRequestForwardToIoQueue(Request, context->NotificationQueue);
        }
        WdfWaitLockRelease(context->nnLock);
    } break;

    default:
        WdfRequestComplete(Request, STATUS_UNSUCCESSFUL);
    }
}

VOID
tgwinkEvtIoStop(
    _In_ WDFQUEUE Queue,
    _In_ WDFREQUEST Request,
    _In_ ULONG ActionFlags
    )
{
    UNREFERENCED_PARAMETER(Queue);
    UNREFERENCED_PARAMETER(Request);
    UNREFERENCED_PARAMETER(ActionFlags);
}

VOID 
tgwinkEvtIoWrite(
    WDFQUEUE Queue,
    WDFREQUEST Request,
    size_t Length
    )
{
    NTSTATUS status;
    WDFMEMORY mem;
    WDF_REQUEST_PARAMETERS params;
    ULONG offset;
    ULONG result;
    PDEVICE_CONTEXT context;
    WDFDEVICE device;
    
    device = WdfIoQueueGetDevice(Queue);
    context = DeviceGetContext(device);

    WDF_REQUEST_PARAMETERS_INIT(&params);

    WdfRequestGetParameters(Request, &params);

    offset = (ULONG)params.Parameters.Write.DeviceOffset;
    
    status = WdfRequestRetrieveInputMemory(Request, &mem);
    if (!NT_SUCCESS(status)) {
        KdPrint("tgwinkEvtIoRead could not get request memory buffer, status 0x%x\n", status);
        WdfVerifierDbgBreakPoint();
        WdfRequestCompleteWithInformation(Request, status, 0);
        return;
    }

    result = context->busInterface.SetBusData(context->busInterface.Context, PCI_WHICHSPACE_CONFIG, WdfMemoryGetBuffer(mem, NULL), offset, (ULONG)Length);

    WdfRequestCompleteWithInformation(Request, STATUS_SUCCESS, (ULONG_PTR)result);
}

VOID
tgwinkEvtIoRead(
    WDFQUEUE Queue,
    WDFREQUEST Request,
    size_t Length
    )
{
    NTSTATUS status;
    WDFMEMORY mem;
    WDF_REQUEST_PARAMETERS params;
    ULONG offset;
    ULONG result;
    PDEVICE_CONTEXT context;
    WDFDEVICE device;
    
    device = WdfIoQueueGetDevice(Queue);
    context = DeviceGetContext(device);

    WDF_REQUEST_PARAMETERS_INIT(&params);

    WdfRequestGetParameters(Request, &params);

    offset = (ULONG)params.Parameters.Read.DeviceOffset;

    status = WdfRequestRetrieveOutputMemory(Request, &mem);
    if (!NT_SUCCESS(status)) {
        KdPrint("tgwinkEvtIoRead could not get request memory buffer, status 0x%x\n", status);
        WdfVerifierDbgBreakPoint();
        WdfRequestCompleteWithInformation(Request, status, 0);
        return;
    }

    result = context->busInterface.GetBusData(context->busInterface.Context, PCI_WHICHSPACE_CONFIG, WdfMemoryGetBuffer(mem, NULL), offset, (ULONG)Length);

    WdfRequestCompleteWithInformation(Request, STATUS_SUCCESS, (ULONG_PTR)result);
}


