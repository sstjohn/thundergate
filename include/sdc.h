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

#ifndef _SDC_H_
#define _SDC_H_

#include "utypes.h"

struct sdc_mode {
    u32 reserved :27;
    u32 cdelay :1;
    u32 reserved2 :2;
    u32 enable :1;
    u32 reset :1;
};

struct sdc_pre_dma_command_exchange {
    u32 pass :1;
    u32 skip :1;
    u32 end_of_frag :1;
    u32 reserved :17;
    u32 head_txmbuf_ptr :6;
    u32 tail_txmbuf_ptr :6;
};

struct sdc_regs {
    struct sdc_mode mode;
    u32 unknown;
    struct sdc_pre_dma_command_exchange pre_dma_command_exchange;
};

#endif
