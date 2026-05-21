# ThunderGate revival: review and hardware bring-up

This document records the modernization effort and the runbook used to
verify it on hardware. It tracks the `modernization` branch through
Phase 6, where macOS bring-up is complete; the Linux and Windows
hardware runs are still open.

---

## 1. Status

Phases 0–5 of the modernization plan are complete. Phase 6, hardware
verification, is done on macOS; the Linux and Windows hardware exercises
are still pending.

| Phase | Work | State |
|---|---|---|
| 0 | Repo hygiene, submodules, `requirements.txt` | done |
| 1 | mips-elf GCC 16 `-mtigon` cross-toolchain | done |
| 2 | Python 2 → 3, whole toolkit | done |
| 3 | On-core ARP/IPv4/ICMP/UDP stack | done |
| 4 | macOS PCIDriverKit dext (4a flash, 4b DMA+MSI) | done |
| 5 | efi/, Windows, Linux touch-ups | done |
| 6a | Hardware verification, macOS | done |
| 6b | Hardware verification, Linux | open |
| 6c | Hardware verification, Windows / efi | open |

## 2. What is verified, hardware-free

All of the following pass on the build host today:

- **Firmware**, via `misc/verify-fw.sh`: the full `fw.img` links (20984
  bytes) with no instruction the Tigon3 core lacks.
- **On-core TCP/IP stack**, via `make -C fw/net/test && fw/net/test/nettest`:
  18/18 checks (ARP reply, ICMP echo, UDP echo).
- **Python**: all 81 files compile; the `py/tests/` suite (11 tests)
  passes; an import sweep of every module is clean apart from
  platform-gated and optional-dependency modules (see §4).
- **The dext**: `macos/TGDext/build.sh` runs Xcode's `iig` and the
  DriverKit + PCIDriverKit SDKs and links the driver executable
  (`Mach-O 64-bit arm64e`). The C++ and every DriverKit API call site
  compile and link clean; the build settled four real signature defects.

## 3. What is verified on hardware (macOS bring-up, Phase 6a)

Every Phase 6 risk item was exercised end to end on a Thunderbolt
Gigabit Ethernet adapter from macOS:

- **The dext is signed, installed, and matched.** Built as a DriverKit
  target inside the `tgctl` Xcode project, embedded in the container app,
  signed with the user's developer ID, activated through `tgctl`, and
  matched against the re-plugged Thunderbolt adapter at probe score
  100000. `ioreg` reports `TGPCIDevice` (an `IOUserService`) as the
  child of `ethernet@0`.
- **The flash path over the dext works** end to end.
  `.venv/bin/python3 py/main.py -b` produces a recoverable `eeprom.bak`,
  and `-i` installs the bootcode and oprom through the dext's
  config-space accessors.
- **DMA and interrupts (Phase 4b).** `MacOSMemMgr` allocates and maps a
  1 MiB DMA buffer through the dext's IOMMU window with a range-based
  paddr lookup, staying inside the 16-slot dext DMA budget.
  `wait_interrupt()` delivers MSI-X status-tag updates into the
  `_aiotap` asyncio loop and acks the tag steady-state.
- **The on-core stack answers from the firmware.** With `fw/fw.elf`
  loaded into SRAM via `blocks/cpu.py:image_load()` and again from
  installed NVRAM, a peer on the segment receives ICMP echo, ARP, and
  UDP echo from the firmware's IP.
- **The userspace TAP driver bridges the NIC to the host.** `_aiotap`'s
  feth/BPF/NDRV macOS backend carries traffic both directions: host-to-NIC
  injection (commit `1ba5a16`) and NIC-to-host receive (commit `5901c6f`,
  which closed out a stack of bpf_hdr / rcb / IRQ-ack / feth-MAC /
  see-sent bugs).

## 4. What is still pending hardware verification

Treat these as the risk list for the remaining work:

- **Linux end to end.** The Linux flash and TAP paths are only the
  Python 2→3 port and have not been re-exercised on hardware. Lowest
  risk of the open items, since no new code paths since v0.
- **Windows end to end.** `tgwink` (the KMDF NIC driver) and the
  TAP-Windows6 host adapter need to be installed and run; `tgwin.sln`
  builds and the INF now declares `DmaRemappingCompatible`, but the
  signed-and-running validation is still open.
- **`efi/`.** The `gnu-efi` submodule was bumped to 3.0.18 but the
  option ROM has not been re-flashed and verified against Intel + VT-d
  on hardware. No Apple Silicon target.

## 4. The TAP drivers

The toolkit keeps three userspace TAP implementations, each a different
take on the same job. `py/main.py -d` runs one; `--tap` selects which, and
otherwise a per-platform default applies. A driver that does not support
the host platform is rejected before the device is touched.

- `py/tap/`: asyncio, built as a `Driver` object running cooperative
  tasks; Linux and Windows, the default there.
- `py/_tap/`: synchronous, a `select()` loop around a `TapDriver` class
  with per-OS backends; Linux and Windows. `testdrv.py` (`main.py -t`)
  also uses it.
- `py/_aiotap/`: an asyncio rework of `_tap`'s `TapDriver` with a macOS
  feth/BPF/NDRV backend (`_aiotap/macos.py`); Linux, Windows and macOS,
  the default on macOS. Exercising the macOS backend against the live
  dext is Phase 6 work; the flash path (the core goal) does not need it.

## 5. Bring-up runbook

### 5.0 Recommended order

In practice we did **macOS first** (§5.3, §5.4) and it worked. If you
are re-running the bring-up from scratch on a fresh machine, **Linux
first** is the lower-risk path: it exercises the least unverified code,
the flash path is only the Python 2→3 port, and reaching the on-core
milestone (the stack answering a ping) needs no NVRAM write at all:
`blocks/cpu.py:image_load()` loads the firmware straight into the
core's SRAM.

### 5.1 Linux: toolkit and the on-core stack *(the milestone)*

Setup: follow `doc/INSTALL.linux.md` (deps, venv, `boltctl authorize`
for a Thunderbolt adapter, `vfio-pci` binding).

1. **Back up the EEPROM first. Always.**
   ```
   .venv/bin/python3 py/main.py -b      # writes eeprom.bak
   ```
2. **Load the firmware into the core's SRAM** (fast iteration, no flash):
   use `blocks/cpu.py:image_load()` with `fw/fw.elf` from the shell
   (`py/main.py -s`). This puts the stack on the core directly.
3. **From a peer on the same segment**, with the firmware's IP
   (`DEFAULT_IP_ADDR` in `fw/config.h`):
   - `ping <ip>`: expect ICMP echo replies.
   - `arping <ip>`: expect ARP replies.
   - `nc -u <ip> 7` then type: expect a UDP echo.
4. **Regression:** confirm the legacy `0x88b5` control protocol still
   works (it shares `rx()` with the new dispatch).

This is the project's headline goal: the MIPS core servicing a network
stack independently of the host.

### 5.2 Linux: NVRAM flash (persistence)

```
.venv/bin/python3 py/main.py -i
```
Installs the firmware via `blocks/nvram.py:install_thundergate()`.
Confirm the bootcode magic `0xb49a89ab` at gencomm offset `0xb50`.
`eeprom.bak` is the recovery path if a flash goes wrong.

### 5.3 macOS: the dext and the flash path *(done)*

Setup: follow `doc/INSTALL.macos.md` end to end. The dext already
compiles and links (`macos/TGDext/build.sh`); the Xcode DriverKit target
is needed to embed it in the `tgctl` app and sign it. Then disable SIP,
`systemextensionsctl developer on`, and install via `tgctl`.

1. `systemextensionsctl list` shows `TGDext` `[activated enabled]`.
2. **Hand the device to the dext.** The Tigon3 is matched at boot by
   the built-in `AppleBCM5701Ethernet` kext (probe score 2048). The dext
   personality probes at 100000, so it wins, but only on a *re-match*:
   IOKit does not re-evaluate a device already bound to a driver. After
   the dext is active, **unplug and replug the Thunderbolt adapter** to
   force re-enumeration. Confirm with
   `ioreg -rc IOPCIDevice -n ethernet -w0` that `ethernet@0`'s child is
   now `TGPCIDevice` (an `IOUserService`), not `BCM5701Enet`. The `en8`
   interface disappears (expected; the NIC is the dext's now).
3. `log stream --predicate 'sender == "TGDext"'` during the replug.
   expect `Start: ok -- BAR0 is N bytes`.
4. `.venv/bin/python3 py/main.py -b` then `-i`: the flash path over the
   dext, identical to Linux.

If the dext does *not* win the match (still `BCM5701Enet`), the fallback
is to stop the kext competing: boot with `AppleBCM5701Ethernet` excluded
via a `kmutil` exclusion list (SIP is already disabled). Try the probe
score first; it is the standard mechanism.

### 5.4 macOS: DMA + interrupts (4b) *(done)*

`MacOSMemMgr` (DMA buffer alloc/map) and `wait_interrupt()` ran against
the live device; the asyncio bridge is finalized; the `_aiotap` macOS
backend (`main.py -d`, §5) carries traffic both ways through the live
dext.

### 5.5 Windows / efi (later, lower priority)

- Windows (`doc/INSTALL.windows.md`): build `tgwin.sln`, test-sign,
  install `tgwink`; verify flash + TAP. The INF now declares
  `DmaRemappingCompatible`.
- efi/: `doc/INSTALL.linux.md` host, `make -C ext/gnu-efi` then
  `make -C efi`; verify the option ROM and DMAR on Intel + VT-d.

## 6. If something goes wrong

- **Always** have `eeprom.bak` before any `-i`. A bad flash is
  recoverable from it; without it, an SPI programmer is the only way
  back.
- The firmware can be run from SRAM (`image_load`) without ever touching
  NVRAM. Prefer that for all stack iteration.
- dext misbehaviour: `log show --predicate 'sender == "TGDext"'`.
