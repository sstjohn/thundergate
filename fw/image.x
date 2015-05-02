SECTIONS
{
    .text 0x08008000 : { 
        main.o(.text)
        *(.text)
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
