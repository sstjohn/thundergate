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
.extern _edata
.extern _end
.extern test
.text
    andi    sp,r0,0
    lui     sp,0x801
    andi    ra,r0,0

    addiu   sp,sp,-16
    sw      ra,12(sp)
    sw      fp,8(sp)
    move    fp,sp
begin:
    lui s0,%hi(_edata)
    addi s0,%lo(_edata)
    lui s1,%hi(_end)
    addi s1,%lo(_end)
1:  beq s0,s1,2f
    nop
    sw r0,0(s0)
    addiu s0,s0,4
    b 1b
    nop
2:  jal test
    ori v0,r0,1
    beqz v0,2b
    nop
failed:
.set noat
    and $1,$1,$0
    lui $1,0xFFFF
    ori $1,$1,0xDEAD
    nop
    break
    
.data 
.align 4