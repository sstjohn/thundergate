# Thundergate on Linux #

These instructions assume a Debian 8 host.

## Build ##

1. Install dependencies:

    ~~~
$ sudo apt-get install build-essential curl texinfo flex git ca-certificates  \
            gnu-efi python python-dev python-ctypeslib libgmp-dev libmpfr-dev \
	    libmpc-dev python-pip ipython
$ sudo pip install capstone bidict pyelftools
$ sudo easy_install git+http://github.com/sstjohn/python-eficompressor.git
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

## Install ##

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

## Use ##

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