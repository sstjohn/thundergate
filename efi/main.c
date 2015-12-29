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

#include "dmarf.h"

u32 tg_dp[12] = {0};
u32 tg_dp_len = 0;

static EFI_IMAGE_UNLOAD orig_unload = 0;

static EFI_STATUS EFI_FUNCTION DmarfUnload(IN EFI_HANDLE ImageHandle)
{
  EFI_INPUT_KEY key;

  if (orig_unload) {
	EFI_STATUS tmp;
	DbgPrint(L"calling original unload handler\n");
	tmp = (*orig_unload)(ImageHandle);
	DbgPrint(L"original unload handler returned %x\n", tmp);
  }

  DbgPrint(L"dmarf unloading\n");
  
  return EFI_SUCCESS;
}

#define EFI_COMPONENT_NAME_PROTOCOL_GUID \
	  { 0x107a772c, 0xd5e1, 0x11d4, { 0x9a, 0x46, 0x0, 0x90, 0x27, 0x3f, 0xc1, 0x4d } }

EFI_GUID EfiComponentNameProtocolGuid = EFI_COMPONENT_NAME_PROTOCOL_GUID;

typedef struct _EFI_COMPONENT_NAME_PROTOCOL EFI_COMPONENT_NAME_PROTOCOL;

struct _EFI_COMPONENT_NAME_PROTOCOL {
	EFI_STATUS (EFI_FUNCTION EFIAPI *dname)(
			EFI_COMPONENT_NAME_PROTOCOL *,
			CHAR8 *,
			CHAR16 **);
	EFI_STATUS (EFI_FUNCTION EFIAPI *cname)(
			EFI_COMPONENT_NAME_PROTOCOL *,
			EFI_HANDLE,
			EFI_HANDLE,
			CHAR8 *,
			CHAR16 **);
	CHAR8 *langs;
};

CHAR16 dmarf_driver_name[] = L"ThunderGate DMARF";

EFI_STATUS EFI_FUNCTION EFIAPI get_driver_name(
	EFI_COMPONENT_NAME_PROTOCOL *this, CHAR8 *lang, CHAR16 **drivername)
{
	*drivername = dmarf_driver_name;
	return EFI_SUCCESS;
}

EFI_STATUS EFI_FUNCTION EFIAPI get_controller_name(
	EFI_COMPONENT_NAME_PROTOCOL *this, EFI_HANDLE controller, 
	EFI_HANDLE child, CHAR8 *lang, CHAR16 **controllername)
{
	return EFI_UNSUPPORTED;
}

EFI_COMPONENT_NAME_PROTOCOL dmarf_component_name = {
	get_driver_name,
	get_controller_name,
	"eng"
};

#define EFI_DRIVER_BINDING_PROTOCOL_GUID \
  {0x18A031AB,0xB443,0x4D1A,0xA5,0xC0,0x0C,0x09,0x26,0x1E,0x9F,0x71}

EFI_GUID EfiDriverBindingProtocolGuid = EFI_DRIVER_BINDING_PROTOCOL_GUID;

EFI_GUID EfiDevicePathProtocol = DEVICE_PATH_PROTOCOL;

typedef struct _EFI_DRIVER_BINDING_PROTOCOL EFI_DRIVER_BINDING_PROTOCOL;

struct _EFI_DRIVER_BINDING_PROTOCOL {
  EFI_STATUS (EFIAPI *Supported)(EFI_DRIVER_BINDING_PROTOCOL*,
		EFI_HANDLE, EFI_DEVICE_PATH *);
  EFI_STATUS (EFIAPI *Start)(EFI_DRIVER_BINDING_PROTOCOL *,
		EFI_HANDLE, EFI_DEVICE_PATH *);
  EFI_STATUS (EFIAPI *Stop)(EFI_DRIVER_BINDING_PROTOCOL *,
		EFI_HANDLE, UINTN, EFI_HANDLE *);
  UINT32                                Version;
  EFI_HANDLE                            ImageHandle;
  EFI_HANDLE                            DriverBindingHandle;
};

EFI_GUID EfiPciIoProtocolGuid = EFI_PCI_IO_PROTOCOL;

EFI_STATUS EFIAPI drv_supported(
		EFI_DRIVER_BINDING_PROTOCOL *this,
		EFI_HANDLE hController, 
		EFI_DEVICE_PATH *remaining_device_path)
{
	EFI_PCI_IO *pci;
	EFI_STATUS s;
	UINTN seg, bus, dev, fun;
	PCI_TYPE00 pci_hdr;
	EFI_STATUS ret = EFI_UNSUPPORTED;

	s = uefi_call_wrapper(BS->OpenProtocol, 6,
			hController, 
			&EfiPciIoProtocolGuid,
			(void **)&pci,
			this->DriverBindingHandle,
			hController,
			EFI_OPEN_PROTOCOL_BY_DRIVER);

	if (EFI_ERROR(s))
		return EFI_UNSUPPORTED;


	s = pci->Pci.Read(pci, EfiPciIoWidthUint32, 0, sizeof(pci_hdr) / sizeof(UINT32), &pci_hdr);
	if (EFI_ERROR(s)) {
		goto done;
	}

	if (pci_hdr.Hdr.VendorId == 0x14e4 && pci_hdr.Hdr.DeviceId == 0x1682) {
		EFI_DEV_PATH *dp = NULL;

		tg_dp_len = 0;

		s = pci->GetLocation(pci, &seg, &bus, &dev, &fun);
		if (EFI_ERROR(s)) {
			goto done;
		}
		DbgPrint(L"found a tb gige adapter at %02x:%02x.%02x.\n", bus, dev, fun);

		s = uefi_call_wrapper(BS->HandleProtocol, 3,
				hController,
				&EfiDevicePathProtocol,
				(void **)&dp);

		if (EFI_ERROR(s)) {
			DbgPrint(L"does not support device path protocol\n");
			goto done;
		}

		while (dp->DevPath.Type != 0x7f) {
			DbgPrint(L"device path type: %x, subtype: %x, l1: %x, l2: %x ",
					dp->DevPath.Type, dp->DevPath.SubType, dp->DevPath.Length[0], dp->DevPath.Length[1]);

			switch(dp->DevPath.Type) {
				case 1:
					DbgPrint(L"pci dev %02x fn %02x\n", dp->Pci.Device,
							dp->Pci.Function);
					tg_dp[tg_dp_len++] = dp->Pci.Device << 16 | dp->Pci.Function;
					break;
				case 2:
					DbgPrint(L"acpi hid %08x, uid %08x\n",
							dp->Acpi.HID, dp->Acpi.UID);
					break;
				default:
					DbgPrint(L"\n");
					break;
			}
			dp = (EFI_DEV_PATH *)(((uintptr_t)dp) + dp->DevPath.Length[0]);
		}

		ret = EFI_SUCCESS;
	}

	

done:
	uefi_call_wrapper(BS->CloseProtocol, 4,
			hController,
			&EfiPciIoProtocolGuid,
			this->DriverBindingHandle,
			hController);

	return ret;
}

EFI_STATUS EFIAPI drv_start(
		EFI_DRIVER_BINDING_PROTOCOL *this,
		EFI_HANDLE hController,
		EFI_DEVICE_PATH *remaining_device_path)
{
	return EFI_SUCCESS;
}

EFI_STATUS EFIAPI drv_stop(
		EFI_DRIVER_BINDING_PROTOCOL *this,
		EFI_HANDLE hController,
		UINTN number_of_children,
		EFI_HANDLE *child_handle_buffer)
{
	return EFI_SUCCESS;
}

EFI_DRIVER_BINDING_PROTOCOL dmarf_driver_binding = {
	drv_supported,
	drv_start,
	drv_stop,
	0x10 << 16,
	0,
	0
};

EFI_STATUS efi_main(EFI_HANDLE ImageHandle, EFI_SYSTEM_TABLE *SysTab)
{
  EFI_STATUS Status;
  EFI_LOADED_IMAGE *LoadedImage = NULL;
  EFI_EVENT evt;

  InitializeLib(ImageHandle, SysTab);

  dmarf_driver_binding.ImageHandle = ImageHandle;
  dmarf_driver_binding.DriverBindingHandle = ImageHandle;


  Status = uefi_call_wrapper(BS->InstallProtocolInterface, 4,
		  &ImageHandle, &EfiDriverBindingProtocolGuid,
		  0, (void *)&dmarf_driver_binding);
  if (EFI_ERROR(Status))
	  DbgPrint(L"failed to install driver binding protocol handler: %r\n", Status);
  else
	  DbgPrint(L"installed driver binding protocol handler to image handle\n");

  Status = uefi_call_wrapper(BS->InstallProtocolInterface, 4,
		  &ImageHandle, &EfiComponentNameProtocolGuid,
		  0, (void *)&dmarf_component_name);
  if (EFI_ERROR(Status))
	  DbgPrint(L"failed to install component name protocol handler: %r\n", Status);
  else
	  DbgPrint(L"installed component name protocol handler to image handle\n");


  Status = uefi_call_wrapper(BS->HandleProtocol, 3,
                             ImageHandle, &LoadedImageProtocol,
                             (void **)&LoadedImage);

  if (EFI_ERROR(Status)) {
	  DbgPrint(L"loaded image protocol fail: %r\n", Status);
	  return EFI_SUCCESS;
  }

  if (LoadedImage->Unload) {
	  DbgPrint(L"replacing unload handler\n");
	  orig_unload = LoadedImage->Unload;
  } else {
	  DbgPrint(L"installing unload handler\n");
  }

  LoadedImage->Unload = (EFI_IMAGE_UNLOAD)DmarfUnload;
 
  DbgPrint(L"installing boot services exit signal handler\n");

  Status = uefi_call_wrapper(BS->CreateEvent, 5, 
          EVT_SIGNAL_EXIT_BOOT_SERVICES, TPL_NOTIFY,
          &werk, NULL, &evt);

  uefi_call_wrapper(BS->Exit, 4, ImageHandle, EFI_SUCCESS, 0, NULL);
  return EFI_SUCCESS;
}
