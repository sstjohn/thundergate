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

#ifndef _MBOX_H_
#define _MBOX_H_

enum known_mailboxes {
    mb_interrupt = 0,
    mb_rbd_standard_producer = 0x68 / 8,
    mb_rbd_rr0_consumer = 0x80 / 8,
    mb_rbd_rr1_consumer = 0x88 / 8,
    mb_rbd_rr2_consumer = 0x90 / 8,
    mb_rbd_rr3_consumer = 0x98 / 8,
    mb_sbd_host_producer = 0x100 / 8,
    mb_sbd_nic_producer = 0x380 / 8,
};

struct mailbox {
    u32 hi;
    u32 low;
};

struct hpmb_regs {
    struct mailbox box[0x200 / 8];
};

struct lpmb_regs {
    struct mailbox box[0x200 / 8];
};

#endif
