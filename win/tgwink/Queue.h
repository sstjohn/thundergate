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

EXTERN_C_START

typedef struct _QUEUE_CONTEXT {

    ULONG PrivateDeviceData;  // just a placeholder

} QUEUE_CONTEXT, *PQUEUE_CONTEXT;

WDF_DECLARE_CONTEXT_TYPE_WITH_NAME(QUEUE_CONTEXT, QueueGetContext)

NTSTATUS
tgwinkQueueInitialize(
    _In_ WDFDEVICE hDevice
    );

EVT_WDF_IO_QUEUE_IO_DEVICE_CONTROL tgwinkEvtIoDeviceControl;
EVT_WDF_IO_QUEUE_IO_STOP tgwinkEvtIoStop;
EVT_WDF_IO_QUEUE_IO_READ tgwinkEvtIoRead;
EVT_WDF_IO_QUEUE_IO_WRITE tgwinkEvtIoWrite;

EXTERN_C_END