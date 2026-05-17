#!/usr/bin/env bash
#
# package.sh - assemble and ad-hoc-sign the ThunderGate dext + container app.
#
# Produces macos/build/tgctl.app, with the dext embedded, signed to run
# locally (no certificate, no Apple Developer account). Installing it
# requires SIP disabled and `systemextensionsctl developer on` -- see
# doc/INSTALL.macos.md.
#
# Usage: macos/package.sh   then run build/tgctl.app/Contents/MacOS/tgctl

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

APP_ID=lol.ssj.thundergate
DEXT_ID=lol.ssj.thundergate.TGDext
OUT=build

# 1. build the dext driver executable and the container-app executable.
TGDext/build.sh
xcrun swiftc -target arm64-apple-macos12.0 -framework SystemExtensions \
    -o "$OUT/tgctl-exe" tgctl/main.swift

# 2. assemble the .dext bundle inside the app's SystemExtensions dir.
#    A dext is a *flat* (iOS-style) bundle -- Info.plist and executable
#    at the top level. Both the bundle and the executable are named by
#    the dext's bundle identifier: OSSystemExtensionRequest matches the
#    extension by that name (the PRODUCT_NAME == bundle-id rule), so the
#    executable must NOT have a short name.
APP="$OUT/tgctl.app"
DEXT="$APP/Contents/Library/SystemExtensions/$DEXT_ID.dext"
rm -rf "$APP"
mkdir -p "$DEXT"
cp TGDext/Info.plist       "$DEXT/Info.plist"
cp TGDext/build/tgdext-exe "$DEXT/$DEXT_ID"
chmod +x "$DEXT/$DEXT_ID"

# 3. assemble the .app bundle.
mkdir -p "$APP/Contents/MacOS"
cp tgctl/Info.plist  "$APP/Contents/Info.plist"
cp "$OUT/tgctl-exe"  "$APP/Contents/MacOS/tgctl"
chmod +x "$APP/Contents/MacOS/tgctl"

# 4. normalize the entitlements -- codesign's AMFI XML parser rejects the
#    explanatory comments in the source .entitlements files; plutil
#    re-serializes a clean, comment-free copy.
plutil -convert xml1 -o "$OUT/TGDext.entitlements" TGDext/TGDext.entitlements
plutil -convert xml1 -o "$OUT/tgctl.entitlements"  tgctl/tgctl.entitlements

# 5. sign inner-to-outer: ad-hoc ("-"), entitlements embedded directly.
codesign --force --sign - --identifier "$DEXT_ID" \
    --entitlements "$OUT/TGDext.entitlements" --timestamp=none "$DEXT"
codesign --force --sign - --identifier "$APP_ID" \
    --entitlements "$OUT/tgctl.entitlements" --timestamp=none "$APP"

echo
echo "package: OK -- $APP"
codesign --verify --deep --strict --verbose=1 "$APP" 2>&1 | tail -2
