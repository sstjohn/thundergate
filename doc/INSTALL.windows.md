# Thundergate on Windows #

These instructions assume a Windows 10 x64.

## Dependencies ##

1. Install Python 2.7 x64. Make sure to select the option to add the Python
binary to your system PATH.

2. Install Visual Studio 2015, the Windows Driver Kit for Windows 10, and
Python Tools for Visual Studio.

3. Install Microsoft Visual C++ for Python 2.7.

4. Install required Python packages from an administrative command prompt:

    ~~~
C:\>pip install bidict ipython pyreadline
    ~~~

5. Clone Thundergate source repository:

    ~~~
C:\>git clone http://github.com/sstjohn/thundergate.git
C:\>cd thundergate
C:\thundergate>git submodule init
C:\thundergate>git submodule update
    ~~~

6. Optionally, install CMake, and then Python packages required for firmware
debugging. From an administrative VS2015 x64 Native Tools Command Crompt (found
under Start -> All Apps -> Visual Studio 2015, right click, select More -> Run
as Administrator):

    ~~~
C:\thundergate>pip install pyelftools capstone
    ~~~

7. Optionally, install the included Python EFI image compression package, which
is required for firmware development. Again from an administrative VS2015 x64
Native Tools Command Prompt:

    ~~~
c:\thundergate>pip install .\python-eficompressor
    ~~~

8. Optionally, install MSYS2, and then follow the instructions in
[firmware.md] to install a binutils/gcc
toolchain targeting the Tigon3's MIPS processor.

9. Optionally, install the TAP-Windows6 package from OpenVPN. This package is
required in order to use the Thundergate TAP adapter functionality.

## Build ##

To build from the IDE, open the file win\tgwin.sln in Visual Studio 2015, and
select "Build Solution" from the Build menu.

To build from a VS2015 x64 Native Tools Command Prompt:

   ~~~
c:\thundergate>msbuild win\tgwin.sln
   ~~~

## Install ##

A driver is required for operation on Windows 10, as PCI resources aren't
conveniently laid out for userspace consumption under /sys as they are in
Linux. Be advised this driver necessarily replaces the Broadcom-developed
driver for the device, precluding its normal use as a network adapter.

As a result of Windows 10's driver signing requirements, you will need to
enable "Test Mode" to install the Thundergate driver. From an administrative
command prompt, run:

   ~~~
c:\>bcdedit -set testsigning on
The operation completed successfully.
   ~~~

After rebooting, the words "Test Mode" should appear in the lower left corner
of your desktop.

Next, you will need to install your test signing certificate, generated during
the build, into the Windows Trusted Root Certificate store. From an
administrative VS2015 x64 Native Tools Command Prompt:

   ~~~
c:\>certmgr.exe -add thundergate\win\x64\debug\tgwink.cer -s -r localMachine root
CertMgr Succeeded
   ~~~

Finally, install the driver itself:

   ~~~
c:\>devcon update thundergate\win\x64\debug\tgwink\tgwink.inf "pci\ven_14e4&dev_1682"
Updating drivers for pci\ven_14e4&dev_1682 from c:\thundergate\win\x64\debug\tgwink\tgwink.inf.
Drivers installed successfully.
   ~~~

Possibly subsequent to a reboot, your Broadcom NetLink device will have
disappeared from the 'Network Adapters' subtree in Device Manager, and a new
device named 'tgwink Device' will have appeared under 'System Devices.' This
indicates only that the driver was successfully installed; the device itself
remains unmodified by this procedure. Check to ensure that the 'tgwink Device'
is present in the Device Manager and that its device properties do not report
an error code. 

## Use ##

    ~~~
c:\thundergate>python py\main.py --help

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

usage: main.py [-h] [-p] [--ptvsdpass PTVSDPASS] [--ptvsdwait] [-t] [-s] [-b]
               [-d] [-i]

optional arguments:
  -h, --help            show this help message and exit
  -p, --ptvsd           enable ptvsd server
  --ptvsdpass PTVSDPASS
                        ptvsd server password
  --ptvsdwait           wait for ptvsd attachment at startup
  -t, --tests           run tests
  -s, --shell           ipython cli
  -b, --backup          create eeprom backup
  -d, --driver          load userspace tap driver
  -i, --install         install thundergate firmware

    ~~~
