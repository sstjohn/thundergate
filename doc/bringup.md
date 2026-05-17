# ThunderGate revival — review and hardware bring-up

This document is the pre-hardware review of the modernization effort and
the runbook for verifying it once a Tigon3 NIC is available. It assumes
the modernization branch (`modernization`).

---

## 1. Status

Phases 0–5 of the modernization plan are complete; Phase 6 is the
hardware verification below.

| Phase | Work | State |
|---|---|---|
| 0 | Repo hygiene, submodules, `requirements.txt` | done |
| 1 | mips-elf GCC 14 `-mtigon` cross-toolchain | done |
| 2 | Python 2 → 3, whole toolkit | done |
| 3 | On-core ARP/IPv4/ICMP/UDP stack | done |
| 4 | macOS PCIDriverKit dext (4a flash, 4b DMA+MSI) | done |
| 5 | efi/, Windows, Linux touch-ups | done |
| 6 | Hardware verification | **this document** |

## 2. What is verified, hardware-free

All of the following pass on the build host today:

- **Firmware** — `misc/verify-fw.sh`: the full `fw.img` links (20984
  bytes) with no instruction the Tigon3 core lacks.
- **On-core TCP/IP stack** — `make -C fw/net/test && fw/net/test/nettest`:
  18/18 checks (ARP reply, ICMP echo, UDP echo).
- **Python** — all 81 files compile; the `py/tests/` suite (11 tests)
  passes; an import sweep of every module is clean apart from
  platform-gated and optional-dependency modules (see §4).

## 3. What is NOT verifiable without hardware or Xcode

Treat these as the risk list for bring-up:

- **The dext C++ (`macos/TGDext/`).** It builds only in an Xcode
  DriverKit target — the `.iig` files need Xcode's `iig` tool and the
  PCIDriverKit SDK. The DriverKit API call sites (`GetBARInfo`,
  `_CopyDeviceMemoryWithIndex`, `IODMACommand`, `IOInterruptDispatchSource`,
  the `IMPL` macro, `super`, `AsyncCompletion`) are written from the
  documentation; expect to settle a few signatures against the installed
  SDK on the first Xcode build. The architecture and control flow are
  sound; the uncertainty is API surface, not design.
- **`interfaces/macos.py` `wait_interrupt()`.** The Mach-message receive
  is written but the bridge into the TAP driver's asyncio loop is
  finalized on hardware (Phase 6c).
- **`efi/`.** The `gnu-efi` submodule was bumped to 3.0.18 but the option
  ROM is built and verified only on Intel + VT-d (Phase 6e, lowest
  priority). It has no Apple Silicon target.

## 4. Open items surfaced by review (not bring-up blockers)

- **TAP drivers — resolved.** `py/main.py -d` runs the `tap/` package
  (the live userspace TAP driver, Linux/Windows). `testdrv.py` (the
  `-t` test driver) was *broken*, not dead — it imported a long-removed
  `tapdrv` module — and is now repointed at `_tap/`, which exports the
  same `TapDriver` and imports cleanly. The trollius-based `_aiotap/`
  was the superseded twin of `_tap/`, referenced by nothing, and has
  been removed. `tap/` and `_tap/` both remain as Linux TAP drivers.
- **No macOS TAP path yet.** `tap/` is Linux/Windows-only; consuming the
  Phase 4b dext DMA/MSI from a macOS `tap` backend is unbuilt. The flash
  path (the core goal) does not need it.

## 5. Bring-up runbook

### 5.0 Recommended order

Do **Linux first**. It exercises the least unverified code — the flash
path there is only the Python 2→3 port, no new dext. Reaching the core
milestone (the on-core stack answering a ping) needs no NVRAM write at
all: `blocks/cpu.py:image_load()` loads the firmware straight into the
core's SRAM. macOS bring-up (the new dext) follows.

### 5.1 Linux — toolkit and the on-core stack *(the milestone)*

Setup: follow `doc/INSTALL.linux.md` (deps, venv, `boltctl authorize`
for a Thunderbolt adapter, `vfio-pci` binding).

1. **Back up the EEPROM first — always.**
   ```
   .venv/bin/python3 py/main.py -b      # writes eeprom.bak
   ```
2. **Load the firmware into the core's SRAM** (fast iteration, no flash):
   use `blocks/cpu.py:image_load()` with `fw/fw.elf` from the shell
   (`py/main.py -s`). This puts the stack on the core directly.
3. **From a peer on the same segment**, with the firmware's IP
   (`DEFAULT_IP_ADDR` in `fw/config.h`):
   - `ping <ip>` — expect ICMP echo replies.
   - `arping <ip>` — expect ARP replies.
   - `nc -u <ip> 7` then type — expect a UDP echo.
4. **Regression:** confirm the legacy `0x88b5` control protocol still
   works (it shares `rx()` with the new dispatch).

This is the project's headline goal: the MIPS core servicing a network
stack independently of the host.

### 5.2 Linux — NVRAM flash (persistence)

```
.venv/bin/python3 py/main.py -i
```
Installs the firmware via `blocks/nvram.py:install_thundergate()`.
Confirm the bootcode magic `0xb49a89ab` at gencomm offset `0xb50`.
`eeprom.bak` is the recovery path if a flash goes wrong.

### 5.3 macOS — the dext and the flash path

Setup: follow `doc/INSTALL.macos.md` end to end — build the dext in an
Xcode DriverKit target (settle any SDK signature mismatches; see §3),
disable SIP, `systemextensionsctl developer on`, install via `tgctl`.

1. `systemextensionsctl list` shows `TGDext` `[activated enabled]`.
2. `log stream --predicate 'sender == "TGDext"'` while plugging in the
   NIC — expect `Start: ok -- BAR0 is N bytes`.
3. `.venv/bin/python3 py/main.py -b` then `-i` — the flash path over the
   dext, identical to Linux.

### 5.4 macOS — DMA + interrupts (4b)

Exercise `MacOSMemMgr` (DMA buffer alloc/map) and `wait_interrupt()`
against the live device; finalize the asyncio bridge. A macOS `tap`
backend is still to be written (§4).

### 5.5 Windows / efi (later, lower priority)

- Windows: `doc/INSTALL.windows.md` — build `tgwin.sln`, test-sign,
  install `tgwink`; verify flash + TAP. The INF now declares
  `DmaRemappingCompatible`.
- efi/: `doc/INSTALL.linux.md` host, `make -C ext/gnu-efi` then
  `make -C efi`; verify the option ROM and DMAR on Intel + VT-d.

## 6. If something goes wrong

- **Always** have `eeprom.bak` before any `-i`. A bad flash is
  recoverable from it; without it, an SPI programmer is the only way
  back.
- The firmware can be run from SRAM (`image_load`) without ever touching
  NVRAM — prefer that for all stack iteration.
- dext misbehaviour: `log show --predicate 'sender == "TGDext"'`.
