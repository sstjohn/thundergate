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

#ifndef _STATUS_BLOCK_H_
#define _STATUS_BLOCK_H_

#include "utypes.h"

struct status_block {
    struct {
        u32 updated :1;
        u32 link_status :1;
        u32 attention :1;
        u32 reserved1 :29;
    };
    struct {
        u32 status_tag :8;
        u32 reserved2 :24;
    };
    struct {
        u32 rr1_pi :16;
        u32 rpci :16;
    };
    struct {
        u32 rr3_pi :16;
        u32 rr2_pi :16;
    };
    struct {
        u32 rr0_pi :16;
        u32 sbdci :16;
    };
    struct {
        u32 rjpci :16;
        u32 reserved6 :16;
    };
};

#endif
