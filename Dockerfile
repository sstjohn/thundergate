# syntax=docker/dockerfile:1.7
#
# ThunderGate Linux CI image.
#
# Stage 1 builds the mips-elf cross-toolchain (binutils 2.46 + gcc 16.1) the
# firmware needs; that stage is slow but cacheable. Stage 2 is a Debian 13
# (Trixie) runtime with the host build tools, a pre-populated Python venv,
# and an entrypoint that copies a mounted source tree into the container,
# builds fw/ and efi/, and runs the Python and net-stack tests.
#
# Use via misc/docker-linux-ci.sh.

# --- stage 1: mips-elf cross-toolchain --------------------------------------
FROM debian:13-slim AS toolchain

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential ca-certificates curl xz-utils \
        flex bison texinfo \
        libgmp-dev libmpfr-dev libmpc-dev libisl-dev zlib1g-dev \
        python3 \
 && rm -rf /var/lib/apt/lists/*

COPY misc/build-toolchain.sh /tmp/misc/build-toolchain.sh
COPY misc/mtigon-patch.py    /tmp/misc/mtigon-patch.py

ENV TG_TOOLCHAIN_PREFIX=/opt/toolchain
ENV TG_TOOLCHAIN_BUILD=/tmp/toolchain-build
RUN bash /tmp/misc/build-toolchain.sh \
 && rm -rf /tmp/toolchain-build /tmp/misc


# --- stage 2: runtime -------------------------------------------------------
FROM debian:13-slim AS runtime

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates git rsync \
        build-essential \
        clang lld \
        binutils binutils-x86-64-linux-gnu binutils-aarch64-linux-gnu \
        python3 python3-venv python3-dev \
 && rm -rf /var/lib/apt/lists/*

COPY --from=toolchain /opt/toolchain /opt/toolchain

# requirements.txt + python-eficompressor go into /opt/venv at image-build
# time. The entrypoint symlinks /work/.venv -> /opt/venv so the firmware
# and EFI Makefiles (hardcoded to $(PROJ_ROOT)/.venv/bin/python3) find it.
#
# The ext/python-eficompressor checkout is staged alongside requirements.txt
# so the './ext/python-eficompressor' line in the requirements resolves.
#
# wxpython is filtered out: it has no Linux wheels and building it from
# source needs the full GTK/WebKit SDK. The CI image runs no GUI, and
# nothing the build or tests touch imports wxpython.
COPY requirements.txt          /tmp/venv-build/requirements.txt
COPY ext/python-eficompressor  /tmp/venv-build/ext/python-eficompressor
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
 && cd /tmp/venv-build \
 && grep -viE '^[[:space:]]*wxpython' requirements.txt > requirements-ci.txt \
 && /opt/venv/bin/pip install --no-cache-dir -r requirements-ci.txt \
 && rm -rf /tmp/venv-build

COPY misc/docker-linux-ci-entrypoint.sh /usr/local/bin/run-ci
RUN chmod +x /usr/local/bin/run-ci

ENV PATH=/opt/toolchain/bin:/opt/venv/bin:$PATH
ENV TG_TOOLCHAIN_PREFIX=/opt/toolchain

WORKDIR /work
ENTRYPOINT ["/usr/local/bin/run-ci"]
CMD ["all"]
