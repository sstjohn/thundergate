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

int global_variable = 0;
const int constant_integer = 0x31337;

void leaf_function()
{
    global_variable++;
}

void non_leaf_function(int i)
{
    int j = 0;
    while (j < i) 
        j++;
    leaf_function();
}

int test() 
{
    int i = 0;
    while (i < 0xff)
        i++;
    non_leaf_function(i);
    return 0;
}
