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

#ifndef _PCIE_ALT_H_
#define _PCIE_ALT_H_

struct pcie_pl_lo_regs {
    u32 phyctl0;
    u32 phyctl1;
    u32 phyctl2;
    u32 phyctl3;
    u32 phyctl4;
    u32 phyctl5;
};

struct pcie_dl_lo_ftsmax {
    u32 unknown :24;
    u32 val :8;
};

struct pcie_dl_lo_regs {
    u32 unknown0;
    u32 unknown4;
    u32 unknown8;
    struct pcie_dl_lo_ftsmax ftsmax;
};

struct pcie_alt_regs {
    union {
        struct pcie_dl_lo_regs dll;
        struct pcie_pl_lo_regs pll;
    };
};

#endif
