#!/usr/bin/env bash
#
# build-toolchain.sh — build a mips-elf cross-toolchain for ThunderGate firmware.
#
# The Broadcom Tigon3 on-chip MIPS core is not a stock MIPS: it lacks the
# lwl/lwr/swl/swr unaligned load/store instructions, the mult/multu and
# div/divu instructions, and the HI/LO register file. GCC is given a -mtigon
# target flag (applied by misc/mtigon-patch.py) that suppresses all of them;
# multiply/divide go through libgcc's own soft routines, built with -mtigon.
#
# This replaces the binutils-2.25 + GCC-5.1 recipe in doc/firmware.md, which
# no longer builds on a modern host. Runs natively on macOS (Apple Silicon and
# Intel) and on Linux.
#
# Usage:
#   misc/build-toolchain.sh [stage]
#     stage = all (default) | deps | fetch | binutils | gcc | clean
#
# Environment overrides:
#   TG_TOOLCHAIN_PREFIX   install location   (default: <repo>/toolchain)
#   TG_TOOLCHAIN_BUILD    scratch build dir  (default: <repo>/.toolchain-build)
#
# After a successful build, add "$TG_TOOLCHAIN_PREFIX/bin" to PATH so that
# fw/Makefile finds mips-elf-gcc.

set -euo pipefail

BINUTILS_VER=2.42
GCC_VER=14.2.0

TARGET=mips-elf
PROJ_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PREFIX="${TG_TOOLCHAIN_PREFIX:-$PROJ_ROOT/toolchain}"
BUILD="${TG_TOOLCHAIN_BUILD:-$PROJ_ROOT/.toolchain-build}"
JOBS="$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)"

BINUTILS_TARBALL="binutils-$BINUTILS_VER.tar.xz"
GCC_TARBALL="gcc-$GCC_VER.tar.xz"
BINUTILS_URL="https://ftp.gnu.org/gnu/binutils/$BINUTILS_TARBALL"
GCC_URL="https://ftp.gnu.org/gnu/gcc/gcc-$GCC_VER/$GCC_TARBALL"

say()  { printf '\033[1;36m[toolchain]\033[0m %s\n' "$*"; }
die()  { printf '\033[1;31m[toolchain] error:\033[0m %s\n' "$*" >&2; exit 1; }

# --- host detection -----------------------------------------------------------
# GCC's configure wants GNU sed; Homebrew installs it as `gsed`. Prepend the
# Homebrew gnubin shim and resolve the math-library prefixes for --with-*.
detect_host() {
    UNAME="$(uname -s)"
    if [ "$UNAME" = "Darwin" ]; then
        command -v brew >/dev/null || die "Homebrew is required on macOS"
        BREW="$(brew --prefix)"
        export PATH="$BREW/opt/gnu-sed/libexec/gnubin:$PATH"
        GMP="$BREW/opt/gmp"; MPFR="$BREW/opt/mpfr"
        MPC="$BREW/opt/libmpc"; ISL="$BREW/opt/isl"
        export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
    else
        # Linux: rely on system-installed dev packages; configure auto-detects.
        GMP=; MPFR=; MPC=; ISL=
    fi
}

with_math() {
    # Emit --with-gmp= style flags only when an explicit prefix was resolved.
    local f=""
    [ -n "${GMP:-}" ]  && f="$f --with-gmp=$GMP"
    [ -n "${MPFR:-}" ] && f="$f --with-mpfr=$MPFR"
    [ -n "${MPC:-}" ]  && f="$f --with-mpc=$MPC"
    [ -n "${ISL:-}" ]  && f="$f --with-isl=$ISL"
    echo "$f"
}

# --- stages -------------------------------------------------------------------
stage_deps() {
    say "checking build prerequisites"
    if [ "$(uname -s)" = "Darwin" ]; then
        local missing=""
        for p in gmp mpfr libmpc isl texinfo gnu-sed; do
            brew list --versions "$p" >/dev/null 2>&1 || missing="$missing $p"
        done
        [ -n "$missing" ] && die "missing Homebrew packages:$missing (run: brew install$missing)"
    fi
    command -v makeinfo >/dev/null || die "texinfo/makeinfo not on PATH"
    say "prerequisites OK"
}

stage_fetch() {
    mkdir -p "$BUILD"
    cd "$BUILD"
    [ -f "$BINUTILS_TARBALL" ] || { say "downloading $BINUTILS_TARBALL"; curl -fL# -o "$BINUTILS_TARBALL" "$BINUTILS_URL"; }
    [ -f "$GCC_TARBALL" ]      || { say "downloading $GCC_TARBALL";      curl -fL# -o "$GCC_TARBALL" "$GCC_URL"; }
    [ -d "binutils-$BINUTILS_VER" ] || { say "extracting binutils"; tar xf "$BINUTILS_TARBALL"; }
    [ -d "gcc-$GCC_VER" ]           || { say "extracting gcc";      tar xf "$GCC_TARBALL"; }

    say "applying -mtigon target patch to GCC $GCC_VER"
    python3 "$PROJ_ROOT/misc/mtigon-patch.py" "$BUILD/gcc-$GCC_VER"
}

stage_binutils() {
    say "building binutils $BINUTILS_VER -> $TARGET"
    rm -rf "$BUILD/build-binutils"
    mkdir -p "$BUILD/build-binutils"
    cd "$BUILD/build-binutils"
    # --with-system-zlib: the bundled zlib's zutil.h misdetects modern macOS
    # and #defines fdopen to NULL, which breaks the SDK <stdio.h>. Use the
    # host's zlib instead.
    "$BUILD/binutils-$BINUTILS_VER/configure" \
        --target="$TARGET" --prefix="$PREFIX" \
        --disable-nls --disable-werror --with-sysroot --with-system-zlib
    make -j"$JOBS"
    make install
    say "binutils installed"
}

stage_gcc() {
    [ -x "$PREFIX/bin/$TARGET-as" ] || die "binutils not installed; run the binutils stage first"
    export PATH="$PREFIX/bin:$PATH"
    say "building gcc $GCC_VER -> $TARGET (this takes a while)"
    rm -rf "$BUILD/build-gcc"
    mkdir -p "$BUILD/build-gcc"
    cd "$BUILD/build-gcc"
    # shellcheck disable=SC2046
    "$BUILD/gcc-$GCC_VER/configure" \
        --target="$TARGET" --prefix="$PREFIX" \
        --enable-languages=c --without-headers --with-newlib \
        --disable-nls --disable-shared --disable-threads \
        --disable-libssp --disable-libquadmath --disable-libgomp --disable-libatomic \
        --disable-multilib --with-system-zlib \
        --with-arch=mips2 --with-tune=r6000 --with-float=soft \
        $(with_math)
    # The Tigon3 core has no hardware multiply/divide, so GCC's generated
    # code calls libgcc's soft __mulsi3/__divsi3/... routines. Build and
    # install target-libgcc with -mtigon (applied to libgcc via the t-elf
    # patch). One routine, _mulvsi3 -- the trapping signed multiply -- ICEs
    # under -mtigon in GCC 14; the patch excludes it via LIB2FUNCS_EXCLUDE.
    # __mulvsi3 is emitted only for -ftrapv / __builtin_*_overflow, which the
    # firmware never uses, so libgcc still links cleanly.
    make -j"$JOBS" all-gcc
    make install-gcc
    make -j"$JOBS" all-target-libgcc
    make install-target-libgcc
    say "gcc + libgcc installed"
}

stage_clean() {
    say "removing build scratch dir $BUILD"
    rm -rf "$BUILD"
}

# --- driver -------------------------------------------------------------------
detect_host
case "${1:-all}" in
    all)      stage_deps; stage_fetch; stage_binutils; stage_gcc ;;
    deps)     stage_deps ;;
    fetch)    stage_fetch ;;
    binutils) stage_binutils ;;
    gcc)      stage_gcc ;;
    clean)    stage_clean ;;
    *)        die "unknown stage '$1' (use: all|deps|fetch|binutils|gcc|clean)" ;;
esac

if [ "${1:-all}" = "all" ]; then
    say "done. Toolchain in $PREFIX"
    say "add it to PATH:  export PATH=\"$PREFIX/bin:\$PATH\""
fi
