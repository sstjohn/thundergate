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

#ifndef _DMARF_H_
#define _DMARF_H_

#include <efi.h>
#include <efidevp.h>
#include <efilib.h>
#include <efiprot.h>
#include <efipciio.h>
#include <eficon.h>

#include <stddef.h>   /* wchar_t -- freestanding; <wchar.h> is hosted-only */
#include "acpi.h"

#define DISABLE_DMAR 1
#define IDENTITY_MAP_FIRST_16M 1
#define IDENTITY_MAP_DRHD 1

/* IORT (ARM SMMU) -- mirrors the DMAR knobs above. DISABLE_IORT renames
   the table so the OS never parses it; IDENTITY_MAP_RMR (the surgical
   RMR path) stays gated off, exactly like IDENTITY_MAP_* for DMAR. */
#define DISABLE_IORT 1
#define IDENTITY_MAP_RMR 1

#if VERBOSE
#define DbgPrint(x, ...) Print(x, ##__VA_ARGS__)
#else
#define DbgPrint(x, ...)
#endif

extern u32 tg_dp[12];
extern u32 tg_dp_len;
extern u32 tg_rid;

void splash();

void walk_iort(void *iort);
void update_tbl_cksum(void *tbl);

void EFIAPI werk(EFI_EVENT Event, VOID *Context);

#endif
