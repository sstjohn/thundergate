<pre>
#######                                            #####
   #    #    # #    # #    # #####  ###### #####  #     #   ##   ##### ######
   #    #    # #    # ##   # #    # #      #    # #        #  #    #   #
   #    ###### #    # # #  # #    # #####  #    # #  #### #    #   #   #####
   #    #    # #    # #  # # #    # #      #####  #     # ######   #   #
   #    #    # #    # #   ## #    # #      #   #  #     # #    #   #   #
   #    #    #  ####  #    # #####  ###### #    #  #####  #    #   #   ######

                                 Version 0.5.0
                        Copyright (c) 2015 Saul St John

                            <a href="http://thundergate.io">http://thundergate.io</a>
</pre>

# Introduction #

ThunderGate is a collection of tools for the manipulation of Tigon3 Gigabit
Ethernet controllers, with special emphasis on the Broadcom NetLink 57762,
such as is found in Apple Thunderbolt Gigabit Ethernet adapters.

Tigon3 controllers contain a variety of architectural blocks, including a PCI
endpoint, an 802.3 media access controller, on-chip ram, DMA read and write
engines, nonvolatile storage, and one or more MIPS processors.

These features are exposed by ThunderGate through an easy-to-use Python
interface, allowing for reverse engineering, development, and deployment of
custom firmware and applications. Examples provided include a userspace VFIO
tap driver, a firmware application capable of monitoring and manipulating
network traffic and host memory, and a PCI option rom containing an EFI boot
services driver which can either inhibit the employ or compromise the 
effectivity of Intel I/O MMU address translation (VT-d).

# Warning #

This is experimental software made available to you under the terms of
the GPLv3. You assume all risks in using it. Please refer to the COPYING file
for details.

# Host Installation #

These instructions assume a Debian 8 host.

1. Install dependencies:

    ~~~
$ sudo apt-get install build-essential curl texinfo flex git ca-certificates  \
            gnu-efi python python-ctypeslib libgmp-dev libmpfr-dev libmpc-dev \
            python-pip ipython
$ sudo pip install capstone bidict
$ sudo easy_install git+http://github.com/nebula/python-eficompressor.git
    ~~~

2. Clone repository:

    ~~~
$ git clone http://github.com/sstjohn/thundergate.git
    ~~~

3. Retrieve, compile and install cross mips-elf binutils:

    ~~~
$ curl -O http://ftp.gnu.org/gnu/binutils/binutils-2.25.tar.bz2
$ tar xfi binutils-2.25.tar.bz2
$ mkdir binutils-build
$ pushd binutils-build
$ ../binutils-2.25/configure --target=mips-elf --with-sysroot --disable-nls
$ make && sudo make install && popd
    ~~~

4. Retrieve, patch, compile and install cross mips-elf GCC 5.1:

    ~~~
$ curl -O http://ftp.gnu.org/gnu/gcc/gcc-5.1.0/gcc-5.1.0.tar.bz2
$ tar xfi gcc-5.1.0.tar.bz2
$ pushd gcc-5.1.0
$ patch -p1 < ../thundergate/misc/gcc-5.1.0-mtigon.patch
$ popd
$ mkdir gcc-build
$ pushd gcc-build
$ ../gcc-5.1.0/configure --target=mips-elf --program-prefix=mips-elf-        \
        --disable-nls --enable-languages=c,c++ --without-headers             \
        --without-llsc --with-tune=r6000 --with-arch=mips2 --disable-biarch  \
        --disable-multilib --with-float=soft --without-hard-float
$ make all-gcc && make all-target-libgcc
$ sudo make install-gcc && sudo make install-target-libgcc && popd
    ~~~

5. Compile ThunderGate:

    ~~~
$ cd thundergate
$ make
    ~~~

# Host Setup #

You should begin by taking a backup image of the factory-released firmware as
it was when you bought the device. This image can be used to restore the device
to a working state in the event that you should break it using ThunderGate.
See `man ethtool` for details on conducting a device firmware dump.

In order to launch ThunderGate, you will need to know the BDF
(Bus-Device-Function) of your Tigon3 device. This information can be
obtained from, e.g., ```lspci```:

~~~
$ sudo lspci -d14e4: | grep Ethernet
0a:00.0 Ethernet controller: Broadcom Corporation NetXtreme BCM57762 Gigabit Ethernet PCIe
~~~

As is commonly the case on Apple hardware, the BDF for the Thunderbolt
Gigabit in this example is '0a:00.0'.

In order to use the userspace tap driver, the network interface device
will need to be bound to the ```vfio-pci``` kernel module:
~~~
$ sudo modprobe vfio-pci
$ echo $BDF | sudo tee /sys/bus/pci/devices/$BDF/driver/unbind
$ echo $BDF | sudo tee /sys/bus/pci/drivers/vfio-pci/bind
~~~

All other functionality is available regardless of the kernel driver in use.

# Local Usage #

<pre>
$ py/main.py -h
usage: main.py [-h] [-v] [-d] [-t] [-s] device

positional arguments:
  device        BDF of tg3 PCI device

optional arguments:
  -h, --help     show this help message and exit
  -i, --install  install thundergate firmware
  -u, --uio      use uio pci generic interface
  -v, --vfio     use vfio interface
  -d, --driver   load userspace tap driver
  -t, --tests    run tests
  -s, --shell    ipython cli
</pre>

## Firmware Installation ##

The ```-i``` argument can be used to install all example firmware
to a Thunderbolt Gigabit Ethernet adapter device as follows:
<pre>
 $ sudo py/main.py -i 0a:00.0

          ThunderGate
	 Version 0.5.0
Copyright (c) 2015 Saul St John
     http://thundergate.io

[+] tg3 inspector initializing
[+] huge pages available
[+] enumerating device capabilities
[+] mapping device memory window
[+] masking interrupts
[+] requesting nvram lock...  granted.
[+] enabling nvram access
[+] resetting nvram state machine
[+] requesting nvram lock...  granted.
[+] enabling nvram access
[+] enabling nvram write in grc block
[+] enabling nvram write access
[+] installing thundergate oprom
[+] writing block length 4604 at offset 25fc.....................
[+] installing thundergate rxcpu firmware
[+] writing block length 1630 at offset 6c00.........
[+] tg3 inspector terminated
</pre>

## Firmware Usage ##

The ThunderGate firmware implements a network protocol allowing for remote
control of the device and host system by an Ethernet-connected peer.
Currently supported actions include reading and writing from device and host
memory, forging network traffic, sending host interrupts, and manipulation
of PCI capabilities configuration. Please refer to ```fw/app.c```, 
```include/proto.c```, and ```py/client.py``` for specifics.

# Further Reading #

A report describing an older version of this project can be found at
<http://pages.cs.wisc.edu/~sstjohn/tg_old.pdf>.
