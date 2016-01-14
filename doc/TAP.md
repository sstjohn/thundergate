# Thundergate TAP Driver #

The Thundergate toolkit includes Python modules inplementing a 
PCI driver for Broadcom 57xx devices, and a TAP interface driver
consuming it. Used together, they provide a userspace hardware 
interface between the network hardware and the kernel's TCP/IP
stack.

This functionality is available on Windows and Linux.

## Usage ##

Specify `-d` on the command line to start the execution of the driver. Eg:

Windows:

    ~~~
c:\thundergate\>python py\main.py -d
    ~~~

Linux:

    ~~~
$ python py/main.py -d $DEVICE_BDF
    ~~~

The driver runs in the foreground offers a minimal single-key interface.

    ~~~
...
[+] produced 128 rx buffers
[+] enabling transmit mac
[+] enabling receive mac
[+] configuring led
[+] waiting for interrupts...
[+] detecting link
[+] full duplex gige link negotated (res: 0000ff3c, txpause: False, rxpause: False)

d - link detect
h - help
q - quit
s - dump statistics
r - reset statistics
v - toggle verbosity
    ~~~

## Notes ##

 * The TAP interface created will assume the next available device name
on the host system, e.g. 'tapX' on Linux, or "TAP-Windows Adapter #X." It
should only persist for the life of the process, but the cleanup code
is in `finally` blocks, so crashed processes might leave behind dead
interfaces requring manual cleanup.

 * The TAP device will bring itself up and down based on the state of
the link, but may need IP configuration using host OS tools (such
as Linux's `ip` or `ifconfig`,  or Windows's `ipconfig` or `ncpa.cpl`.)

 * Link detection and change notifications are hit-and-miss, and may not
trigger at startup. Press `d` to force link re-negotiation.

## Performance ##

Performance was measured using iPerf3 over a point-to-point Cat5 cable
connecting a MacBook Air running Debian 8 and a MacBook Pro running
Windows 10. These numbers are only meaningful relatively.

(to be continued...)