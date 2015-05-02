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

#ifndef _RSS_H_
#define _RSS_H_

struct rss_ind_table_1 {
    u32 reserved30 :2;
    u32 table_entry0 :2;
    u32 reserved26 :2;
    u32 table_entry1 :2;
    u32 reserved22 :2;
    u32 table_entry2 :2;
    u32 reserved18 :2;
    u32 table_entry3 :2;
    u32 reserved14 :2;
    u32 table_entry4 :2;
    u32 reserved10 :2;
    u32 table_entry5 :2;
    u32 reserved6 :2;
    u32 table_entry6 :2;
    u32 reserved2 :2;
    u32 table_entry7 :2;
};
struct rss_ind_table_2 {
    u32 reserved30 :2;
    u32 table_entry8 :2;
    u32 reserved26 :2;
    u32 table_entry9 :2;
    u32 reserved22 :2;
    u32 table_entry10 :2;
    u32 reserved18 :2;
    u32 table_entry11 :2;
    u32 reserved14 :2;
    u32 table_entry12 :2;
    u32 reserved10 :2;
    u32 table_entry13 :2;
    u32 reserved6 :2;
    u32 table_entry14 :2;
    u32 reserved2 :2;
    u32 table_entry15 :2;
};
struct rss_ind_table_3 {
    u32 reserved30 :2;
    u32 table_entry16 :2;
    u32 reserved26 :2;
    u32 table_entry17 :2;
    u32 reserved22 :2;
    u32 table_entry18 :2;
    u32 reserved18 :2;
    u32 table_entry19 :2;
    u32 reserved14 :2;
    u32 table_entry20 :2;
    u32 reserved10 :2;
    u32 table_entry21 :2;
    u32 reserved6 :2;
    u32 table_entry22 :2;
    u32 reserved2 :2;
    u32 table_entry23 :2;
};
struct rss_ind_table_4 {
    u32 reserved30 :2;
    u32 table_entry24 :2;
    u32 reserved26 :2;
    u32 table_entry25 :2;
    u32 reserved22 :2;
    u32 table_entry26 :2;
    u32 reserved18 :2;
    u32 table_entry27 :2;
    u32 reserved14 :2;
    u32 table_entry28 :2;
    u32 reserved10 :2;
    u32 table_entry29 :2;
    u32 reserved6 :2;
    u32 table_entry30 :2;
    u32 reserved2 :2;
    u32 table_entry31 :2;
};
struct rss_ind_table_5 {
    u32 reserved30 :2;
    u32 table_entry32 :2;
    u32 reserved26 :2;
    u32 table_entry33 :2;
    u32 reserved22 :2;
    u32 table_entry34 :2;
    u32 reserved18 :2;
    u32 table_entry35 :2;
    u32 reserved14 :2;
    u32 table_entry36 :2;
    u32 reserved10 :2;
    u32 table_entry37 :2;
    u32 reserved6 :2;
    u32 table_entry38 :2;
    u32 reserved2 :2;
    u32 table_entry39 :2;
};
struct rss_ind_table_6 {
    u32 reserved30 :2;
    u32 table_entry40 :2;
    u32 reserved26 :2;
    u32 table_entry41 :2;
    u32 reserved22 :2;
    u32 table_entry42 :2;
    u32 reserved18 :2;
    u32 table_entry43 :2;
    u32 reserved14 :2;
    u32 table_entry44 :2;
    u32 reserved10 :2;
    u32 table_entry45 :2;
    u32 reserved6 :2;
    u32 table_entry46 :2;
    u32 reserved2 :2;
    u32 table_entry47 :2;
};
struct rss_ind_table_7 {
    u32 reserved30 :2;
    u32 table_entry48 :2;
    u32 reserved26 :2;
    u32 table_entry49 :2;
    u32 reserved22 :2;
    u32 table_entry50 :2;
    u32 reserved18 :2;
    u32 table_entry51 :2;
    u32 reserved14 :2;
    u32 table_entry52 :2;
    u32 reserved10 :2;
    u32 table_entry53 :2;
    u32 reserved6 :2;
    u32 table_entry54 :2;
    u32 reserved2 :2;
    u32 table_entry55 :2;
};
struct rss_ind_table_8 {
    u32 reserved30 :2;
    u32 table_entry56 :2;
    u32 reserved26 :2;
    u32 table_entry57 :2;
    u32 reserved22 :2;
    u32 table_entry58 :2;
    u32 reserved18 :2;
    u32 table_entry59 :2;
    u32 reserved14 :2;
    u32 table_entry60 :2;
    u32 reserved10 :2;
    u32 table_entry61 :2;
    u32 reserved6 :2;
    u32 table_entry62 :2;
    u32 reserved2 :2;
    u32 table_entry63 :2;
};
struct rss_ind_table_9 {
    u32 reserved30 :2;
    u32 table_entry64 :2;
    u32 reserved26 :2;
    u32 table_entry65 :2;
    u32 reserved22 :2;
    u32 table_entry66 :2;
    u32 reserved18 :2;
    u32 table_entry67 :2;
    u32 reserved14 :2;
    u32 table_entry68 :2;
    u32 reserved10 :2;
    u32 table_entry69 :2;
    u32 reserved6 :2;
    u32 table_entry70 :2;
    u32 reserved2 :2;
    u32 table_entry71 :2;
};

struct rss_ind_table_10 {
    u32 reserved30 :2;
    u32 table_entry72 :2;
    u32 reserved26 :2;
    u32 table_entry73 :2;
    u32 reserved22 :2;
    u32 table_entry74 :2;
    u32 reserved18 :2;
    u32 table_entry75 :2;
    u32 reserved14 :2;
    u32 table_entry76 :2;
    u32 reserved10 :2;
    u32 table_entry77 :2;
    u32 reserved6 :2;
    u32 table_entry78 :2;
    u32 reserved2 :2;
    u32 table_entry79 :2;
};
struct rss_ind_table_11 {
    u32 reserved30 :2;
    u32 table_entry80 :2;
    u32 reserved26 :2;
    u32 table_entry81 :2;
    u32 reserved22 :2;
    u32 table_entry82 :2;
    u32 reserved18 :2;
    u32 table_entry83 :2;
    u32 reserved14 :2;
    u32 table_entry84 :2;
    u32 reserved10 :2;
    u32 table_entry85 :2;
    u32 reserved6 :2;
    u32 table_entry86 :2;
    u32 reserved2 :2;
    u32 table_entry87 :2;
};
struct rss_ind_table_12 {
    u32 reserved30 :2;
    u32 table_entry88 :2;
    u32 reserved26 :2;
    u32 table_entry89 :2;
    u32 reserved22 :2;
    u32 table_entry90 :2;
    u32 reserved18 :2;
    u32 table_entry91 :2;
    u32 reserved14 :2;
    u32 table_entry92 :2;
    u32 reserved10 :2;
    u32 table_entry93 :2;
    u32 reserved6 :2;
    u32 table_entry94 :2;
    u32 reserved2 :2;
    u32 table_entry95 :2;
};
struct rss_ind_table_13 {
    u32 reserved30 :2;
    u32 table_entry96 :2;
    u32 reserved26 :2;
    u32 table_entry97 :2;
    u32 reserved22 :2;
    u32 table_entry98 :2;
    u32 reserved18 :2;
    u32 table_entry99 :2;
    u32 reserved14 :2;
    u32 table_entry100 :2;
    u32 reserved10 :2;
    u32 table_entry101 :2;
    u32 reserved6 :2;
    u32 table_entry102 :2;
    u32 reserved2 :2;
    u32 table_entry103 :2;
};
struct rss_ind_table_14 {
    u32 reserved30 :2;
    u32 table_entry104 :2;
    u32 reserved26 :2;
    u32 table_entry105 :2;
    u32 reserved22 :2;
    u32 table_entry106 :2;
    u32 reserved18 :2;
    u32 table_entry107 :2;
    u32 reserved14 :2;
    u32 table_entry108 :2;
    u32 reserved10 :2;
    u32 table_entry109 :2;
    u32 reserved6 :2;
    u32 table_entry110 :2;
    u32 reserved2 :2;
    u32 table_entry111 :2;
};
struct rss_ind_table_15 {
    u32 reserved30 :2;
    u32 table_entry112 :2;
    u32 reserved26 :2;
    u32 table_entry113 :2;
    u32 reserved22 :2;
    u32 table_entry114 :2;
    u32 reserved18 :2;
    u32 table_entry115 :2;
    u32 reserved14 :2;
    u32 table_entry116 :2;
    u32 reserved10 :2;
    u32 table_entry117 :2;
    u32 reserved6 :2;
    u32 table_entry118 :2;
    u32 reserved2 :2;
    u32 table_entry119 :2;
};
struct rss_ind_table_16 {
    u32 reserved30 :2;
    u32 table_entry120 :2;
    u32 reserved26 :2;
    u32 table_entry121 :2;
    u32 reserved22 :2;
    u32 table_entry122 :2;
    u32 reserved18 :2;
    u32 table_entry123 :2;
    u32 reserved14 :2;
    u32 table_entry124 :2;
    u32 reserved10 :2;
    u32 table_entry125 :2;
    u32 reserved6 :2;
    u32 table_entry126 :2;
    u32 reserved2 :2;
    u32 table_entry127 :2;
};
struct rss_hash_key {
    u32 byte1 :8;
    u32 byte2 :8;
    u32 byte3 :8;
    u32 byte4 :8;
};
struct rmac_programmable_ipv6_extension_header {
    u32 hdr_type2_en :1;
    u32 hdr_type1_en :1;
    u32 reserved16 :14;
    u32 hdr_type2 :8;
    u32 hdr_type1 :8;
};

struct rss_regs {
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

    struct rss_ind_table_1 ind_table_1;
    struct rss_ind_table_2 ind_table_2;
    struct rss_ind_table_3 ind_table_3;
    struct rss_ind_table_4 ind_table_4;

    struct rss_ind_table_5 ind_table_5;
    struct rss_ind_table_6 ind_table_6;
    struct rss_ind_table_7 ind_table_7;
    struct rss_ind_table_8 ind_table_8;

    struct rss_ind_table_9 ind_table_9;
    struct rss_ind_table_10 ind_table_10;
    struct rss_ind_table_11 ind_table_11;
    struct rss_ind_table_12 ind_table_12;

    struct rss_ind_table_13 ind_table_13;
    struct rss_ind_table_14 ind_table_14;
    struct rss_ind_table_15 ind_table_15;
    struct rss_ind_table_16 ind_table_16;

    struct rss_hash_key hash_key_0;
    struct rss_hash_key hash_key_1;
    struct rss_hash_key hash_key_2;
    struct rss_hash_key hash_key_3;

    struct rss_hash_key hash_key_4;
    struct rss_hash_key hash_key_5;
    struct rss_hash_key hash_key_6;
    struct rss_hash_key hash_key_7;

    struct rss_hash_key hash_key_8;
    struct rss_hash_key hash_key_9;
    u32 ofs_98;
    u32 ofs_9c;

    struct rmac_programmable_ipv6_extension_header rmac_ipv6_ext_hdr;
};
#endif
