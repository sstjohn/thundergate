SECTIONS
{
    .text 0x08008000 : { 
        entry.o(.text)
        *(.text)
	main.o(.text)
    }

    .data ADDR(.text)+SIZEOF(.text) : { 
        *(.data) 
    }

    .rodata ADDR(.data)+SIZEOF(.data) : { 
        *(.rodata)
	*(.rodata.*) 
    }


    .bss ADDR(.rodata)+SIZEOF(.rodata) : { 
        *(.bss) 
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
