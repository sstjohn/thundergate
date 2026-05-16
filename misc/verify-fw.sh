#!/usr/bin/env bash
#
# verify-fw.sh — verify the ThunderGate firmware toolchain output.
#
# Compiles every fw/*.c with the mips-elf cross-toolchain and -mtigon, then
# disassembles the result and fails if any instruction the Tigon3 core lacks
# (unaligned load/store, hardware multiply/divide, HI/LO moves) was emitted.
#
# This is the hardware-free Phase 1 gate. The full fw.elf link additionally
# needs fw/fixed.sym from py/symgen.py; that check is added once the Python
# port (Phase 2) lands.
#
# Usage: misc/verify-fw.sh

set -euo pipefail

PROJ_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLCHAIN="${TG_TOOLCHAIN_PREFIX:-$PROJ_ROOT/toolchain}"
export PATH="$TOOLCHAIN/bin:$PATH"

CC=mips-elf-gcc
OBJDUMP=mips-elf-objdump

# Instructions absent on the Tigon3 MIPS core. Emitting any of these means
# the -mtigon patch failed to suppress something.
FORBIDDEN='lwl|lwr|swl|swr|ldl|ldr|sdl|sdr|mult|multu|div|divu|madd|maddu|msub|msubu|mfhi|mflo|mthi|mtlo'

# Codegen flags from fw/Makefile (debug-only flags omitted; they do not
# affect instruction selection).
CFLAGS=(-mips2 -march=r6000 -mfix-r4000 -G 0 -fno-pic -fno-builtin
        -mno-shared -mno-abicalls -mno-llsc -mno-split-addresses
        -mtigon -msoft-float -std=gnu11 -Wno-main
        "-I$PROJ_ROOT/include" "-I$PROJ_ROOT/fw")

command -v "$CC" >/dev/null \
    || { echo "verify-fw: $CC not found — run misc/build-toolchain.sh first" >&2; exit 1; }

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

fail=0
for src in "$PROJ_ROOT"/fw/*.c "$PROJ_ROOT"/fw/net/*.c; do
    if ! "$CC" "${CFLAGS[@]}" -c "$src" -o "$work/$(basename "$src" .c).o"; then
        echo "verify-fw: COMPILE FAILED: $src" >&2
        fail=1
    fi
done
[ "$fail" -eq 0 ] || { echo "verify-fw: firmware did not compile" >&2; exit 1; }

hits="$("$OBJDUMP" -d "$work"/*.o | grep -wiE "$FORBIDDEN" || true)"
if [ -n "$hits" ]; then
    echo "verify-fw: FAIL — instructions the Tigon3 core lacks were emitted:" >&2
    echo "$hits" >&2
    exit 1
fi

echo "verify-fw: OK — $(ls "$work"/*.o | wc -l | tr -d ' ') firmware objects compiled, no forbidden instructions"
