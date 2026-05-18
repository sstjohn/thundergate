#!/usr/bin/env bash
#
# verify-fw.sh — build the ThunderGate firmware and verify the output.
#
# Runs the full firmware build (fw/Makefile) and fails if any instruction
# the Tigon3 core lacks -- unaligned load/store, hardware multiply/divide,
# HI/LO moves -- was emitted into the linked image.
#
# Requires the mips-elf cross-toolchain (misc/build-toolchain.sh) and the
# project virtualenv (.venv, used by py/symgen.py to generate fixed.sym).
#
# Usage: misc/verify-fw.sh

set -euo pipefail

PROJ_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLCHAIN="${TG_TOOLCHAIN_PREFIX:-$PROJ_ROOT/toolchain}"
export PATH="$TOOLCHAIN/bin:$PATH"

# Instructions absent on the Tigon3 MIPS core.
FORBIDDEN='lwl|lwr|swl|swr|ldl|ldr|sdl|sdr|mult|multu|div|divu|madd|maddu|msub|msubu|mfhi|mflo|mthi|mtlo'

command -v mips-elf-gcc >/dev/null \
    || { echo "verify-fw: mips-elf toolchain not found — run misc/build-toolchain.sh" >&2; exit 1; }

log="$(mktemp)"
trap 'rm -f "$log"' EXIT

make -C "$PROJ_ROOT/fw" clean >/dev/null 2>&1 || true
if ! make -C "$PROJ_ROOT/fw" >"$log" 2>&1; then
    echo "verify-fw: firmware build failed:" >&2
    tail -20 "$log" >&2
    exit 1
fi
[ -f "$PROJ_ROOT/fw/fw.img" ] || { echo "verify-fw: fw.img was not produced" >&2; exit 1; }

# The firmware loads at 0x08000000 in the RX-CPU scratch pad and runs with
# the stack at 0x08010000; image.x asserts text+data+bss stay below
# 0x0800E000 -- 56 KB, leaving 8 KB of stack headroom. Past that the core
# never boots.
size="$(wc -c < "$PROJ_ROOT/fw/fw.img" | tr -d ' ')"
if [ "$size" -gt 57344 ]; then
    echo "verify-fw: FAIL — fw.img is $size bytes, over the 56 KB image budget" >&2
    exit 1
fi

hits="$(mips-elf-objdump -d "$PROJ_ROOT/fw/fw.elf" | grep -wiE "$FORBIDDEN" || true)"
if [ -n "$hits" ]; then
    echo "verify-fw: FAIL — the linked firmware contains instructions the core lacks:" >&2
    echo "$hits" >&2
    exit 1
fi

echo "verify-fw: OK — fw.img built ($size bytes, within the 56 KB budget), no forbidden instructions"
