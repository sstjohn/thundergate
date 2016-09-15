import sys

if sys.platform == "win32":
    from win_fun import *
elif sys.platform == "linux2":
    from linux_fun import *
else:
    raise NotImplementedError("only win32 and linux are supported")
