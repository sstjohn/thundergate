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

#ifndef _NVRAM_H_
#define _NVRAM_H_

#include "utypes.h"

#define TG3_MAGIC 0x669955aa
#define CRC32_POLYNOMIAL 0xEDB88320

#define TG3_IMAGE_TYPE_PXE          0
#define TG3_IMAGE_TYPE_ASF_INIT     1

#define TG3_IMAGE_TYPE(x) ((x) >> 24)
#define TG3_IMAGE_EXE_A_MASK 0x00800000
#define TG3_IMAGE_EXE_B_MASK 0x00400000
#define TG3_IMAGE_LEN(x) (((x) & 0x3fffff) << 2)

struct nvram_dir_item {
    u32 sram_start;
    u32 typelen;
    u32 nvram_start;
}; 

#define TG3_FEAT_ASF 0x80
#define TG3_FEAT_PXE 0x02

struct nvram_header {
    struct {
        u32 mgaic;
        u32 bc_sram_start;
        u32 bc_words;
        u32 bc_nvram_start;
        u32 crc;
    } bs;
    struct nvram_dir_item directory[8];
    struct {
        u16 len;
        u8 dir_cksum;
        u8 rev;
        u32 _unused;
        u8 mac_address[8];
        char partno[16];
        char partrev[2];
        u16 bc_rev;
        u8 mfg_date[4];
        u16 mba_vlan_p1;
        u16 mba_vlan_p2;
        u16 pci_did;
        u16 pci_vid;
        u16 pci_ssid;
        u16 pci_svid;
        u16 cpu_mhz;
        u8 smbus_addr1;
        u8 smbus_addr0;
        u8 mac_backup[8];
        u8 mac_backup_p2[8];
        u32 power_dissipated;
        u32 power_consumed;
        u32 feat_cfg;
        u32 hw_cfg;
        u8 mac_address_p2[8];
        u32 feat_cfg_p2;
        u32 hw_cfg_p2;
        u32 shared_cfg;
        u32 power_budget_0;
        u32 power_budget_1;
        u32 serworks_use;
        u32 serdes_override;
        u16 tpm_nvram_size;
        u16 mac_nvram_size;
        u32 power_budget_2;
        u32 power_budget_3;
        u32 crc;
    } mfg;
};


struct nvram_command {
	u32 policy_error :4;
	u32 atmel_page_size :1;
	u32 reserved1 :4;
	u32 reserved2 :1;
	u32 reserved3 :1;
	u32 reserved4 :1;
	u32 wrsr :1;
	u32 ewsr :1;
	u32 write_disable_command :1;
	u32 write_enable_command :1;
	u32 reserved5 :5;
	u32 atmel_power_of_2_pg_sz :1;
	u32 atmel_pg_sz_rd :1;
	u32 last :1;
	u32 first :1;
	u32 erase :1;
	u32 wr :1;
	u32 doit :1;
	u32 done :1;
	u32 reserved6 :2;
	u32 reset :1;
};

struct nvram_status {
	u32 reserved :1;
	u32 spi_at_read_state :5;
	u32 spi_at_write_state :6;
	u32 spi_st_read_state :4;
	u32 spi_st_write_state :6;
	u32 seq_fsm_state :4;
	u32 see_fsm_state :6;
};

struct nvram_software_arbitration {
	u32 reserved :16;
	u32 req3 :1;
	u32 req2 :1;
	u32 req1 :1;
	u32 req0 :1;
	u32 arb_won3 :1;
	u32 arb_won2 :1;
	u32 arb_won1 :1;
	u32 arb_won0 :1;
	u32 req_clr3 :1;
	u32 req_clr2 :1;
	u32 req_clr1 :1;
	u32 req_clr0 :1;
	u32 req_set3 :1;
	u32 req_set2 :1;
	u32 req_set1 :1;
	u32 req_set0 :1;
};

struct nvram_access {
	u32 reserved :26;
	u32 st_lockup_fix_enable :1;
	u32 disable_auto_eeprom_reset :1;
	u32 eprom_sda_oe_mode :1;
	u32 ate_mode :1;
	u32 write_enable :1;
	u32 enable :1;
};

struct nvram_write1 {
	u32 reserved :16;
	u32 disable_command :8;
	u32 enable_command :8;
};

struct nvram_arbitration_watchdog {
	u32 reserved_31_28 :4;
	u32 reserved_27_24 :4;
	u32 reserved_23_8 :16;
	u32 reserved_7 :1;
	u32 reserved_6 :1;
	u32 reserved_5 :1;
	u32 reserved_4_0 :5;
};

struct nvram_regs {
	struct nvram_command command;
	struct nvram_status status;
	u32 write_data;
	u32 data_address;

	u32 read_data;
	u32 config1;
	u32 config2;
	u32 config3;

	struct nvram_software_arbitration sw_arb;
	struct nvram_access access;
	struct nvram_write1 write1;
	struct nvram_arbitration_watchdog arbitration_watchdog_timer_register;

	u32 address_lockout_boundary;
	u32 address_lockout_address_counter_debug;
        u32 auto_sense_status;
};
#endif
