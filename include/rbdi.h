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

#ifndef _RBDI_H_
#define _RBDI_H_

struct rbdi_mode {
    union {
        struct {
            u32 reserved :29;
            u32 receive_bds_available_on_disabled_rbd_ring_attn_enable :1;
            u32 enable :1;
            u32 reset :1;
        };
        u32 word;
    };
};

struct rbdi_status {
    u32 reserved :29;
    u32 receive_bds_available_on_disabled_rbd_ring :1;
    u32 reserved2 :2;
};

struct rbdi_ring_replenish_threshold {
    u32 reserved :22;
    u32 count :10;
};

struct rbdi_regs {
    struct rbdi_mode mode;
    struct rbdi_status status;
    u32 local_jumbo_rbd_pi;
    u32 local_std_rbd_pi;
    u32 local_mini_rbd_pi;
    struct rbdi_ring_replenish_threshold mini_ring_replenish_threshold;
    struct rbdi_ring_replenish_threshold std_ring_replenish_threshold;
    struct rbdi_ring_replenish_threshold jumbo_ring_replenish_threshold;
    u32 reserved[0xe0 >> 2];
    struct rbdi_ring_replenish_threshold std_ring_replenish_watermark;
    struct rbdi_ring_replenish_threshold jumbo_ring_replenish_watermark;
};

#endif
