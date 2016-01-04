/*
*  ThunderGate - an open source toolkit for PCI bus exploration
*  Copyright (C) 2015  Saul St. John
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
#pragma alloc_text (PAGE, tgwinkCreateDevice)
#pragma alloc_text (PAGE, tgwinkPrepareHardware)
#pragma alloc_text (PAGE, tgwinkReleaseHardware)
#pragma alloc_text (PAGE, tgwinkDeviceContextCleanup)
#endif

NTSTATUS
tgwinkPrepareHardware(
	_In_ WDFDEVICE Device,
	_In_ WDFCMRESLIST Resources,
	_In_ WDFCMRESLIST ResourcesTranslated
	)
{
	PCM_PARTIAL_RESOURCE_DESCRIPTOR desc;
	DEVICE_CONTEXT *context;
	int barSeen = 0;
	NTSTATUS result;
	
	PAGED_CODE();

	context = DeviceGetContext(Device);

	for (unsigned i = 0; i < WdfCmResourceListGetCount(ResourcesTranslated); i++) {
		desc = WdfCmResourceListGetDescriptor(ResourcesTranslated, i);

		switch (desc->Type) {
		
		case CmResourceTypePort:
			DbgBreakPoint();
			break;

		case CmResourceTypeInterrupt:
		{
			WDF_INTERRUPT_CONFIG irqConfig;
			WDF_OBJECT_ATTRIBUTES oAttrs;

			if (NULL != context->hIrq) {
				KdPrint("Ignoring another interrupt for this device!\n");
			} else {
				WDF_INTERRUPT_CONFIG_INIT(&irqConfig, &tgwinkServiceInterrupt, NULL);
				irqConfig.EvtInterruptWorkItem = &tgwinkInterruptWerk;
				irqConfig.InterruptTranslated = desc;
				irqConfig.InterruptRaw = WdfCmResourceListGetDescriptor(Resources, i);

				WDF_OBJECT_ATTRIBUTES_INIT_CONTEXT_TYPE(&oAttrs, INTERRUPT_CONTEXT);

				result = WdfInterruptCreate(Device, &irqConfig, &oAttrs, &context->hIrq);
				if (!NT_SUCCESS(result)) {
					KdPrint("Unable to create a WDFINTERRUPT object hey, status %x\n", result);
					//return result;
				}
				else {
					KdPrint("Found an interrupt-type resource!\n");
				}
			}
		} break;

		case CmResourceTypeMemory:
			ASSERT(barSeen < 2);
			
			KdPrint("Found Base Address Register-type resource #%d.\n", barSeen);
			
			context->bar[barSeen].length = desc->u.Memory.Length;
			KdPrint("  length: %d\n", desc->u.Memory.Length);
			context->bar[barSeen].phyAddr = desc->u.Memory.Start;
			KdPrint("  physical address: %08x\n", desc->u.Memory.Start);
			context->bar[barSeen].mapAddr = MmMapIoSpace(desc->u.Memory.Start, desc->u.Memory.Length, MmNonCached);
			KdPrint("  virtual address: %08x\n", context->bar[barSeen].mapAddr);
			
			desc = WdfCmResourceListGetDescriptor(Resources, i);
			context->bar[barSeen].busAddr = desc->u.Memory.Start;
			KdPrint("  bus address: %08x\n", desc->u.Memory.Start);

			barSeen++;
			break;

		case CmResourceTypeConfigData:
			KdPrint("Found ConfigData-type resource!\n");
			DbgBreakPoint();
			break;

		case CmResourceTypeDevicePrivate:
			KdPrint("Found private-type resource!\n");
			break;

		default:
			KdPrint("Found unknown resource of type %d!\n", desc->Type);
			DbgBreakPoint();
		}
	}

	if (barSeen != 2)
		return STATUS_BAD_DATA;
	
	context->busInterface.Size = sizeof(BUS_INTERFACE_STANDARD);

	result = WdfFdoQueryForInterface(Device, &GUID_BUS_INTERFACE_STANDARD, (PINTERFACE)&context->busInterface, sizeof(BUS_INTERFACE_STANDARD), 1, NULL);

	if (!NT_SUCCESS(result)) {
		KdPrint("Failed to find BUS_INTERFACE_STANDARD in tgwinkPrepareHardware, error code %d.\n", result);
		return result;
	}

	return STATUS_SUCCESS;
}

NTSTATUS
tgwinkReleaseHardware(
	_In_ WDFDEVICE Device,
	_In_ WDFCMRESLIST ResourcesTranslated
	)
{
	DEVICE_CONTEXT *context;
	PAGED_CODE();
	UNREFERENCED_PARAMETER(ResourcesTranslated);

	context = DeviceGetContext(Device);
	for (int i = 0; i < 2; i++) {
		if (context->bar[i].mapAddr != 0) {
			MmUnmapIoSpace(context->bar[i].mapAddr, context->bar[i].length);
			context->bar[i].mapAddr = 0;
		}
	}
	
	return STATUS_SUCCESS;
}

NTSTATUS
tgwinkCreateDevice(
	_Inout_ PWDFDEVICE_INIT DeviceInit
	)
{
	WDF_OBJECT_ATTRIBUTES   fdoAttributes;
	WDFDEVICE device;
	WDF_PNPPOWER_EVENT_CALLBACKS pnpCallbacks;
	NTSTATUS status;
	PDEVICE_CONTEXT context;
	UNICODE_STRING pmemDevNam;
	OBJECT_ATTRIBUTES oAttr;

	PAGED_CODE();

	WDF_PNPPOWER_EVENT_CALLBACKS_INIT(&pnpCallbacks);
	pnpCallbacks.EvtDevicePrepareHardware = tgwinkPrepareHardware;
	pnpCallbacks.EvtDeviceReleaseHardware = tgwinkReleaseHardware;
	WdfDeviceInitSetPnpPowerEventCallbacks(DeviceInit, &pnpCallbacks);

	WdfDeviceInitSetIoType(DeviceInit, WdfDeviceIoDirect);

	WDF_OBJECT_ATTRIBUTES_INIT_CONTEXT_TYPE(&fdoAttributes, DEVICE_CONTEXT);
	fdoAttributes.SynchronizationScope = WdfSynchronizationScopeDevice;
	fdoAttributes.EvtCleanupCallback = tgwinkDeviceContextCleanup;

	status = WdfDeviceCreate(&DeviceInit, &fdoAttributes, &device);

	if (!NT_SUCCESS(status)) {
		KdPrint("WdfDeviceCreate failed with status 0x%08x\n", status);
		return status;
	}

	context = DeviceGetContext(device);
	context->hIrq = NULL;

	RtlInitUnicodeString(&pmemDevNam, L"\\Device\\PhysicalMemory");
	InitializeObjectAttributes(&oAttr, &pmemDevNam, OBJ_CASE_INSENSITIVE, NULL, NULL);
	status = ZwOpenSection(&context->hMemory, SECTION_MAP_READ | SECTION_MAP_WRITE, &oAttr);
	if (!NT_SUCCESS(status)) {
		KdPrint("ZwOpenSection failed to open physical memory device with status 0x%08x\n", status);
		return status;
	}

	status = WdfDeviceCreateDeviceInterface(
		device,
		&GUID_DEVINTERFACE_tgwink,
		NULL
		);

	if (!NT_SUCCESS(status)) {
		KdPrint("WdfDeviceCreateDeviceInterface failed sith status 0x%08x\n", status);
		return status;
	}
	
	status = tgwinkQueueInitialize(device);
	if (!NT_SUCCESS(status)) {
		KdPrint("tgwinkQueueInitialize failed with status 0x%08x\n", status);
		return status;
	}

	return status;
}

void
tgwinkDeviceContextCleanup(
	_In_ WDFOBJECT Device
	)
{
	PAGED_CODE();

	UNREFERENCED_PARAMETER(Device);
}

BOOLEAN
tgwinkServiceInterrupt(
	_In_ WDFINTERRUPT Interrupt,
	_In_ ULONG MessageID
	)
{
	UNREFERENCED_PARAMETER(MessageID);
	PINTERRUPT_CONTEXT iContext = InterruptGetContext(Interrupt);

	iContext->serial = InterlockedIncrement64(&iContext->serial);
	WdfInterruptQueueWorkItemForIsr(Interrupt);
	
	return TRUE;
}

void
tgwinkInterruptWerk(
	_In_ WDFINTERRUPT Interrupt,
	_In_ WDFOBJECT Object
	)
{
	PINTERRUPT_CONTEXT iCtx = InterruptGetContext(Interrupt);
	WDFDEVICE dev = Object;
	PDEVICE_CONTEXT dCtx = DeviceGetContext(dev);
	WDFREQUEST pending;
	NTSTATUS res;
	WDFMEMORY out;

	KdPrint("Werking interrupt #%x...\n", iCtx->serial);
	res = WdfIoQueueRetrieveNextRequest(dCtx->NotificationQueue, &pending);
	if (!NT_SUCCESS(res)) {
		if (res == STATUS_NO_MORE_ENTRIES)
			KdPrint("No one was waiting!");
		else
			KdPrint("WdfIoQueueRetrieveNextRequest returned unknown error %x\n", res);
		return;
	} 
	res = WdfRequestRetrieveOutputMemory(pending, &out);
	if (!NT_SUCCESS(res)) {
		KdPrint("Couldn't retrieve output buffer, error %x\n", res);
		WdfRequestComplete(pending, STATUS_UNSUCCESSFUL);
		return;
	}
	res = WdfMemoryCopyFromBuffer(out, 0, &iCtx->serial, 8);
	if (!NT_SUCCESS(res)) {
		KdPrint("Couldn't copy to output buffer, error %x\n", res);
		WdfRequestComplete(pending, STATUS_UNSUCCESSFUL);
		return;
	}
	WdfRequestCompleteWithInformation(pending, STATUS_SUCCESS, 8);
	KdPrint("Completed interrupt werk by notifying pending queue request.\n");
}