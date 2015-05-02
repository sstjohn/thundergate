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

#ifndef _WDMA_H_
#define _WDMA_H_

#include "utypes.h"

struct wdma_mode {
    u32 reserved :2;
    u32 status_tag_fix_enable :1;
    u32 reserved2 :10;
    u32 swap_test_en :1;
    u32 hc_byte_swap :1;
    u32 hc_word_swap :1;
    u32 bd_byte_swap :1;
    u32 bd_word_swap :1;
    u32 data_byte_swap :1;
    u32 data_word_swap :1;
    u32 software_byte_swap_control :1;
    u32 receive_accelerate_mode :1;
    u32 write_dma_local_memory :1;
    u32 write_dma_pci_fifo_overwrite_attention_enable :1;
    u32 write_dma_pci_fifo_underrun_attention_enable :1;
    u32 write_dma_pci_fifo_overrun_attention_enable :1;
    u32 write_dma_pci_host_address_overflow_error_attention_enable :1;
    u32 write_dma_pci_parity_error_attention_enable :1;
    u32 write_dma_pci_master_abort_attention_enable :1;
    u32 write_dma_pci_target_abort_attention_enable :1;
    u32 enable :1;
    u32 reset :1;
};

struct wdma_status {
    u32 reserved :22;
    u32 write_dma_local_memory_read_longer_than_dma_length_error :1;
    u32 write_dma_pci_fifo_overwrite_error :1;
    u32 write_dma_pci_fifo_underrun_error :1;
    u32 write_dma_pci_fifo_overrun_error :1;
    u32 write_dma_pci_host_address_overflow_error :1;
    u32 reserved1 :5;
};

struct wdma_regs {
    struct wdma_mode mode;
    struct wdma_status status;
};

#endif
