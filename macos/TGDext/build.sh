#!/usr/bin/env bash
#
# build.sh - build-validate the ThunderGate dext from the command line.
#
# Runs Xcode's iig tool over the .iig interfaces, compiles the dext
# against the DriverKit + PCIDriverKit SDKs, and links the driver
# executable. This proves the dext compiles and links; producing a
# signed, installable .dext bundle is done from Xcode (see
# doc/INSTALL.macos.md) or by codesigning the executable below.
#
# Requires Xcode with the DriverKit SDK.
#
# Usage: macos/TGDext/build.sh

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

SDK="$(xcrun --sdk driverkit --show-sdk-path)"
[ -d "$SDK" ] || { echo "build: DriverKit SDK not found -- install Xcode" >&2; exit 1; }

BUILD=build
rm -rf "$BUILD"
mkdir -p "$BUILD/TGDext"

IFACES="TGPCIDevice TGUserClient"

# 1. iig: generate the headers and dispatch glue from the .iig interfaces.
#    -D__IIG=1 makes the SDK headers expose the iig qualifier keywords.
for f in $IFACES; do
    xcrun iig --def "$f.iig" \
        --header "$BUILD/TGDext/$f.h" --impl "$BUILD/$f.iig.cpp" \
        --framework-name TGDext \
        -- -x c++ -std=gnu++17 -D__IIG=1 -isysroot "$SDK" -I.
done

# 2. compile the dext sources and the generated glue.
#    arm64e, NOT arm64: the kernel refuses to exec an arm64 DriverKit
#    binary ("exec_mach_imgact: disallowing arm64 platform driverkit
#    binary ... should be arm64e") -- the dext matches but never launches.
CXXFLAGS=(-x c++ -std=gnu++17 -arch arm64e -fno-exceptions -fno-rtti
          -I. -I"$BUILD" -I"$BUILD/TGDext")
OBJS=()
for f in $IFACES; do
    xcrun --sdk driverkit clang++ -c "${CXXFLAGS[@]}" -o "$BUILD/$f.o"     "$f.cpp"
    xcrun --sdk driverkit clang++ -c "${CXXFLAGS[@]}" -o "$BUILD/$f.iig.o" "$BUILD/$f.iig.cpp"
    OBJS+=("$BUILD/$f.o" "$BUILD/$f.iig.o")
done

# 3. link the driver executable against the DriverKit runtime.
xcrun --sdk driverkit clang++ -arch arm64e "${OBJS[@]}" \
    -framework DriverKit -framework PCIDriverKit \
    -o "$BUILD/tgdext-exe"

echo "build: OK -- $(file -b "$BUILD/tgdext-exe")"
