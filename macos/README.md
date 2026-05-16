# macOS support

On macOS, ThunderGate reaches the Tigon3 NIC through a PCIDriverKit
driver extension (dext). This directory holds the dext and the
container application that installs it.

## Layout

- **`TGDext/`** — the driver extension.
  - `TGPCIDevice.{iig,cpp}` — the `IOService` that matches the Tigon3
    PCI device, opens it, and keeps a descriptor for BAR 0.
  - `TGUserClient.{iig,cpp}` — the `IOUserClient`: config-space read/write
    plus the BAR 0 mapping handed to user space.
  - `tg_dext.h` — the dext↔client ABI (method selectors, memory types);
    mirrored by `py/interfaces/macos.py`.
  - `Info.plist` — `IOKitPersonalities` (PCI matching) and the
    user-client class.
  - `TGDext.entitlements` — DriverKit entitlements.
- **`tgctl/`** — the container app. A dext can only be installed by an
  application bundle that embeds it; `tgctl` submits the
  `OSSystemExtensionRequest` that activates (or deactivates) `TGDext`.

The user-space half lives in `py/interfaces/macos.py`, which opens an
`IOUserClient` connection to the dext over `IOKit.framework`.

## Building

The dext is **not** built by any Makefile in this repo. `.iig` files are
processed by Xcode's `iig` tool, which generates the `TGPCIDevice.h` and
`TGUserClient.h` headers that the `.cpp` files `#include`; the DriverKit
and PCIDriverKit SDK headers ship only with Xcode.

> **Note for editors / language servers:** opening `TGDext/*.cpp` with a
> plain C++ language server will report missing headers
> (`PCIDriverKit/PCIDriverKit.h`, `TGPCIDevice.h`) and unknown
> `IMPL` / `super` identifiers. That is expected — those are provided by
> the DriverKit SDK and by the `iig`-generated headers, neither of which
> exists outside an Xcode DriverKit build. The dext compiles inside an
> Xcode DriverKit target.

Step-by-step instructions — creating the Xcode project, signing, SIP and
developer-mode setup, installing, and running — are in
[`../doc/INSTALL.macos.md`](../doc/INSTALL.macos.md).
