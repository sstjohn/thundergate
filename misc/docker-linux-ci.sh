#!/usr/bin/env bash
#
# misc/docker-linux-ci.sh -- run the ThunderGate Linux build + tests in a
# Debian 13 Docker container. Builds the image on first use; subsequent
# runs reuse the cached mips-elf cross-toolchain.
#
# Usage:
#   misc/docker-linux-ci.sh                  # build image + run all stages
#   misc/docker-linux-ci.sh fw               # firmware build + verify-fw
#   misc/docker-linux-ci.sh efi              # EFI option-ROM build
#   misc/docker-linux-ci.sh pytest           # Python unit tests
#   misc/docker-linux-ci.sh nettest          # net-stack host harness
#   misc/docker-linux-ci.sh shell            # interactive bash
#   TG_CI_REBUILD=1 misc/docker-linux-ci.sh  # force docker build --no-cache
#
# The host source tree is bind-mounted read-only at /src; the container
# stages a clean copy at /work before building, so host build artefacts
# never collide with the in-container build.

set -euo pipefail

PROJ_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE="${TG_CI_IMAGE:-thundergate-linux-ci:latest}"

command -v docker >/dev/null || {
    echo "docker not on PATH" >&2; exit 1
}

build_args=()
[ "${TG_CI_REBUILD:-0}" = "1" ] && build_args+=(--no-cache)

if [ "${TG_CI_REBUILD:-0}" = "1" ] || ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
    echo "[docker-linux-ci] building $IMAGE (the mips-elf toolchain stage takes a while)"
    docker build "${build_args[@]}" -t "$IMAGE" -f "$PROJ_ROOT/Dockerfile" "$PROJ_ROOT"
fi

exec docker run --rm -it \
    -v "$PROJ_ROOT:/src:ro" \
    "$IMAGE" "$@"
