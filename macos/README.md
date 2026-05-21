# macOS support

On macOS, ThunderGate reaches the Tigon3 NIC through a PCIDriverKit
driver extension (dext). This directory holds the dext and the
container application that installs it.

## Layout

- **`TGDext/`**: the driver extension.
  - `TGPCIDevice.{iig,cpp}`: the `IOService` that matches the Tigon3
    PCI device, opens it, and keeps a descriptor for BAR 0.
  - `TGUserClient.{iig,cpp}` (the `IOUserClient`): config-space read/write
    plus the BAR 0 mapping handed to user space.
  - `tg_dext.h`: the dext↔client ABI (method selectors, memory types);
    mirrored by `py/interfaces/macos.py`.
  - `Info.plist`: `IOKitPersonalities` (PCI matching) and the
    user-client class.
  - `TGDext.entitlements`: DriverKit entitlements.
- **`tgctl/`**: the container app. A dext can only be installed by an
  application bundle that embeds it; `tgctl` submits the
  `OSSystemExtensionRequest` that activates (or deactivates) `TGDext`.

The user-space half lives in `py/interfaces/macos.py`, which opens an
`IOUserClient` connection to the dext over `IOKit.framework`.

## Building

To **build-validate** the dext (run `iig`, compile, and link the driver
executable), use `TGDext/build.sh` (requires Xcode with the DriverKit
SDK). A clean run reports `build: OK -- Mach-O 64-bit executable arm64e`.

`.iig` files are processed by Xcode's `iig` tool, which generates the
`TGPCIDevice.h` / `TGUserClient.h` headers that the `.cpp` files
`#include`; the DriverKit and PCIDriverKit SDKs ship only with Xcode.

> **Note for editors / language servers:** opening `TGDext/*.cpp` with a
> plain C++ language server will report missing headers
> (`PCIDriverKit/PCIDriverKit.h`, `TGPCIDevice.h`) and unknown
> `IMPL` / `super` identifiers. That is expected; those come from the
> DriverKit SDK and the `iig`-generated headers; `build.sh` supplies
> both. The dext compiles cleanly there.

`build.sh` does not produce a *signed, installable* `.dext`. That needs
an Xcode DriverKit target (to embed the dext in the `tgctl` app) and code
signing. Step-by-step instructions (Xcode project, signing, SIP and
developer-mode setup, installing, and running) are in
[`../doc/INSTALL.macos.md`](../doc/INSTALL.macos.md).
