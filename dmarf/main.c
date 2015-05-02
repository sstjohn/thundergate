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
#include <efi/efilib.h>
#include <wchar.h>
#include "acpi.h"

void
walk_xsdt(struct xsdt *xsdt)
{
    int i;
    u32 cksum = 0;
    char buf[5];

    int count = (xsdt->h.length - sizeof(struct acpi_sdt_hdr)) / 8;

    for (i = 0; i < count; i++) {
        struct acpi_sdt_hdr *sdt = xsdt->sdt[i];

        if (strncmpa(sdt->sig, "DMAR", 4) == 0) {
            CopyMem(sdt->sig, "RAMD", 4);
            /* Print(L"DMARF!\n"); */
        }
    }
}

void
follow_rsdp2(struct rsdp2_t *tbl)
{
    walk_xsdt((struct xsdt *)tbl->xsdt_address);
}

static EFI_GUID gAcpi20TableGuid = ACPI_20_TABLE_GUID;

void
EFIAPI
werk(EFI_EVENT Event, VOID *Context)
{
    int i;
    for (i = 0; i < ST->NumberOfTableEntries; i++) {
            if (CompareGuid(&ST->ConfigurationTable[i].VendorGuid,
                        &gAcpi20TableGuid) == 0) {
                follow_rsdp2(ST->ConfigurationTable[i].VendorTable);
                break;
        }
    }
}

static
EFI_STATUS
EFI_FUNCTION
DmarfUnload(IN EFI_HANDLE ImageHandle)
{
  return EFI_SUCCESS;
}

EFI_STATUS
efi_main (EFI_HANDLE ImageHandle, EFI_SYSTEM_TABLE *SysTab)
{
  EFI_STATUS Status;
  EFI_LOADED_IMAGE *LoadedImage = NULL;
  EFI_EVENT evt;

  InitializeLib(ImageHandle, SysTab);

  Status = uefi_call_wrapper(BS->OpenProtocol, 6,
                             ImageHandle, &LoadedImageProtocol,
                             (void **)&LoadedImage, ImageHandle,
                             NULL, EFI_OPEN_PROTOCOL_GET_PROTOCOL);
  if (!EFI_ERROR(Status))
    LoadedImage->Unload = (EFI_IMAGE_UNLOAD)DmarfUnload;

  Status = uefi_call_wrapper(BS->CreateEvent, 5, 
          EVT_SIGNAL_EXIT_BOOT_SERVICES, TPL_NOTIFY,
          &werk, NULL, &evt);

  uefi_call_wrapper(BS->Exit, 4, ImageHandle, EFI_SUCCESS, 0, NULL);
  return EFI_SUCCESS;
}
