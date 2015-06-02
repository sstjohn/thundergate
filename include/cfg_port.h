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

#ifndef _CFG_PORT_H_
#define _CFG_PORT_H_

struct cfg_port_cap_ctrl {
	u32 unknown4 :28;
	u32 pm_en :1;
	u32 vpd_en :1;
	u32 msi_en :1;
	u32 msix_en :1;
};

struct cfg_port_bar_ctrl {
	u32 unknown12 :20;
	u32 rom_bar_sz :4;
	u32 unknown4 :4;
	u32 bar0_sz :4;
};

struct cfg_port_regs {
    u32 ofs_00;
    u32 ofs_04;
    struct cfg_port_bar_ctrl bar_ctrl;
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

    struct cfg_port_cap_ctrl cap_ctrl;
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
    
    u32 ofs_200;
    u32 ofs_204;
    u32 ofs_208;
    u32 ofs_20c;

    u32 ofs_210;
    u32 ofs_214;
    u32 ofs_218;
    u32 ofs_21c;

    u32 ofs_220;
    u32 ofs_224;
    u32 ofs_228;
    u32 ofs_22c;

    u32 ofs_230;
    u32 ofs_234;
    u32 ofs_238;
    u32 ofs_23c;

    u32 ofs_240;
    u32 ofs_244;
    u32 ofs_248;
    u32 ofs_24c;

    u32 ofs_250;
    u32 ofs_254;
    u32 ofs_258;
    u32 ofs_25c;

    u32 ofs_260;
    u32 ofs_264;
    u32 ofs_268;
    u32 ofs_26c;

    u32 ofs_270;
    u32 ofs_274;
    u32 ofs_278;
    u32 ofs_27c;

    u32 ofs_280;
    u32 ofs_284;
    u32 ofs_288;
    u32 ofs_28c;

    u32 ofs_290;
    u32 ofs_294;
    u32 ofs_298;
    u32 ofs_29c;

    u32 ofs_2a0;
    u32 ofs_2a4;
    u32 ofs_2a8;
    u32 ofs_2ac;

    u32 ofs_2b0;
    u32 ofs_2b4;
    u32 ofs_2b8;
    u32 ofs_2bc;

    u32 ofs_2c0;
    u32 ofs_2c4;
    u32 ofs_2c8;
    u32 ofs_2cc;

    u32 ofs_2d0;
    u32 ofs_2d4;
    u32 ofs_2d8;
    u32 ofs_2dc;

    u32 ofs_2e0;
    u32 ofs_2e4;
    u32 ofs_2e8;
    u32 ofs_2ec;

    u32 ofs_2f0;
    u32 ofs_2f4;
    u32 ofs_2f8;
    u32 ofs_2fc;
    
    u32 ofs_300;
    u32 ofs_304;
    u32 ofs_308;
    u32 ofs_30c;

    u32 ofs_310;
    u32 ofs_314;
    u32 ofs_318;
    u32 ofs_31c;

    u32 ofs_320;
    u32 ofs_324;
    u32 ofs_328;
    u32 ofs_32c;

    u32 ofs_330;
    u32 ofs_334;
    u32 ofs_338;
    u32 ofs_33c;

    u32 ofs_340;
    u32 ofs_344;
    u32 ofs_348;
    u32 ofs_34c;

    u32 ofs_350;
    u32 ofs_354;
    u32 ofs_358;
    u32 ofs_35c;

    u32 ofs_360;
    u32 ofs_364;
    u32 ofs_368;
    u32 ofs_36c;

    u32 ofs_370;
    u32 ofs_374;
    u32 ofs_378;
    u32 ofs_37c;

    u32 ofs_380;
    u32 ofs_384;
    u32 ofs_388;
    u32 ofs_38c;

    u32 ofs_390;
    u32 ofs_394;
    u32 ofs_398;
    u32 ofs_39c;

    u32 ofs_3a0;
    u32 ofs_3a4;
    u32 ofs_3a8;
    u32 ofs_3ac;

    u32 ofs_3b0;
    u32 ofs_3b4;
    u32 ofs_3b8;
    u32 ofs_3bc;

    u32 ofs_3c0;
    u32 ofs_3c4;
    u32 ofs_3c8;
    u32 ofs_3cc;

    u32 ofs_3d0;
    u32 ofs_3d4;
    u32 ofs_3d8;
    u32 ofs_3dc;

    u32 ofs_3e0;
    u32 ofs_3e4;
    u32 ofs_3e8;
    u32 ofs_3ec;

    u32 ofs_3f0;
    u32 ofs_3f4;
    u32 ofs_3f8;
    u32 ofs_3fc;
};

#endif
