#!/usr/bin/env bash
#
# In-container entrypoint for the ThunderGate Linux CI image.
#
# The host source tree is bind-mounted read-only at /src. This script
# stages a clean copy at /work (so host build artefacts -- macOS .o
# files, the host venv, the host toolchain dir -- don't leak in),
# wires up the pre-built venv at /opt/venv as /work/.venv (the
# firmware and EFI Makefiles look for $(PROJ_ROOT)/.venv/bin/python3),
# and dispatches the requested stage.
#
# Stages:
#   all       (default) fw + efi + pytest + nettest
#   fw        firmware build + misc/verify-fw.sh
#   efi       EFI option-ROM build for x86_64 + aarch64
#   pytest    python unit tests (py/tests/)
#   nettest   host build of the on-core TCP/IP stack test harness
#   shell     drop to bash with /work prepared
# Anything else is exec'd verbatim inside /work.

set -euo pipefail

if [ ! -d /src ]; then
    echo "run-ci: expected the source tree bind-mounted at /src" >&2
    exit 2
fi

# Stage a clean copy of the source. Exclusions:
#   .git/                 - not needed for the build
#   .venv/, toolchain/    - host-built, would shadow /opt/{venv,toolchain}
#   .toolchain-build/     - host scratch dir for misc/build-toolchain.sh
#   build artefacts       - *.o, *.so, *.efi, *.rom, *.elf, *.img, *.dSYM/
#   per-arch gnu-efi dirs - host-built (re-derived per CFLAGS in the container)
#   editor/test caches    - .pytest_cache/, __pycache__/, .vscode/, .claude/
mkdir -p /work
rsync -a --delete \
    --exclude='.git/' \
    --exclude='.venv/' \
    --exclude='toolchain/' \
    --exclude='.toolchain-build/' \
    --exclude='.pytest_cache/' \
    --exclude='__pycache__/' \
    --exclude='.vscode/' \
    --exclude='.claude/' \
    --exclude='*.o' \
    --exclude='*.so' \
    --exclude='*.efi' \
    --exclude='*.rom' \
    --exclude='*.elf' \
    --exclude='*.img' \
    --exclude='*.dSYM/' \
    --exclude='fw/fixed.sym' \
    --exclude='fw/net/test/nettest' \
    --exclude='efi/x86_64/' \
    --exclude='efi/aarch64/' \
    --exclude='ext/gnu-efi/x86_64/' \
    --exclude='ext/gnu-efi/aarch64/' \
    --exclude='ext/python-eficompressor/build/' \
    --exclude='eeprom.bak' \
    --exclude='eeproms/' \
    /src/ /work/

ln -sfn /opt/venv /work/.venv

cd /work

say() { printf '\033[1;36m[run-ci]\033[0m %s\n' "$*"; }

step_tglib() {
    # py/symgen.py imports device, which imports the ctypesgen-generated
    # tglib. Build it once; downstream steps reuse it.
    [ -f py/tglib.py ] && return 0
    say "generating py/tglib.py (ctypesgen)"
    make -C py tglib.py
}

step_fw() {
    step_tglib
    say "building firmware (fw/) + verify-fw"
    bash misc/verify-fw.sh
}

step_efi() {
    say "building EFI option ROM (efi/)"
    make -C efi
}

step_pytest() {
    step_tglib
    say "running py/tests"
    (cd py && python3 -m pytest -v tests)
}

step_nettest() {
    say "building + running fw/net/test"
    make -C fw/net/test run
}

case "${1:-all}" in
    all)
        step_fw
        step_efi
        step_pytest
        step_nettest
        say "OK -- all stages passed"
        ;;
    fw)      step_fw ;;
    efi)     step_efi ;;
    pytest)  step_pytest ;;
    nettest) step_nettest ;;
    shell)   exec bash ;;
    *)       exec "$@" ;;
esac
