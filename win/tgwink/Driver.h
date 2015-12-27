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

#define INITGUID

#include <ntddk.h>
#include <wdf.h>
#include <wdmguid.h>

#include "device.h"
#include "queue.h"

#undef KdPrint
#define KdPrint(format, ...) DbgPrintEx(DPFLTR_DEFAULT_ID, DPFLTR_ERROR_LEVEL, format, __VA_ARGS__)

EXTERN_C_START

DRIVER_INITIALIZE DriverEntry;
EVT_WDF_DRIVER_DEVICE_ADD tgwinkEvtDeviceAdd;
EVT_WDF_OBJECT_CONTEXT_CLEANUP tgwinkEvtDriverContextCleanup;

EXTERN_C_END
