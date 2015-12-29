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

u64 drhd_base = 0;

u32 walk_dev_scope(void *a)
{
	struct dmar_dev_scope *ds = a;
	u32 ds_sz = ds->length;
	u32 offset = 0;

	DbgPrint(L"\n");
	DbgPrint(L"device scope type: %d ", ds->type);
	switch (ds->type) {
		case 1: DbgPrint(L"(pcie endpoint)\n"); break;
		case 2: DbgPrint(L"(pcie subtree)\n"); break;
		case 3: DbgPrint(L"(ioapic)\n"); break;
		case 4: DbgPrint(L"(msi capable hpet)\n"); break;
		case 5: DbgPrint(L"(acpi namespace device)\n"); break;
		default: DbgPrint(L"unknown)\n"); break;
	}
	DbgPrint(L"device scope length: %d\n", ds->length);
	DbgPrint(L"device scope reserved: %d\n", ds->reserved);
	DbgPrint(L"device scope enum id: %02x ", ds->enum_id);
	switch (ds->type) {
		case 3: DbgPrint(L"(io apic id)\n"); break;
		case 4: DbgPrint(L"(hpet number)\n"); break;
		case 5: DbgPrint(L"(acpi device number)\n"); break;
		default: DbgPrint(L"(reserved)\n"); break;
	}
	DbgPrint(L"device scope start bus num: %02x\n", ds->start_bus_number);
	
	offset += sizeof(struct dmar_dev_scope);
	
	DbgPrint(L"device scope path: ");
	while (offset < ds_sz) {
		u16 tmp = *((u16 *)((uintptr_t)a + offset));
		u8 dev = tmp >> 8;
		u8 fun = tmp & 0xff;
		DbgPrint(L"%02x:%02x ", dev, fun);
		offset += 2;
	}
	DbgPrint(L"\n");	

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

	r->length += create_dev_scope((uintptr_t)a + sizeof(struct dmar_rmrr));
	return r->length;
}

void walk_rmrr(void *a)
{
	struct dmar_rmrr *r = a;
	u32 r_sz = r->length;
	u32 offset = 0;

	DbgPrint(L"\n");
	DbgPrint(L"rmrr length: %d\n", r->length);
	DbgPrint(L"rmrr reserved: %d\n", r->reserved);
	DbgPrint(L"rmrr segment num: %04x\n", r->seg_no);
	DbgPrint(L"rmrr base addr: %lx\n", r->base_addr);
	DbgPrint(L"rmrr limit addr: %lx\n", r->limit_addr);

	offset += sizeof(struct dmar_rmrr);

	while (offset < r_sz)
		offset += walk_dev_scope((uintptr_t)a + offset);
}

void walk_drhd(void *a)
{
	struct dmar_drhd *drhd = a;
	u32 drhd_sz = drhd->length;
	u32 offset = 0;

	DbgPrint(L"\n");
	DbgPrint(L"drhd length: %d\n", drhd->length);
	DbgPrint(L"drhd flags: %d", drhd->flags);
	if (drhd->flags != 0) {
		DbgPrint(L": ");
		if (drhd->flags & 1)
			DbgPrint(L"include_pci_all ");
		if (drhd->flags & ~1)
			DbgPrint(L"unknown_flagset_%x", drhd->flags);
	};
	DbgPrint(L"\n");
	DbgPrint(L"drhd reserved: %d\n", drhd->reserved);
	DbgPrint(L"drhd seg num: %04x\n", drhd->seg_no);
	DbgPrint(L"drhd base addr: %lx\n", drhd->base_address);

	offset += sizeof(struct dmar_drhd);

	if ((drhd->flags & 1) == 1)
		drhd_base = drhd->base_address;

	while (offset < drhd_sz)
		offset += walk_dev_scope((uintptr_t)a + offset);
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

	DbgPrint(L"table sig: %.4a\n", dmar_tbl->sig);
	DbgPrint(L"table len: %d\n", dmar_tbl->length);
	DbgPrint(L"table rev: %d\n", dmar_tbl->rev);
	DbgPrint(L"table sum: %d\n", dmar_tbl->cksum);
	DbgPrint(L"\n");
	DbgPrint(L"oemid: %.6a\n", dmar_tbl->oemid);
	DbgPrint(L"oemtableid: %.8a\n", dmar_tbl->oemtableid);
	DbgPrint(L"oemrev: %d\n", dmar_tbl->oem_rev);
	DbgPrint(L"creator id: %.4a\n", dmar_tbl->creator_id);
	DbgPrint(L"creator rev: %d\n", dmar_tbl->creator_rev);
	DbgPrint(L"host addr width: %d\n", (u32)(dmar_tbl->host_addr_width + 1));
	DbgPrint(L"flags: %d ", dmar_tbl->flags);
	if (dmar_tbl->flags > 0) {
		if (dmar_tbl->flags & 1)
			DbgPrint(L"intr_remap ");
		if (dmar_tbl->flags & 2)
			DbgPrint(L"x2apic_opt_out ");
		if (dmar_tbl->flags & ~3)
			DbgPrint(L"unknown_flagset_%x", dmar_tbl->flags);
	};
	DbgPrint(L"\n");
	DbgPrint(L"reserved: %.10a\n", dmar_tbl->reserved);

	offset += sizeof(struct dmar_tbl_hdr);

	if (offset >= tbl_sz)
		return;
	
	do {
       	    u32 tmp = *((u32 *)((uintptr_t)a + offset));
	    u16 ln = tmp >> 16;
	    u16 nt = tmp & 0xffff;

	    DbgPrint(L"\n\n");
	    
	    switch(nt) {
	    case 0:
		DbgPrint(L"drhd at offset %d\n", offset);
		walk_drhd((uintptr_t)a+offset);
		break;
	    case 1:
		DbgPrint(L"rmrr at offset %d\n", offset);
		walk_rmrr((uintptr_t)a+offset);
		break;
	    default:
		DbgPrint(L"type %d at offset %d\n", nt, offset);
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
		DbgPrint(L"\n\nnew rmrr created: \n");
		walk_rmrr(a + offset);
	} 
#endif
#if IDENTITY_MAP_DRHD
	if (drhd_base != 0) {
		rmrr_sz = create_rmrr(a + dmar_tbl->length, drhd_base, drhd_base + 0x1000);

		if (rmrr_sz) {
			DbgPrint(L"\n\nnew rmrr created: \n");
			walk_rmrr(a + dmar_tbl->length);
			dmar_tbl->length += rmrr_sz;
		}
	}
#endif
#endif
	if (!rmrr_sz) {
	    DbgPrint(L"\n\nDMARF!\n");
	    CopyMem(dmar_tbl->sig, "RAMD", 4);
	}
	update_tbl_cksum(a);
}

void walk_xsdt(struct xsdt *xsdt)
{
    int i;

    int count = (xsdt->h.length - sizeof(struct acpi_sdt_hdr)) / 8;

    DbgPrint(L"enumerating %d sdts in xsdt at %lx\n\n", count, xsdt);

    for (i = 0; i < count; i++) {
        struct acpi_sdt_hdr *sdt = xsdt->sdt[i];

	DbgPrint(L"table at %lx signature %.4a\n", sdt, sdt->sig);

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
    splash();
    for (int i = 0; i < ST->NumberOfTableEntries; i++) {
	    if (CompareGuid(&ST->ConfigurationTable[i].VendorGuid,
			&gAcpi20TableGuid) == 0) {
		follow_rsdp2(ST->ConfigurationTable[i].VendorTable);
	}
    }
}
