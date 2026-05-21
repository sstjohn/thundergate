#!/usr/bin/env python3
"""Apply the -mtigon target flag to a GCC source tree.

The Broadcom Tigon3 on-chip MIPS core is not a stock MIPS: it lacks the
lwl/lwr/swl/swr unaligned load/store instructions, the mult/multu and
div/divu instructions, and the HI/LO register file. The historical
gcc-5.1.0-mtigon.patch added a -mtigon flag that suppresses all of them.

That patch was line-context based and no longer applies to a modern GCC.
This script instead re-derives every change *by macro and function name*,
so it survives GCC's source reorganisation between releases. Verified
against GCC 16.1.0.

What it does NOT do, and why:
  * It does not re-add the original patch's mips_init_libfuncs hunk. That
    hunk set the SImode/DImode div and mul libfuncs to __divsi3/__divdi3/
    __muldi3 -- which are already GCC's defaults for a non-vr4120 build.
    It was redundant, and editing a function body is the most fragile kind
    of patch, so it is dropped.
It DOES extend the libgcc build (libgcc/config/mips/t-elf, plus a generated
tg-mulsi3.c). Stock MIPS has hardware mult/div, so libgcc ships no SImode soft
routines; code built with -mtigon calls __mulsi3/__divsi3/__udivsi3/__modsi3/
__umodsi3. The patch pulls in GCC's own generic soft divide (divmod.c,
udivmod.c, udivmodsi4.c) and installs a soft __mulsi3 (GCC's own shift-add
routine, the one it ships for every no-multiply target), and builds libgcc2
itself with -mtigon.

Idempotent: re-running on an already-patched tree is a no-op. Exits non-zero
with a clear message if an expected anchor is missing (a future GCC moved
something), so the build fails loudly rather than silently mis-patching.

Usage:  mtigon-patch.py <path-to-gcc-source-tree>
"""

import os
import re
import sys


def die(msg):
    sys.stderr.write("mtigon-patch: error: %s\n" % msg)
    sys.exit(1)


def info(msg):
    sys.stdout.write("mtigon-patch: %s\n" % msg)


def read(path):
    if not os.path.isfile(path):
        die("not found: %s (is this a GCC source tree?)" % path)
    with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write(text)


# --- gcc/config/mips/mips.h ---------------------------------------------------
# Each boolean macro gains a TIGON guard. The macro body may span several
# lines via backslash continuation; we capture the whole body, flatten it,
# and re-emit it wrapped as ((<body>) <op> <token>) -- which is correct
# regardless of the body's internal structure.
MIPS_H_MACROS = [
    ("TARGET_HARD_FLOAT", "&&", "!TARGET_TIGON"),
    ("TARGET_SOFT_FLOAT", "||", "TARGET_TIGON"),
    ("ISA_HAS_ODD_SPREG", "&&", "!TARGET_TIGON"),
    ("ISA_HAS_MUL3",      "&&", "!TARGET_TIGON"),
    ("ISA_HAS_HILO",      "&&", "!TARGET_TIGON"),
    ("ISA_HAS_MULT",      "&&", "!TARGET_TIGON"),
    ("ISA_HAS_DIV",       "&&", "!TARGET_TIGON"),
    ("ISA_HAS_LWL_LWR",   "&&", "!TARGET_TIGON"),
    ("ISA_HAS_TRUNC_W",   "&&", "!TARGET_TIGON"),
]


def patch_mips_h(tree):
    path = os.path.join(tree, "gcc/config/mips/mips.h")
    text = read(path)
    changed = 0
    for name, op, token in MIPS_H_MACROS:
        pat = re.compile(
            r"(^[ \t]*#[ \t]*define[ \t]+" + re.escape(name) + r"[ \t]+)"
            r"((?:.*\\\n)*.*)",
            re.M,
        )
        m = pat.search(text)
        if not m:
            die("mips.h: macro %s not found" % name)
        prefix, body = m.group(1), m.group(2)
        if "TARGET_TIGON" in body:
            continue  # already patched
        flat = re.sub(r"\\\n", "", body)
        flat = re.sub(r"[ \t]+", " ", flat).strip()
        new = "%s((%s) %s %s)" % (prefix, flat, op, token)
        text = text[: m.start()] + new + text[m.end():]
        changed += 1
    if changed:
        write(path, text)
    info("mips.h: %d macro(s) guarded with !TARGET_TIGON" % changed)


# --- gcc/config/mips/mips.opt -------------------------------------------------
MTIGON_OPT = """
mtigon
Target Var(TARGET_TIGON)
Do not use lwl/lwr/swl/swr, mult/multu, div/divu or HI/LO (Broadcom Tigon3).
"""


def patch_mips_opt(tree):
    path = os.path.join(tree, "gcc/config/mips/mips.opt")
    text = read(path)
    if "TARGET_TIGON" in text:
        info("mips.opt: -mtigon option already present")
        return
    if not text.endswith("\n"):
        text += "\n"
    write(path, text + MTIGON_OPT)
    info("mips.opt: added -mtigon option")


# --- gcc/config/mips/mips.cc --------------------------------------------------
# In mips_mulsidi3_gen_fn, the widening 32x32->64 multiply expander must fall
# back to a libcall on Tigon (it otherwise reaches patterns that emit `mult`).
# Insert `if (TARGET_TIGON) return NULL;` before the first ISA_HAS_R6MUL test
# inside that function.
def patch_mips_cc(tree):
    path = os.path.join(tree, "gcc/config/mips/mips.cc")
    text = read(path)
    fpos = text.find("\nmips_mulsidi3_gen_fn (")
    if fpos < 0:
        die("mips.cc: function mips_mulsidi3_gen_fn not found")
    anchor = "if (ISA_HAS_R6MUL)"
    apos = text.find(anchor, fpos)
    if apos < 0:
        die("mips.cc: anchor 'if (ISA_HAS_R6MUL)' not found in mips_mulsidi3_gen_fn")
    if "TARGET_TIGON" in text[fpos:apos]:
        info("mips.cc: mips_mulsidi3_gen_fn already patched")
        return
    line_start = text.rfind("\n", 0, apos) + 1
    indent = text[line_start:apos]  # leading whitespace of the anchor line
    snippet = "%sif (TARGET_TIGON)\n%s  return NULL;\n" % (indent, indent)
    write(path, text[:line_start] + snippet + text[line_start:])
    info("mips.cc: mips_mulsidi3_gen_fn returns a libcall for -mtigon")


# --- libgcc soft multiply/divide for -mtigon ----------------------------------
# Stock MIPS has hardware mult/div, so libgcc never builds the SImode soft
# routines a -mtigon build calls. Two parts fix that, both in t-elf:
#   * LIB2ADD pulls in GCC's own generic soft divide (libgcc/divmod.c,
#     udivmod.c, udivmodsi4.c -- the same files pdp11 and iq2000 use) plus a
#     soft __mulsi3 (config/mips/tg-mulsi3.c, written by patch_tg_mulsi3).
#   * libgcc2 itself is built with -mtigon; _mulvsi3 is excluded because the
#     trapping signed multiply ICEs under -mtigon (it is only ever called by
#     -ftrapv / __builtin_*_overflow, which the firmware does not use).
T_ELF_ADD = """
# ThunderGate: -mtigon libgcc. Build libgcc2 with -mtigon so its soft
# routines avoid mult/div/HILO and lwl/lwr on the Broadcom Tigon3 core.
HOST_LIBGCC2_CFLAGS += -mtigon
# _mulvsi3 (trapping signed multiply) ICEs under -mtigon; it is referenced
# only by -ftrapv / __builtin_mul_overflow, which the firmware never uses.
LIB2FUNCS_EXCLUDE += _mulvsi3
# Stock MIPS has hardware mult/div so libgcc omits the SImode soft routines a
# -mtigon build needs. Add GCC's own generic soft divide and a soft __mulsi3
# (the shift-add routine GCC ships for its no-multiply targets).
LIB2ADD += $(srcdir)/divmod.c $(srcdir)/udivmod.c $(srcdir)/udivmodsi4.c \\
           $(srcdir)/config/mips/tg-mulsi3.c
"""

# config/mips/tg-mulsi3.c: GCC's own shift-and-add __mulsi3 -- the routine it
# ships as config/nios2/lib2-mul.c, config/lm32/_mulsi3.c, ... for every
# target that lacks a hardware multiply -- with self-contained mode typedefs.
TG_MULSI3_C = '''/* Soft 32-bit integer multiply for the Broadcom Tigon3 MIPS core.

   The Tigon3 on-chip MIPS core has no mult/multu instruction, so GCC built
   with -mtigon emits a __mulsi3 libcall. Stock MIPS always has a hardware
   multiply, so libgcc carries no soft __mulsi3 for MIPS. This is the
   shift-and-add routine GCC itself ships for its other no-multiply targets
   (config/nios2/lib2-mul.c, config/lm32/_mulsi3.c, ...), placed here so the
   -mtigon libgcc build is self-contained. Installed by misc/mtigon-patch.py.

   Copyright (C) 2012-2024 Free Software Foundation, Inc.

   This file is free software; you can redistribute it and/or modify it
   under the terms of the GNU General Public License as published by the
   Free Software Foundation; either version 3, or (at your option) any
   later version.

   This file is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
   General Public License for more details.

   Under Section 7 of GPL version 3, you are granted additional
   permissions described in the GCC Runtime Library Exception, version
   3.1, as published by the Free Software Foundation.

   You should have received a copy of the GNU General Public License and
   a copy of the GCC Runtime Library Exception along with this program;
   see the files COPYING3 and COPYING.RUNTIME respectively. If not, see
   <http://www.gnu.org/licenses/>. */

typedef int SItype __attribute__ ((mode (SI)));
typedef unsigned int USItype __attribute__ ((mode (SI)));

SItype
__mulsi3 (SItype a, SItype b)
{
  SItype res = 0;
  USItype cnt = a;

  while (cnt)
    {
      if (cnt & 1)
	res += b;
      b <<= 1;
      cnt >>= 1;
    }

  return res;
}
'''


def patch_t_elf(tree):
    path = os.path.join(tree, "libgcc/config/mips/t-elf")
    text = read(path)
    idx = text.find("# ThunderGate")
    if idx >= 0:
        if "tg-mulsi3.c" in text[idx:]:
            info("t-elf: -mtigon libgcc block already present")
            return
        # A prior revision of the ThunderGate block is present; drop it
        # (back to before its first comment) and re-append the current one.
        text = text[:idx]
    text = text.rstrip() + "\n"
    write(path, text + T_ELF_ADD)
    info("t-elf: -mtigon libgcc block installed (soft mul/div, _mulvsi3 out)")


def patch_tg_mulsi3(tree):
    path = os.path.join(tree, "libgcc/config/mips/tg-mulsi3.c")
    if os.path.isfile(path) and read(path) == TG_MULSI3_C:
        info("tg-mulsi3.c: already present")
        return
    write(path, TG_MULSI3_C)
    info("tg-mulsi3.c: soft __mulsi3 installed")


def main():
    if len(sys.argv) != 2:
        die("usage: mtigon-patch.py <path-to-gcc-source-tree>")
    tree = sys.argv[1]
    if not os.path.isdir(tree):
        die("not a directory: %s" % tree)
    patch_mips_h(tree)
    patch_mips_opt(tree)
    patch_mips_cc(tree)
    patch_t_elf(tree)
    patch_tg_mulsi3(tree)
    info("done")


if __name__ == "__main__":
    main()
