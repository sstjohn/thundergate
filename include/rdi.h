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

#ifndef _RDI_H_
#define _RDI_H_

struct rdi_mode {
    u32 reserved :27;
    u32 illegal_return_ring_size :1;
    u32 frame_size_too_large_for_bd :1;
    u32 reserved2 :1;
    u32 enable :1;
    u32 reset :1;
};

struct rdi_status {
    u32 reserved :27;
    u32 illegal_return_ring_size :1;
    u32 frame_size_too_large_for_bd :1;
    u32 reserved2 :3;
};

struct rcb_registers {
    u32 host_addr_hi;
    u32 host_addr_low;
    struct {
        u32 ring_size :16;
        u32 max_frame_len :14;
        u32 disable_ring :1;
        u32 reserved :1;
    };
    u32 nic_addr;
};

struct rdi_regs {
    struct rdi_mode mode;
    struct rdi_status status;
    u32 unknown[14];
    struct rcb_registers jumbo_rcb;
    struct rcb_registers std_rcb;
    struct rcb_registers mini_rcb;
    u32 local_jumbo_rbd_ci;
    u32 local_std_rbd_ci;
    u32 local_mini_rbd_ci;
    u32 unknown2;
    u32 local_rr_pi[16];
    u32 hw_diag;
};

#endif
