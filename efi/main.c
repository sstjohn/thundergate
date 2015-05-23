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

#include <efi/efi.h>
#include <efi/efidevp.h>
#include <efi/efilib.h>
#include <efi/efiprot.h>
#include <efi/efipciio.h>
#include <wchar.h>
#include "acpi.h"

#define DISABLE_DMAR 1
#define IDENTITY_MAP_FIRST_16M 1
#define IDENTITY_MAP_DRHD 1

u32 tg_dp[12] = {0};
u32 tg_dp_len = 0;
u64 drhd_base = 0;

u32 walk_dev_scope(void *a)
{
	struct dmar_dev_scope *ds = a;
	u32 ds_sz = ds->length;
	u32 offset = 0;

	Print(L"\n");
	Print(L"device scope type: %d ", ds->type);
	switch (ds->type) {
		case 1: Print(L"(pcie endpoint)\n"); break;
		case 2: Print(L"(pcie subtree)\n"); break;
		case 3: Print(L"(ioapic)\n"); break;
		case 4: Print(L"(msi capable hpet)\n"); break;
		case 5: Print(L"(acpi namespace device)\n"); break;
		default: Print(L"unknown)\n"); break;
	}
	Print(L"device scope length: %d\n", ds->length);
	Print(L"device scope reserved: %d\n", ds->reserved);
	Print(L"device scope enum id: %02x ", ds->enum_id);
	switch (ds->type) {
		case 3: Print(L"(io apic id)\n"); break;
		case 4: Print(L"(hpet number)\n"); break;
		case 5: Print(L"(acpi device number)\n"); break;
		default: Print(L"(reserved)\n"); break;
	}
	Print(L"device scope start bus num: %02x\n", ds->start_bus_number);
	
	offset += sizeof(struct dmar_dev_scope);
	
	Print(L"device scope path: ");
	while (offset < ds_sz) {
		u16 tmp = *((u16 *)(a + offset));
		u8 dev = tmp >> 8;
		u8 fun = tmp & 0xff;
		Print(L"%02x:%02x ", dev, fun);
		offset += 2;
	}
	Print(L"\n");	

	return ds_sz;
}

u32 create_dev_scope(void *a)
{
	struct dmar_dev_scope *ds = a;

	ds->length = sizeof(struct dmar_dev_scope) + 2 * tg_dp_len;
	ds->type = 1;
        ds->reserved = 0;
	ds->enum_id = 1;
	ds->start_bus_number = 0;

	for (int i = 0; i < tg_dp_len; i++) {
		ds->path[i].device = tg_dp[i] >> 16;
		ds->path[i].function = tg_dp[i] & 0xff;
	}

	return ds->length;
}

u32 create_rmrr(void *a, u64 base, u64 limit)
{
	struct dmar_rmrr *r = a;
	
	if (tg_dp_len == 0)
		return 0;

	r->type = 1;
	r->length = sizeof(struct dmar_rmrr);
	r->flags = 1;
	r->reserved = 0;
	r->seg_no = 0;
	r->base_addr = base;
	r->limit_addr = limit;

	r->length += create_dev_scope(a + sizeof(struct dmar_rmrr));
	return r->length;
}

void walk_rmrr(void *a)
{
	struct dmar_rmrr *r = a;
	u32 r_sz = r->length;
	u32 offset = 0;

	Print(L"\n");
	Print(L"rmrr length: %d\n", r->length);
	Print(L"rmrr reserved: %d\n", r->reserved);
	Print(L"rmrr segment num: %04x\n", r->seg_no);
	Print(L"rmrr base addr: %lx\n", r->base_addr);
	Print(L"rmrr limit addr: %lx\n", r->limit_addr);

	offset += sizeof(struct dmar_rmrr);

	while (offset < r_sz)
		offset += walk_dev_scope(a + offset);
}

void walk_drhd(void *a)
{
	struct dmar_drhd *drhd = a;
	u32 drhd_sz = drhd->length;
	u32 offset = 0;

	Print(L"\n");
	Print(L"drhd length: %d\n", drhd->length);
	Print(L"drhd flags: %d", drhd->flags);
	if (drhd->flags != 0) {
		Print(L": ");
		if (drhd->flags & 1)
			Print(L"include_pci_all ");
		if (drhd->flags & ~1)
			Print(L"unknown_flagset_%x", drhd->flags);
	};
	Print(L"\n");
	Print(L"drhd reserved: %d\n", drhd->reserved);
	Print(L"drhd seg num: %04x\n", drhd->seg_no);
	Print(L"drhd base addr: %lx\n", drhd->base_address);

	offset += sizeof(struct dmar_drhd);

	if ((drhd->flags & 1) == 1)
		drhd_base = drhd->base_address;

	while (offset < drhd_sz)
		offset += walk_dev_scope(a + offset);
}

void update_tbl_cksum(void *a)
{
	struct acpi_sdt_hdr *hdr = a;
	u8 *words = a;
	u32 sum = 0;

	hdr->cksum = 0;
	for (int i = 0; i < hdr->length; i++)
		sum += words[i];
	hdr->cksum = 0x100 - (sum & 0xff);
}

void walk_dmar(void *a)
{
	struct dmar_tbl_hdr *dmar_tbl = a;
	u32 tbl_sz = dmar_tbl->length;
	u32 offset = 0;

	Print(L"table sig: %.4a\n", dmar_tbl->sig);
	Print(L"table len: %d\n", dmar_tbl->length);
	Print(L"table rev: %d\n", dmar_tbl->rev);
	Print(L"table sum: %d\n", dmar_tbl->cksum);
	Print(L"\n");
	Print(L"oemid: %.6a\n", dmar_tbl->oemid);
	Print(L"oemtableid: %.8a\n", dmar_tbl->oemtableid);
	Print(L"oemrev: %d\n", dmar_tbl->oem_rev);
	Print(L"creator id: %.4a\n", dmar_tbl->creator_id);
	Print(L"creator rev: %d\n", dmar_tbl->creator_rev);
	Print(L"host addr width: %d\n", (u32)(dmar_tbl->host_addr_width + 1));
	Print(L"flags: %d ", dmar_tbl->flags);
	if (dmar_tbl->flags > 0) {
		if (dmar_tbl->flags & 1)
			Print(L"intr_remap ");
		if (dmar_tbl->flags & 2)
			Print(L"x2apic_opt_out ");
		if (dmar_tbl->flags & ~3)
			Print(L"unknown_flagset_%x", dmar_tbl->flags);
	};
	Print(L"\n");
	Print(L"reserved: %.10a\n", dmar_tbl->reserved);

	offset += sizeof(struct dmar_tbl_hdr);

	if (offset >= tbl_sz)
		return;
	
	do {
       	    u32 tmp = *((u32 *)(a + offset));
	    u16 ln = tmp >> 16;
	    u16 nt = tmp & 0xffff;

	    Print(L"\n\n");
	    
	    switch(nt) {
	    case 0:
		Print(L"drhd at offset %d\n", offset);
		walk_drhd(a+offset);
		break;
	    case 1:
		Print(L"rmrr at offset %d\n", offset);
		walk_rmrr(a+offset);
		break;
	    default:
		Print(L"type %d at offset %d\n", nt, offset);
		break;
	    }
	    
	    offset += ln;
	} while(offset < tbl_sz);

	u32 rmrr_sz = 0;

#if !DISABLE_DMAR
#if IDENTITY_MAP_FIRST_16M
	rmrr_sz = create_rmrr(a + offset, 0, 0xffffff);
	if (rmrr_sz) {
		dmar_tbl->length += rmrr_sz;
		Print(L"\n\nnew rmrr created: \n");
		walk_rmrr(a + offset);
	} 
#endif
#if IDENTITY_MAP_DRHD
	if (drhd_base != 0) {
		rmrr_sz = create_rmrr(a + dmar_tbl->length, drhd_base, drhd_base + 0x1000);

		if (rmrr_sz) {
			Print(L"\n\nnew rmrr created: \n");
			walk_rmrr(a + dmar_tbl->length);
			dmar_tbl->length += rmrr_sz;
		}
	}
#endif
#endif
	if (!rmrr_sz) {
	    Print(L"\n\nDMARF!\n");
	    CopyMem(dmar_tbl->sig, "RAMD", 4);
	}
	update_tbl_cksum(a);
}

void walk_xsdt(struct xsdt *xsdt)
{
    int i;

    int count = (xsdt->h.length - sizeof(struct acpi_sdt_hdr)) / 8;

    Print(L"enumerating %d sdts in xsdt at %lx\n\n", count, xsdt);

    for (i = 0; i < count; i++) {
        struct acpi_sdt_hdr *sdt = xsdt->sdt[i];

	Print(L"table at %lx signature %.4a\n", sdt, sdt->sig);

        if (strncmpa(sdt->sig, "DMAR", 4) == 0) {
	    walk_dmar(sdt);
        }
    }
}

void follow_rsdp2(struct rsdp2_t *tbl)
{
    walk_xsdt((struct xsdt *)tbl->xsdt_address);
}

static EFI_GUID gAcpi20TableGuid = ACPI_20_TABLE_GUID;

void EFIAPI werk(EFI_EVENT Event, VOID *Context)
{
    for (int i = 0; i < ST->NumberOfTableEntries; i++) {
	    if (CompareGuid(&ST->ConfigurationTable[i].VendorGuid,
			&gAcpi20TableGuid) == 0) {
		follow_rsdp2(ST->ConfigurationTable[i].VendorTable);
	}
    }
}

static EFI_IMAGE_UNLOAD orig_unload = 0;

static EFI_STATUS EFI_FUNCTION DmarfUnload(IN EFI_HANDLE ImageHandle)
{
  EFI_INPUT_KEY key;

  if (orig_unload) {
	EFI_STATUS tmp;
	Print(L"calling original unload handler\n");
	tmp = (*orig_unload)(ImageHandle);
	Print(L"original unload handler returned %x\n", tmp);
  }

  Print(L"dmarf unloading\n");
  
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
		Print(L"found a tb gige adapter at %02x:%02x.%02x.\n", bus, dev, fun);

		s = uefi_call_wrapper(BS->HandleProtocol, 3,
				hController,
				&EfiDevicePathProtocol,
				(void **)&dp);

		if (EFI_ERROR(s)) {
			Print(L"does not support device path protocol\n");
			goto done;
		}

		while (dp->DevPath.Type != 0x7f) {
			Print(L"device path type: %x, subtype: %x, l1: %x, l2: %x ",
					dp->DevPath.Type, dp->DevPath.SubType, dp->DevPath.Length[0], dp->DevPath.Length[1]);

			switch(dp->DevPath.Type) {
				case 1:
					Print(L"pci dev %02x fn %02x\n", dp->Pci.Device,
							dp->Pci.Function);
					tg_dp[tg_dp_len++] = dp->Pci.Device << 16 | dp->Pci.Function;
					break;
				case 2:
					Print(L"acpi hid %08x, uid %08x\n",
							dp->Acpi.HID, dp->Acpi.UID);
					break;
				default:
					Print(L"\n");
					break;
			}
			dp = (EFI_DEV_PATH *)(((void *)dp) + dp->DevPath.Length[0]);
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

  Print(L"dmarf initialized\n");

  dmarf_driver_binding.ImageHandle = ImageHandle;
  dmarf_driver_binding.DriverBindingHandle = ImageHandle;


  Status = uefi_call_wrapper(BS->InstallProtocolInterface, 4,
		  &ImageHandle, &EfiDriverBindingProtocolGuid,
		  0, (void *)&dmarf_driver_binding);
  if (EFI_ERROR(Status))
	  Print(L"failed to install driver binding protocol handler: %r\n", Status);
  else
	  Print(L"installed driver binding protocol handler to image handle\n");

  Status = uefi_call_wrapper(BS->InstallProtocolInterface, 4,
		  &ImageHandle, &EfiComponentNameProtocolGuid,
		  0, (void *)&dmarf_component_name);
  if (EFI_ERROR(Status))
	  Print(L"failed to install component name protocol handler: %r\n", Status);
  else
	  Print(L"installed component name protocol handler to image handle\n");


  Status = uefi_call_wrapper(BS->HandleProtocol, 3,
                             ImageHandle, &LoadedImageProtocol,
                             (void **)&LoadedImage);

  if (EFI_ERROR(Status)) {
	  Print(L"loaded image protocol fail: %r\n", Status);
	  return EFI_SUCCESS;
  }

  if (LoadedImage->Unload) {
	  Print(L"replacing unload handler\n");
	  orig_unload = LoadedImage->Unload;
  } else {
	  Print(L"installing unload handler\n");
  }

  LoadedImage->Unload = (EFI_IMAGE_UNLOAD)DmarfUnload;
 
  Print(L"installing boot services exit signal handler\n");

  Status = uefi_call_wrapper(BS->CreateEvent, 5, 
          EVT_SIGNAL_EXIT_BOOT_SERVICES, TPL_NOTIFY,
          &werk, NULL, &evt);

  uefi_call_wrapper(BS->Exit, 4, ImageHandle, EFI_SUCCESS, 0, NULL);
  return EFI_SUCCESS;
}
