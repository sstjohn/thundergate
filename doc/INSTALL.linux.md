# ThunderGate on Linux

These instructions target a current Linux distribution (Debian 12+,
Ubuntu 24.04+, or similar) with Python 3.13 or newer.

## Build

1. Install the build dependencies (Debian/Ubuntu names):

   ~~~
   $ sudo apt-get install build-essential git texinfo flex bison \
         python3 python3-venv python3-dev \
         libgmp-dev libmpfr-dev libmpc-dev \
         bolt
   ~~~

2. Clone the repository and its submodules:

   ~~~
   $ git clone https://github.com/sstjohn/thundergate.git
   $ cd thundergate
   $ git submodule update --init --recursive
   ~~~

3. Create the Python virtualenv and install the dependencies:

   ~~~
   $ python3 -m venv .venv
   $ .venv/bin/pip install -r requirements.txt
   $ .venv/bin/pip install ext/python-eficompressor
   ~~~

4. Build the Tigon3 MIPS cross-toolchain (see [firmware.md](firmware.md)):

   ~~~
   $ misc/build-toolchain.sh
   ~~~

5. Build the firmware and verify it:

   ~~~
   $ misc/verify-fw.sh
   ~~~

## Thunderbolt authorization

Many Tigon3 adapters on Apple hardware are Thunderbolt devices. Modern
Linux gates Thunderbolt devices behind a security level managed by
`boltctl`; an unauthorized device will not appear on the PCI bus.

List devices and authorize the NIC:

~~~
$ boltctl list
$ boltctl authorize <uuid>      # authorize for this session
$ boltctl enroll <uuid>         # optional: authorize permanently
~~~

If `boltctl list` shows nothing and the adapter is plugged in, the
Thunderbolt security level may be `secure` or `dponly`; `boltctl` is
still the tool to authorize it.

## Binding to vfio-pci

For the userspace TAP driver, bind the NIC to `vfio-pci` — that is the
standard way to receive MSI/MSI-X interrupts in userspace on Linux, and
it requires an IOMMU. Without it the driver falls back to polling the
status block, at a cost in responsiveness and power.

Find the device's BDF:

~~~
$ lspci -d 14e4: | grep Ethernet
0a:00.0 Ethernet controller: Broadcom ... NetXtreme BCM57762 Gigabit Ethernet PCIe
~~~

Bind it to `vfio-pci` using `driver_override`:

~~~
$ BDF=0000:0a:00.0
$ sudo modprobe vfio-pci
$ echo vfio-pci | sudo tee /sys/bus/pci/devices/$BDF/driver_override
$ echo $BDF | sudo tee /sys/bus/pci/devices/$BDF/driver/unbind
$ echo $BDF | sudo tee /sys/bus/pci/drivers_probe
~~~

The flash path (`-b`, `-i`) also works against the default `tg3` driver
through sysfs, but `-d` (the TAP driver) needs `vfio-pci`.

## Use

~~~
$ .venv/bin/python3 py/main.py --help
  -b, --backup    create eeprom backup
  -i, --install   install thundergate firmware
  -d, --driver    load userspace tap driver
  -s, --shell     ipython cli
~~~

Always capture an EEPROM backup before flashing:

~~~
$ .venv/bin/python3 py/main.py -b
$ .venv/bin/python3 py/main.py -i
~~~
