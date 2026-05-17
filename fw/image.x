SECTIONS
{
    /* Bootcode load address. The Tigon3 ROM loads the firmware to
       bc_sram_start (0x08008000, from the NVRAM header bs struct) and
       jumps there, so the image MUST link here to match. The scratch
       pad is 0x08000000-0x0800FFFF (64 KB); from 0x08008000 only the
       upper 32 KB is usable -- text+data+bss+stack must all fit within
       0x08008000-0x0800FFFF. */
    .text 0x08008000 : {
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
