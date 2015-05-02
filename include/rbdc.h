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

#ifndef _RBDC_H_
#define _RBDC_H_

struct rbdc_mode {
    struct {
        u32 reserved :29;
        u32 attention_enable :1;
        u32 enable :1;
        u32 reset :1;
    };
};

struct rbdc_status {
    u32 reserved :29;
    u32 error :1;
    u32 reserved2 :2;
};

struct rbdc_rbd_pi {
    u32 reserved :23;
    u32 bd_pi :9;
};

struct rbdc_regs {
    struct rbdc_mode mode;
    struct rbdc_status status;
    struct rbdc_rbd_pi jumbo_rbd_pi;
    struct rbdc_rbd_pi std_rbd_pi;
    struct rbdc_rbd_pi mini_rbd_pi;
};

#endif
