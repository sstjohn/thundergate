# Thundergate Firmware #

## Toolchain ##

A bespoke cross-compiler targeting the Tigon3 (MIPS-ish) processor is required
in order to build custom firmware targeting the device. Produce one as follows
on Linux, or on Windows within an MSYS2 environment.

1. Retrieve, compile and install cross mips-elf binutils:

    ~~~
$ curl -O http://ftp.gnu.org/gnu/binutils/binutils-2.25.tar.bz2
$ tar xfi binutils-2.25.tar.bz2
$ mkdir binutils-build
$ pushd binutils-build
$ ../binutils-2.25/configure --target=mips-elf --with-sysroot --disable-nls
$ make && sudo make install && popd
    ~~~

2. Retrieve, patch, compile and install cross mips-elf GCC 5.1:

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

## Build ##

On both Linux and Windows, firmware image compilation is Makefile-driven,
although basic hooks are present to trigger firmware recompilation from within
VS2015 if MSYS2 is available. The top-level make target 'fw' serves to produce
output files fw/fw.elf, a debuggable MIPS ELF executable with symbols, and
fw/fw.img, a stripped version of the former linked appropriate for execution on
the Tigon3 core.

## Install ##

You should begin by taking a backup image of the factory-released firmware as
it was when you bought the device. This image can be used to restore the device
to a working state in the event that you should break it using ThunderGate, or
should you wish to restore its original functionality. You will be presented
with the option to create such a backup if the file 'eeprom.bak' does not exist
in the project root; it is highly recommended that you do so.

The ```-i``` argument can be used to install built example firmware
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

## Use ##

The ThunderGate firmware implements a network protocol allowing for remote
control of the device and host system by an Ethernet-connected peer.  Currently
supported actions include reading and writing from device and host memory,
forging network traffic, sending host interrupts, and manipulation of PCI
capabilities configuration. Please refer to ```fw/app.c```,
```include/proto.h```, and ```py/client.py``` for specifics.
