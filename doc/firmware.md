# Thundergate Firmware #

## Toolchain ##

Building custom firmware needs a cross-compiler for the Tigon3's MIPS-ish
core. Build one with:

    ~~~
$ misc/build-toolchain.sh
    ~~~

This produces a mips-elf GCC 14.2 cross-toolchain under `toolchain/`. GCC is
patched (`misc/mtigon-patch.py`) with a `-mtigon` target that suppresses the
instructions the core lacks -- unaligned load/store, hardware
multiply/divide, and the HI/LO registers -- so multiply and divide go through
libgcc's soft routines instead. Add `toolchain/bin` to your PATH so
`fw/Makefile` finds `mips-elf-gcc`. The script runs on Linux and macOS.

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
	  Version 1.0
Copyright (C) 2015-2026  Saul St. John
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
