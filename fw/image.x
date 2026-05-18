SECTIONS
{
    /* Load/run address. The RX-CPU scratch pad is 0x08000000-0x0800FFFF
       (64 KB). Apple's own on-NIC firmware loads RX-CPU images at this base
       (see fw/apple-ref -- its mDNS/Bonjour image is ~40 KB) with the stack
       at the top of the pad, 0x08010000. The image is loaded to 0x08000000
       by the host (py/blocks/cpu.py image_load) or by the bootcode; text,
       rodata, data and bss grow up from here while the stack grows down
       from 0x08010000, so the whole 64 KB is available. */
    .text 0x08000000 : {
        entry.o(.text)
        *(.text)
        main.o(.text)
    }

    .rodata ADDR(.text)+SIZEOF(.text) : {
        *(.rodata)
        *(.rodata.*)
    }

    .data ADDR(.rodata)+SIZEOF(.rodata) : {
        *(.data)
        PROVIDE(_edata = .);
    }

    .bss ADDR(.data)+SIZEOF(.data) : {
        *(.bss)
        PROVIDE(_end = .);
    }

    /* text+data+bss must stop short of the 0x08010000 stack; this leaves
       at least 8 KB of headroom and fails the link loudly otherwise. */
    ASSERT(_end <= 0x0800E000, "firmware image overflows the scratch pad")

    .eh_frame : {
	    *(.eh_frame)
    }

    .pdr : {
	    *(.pdr)
    }

    .reginfo : {
        *(.reginfo)
    }

    .MIPS.abiflags : {
	    *(.MIPS.abiflags)
    }

    .scommon : {
        *(.scommon)
    }
}
