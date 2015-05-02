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

#endif
