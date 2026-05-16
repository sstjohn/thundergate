#!/usr/bin/env python3
"""Apply the -mtigon target flag to a GCC source tree.

The Broadcom Tigon3 on-chip MIPS core is not a stock MIPS: it lacks the
lwl/lwr/swl/swr unaligned load/store instructions, the mult/multu and
div/divu instructions, and the HI/LO register file. The historical
gcc-5.1.0-mtigon.patch added a -mtigon flag that suppresses all of them.

That patch was line-context based and no longer applies to a modern GCC.
This script instead re-derives every change *by macro and function name*,
so it survives GCC's source reorganisation between releases. Verified
against GCC 14.2.0.

What it does NOT do, and why:
  * It does not re-add the original patch's mips_init_libfuncs hunk. That
    hunk set the SImode/DImode div and mul libfuncs to __divsi3/__divdi3/
    __muldi3 -- which are already GCC's defaults for a non-vr4120 build.
    It was redundant, and editing a function body is the most fragile kind
    of patch, so it is dropped.
  * It does not add custom libgcc routines. Stock libgcc2.c already supplies
    the soft __divsi3/__udivsi3/__mulsi3/__muldi3/... and t-elf is patched
    below to build libgcc2 itself with -mtigon. If a genuine gap exists it
    appears as an undefined symbol when fw.elf links -- a precise, debuggable
    signal, far better than guessing.

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


# --- libgcc/config/mips/t-elf -------------------------------------------------
T_ELF_ADD = """
# ThunderGate: build libgcc2 with -mtigon so its soft multiply/divide
# routines avoid mult/div/HILO and lwl/lwr on the Broadcom Tigon3 core.
HOST_LIBGCC2_CFLAGS += -mtigon
"""


def patch_t_elf(tree):
    path = os.path.join(tree, "libgcc/config/mips/t-elf")
    text = read(path)
    if "-mtigon" in text:
        info("t-elf: -mtigon already present")
        return
    if not text.endswith("\n"):
        text += "\n"
    write(path, text + T_ELF_ADD)
    info("t-elf: libgcc2 will be built with -mtigon")


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
    info("done")


if __name__ == "__main__":
    main()
