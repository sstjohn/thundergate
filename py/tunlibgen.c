/*
 *  ThunderGate - an open source toolkit for PCI bus exploration
 *  Copyright (C) 2015  Saul St. John
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <stdio.h>

#ifdef _MSC_VER
#include <tap-windows.h>
#else
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <linux/socket.h>
#include <linux/if.h>
#include <linux/if_tun.h>
#endif

int main(int argc, char *argv[])
{
    printf("TUNSETIFF = 0x%x\n", TUNSETIFF);
    printf("IFF_TUN = 0x%x\n", IFF_TUN);
    printf("IFF_TAP = 0x%x\n", IFF_TAP);
    printf("IFF_NO_PI = 0x%x\n", IFF_NO_PI);
    printf("IFNAMSIZ = 0x%x\n", IFNAMSIZ);

    return 0;
}
