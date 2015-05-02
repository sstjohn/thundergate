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

#ifndef _RTSDI_H_
#define _RTSDI_H_

#include "../include/utypes.h"

struct rtsdi_mode {
    u32 reserved :26;
    u32 multiple_segment_enable :1;
    u32 pre_dma_debug :1;
    u32 hardware_pre_dma_enable :1;
    u32 stats_overflow_attention_enable :1;
    u32 enable :1;
    u32 reset :1;
};

struct rtsdi_status {
    u32 reserved :29;
    u32 stats_overflow_attention :1;
    u32 reserved2 :2;
};

struct rtsdi_statistics_control {
    u32 reserved :27;
    u32 zap_statistics :1;
    u32 flush_statistics :1;
    u32 statistics_clear :1;
    u32 faster_update :1;
    u32 statistics_enable :1;
};

struct rtsdi_statistics_mask {
    u32 reserved :31;
    u32 counters_enable_mask :1;
};

struct rtsdi_statistics_increment_mask {
    u32 reserved :8;
    u32 counters_increment_mask_1 :5;
    u32 reserved2 :3;
    u32 counters_increment_mask_2 :16;
};

struct rtsdi_regs {
    struct rtsdi_mode mode;
    struct rtsdi_status status;
    struct rtsdi_statistics_control statistics_control;
    struct rtsdi_statistics_mask statistics_mask;
    
    struct rtsdi_statistics_increment_mask statistics_increment_mask;
    u32 ofs_14;
    u32 ofs_18;
    u32 ofs_1c;

    u32 av_fetch_delay;
    u32 av_fetch_cx_comp;
    u32 av_fetch_l1_comp;
};

#endif
