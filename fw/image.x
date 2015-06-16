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
    }


    .bss ADDR(.rodata)+SIZEOF(.rodata) : { 
        *(.bss) 
    }

    .reginfo : {
        *(.reginfo)
    }
}
