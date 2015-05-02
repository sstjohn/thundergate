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

#ifndef _SBDI_H_
#define _SBDI_H_

#include "utypes.h"

struct sbdi_mode {
    u32 reserved :26;
    u32 multi_txq_en :1;
    u32 pass_bit :1;
    u32 rupd_enable :1;
    u32 attention_enable :1;
    u32 enable :1;
    u32 reset :1;
};

struct sbdi_status {
    u32 reserved :29;
    u32 error :1;
    u32 reserved2 :2;
};

struct sbdi_regs {
    struct sbdi_mode mode;
    struct sbdi_status status;
    u32 prod_idx[16];
};

#endif

