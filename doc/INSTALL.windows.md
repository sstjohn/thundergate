# ThunderGate on Windows

These instructions target Windows 11 x64 with Python 3.13 or newer.

## Dependencies

1. Install **Python 3.13+ (64-bit)** and add it to `PATH`.

2. Install **Visual Studio 2022** with the *Desktop development with C++*
   workload, the **Windows Driver Kit (WDK)** matching your Windows SDK,
   and (optionally) the *Python development* workload.

3. Clone the repository and its submodules:

   ~~~
   C:\>git clone https://github.com/sstjohn/thundergate.git
   C:\>cd thundergate
   C:\thundergate>git submodule update --init --recursive
   ~~~

4. Create the virtualenv and install the Python dependencies:

   ~~~
   C:\thundergate>py -m venv .venv
   C:\thundergate>.venv\Scripts\pip install -r requirements.txt
   C:\thundergate>.venv\Scripts\pip install ext\python-eficompressor
   ~~~

5. *Optional, for firmware development:* install MSYS2 and build the
   Tigon3 MIPS cross-toolchain following [firmware.md](firmware.md).

6. *Optional, for the TAP adapter:* install the TAP-Windows6 package
   from OpenVPN.

## Build

From the IDE: open `win\tgwin.sln` in Visual Studio 2022 and *Build
Solution*. From a *x64 Native Tools Command Prompt*:

~~~
C:\thundergate>msbuild win\tgwin.sln
~~~

## Install the driver

Windows cannot expose PCI resources to userspace the way Linux sysfs
does, so the `tgwink` kernel driver is required. It replaces the
Broadcom network driver for the device, so the NIC stops working as an
ordinary network adapter while `tgwink` is bound.

### Driver signing

Windows 11 x64 enforces driver signing. There are two paths:

- **Development (test signing).** Enable test mode, then trust the
  certificate the build produced:

  ~~~
  C:\>bcdedit -set testsigning on
  ~~~

  Reboot ("Test Mode" appears at the lower-right of the desktop), then,
  from an administrative prompt, add the test certificate to both the
  Trusted Root and Trusted Publishers stores:

  ~~~
  C:\>certutil -addstore -f root  win\x64\Debug\tgwink.cer
  C:\>certutil -addstore -f trustedpublisher win\x64\Debug\tgwink.cer
  ~~~

- **Production (attestation signing).** For a driver that installs
  without test mode, the driver package must be signed through the
  Microsoft Hardware Developer portal: submit the `.cab` for
  **attestation signing** (this needs an Azure-linked partner account
  and an EV code-signing certificate). Attestation signing returns a
  Microsoft-signed package that Windows 11 accepts normally. ThunderGate
  is a research tool, so test signing is the expected path.

### DMA remapping (Kernel DMA Protection)

On Windows 11, Kernel DMA Protection blocks bus-mastering Thunderbolt /
PCIe devices while the machine is locked. `tgwink.inf` now declares
`DmaRemappingCompatible`, so the device keeps working with the IOMMU
enabled and is not cut off when the screen locks. No extra step is
needed; this note is here so the behaviour is not mistaken for a fault.

### Installing

From an administrative prompt:

~~~
C:\>pnputil /add-driver win\x64\Debug\tgwink\tgwink.inf /install
~~~

(`devcon update ... "pci\ven_14e4&dev_1682"` also works if you have
`devcon` from the WDK.)

After installation the Broadcom adapter disappears from *Network
Adapters* in Device Manager and a *tgwink Device* appears under *System
Devices*. Confirm it is present with no error code — the device itself
is unmodified by this; only the bound driver changed.

## Use

~~~
C:\thundergate>.venv\Scripts\python py\main.py --help
  -b, --backup    create eeprom backup
  -i, --install   install thundergate firmware
  -d, --driver    load userspace tap driver
  -s, --shell     ipython cli
~~~

Always capture an EEPROM backup before flashing (`-b`, then `-i`).
