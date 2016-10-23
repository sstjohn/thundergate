SECTIONS
{
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
