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

#ifndef _SBDC_H_
#define _SBDC_H_

#include "utypes.h"

struct sbdc_mode {
    u32 reserved :29;
    u32 attention_enable :1;
    u32 enable :1;
    u32 reset :1;
};

struct sbdc_debug {
    u32 reserved :29;
    u32 rstate :3;
};

struct sbdc_regs {
    struct sbdc_mode mode;
    struct sbdc_debug debug;
};

#endif
