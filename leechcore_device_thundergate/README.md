# leechcore_device_thundergate

A LeechCore device plugin that lets **MemProcFS / LeechCore** acquire the
physical memory of a machine fitted with a ThunderGate-flashed Broadcom
NIC -- e.g. inspect an Intel host from an Apple Silicon Mac.

## Pieces

    MemProcFS / LeechCore            (e.g. Apple Silicon Mac)
        |  -device thundergate://daemon=<host>:<port>
        v
    leechcore_device_thundergate     (this plugin, .dylib / .so)
        |  TCP, 16-byte little-endian request protocol
        v
    py/leechbridge.py                (daemon; Linux, target's segment)
        |  ThunderGateInterface -- raw Ethernet, EtherType 0x88b5
        v
    rxcpu firmware  ->  dma_read / dma_write  ->  target host RAM

`leechbridge.py` must run on a Linux host on the same Ethernet segment as
the target's NIC -- ThunderGate's control protocol needs `AF_PACKET`. The
plugin and MemProcFS run wherever you do the analysis and reach the
daemon over TCP.

## Run

Daemon, on a Linux box on the target's segment, as root:

    python3 py/leechbridge.py eth0 --listen 0.0.0.0:28473 --size 0x200000000

Analysis host:

    memprocfs -device 'thundergate://daemon=10.0.0.2:28473'

## Build

Drop this directory into a [LeechCore-plugins](https://github.com/ufrisk/LeechCore-plugins)
checkout, next to `leechcore_device_skeleton`, then `make`. The build
needs that project's `includes/leechcore_device.h` and the `leechcore`
runtime library; the result lands in `../files/`.

## Status

- `py/leechbridge.py` -- complete; relays READ / WRITE / INFO to the
  `ThunderGateInterface` in `client.py`.
- The plugin C -- written to the LeechCore-plugins skeleton ABI but **not
  verified against a live build**. If a struct field or helper differs in
  your `leechcore_device.h` (the `LcMemMap_AddRange` and `Config.fVolatile`
  lines are the likely spots), adjust per the comments in the `.c`.
- Writes depend on the rxcpu `dma_write` firmware, which is itself
  hardware-unverified. Reads (`dma_read`) work first; writes once
  `dma_write` is brought up on hardware.
