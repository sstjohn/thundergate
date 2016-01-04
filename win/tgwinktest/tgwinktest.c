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

#include <windows.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <tchar.h>
#include <setupapi.h>
#include <initguid.h>
#include <SDKDDKVer.h>
#include <newdev.h>
#include <devpkey.h>
#include <NTSecAPI.h>
#include "Public.h"

#pragma comment (lib, "setupapi.lib")

int main()
{
	HDEVINFO hDevInfo;
	SP_DEVICE_INTERFACE_DATA devIntData;
	PSP_DEVICE_INTERFACE_DETAIL_DATA pDevIntDetail = NULL;
	SP_DEVINFO_DATA devInfoData;
	DWORD requiredSize;
	int idx = 0; 
	

	hDevInfo = SetupDiGetClassDevs(&GUID_DEVINTERFACE_tgwink, NULL, NULL, DIGCF_DEVICEINTERFACE | DIGCF_PRESENT);

	if (INVALID_HANDLE_VALUE == hDevInfo) {
		printf("SetupDiCreateDeviceInfoList failed!\n");
		return 1;
	}

	devIntData.cbSize = sizeof(SP_DEVICE_INTERFACE_DATA);
	devInfoData.cbSize = sizeof(SP_DEVINFO_DATA);

	while (SetupDiEnumDeviceInterfaces( hDevInfo, NULL, &GUID_DEVINTERFACE_tgwink, idx, &devIntData)) {
		printf("Found device interface #%d.\n", idx);
 
		SetupDiGetDeviceInterfaceDetail(hDevInfo, &devIntData, NULL, 0, &requiredSize, NULL);
		if (pDevIntDetail != NULL) {
			free(pDevIntDetail);
			pDevIntDetail = NULL;
		}
		pDevIntDetail = (PSP_DEVICE_INTERFACE_DETAIL_DATA)malloc(requiredSize);
		pDevIntDetail->cbSize = sizeof(SP_DEVICE_INTERFACE_DETAIL_DATA);
		if (!SetupDiGetDeviceInterfaceDetail(hDevInfo, &devIntData, pDevIntDetail, requiredSize, NULL, &devInfoData)) {
			printf("SetupDiGetDeviceInterfaceDetail failed!\n");
			return 1;
		}

		_tprintf(TEXT("Device path: %s\n"), pDevIntDetail->DevicePath);
		
		idx++;
	}

	printf("Found %d total device interfaces.\n", idx);

	if (idx == 1) {
		HANDLE h = CreateFile(pDevIntDetail->DevicePath, GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);

		if (INVALID_HANDLE_VALUE == h) {
			LPTSTR eTxt = NULL;
			DWORD error = GetLastError();

			FormatMessage(FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_IGNORE_INSERTS, NULL, error, MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL), (LPTSTR)&eTxt, 0, NULL);

			if (NULL != eTxt) {
				wprintf(L"Failed to open handle to device interface: %s\n", eTxt);
				LocalFree(eTxt);
			} else {
				printf("Failed to open handle to device interface, error code %d.\n", error);
			}

		} else {
			uint32_t readBuffer;
			DWORD bytesRead;
			void *bar;
			
			printf("Successfully opened handle to device interface!\n");

			if (ReadFile(h, &readBuffer, 4, &bytesRead, NULL)) {
				if (bytesRead == 4) {
					printf("Successfully read from device interface handle: 0x%08x\n", readBuffer);
				} else {
					printf("Read an incorrect number of bytes. ?!\n");
				}
			} else {
				printf("Failed to read from interface handle!\n");
			}

			bytesRead = DeviceIoControl(h, IOCTL_TGWINK_SAY_HELLO, NULL, 0, &readBuffer, 4, NULL, NULL);
			if (0 == bytesRead) {
				printf("DeviceIoControl SAY_HELLO failed, error code %08x\n", GetLastError());
			} else {
				printf("DeviceIoControl SAY_HELLO put %08x into the buffer!\n", readBuffer);
			}

			bytesRead = DeviceIoControl(h, IOCTL_TGWINK_MAP_BAR_0, NULL, 0, &bar, sizeof(void *), NULL, NULL);
			if (0 == bytesRead) {
				printf("DeviceIoControl MAP_BAR_0 failed, error code %08x\n", GetLastError());
			}
			else {
				printf("DeviceIoControl MAP_BAR_0 put %p into the buffer!\n", bar);
				printf("Data at mapped address: %08x\n", *((int *)bar));
			}

			CloseHandle(h);
		}
	}

	if (pDevIntDetail != NULL)
		free(pDevIntDetail);

	system("pause");

	return 0;
}

