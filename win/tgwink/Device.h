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

#include "public.h"

EXTERN_C_START

typedef struct _DEVICE_CONTEXT
{
	WDFQUEUE IoDefaultQueue;
	struct {
		unsigned length;
		PHYSICAL_ADDRESS busAddr;
		PHYSICAL_ADDRESS phyAddr;
		PVOID mapAddr;
	} bar[2];
	BUS_INTERFACE_STANDARD busInterface;
	HANDLE hMemory;
} DEVICE_CONTEXT, *PDEVICE_CONTEXT;

WDF_DECLARE_CONTEXT_TYPE_WITH_NAME(DEVICE_CONTEXT, DeviceGetContext)

NTSTATUS
tgwinkCreateDevice(
	_Inout_ PWDFDEVICE_INIT DeviceInit
	);

EVT_WDF_DEVICE_CONTEXT_CLEANUP tgwinkDeviceContextCleanup;
EVT_WDF_DEVICE_PREPARE_HARDWARE tgwinkPrepareHardware;
EVT_WDF_DEVICE_RELEASE_HARDWARE tgwinkReleaseHardware;

EXTERN_C_END