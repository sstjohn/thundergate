'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2016 Saul St. John

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import json
import sys
import platform
import traceback
import functools

def find_tgmain():
    pname = os.path.abspath(sys.argv[0])
    pdir = os.path.dirname(pname)
    mname = ""
    if os.path.exists(pdir + os.sep + "main.py"):
        mname = pdir + os.sep + "main.py"
    else:
        try:
            sname = os.readlink(pname)
            sdir = os.path.dirname(sname)
            if os.path.exists(sdir + os.sep + "main.py"):
                mname = sdir + os.sep + "main.py"
        except: pass
    if len(sys.argv) > 1:
        adir = sys.argv[1]
        if os.path.exists(adir + os.sep + "py" + os.sep + "main.py"):
            mname = adir + os.sep + "py" + os.sep + "main.py"
    if mname == "":
        try:
            edir = os.environ["TGDIR"]
            if os.path.exists(edir + os.sep + "py" + os.sep + "main.py"):
                mname = edir + os.sep + "py" + os.sep + "main.py"
        except: pass
    if mname == "" and os.path.exists(pdir + os.sep + "tgdir.conf"):
        with open(pdir + os.sep + "tgdir.conf", "r") as f:
            fdir = f.readline().strip()
        if os.path.exists(fdir + os.sep + "py" + os.sep + "main.py"):
            mname = fdir + os.sep + "py" + os.sep + "main.py"
    if mname == "":
        raise Exception("couldn't locate thundergate directory")
    return mname

if __name__ == "__main__":
    main_file = find_tgmain()
    os.chdir(os.path.dirname(os.path.dirname(main_file)))
    sys.path = [os.path.dirname(main_file)] + sys.path
    import main
    sys.exit(main.main([main_file, "--cdpserver"]))
