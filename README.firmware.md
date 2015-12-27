# Thundergate Firmware #

## Build ##

## Install ##

You should begin by taking a backup image of the factory-released firmware as
it was when you bought the device. This image can be used to restore the device
to a working state in the event that you should break it using ThunderGate, or
should you wish to restore its original functionality. You will be presented
with the option to create such a backup if the file 'eeprom.bak' does not 
exist in the project root; it is highly recommended that you do so.

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
control of the device and host system by an Ethernet-connected peer.
Currently supported actions include reading and writing from device and host
memory, forging network traffic, sending host interrupts, and manipulation
of PCI capabilities configuration. Please refer to ```fw/app.c```, 
```include/proto.h```, and ```py/client.py``` for specifics.