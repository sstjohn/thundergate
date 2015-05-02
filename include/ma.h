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

#ifndef _MA_H_
#define _MA_H_

struct ma_mode {
    union {
        struct {
            u32 tx_mbuf_cfg :2;
            u32 cpu_pipeline_request_disable :1;
            u32 low_latency_enable :1;
            
            u32 fast_path_read_disable :1;
            u32 reserved21 :6;
            u32 dmaw2_addr_trap :1;
            
            u32 bufman_addr_trap :1;
            u32 txbd_addr_trap :1;
            u32 sdc_dmac_trap :1;
            u32 sdi_addr_trap :1;

            u32 mcf_addr_trap :1;
            u32 hc_addr_trap :1;
            u32 dc_addr_trap :1;
            u32 rdi2_addr_trap :1;
            
            u32 rdi1_addr_trap :1;
            u32 rq_addr_trap :1;
            u32 dmar2_addr_trap :1;
            u32 pci_addr_trap :1;
            
            u32 tx_risc_addr_trap :1;
            u32 rx_risc_addr_trap :1;
            u32 dmar1_addr_trap :1;
            u32 dmaw1_addr_trap :1;
            
            u32 rx_mac_addr_trap :1;
            u32 tx_mac_addr_trap :1;
            u32 enable :1;
            u32 reset :1;
        };
        u32 word;
    };
};

#define MA_ALL_TRAPS 0x00111d7c

struct ma_status {
    u32 reserved :11;
    u32 dmaw2_addr_trap :1;
    u32 reserved2 :3;
    u32 sdi_addr_trap :1;
    u32 reserved3 :3;
    u32 rdi2_addr_trap :1;
    u32 rdi1_addr_trap :1;
    u32 rq_addr_trap :1;
    u32 reserved4 :1;
    u32 pci_addr_trap :1;
    u32 reserved5 :1;
    u32 rx_risc_addr_trap :1;
    u32 dmar1_addr_trap :1;
    u32 dmaw1_addr_trap :1;
    u32 rx_mac_addr_trap :1;
    u32 tx_mac_addr_trap :1;
    u32 reserved6 :2;
};


struct ma_regs {
    struct ma_mode mode;
    struct ma_status status;
    u32 trap_addr_low;
    u32 trap_addr_hi;
};

#endif
