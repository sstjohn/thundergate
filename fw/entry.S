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
.extern test

.text
.globl _start
.cfi_startproc
.ent _start
.type _start, @function
_start:
.frame fp,16,ra
    addiu   sp,sp,-16
.cfi_def_cfa_offset 16
    sw      ra,12(sp)
.cfi_offset 31,-4
    sw      fp,8(sp)
.cfi_offset 30, -8
    move    fp,sp
.cfi_def_cfa_register 30
begin:
    and s0,s0,$zero
    ori s0,s0,0xffff
reset:
    lw s1,(counter)
    addiu s1,1
    sw s1,(counter)
    jal test
    nop
    and s2,s2,$zero
loop:
    addiu s2,1
    beq s0,s2,reset
    nop
    j loop
    nop
failed:
.set noat
    and $1,$1,$0
    lui $1,0xFFFF
    ori $1,$1,0xDEAD
    nop
    break
    nop
    move sp,fp
.cfi_def_cfa_register 29
    lw ra,12(sp)
.cfi_restore 31
    lw fp,8(sp)
.cfi_restore 30
    addiu sp,sp,16
.cfi_def_cfa_offset 0
    j ra
    nop
.cfi_endproc
.end _start

.data 
.align 4
counter: .word 0
test_string: .asciiz "test string"