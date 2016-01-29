#!/usr/bin/env python

import os
import shutil
import sys

def mkdir_f(path):
    try:
        os.mkdir(path)
    except OSError as e:
        if e.errno == 17:
            return
        raise e

if __name__ == "__main__":
    tgdir = sys.argv[0]
    if tgdir != "":
        tgdir = os.path.abspath(tgdir)
        tgdir = os.sep.join(tgdir.split(os.sep)[:-2])
        cwd = os.getcwd()
        if tgdir != cwd:
            os.chdir(tgdir)

    path = os.path.expanduser("~")
    for d in [".vscode", "extensions", "thundergate"]:
        path += os.sep + d
        mkdir_f(path)

    shutil.copy("vsc-ext/package.json", path)
    shutil.copy("py/cdp.py", path)
    with open("%s/tgdir.conf" % path, "w") as f:
        f.write(tgdir)

    print "all set"
