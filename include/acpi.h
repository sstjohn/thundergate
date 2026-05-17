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

#if defined(_MSC_VER) || defined(CTYPESGEN)
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

/* ACPI I/O Remapping Table (IORT) -- the ARM analogue of DMAR. An ARM
   UEFI platform has no DMAR (that is Intel VT-d only); the OS learns
   the SMMU topology, and programs DMA isolation, from the IORT. */

#define IORT_NODE_ITS_GROUP        0
#define IORT_NODE_NAMED_COMPONENT  1
#define IORT_NODE_ROOT_COMPLEX     2
#define IORT_NODE_SMMU_V1V2        3
#define IORT_NODE_SMMU_V3          4
#define IORT_NODE_PMCG             5
#define IORT_NODE_RMR              6

struct __attribute__((packed)) iort_tbl_hdr {
	char sig[4];
	u32 length;
	u8 rev;
	u8 cksum;
	char oemid[6];
	char oemtableid[8];
	u32 oem_rev;
	char creator_id[4];
	u32 creator_rev;
	u32 node_count;
	u32 node_offset;
	u32 reserved;
};

struct __attribute__((packed)) iort_node {
	u8 type;
	u16 length;
	u8 rev;
	u32 identifier;
	u32 mapping_count;
	u32 mapping_offset;
};

struct __attribute__((packed)) iort_id_mapping {
	u32 input_base;
	u32 id_count;
	u32 output_base;
	u32 output_reference;
	u32 flags;
};

struct __attribute__((packed)) iort_smmu {
	struct iort_node node;
	u64 base_address;          /* SMMUv1/v2 and SMMUv3 both begin here */
};

/* RMR node (type 6, IORT revision E): the SMMU analogue of a DMAR
   RMRR -- forces a 1:1 (identity) SMMU mapping of physical memory. */
struct __attribute__((packed)) iort_rmr {
	struct iort_node node;
	u32 flags;
	u32 desc_count;
	u32 desc_offset;
};

struct __attribute__((packed)) iort_rmr_desc {
	u64 base;
	u64 length;
	u32 reserved;
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
