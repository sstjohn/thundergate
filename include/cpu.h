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

#ifndef _CPU_H_
#define _CPU_H_

struct cpu_mode {
    u32 reserved :17;
    u32 register_addr_trap_halt_en :1;
    u32 memory_addr_trap_halt_en :1;
    u32 invalid_instruction_fetch_halt_en :1;

    u32 invalid_data_access_halt_en :1;
    u32 halt :1;
    u32 reserved2 :1;
    u32 reserved3 :1;
    
    u32 watchdog_interrupt_en :1;
    u32 rom_fail :1;
    u32 reserved4 :1;
    u32 reserved5 :1;

    u32 page_0_instr_halt_en :1;
    u32 page_0_data_halt_en :1;
    u32 single_step :1;
    u32 reset :1;
};

struct cpu_status {
    union {
        struct {
            u32 blocking_read :1;
            u32 ma_request_fifo_overflow :1;
            u32 ma_data_bytemask_fifo_overflow :1;
            u32 ma_outstanding_read_fifo_overflow :1;
            u32 ma_outstanding_write_fifo_overflow :1;
            u32 reserved :11;
            u32 instruction_fetch_stall :1;
            u32 data_access_stall :1;
            u32 reserved2 :1;
            u32 interrupt_received :1;
            u32 reserved3 :1;
            u32 halted :1;
            u32 register_address_trap :1;
            u32 memory_address_trap :1;
            u32 bad_memory_alignment :1;
            u32 invalid_instruction_fetch :1;
            u32 invalid_data_access :1;
            u32 page_0_instr_reference :1;
            u32 page_0_data_reference :1;
            u32 invalid_instruction :1;
            u32 halt_instruction_executed :1;
            u32 hardware_breakpoint :1;
        };
        u32 word;
    };
};

struct cpu_event_mask {
    u32 unknown :18;
    u32 reserved :1;
    u32 interrupt :1;
    u32 spad_underflow :1;
    u32 soft_halted :1;
    u32 reserved2 :1;
    u32 fio_abort :1;
    u32 align_halted :1;
    u32 bad_pc_halted  :1;
    u32 bad_data_addr_halted :1;
    u32 page_0_instr_halted :1;
    u32 page_0_data_halted :1;
    u32 bad_instr_halted :1;
    u32 reserved3 :1;
    u32 breakpoint :1;
};

struct cpu_breakpoint {
    union {
        u32 address;
        struct {
            u32 addr_word :30;
            u32 reserved :1;
            u32 disabled :1;
        };
    };
};

struct cpu_last_branch_address {
    u32 addr_word :30;
    u32 type :1;
    u32 reserved :1;
};

struct cpu_regs {
    struct cpu_mode mode;
    struct cpu_status status;
    struct cpu_event_mask mask;
    u32 ofs_0c;
    
    u32 ofs_10;
    u32 ofs_14;
    u32 ofs_18;
    u32 pc;
    
    u32 instruction;
    u32 spad_uflow;
    u32 watchdog_enable;
    u32 watchdog_vector;
    
    u32 watchdog_saved_pc;
    struct cpu_breakpoint breakpoint;
    u32 ofs_38;
    u32 ofs_3c;

    u32 ofs_40;
    u32 watchdog_saved_state;
    struct cpu_last_branch_address lba;
    u32 spad_uflow_set;
    
    u32 ofs_50;
    u32 ofs_54;
    u32 ofs_58;
    u32 ofs_5c;

    u32 ofs_60;
    u32 ofs_64;
    u32 ofs_68;
    u32 ofs_6c;

    u32 ofs_70;
    u32 ofs_74;
    u32 ofs_78;
    u32 ofs_7c;

    u32 ofs_80;
    u32 ofs_84;
    u32 ofs_88;
    u32 ofs_8c;

    u32 ofs_90;
    u32 ofs_94;
    u32 ofs_98;
    u32 ofs_9c;

    u32 ofs_a0;
    u32 ofs_a4;
    u32 ofs_a8;
    u32 ofs_ac;

    u32 ofs_b0;
    u32 ofs_b4;
    u32 ofs_b8;
    u32 ofs_bc;

    u32 ofs_c0;
    u32 ofs_c4;
    u32 ofs_c8;
    u32 ofs_cc;
 
    u32 ofs_d0;
    u32 ofs_d4;
    u32 ofs_d8;
    u32 ofs_dc;

    u32 ofs_e0;
    u32 ofs_e4;
    u32 ofs_e8;
    u32 ofs_ec;

    u32 ofs_f0;
    u32 ofs_f4;
    u32 ofs_f8;
    u32 ofs_fc;
    
    u32 vcpu_status;
    u32 device_configuration;
    u32 vcpu_holding;
    u32 vcpu_data;

    u32 vcpu_debug;
    u32 vcpu_config_shadow_1;
    u32 vcpu_config_shadow_2;
    u32 ofs_11c;

    u32 ofs_120;
    u32 ofs_124;
    u32 ofs_128;
    u32 ofs_12c;

    u32 ofs_130;
    u32 ofs_134;
    u32 ofs_138;
    u32 ofs_13c;

    u32 ofs_140;
    u32 ofs_144;
    u32 ofs_148;
    u32 ofs_14c;

    u32 ofs_150;
    u32 ofs_154;
    u32 ofs_158;
    u32 ofs_15c;

    u32 ofs_160;
    u32 ofs_164;
    u32 ofs_168;
    u32 ofs_16c;

    u32 ofs_170;
    u32 ofs_174;
    u32 ofs_178;
    u32 ofs_17c;

    u32 ofs_180;
    u32 ofs_184;
    u32 ofs_188;
    u32 ofs_18c;

    u32 ofs_190;
    u32 ofs_194;
    u32 ofs_198;
    u32 ofs_19c;

    u32 ofs_1a0;
    u32 ofs_1a4;
    u32 ofs_1a8;
    u32 ofs_1ac;

    u32 ofs_1b0;
    u32 ofs_1b4;
    u32 ofs_1b8;
    u32 ofs_1bc;
    
    u32 ofs_1c0;
    u32 ofs_1c4;
    u32 ofs_1c8;
    u32 ofs_1cc;
    
    u32 ofs_1d0;
    u32 ofs_1d4;
    u32 ofs_1d8;
    u32 ofs_1dc;

    u32 ofs_1e0;
    u32 ofs_1e4;
    u32 ofs_1e8;
    u32 ofs_1ec;
    
    u32 ofs_1f0;
    u32 ofs_1f4;
    u32 ofs_1f8;
    u32 ofs_1fc;

    u32 r0;
    u32 r1;
    u32 r2;
    u32 r3;

    u32 r4;
    u32 r5;
    u32 r6;
    u32 r7;

    u32 r8;
    u32 r9;
    u32 r10;
    u32 r11;

    u32 r12;
    u32 r13;
    u32 r14;
    u32 r15;

    u32 r16;
    u32 r17;
    u32 r18;
    u32 r19;

    u32 r20;
    u32 r21;
    u32 r22;
    u32 r23;

    u32 r24;
    u32 r25;
    u32 r26;
    u32 r27;

    u32 r28;
    u32 r29;
    u32 r30;
    u32 r31;
};

#endif
