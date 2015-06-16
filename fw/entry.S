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

#include "regdef.h"
.set noreorder
.extern init
.text
_start:
    addiu sp, sp, (-24)
    sw ra, 20(sp)
loop:
    jal init
    nop
    bnez v0,failed
    nop
    b _start
    nop
failed:
.set noat
    and $1,$1,$0
    lui $1,0xFFFF
    ori $1,$1,0xDEAD
    nop
    break
