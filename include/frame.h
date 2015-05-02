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

#ifndef _FRAME_H_
#define _FRAME_H_

#include "../include/utypes.h"

struct frame {
    u8 dest[6];
    u8 src[6];
    u16 type;
    u8 data[0];
};

struct vlan_frame {
    u8 dest[6];
    u8 src[6];
    u16 tpid;
    union {
        u16 tci;
        struct {
            u16 priority :3;
            u16 cfi :1;
            u16 vlan :12;
        };
    };
    u16 type;
    u8 data[0];
};

#endif
