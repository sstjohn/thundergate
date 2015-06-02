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

#ifndef _CR_PORT_H_
#define _CR_PORT_H_

struct cr_port_regs {
    u32 ofs_00;
    u32 ofs_04;
    u32 ofs_08;
    u32 ofs_0c;

    u32 ofs_10;
    u32 ofs_14;
    u32 ofs_18;
    u32 ofs_1c;

    u32 ofs_20;
    u32 ofs_24;
    u32 ofs_28;
    u32 ofs_2c;

    u32 ofs_30;
    u32 ofs_34;
    u32 ofs_38;
    u32 ofs_3c;

    u32 ofs_40;
    u32 ofs_44;
    u32 ofs_48;
    u32 ofs_4c;

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
    
    u32 ofs_100;
    u32 ofs_104;
    u32 ofs_108;
    u32 ofs_10c;

    u32 ofs_110;
    u32 ofs_114;
    u32 ofs_118;
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
};

#endif
