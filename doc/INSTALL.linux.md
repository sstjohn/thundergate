# Thundergate on Linux #

These instructions assume a Debian 8 host.

## Build ##

1. Install external dependencies:

    ~~~
$ sudo apt-get install build-essential curl texinfo flex git ca-certificates  \
            gnu-efi python python-dev python-ctypeslib libgmp-dev libmpfr-dev \
	    libmpc-dev python-pip ipython
$ sudo pip install capstone bidict pyelftools
    ~~~

2. Clone repository:

    ~~~
$ git clone http://github.com/sstjohn/thundergate.git
$ cd thundergate
$ git submodule init
$ git submodule update
    ~~~

3. Install distributed dependencies:

    ~~~
$ pip install ./python-eficompressor
    ~~~

4. Build Tigon3 cross-tools following the instructions from [firmware.md](firmware.md).

5. Compile ThunderGate:

    ~~~
$ cd thundergate
$ make
    ~~~

## Install ##

For maximal userspace tap driver performance, the network interface device
should be bound to the ```vfio-pci``` kernel module. This appears to be the
only standard interface for receiving MSI/MSIX interrupts in userspace on
Linux; users without an IOMMU are out of luck. Absent that, the driver operates
by polling on the status block for updates, at the cost of responsiveness and
energy efficiency.

First, determine the BDF of your Tigon3 device. This information can be
obtained from, e.g., ```lspci```:

~~~
$ sudo lspci -d14e4: | grep Ethernet
0a:00.0 Ethernet controller: Broadcom Corporation NetXtreme BCM57762 Gigabit Ethernet PCIe
~~~

As is commonly the case on Apple hardware, the BDF for the Thunderbolt NIC in
this example is '0a:00.0'. Next, unbind the device from the default kernel
module (likely tg3), and rebind it to vfio-pci as such:

~~~
$ sudo modprobe vfio-pci
$ echo $BDF | sudo tee /sys/bus/pci/devices/$BDF/driver/unbind
$ echo $BDF | sudo tee /sys/bus/pci/drivers/vfio-pci/bind
~~~

## Use ##

<pre>
$ py/main.py -h
usage: main.py [-h] [--device DEVICE] [-p] [--ptvsdpass PTVSDPASS]
               [--ptvsdwait] [-t] [-s] [-b] [-d] [-i]

optional arguments:
  -h, --help            show this help message and exit
  --device DEVICE       BDF of tg3 PCI device
  -p, --ptvsd           enable ptvsd server
  --ptvsdpass PTVSDPASS
                        ptvsd server password
  --ptvsdwait           wait for ptvsd attachment at startup
  -t, --tests           run tests
  -s, --shell           ipython cli
  -b, --backup          create eeprom backup
  -d, --driver          load userspace tap driver
  -i, --install         install thundergate firmware
</pre>
