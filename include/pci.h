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

#ifndef _PCI_REGS_H_
#define _PCI_REGS_H_

struct pci_status {
    union {
        struct {
            u16 detected_parity_error :1;
            u16 signaled_system_error :1;
            u16 received_master_abort :1;
            u16 received_target_abort :1;
            u16 signaled_target_abort :1;
            u16 devsel_timing :2;
            u16 master_data_parity_error :1;
            u16 fast_back_to_back_capable :1;
            u16 reserved :1;
            u16 sixty_six_mhz_capable :1;
            u16 capabilities_list :1;
            u16 interrupt_status :1;
            u16 reserved2 :3;
        };
        u16 word;
    };
};

struct pci_command {
    union {
	struct {
	    u16 reserved3 :5;
	    u16 interrupt_disable :1;
	    u16 fast_back_to_back_enable :1;
	    u16 system_error_enable :1;
	    u16 stepping_control :1;
	    u16 parity_error_enable :1;
	    u16 vga_palette_snoop :1;
	    u16 memory_write_and_invalidate :1;
	    u16 special_cycles :1;
	    u16 bus_master :1;
	    u16 memory_space :1;
	    u16 io_space :1;
	};
    	u16 word;
    };
};

struct pci_pm_cap {
    u32 pme_support :5;
    u32 d2_support :1;
    u32 d1_support :1;
    u32 aux_current :3;
    u32 dsi :1;
    u32 reserved6 :1;
    u32 pme_clock :1;
    u32 version :3;
    u32 next_cap :8;
    u32 cap_id :8;
};

struct pci_pm_ctrl_status {
        u32 pm_data :8;
        u32 reserved7 :8;
        u32 pme_status :1;
        u32 data_scale :2;
        u32 data_select :4;
        u32 pme_enable :1;
        u32 reserved8 :4;
        u32 no_soft_reset :1;
        u32 reserved9 :1;
        u32 power_state :2;
};

struct pci_msi_cap_hdr {
    u32 msi_control :7;
    u32 msi_pvmask_capable :1;
    u32 sixty_four_bit_addr_capable :1;
    u32 multiple_message_enable :3;
    u32 multiple_message_capable :3;
    u32 msi_enable :1;
    u32 next_cap :8;
    u32 cap_id :8;
};

struct pci_misc_host_ctrl {
    u32 asic_rev_id :16;
    u32 unused :6;
    u32 enable_tagged_status_mode :1;
    u32 mask_interrupt_mode :1;
    u32 enable_indirect_access :1;
    u32 enable_register_word_swap :1;
    u32 enable_clock_control_register_rw_cap :1;
    u32 enable_pci_state_register_rw_cap :1;
    u32 enable_endian_word_swap :1;
    u32 enable_endian_byte_swap :1;
    u32 mask_interrupt :1;
    u32 clear_interrupt :1;
};

struct pci_dma_rw_ctrl {
    u32 reserved25 :7;
    u32 cr_write_watermark :3;
    u32 dma_write_watermark :3;
    u32 reserved10 :9;
    u32 card_reader_dma_read_mrrs :3;
    u32 dma_read_mrrs_for_slow_speed :3;
    u32 reserved1 :3;
    u32 disable_cache_alignment :1;
};

struct pci_state {
    u32 reserved14 :16;
    u32 unused4 :1;
    u32 reserved15 :2;
    u32 pci_vaux_present :1;
    u32 unused5 :3;
    u32 flat_mode :1;
    u32 reserved16 :1;
    u32 rom_retry_enable :1;
    u32 rom_enable :1;
    u32 bus_32_bit :1;
    u32 bus_speed_hi :1;
    u32 conv_pci_mode :1;
    u32 int_not_active :1;
    u32 force_reset :1;
};

struct pci_device_id {
    u32 did :16;
    u32 vid :16;
};

struct pci_class_code_rev_id {
    u32 class_code :24;
    u32 rev_id :8;
};

struct pci_regs {
    struct {
        u32 did :16;
        u32 vid :16;
    };
    struct {
        struct pci_status status;
        struct pci_command command;
    };
    struct pci_class_code_rev_id class_code_rev_id;
    struct {
        u8 bist :8;
        u32 hdr_type :8;
        u32 lat_timer :8;
        u32 cache_line_sz :8;
    };
    u32 bar0_hi;
    u32 bar0_low;
    u32 bar1_hi;
    u32 bar1_low;
    u32 bar2_hi;
    u32 bar2_low;
    u32 cardbus_cis_ptr;
    struct {
        u16 ssid;
        u16 svid;
    };
    u32 rombar; 
    struct {
        u32 reserved1 :24;
        u32 cap_ptr :8;
    };
    u32 reserved2;
    struct {
        u32 max_lat :8;
        u32 min_gnt :8;
        u32 int_pin :8;
        u32 int_line :8;
    }; 
    /* 0x40 */
    u64 int_mailbox;
    struct pci_pm_cap pm_cap;
    struct pci_pm_ctrl_status pm_ctrl_status;
    /* 0x50 */
    u32 unknown2[2];
    struct pci_msi_cap_hdr msi_cap_hdr;
    u32 msi_lower_address;
    /* 0x60 */
    u32 msi_upper_address;
    u32 msi_data;
    struct pci_misc_host_ctrl misc_host_ctrl;
    struct pci_dma_rw_ctrl dma_rw_ctrl;
    /* 0x70 */
    struct pci_state state;
    u32 reset_counters_initial_values;
    u32 reg_base_addr;
    u32 mem_base_addr;
    /* 0x80 */
    u32 reg_data;
    u32 mem_data;
    u32 unknown3[2];
    /* 0x90 */
    u32 misc_local_control;
    u32 unknown4;
    u32 std_ring_prod_ci_hi;
    u32 std_ring_prod_ci_low;
    /* 0xa0 */
    u32 recv_ret_ring_ci_hi;
    u32 recv_ret_ring_ci_low;
};

#endif
