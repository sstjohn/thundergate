<pre>
#######                                            #####
   #    #    # #    # #    # #####  ###### #####  #     #   ##   ##### ######
   #    #    # #    # ##   # #    # #      #    # #        #  #    #   #
   #    ###### #    # # #  # #    # #####  #    # #  #### #    #   #   #####
   #    #    # #    # #  # # #    # #      #####  #     # ######   #   #
   #    #    # #    # #   ## #    # #      #   #  #     # #    #   #   #
   #    #    #  ####  #    # #####  ###### #    #  #####  #    #   #   ######

                             Version 0.9.5
                 Copyright (c) 2015-2016 Saul St John
                          http://thundergate.io
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

# Further Reading #

 * [Linux usage](doc/README.linux.md)
 * [Windows usage](doc/README.windows.md)
 * [Firmware usage](doc/README.firmware.md)

Additionally, an old report describing an older version of this project can be
found at <http://thundergate.io/tg_old.pdf>.
