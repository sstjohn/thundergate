# Installing and running ThunderGate on macOS

This guide covers the macOS-native path: building the PCIDriverKit driver
extension (dext), preparing the machine, installing the dext, and running
the ThunderGate toolkit against a Tigon3 NIC.

macOS support is **additive** — the Linux and Windows paths are
unaffected. See `INSTALL.linux.md` / `INSTALL.windows.md` for those.

> **Security note.** The local-development path below disables System
> Integrity Protection. That lowers the security of the whole machine.
> Use a machine you are willing to run that way (a dedicated research
> box), and re-enable SIP when you are done — see *Reverting*.

---

## 1. Prerequisites

- macOS 11 or later, Intel or Apple Silicon.
- **Xcode** (from the App Store) and its command-line tools:
  `xcode-select --install`.
- Python 3.13+ and the project virtualenv (see the top-level `README` /
  `requirements.txt`):
  ```sh
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
  ```
- To build firmware as well, the mips-elf cross-toolchain:
  `misc/build-toolchain.sh` (not needed just to flash a prebuilt image).
- A Broadcom Tigon3 NIC. If it is a Thunderbolt-attached adapter, approve
  it first (System Settings shows a prompt, or use `boltctl` semantics —
  on macOS, accept the "Allow Accessories to Connect" prompt).

No paid Apple Developer account is required for the local-development
path. A signed, notarized, distributable build *does* require one, plus
Apple's grant of the restricted `com.apple.developer.driverkit*`
entitlements — that is out of scope here.

---

## 2. Build the dext and container app in Xcode

The dext (`macos/TGDext/`) and app (`macos/tgctl/`) are provided as
source. Assemble them into an Xcode project once:

1. **New app target.** Xcode → File → New → Project → macOS → **App**.
   - Product Name: `tgctl`
   - Bundle Identifier: `lol.ssj.thundergate`
   - Language: Swift
   - Save it anywhere (e.g. `macos/ThunderGate.xcodeproj`).
2. **Use the provided app source.** Delete the generated `*App.swift` /
   `ContentView.swift`. Add `macos/tgctl/main.swift` to the `tgctl`
   target. In the target's Build Settings / Info, point it at
   `macos/tgctl/Info.plist`; in Signing & Capabilities add
   `macos/tgctl/tgctl.entitlements` (it grants
   `com.apple.developer.system-extension.install`).
3. **New dext target.** File → New → Target → macOS → **Driver
   Extension**.
   - Bundle Identifier: `lol.ssj.thundergate.TGDext`
     (it must be prefixed by the app's bundle identifier).
   - In the dext target's Build Settings, set **`PRODUCT_NAME` to
     `$(PRODUCT_BUNDLE_IDENTIFIER)`**. The dext executable must be named
     by its bundle identifier, or `OSSystemExtensionRequest` fails with
     "Extension not found in App bundle."
   - Xcode automatically embeds the dext in the `tgctl` app.
4. **Use the provided dext source.** Delete the generated dext sources.
   Add to the `TGDext` target: `TGPCIDevice.iig`, `TGPCIDevice.cpp`,
   `TGUserClient.iig`, `TGUserClient.cpp`, and `tg_dext.h` from
   `macos/TGDext/`. Set the target's Info.plist to
   `macos/TGDext/Info.plist` and its entitlements to
   `macos/TGDext/TGDext.entitlements`.
5. **Signing.** For local development, set both targets' signing to
   *Sign to Run Locally* (Build Settings → Code Signing Identity), or
   select your personal team. Restricted DriverKit entitlements need not
   be granted for the SIP-disabled path in step 3.
6. **Build** (⌘B). The `iig` tool generates `TGPCIDevice.h` /
   `TGUserClient.h` from the `.iig` files during the build.

If the build stops on a DriverKit/PCIDriverKit API mismatch (method
signature differs in your SDK), fix it against the SDK headers under
`$(xcrun --sdk driverkit --show-sdk-path)` — the call sites are
annotated in the `.cpp` files.

---

## 3. Prepare the machine

Driver extensions that are only locally signed require SIP disabled and
System Extension developer mode.

### Disable SIP

**Apple Silicon:**
1. Shut down. Press and hold the power button until "Loading startup
   options" appears; choose Options → Continue (recoveryOS).
2. Utilities → Startup Security Utility → select the system disk → set
   **Reduced Security**.
3. Utilities → Terminal → `csrutil disable` → confirm.
4. Reboot.

**Intel:**
1. Reboot holding ⌘-R to enter recoveryOS.
2. Utilities → Terminal → `csrutil disable`.
3. Reboot.

Confirm afterwards: `csrutil status` → *System Integrity Protection
status: disabled*.

### Enable System Extension developer mode

In the normal OS:
```sh
systemextensionsctl developer on
```

---

## 4. Install the dext

1. In Xcode, **Run** the `tgctl` scheme (⌘R), or build it and run the
   app bundle directly. On launch `tgctl` submits an activation request
   for `lol.ssj.thundergate.TGDext` and prints progress.
2. If macOS asks for approval, allow the extension in System Settings →
   General → Login Items & Extensions, then re-run `tgctl`.
3. Verify:
   ```sh
   systemextensionsctl list
   ```
   `lol.ssj.thundergate.TGDext` should show `[activated
   enabled]`.

With a matching Tigon3 NIC present, the dext matches it; check the
system log:
```sh
log show --predicate 'sender == "TGDext"' --last 5m
```

To remove the dext later: `tgctl deactivate`.

---

## 5. Run ThunderGate

With the dext active and the NIC present, the toolkit runs normally;
`py/main.py` selects the macOS interface automatically.

```sh
.venv/bin/python3 py/main.py -b      # back up the EEPROM first
.venv/bin/python3 py/main.py -i      # install the ThunderGate firmware
```

`py/interfaces/macos.py` connects to the dext, maps BAR 0, and performs
config-space access through it — the same flash path used on Linux and
Windows.

---

## 6. Reverting

1. Deactivate the dext: `tgctl deactivate` (or
   `systemextensionsctl uninstall <teamID> <bundleID>`).
2. Re-enable SIP — recoveryOS Terminal: `csrutil enable` (Apple Silicon:
   also restore *Full Security* in Startup Security Utility if desired),
   then reboot.
3. Optionally `systemextensionsctl developer off`.

---

## 7. Troubleshooting

- **`tgctl`: "request failed"** — SIP still enabled, developer mode off,
  or the app is not signed. Recheck section 3 and the signing in
  section 2.
- **`systemextensionsctl list` shows the dext but not `[activated
  enabled]`** — approve it in System Settings, then re-run `tgctl`.
- **Python: "ThunderGate dext not found"** — the dext is not activated,
  or no matching NIC is present. Confirm the device ID is in
  `macos/TGDext/Info.plist` `IOPCIMatch` (and in `TGDext.entitlements`);
  find it with `system_profiler SPPCIDataType`.
- **The dext loads but does not match the NIC** — the device ID is not
  in `IOPCIMatch`. Add `0xDDDDVVVV` (device ID, then vendor `14e4`) to
  both the Info.plist and the entitlements, and rebuild.
- **Inspect dext logs** — `log show --predicate 'sender == "TGDext"'
  --last 10m`, or stream with `log stream --predicate 'sender ==
  "TGDext"'`.
