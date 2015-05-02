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

#ifndef _RBDRULES_H
#define _RBDRULES_H

#include "../include/utypes.h"

struct rbd_rule {
    u32 enabled :1;
    u32 and_with_next :1;
    u32 p1 :1;
    u32 p2 :1;
    u32 p3 :1;
    u32 mask :1;
    u32 discard :1;
    u32 map :1;
    u32 reserved :6;
    u32 op :2;
    u32 header :3;
    u32 frame_class :5;
    u32 offset :8;
};

struct rbd_value_mask {
    u16 mask;
    u16 value;
};

#define RBD_RULE_OP_EQUAL 0
#define RBD_RULE_OP_NOTEQUAL 1
#define RBD_RULE_OP_GREATER 2
#define RBD_RULE_OP_LESS 3
#define RBD_RULE_HDR_FRAME 0
#define RBD_RULE_HDR_IP 1
#define RBD_RULE_HDR_TCP 2
#define RBD_RULE_HDR_UDP 3
#define RBD_RULE_HDR_DATA 4

#endif
