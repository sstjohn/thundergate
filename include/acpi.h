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

#ifndef _ACPI_H_
#define _ACPI_H_

#include "utypes.h"

#ifdef _MSC_VER
#define __attribute__(x)
#define ANYSIZE_ARRAY 1
#pragma pack(push, 1)
#else
#define ANYSIZE_ARRAY 0
#endif

struct __attribute__((packed)) dmar_tbl_hdr {
	char sig[4];
	u32 length;
	u8 rev;
	u8 cksum;
	char oemid[6];
	char oemtableid[8];
	u32 oem_rev;
	char creator_id[4];
	u32 creator_rev;
	u8 host_addr_width;
	u8 flags;
	char reserved[10];
};

struct __attribute__((packed)) dmar_dev_scope {
	u8 type;
	u8 length;
	u16 reserved;
	u8 enum_id;
	u8 start_bus_number;
	struct __attribute__((packed)) {
		u8 device;
		u8 function;
	} path[ANYSIZE_ARRAY];
};

struct __attribute__((packed)) dmar_drhd {
	u16 type;
	u16 length;
	u8 flags;
	u8 reserved;
	u16 seg_no;
	u64 base_address;
};

struct __attribute__((packed)) dmar_rmrr {
	u16 type;
	u16 length;
	u8 flags;
	u8 reserved;
	u16 seg_no;
	u64 base_addr;
	u64 limit_addr;
};

struct __attribute__((packed)) dmar_atsr {
	u16 type;
	u16 length;
	u8 flags;
	u8 reserved;
	u16 seg_no; 
	struct dmar_dev_scope dev_scope[ANYSIZE_ARRAY];
};

struct __attribute__((packed)) dmar_rhsa {
	u16 type;
	u16 length;
	u32 reserved;
	u64 base_addr;
	u32 proximity_domain;
};

struct __attribute__((packed)) dmar_andd {
	u16 type;
	u16 length;
	u8 reserved[3];
	u8 acpi_dev_no;
	char object_name[0];
};

struct __attribute__((packed)) acpi_sdt_hdr {
        char sig[4];
        u32 length;
        u8 rev;
        u8 cksum;
        char oemid[6];
        char oemtableid[8];
        u32 oem_rev;
        u32 creator_id;
        u32 creator_rev;
};

struct __attribute__((packed)) xsdt {
    struct acpi_sdt_hdr h;
    struct acpi_sdt_hdr *sdt[0];
};

struct __attribute__((packed)) rsdp_t {
    char sig[8];
    u8 cksum;
    char oemid[6];
    u8 rev;
    u32 rsdt_address;
};

struct __attribute__((packed)) rsdp2_t {
    char sig[8];
    u8 cksum;
    char oemid[6];
    u8 rev;
    u32 rsdt_address;

    u32 length;
    u64 xsdt_address;
    u8 extended_cksum;
    u8 reserved[3];
};

#ifdef _MSC_VER
#pragma pack(pop)
#endif

#endif
