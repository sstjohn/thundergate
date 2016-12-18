'''Wrapper for acpi.h

Generated with:
/usr/local/bin/ctypesgen.py -I/home/saul/thundergate/include -o tglib.py --no-macros /home/saul/thundergate/include/acpi.h /home/saul/thundergate/include/asf.h /home/saul/thundergate/include/bd.h /home/saul/thundergate/include/bdrdma.h /home/saul/thundergate/include/bufman.h /home/saul/thundergate/include/cfg_port.h /home/saul/thundergate/include/cpmu.h /home/saul/thundergate/include/cpu.h /home/saul/thundergate/include/cr_port.h /home/saul/thundergate/include/dmac.h /home/saul/thundergate/include/dma.h /home/saul/thundergate/include/emac.h /home/saul/thundergate/include/frame.h /home/saul/thundergate/include/ftq.h /home/saul/thundergate/include/gencomm.h /home/saul/thundergate/include/grc.h /home/saul/thundergate/include/hc.h /home/saul/thundergate/include/ma.h /home/saul/thundergate/include/mbox.h /home/saul/thundergate/include/mbuf.h /home/saul/thundergate/include/msi.h /home/saul/thundergate/include/nrdma.h /home/saul/thundergate/include/nvram.h /home/saul/thundergate/include/otp.h /home/saul/thundergate/include/pcie_alt.h /home/saul/thundergate/include/pcie.h /home/saul/thundergate/include/pci.h /home/saul/thundergate/include/proto.h /home/saul/thundergate/include/rbdc.h /home/saul/thundergate/include/rbdi.h /home/saul/thundergate/include/rbdrules.h /home/saul/thundergate/include/rcb.h /home/saul/thundergate/include/rdc.h /home/saul/thundergate/include/rdi.h /home/saul/thundergate/include/rdma.h /home/saul/thundergate/include/regdef.h /home/saul/thundergate/include/rlp.h /home/saul/thundergate/include/rss.h /home/saul/thundergate/include/rtsdi.h /home/saul/thundergate/include/sbdc.h /home/saul/thundergate/include/sbdi.h /home/saul/thundergate/include/sbds.h /home/saul/thundergate/include/sdc.h /home/saul/thundergate/include/sdi.h /home/saul/thundergate/include/stats.h /home/saul/thundergate/include/status_block.h /home/saul/thundergate/include/tcp_seg_ctrl.h /home/saul/thundergate/include/utypes.h /home/saul/thundergate/include/wdma.h

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname

        else:
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# No libraries

# No modules

u8 = c_uint8 # /home/saul/thundergate/include/utypes.h: 36

u16 = c_uint16 # /home/saul/thundergate/include/utypes.h: 37

u32 = c_uint32 # /home/saul/thundergate/include/utypes.h: 38

u64 = c_uint64 # /home/saul/thundergate/include/utypes.h: 39

# /home/saul/thundergate/include/acpi.h: 32
class struct_dmar_tbl_hdr(Structure):
    pass

struct_dmar_tbl_hdr.__slots__ = [
    'sig',
    'length',
    'rev',
    'cksum',
    'oemid',
    'oemtableid',
    'oem_rev',
    'creator_id',
    'creator_rev',
    'host_addr_width',
    'flags',
    'reserved',
]
struct_dmar_tbl_hdr._fields_ = [
    ('sig', c_char * 4),
    ('length', u32),
    ('rev', u8),
    ('cksum', u8),
    ('oemid', c_char * 6),
    ('oemtableid', c_char * 8),
    ('oem_rev', u32),
    ('creator_id', c_char * 4),
    ('creator_rev', u32),
    ('host_addr_width', u8),
    ('flags', u8),
    ('reserved', c_char * 10),
]

# /home/saul/thundergate/include/acpi.h: 53
class struct_anon_1(Structure):
    pass

struct_anon_1.__slots__ = [
    'device',
    'function',
]
struct_anon_1._fields_ = [
    ('device', u8),
    ('function', u8),
]

# /home/saul/thundergate/include/acpi.h: 47
class struct_dmar_dev_scope(Structure):
    pass

struct_dmar_dev_scope.__slots__ = [
    'type',
    'length',
    'reserved',
    'enum_id',
    'start_bus_number',
    'path',
]
struct_dmar_dev_scope._fields_ = [
    ('type', u8),
    ('length', u8),
    ('reserved', u16),
    ('enum_id', u8),
    ('start_bus_number', u8),
    ('path', struct_anon_1 * 1),
]

# /home/saul/thundergate/include/acpi.h: 59
class struct_dmar_drhd(Structure):
    pass

struct_dmar_drhd.__slots__ = [
    'type',
    'length',
    'flags',
    'reserved',
    'seg_no',
    'base_address',
]
struct_dmar_drhd._fields_ = [
    ('type', u16),
    ('length', u16),
    ('flags', u8),
    ('reserved', u8),
    ('seg_no', u16),
    ('base_address', u64),
]

# /home/saul/thundergate/include/acpi.h: 68
class struct_dmar_rmrr(Structure):
    pass

struct_dmar_rmrr.__slots__ = [
    'type',
    'length',
    'flags',
    'reserved',
    'seg_no',
    'base_addr',
    'limit_addr',
]
struct_dmar_rmrr._fields_ = [
    ('type', u16),
    ('length', u16),
    ('flags', u8),
    ('reserved', u8),
    ('seg_no', u16),
    ('base_addr', u64),
    ('limit_addr', u64),
]

# /home/saul/thundergate/include/acpi.h: 78
class struct_dmar_atsr(Structure):
    pass

struct_dmar_atsr.__slots__ = [
    'type',
    'length',
    'flags',
    'reserved',
    'seg_no',
    'dev_scope',
]
struct_dmar_atsr._fields_ = [
    ('type', u16),
    ('length', u16),
    ('flags', u8),
    ('reserved', u8),
    ('seg_no', u16),
    ('dev_scope', struct_dmar_dev_scope * 1),
]

# /home/saul/thundergate/include/acpi.h: 87
class struct_dmar_rhsa(Structure):
    pass

struct_dmar_rhsa.__slots__ = [
    'type',
    'length',
    'reserved',
    'base_addr',
    'proximity_domain',
]
struct_dmar_rhsa._fields_ = [
    ('type', u16),
    ('length', u16),
    ('reserved', u32),
    ('base_addr', u64),
    ('proximity_domain', u32),
]

# /home/saul/thundergate/include/acpi.h: 95
class struct_dmar_andd(Structure):
    pass

struct_dmar_andd.__slots__ = [
    'type',
    'length',
    'reserved',
    'acpi_dev_no',
    'object_name',
]
struct_dmar_andd._fields_ = [
    ('type', u16),
    ('length', u16),
    ('reserved', u8 * 3),
    ('acpi_dev_no', u8),
    ('object_name', c_char * 0),
]

# /home/saul/thundergate/include/acpi.h: 103
class struct_acpi_sdt_hdr(Structure):
    pass

struct_acpi_sdt_hdr.__slots__ = [
    'sig',
    'length',
    'rev',
    'cksum',
    'oemid',
    'oemtableid',
    'oem_rev',
    'creator_id',
    'creator_rev',
]
struct_acpi_sdt_hdr._fields_ = [
    ('sig', c_char * 4),
    ('length', u32),
    ('rev', u8),
    ('cksum', u8),
    ('oemid', c_char * 6),
    ('oemtableid', c_char * 8),
    ('oem_rev', u32),
    ('creator_id', u32),
    ('creator_rev', u32),
]

# /home/saul/thundergate/include/acpi.h: 115
class struct_xsdt(Structure):
    pass

struct_xsdt.__slots__ = [
    'h',
    'sdt',
]
struct_xsdt._fields_ = [
    ('h', struct_acpi_sdt_hdr),
    ('sdt', POINTER(struct_acpi_sdt_hdr) * 0),
]

# /home/saul/thundergate/include/acpi.h: 120
class struct_rsdp_t(Structure):
    pass

struct_rsdp_t.__slots__ = [
    'sig',
    'cksum',
    'oemid',
    'rev',
    'rsdt_address',
]
struct_rsdp_t._fields_ = [
    ('sig', c_char * 8),
    ('cksum', u8),
    ('oemid', c_char * 6),
    ('rev', u8),
    ('rsdt_address', u32),
]

# /home/saul/thundergate/include/acpi.h: 128
class struct_rsdp2_t(Structure):
    pass

struct_rsdp2_t.__slots__ = [
    'sig',
    'cksum',
    'oemid',
    'rev',
    'rsdt_address',
    'length',
    'xsdt_address',
    'extended_cksum',
    'reserved',
]
struct_rsdp2_t._fields_ = [
    ('sig', c_char * 8),
    ('cksum', u8),
    ('oemid', c_char * 6),
    ('rev', u8),
    ('rsdt_address', u32),
    ('length', u32),
    ('xsdt_address', u64),
    ('extended_cksum', u8),
    ('reserved', u8 * 3),
]

# /home/saul/thundergate/include/asf.h: 24
class struct_asf_control(Structure):
    pass

struct_asf_control.__slots__ = [
    'smb_early_attention',
    'smb_enable_addr_0',
    'nic_smb_addr_2',
    'nic_smb_addr_1',
    'smb_autoread',
    'smb_addr_filter',
    'smb_bit_bang_en',
    'smb_en',
    'asf_attention_loc',
    'smb_attention',
    'retransmission_timer_expired',
    'poll_legacy_timer_expired',
    'poll_asf_timer_expired',
    'heartbeat_timer_expired',
    'watchdog_timer_expired',
    'timestamp_counter_en',
    'reset',
]
struct_asf_control._fields_ = [
    ('smb_early_attention', u32, 1),
    ('smb_enable_addr_0', u32, 1),
    ('nic_smb_addr_2', u32, 7),
    ('nic_smb_addr_1', u32, 7),
    ('smb_autoread', u32, 1),
    ('smb_addr_filter', u32, 1),
    ('smb_bit_bang_en', u32, 1),
    ('smb_en', u32, 1),
    ('asf_attention_loc', u32, 4),
    ('smb_attention', u32, 1),
    ('retransmission_timer_expired', u32, 1),
    ('poll_legacy_timer_expired', u32, 1),
    ('poll_asf_timer_expired', u32, 1),
    ('heartbeat_timer_expired', u32, 1),
    ('watchdog_timer_expired', u32, 1),
    ('timestamp_counter_en', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/asf.h: 44
class struct_asf_smbus_input(Structure):
    pass

struct_asf_smbus_input.__slots__ = [
    'reserved',
    'smb_input_status',
    'input_firstbye',
    'input_done',
    'input_ready',
    'data_input',
]
struct_asf_smbus_input._fields_ = [
    ('reserved', u32, 18),
    ('smb_input_status', u32, 3),
    ('input_firstbye', u32, 1),
    ('input_done', u32, 1),
    ('input_ready', u32, 1),
    ('data_input', u32, 8),
]

# /home/saul/thundergate/include/asf.h: 53
class struct_asf_smbus_output(Structure):
    pass

struct_asf_smbus_output.__slots__ = [
    'reserved',
    'clock_input',
    'clock_enable',
    'data_input_value',
    'data_enable',
    'slave_mode',
    'output_status',
    'read_length',
    'get_receive_length',
    'enable_pec',
    'access_type',
    'output_last',
    'output_start',
    'output_ready',
    'data_output',
]
struct_asf_smbus_output._fields_ = [
    ('reserved', u32, 3),
    ('clock_input', u32, 1),
    ('clock_enable', u32, 1),
    ('data_input_value', u32, 1),
    ('data_enable', u32, 1),
    ('slave_mode', u32, 1),
    ('output_status', u32, 4),
    ('read_length', u32, 6),
    ('get_receive_length', u32, 1),
    ('enable_pec', u32, 1),
    ('access_type', u32, 1),
    ('output_last', u32, 1),
    ('output_start', u32, 1),
    ('output_ready', u32, 1),
    ('data_output', u32, 8),
]

# /home/saul/thundergate/include/asf.h: 71
class struct_asf_watchdog_timer(Structure):
    pass

struct_asf_watchdog_timer.__slots__ = [
    'reserved',
    'count',
]
struct_asf_watchdog_timer._fields_ = [
    ('reserved', u32, 24),
    ('count', u32, 8),
]

# /home/saul/thundergate/include/asf.h: 76
class struct_asf_heartbeat_timer(Structure):
    pass

struct_asf_heartbeat_timer.__slots__ = [
    'reserved',
    'count',
]
struct_asf_heartbeat_timer._fields_ = [
    ('reserved', u32, 16),
    ('count', u32, 8),
]

# /home/saul/thundergate/include/asf.h: 81
class struct_asf_poll_timer(Structure):
    pass

struct_asf_poll_timer.__slots__ = [
    'reserved',
    'count',
]
struct_asf_poll_timer._fields_ = [
    ('reserved', u32, 24),
    ('count', u32, 8),
]

# /home/saul/thundergate/include/asf.h: 86
class struct_asf_poll_legacy_timer(Structure):
    pass

struct_asf_poll_legacy_timer.__slots__ = [
    'reserved',
    'count',
]
struct_asf_poll_legacy_timer._fields_ = [
    ('reserved', u32, 24),
    ('count', u32, 8),
]

# /home/saul/thundergate/include/asf.h: 91
class struct_asf_retransmission_timer(Structure):
    pass

struct_asf_retransmission_timer.__slots__ = [
    'reserved',
    'count',
]
struct_asf_retransmission_timer._fields_ = [
    ('reserved', u32, 24),
    ('count', u32, 8),
]

# /home/saul/thundergate/include/asf.h: 96
class struct_asf_time_stamp_counter(Structure):
    pass

struct_asf_time_stamp_counter.__slots__ = [
    'count',
]
struct_asf_time_stamp_counter._fields_ = [
    ('count', u32),
]

# /home/saul/thundergate/include/asf.h: 100
class struct_asf_smbus_driver_select(Structure):
    pass

struct_asf_smbus_driver_select.__slots__ = [
    'enable_smbus_stretching',
    'reserved',
    'rng',
    'valid',
    'div2',
    'rng_enable',
    'rng_reset',
    'reserved2',
]
struct_asf_smbus_driver_select._fields_ = [
    ('enable_smbus_stretching', u32, 1),
    ('reserved', u32, 9),
    ('rng', u32, 2),
    ('valid', u32, 1),
    ('div2', u32, 1),
    ('rng_enable', u32, 1),
    ('rng_reset', u32, 1),
    ('reserved2', u32, 16),
]

# /home/saul/thundergate/include/asf.h: 111
class struct_asf_regs(Structure):
    pass

struct_asf_regs.__slots__ = [
    'control',
    'smbus_input',
    'smbus_output',
    'watchdog_timer',
    'heartbeat_timer',
    'poll_timer',
    'poll_legacy_timer',
    'retransmission_timer',
    'time_stamp_counter',
    'smbus_driver_select',
]
struct_asf_regs._fields_ = [
    ('control', struct_asf_control),
    ('smbus_input', struct_asf_smbus_input),
    ('smbus_output', struct_asf_smbus_output),
    ('watchdog_timer', struct_asf_watchdog_timer),
    ('heartbeat_timer', struct_asf_heartbeat_timer),
    ('poll_timer', struct_asf_poll_timer),
    ('poll_legacy_timer', struct_asf_poll_legacy_timer),
    ('retransmission_timer', struct_asf_retransmission_timer),
    ('time_stamp_counter', struct_asf_time_stamp_counter),
    ('smbus_driver_select', struct_asf_smbus_driver_select),
]

# /home/saul/thundergate/include/bd.h: 24
class struct_sbd_flags(Structure):
    pass

# /home/saul/thundergate/include/bd.h: 69
class struct_sbd(Structure):
    pass

struct_sbd.__slots__ = [
    'addr_hi',
    'addr_low',
    'flags',
    'length',
    'vlan_tag',
    'mss',
    'hdrlen_0_1',
]
struct_sbd._fields_ = [
    ('addr_hi', u32),
    ('addr_low', u32),
    ('flags', struct_sbd_flags),
    ('length', u16),
    ('vlan_tag', u16),
    ('mss', u16, 14),
    ('hdrlen_0_1', u16, 2),
]

# /home/saul/thundergate/include/bd.h: 91
class struct_rbd_flags(Structure):
    pass

# /home/saul/thundergate/include/bd.h: 113
class struct_rbd_error_flags(Structure):
    pass

# /home/saul/thundergate/include/bd.h: 137
class struct_rbd(Structure):
    pass

struct_rbd.__slots__ = [
    'addr_hi',
    'addr_low',
    'length',
    'index',
    'type',
    'flags',
    'ip_cksum',
    'l4_cksum',
    'error_flags',
    'vlan_tag',
    'rss_hash',
    'opaque',
]
struct_rbd._fields_ = [
    ('addr_hi', u32),
    ('addr_low', u32),
    ('length', u16),
    ('index', u16),
    ('type', u16),
    ('flags', struct_rbd_flags),
    ('ip_cksum', u16),
    ('l4_cksum', u16),
    ('error_flags', struct_rbd_error_flags),
    ('vlan_tag', u16),
    ('rss_hash', u32),
    ('opaque', u32),
]

# /home/saul/thundergate/include/bd.h: 152
class struct_rbd_ex(Structure):
    pass

struct_rbd_ex.__slots__ = [
    'addr1_hi',
    'addr1_low',
    'addr2_hi',
    'addr2_low',
    'addr3_hi',
    'addr3_low',
    'len1',
    'len2',
    'len3',
    'reserved',
    'addr0_hi',
    'addr0_low',
    'index',
    'len0',
    'type',
    'flats',
    'ip_cksum',
    'tcp_udp_cksum',
    'error_flags',
    'vlan_tag',
    'rss_hash',
    'opaque',
]
struct_rbd_ex._fields_ = [
    ('addr1_hi', u32),
    ('addr1_low', u32),
    ('addr2_hi', u32),
    ('addr2_low', u32),
    ('addr3_hi', u32),
    ('addr3_low', u32),
    ('len1', u16),
    ('len2', u16),
    ('len3', u16),
    ('reserved', u16),
    ('addr0_hi', u32),
    ('addr0_low', u32),
    ('index', u16),
    ('len0', u16),
    ('type', u16),
    ('flats', u16),
    ('ip_cksum', u16),
    ('tcp_udp_cksum', u16),
    ('error_flags', u16),
    ('vlan_tag', u16),
    ('rss_hash', u32),
    ('opaque', u32),
]

# /home/saul/thundergate/include/bdrdma.h: 24
class struct_bdrdma_mode(Structure):
    pass

struct_bdrdma_mode.__slots__ = [
    'reserved26',
    'addr_oflow_err_log_en',
    'reserved18',
    'pci_req_burst_len',
    'reserved14',
    'attention_enables',
    'enable',
    'reserved0',
]
struct_bdrdma_mode._fields_ = [
    ('reserved26', u32, 6),
    ('addr_oflow_err_log_en', u32, 1),
    ('reserved18', u32, 7),
    ('pci_req_burst_len', u32, 2),
    ('reserved14', u32, 2),
    ('attention_enables', u32, 12),
    ('enable', u32, 1),
    ('reserved0', u32, 1),
]

# /home/saul/thundergate/include/bdrdma.h: 36
class struct_bdrdma_status(Structure):
    pass

struct_bdrdma_status.__slots__ = [
    'reserved10',
    'malformed_tlp_or_poison_tlp_err_det',
    'local_mem_wr_longer_than_dma_len_err',
    'pci_fifo_overread_err',
    'pci_fifo_underread_err',
    'pci_fifo_overrun_err',
    'pci_host_addr_oflow_err',
    'dma_rd_compltn_timeout',
    'compltn_abrt_err',
    'unsup_req_err_det',
    'reserved0',
]
struct_bdrdma_status._fields_ = [
    ('reserved10', u32, 21),
    ('malformed_tlp_or_poison_tlp_err_det', u32, 1),
    ('local_mem_wr_longer_than_dma_len_err', u32, 1),
    ('pci_fifo_overread_err', u32, 1),
    ('pci_fifo_underread_err', u32, 1),
    ('pci_fifo_overrun_err', u32, 1),
    ('pci_host_addr_oflow_err', u32, 1),
    ('dma_rd_compltn_timeout', u32, 1),
    ('compltn_abrt_err', u32, 1),
    ('unsup_req_err_det', u32, 1),
    ('reserved0', u32, 2),
]

# /home/saul/thundergate/include/bdrdma.h: 50
class struct_bdrdma_len_dbg(Structure):
    pass

struct_bdrdma_len_dbg.__slots__ = [
    'rdmad_length_b_2',
    'rdmad_length_b_1',
]
struct_bdrdma_len_dbg._fields_ = [
    ('rdmad_length_b_2', u32, 16),
    ('rdmad_length_b_1', u32, 16),
]

# /home/saul/thundergate/include/bdrdma.h: 55
class struct_bdrdma_rstates_dbg(Structure):
    pass

struct_bdrdma_rstates_dbg.__slots__ = [
    'rbdi_cnt',
    'reserved2',
    'rstate1',
]
struct_bdrdma_rstates_dbg._fields_ = [
    ('rbdi_cnt', u32, 16),
    ('reserved2', u32, 14),
    ('rstate1', u32, 2),
]

# /home/saul/thundergate/include/bdrdma.h: 61
class struct_bdrdma_rstate2_dbg(Structure):
    pass

struct_bdrdma_rstate2_dbg.__slots__ = [
    'host_addr',
    'rstate2',
]
struct_bdrdma_rstate2_dbg._fields_ = [
    ('host_addr', u32, 28),
    ('rstate2', u32, 4),
]

# /home/saul/thundergate/include/bdrdma.h: 66
class struct_bdrdma_bd_status_dbg(Structure):
    pass

struct_bdrdma_bd_status_dbg.__slots__ = [
    'rlctrl',
    'dmad_load_and_mem_ok',
    'int_rh_dmad_load',
    'rh_dmad_load_fst',
    'rh_dmad_done_syn3',
    'rh_dmad_load_en',
    'rh_dmad_no_empty',
    'hold_dmad_n_empty',
    'rwr_ptr',
    'rrd_ptr',
    'dmad_pnt2',
    'dmad_pnt1',
    'dmad_pnt0',
    'dmad_pnt',
    'reserved3',
    'bd_non_mbuf',
    'fst_bd_mbuf',
    'lst_bd_mbuf',
]
struct_bdrdma_bd_status_dbg._fields_ = [
    ('rlctrl', u32, 9),
    ('dmad_load_and_mem_ok', u32, 1),
    ('int_rh_dmad_load', u32, 1),
    ('rh_dmad_load_fst', u32, 1),
    ('rh_dmad_done_syn3', u32, 1),
    ('rh_dmad_load_en', u32, 1),
    ('rh_dmad_no_empty', u32, 1),
    ('hold_dmad_n_empty', u32, 1),
    ('rwr_ptr', u32, 2),
    ('rrd_ptr', u32, 2),
    ('dmad_pnt2', u32, 2),
    ('dmad_pnt1', u32, 2),
    ('dmad_pnt0', u32, 2),
    ('dmad_pnt', u32, 2),
    ('reserved3', u32, 1),
    ('bd_non_mbuf', u32, 1),
    ('fst_bd_mbuf', u32, 1),
    ('lst_bd_mbuf', u32, 1),
]

# /home/saul/thundergate/include/bdrdma.h: 88
class struct_bdrdma_req_ptr_dbg(Structure):
    pass

struct_bdrdma_req_ptr_dbg.__slots__ = [
    'ih_dmad_len',
    'reserved13',
    'txmbuf_left',
    'rh_dmad_load_en',
    'rftq_d_dmad_pnt',
    'rftq_b_dmad_pnt',
]
struct_bdrdma_req_ptr_dbg._fields_ = [
    ('ih_dmad_len', u32, 16),
    ('reserved13', u32, 3),
    ('txmbuf_left', u32, 8),
    ('rh_dmad_load_en', u32, 1),
    ('rftq_d_dmad_pnt', u32, 2),
    ('rftq_b_dmad_pnt', u32, 2),
]

# /home/saul/thundergate/include/bdrdma.h: 97
class struct_bdrdma_hold_d_dmad_dbg(Structure):
    pass

struct_bdrdma_hold_d_dmad_dbg.__slots__ = [
    'reserved4',
    'rhold_b_dmad',
    'reserved0',
]
struct_bdrdma_hold_d_dmad_dbg._fields_ = [
    ('reserved4', u32, 28),
    ('rhold_b_dmad', u32, 2),
    ('reserved0', u32, 2),
]

# /home/saul/thundergate/include/bdrdma.h: 103
class struct_bdrdma_len_and_addr_idx_dbg(Structure):
    pass

struct_bdrdma_len_and_addr_idx_dbg.__slots__ = [
    'rdma_rd_length',
    'reserved0',
]
struct_bdrdma_len_and_addr_idx_dbg._fields_ = [
    ('rdma_rd_length', u32, 16),
    ('reserved0', u32, 16),
]

# /home/saul/thundergate/include/bdrdma.h: 108
class struct_bdrdma_addr_idx_dbg(Structure):
    pass

struct_bdrdma_addr_idx_dbg.__slots__ = [
    'reserved5',
    'h_host_addr_i',
]
struct_bdrdma_addr_idx_dbg._fields_ = [
    ('reserved5', u32, 23),
    ('h_host_addr_i', u32, 5),
]

# /home/saul/thundergate/include/bdrdma.h: 113
class struct_bdrdma_pcie_dbg_status(Structure):
    pass

struct_bdrdma_pcie_dbg_status.__slots__ = [
    'lt_term',
    'reserved27',
    'lt_too_lg',
    'lt_dma_reload',
    'lt_dma_good',
    'cur_trans_active',
    'dr_pci_req',
    'dr_pci_word_swap',
    'dr_pci_byte_swap',
    'new_slow_core_clk_mode',
    'rbd_non_mbuf',
    'rfst_bd_mbuf',
    'rlsd_bd_mbuf',
    'dr_pci_len',
]
struct_bdrdma_pcie_dbg_status._fields_ = [
    ('lt_term', u32, 4),
    ('reserved27', u32, 1),
    ('lt_too_lg', u32, 1),
    ('lt_dma_reload', u32, 1),
    ('lt_dma_good', u32, 1),
    ('cur_trans_active', u32, 1),
    ('dr_pci_req', u32, 1),
    ('dr_pci_word_swap', u32, 1),
    ('dr_pci_byte_swap', u32, 1),
    ('new_slow_core_clk_mode', u32, 1),
    ('rbd_non_mbuf', u32, 1),
    ('rfst_bd_mbuf', u32, 1),
    ('rlsd_bd_mbuf', u32, 1),
    ('dr_pci_len', u32, 16),
]

# /home/saul/thundergate/include/bdrdma.h: 130
class struct_bdrdma_pcie_dma_rd_req_addr_dbg(Structure):
    pass

struct_bdrdma_pcie_dma_rd_req_addr_dbg.__slots__ = [
    'dr_pci_ad_hi',
    'dr_pci_ad_lo',
]
struct_bdrdma_pcie_dma_rd_req_addr_dbg._fields_ = [
    ('dr_pci_ad_hi', u32, 16),
    ('dr_pci_ad_lo', u32, 16),
]

# /home/saul/thundergate/include/bdrdma.h: 135
class struct_bdrdma_pcie_dma_req_len_dbg(Structure):
    pass

struct_bdrdma_pcie_dma_req_len_dbg.__slots__ = [
    'reserved16',
    'rdma_len',
]
struct_bdrdma_pcie_dma_req_len_dbg._fields_ = [
    ('reserved16', u32, 16),
    ('rdma_len', u32, 16),
]

# /home/saul/thundergate/include/bdrdma.h: 140
class struct_bdrdma_fifo1_dbg(Structure):
    pass

struct_bdrdma_fifo1_dbg.__slots__ = [
    'reserved9',
    'c_write_addr',
]
struct_bdrdma_fifo1_dbg._fields_ = [
    ('reserved9', u32, 23),
    ('c_write_addr', u32, 9),
]

# /home/saul/thundergate/include/bdrdma.h: 145
class struct_bdrdma_fifo2_dbg(Structure):
    pass

struct_bdrdma_fifo2_dbg.__slots__ = [
    'reserved18',
    'rlctrl_in',
    'c_read_addr',
]
struct_bdrdma_fifo2_dbg._fields_ = [
    ('reserved18', u32, 14),
    ('rlctrl_in', u32, 9),
    ('c_read_addr', u32, 9),
]

# /home/saul/thundergate/include/bdrdma.h: 151
class struct_bdrdma_rsvrd_ctrl(Structure):
    pass

struct_bdrdma_rsvrd_ctrl.__slots__ = [
    'reserved21',
    'sel_fed_en_bd',
    'fifo_high_mark_bd',
    'fifo_low_mark_bd',
    'slow_clock_fix_dis_bd',
    'hw_fix_cq25155_en',
    'reserved0',
]
struct_bdrdma_rsvrd_ctrl._fields_ = [
    ('reserved21', u32, 11),
    ('sel_fed_en_bd', u32, 1),
    ('fifo_high_mark_bd', u32, 8),
    ('fifo_low_mark_bd', u32, 8),
    ('slow_clock_fix_dis_bd', u32, 1),
    ('hw_fix_cq25155_en', u32, 1),
    ('reserved0', u32, 2),
]

# /home/saul/thundergate/include/bdrdma.h: 161
class struct_bdrdma_regs(Structure):
    pass

struct_bdrdma_regs.__slots__ = [
    'mode',
    'status',
    'len_dbg',
    'rstates_dbg',
    'rstate2_dbg',
    'bd_status_dbg',
    'req_ptr_dbg',
    'hold_d_dmad_dbg',
    'len_and_addr_idx_dbg',
    'addr_idx_dbg',
    'pcie_dbg_status',
    'pcie_dma_rd_req_addr_dbg',
    'pcie_dma_req_len_dbg',
    'fifo1_dbg',
    'fifo2_dbg',
    'ofs_3c',
    'ofs_40',
    'ofs_44',
    'ofs_48',
    'ofs_4c',
    'ofs_50',
    'ofs_54',
    'ofs_58',
    'ofs_5c',
    'ofs_60',
    'ofs_64',
    'ofs_68',
    'ofs_6c',
    'bdrdma_reserved_cntrl',
    'bdrdma_flow_reserved_cntrl',
    'bdrdma_corruption_en_ctrl',
    'ofs_7c',
]
struct_bdrdma_regs._fields_ = [
    ('mode', struct_bdrdma_mode),
    ('status', struct_bdrdma_status),
    ('len_dbg', struct_bdrdma_len_dbg),
    ('rstates_dbg', struct_bdrdma_rstates_dbg),
    ('rstate2_dbg', struct_bdrdma_rstate2_dbg),
    ('bd_status_dbg', struct_bdrdma_bd_status_dbg),
    ('req_ptr_dbg', struct_bdrdma_req_ptr_dbg),
    ('hold_d_dmad_dbg', struct_bdrdma_hold_d_dmad_dbg),
    ('len_and_addr_idx_dbg', struct_bdrdma_len_and_addr_idx_dbg),
    ('addr_idx_dbg', struct_bdrdma_addr_idx_dbg),
    ('pcie_dbg_status', struct_bdrdma_pcie_dbg_status),
    ('pcie_dma_rd_req_addr_dbg', struct_bdrdma_pcie_dma_rd_req_addr_dbg),
    ('pcie_dma_req_len_dbg', struct_bdrdma_pcie_dma_req_len_dbg),
    ('fifo1_dbg', struct_bdrdma_fifo1_dbg),
    ('fifo2_dbg', struct_bdrdma_fifo2_dbg),
    ('ofs_3c', u32),
    ('ofs_40', u32),
    ('ofs_44', u32),
    ('ofs_48', u32),
    ('ofs_4c', u32),
    ('ofs_50', u32),
    ('ofs_54', u32),
    ('ofs_58', u32),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('ofs_6c', u32),
    ('bdrdma_reserved_cntrl', u32),
    ('bdrdma_flow_reserved_cntrl', u32),
    ('bdrdma_corruption_en_ctrl', u32),
    ('ofs_7c', u32),
]

# /home/saul/thundergate/include/bufman.h: 22
class struct_bufman_mode(Structure):
    pass

# /home/saul/thundergate/include/bufman.h: 38
class struct_bufman_status(Structure):
    pass

struct_bufman_status.__slots__ = [
    'test_mode',
    'mbuf_low_attention',
    'reserved',
    'error',
    'reserved2',
]
struct_bufman_status._fields_ = [
    ('test_mode', u32, 27),
    ('mbuf_low_attention', u32, 1),
    ('reserved', u32, 1),
    ('error', u32, 1),
    ('reserved2', u32, 2),
]

# /home/saul/thundergate/include/bufman.h: 46
class struct_bufman_mbuf_pool_bar(Structure):
    pass

struct_bufman_mbuf_pool_bar.__slots__ = [
    'reserved',
    'mbuf_base_addr',
]
struct_bufman_mbuf_pool_bar._fields_ = [
    ('reserved', u32, 9),
    ('mbuf_base_addr', u32, 23),
]

# /home/saul/thundergate/include/bufman.h: 51
class struct_bufman_mbuf_pool_length(Structure):
    pass

struct_bufman_mbuf_pool_length.__slots__ = [
    'reserved',
    'mbuf_length',
]
struct_bufman_mbuf_pool_length._fields_ = [
    ('reserved', u32, 9),
    ('mbuf_length', u32, 23),
]

# /home/saul/thundergate/include/bufman.h: 56
class struct_bufman_rdma_mbuf_low_watermark(Structure):
    pass

struct_bufman_rdma_mbuf_low_watermark.__slots__ = [
    'reserved',
    'count',
]
struct_bufman_rdma_mbuf_low_watermark._fields_ = [
    ('reserved', u32, 26),
    ('count', u32, 6),
]

# /home/saul/thundergate/include/bufman.h: 61
class struct_bufman_dma_mbuf_low_watermark(Structure):
    pass

struct_bufman_dma_mbuf_low_watermark.__slots__ = [
    'reserved',
    'count',
]
struct_bufman_dma_mbuf_low_watermark._fields_ = [
    ('reserved', u32, 23),
    ('count', u32, 9),
]

# /home/saul/thundergate/include/bufman.h: 66
class struct_bufman_mbuf_high_watermark(Structure):
    pass

struct_bufman_mbuf_high_watermark.__slots__ = [
    'reserved',
    'count',
]
struct_bufman_mbuf_high_watermark._fields_ = [
    ('reserved', u32, 23),
    ('count', u32, 9),
]

# /home/saul/thundergate/include/bufman.h: 71
class struct_bufman_risc_mbuf_cluster_allocation_request(Structure):
    pass

struct_bufman_risc_mbuf_cluster_allocation_request.__slots__ = [
    'allocation_request',
    'reserved',
]
struct_bufman_risc_mbuf_cluster_allocation_request._fields_ = [
    ('allocation_request', u32, 1),
    ('reserved', u32, 31),
]

# /home/saul/thundergate/include/bufman.h: 76
class struct_bufman_risc_mbuf_cluster_allocation_response(Structure):
    pass

struct_bufman_risc_mbuf_cluster_allocation_response.__slots__ = [
    'mbuf',
]
struct_bufman_risc_mbuf_cluster_allocation_response._fields_ = [
    ('mbuf', u32),
]

# /home/saul/thundergate/include/bufman.h: 80
class struct_bufman_hardware_diagnostic_1(Structure):
    pass

struct_bufman_hardware_diagnostic_1.__slots__ = [
    'reserved',
    'last_txmbuf_deallocation_head_ptr',
    'reserved2',
    'last_txmbuf_deallocation_tail_ptr',
    'reserved3',
    'next_txmbuf_allocation_ptr',
]
struct_bufman_hardware_diagnostic_1._fields_ = [
    ('reserved', u32, 6),
    ('last_txmbuf_deallocation_head_ptr', u32, 6),
    ('reserved2', u32, 4),
    ('last_txmbuf_deallocation_tail_ptr', u32, 6),
    ('reserved3', u32, 4),
    ('next_txmbuf_allocation_ptr', u32, 6),
]

# /home/saul/thundergate/include/bufman.h: 89
class struct_bufman_hardware_diagnostic_2(Structure):
    pass

struct_bufman_hardware_diagnostic_2.__slots__ = [
    'reserved',
    'rxmbuf_count',
    'reserved2',
    'txmbuf_count',
    'rxmbuf_left',
]
struct_bufman_hardware_diagnostic_2._fields_ = [
    ('reserved', u32, 7),
    ('rxmbuf_count', u32, 9),
    ('reserved2', u32, 1),
    ('txmbuf_count', u32, 6),
    ('rxmbuf_left', u32, 9),
]

# /home/saul/thundergate/include/bufman.h: 97
class struct_bufman_hardware_diagnostic_3(Structure):
    pass

struct_bufman_hardware_diagnostic_3.__slots__ = [
    'reserved',
    'next_rxmbuf_deallocation_ptr',
    'reserved2',
    'next_rxmbuf_allocation_ptr',
]
struct_bufman_hardware_diagnostic_3._fields_ = [
    ('reserved', u32, 7),
    ('next_rxmbuf_deallocation_ptr', u32, 9),
    ('reserved2', u32, 7),
    ('next_rxmbuf_allocation_ptr', u32, 9),
]

# /home/saul/thundergate/include/bufman.h: 104
class struct_bufman_receive_flow_threshold(Structure):
    pass

struct_bufman_receive_flow_threshold.__slots__ = [
    'reserved',
    'mbuf_threshold',
]
struct_bufman_receive_flow_threshold._fields_ = [
    ('reserved', u32, 23),
    ('mbuf_threshold', u32, 9),
]

# /home/saul/thundergate/include/bufman.h: 109
class struct_bufman_regs(Structure):
    pass

struct_bufman_regs.__slots__ = [
    'mode',
    'status',
    'mbuf_pool_base_address',
    'mbuf_pool_length',
    'rdma_mbuf_low_watermark',
    'dma_mbuf_low_watermark',
    'mbuf_high_watermark',
    'rx_risc_mbuf_cluster_allocation_request',
    'rx_risc_mbuf_cluster_allocation_response',
    'tx_risc_mbuf_cluster_allocation_request',
    'tx_risc_mbuf_cluster_allocation_response',
    'dma_desc_pool_addr',
    'dma_desc_pool_size',
    'dma_low_water',
    'dma_high_water',
    'rx_dma_alloc_request',
    'rx_dma_alloc_response',
    'tx_dma_alloc_request',
    'tx_dma_alloc_response',
    'hardware_diagnostic_1',
    'hardware_diagnostic_2',
    'hardware_diagnostic_3',
    'receive_flow_threshold',
]
struct_bufman_regs._fields_ = [
    ('mode', struct_bufman_mode),
    ('status', struct_bufman_status),
    ('mbuf_pool_base_address', struct_bufman_mbuf_pool_bar),
    ('mbuf_pool_length', struct_bufman_mbuf_pool_length),
    ('rdma_mbuf_low_watermark', struct_bufman_rdma_mbuf_low_watermark),
    ('dma_mbuf_low_watermark', struct_bufman_dma_mbuf_low_watermark),
    ('mbuf_high_watermark', struct_bufman_mbuf_high_watermark),
    ('rx_risc_mbuf_cluster_allocation_request', struct_bufman_risc_mbuf_cluster_allocation_request),
    ('rx_risc_mbuf_cluster_allocation_response', struct_bufman_risc_mbuf_cluster_allocation_response),
    ('tx_risc_mbuf_cluster_allocation_request', struct_bufman_risc_mbuf_cluster_allocation_request),
    ('tx_risc_mbuf_cluster_allocation_response', struct_bufman_risc_mbuf_cluster_allocation_response),
    ('dma_desc_pool_addr', u32),
    ('dma_desc_pool_size', u32),
    ('dma_low_water', u32),
    ('dma_high_water', u32),
    ('rx_dma_alloc_request', u32),
    ('rx_dma_alloc_response', u32),
    ('tx_dma_alloc_request', u32),
    ('tx_dma_alloc_response', u32),
    ('hardware_diagnostic_1', struct_bufman_hardware_diagnostic_1),
    ('hardware_diagnostic_2', struct_bufman_hardware_diagnostic_2),
    ('hardware_diagnostic_3', struct_bufman_hardware_diagnostic_3),
    ('receive_flow_threshold', struct_bufman_receive_flow_threshold),
]

# /home/saul/thundergate/include/cfg_port.h: 22
class struct_cfg_port_cap_ctrl(Structure):
    pass

struct_cfg_port_cap_ctrl.__slots__ = [
    'unknown4',
    'pm_en',
    'vpd_en',
    'msi_en',
    'msix_en',
]
struct_cfg_port_cap_ctrl._fields_ = [
    ('unknown4', u32, 28),
    ('pm_en', u32, 1),
    ('vpd_en', u32, 1),
    ('msi_en', u32, 1),
    ('msix_en', u32, 1),
]

# /home/saul/thundergate/include/cfg_port.h: 30
class struct_cfg_port_bar_ctrl(Structure):
    pass

struct_cfg_port_bar_ctrl.__slots__ = [
    'unknown12',
    'rom_bar_sz',
    'unknown4',
    'bar0_64bit',
    'bar0_sz',
]
struct_cfg_port_bar_ctrl._fields_ = [
    ('unknown12', u32, 20),
    ('rom_bar_sz', u32, 4),
    ('unknown4', u32, 3),
    ('bar0_64bit', u32, 1),
    ('bar0_sz', u32, 4),
]

# /home/saul/thundergate/include/cfg_port.h: 38
class struct_cfg_port_pci_id(Structure):
    pass

# /home/saul/thundergate/include/cfg_port.h: 48
class struct_cfg_port_pci_sid(Structure):
    pass

# /home/saul/thundergate/include/cfg_port.h: 58
class struct_cfg_port_pci_class(Structure):
    pass

# /home/saul/thundergate/include/cfg_port.h: 70
class struct_cfg_port_regs(Structure):
    pass

struct_cfg_port_regs.__slots__ = [
    'ofs_00',
    'ofs_04',
    'bar_ctrl',
    'ofs_0c',
    'ofs_10',
    'ofs_14',
    'ofs_18',
    'ofs_1c',
    'ofs_20',
    'ofs_24',
    'ofs_28',
    'ofs_2c',
    'ofs_30',
    'pci_id',
    'pci_sid',
    'pci_class',
    'cap_ctrl',
    'ofs_44',
    'ofs_48',
    'ofs_4c',
    'ofs_50',
    'ofs_54',
    'ofs_58',
    'ofs_5c',
    'ofs_60',
    'ofs_64',
    'ofs_68',
    'ofs_6c',
    'ofs_70',
    'ofs_74',
    'ofs_78',
    'ofs_7c',
    'ofs_80',
    'ofs_84',
    'ofs_88',
    'ofs_8c',
    'ofs_90',
    'ofs_94',
    'ofs_98',
    'ofs_9c',
    'ofs_a0',
    'ofs_a4',
    'ofs_a8',
    'ofs_ac',
    'ofs_b0',
    'ofs_b4',
    'ofs_b8',
    'ofs_bc',
    'ofs_c0',
    'ofs_c4',
    'ofs_c8',
    'ofs_cc',
    'ofs_d0',
    'ofs_d4',
    'ofs_d8',
    'ofs_dc',
    'ofs_e0',
    'ofs_e4',
    'ofs_e8',
    'ofs_ec',
    'ofs_f0',
    'ofs_f4',
    'ofs_f8',
    'ofs_fc',
    'ofs_100',
    'ofs_104',
    'ofs_108',
    'ofs_10c',
    'ofs_110',
    'ofs_114',
    'ofs_118',
    'ofs_11c',
    'ofs_120',
    'ofs_124',
    'ofs_128',
    'ofs_12c',
    'ofs_130',
    'ofs_134',
    'ofs_138',
    'ofs_13c',
    'ofs_140',
    'ofs_144',
    'ofs_148',
    'ofs_14c',
    'ofs_150',
    'ofs_154',
    'ofs_158',
    'ofs_15c',
    'ofs_160',
    'ofs_164',
    'ofs_168',
    'ofs_16c',
    'ofs_170',
    'ofs_174',
    'ofs_178',
    'ofs_17c',
    'ofs_180',
    'ofs_184',
    'ofs_188',
    'ofs_18c',
    'ofs_190',
    'ofs_194',
    'ofs_198',
    'ofs_19c',
    'ofs_1a0',
    'ofs_1a4',
    'ofs_1a8',
    'ofs_1ac',
    'ofs_1b0',
    'ofs_1b4',
    'ofs_1b8',
    'ofs_1bc',
    'ofs_1c0',
    'ofs_1c4',
    'ofs_1c8',
    'ofs_1cc',
    'ofs_1d0',
    'ofs_1d4',
    'ofs_1d8',
    'ofs_1dc',
    'ofs_1e0',
    'ofs_1e4',
    'ofs_1e8',
    'ofs_1ec',
    'ofs_1f0',
    'ofs_1f4',
    'ofs_1f8',
    'ofs_1fc',
    'ofs_200',
    'ofs_204',
    'ofs_208',
    'ofs_20c',
    'ofs_210',
    'ofs_214',
    'ofs_218',
    'ofs_21c',
    'ofs_220',
    'ofs_224',
    'ofs_228',
    'ofs_22c',
    'ofs_230',
    'ofs_234',
    'ofs_238',
    'ofs_23c',
    'ofs_240',
    'ofs_244',
    'ofs_248',
    'ofs_24c',
    'ofs_250',
    'ofs_254',
    'ofs_258',
    'ofs_25c',
    'ofs_260',
    'ofs_264',
    'ofs_268',
    'ofs_26c',
    'ofs_270',
    'ofs_274',
    'ofs_278',
    'ofs_27c',
    'ofs_280',
    'ofs_284',
    'ofs_288',
    'ofs_28c',
    'ofs_290',
    'ofs_294',
    'ofs_298',
    'ofs_29c',
    'ofs_2a0',
    'ofs_2a4',
    'ofs_2a8',
    'ofs_2ac',
    'ofs_2b0',
    'ofs_2b4',
    'ofs_2b8',
    'ofs_2bc',
    'ofs_2c0',
    'ofs_2c4',
    'ofs_2c8',
    'ofs_2cc',
    'ofs_2d0',
    'ofs_2d4',
    'ofs_2d8',
    'ofs_2dc',
    'ofs_2e0',
    'ofs_2e4',
    'ofs_2e8',
    'ofs_2ec',
    'ofs_2f0',
    'ofs_2f4',
    'ofs_2f8',
    'ofs_2fc',
    'ofs_300',
    'ofs_304',
    'ofs_308',
    'ofs_30c',
    'ofs_310',
    'ofs_314',
    'ofs_318',
    'ofs_31c',
    'ofs_320',
    'ofs_324',
    'ofs_328',
    'ofs_32c',
    'ofs_330',
    'ofs_334',
    'ofs_338',
    'ofs_33c',
    'ofs_340',
    'ofs_344',
    'ofs_348',
    'ofs_34c',
    'ofs_350',
    'ofs_354',
    'ofs_358',
    'ofs_35c',
    'ofs_360',
    'ofs_364',
    'ofs_368',
    'ofs_36c',
    'ofs_370',
    'ofs_374',
    'ofs_378',
    'ofs_37c',
    'ofs_380',
    'ofs_384',
    'ofs_388',
    'ofs_38c',
    'ofs_390',
    'ofs_394',
    'ofs_398',
    'ofs_39c',
    'ofs_3a0',
    'ofs_3a4',
    'ofs_3a8',
    'ofs_3ac',
    'ofs_3b0',
    'ofs_3b4',
    'ofs_3b8',
    'ofs_3bc',
    'ofs_3c0',
    'ofs_3c4',
    'ofs_3c8',
    'ofs_3cc',
    'ofs_3d0',
    'ofs_3d4',
    'ofs_3d8',
    'ofs_3dc',
    'ofs_3e0',
    'ofs_3e4',
    'ofs_3e8',
    'ofs_3ec',
    'ofs_3f0',
    'ofs_3f4',
    'ofs_3f8',
    'ofs_3fc',
]
struct_cfg_port_regs._fields_ = [
    ('ofs_00', u32),
    ('ofs_04', u32),
    ('bar_ctrl', struct_cfg_port_bar_ctrl),
    ('ofs_0c', u32),
    ('ofs_10', u32),
    ('ofs_14', u32),
    ('ofs_18', u32),
    ('ofs_1c', u32),
    ('ofs_20', u32),
    ('ofs_24', u32),
    ('ofs_28', u32),
    ('ofs_2c', u32),
    ('ofs_30', u32),
    ('pci_id', struct_cfg_port_pci_id),
    ('pci_sid', struct_cfg_port_pci_sid),
    ('pci_class', struct_cfg_port_pci_class),
    ('cap_ctrl', struct_cfg_port_cap_ctrl),
    ('ofs_44', u32),
    ('ofs_48', u32),
    ('ofs_4c', u32),
    ('ofs_50', u32),
    ('ofs_54', u32),
    ('ofs_58', u32),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('ofs_6c', u32),
    ('ofs_70', u32),
    ('ofs_74', u32),
    ('ofs_78', u32),
    ('ofs_7c', u32),
    ('ofs_80', u32),
    ('ofs_84', u32),
    ('ofs_88', u32),
    ('ofs_8c', u32),
    ('ofs_90', u32),
    ('ofs_94', u32),
    ('ofs_98', u32),
    ('ofs_9c', u32),
    ('ofs_a0', u32),
    ('ofs_a4', u32),
    ('ofs_a8', u32),
    ('ofs_ac', u32),
    ('ofs_b0', u32),
    ('ofs_b4', u32),
    ('ofs_b8', u32),
    ('ofs_bc', u32),
    ('ofs_c0', u32),
    ('ofs_c4', u32),
    ('ofs_c8', u32),
    ('ofs_cc', u32),
    ('ofs_d0', u32),
    ('ofs_d4', u32),
    ('ofs_d8', u32),
    ('ofs_dc', u32),
    ('ofs_e0', u32),
    ('ofs_e4', u32),
    ('ofs_e8', u32),
    ('ofs_ec', u32),
    ('ofs_f0', u32),
    ('ofs_f4', u32),
    ('ofs_f8', u32),
    ('ofs_fc', u32),
    ('ofs_100', u32),
    ('ofs_104', u32),
    ('ofs_108', u32),
    ('ofs_10c', u32),
    ('ofs_110', u32),
    ('ofs_114', u32),
    ('ofs_118', u32),
    ('ofs_11c', u32),
    ('ofs_120', u32),
    ('ofs_124', u32),
    ('ofs_128', u32),
    ('ofs_12c', u32),
    ('ofs_130', u32),
    ('ofs_134', u32),
    ('ofs_138', u32),
    ('ofs_13c', u32),
    ('ofs_140', u32),
    ('ofs_144', u32),
    ('ofs_148', u32),
    ('ofs_14c', u32),
    ('ofs_150', u32),
    ('ofs_154', u32),
    ('ofs_158', u32),
    ('ofs_15c', u32),
    ('ofs_160', u32),
    ('ofs_164', u32),
    ('ofs_168', u32),
    ('ofs_16c', u32),
    ('ofs_170', u32),
    ('ofs_174', u32),
    ('ofs_178', u32),
    ('ofs_17c', u32),
    ('ofs_180', u32),
    ('ofs_184', u32),
    ('ofs_188', u32),
    ('ofs_18c', u32),
    ('ofs_190', u32),
    ('ofs_194', u32),
    ('ofs_198', u32),
    ('ofs_19c', u32),
    ('ofs_1a0', u32),
    ('ofs_1a4', u32),
    ('ofs_1a8', u32),
    ('ofs_1ac', u32),
    ('ofs_1b0', u32),
    ('ofs_1b4', u32),
    ('ofs_1b8', u32),
    ('ofs_1bc', u32),
    ('ofs_1c0', u32),
    ('ofs_1c4', u32),
    ('ofs_1c8', u32),
    ('ofs_1cc', u32),
    ('ofs_1d0', u32),
    ('ofs_1d4', u32),
    ('ofs_1d8', u32),
    ('ofs_1dc', u32),
    ('ofs_1e0', u32),
    ('ofs_1e4', u32),
    ('ofs_1e8', u32),
    ('ofs_1ec', u32),
    ('ofs_1f0', u32),
    ('ofs_1f4', u32),
    ('ofs_1f8', u32),
    ('ofs_1fc', u32),
    ('ofs_200', u32),
    ('ofs_204', u32),
    ('ofs_208', u32),
    ('ofs_20c', u32),
    ('ofs_210', u32),
    ('ofs_214', u32),
    ('ofs_218', u32),
    ('ofs_21c', u32),
    ('ofs_220', u32),
    ('ofs_224', u32),
    ('ofs_228', u32),
    ('ofs_22c', u32),
    ('ofs_230', u32),
    ('ofs_234', u32),
    ('ofs_238', u32),
    ('ofs_23c', u32),
    ('ofs_240', u32),
    ('ofs_244', u32),
    ('ofs_248', u32),
    ('ofs_24c', u32),
    ('ofs_250', u32),
    ('ofs_254', u32),
    ('ofs_258', u32),
    ('ofs_25c', u32),
    ('ofs_260', u32),
    ('ofs_264', u32),
    ('ofs_268', u32),
    ('ofs_26c', u32),
    ('ofs_270', u32),
    ('ofs_274', u32),
    ('ofs_278', u32),
    ('ofs_27c', u32),
    ('ofs_280', u32),
    ('ofs_284', u32),
    ('ofs_288', u32),
    ('ofs_28c', u32),
    ('ofs_290', u32),
    ('ofs_294', u32),
    ('ofs_298', u32),
    ('ofs_29c', u32),
    ('ofs_2a0', u32),
    ('ofs_2a4', u32),
    ('ofs_2a8', u32),
    ('ofs_2ac', u32),
    ('ofs_2b0', u32),
    ('ofs_2b4', u32),
    ('ofs_2b8', u32),
    ('ofs_2bc', u32),
    ('ofs_2c0', u32),
    ('ofs_2c4', u32),
    ('ofs_2c8', u32),
    ('ofs_2cc', u32),
    ('ofs_2d0', u32),
    ('ofs_2d4', u32),
    ('ofs_2d8', u32),
    ('ofs_2dc', u32),
    ('ofs_2e0', u32),
    ('ofs_2e4', u32),
    ('ofs_2e8', u32),
    ('ofs_2ec', u32),
    ('ofs_2f0', u32),
    ('ofs_2f4', u32),
    ('ofs_2f8', u32),
    ('ofs_2fc', u32),
    ('ofs_300', u32),
    ('ofs_304', u32),
    ('ofs_308', u32),
    ('ofs_30c', u32),
    ('ofs_310', u32),
    ('ofs_314', u32),
    ('ofs_318', u32),
    ('ofs_31c', u32),
    ('ofs_320', u32),
    ('ofs_324', u32),
    ('ofs_328', u32),
    ('ofs_32c', u32),
    ('ofs_330', u32),
    ('ofs_334', u32),
    ('ofs_338', u32),
    ('ofs_33c', u32),
    ('ofs_340', u32),
    ('ofs_344', u32),
    ('ofs_348', u32),
    ('ofs_34c', u32),
    ('ofs_350', u32),
    ('ofs_354', u32),
    ('ofs_358', u32),
    ('ofs_35c', u32),
    ('ofs_360', u32),
    ('ofs_364', u32),
    ('ofs_368', u32),
    ('ofs_36c', u32),
    ('ofs_370', u32),
    ('ofs_374', u32),
    ('ofs_378', u32),
    ('ofs_37c', u32),
    ('ofs_380', u32),
    ('ofs_384', u32),
    ('ofs_388', u32),
    ('ofs_38c', u32),
    ('ofs_390', u32),
    ('ofs_394', u32),
    ('ofs_398', u32),
    ('ofs_39c', u32),
    ('ofs_3a0', u32),
    ('ofs_3a4', u32),
    ('ofs_3a8', u32),
    ('ofs_3ac', u32),
    ('ofs_3b0', u32),
    ('ofs_3b4', u32),
    ('ofs_3b8', u32),
    ('ofs_3bc', u32),
    ('ofs_3c0', u32),
    ('ofs_3c4', u32),
    ('ofs_3c8', u32),
    ('ofs_3cc', u32),
    ('ofs_3d0', u32),
    ('ofs_3d4', u32),
    ('ofs_3d8', u32),
    ('ofs_3dc', u32),
    ('ofs_3e0', u32),
    ('ofs_3e4', u32),
    ('ofs_3e8', u32),
    ('ofs_3ec', u32),
    ('ofs_3f0', u32),
    ('ofs_3f4', u32),
    ('ofs_3f8', u32),
    ('ofs_3fc', u32),
]

# /home/saul/thundergate/include/cpmu.h: 22
class struct_cpmu_control(Structure):
    pass

struct_cpmu_control.__slots__ = [
    'reserved31',
    'reserved30',
    'reserved29',
    'always_force_gphy_dll_on',
    'enable_gphy_powerdown_in_dou',
    'reserved26',
    'reserved25',
    'reserved24',
    'reserved23',
    'sw_ctrl_ape_reset',
    'sw_ctrl_core_reset',
    'media_sense_power_mode_enable',
    'reserved19',
    'legacy_timer_enable',
    'frequency_multiplier_enable',
    'gphy_10mb_receive_only_mode_enable',
    'play_dead_mode_enable',
    'link_speed_power_mode_enable',
    'hide_pcie_function',
    'link_aware_power_mode_enable',
    'link_idle_power_mode_enable',
    'card_reader_idle_enable',
    'card_read_iddq',
    'lan_iddq',
    'ape_deep_sleep_mode_en',
    'ape_sleep_mode_en',
    'reserved3',
    'power_down',
    'register_software_reset',
    'software_reset',
]
struct_cpmu_control._fields_ = [
    ('reserved31', u32, 1),
    ('reserved30', u32, 1),
    ('reserved29', u32, 1),
    ('always_force_gphy_dll_on', u32, 1),
    ('enable_gphy_powerdown_in_dou', u32, 1),
    ('reserved26', u32, 1),
    ('reserved25', u32, 1),
    ('reserved24', u32, 1),
    ('reserved23', u32, 1),
    ('sw_ctrl_ape_reset', u32, 1),
    ('sw_ctrl_core_reset', u32, 1),
    ('media_sense_power_mode_enable', u32, 1),
    ('reserved19', u32, 1),
    ('legacy_timer_enable', u32, 1),
    ('frequency_multiplier_enable', u32, 1),
    ('gphy_10mb_receive_only_mode_enable', u32, 1),
    ('play_dead_mode_enable', u32, 1),
    ('link_speed_power_mode_enable', u32, 1),
    ('hide_pcie_function', u32, 3),
    ('link_aware_power_mode_enable', u32, 1),
    ('link_idle_power_mode_enable', u32, 1),
    ('card_reader_idle_enable', u32, 1),
    ('card_read_iddq', u32, 1),
    ('lan_iddq', u32, 1),
    ('ape_deep_sleep_mode_en', u32, 1),
    ('ape_sleep_mode_en', u32, 1),
    ('reserved3', u32, 1),
    ('power_down', u32, 1),
    ('register_software_reset', u32, 1),
    ('software_reset', u32, 1),
]

# /home/saul/thundergate/include/cpmu.h: 55
class struct_cpmu_clock(Structure):
    pass

struct_cpmu_clock.__slots__ = [
    'reserved21',
    'mac_clock_switch',
    'reserved13',
    'ape_clock_switch',
    'reserved0',
]
struct_cpmu_clock._fields_ = [
    ('reserved21', u32, 11),
    ('mac_clock_switch', u32, 5),
    ('reserved13', u32, 3),
    ('ape_clock_switch', u32, 5),
    ('reserved0', u32, 8),
]

# /home/saul/thundergate/include/cpmu.h: 63
class struct_cpmu_override(Structure):
    pass

struct_cpmu_override.__slots__ = [
    'reserved',
    'mac_clock_speed_override_enable',
    'reserved2',
]
struct_cpmu_override._fields_ = [
    ('reserved', u32, 18),
    ('mac_clock_speed_override_enable', u32, 1),
    ('reserved2', u32, 13),
]

# /home/saul/thundergate/include/cpmu.h: 69
class struct_cpmu_status(Structure):
    pass

struct_cpmu_status.__slots__ = [
    'reserved',
    'wol_acpi_detection_enabled',
    'wol_magic_packet_detection_enabled',
    'ethernet_link',
    'link_idle',
    'reserved2',
    'reserved3',
    'vmain_power',
    'iddq',
    'power_state',
    'energy_detect',
    'cpmu_power',
    'pm_state_machine_state',
]
struct_cpmu_status._fields_ = [
    ('reserved', u32, 9),
    ('wol_acpi_detection_enabled', u32, 1),
    ('wol_magic_packet_detection_enabled', u32, 1),
    ('ethernet_link', u32, 2),
    ('link_idle', u32, 1),
    ('reserved2', u32, 2),
    ('reserved3', u32, 2),
    ('vmain_power', u32, 1),
    ('iddq', u32, 3),
    ('power_state', u32, 2),
    ('energy_detect', u32, 1),
    ('cpmu_power', u32, 3),
    ('pm_state_machine_state', u32, 4),
]

# /home/saul/thundergate/include/cpmu.h: 85
class struct_cpmu_clock_status(Structure):
    pass

struct_cpmu_clock_status.__slots__ = [
    'reserved30',
    'flash_clk_dis',
    'reserved26',
    'ape_hclk_dis',
    'ape_fclk_dis',
    'reserved21',
    'mac_clk_sw',
    'reserved13',
    'ape_clk_sw',
    'reserved7',
    'flash_clk_sw',
    'reserved0',
]
struct_cpmu_clock_status._fields_ = [
    ('reserved30', u32, 2),
    ('flash_clk_dis', u32, 1),
    ('reserved26', u32, 3),
    ('ape_hclk_dis', u32, 1),
    ('ape_fclk_dis', u32, 1),
    ('reserved21', u32, 3),
    ('mac_clk_sw', u32, 5),
    ('reserved13', u32, 3),
    ('ape_clk_sw', u32, 5),
    ('reserved7', u32, 1),
    ('flash_clk_sw', u32, 3),
    ('reserved0', u32, 4),
]

# /home/saul/thundergate/include/cpmu.h: 100
class struct_cpmu_pcie_status(Structure):
    pass

struct_cpmu_pcie_status.__slots__ = [
    'dl_active',
    'debug_vector_sel_2',
    'debug_vector_2',
    'phylinkup',
    'debug_vector_sel_1',
    'debug_vector_1',
]
struct_cpmu_pcie_status._fields_ = [
    ('dl_active', u32, 1),
    ('debug_vector_sel_2', u32, 4),
    ('debug_vector_2', u32, 11),
    ('phylinkup', u32, 1),
    ('debug_vector_sel_1', u32, 4),
    ('debug_vector_1', u32, 11),
]

# /home/saul/thundergate/include/cpmu.h: 109
class struct_cpmu_gphy_control_status(Structure):
    pass

struct_cpmu_gphy_control_status.__slots__ = [
    'logan_sku',
    'reserved14',
    'gphy_10mb_rcv_only_mode_tx_idle_debounce_timer',
    'reserved11',
    'dll_iddq_state',
    'pwrdn',
    'set_bias_iddq',
    'force_dll_on',
    'dll_pwrdn_ok',
    'sw_ctrl_por',
    'reset_ctrl',
    'reserved3',
    'dll_handshaking_disable',
    'bias_iddq',
    'phy_iddq',
]
struct_cpmu_gphy_control_status._fields_ = [
    ('logan_sku', u32, 3),
    ('reserved14', u32, 15),
    ('gphy_10mb_rcv_only_mode_tx_idle_debounce_timer', u32, 2),
    ('reserved11', u32, 1),
    ('dll_iddq_state', u32, 1),
    ('pwrdn', u32, 1),
    ('set_bias_iddq', u32, 1),
    ('force_dll_on', u32, 1),
    ('dll_pwrdn_ok', u32, 1),
    ('sw_ctrl_por', u32, 1),
    ('reset_ctrl', u32, 1),
    ('reserved3', u32, 1),
    ('dll_handshaking_disable', u32, 1),
    ('bias_iddq', u32, 1),
    ('phy_iddq', u32, 1),
]

# /home/saul/thundergate/include/cpmu.h: 127
class struct_cpmu_ram_control(Structure):
    pass

struct_cpmu_ram_control.__slots__ = [
    'core_ram_power_down',
    'bd_ram_power_down',
    'reserved22',
    'disable_secure_fw_loading_status',
    'remove_lan_function',
    'reserved18',
    'hide_function_7',
    'hide_function_6',
    'hide_function_5',
    'hide_function_4',
    'hide_function_3',
    'hide_function_2',
    'hide_function_1',
    'hide_function_0',
    'reserved8',
    'ram_bank7_dis',
    'ram_bank6_dis',
    'ram_bank5_dis',
    'ram_bank4_dis',
    'ram_bank3_dis',
    'ram_bank2_dis',
    'ram_bank1_dis',
    'ram_bank0_dis',
]
struct_cpmu_ram_control._fields_ = [
    ('core_ram_power_down', u32, 1),
    ('bd_ram_power_down', u32, 1),
    ('reserved22', u32, 8),
    ('disable_secure_fw_loading_status', u32, 1),
    ('remove_lan_function', u32, 1),
    ('reserved18', u32, 2),
    ('hide_function_7', u32, 1),
    ('hide_function_6', u32, 1),
    ('hide_function_5', u32, 1),
    ('hide_function_4', u32, 1),
    ('hide_function_3', u32, 1),
    ('hide_function_2', u32, 1),
    ('hide_function_1', u32, 1),
    ('hide_function_0', u32, 1),
    ('reserved8', u32, 2),
    ('ram_bank7_dis', u32, 1),
    ('ram_bank6_dis', u32, 1),
    ('ram_bank5_dis', u32, 1),
    ('ram_bank4_dis', u32, 1),
    ('ram_bank3_dis', u32, 1),
    ('ram_bank2_dis', u32, 1),
    ('ram_bank1_dis', u32, 1),
    ('ram_bank0_dis', u32, 1),
]

# /home/saul/thundergate/include/cpmu.h: 153
class struct_cpmu_cr_idle_det_debounce_ctrl(Structure):
    pass

struct_cpmu_cr_idle_det_debounce_ctrl.__slots__ = [
    'reserved16',
    'timer',
]
struct_cpmu_cr_idle_det_debounce_ctrl._fields_ = [
    ('reserved16', u32, 16),
    ('timer', u32, 16),
]

# /home/saul/thundergate/include/cpmu.h: 158
class struct_cpmu_core_idle_det_debounce_ctrl(Structure):
    pass

struct_cpmu_core_idle_det_debounce_ctrl.__slots__ = [
    'reserved8',
    'timer',
]
struct_cpmu_core_idle_det_debounce_ctrl._fields_ = [
    ('reserved8', u32, 24),
    ('timer', u32, 8),
]

# /home/saul/thundergate/include/cpmu.h: 163
class struct_cpmu_pcie_idle_det_debounce_ctrl(Structure):
    pass

struct_cpmu_pcie_idle_det_debounce_ctrl.__slots__ = [
    'reserved8',
    'timer',
]
struct_cpmu_pcie_idle_det_debounce_ctrl._fields_ = [
    ('reserved8', u32, 24),
    ('timer', u32, 8),
]

# /home/saul/thundergate/include/cpmu.h: 168
class struct_cpmu_energy_det_debounce_ctrl(Structure):
    pass

struct_cpmu_energy_det_debounce_ctrl.__slots__ = [
    'reserved10',
    'energy_detect_select',
    'select_hw_energy_det',
    'select_sw_hw_oring_energy_det',
    'sw_force_energy_det_value',
    'disable_energy_det_debounce_low',
    'disable_energy_det_debounce_high',
    'energy_det_debounce_high_limit',
    'energy_det_debounce_low_limit',
]
struct_cpmu_energy_det_debounce_ctrl._fields_ = [
    ('reserved10', u32, 22),
    ('energy_detect_select', u32, 1),
    ('select_hw_energy_det', u32, 1),
    ('select_sw_hw_oring_energy_det', u32, 1),
    ('sw_force_energy_det_value', u32, 1),
    ('disable_energy_det_debounce_low', u32, 1),
    ('disable_energy_det_debounce_high', u32, 1),
    ('energy_det_debounce_high_limit', u32, 2),
    ('energy_det_debounce_low_limit', u32, 2),
]

# /home/saul/thundergate/include/cpmu.h: 180
class struct_cpmu_dll_lock_timer(Structure):
    pass

struct_cpmu_dll_lock_timer.__slots__ = [
    'reserved12',
    'gphy_dll_lock_dimer_enable',
    'gphy_dll_lock_timer',
]
struct_cpmu_dll_lock_timer._fields_ = [
    ('reserved12', u32, 20),
    ('gphy_dll_lock_dimer_enable', u32, 1),
    ('gphy_dll_lock_timer', u32, 11),
]

# /home/saul/thundergate/include/cpmu.h: 186
class struct_cpmu_chip_id(Structure):
    pass

struct_cpmu_chip_id.__slots__ = [
    'chip_id_hi',
    'chip_id_lo',
    'base_layer_revision',
    'metal_layer_revision',
]
struct_cpmu_chip_id._fields_ = [
    ('chip_id_hi', u32, 4),
    ('chip_id_lo', u32, 16),
    ('base_layer_revision', u32, 4),
    ('metal_layer_revision', u32, 8),
]

# /home/saul/thundergate/include/cpmu.h: 193
class struct_cpmu_mutex(Structure):
    pass

struct_cpmu_mutex.__slots__ = [
    'reserved13',
    'req_12',
    'reserved9',
    'req_8',
    'reserved5',
    'req_4',
    'reserved3',
    'req_2',
    'reserved0',
]
struct_cpmu_mutex._fields_ = [
    ('reserved13', u32, 19),
    ('req_12', u32, 1),
    ('reserved9', u32, 3),
    ('req_8', u32, 1),
    ('reserved5', u32, 3),
    ('req_4', u32, 1),
    ('reserved3', u32, 1),
    ('req_2', u32, 1),
    ('reserved0', u32, 2),
]

# /home/saul/thundergate/include/cpmu.h: 205
class struct_cpmu_padring_control(Structure):
    pass

struct_cpmu_padring_control.__slots__ = [
    'power_sm_or_state',
    'power_sm_override',
    'cr_io_hys_en',
    'cr_activity_led_en',
    'switching_regulator_power_off_option',
    'cr_bus_power_dis',
    'unknown',
    'pcie_serdes_pll_tuning_bypass',
    'pcie_serdes_lfck_rx_select_cnt0',
    'pcie_serdes_lfck_rx_select_refclk',
    'reserved',
    'clkreq_l_in_low_power_mode_improvement',
    'cq31984_opt_2_fix_disable',
    'serdes_standalone_mode',
    'pipe_standalone_mode_control',
    'cq31984_opt_4_fix_enable',
    'cq31177_fix_disable',
    'cq30674_fix_enable',
    'chicken_bit_for_cq31116',
    'cq31984_opt_3_fix_disable',
    'disable_default_gigabit_advertisement',
    'enable_gphy_reset_on_perst_l_deassertion',
    'cq39842_fix_disable',
    'cq39544_fix_disable',
    'reserved2',
    'eclk_switch_using_link_status_disable',
    'perst_l_pad_hysteris_enable',
]
struct_cpmu_padring_control._fields_ = [
    ('power_sm_or_state', u32, 4),
    ('power_sm_override', u32, 1),
    ('cr_io_hys_en', u32, 1),
    ('cr_activity_led_en', u32, 1),
    ('switching_regulator_power_off_option', u32, 1),
    ('cr_bus_power_dis', u32, 1),
    ('unknown', u32, 3),
    ('pcie_serdes_pll_tuning_bypass', u32, 1),
    ('pcie_serdes_lfck_rx_select_cnt0', u32, 1),
    ('pcie_serdes_lfck_rx_select_refclk', u32, 1),
    ('reserved', u32, 1),
    ('clkreq_l_in_low_power_mode_improvement', u32, 1),
    ('cq31984_opt_2_fix_disable', u32, 1),
    ('serdes_standalone_mode', u32, 1),
    ('pipe_standalone_mode_control', u32, 1),
    ('cq31984_opt_4_fix_enable', u32, 1),
    ('cq31177_fix_disable', u32, 1),
    ('cq30674_fix_enable', u32, 1),
    ('chicken_bit_for_cq31116', u32, 1),
    ('cq31984_opt_3_fix_disable', u32, 1),
    ('disable_default_gigabit_advertisement', u32, 1),
    ('enable_gphy_reset_on_perst_l_deassertion', u32, 1),
    ('cq39842_fix_disable', u32, 1),
    ('cq39544_fix_disable', u32, 1),
    ('reserved2', u32, 1),
    ('eclk_switch_using_link_status_disable', u32, 1),
    ('perst_l_pad_hysteris_enable', u32, 1),
]

# /home/saul/thundergate/include/cpmu.h: 237
class struct_cpmu_regs(Structure):
    pass

struct_cpmu_regs.__slots__ = [
    'control',
    'no_link_or_10mb_policy',
    'megabit_policy',
    'gigabit_policy',
    'link_aware_policy',
    'd0u_policy',
    'link_idle_policy',
    'ofs_1c',
    'ofs_20',
    'override_policy',
    'override_enable',
    'status',
    'clock_status',
    'pcie_status',
    'gphy_control_status',
    'ram_control',
    'cr_idle_detect_debounce_ctrl',
    'eee_debug',
    'core_idle_detect_debounce_ctrl',
    'pcie_idle_detect_debounce_ctrl',
    'energy_detect_debounce_timer',
    'dll_lock_timer',
    'chip_id',
    'mutex_request',
    'mutex_grant',
    'ofs_64',
    'padring_control',
    'ofs_6c',
    'link_idle_control',
    'link_idle_status',
    'play_dead_mode_iddq_debounce_control',
    'top_misc_control_1',
    'debug_bus',
    'debug_select',
    'ofs_88',
    'ofs_8c',
    'ltr_control',
    'ofs_94',
    'ofs_98',
    'ofs_9c',
    'swregulator_control_1',
    'swregulator_control_2',
    'swregulator_control_3',
    'misc_control',
    'eee_mode',
    'eee_debounce_timer1_control',
    'eee_debounce_timer2_control',
    'eee_link_idle_control',
    'eee_link_idle_status',
    'eee_statistic_counter_1',
    'eee_statistic_counter_2',
    'eee_statistic_counter_3',
    'eee_control',
    'current_measurement_control',
    'current_measurement_read_upper',
    'current_measurement_read_lower',
    'card_reader_idle_control',
    'card_reader_clock_policy',
    'card_reader_clock_status',
    'ofs_ec',
    'pll_control_1',
    'pll_control_2',
    'pll_control_3',
    'clock_gen_control',
]
struct_cpmu_regs._fields_ = [
    ('control', struct_cpmu_control),
    ('no_link_or_10mb_policy', struct_cpmu_clock),
    ('megabit_policy', struct_cpmu_clock),
    ('gigabit_policy', struct_cpmu_clock),
    ('link_aware_policy', struct_cpmu_clock),
    ('d0u_policy', struct_cpmu_clock),
    ('link_idle_policy', struct_cpmu_clock),
    ('ofs_1c', u32),
    ('ofs_20', u32),
    ('override_policy', struct_cpmu_clock),
    ('override_enable', struct_cpmu_override),
    ('status', struct_cpmu_status),
    ('clock_status', struct_cpmu_clock_status),
    ('pcie_status', struct_cpmu_pcie_status),
    ('gphy_control_status', struct_cpmu_gphy_control_status),
    ('ram_control', struct_cpmu_ram_control),
    ('cr_idle_detect_debounce_ctrl', struct_cpmu_cr_idle_det_debounce_ctrl),
    ('eee_debug', u32),
    ('core_idle_detect_debounce_ctrl', struct_cpmu_core_idle_det_debounce_ctrl),
    ('pcie_idle_detect_debounce_ctrl', struct_cpmu_pcie_idle_det_debounce_ctrl),
    ('energy_detect_debounce_timer', struct_cpmu_energy_det_debounce_ctrl),
    ('dll_lock_timer', struct_cpmu_dll_lock_timer),
    ('chip_id', struct_cpmu_chip_id),
    ('mutex_request', struct_cpmu_mutex),
    ('mutex_grant', struct_cpmu_mutex),
    ('ofs_64', u32),
    ('padring_control', struct_cpmu_padring_control),
    ('ofs_6c', u32),
    ('link_idle_control', u32),
    ('link_idle_status', u32),
    ('play_dead_mode_iddq_debounce_control', u32),
    ('top_misc_control_1', u32),
    ('debug_bus', u32),
    ('debug_select', u32),
    ('ofs_88', u32),
    ('ofs_8c', u32),
    ('ltr_control', u32),
    ('ofs_94', u32),
    ('ofs_98', u32),
    ('ofs_9c', u32),
    ('swregulator_control_1', u32),
    ('swregulator_control_2', u32),
    ('swregulator_control_3', u32),
    ('misc_control', u32),
    ('eee_mode', u32),
    ('eee_debounce_timer1_control', u32),
    ('eee_debounce_timer2_control', u32),
    ('eee_link_idle_control', u32),
    ('eee_link_idle_status', u32),
    ('eee_statistic_counter_1', u32),
    ('eee_statistic_counter_2', u32),
    ('eee_statistic_counter_3', u32),
    ('eee_control', u32),
    ('current_measurement_control', u32),
    ('current_measurement_read_upper', u32),
    ('current_measurement_read_lower', u32),
    ('card_reader_idle_control', u32),
    ('card_reader_clock_policy', u32),
    ('card_reader_clock_status', u32),
    ('ofs_ec', u32),
    ('pll_control_1', u32),
    ('pll_control_2', u32),
    ('pll_control_3', u32),
    ('clock_gen_control', u32),
]

# /home/saul/thundergate/include/cpu.h: 22
class struct_cpu_mode(Structure):
    pass

struct_cpu_mode.__slots__ = [
    'reserved15',
    'register_addr_trap_halt_en',
    'memory_addr_trap_halt_en',
    'invalid_instruction_fetch_halt_en',
    'invalid_data_access_halt_en',
    'halt',
    'flush_icache',
    'icache_pref_en',
    'watchdog_en',
    'rom_fail',
    'data_cache_en',
    'write_post_en',
    'page_0_instr_halt_en',
    'page_0_data_halt_en',
    'single_step',
    'reset',
]
struct_cpu_mode._fields_ = [
    ('reserved15', u32, 17),
    ('register_addr_trap_halt_en', u32, 1),
    ('memory_addr_trap_halt_en', u32, 1),
    ('invalid_instruction_fetch_halt_en', u32, 1),
    ('invalid_data_access_halt_en', u32, 1),
    ('halt', u32, 1),
    ('flush_icache', u32, 1),
    ('icache_pref_en', u32, 1),
    ('watchdog_en', u32, 1),
    ('rom_fail', u32, 1),
    ('data_cache_en', u32, 1),
    ('write_post_en', u32, 1),
    ('page_0_instr_halt_en', u32, 1),
    ('page_0_data_halt_en', u32, 1),
    ('single_step', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/cpu.h: 44
class struct_cpu_status(Structure):
    pass

# /home/saul/thundergate/include/cpu.h: 74
class struct_cpu_event_mask(Structure):
    pass

struct_cpu_event_mask.__slots__ = [
    'unknown',
    'reserved13',
    'interrupt',
    'spad_underflow',
    'soft_halted',
    'reserved9',
    'fio_abort',
    'align_halted',
    'bad_pc_halted',
    'bad_data_addr_halted',
    'page_0_instr_halted',
    'page_0_data_halted',
    'bad_instr_halted',
    'reserved1',
    'breakpoint',
]
struct_cpu_event_mask._fields_ = [
    ('unknown', u32, 18),
    ('reserved13', u32, 1),
    ('interrupt', u32, 1),
    ('spad_underflow', u32, 1),
    ('soft_halted', u32, 1),
    ('reserved9', u32, 1),
    ('fio_abort', u32, 1),
    ('align_halted', u32, 1),
    ('bad_pc_halted', u32, 1),
    ('bad_data_addr_halted', u32, 1),
    ('page_0_instr_halted', u32, 1),
    ('page_0_data_halted', u32, 1),
    ('bad_instr_halted', u32, 1),
    ('reserved1', u32, 1),
    ('breakpoint', u32, 1),
]

# /home/saul/thundergate/include/cpu.h: 92
class struct_cpu_breakpoint(Structure):
    pass

# /home/saul/thundergate/include/cpu.h: 103
class struct_cpu_last_branch_address(Structure):
    pass

# /home/saul/thundergate/include/cpu.h: 114
class struct_cpu_regs(Structure):
    pass

struct_cpu_regs.__slots__ = [
    'mode',
    'status',
    'mask',
    'ofs_0c',
    'ofs_10',
    'ofs_14',
    'ofs_18',
    'pc',
    'ir',
    'spad_uflow',
    'watchdog_enable',
    'watchdog_vector',
    'watchdog_saved_pc',
    'breakpoint',
    'ofs_38',
    'ofs_3c',
    'ofs_40',
    'watchdog_saved_state',
    'lba',
    'spad_uflow_set',
    'ofs_50',
    'ofs_54',
    'ofs_58',
    'ofs_5c',
    'ofs_60',
    'ofs_64',
    'ofs_68',
    'ofs_6c',
    'ofs_70',
    'ofs_74',
    'ofs_78',
    'ofs_7c',
    'ofs_80',
    'ofs_84',
    'ofs_88',
    'ofs_8c',
    'ofs_90',
    'ofs_94',
    'ofs_98',
    'ofs_9c',
    'ofs_a0',
    'ofs_a4',
    'ofs_a8',
    'ofs_ac',
    'ofs_b0',
    'ofs_b4',
    'ofs_b8',
    'ofs_bc',
    'ofs_c0',
    'ofs_c4',
    'ofs_c8',
    'ofs_cc',
    'ofs_d0',
    'ofs_d4',
    'ofs_d8',
    'ofs_dc',
    'ofs_e0',
    'ofs_e4',
    'ofs_e8',
    'ofs_ec',
    'ofs_f0',
    'ofs_f4',
    'ofs_f8',
    'ofs_fc',
    'vcpu_status',
    'device_configuration',
    'vcpu_holding',
    'vcpu_data',
    'vcpu_debug',
    'vcpu_config_shadow_1',
    'vcpu_config_shadow_2',
    'ofs_11c',
    'ofs_120',
    'ofs_124',
    'ofs_128',
    'ofs_12c',
    'ofs_130',
    'ofs_134',
    'ofs_138',
    'ofs_13c',
    'ofs_140',
    'ofs_144',
    'ofs_148',
    'ofs_14c',
    'ofs_150',
    'ofs_154',
    'ofs_158',
    'ofs_15c',
    'ofs_160',
    'ofs_164',
    'ofs_168',
    'ofs_16c',
    'ofs_170',
    'ofs_174',
    'ofs_178',
    'ofs_17c',
    'ofs_180',
    'ofs_184',
    'ofs_188',
    'ofs_18c',
    'ofs_190',
    'ofs_194',
    'ofs_198',
    'ofs_19c',
    'ofs_1a0',
    'ofs_1a4',
    'ofs_1a8',
    'ofs_1ac',
    'ofs_1b0',
    'ofs_1b4',
    'ofs_1b8',
    'ofs_1bc',
    'ofs_1c0',
    'ofs_1c4',
    'ofs_1c8',
    'ofs_1cc',
    'ofs_1d0',
    'ofs_1d4',
    'ofs_1d8',
    'ofs_1dc',
    'ofs_1e0',
    'ofs_1e4',
    'ofs_1e8',
    'ofs_1ec',
    'ofs_1f0',
    'ofs_1f4',
    'ofs_1f8',
    'ofs_1fc',
    'r0',
    'r1',
    'r2',
    'r3',
    'r4',
    'r5',
    'r6',
    'r7',
    'r8',
    'r9',
    'r10',
    'r11',
    'r12',
    'r13',
    'r14',
    'r15',
    'r16',
    'r17',
    'r18',
    'r19',
    'r20',
    'r21',
    'r22',
    'r23',
    'r24',
    'r25',
    'r26',
    'r27',
    'r28',
    'r29',
    'r30',
    'r31',
]
struct_cpu_regs._fields_ = [
    ('mode', struct_cpu_mode),
    ('status', struct_cpu_status),
    ('mask', struct_cpu_event_mask),
    ('ofs_0c', u32),
    ('ofs_10', u32),
    ('ofs_14', u32),
    ('ofs_18', u32),
    ('pc', u32),
    ('ir', u32),
    ('spad_uflow', u32),
    ('watchdog_enable', u32),
    ('watchdog_vector', u32),
    ('watchdog_saved_pc', u32),
    ('breakpoint', struct_cpu_breakpoint),
    ('ofs_38', u32),
    ('ofs_3c', u32),
    ('ofs_40', u32),
    ('watchdog_saved_state', u32),
    ('lba', struct_cpu_last_branch_address),
    ('spad_uflow_set', u32),
    ('ofs_50', u32),
    ('ofs_54', u32),
    ('ofs_58', u32),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('ofs_6c', u32),
    ('ofs_70', u32),
    ('ofs_74', u32),
    ('ofs_78', u32),
    ('ofs_7c', u32),
    ('ofs_80', u32),
    ('ofs_84', u32),
    ('ofs_88', u32),
    ('ofs_8c', u32),
    ('ofs_90', u32),
    ('ofs_94', u32),
    ('ofs_98', u32),
    ('ofs_9c', u32),
    ('ofs_a0', u32),
    ('ofs_a4', u32),
    ('ofs_a8', u32),
    ('ofs_ac', u32),
    ('ofs_b0', u32),
    ('ofs_b4', u32),
    ('ofs_b8', u32),
    ('ofs_bc', u32),
    ('ofs_c0', u32),
    ('ofs_c4', u32),
    ('ofs_c8', u32),
    ('ofs_cc', u32),
    ('ofs_d0', u32),
    ('ofs_d4', u32),
    ('ofs_d8', u32),
    ('ofs_dc', u32),
    ('ofs_e0', u32),
    ('ofs_e4', u32),
    ('ofs_e8', u32),
    ('ofs_ec', u32),
    ('ofs_f0', u32),
    ('ofs_f4', u32),
    ('ofs_f8', u32),
    ('ofs_fc', u32),
    ('vcpu_status', u32),
    ('device_configuration', u32),
    ('vcpu_holding', u32),
    ('vcpu_data', u32),
    ('vcpu_debug', u32),
    ('vcpu_config_shadow_1', u32),
    ('vcpu_config_shadow_2', u32),
    ('ofs_11c', u32),
    ('ofs_120', u32),
    ('ofs_124', u32),
    ('ofs_128', u32),
    ('ofs_12c', u32),
    ('ofs_130', u32),
    ('ofs_134', u32),
    ('ofs_138', u32),
    ('ofs_13c', u32),
    ('ofs_140', u32),
    ('ofs_144', u32),
    ('ofs_148', u32),
    ('ofs_14c', u32),
    ('ofs_150', u32),
    ('ofs_154', u32),
    ('ofs_158', u32),
    ('ofs_15c', u32),
    ('ofs_160', u32),
    ('ofs_164', u32),
    ('ofs_168', u32),
    ('ofs_16c', u32),
    ('ofs_170', u32),
    ('ofs_174', u32),
    ('ofs_178', u32),
    ('ofs_17c', u32),
    ('ofs_180', u32),
    ('ofs_184', u32),
    ('ofs_188', u32),
    ('ofs_18c', u32),
    ('ofs_190', u32),
    ('ofs_194', u32),
    ('ofs_198', u32),
    ('ofs_19c', u32),
    ('ofs_1a0', u32),
    ('ofs_1a4', u32),
    ('ofs_1a8', u32),
    ('ofs_1ac', u32),
    ('ofs_1b0', u32),
    ('ofs_1b4', u32),
    ('ofs_1b8', u32),
    ('ofs_1bc', u32),
    ('ofs_1c0', u32),
    ('ofs_1c4', u32),
    ('ofs_1c8', u32),
    ('ofs_1cc', u32),
    ('ofs_1d0', u32),
    ('ofs_1d4', u32),
    ('ofs_1d8', u32),
    ('ofs_1dc', u32),
    ('ofs_1e0', u32),
    ('ofs_1e4', u32),
    ('ofs_1e8', u32),
    ('ofs_1ec', u32),
    ('ofs_1f0', u32),
    ('ofs_1f4', u32),
    ('ofs_1f8', u32),
    ('ofs_1fc', u32),
    ('r0', u32),
    ('r1', u32),
    ('r2', u32),
    ('r3', u32),
    ('r4', u32),
    ('r5', u32),
    ('r6', u32),
    ('r7', u32),
    ('r8', u32),
    ('r9', u32),
    ('r10', u32),
    ('r11', u32),
    ('r12', u32),
    ('r13', u32),
    ('r14', u32),
    ('r15', u32),
    ('r16', u32),
    ('r17', u32),
    ('r18', u32),
    ('r19', u32),
    ('r20', u32),
    ('r21', u32),
    ('r22', u32),
    ('r23', u32),
    ('r24', u32),
    ('r25', u32),
    ('r26', u32),
    ('r27', u32),
    ('r28', u32),
    ('r29', u32),
    ('r30', u32),
    ('r31', u32),
]

# /home/saul/thundergate/include/cr_port.h: 22
class struct_cr_port_regs(Structure):
    pass

struct_cr_port_regs.__slots__ = [
    'ofs_00',
    'ofs_04',
    'ofs_08',
    'ofs_0c',
    'ofs_10',
    'ofs_14',
    'ofs_18',
    'ofs_1c',
    'ofs_20',
    'ofs_24',
    'ofs_28',
    'ofs_2c',
    'ofs_30',
    'ofs_34',
    'ofs_38',
    'ofs_3c',
    'ofs_40',
    'ofs_44',
    'ofs_48',
    'ofs_4c',
    'ofs_50',
    'ofs_54',
    'ofs_58',
    'ofs_5c',
    'ofs_60',
    'ofs_64',
    'ofs_68',
    'ofs_6c',
    'ofs_70',
    'ofs_74',
    'ofs_78',
    'ofs_7c',
    'ofs_80',
    'ofs_84',
    'ofs_88',
    'ofs_8c',
    'ofs_90',
    'ofs_94',
    'ofs_98',
    'ofs_9c',
    'ofs_a0',
    'ofs_a4',
    'ofs_a8',
    'ofs_ac',
    'ofs_b0',
    'ofs_b4',
    'ofs_b8',
    'ofs_bc',
    'ofs_c0',
    'ofs_c4',
    'ofs_c8',
    'ofs_cc',
    'ofs_d0',
    'ofs_d4',
    'ofs_d8',
    'ofs_dc',
    'ofs_e0',
    'ofs_e4',
    'ofs_e8',
    'ofs_ec',
    'ofs_f0',
    'ofs_f4',
    'ofs_f8',
    'ofs_fc',
    'ofs_100',
    'ofs_104',
    'ofs_108',
    'ofs_10c',
    'ofs_110',
    'ofs_114',
    'ofs_118',
    'ofs_11c',
    'ofs_120',
    'ofs_124',
    'ofs_128',
    'ofs_12c',
    'ofs_130',
    'ofs_134',
    'ofs_138',
    'ofs_13c',
    'ofs_140',
    'ofs_144',
    'ofs_148',
    'ofs_14c',
    'ofs_150',
    'ofs_154',
    'ofs_158',
    'ofs_15c',
    'ofs_160',
    'ofs_164',
    'ofs_168',
    'ofs_16c',
    'ofs_170',
    'ofs_174',
    'ofs_178',
    'ofs_17c',
    'ofs_180',
    'ofs_184',
    'ofs_188',
    'ofs_18c',
    'ofs_190',
    'ofs_194',
    'ofs_198',
    'ofs_19c',
    'ofs_1a0',
    'ofs_1a4',
    'ofs_1a8',
    'ofs_1ac',
    'ofs_1b0',
    'ofs_1b4',
    'ofs_1b8',
    'ofs_1bc',
    'ofs_1c0',
    'ofs_1c4',
    'ofs_1c8',
    'ofs_1cc',
    'ofs_1d0',
    'ofs_1d4',
    'ofs_1d8',
    'ofs_1dc',
    'ofs_1e0',
    'ofs_1e4',
    'ofs_1e8',
    'ofs_1ec',
    'ofs_1f0',
    'ofs_1f4',
    'ofs_1f8',
    'ofs_1fc',
]
struct_cr_port_regs._fields_ = [
    ('ofs_00', u32),
    ('ofs_04', u32),
    ('ofs_08', u32),
    ('ofs_0c', u32),
    ('ofs_10', u32),
    ('ofs_14', u32),
    ('ofs_18', u32),
    ('ofs_1c', u32),
    ('ofs_20', u32),
    ('ofs_24', u32),
    ('ofs_28', u32),
    ('ofs_2c', u32),
    ('ofs_30', u32),
    ('ofs_34', u32),
    ('ofs_38', u32),
    ('ofs_3c', u32),
    ('ofs_40', u32),
    ('ofs_44', u32),
    ('ofs_48', u32),
    ('ofs_4c', u32),
    ('ofs_50', u32),
    ('ofs_54', u32),
    ('ofs_58', u32),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('ofs_6c', u32),
    ('ofs_70', u32),
    ('ofs_74', u32),
    ('ofs_78', u32),
    ('ofs_7c', u32),
    ('ofs_80', u32),
    ('ofs_84', u32),
    ('ofs_88', u32),
    ('ofs_8c', u32),
    ('ofs_90', u32),
    ('ofs_94', u32),
    ('ofs_98', u32),
    ('ofs_9c', u32),
    ('ofs_a0', u32),
    ('ofs_a4', u32),
    ('ofs_a8', u32),
    ('ofs_ac', u32),
    ('ofs_b0', u32),
    ('ofs_b4', u32),
    ('ofs_b8', u32),
    ('ofs_bc', u32),
    ('ofs_c0', u32),
    ('ofs_c4', u32),
    ('ofs_c8', u32),
    ('ofs_cc', u32),
    ('ofs_d0', u32),
    ('ofs_d4', u32),
    ('ofs_d8', u32),
    ('ofs_dc', u32),
    ('ofs_e0', u32),
    ('ofs_e4', u32),
    ('ofs_e8', u32),
    ('ofs_ec', u32),
    ('ofs_f0', u32),
    ('ofs_f4', u32),
    ('ofs_f8', u32),
    ('ofs_fc', u32),
    ('ofs_100', u32),
    ('ofs_104', u32),
    ('ofs_108', u32),
    ('ofs_10c', u32),
    ('ofs_110', u32),
    ('ofs_114', u32),
    ('ofs_118', u32),
    ('ofs_11c', u32),
    ('ofs_120', u32),
    ('ofs_124', u32),
    ('ofs_128', u32),
    ('ofs_12c', u32),
    ('ofs_130', u32),
    ('ofs_134', u32),
    ('ofs_138', u32),
    ('ofs_13c', u32),
    ('ofs_140', u32),
    ('ofs_144', u32),
    ('ofs_148', u32),
    ('ofs_14c', u32),
    ('ofs_150', u32),
    ('ofs_154', u32),
    ('ofs_158', u32),
    ('ofs_15c', u32),
    ('ofs_160', u32),
    ('ofs_164', u32),
    ('ofs_168', u32),
    ('ofs_16c', u32),
    ('ofs_170', u32),
    ('ofs_174', u32),
    ('ofs_178', u32),
    ('ofs_17c', u32),
    ('ofs_180', u32),
    ('ofs_184', u32),
    ('ofs_188', u32),
    ('ofs_18c', u32),
    ('ofs_190', u32),
    ('ofs_194', u32),
    ('ofs_198', u32),
    ('ofs_19c', u32),
    ('ofs_1a0', u32),
    ('ofs_1a4', u32),
    ('ofs_1a8', u32),
    ('ofs_1ac', u32),
    ('ofs_1b0', u32),
    ('ofs_1b4', u32),
    ('ofs_1b8', u32),
    ('ofs_1bc', u32),
    ('ofs_1c0', u32),
    ('ofs_1c4', u32),
    ('ofs_1c8', u32),
    ('ofs_1cc', u32),
    ('ofs_1d0', u32),
    ('ofs_1d4', u32),
    ('ofs_1d8', u32),
    ('ofs_1dc', u32),
    ('ofs_1e0', u32),
    ('ofs_1e4', u32),
    ('ofs_1e8', u32),
    ('ofs_1ec', u32),
    ('ofs_1f0', u32),
    ('ofs_1f4', u32),
    ('ofs_1f8', u32),
    ('ofs_1fc', u32),
]

# /home/saul/thundergate/include/dmac.h: 22
class struct_dmac_mode(Structure):
    pass

# /home/saul/thundergate/include/dmac.h: 33
class struct_dmac_regs(Structure):
    pass

struct_dmac_regs.__slots__ = [
    'mode',
]
struct_dmac_regs._fields_ = [
    ('mode', struct_dmac_mode),
]

# /home/saul/thundergate/include/dma.h: 22
class struct_dma_desc(Structure):
    pass

struct_dma_desc.__slots__ = [
    'addr_hi',
    'addr_lo',
    'nic_mbuf',
    'flags',
    'opaque1',
    'opaque2',
    'opaque3',
]
struct_dma_desc._fields_ = [
    ('addr_hi', u32),
    ('addr_lo', u32),
    ('nic_mbuf', u32),
    ('flags', u32),
    ('opaque1', u32),
    ('opaque2', u32),
    ('opaque3', u32),
]

# /home/saul/thundergate/include/emac.h: 24
class struct_emac_mode(Structure):
    pass

struct_emac_mode.__slots__ = [
    'ext_magic_pkt_en',
    'magic_pkt_free_running_mode_en',
    'mac_loop_back_mode_ctrl',
    'en_ape_tx_path',
    'en_ape_rx_path',
    'free_running_acpi',
    'halt_interesting_packets_pme',
    'keep_frame_in_wol',
    'en_fhde',
    'en_rde',
    'en_tde',
    'reserved20',
    'acpi_power_on',
    'magic_packet_detection',
    'send_config_command',
    'flush_tx_statistics',
    'clear_tx_statistics',
    'en_tx_statistics',
    'flush_rx_statistics',
    'clear_rx_statistics',
    'en_rx_statistics',
    'reserved10',
    'max_defer',
    'en_tx_bursting',
    'tagged_mac_control',
    'reserved5',
    'loopback',
    'port_mode',
    'half_duplex',
    'global_reset',
]
struct_emac_mode._fields_ = [
    ('ext_magic_pkt_en', u32, 1),
    ('magic_pkt_free_running_mode_en', u32, 1),
    ('mac_loop_back_mode_ctrl', u32, 1),
    ('en_ape_tx_path', u32, 1),
    ('en_ape_rx_path', u32, 1),
    ('free_running_acpi', u32, 1),
    ('halt_interesting_packets_pme', u32, 1),
    ('keep_frame_in_wol', u32, 1),
    ('en_fhde', u32, 1),
    ('en_rde', u32, 1),
    ('en_tde', u32, 1),
    ('reserved20', u32, 1),
    ('acpi_power_on', u32, 1),
    ('magic_packet_detection', u32, 1),
    ('send_config_command', u32, 1),
    ('flush_tx_statistics', u32, 1),
    ('clear_tx_statistics', u32, 1),
    ('en_tx_statistics', u32, 1),
    ('flush_rx_statistics', u32, 1),
    ('clear_rx_statistics', u32, 1),
    ('en_rx_statistics', u32, 1),
    ('reserved10', u32, 1),
    ('max_defer', u32, 1),
    ('en_tx_bursting', u32, 1),
    ('tagged_mac_control', u32, 1),
    ('reserved5', u32, 2),
    ('loopback', u32, 1),
    ('port_mode', u32, 2),
    ('half_duplex', u32, 1),
    ('global_reset', u32, 1),
]

# /home/saul/thundergate/include/emac.h: 57
class struct_emac_status(Structure):
    pass

struct_emac_status.__slots__ = [
    'reserved29',
    'interesting_packet_pme_attention',
    'tx_statistic_overrun',
    'rx_statistic_overrun',
    'odi_error',
    'ap_error',
    'mii_interrupt',
    'mii_completion',
    'reserved13',
    'link_state_changed',
    'reserved0',
]
struct_emac_status._fields_ = [
    ('reserved29', u32, 3),
    ('interesting_packet_pme_attention', u32, 1),
    ('tx_statistic_overrun', u32, 1),
    ('rx_statistic_overrun', u32, 1),
    ('odi_error', u32, 1),
    ('ap_error', u32, 1),
    ('mii_interrupt', u32, 1),
    ('mii_completion', u32, 1),
    ('reserved13', u32, 9),
    ('link_state_changed', u32, 1),
    ('reserved0', u32, 12),
]

# /home/saul/thundergate/include/emac.h: 71
class struct_emac_event_enable(Structure):
    pass

struct_emac_event_enable.__slots__ = [
    'reserved30',
    'tx_offload_error_interrupt',
    'interesting_packet_pme_attn_en',
    'tx_statistics_overrun',
    'rx_statistics_overrun',
    'odi_error',
    'ap_error',
    'mii_interrupt',
    'mii_completion',
    'reserved13',
    'link_state_changed',
    'reserved0',
]
struct_emac_event_enable._fields_ = [
    ('reserved30', u32, 2),
    ('tx_offload_error_interrupt', u32, 1),
    ('interesting_packet_pme_attn_en', u32, 1),
    ('tx_statistics_overrun', u32, 1),
    ('rx_statistics_overrun', u32, 1),
    ('odi_error', u32, 1),
    ('ap_error', u32, 1),
    ('mii_interrupt', u32, 1),
    ('mii_completion', u32, 1),
    ('reserved13', u32, 9),
    ('link_state_changed', u32, 1),
    ('reserved0', u32, 12),
]

# /home/saul/thundergate/include/emac.h: 86
class struct_emac_led_control(Structure):
    pass

# /home/saul/thundergate/include/emac.h: 112
class struct_transmit_mac_mode(Structure):
    pass

struct_transmit_mac_mode.__slots__ = [
    'rr_weight',
    'transmit_ftq_arbitration_mode',
    'reserved21',
    'txmbuf_burst_size',
    'do_not_insert_gcm_gmac_iv',
    'do_not_drop_packet_if_malformed',
    'do_not_drop_if_sa_found_in_rx_direction',
    'do_not_drop_if_unsupported_ipv6_extension_or_ipv4_option_found',
    'do_not_drop_if_sa_invalid',
    'do_not_drop_if_ah_esp_header_not_found',
    'en_tx_ah_offload',
    'en_rx_esp_offload',
    'enable_bad_txmbuf_lockup_fix',
    'link_aware_enable',
    'enable_long_pause',
    'enable_big_backoff',
    'enable_flow_control',
    'reserved2',
    'enable',
    'reset',
]
struct_transmit_mac_mode._fields_ = [
    ('rr_weight', u32, 5),
    ('transmit_ftq_arbitration_mode', u32, 3),
    ('reserved21', u32, 3),
    ('txmbuf_burst_size', u32, 4),
    ('do_not_insert_gcm_gmac_iv', u32, 1),
    ('do_not_drop_packet_if_malformed', u32, 1),
    ('do_not_drop_if_sa_found_in_rx_direction', u32, 1),
    ('do_not_drop_if_unsupported_ipv6_extension_or_ipv4_option_found', u32, 1),
    ('do_not_drop_if_sa_invalid', u32, 1),
    ('do_not_drop_if_ah_esp_header_not_found', u32, 1),
    ('en_tx_ah_offload', u32, 1),
    ('en_rx_esp_offload', u32, 1),
    ('enable_bad_txmbuf_lockup_fix', u32, 1),
    ('link_aware_enable', u32, 1),
    ('enable_long_pause', u32, 1),
    ('enable_big_backoff', u32, 1),
    ('enable_flow_control', u32, 1),
    ('reserved2', u32, 2),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/emac.h: 135
class struct_transmit_mac_status(Structure):
    pass

# /home/saul/thundergate/include/emac.h: 150
class struct_transmit_mac_lengths(Structure):
    pass

struct_transmit_mac_lengths.__slots__ = [
    'reserved',
    'ipg_crs',
    'ipg',
    'slot',
]
struct_transmit_mac_lengths._fields_ = [
    ('reserved', u32, 18),
    ('ipg_crs', u32, 2),
    ('ipg', u32, 4),
    ('slot', u32, 8),
]

# /home/saul/thundergate/include/emac.h: 157
class struct_receive_mac_mode(Structure):
    pass

struct_receive_mac_mode.__slots__ = [
    'disable_hw_fix_24175',
    'disable_hw_fix_29914',
    'disable_8023_len_chk_fix',
    'reserved28',
    'reserved27',
    'status_ready_new_disable',
    'ipv4_frag_fix',
    'ipv6_enable',
    'rss_enable',
    'rss_hash_mask_bits',
    'rss_tcpipv6_hash_enable',
    'rss_ipv6_hash_enable',
    'rss_tcpipv4_hash_enable',
    'rss_ipv4_hash_enable',
    'reserved14',
    'ape_promisc_mode_en',
    'cq42199_fix_dis',
    'filter_broadcast',
    'keep_vlan_tag_diag',
    'no_crc_check',
    'promiscuous_mode',
    'length_check',
    'accept_runts',
    'keep_oversized',
    'keep_pause',
    'keep_mfc',
    'enable_flow_control',
    'enable',
    'reset',
]
struct_receive_mac_mode._fields_ = [
    ('disable_hw_fix_24175', u32, 1),
    ('disable_hw_fix_29914', u32, 1),
    ('disable_8023_len_chk_fix', u32, 1),
    ('reserved28', u32, 1),
    ('reserved27', u32, 1),
    ('status_ready_new_disable', u32, 1),
    ('ipv4_frag_fix', u32, 1),
    ('ipv6_enable', u32, 1),
    ('rss_enable', u32, 1),
    ('rss_hash_mask_bits', u32, 3),
    ('rss_tcpipv6_hash_enable', u32, 1),
    ('rss_ipv6_hash_enable', u32, 1),
    ('rss_tcpipv4_hash_enable', u32, 1),
    ('rss_ipv4_hash_enable', u32, 1),
    ('reserved14', u32, 2),
    ('ape_promisc_mode_en', u32, 1),
    ('cq42199_fix_dis', u32, 1),
    ('filter_broadcast', u32, 1),
    ('keep_vlan_tag_diag', u32, 1),
    ('no_crc_check', u32, 1),
    ('promiscuous_mode', u32, 1),
    ('length_check', u32, 1),
    ('accept_runts', u32, 1),
    ('keep_oversized', u32, 1),
    ('keep_pause', u32, 1),
    ('keep_mfc', u32, 1),
    ('enable_flow_control', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/emac.h: 189
class struct_receive_mac_status(Structure):
    pass

# /home/saul/thundergate/include/emac.h: 205
class struct_emac_mac_addr(Structure):
    pass

# /home/saul/thundergate/include/emac.h: 225
class struct_emac_rx_rule_control(Structure):
    pass

# /home/saul/thundergate/include/emac.h: 246
class struct_receive_mac_rules_configuration(Structure):
    pass

struct_receive_mac_rules_configuration.__slots__ = [
    'reserved',
    'no_rules_matches_default_class',
    'reserved2',
]
struct_receive_mac_rules_configuration._fields_ = [
    ('reserved', u32, 27),
    ('no_rules_matches_default_class', u32, 3),
    ('reserved2', u32, 2),
]

# /home/saul/thundergate/include/emac.h: 252
class struct_emac_low_watermark_max_receive_frame(Structure):
    pass

struct_emac_low_watermark_max_receive_frame.__slots__ = [
    'reserved',
    'txfifo_almost_empty_thresh',
    'count',
]
struct_emac_low_watermark_max_receive_frame._fields_ = [
    ('reserved', u32, 11),
    ('txfifo_almost_empty_thresh', u32, 5),
    ('count', u32, 16),
]

# /home/saul/thundergate/include/emac.h: 258
class struct_emac_mii_status(Structure):
    pass

struct_emac_mii_status.__slots__ = [
    'communications_register_overlap_error',
    'reserved2',
    'mode_10mbps',
    'link_status',
]
struct_emac_mii_status._fields_ = [
    ('communications_register_overlap_error', u32, 1),
    ('reserved2', u32, 29),
    ('mode_10mbps', u32, 1),
    ('link_status', u32, 1),
]

# /home/saul/thundergate/include/emac.h: 265
class struct_emac_mii_mode(Structure):
    pass

struct_emac_mii_mode.__slots__ = [
    'communication_delay_fix_disable',
    'reserved21',
    'mii_clock_count',
    'enable_constant_mdc_clock_speed',
    'reserved10',
    'phy_address',
    'port_polling',
    'reserved3',
    'auto_control',
    'use_short_preamble',
    'fast_clock',
]
struct_emac_mii_mode._fields_ = [
    ('communication_delay_fix_disable', u32, 1),
    ('reserved21', u32, 10),
    ('mii_clock_count', u32, 5),
    ('enable_constant_mdc_clock_speed', u32, 1),
    ('reserved10', u32, 5),
    ('phy_address', u32, 5),
    ('port_polling', u32, 1),
    ('reserved3', u32, 1),
    ('auto_control', u32, 1),
    ('use_short_preamble', u32, 1),
    ('fast_clock', u32, 1),
]

# /home/saul/thundergate/include/emac.h: 279
class struct_emac_autopolling_status(Structure):
    pass

struct_emac_autopolling_status.__slots__ = [
    'reserved',
    'error',
]
struct_emac_autopolling_status._fields_ = [
    ('reserved', u32, 31),
    ('error', u32, 1),
]

# /home/saul/thundergate/include/emac.h: 284
class struct_emac_mii_communication(Structure):
    pass

struct_emac_mii_communication.__slots__ = [
    'reserved30',
    'start_busy',
    'read_failed',
    'read_command',
    'write_command',
    'phy_addr',
    'reg_addr',
    'data',
]
struct_emac_mii_communication._fields_ = [
    ('reserved30', u32, 2),
    ('start_busy', u32, 1),
    ('read_failed', u32, 1),
    ('read_command', u32, 1),
    ('write_command', u32, 1),
    ('phy_addr', u32, 5),
    ('reg_addr', u32, 5),
    ('data', u32, 16),
]

# /home/saul/thundergate/include/emac.h: 295
class struct_emac_regulator_voltage_control(Structure):
    pass

struct_emac_regulator_voltage_control.__slots__ = [
    'reserved',
    'regclt_1_2v_core',
    'reserved2',
    'spd1000_led_pin_output_override',
    'spd1000_led_pin_output_en_override',
    'spd1000_led_pin_override_en',
    'spd1000_led_pin_input',
    'spd100_led_pin_output_override',
    'spd100_led_pin_output_en_override',
    'spd100_led_pin_override_en',
    'spd100_led_pin_input',
    'link_led_pin_output_override',
    'link_led_pin_output_en_override',
    'link_led_pin_override_en',
    'link_led_pin_input',
    'traffic_led_pin_output_override',
    'traffic_led_pin_output_en_override',
    'traffic_led_pin_override_en',
    'traffic_led_pin_input',
]
struct_emac_regulator_voltage_control._fields_ = [
    ('reserved', u32, 8),
    ('regclt_1_2v_core', u32, 4),
    ('reserved2', u32, 4),
    ('spd1000_led_pin_output_override', u32, 1),
    ('spd1000_led_pin_output_en_override', u32, 1),
    ('spd1000_led_pin_override_en', u32, 1),
    ('spd1000_led_pin_input', u32, 1),
    ('spd100_led_pin_output_override', u32, 1),
    ('spd100_led_pin_output_en_override', u32, 1),
    ('spd100_led_pin_override_en', u32, 1),
    ('spd100_led_pin_input', u32, 1),
    ('link_led_pin_output_override', u32, 1),
    ('link_led_pin_output_en_override', u32, 1),
    ('link_led_pin_override_en', u32, 1),
    ('link_led_pin_input', u32, 1),
    ('traffic_led_pin_output_override', u32, 1),
    ('traffic_led_pin_output_en_override', u32, 1),
    ('traffic_led_pin_override_en', u32, 1),
    ('traffic_led_pin_input', u32, 1),
]

# /home/saul/thundergate/include/emac.h: 346
class struct_anon_2(Structure):
    pass

struct_anon_2.__slots__ = [
    'control',
    'mask_value',
]
struct_anon_2._fields_ = [
    ('control', struct_emac_rx_rule_control),
    ('mask_value', u32),
]

# /home/saul/thundergate/include/emac.h: 320
class struct_emac_regs(Structure):
    pass

struct_emac_regs.__slots__ = [
    'mode',
    'status',
    'event_enable',
    'led_control',
    'addr',
    'wol_pattern_pointer',
    'wol_pattern_configuration',
    'tx_random_backoff',
    'rx_mtu',
    'ofs_40',
    'ofs_44',
    'ofs_48',
    'mii_communication',
    'mii_status',
    'mii_mode',
    'autopolling_status',
    'tx_mac_mode',
    'tx_mac_status',
    'tx_mac_lengths',
    'rx_mac_mode',
    'rx_mac_status',
    'mac_hash_0',
    'mac_hash_1',
    'mac_hash_2',
    'mac_hash_3',
    'rx_rule',
    'ofs_c0',
    'ofs_c4',
    'ofs_c8',
    'ofs_cc',
    'ofs_d0',
    'ofs_d4',
    'ofs_d8',
    'ofs_dc',
    'ofs_e0',
    'ofs_e4',
    'ofs_e8',
    'ofs_ec',
    'ofs_f0',
    'ofs_f4',
    'ofs_f8',
    'ofs_fc',
    'rx_rules_conf',
    'low_watermark_max_receive_frame',
    'ofs_108',
    'ofs_10c',
    'ofs_110',
    'ofs_114',
    'ofs_118',
    'ofs_11c',
    'ofs_120',
    'ofs_124',
    'ofs_128',
    'ofs_12c',
    'ofs_130',
    'ofs_134',
    'ofs_138',
    'ofs_13c',
    'ofs_140',
    'ofs_144',
    'ofs_148',
    'ofs_14c',
    'ofs_150',
    'ofs_154',
    'ofs_158',
    'ofs_15c',
    'ofs_160',
    'ofs_164',
    'ofs_168',
    'ofs_16c',
    'ofs_170',
    'ofs_174',
    'ofs_178',
    'ofs_17c',
    'ofs_180',
    'ofs_184',
    'ofs_188',
    'ofs_18c',
    'regulator_voltage_control',
    'ofs_194',
    'ofs_198',
    'ofs_19c',
    'ofs_1a0',
    'ofs_1a4',
    'ofs_1a8',
    'ofs_1ac',
    'ofs_1b0',
    'ofs_1b4',
    'ofs_1b8',
    'ofs_1bc',
    'eav_tx_time_stamp_lsb',
    'eav_tx_time_stamp_msb',
    'eav_av_transmit_tolerance_window',
    'eav_rt_tx_quality_1',
    'eav_rt_tx_quality_2',
    'eav_rt_tx_quality_3',
    'eav_rt_tx_quality_4',
    'ofs_1dc',
]
struct_emac_regs._fields_ = [
    ('mode', struct_emac_mode),
    ('status', struct_emac_status),
    ('event_enable', struct_emac_event_enable),
    ('led_control', struct_emac_led_control),
    ('addr', struct_emac_mac_addr * 4),
    ('wol_pattern_pointer', u32),
    ('wol_pattern_configuration', u32),
    ('tx_random_backoff', u32),
    ('rx_mtu', u32),
    ('ofs_40', u32),
    ('ofs_44', u32),
    ('ofs_48', u32),
    ('mii_communication', struct_emac_mii_communication),
    ('mii_status', struct_emac_mii_status),
    ('mii_mode', struct_emac_mii_mode),
    ('autopolling_status', struct_emac_autopolling_status),
    ('tx_mac_mode', struct_transmit_mac_mode),
    ('tx_mac_status', struct_transmit_mac_status),
    ('tx_mac_lengths', struct_transmit_mac_lengths),
    ('rx_mac_mode', struct_receive_mac_mode),
    ('rx_mac_status', struct_receive_mac_status),
    ('mac_hash_0', u32),
    ('mac_hash_1', u32),
    ('mac_hash_2', u32),
    ('mac_hash_3', u32),
    ('rx_rule', struct_anon_2 * 8),
    ('ofs_c0', u32),
    ('ofs_c4', u32),
    ('ofs_c8', u32),
    ('ofs_cc', u32),
    ('ofs_d0', u32),
    ('ofs_d4', u32),
    ('ofs_d8', u32),
    ('ofs_dc', u32),
    ('ofs_e0', u32),
    ('ofs_e4', u32),
    ('ofs_e8', u32),
    ('ofs_ec', u32),
    ('ofs_f0', u32),
    ('ofs_f4', u32),
    ('ofs_f8', u32),
    ('ofs_fc', u32),
    ('rx_rules_conf', struct_receive_mac_rules_configuration),
    ('low_watermark_max_receive_frame', struct_emac_low_watermark_max_receive_frame),
    ('ofs_108', u32),
    ('ofs_10c', u32),
    ('ofs_110', u32),
    ('ofs_114', u32),
    ('ofs_118', u32),
    ('ofs_11c', u32),
    ('ofs_120', u32),
    ('ofs_124', u32),
    ('ofs_128', u32),
    ('ofs_12c', u32),
    ('ofs_130', u32),
    ('ofs_134', u32),
    ('ofs_138', u32),
    ('ofs_13c', u32),
    ('ofs_140', u32),
    ('ofs_144', u32),
    ('ofs_148', u32),
    ('ofs_14c', u32),
    ('ofs_150', u32),
    ('ofs_154', u32),
    ('ofs_158', u32),
    ('ofs_15c', u32),
    ('ofs_160', u32),
    ('ofs_164', u32),
    ('ofs_168', u32),
    ('ofs_16c', u32),
    ('ofs_170', u32),
    ('ofs_174', u32),
    ('ofs_178', u32),
    ('ofs_17c', u32),
    ('ofs_180', u32),
    ('ofs_184', u32),
    ('ofs_188', u32),
    ('ofs_18c', u32),
    ('regulator_voltage_control', struct_emac_regulator_voltage_control),
    ('ofs_194', u32),
    ('ofs_198', u32),
    ('ofs_19c', u32),
    ('ofs_1a0', u32),
    ('ofs_1a4', u32),
    ('ofs_1a8', u32),
    ('ofs_1ac', u32),
    ('ofs_1b0', u32),
    ('ofs_1b4', u32),
    ('ofs_1b8', u32),
    ('ofs_1bc', u32),
    ('eav_tx_time_stamp_lsb', u32),
    ('eav_tx_time_stamp_msb', u32),
    ('eav_av_transmit_tolerance_window', u32),
    ('eav_rt_tx_quality_1', u32),
    ('eav_rt_tx_quality_2', u32),
    ('eav_rt_tx_quality_3', u32),
    ('eav_rt_tx_quality_4', u32),
    ('ofs_1dc', u32),
]

# /home/saul/thundergate/include/frame.h: 24
class struct_frame(Structure):
    pass

struct_frame.__slots__ = [
    'dest',
    'src',
    'type',
    'data',
]
struct_frame._fields_ = [
    ('dest', u8 * 6),
    ('src', u8 * 6),
    ('type', u16),
    ('data', u8 * 0),
]

# /home/saul/thundergate/include/frame.h: 31
class struct_vlan_frame(Structure):
    pass

struct_vlan_frame.__slots__ = [
    'dest',
    'src',
    'tpid',
    'type',
    'data',
]
struct_vlan_frame._fields_ = [
    ('dest', u8 * 6),
    ('src', u8 * 6),
    ('tpid', u16),
    ('type', u16),
    ('data', u8 * 0),
]

# /home/saul/thundergate/include/ftq.h: 22
class struct_ftq_reset(Structure):
    pass

# /home/saul/thundergate/include/ftq.h: 48
class struct_ftq_enqueue_dequeue(Structure):
    pass

# /home/saul/thundergate/include/ftq.h: 60
class struct_ftq_write_peek(Structure):
    pass

# /home/saul/thundergate/include/ftq.h: 74
class struct_ftq_queue_regs(Structure):
    pass

struct_ftq_queue_regs.__slots__ = [
    'control',
    'count',
    'q',
    'peek',
]
struct_ftq_queue_regs._fields_ = [
    ('control', u32),
    ('count', u32),
    ('q', struct_ftq_enqueue_dequeue),
    ('peek', struct_ftq_write_peek),
]

# /home/saul/thundergate/include/ftq.h: 81
class struct_ftq_regs(Structure):
    pass

struct_ftq_regs.__slots__ = [
    'reset',
    'ofs_04',
    'ofs_08',
    'ofs_0c',
    'dma_read',
    'dma_high_read',
    'dma_comp_discard',
    'send_bd_comp',
    'send_data_init',
    'dma_write',
    'dma_high_write',
    'sw_type1',
    'send_data_comp',
    'host_coalesce',
    'mac_tx',
    'mbuf_clust_free',
    'rcv_bd_comp',
    'rcv_list_plmt',
    'rdiq',
    'rcv_data_comp',
    'sw_type2',
]
struct_ftq_regs._fields_ = [
    ('reset', struct_ftq_reset),
    ('ofs_04', u32),
    ('ofs_08', u32),
    ('ofs_0c', u32),
    ('dma_read', struct_ftq_queue_regs),
    ('dma_high_read', struct_ftq_queue_regs),
    ('dma_comp_discard', struct_ftq_queue_regs),
    ('send_bd_comp', struct_ftq_queue_regs),
    ('send_data_init', struct_ftq_queue_regs),
    ('dma_write', struct_ftq_queue_regs),
    ('dma_high_write', struct_ftq_queue_regs),
    ('sw_type1', struct_ftq_queue_regs),
    ('send_data_comp', struct_ftq_queue_regs),
    ('host_coalesce', struct_ftq_queue_regs),
    ('mac_tx', struct_ftq_queue_regs),
    ('mbuf_clust_free', struct_ftq_queue_regs),
    ('rcv_bd_comp', struct_ftq_queue_regs),
    ('rcv_list_plmt', struct_ftq_queue_regs),
    ('rdiq', struct_ftq_queue_regs),
    ('rcv_data_comp', struct_ftq_queue_regs),
    ('sw_type2', struct_ftq_queue_regs),
]

# /home/saul/thundergate/include/gencomm.h: 24
class struct_gencomm(Structure):
    pass

struct_gencomm.__slots__ = [
    'dword',
]
struct_gencomm._fields_ = [
    ('dword', u32 * 256),
]

# /home/saul/thundergate/include/grc.h: 22
class struct_grc_mode(Structure):
    pass

struct_grc_mode.__slots__ = [
    'pcie_hi1k_en',
    'multi_cast_enable',
    'pcie_dl_sel',
    'int_on_flow_attn',
    'int_on_dma_attn',
    'int_on_mac_attn',
    'int_on_rxcpu_attn',
    'int_on_txcpu_attn',
    'receive_no_pseudo_header_cksum',
    'pcie_pl_sel',
    'nvram_write_enable',
    'send_no_pseudo_header_cksum',
    'time_sync_enable',
    'eav_mode_enable',
    'host_send_bds',
    'host_stack_up',
    'force_32bit_pci_bus_mode',
    'no_int_on_recv',
    'no_int_on_send',
    'dma_write_sys_attn',
    'allow_bad_frames',
    'no_crc',
    'no_frame_cracking',
    'split_hdr_mode',
    'cr_func_sel',
    'word_swap_data',
    'byte_swap_data',
    'reserved5',
    'word_swap_bd',
    'byte_swap_bd',
    'int_send_tick',
]
struct_grc_mode._fields_ = [
    ('pcie_hi1k_en', u32, 1),
    ('multi_cast_enable', u32, 1),
    ('pcie_dl_sel', u32, 1),
    ('int_on_flow_attn', u32, 1),
    ('int_on_dma_attn', u32, 1),
    ('int_on_mac_attn', u32, 1),
    ('int_on_rxcpu_attn', u32, 1),
    ('int_on_txcpu_attn', u32, 1),
    ('receive_no_pseudo_header_cksum', u32, 1),
    ('pcie_pl_sel', u32, 1),
    ('nvram_write_enable', u32, 1),
    ('send_no_pseudo_header_cksum', u32, 1),
    ('time_sync_enable', u32, 1),
    ('eav_mode_enable', u32, 1),
    ('host_send_bds', u32, 1),
    ('host_stack_up', u32, 1),
    ('force_32bit_pci_bus_mode', u32, 1),
    ('no_int_on_recv', u32, 1),
    ('no_int_on_send', u32, 1),
    ('dma_write_sys_attn', u32, 1),
    ('allow_bad_frames', u32, 1),
    ('no_crc', u32, 1),
    ('no_frame_cracking', u32, 1),
    ('split_hdr_mode', u32, 1),
    ('cr_func_sel', u32, 2),
    ('word_swap_data', u32, 1),
    ('byte_swap_data', u32, 1),
    ('reserved5', u32, 1),
    ('word_swap_bd', u32, 1),
    ('byte_swap_bd', u32, 1),
    ('int_send_tick', u32, 1),
]

# /home/saul/thundergate/include/grc.h: 56
class struct_grc_misc_config(Structure):
    pass

struct_grc_misc_config.__slots__ = [
    'bond_id_7',
    'bond_id_6',
    'disable_grc_reset_on_pcie_block',
    'bond_id_5',
    'bond_id_4',
    'gphy_keep_power_during_reset',
    'reserved1',
    'ram_powerdown',
    'reserved2',
    'bias_iddq',
    'gphy_iddq',
    'powerdown',
    'vmain_prsnt_state',
    'power_state',
    'bond_id_3',
    'bond_id_2',
    'bond_id_1',
    'bond_id_0',
    'reserved3',
    'timer_prescaler',
    'grc_reset',
]
struct_grc_misc_config._fields_ = [
    ('bond_id_7', u32, 1),
    ('bond_id_6', u32, 1),
    ('disable_grc_reset_on_pcie_block', u32, 1),
    ('bond_id_5', u32, 1),
    ('bond_id_4', u32, 1),
    ('gphy_keep_power_during_reset', u32, 1),
    ('reserved1', u32, 1),
    ('ram_powerdown', u32, 1),
    ('reserved2', u32, 1),
    ('bias_iddq', u32, 1),
    ('gphy_iddq', u32, 1),
    ('powerdown', u32, 1),
    ('vmain_prsnt_state', u32, 1),
    ('power_state', u32, 2),
    ('bond_id_3', u32, 1),
    ('bond_id_2', u32, 1),
    ('bond_id_1', u32, 1),
    ('bond_id_0', u32, 1),
    ('reserved3', u32, 5),
    ('timer_prescaler', u32, 7),
    ('grc_reset', u32, 1),
]

# /home/saul/thundergate/include/grc.h: 80
class struct_grc_misc_local_control(Structure):
    pass

struct_grc_misc_local_control.__slots__ = [
    'wake_on_link_up',
    'wake_on_link_down',
    'disable_traffic_led_fix',
    'reserved',
    'pme_assert',
    'reserved1',
    'auto_seeprom',
    'reserved2',
    'ctrl_ssram_type',
    'bank_select',
    'reserved3',
    'enable_ext_memory',
    'gpio2_output',
    'gpio1_output',
    'gpio0_output',
    'gpio2_output_enable',
    'gpio1_output_enable',
    'gpio0_output_enable',
    'gpio2_input',
    'gpio1_input',
    'gpio0_input',
    'reserved4',
    'energy_detection_pin',
    'uart_disable',
    'interrupt_on_attention',
    'set_interrupt',
    'clear_interrupt',
    'interrupt_state',
]
struct_grc_misc_local_control._fields_ = [
    ('wake_on_link_up', u32, 1),
    ('wake_on_link_down', u32, 1),
    ('disable_traffic_led_fix', u32, 1),
    ('reserved', u32, 2),
    ('pme_assert', u32, 1),
    ('reserved1', u32, 1),
    ('auto_seeprom', u32, 1),
    ('reserved2', u32, 1),
    ('ctrl_ssram_type', u32, 1),
    ('bank_select', u32, 1),
    ('reserved3', u32, 3),
    ('enable_ext_memory', u32, 1),
    ('gpio2_output', u32, 1),
    ('gpio1_output', u32, 1),
    ('gpio0_output', u32, 1),
    ('gpio2_output_enable', u32, 1),
    ('gpio1_output_enable', u32, 1),
    ('gpio0_output_enable', u32, 1),
    ('gpio2_input', u32, 1),
    ('gpio1_input', u32, 1),
    ('gpio0_input', u32, 1),
    ('reserved4', u32, 2),
    ('energy_detection_pin', u32, 1),
    ('uart_disable', u32, 1),
    ('interrupt_on_attention', u32, 1),
    ('set_interrupt', u32, 1),
    ('clear_interrupt', u32, 1),
    ('interrupt_state', u32, 1),
]

# /home/saul/thundergate/include/grc.h: 111
class struct_grc_cpu_event(Structure):
    pass

# /home/saul/thundergate/include/grc.h: 151
class struct_grc_cpu_semaphore(Structure):
    pass

struct_grc_cpu_semaphore.__slots__ = [
    'reserved',
    'semaphore',
]
struct_grc_cpu_semaphore._fields_ = [
    ('reserved', u32, 31),
    ('semaphore', u32, 1),
]

# /home/saul/thundergate/include/grc.h: 156
class struct_grc_pcie_misc_status(Structure):
    pass

struct_grc_pcie_misc_status.__slots__ = [
    'reserved',
    'p1_pcie_ack_fifo_underrun',
    'p0_pcie_ack_fifo_underrun',
    'p1_pcie_ack_fifo_overrun',
    'p0_pcie_ack_fifo_overrun',
    'reserved2',
    'pcie_link_in_l23',
    'f0_pcie_powerstate',
    'f1_pcie_powerstate',
    'f2_pcie_powerstate',
    'f3_pcie_powerstate',
    'pcie_phy_attn',
    'pci_grc_intb_f3',
    'pci_grc_intb_f2',
    'pci_grc_intb_f1',
    'pci_grc_inta',
]
struct_grc_pcie_misc_status._fields_ = [
    ('reserved', u32, 8),
    ('p1_pcie_ack_fifo_underrun', u32, 1),
    ('p0_pcie_ack_fifo_underrun', u32, 1),
    ('p1_pcie_ack_fifo_overrun', u32, 1),
    ('p0_pcie_ack_fifo_overrun', u32, 1),
    ('reserved2', u32, 3),
    ('pcie_link_in_l23', u32, 1),
    ('f0_pcie_powerstate', u32, 2),
    ('f1_pcie_powerstate', u32, 2),
    ('f2_pcie_powerstate', u32, 2),
    ('f3_pcie_powerstate', u32, 2),
    ('pcie_phy_attn', u32, 4),
    ('pci_grc_intb_f3', u32, 1),
    ('pci_grc_intb_f2', u32, 1),
    ('pci_grc_intb_f1', u32, 1),
    ('pci_grc_inta', u32, 1),
]

# /home/saul/thundergate/include/grc.h: 175
class struct_grc_cpu_event_enable(Structure):
    pass

# /home/saul/thundergate/include/grc.h: 215
class struct_grc_secfg_1(Structure):
    pass

struct_grc_secfg_1.__slots__ = [
    'cr_vddio_30v_reg_out_adj',
    'cr_vddio_18v_reg_out_adj',
    'si_eedata_pin_str_ctrl',
    'so_pin_str_ctrl',
    'sclk_pin_str_ctrl',
    'so_pin_str_ctrl2',
    'flash_led_pin_sharing_ctrl',
    'sd_clk_pull_up_ctrl',
    'xd_r_b_n_pull_up_ctrl',
    'gpio0_sd_bus_pow_ctrl',
    'sd_bus_pow_led_ctrl',
    'sd_led_output_mode_ctrl',
    'sd_bus_pow_output_pol_ctrl',
    'sd_write_protect_pol_ctrl',
    'sd_mmc_card_detect_pol_ctrl',
    'mem_stk_ins_pol_ctrl',
    'xd_picture_card_det_pol_ctrl',
]
struct_grc_secfg_1._fields_ = [
    ('cr_vddio_30v_reg_out_adj', u32, 4),
    ('cr_vddio_18v_reg_out_adj', u32, 4),
    ('si_eedata_pin_str_ctrl', u32, 3),
    ('so_pin_str_ctrl', u32, 3),
    ('sclk_pin_str_ctrl', u32, 3),
    ('so_pin_str_ctrl2', u32, 3),
    ('flash_led_pin_sharing_ctrl', u32, 1),
    ('sd_clk_pull_up_ctrl', u32, 1),
    ('xd_r_b_n_pull_up_ctrl', u32, 1),
    ('gpio0_sd_bus_pow_ctrl', u32, 1),
    ('sd_bus_pow_led_ctrl', u32, 1),
    ('sd_led_output_mode_ctrl', u32, 2),
    ('sd_bus_pow_output_pol_ctrl', u32, 1),
    ('sd_write_protect_pol_ctrl', u32, 1),
    ('sd_mmc_card_detect_pol_ctrl', u32, 1),
    ('mem_stk_ins_pol_ctrl', u32, 1),
    ('xd_picture_card_det_pol_ctrl', u32, 1),
]

# /home/saul/thundergate/include/grc.h: 235
class struct_grc_secfg_2(Structure):
    pass

struct_grc_secfg_2.__slots__ = [
    'reserved',
    'sd_write_prot_int_pu_pd_ovrd_ctrl',
    'reserved2',
    'mem_stk_ins_int_pu_pd_ovrd_ctrl',
    'xd_picture_card_det_pu_pd_ovrd_ctrl',
]
struct_grc_secfg_2._fields_ = [
    ('reserved', u32, 24),
    ('sd_write_prot_int_pu_pd_ovrd_ctrl', u32, 2),
    ('reserved2', u32, 2),
    ('mem_stk_ins_int_pu_pd_ovrd_ctrl', u32, 2),
    ('xd_picture_card_det_pu_pd_ovrd_ctrl', u32, 2),
]

# /home/saul/thundergate/include/grc.h: 243
class struct_grc_bond_id(Structure):
    pass

struct_grc_bond_id.__slots__ = [
    'serdes_l0_exit_lat_sel',
    'umc_bg_wa',
    'uart_enable',
    'eav_disable',
    'sedata_oe_ctrl',
    'disable_auto_eeprom_reset',
    'eee_lpi_enable_hw_default',
    'pcie_gen2_mode',
    'vaux_prsnt',
    'non_cr_sku',
    'disable_gigabit',
    'disable_led_pin_sharing',
    'cr_regulator_power_down',
    'bond_id',
]
struct_grc_bond_id._fields_ = [
    ('serdes_l0_exit_lat_sel', u32, 2),
    ('umc_bg_wa', u32, 1),
    ('uart_enable', u32, 1),
    ('eav_disable', u32, 1),
    ('sedata_oe_ctrl', u32, 1),
    ('disable_auto_eeprom_reset', u32, 1),
    ('eee_lpi_enable_hw_default', u32, 1),
    ('pcie_gen2_mode', u32, 1),
    ('vaux_prsnt', u32, 2),
    ('non_cr_sku', u32, 1),
    ('disable_gigabit', u32, 1),
    ('disable_led_pin_sharing', u32, 1),
    ('cr_regulator_power_down', u32, 1),
    ('bond_id', u32, 17),
]

# /home/saul/thundergate/include/grc.h: 260
class struct_grc_clock_ctrl(Structure):
    pass

struct_grc_clock_ctrl.__slots__ = [
    'pl_clock_disable',
    'dll_clock_disable',
    'tl_clock_disable',
    'pci_express_clock_to_core_clock',
    'reserved1',
    'reserved2',
    'reserved3',
    'reserved4',
    'reserved5',
    'reserved6',
    'reserved7',
    'select_final_alt_clock_src',
    'slow_core_clock_mode',
    'led_polarity',
    'bist_function_ctrl',
    'asynchronous_bist_reset',
    'reserved8',
    'select_alt_clock_src',
    'select_alt_clock',
    'reserved9',
    'core_clock_disable',
    'reserved10',
    'reserved11',
    'reserved12',
    'reserved13',
]
struct_grc_clock_ctrl._fields_ = [
    ('pl_clock_disable', u32, 1),
    ('dll_clock_disable', u32, 1),
    ('tl_clock_disable', u32, 1),
    ('pci_express_clock_to_core_clock', u32, 1),
    ('reserved1', u32, 1),
    ('reserved2', u32, 1),
    ('reserved3', u32, 1),
    ('reserved4', u32, 1),
    ('reserved5', u32, 1),
    ('reserved6', u32, 1),
    ('reserved7', u32, 1),
    ('select_final_alt_clock_src', u32, 1),
    ('slow_core_clock_mode', u32, 1),
    ('led_polarity', u32, 1),
    ('bist_function_ctrl', u32, 1),
    ('asynchronous_bist_reset', u32, 1),
    ('reserved8', u32, 2),
    ('select_alt_clock_src', u32, 1),
    ('select_alt_clock', u32, 1),
    ('reserved9', u32, 2),
    ('core_clock_disable', u32, 1),
    ('reserved10', u32, 1),
    ('reserved11', u32, 1),
    ('reserved12', u32, 2),
    ('reserved13', u32, 5),
]

# /home/saul/thundergate/include/grc.h: 288
class struct_grc_misc_control(Structure):
    pass

struct_grc_misc_control.__slots__ = [
    'done_dr_fix4_en',
    'done_dr_fix3_en',
    'done_dr_fix2_en',
    'done_dr_fix_en',
    'clkreq_delay_dis',
    'lcrc_dr_fix2_en',
    'lcrc_dr_fix_en',
    'chksum_fix_en',
    'ma_addr_fix_en',
    'ma_prior_en',
    'underrun_fix_en',
    'underrun_clear',
    'overrun_clear',
    'reserved0',
]
struct_grc_misc_control._fields_ = [
    ('done_dr_fix4_en', u32, 1),
    ('done_dr_fix3_en', u32, 1),
    ('done_dr_fix2_en', u32, 1),
    ('done_dr_fix_en', u32, 1),
    ('clkreq_delay_dis', u32, 1),
    ('lcrc_dr_fix2_en', u32, 1),
    ('lcrc_dr_fix_en', u32, 1),
    ('chksum_fix_en', u32, 1),
    ('ma_addr_fix_en', u32, 1),
    ('ma_prior_en', u32, 1),
    ('underrun_fix_en', u32, 1),
    ('underrun_clear', u32, 1),
    ('overrun_clear', u32, 1),
    ('reserved0', u32, 19),
]

# /home/saul/thundergate/include/grc.h: 305
class struct_grc_fastboot_program_counter(Structure):
    pass

# /home/saul/thundergate/include/grc.h: 315
class struct_grc_power_management_debug(Structure):
    pass

struct_grc_power_management_debug.__slots__ = [
    'pclk_sw_force_override_en',
    'pclk_sw_force_override_val',
    'pclk_sw_sel_override_en',
    'pclk_sw_sel_override_val',
    'pclk_sw_force_cond_a_dis',
    'pclk_sw_force_cond_b_dis',
    'pclk_sw_force_cond_c_en',
    'pclk_sw_sel_cond_a_dis',
    'pclk_sw_sel_cond_b_dis',
    'pclk_sw_sel_cond_c_dis',
    'reserved17',
    'perst_override',
    'reserved6',
    'pipe_clkreq_serdes',
    'pipe_aux_power_down',
    'pll_power_down',
    'clock_req_output_stat',
    'reserved1',
    'pll_is_up',
]
struct_grc_power_management_debug._fields_ = [
    ('pclk_sw_force_override_en', u32, 1),
    ('pclk_sw_force_override_val', u32, 1),
    ('pclk_sw_sel_override_en', u32, 1),
    ('pclk_sw_sel_override_val', u32, 1),
    ('pclk_sw_force_cond_a_dis', u32, 1),
    ('pclk_sw_force_cond_b_dis', u32, 1),
    ('pclk_sw_force_cond_c_en', u32, 1),
    ('pclk_sw_sel_cond_a_dis', u32, 1),
    ('pclk_sw_sel_cond_b_dis', u32, 1),
    ('pclk_sw_sel_cond_c_dis', u32, 1),
    ('reserved17', u32, 5),
    ('perst_override', u32, 1),
    ('reserved6', u32, 10),
    ('pipe_clkreq_serdes', u32, 1),
    ('pipe_aux_power_down', u32, 1),
    ('pll_power_down', u32, 1),
    ('clock_req_output_stat', u32, 1),
    ('reserved1', u32, 1),
    ('pll_is_up', u32, 1),
]

# /home/saul/thundergate/include/grc.h: 337
class struct_grc_seeprom_addr(Structure):
    pass

struct_grc_seeprom_addr.__slots__ = [
    'not_write',
    'complete',
    'reset',
    'device_id',
    'start_access',
    'half_clock_period',
    'addr',
    'reserved0',
]
struct_grc_seeprom_addr._fields_ = [
    ('not_write', u32, 1),
    ('complete', u32, 1),
    ('reset', u32, 1),
    ('device_id', u32, 3),
    ('start_access', u32, 1),
    ('half_clock_period', u32, 9),
    ('addr', u32, 14),
    ('reserved0', u32, 2),
]

# /home/saul/thundergate/include/grc.h: 348
class struct_grc_seeprom_ctrl(Structure):
    pass

struct_grc_seeprom_ctrl.__slots__ = [
    'reserved6',
    'data_input',
    'data_output',
    'data_output_tristate',
    'clock_input',
    'clock_output',
    'clock_output_tristate',
]
struct_grc_seeprom_ctrl._fields_ = [
    ('reserved6', u32, 26),
    ('data_input', u32, 1),
    ('data_output', u32, 1),
    ('data_output_tristate', u32, 1),
    ('clock_input', u32, 1),
    ('clock_output', u32, 1),
    ('clock_output_tristate', u32, 1),
]

# /home/saul/thundergate/include/grc.h: 358
class struct_grc_mdi_ctrl(Structure):
    pass

struct_grc_mdi_ctrl.__slots__ = [
    'reserved4',
    'mdi_clk',
    'mdi_sel',
    'mdi_en',
    'mdi_data',
]
struct_grc_mdi_ctrl._fields_ = [
    ('reserved4', u32, 28),
    ('mdi_clk', u32, 1),
    ('mdi_sel', u32, 1),
    ('mdi_en', u32, 1),
    ('mdi_data', u32, 1),
]

# /home/saul/thundergate/include/grc.h: 366
class struct_grc_exp_rom_addr(Structure):
    pass

struct_grc_exp_rom_addr.__slots__ = [
    'test_bits',
    'base',
]
struct_grc_exp_rom_addr._fields_ = [
    ('test_bits', u32, 8),
    ('base', u32, 24),
]

# /home/saul/thundergate/include/grc.h: 371
class struct_grc_regs(Structure):
    pass

struct_grc_regs.__slots__ = [
    'mode',
    'misc_config',
    'misc_local_control',
    'timer',
    'rxcpu_event',
    'rxcpu_timer_reference',
    'rxcpu_semaphore',
    'pcie_misc_status',
    'card_reader_dma_read_policy',
    'card_reader_dma_write_policy',
    'ofs_28',
    'ofs_2c',
    'ofs_30',
    'ofs_34',
    'seeprom_addr',
    'seeprom_data',
    'seeprom_ctrl',
    'mdi_ctrl',
    'seeprom_delay',
    'rxcpu_event_enable',
    'ofs_50',
    'ofs_54',
    'ofs_58',
    'ofs_5c',
    'ofs_60',
    'ofs_64',
    'ofs_68',
    'ofs_6c',
    'msg_xchng_out',
    'msg_xchng_in',
    'ofs_78',
    'ofs_7c',
    'secfg1',
    'secfg2',
    'bond_id',
    'clock_ctrl',
    'misc_control',
    'fastboot_pc',
    'ofs_98',
    'ofs_9c',
    'ofs_a0',
    'power_management_debug',
    'ofs_a8',
    'ofs_ac',
    'ofs_b0',
    'ofs_b4',
    'ofs_b8',
    'ofs_bc',
    'ofs_c0',
    'ofs_c4',
    'ofs_c8',
    'ofs_cc',
    'ofs_d0',
    'ofs_d4',
    'ofs_d8',
    'ofs_dc',
    'ofs_e0',
    'ofs_e4',
    'ofs_e8',
    'exp_rom_addr',
    'ofs_ec',
    'ofs_f0',
    'ofs_f4',
    'ofs_f8',
    'ofs_fc',
]
struct_grc_regs._fields_ = [
    ('mode', struct_grc_mode),
    ('misc_config', struct_grc_misc_config),
    ('misc_local_control', struct_grc_misc_local_control),
    ('timer', u32),
    ('rxcpu_event', struct_grc_cpu_event),
    ('rxcpu_timer_reference', u32),
    ('rxcpu_semaphore', struct_grc_cpu_semaphore),
    ('pcie_misc_status', struct_grc_pcie_misc_status),
    ('card_reader_dma_read_policy', u32),
    ('card_reader_dma_write_policy', u32),
    ('ofs_28', u32),
    ('ofs_2c', u32),
    ('ofs_30', u32),
    ('ofs_34', u32),
    ('seeprom_addr', struct_grc_seeprom_addr),
    ('seeprom_data', u32),
    ('seeprom_ctrl', struct_grc_seeprom_ctrl),
    ('mdi_ctrl', struct_grc_mdi_ctrl),
    ('seeprom_delay', u32),
    ('rxcpu_event_enable', struct_grc_cpu_event_enable),
    ('ofs_50', u32),
    ('ofs_54', u32),
    ('ofs_58', u32),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('ofs_6c', u32),
    ('msg_xchng_out', u32),
    ('msg_xchng_in', u32),
    ('ofs_78', u32),
    ('ofs_7c', u32),
    ('secfg1', struct_grc_secfg_1),
    ('secfg2', struct_grc_secfg_2),
    ('bond_id', struct_grc_bond_id),
    ('clock_ctrl', struct_grc_clock_ctrl),
    ('misc_control', struct_grc_misc_control),
    ('fastboot_pc', struct_grc_fastboot_program_counter),
    ('ofs_98', u32),
    ('ofs_9c', u32),
    ('ofs_a0', u32),
    ('power_management_debug', struct_grc_power_management_debug),
    ('ofs_a8', u32),
    ('ofs_ac', u32),
    ('ofs_b0', u32),
    ('ofs_b4', u32),
    ('ofs_b8', u32),
    ('ofs_bc', u32),
    ('ofs_c0', u32),
    ('ofs_c4', u32),
    ('ofs_c8', u32),
    ('ofs_cc', u32),
    ('ofs_d0', u32),
    ('ofs_d4', u32),
    ('ofs_d8', u32),
    ('ofs_dc', u32),
    ('ofs_e0', u32),
    ('ofs_e4', u32),
    ('ofs_e8', u32),
    ('exp_rom_addr', struct_grc_exp_rom_addr),
    ('ofs_ec', u32),
    ('ofs_f0', u32),
    ('ofs_f4', u32),
    ('ofs_f8', u32),
    ('ofs_fc', u32),
]

# /home/saul/thundergate/include/hc.h: 24
class struct_hc_mode(Structure):
    pass

struct_hc_mode.__slots__ = [
    'during_int_frame_cntr_fix_disable',
    'end_of_rx_stream_detector_fires_all_msix',
    'end_of_rx_stream_int',
    'enable_attn_int_fix',
    'reserved',
    'coalesce_now_1_5',
    'no_int_on_force_update',
    'no_int_on_dmad_force',
    'reserved2',
    'clear_ticks_mode_on_rx',
    'status_block_size',
    'msi_bits',
    'coalesce_now',
    'attn_enable',
    'enable',
    'reset',
]
struct_hc_mode._fields_ = [
    ('during_int_frame_cntr_fix_disable', u32, 1),
    ('end_of_rx_stream_detector_fires_all_msix', u32, 1),
    ('end_of_rx_stream_int', u32, 1),
    ('enable_attn_int_fix', u32, 1),
    ('reserved', u32, 10),
    ('coalesce_now_1_5', u32, 5),
    ('no_int_on_force_update', u32, 1),
    ('no_int_on_dmad_force', u32, 1),
    ('reserved2', u32, 1),
    ('clear_ticks_mode_on_rx', u32, 1),
    ('status_block_size', u32, 2),
    ('msi_bits', u32, 3),
    ('coalesce_now', u32, 1),
    ('attn_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/hc.h: 43
class struct_hc_status(Structure):
    pass

struct_hc_status.__slots__ = [
    'reserved',
    'error',
    'reserved2',
]
struct_hc_status._fields_ = [
    ('reserved', u32, 29),
    ('error', u32, 1),
    ('reserved2', u32, 2),
]

# /home/saul/thundergate/include/hc.h: 49
class struct_hc_flow_attention(Structure):
    pass

struct_hc_flow_attention.__slots__ = [
    'sbdi',
    'sbdc',
    'sbdrs',
    'sdi',
    'sdc',
    'reserved',
    'rbdi',
    'rbdc',
    'rlp',
    'rls',
    'rdi',
    'rdc',
    'rcb_incorrect',
    'dmac_discard',
    'hc',
    'reserved2',
    'ma',
    'mbuf_low_water',
    'reserved3',
]
struct_hc_flow_attention._fields_ = [
    ('sbdi', u32, 1),
    ('sbdc', u32, 1),
    ('sbdrs', u32, 1),
    ('sdi', u32, 1),
    ('sdc', u32, 1),
    ('reserved', u32, 3),
    ('rbdi', u32, 1),
    ('rbdc', u32, 1),
    ('rlp', u32, 1),
    ('rls', u32, 1),
    ('rdi', u32, 1),
    ('rdc', u32, 1),
    ('rcb_incorrect', u32, 1),
    ('dmac_discard', u32, 1),
    ('hc', u32, 1),
    ('reserved2', u32, 7),
    ('ma', u32, 1),
    ('mbuf_low_water', u32, 1),
    ('reserved3', u32, 6),
]

# /home/saul/thundergate/include/hc.h: 71
class struct_hc_regs(Structure):
    pass

struct_hc_regs.__slots__ = [
    'mode',
    'status',
    'rx_coal_ticks',
    'tx_coal_ticks',
    'rx_max_coal_bds',
    'tx_max_coal_bds',
    'ofs_18',
    'ofs_1c',
    'rx_max_coal_bds_in_int',
    'tx_max_coal_bds_in_int',
    'ofs_28',
    'ofs_2c',
    'ofs_30',
    'ofs_34',
    'status_block_host_addr_hi',
    'status_block_host_addr_low',
    'ofs_40',
    'status_block_nic_addr',
    'flow_attention',
    'ofs_4c',
    'nic_jumbo_rbd_ci',
    'nic_std_rbd_ci',
    'nic_mini_rbd_ci',
    'ofs_5c',
    'ofs_60',
    'ofs_64',
    'ofs_68',
    'ofs_6c',
    'ofs_70',
    'ofs_74',
    'ofs_78',
    'ofs_7c',
    'nic_diag_rr_pi',
    'nic_diag_sbd_ci',
]
struct_hc_regs._fields_ = [
    ('mode', struct_hc_mode),
    ('status', struct_hc_status),
    ('rx_coal_ticks', u32),
    ('tx_coal_ticks', u32),
    ('rx_max_coal_bds', u32),
    ('tx_max_coal_bds', u32),
    ('ofs_18', u32),
    ('ofs_1c', u32),
    ('rx_max_coal_bds_in_int', u32),
    ('tx_max_coal_bds_in_int', u32),
    ('ofs_28', u32),
    ('ofs_2c', u32),
    ('ofs_30', u32),
    ('ofs_34', u32),
    ('status_block_host_addr_hi', u32),
    ('status_block_host_addr_low', u32),
    ('ofs_40', u32),
    ('status_block_nic_addr', u32),
    ('flow_attention', struct_hc_flow_attention),
    ('ofs_4c', u32),
    ('nic_jumbo_rbd_ci', u32),
    ('nic_std_rbd_ci', u32),
    ('nic_mini_rbd_ci', u32),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('ofs_6c', u32),
    ('ofs_70', u32),
    ('ofs_74', u32),
    ('ofs_78', u32),
    ('ofs_7c', u32),
    ('nic_diag_rr_pi', u32 * 16),
    ('nic_diag_sbd_ci', u32 * 16),
]

# /home/saul/thundergate/include/ma.h: 22
class struct_ma_mode(Structure):
    pass

# /home/saul/thundergate/include/ma.h: 64
class struct_ma_status(Structure):
    pass

struct_ma_status.__slots__ = [
    'reserved',
    'dmaw2_addr_trap',
    'reserved2',
    'sdi_addr_trap',
    'reserved3',
    'rdi2_addr_trap',
    'rdi1_addr_trap',
    'rq_addr_trap',
    'reserved4',
    'pci_addr_trap',
    'reserved5',
    'rx_risc_addr_trap',
    'dmar1_addr_trap',
    'dmaw1_addr_trap',
    'rx_mac_addr_trap',
    'tx_mac_addr_trap',
    'reserved6',
]
struct_ma_status._fields_ = [
    ('reserved', u32, 11),
    ('dmaw2_addr_trap', u32, 1),
    ('reserved2', u32, 3),
    ('sdi_addr_trap', u32, 1),
    ('reserved3', u32, 3),
    ('rdi2_addr_trap', u32, 1),
    ('rdi1_addr_trap', u32, 1),
    ('rq_addr_trap', u32, 1),
    ('reserved4', u32, 1),
    ('pci_addr_trap', u32, 1),
    ('reserved5', u32, 1),
    ('rx_risc_addr_trap', u32, 1),
    ('dmar1_addr_trap', u32, 1),
    ('dmaw1_addr_trap', u32, 1),
    ('rx_mac_addr_trap', u32, 1),
    ('tx_mac_addr_trap', u32, 1),
    ('reserved6', u32, 2),
]

# /home/saul/thundergate/include/ma.h: 85
class struct_ma_regs(Structure):
    pass

struct_ma_regs.__slots__ = [
    'mode',
    'status',
    'trap_addr_low',
    'trap_addr_hi',
]
struct_ma_regs._fields_ = [
    ('mode', struct_ma_mode),
    ('status', struct_ma_status),
    ('trap_addr_low', u32),
    ('trap_addr_hi', u32),
]

enum_known_mailboxes = c_int # /home/saul/thundergate/include/mbox.h: 22

mb_interrupt = 0 # /home/saul/thundergate/include/mbox.h: 22

mb_rbd_standard_producer = (104 / 8) # /home/saul/thundergate/include/mbox.h: 22

mb_rbd_rr0_consumer = (128 / 8) # /home/saul/thundergate/include/mbox.h: 22

mb_rbd_rr1_consumer = (136 / 8) # /home/saul/thundergate/include/mbox.h: 22

mb_rbd_rr2_consumer = (144 / 8) # /home/saul/thundergate/include/mbox.h: 22

mb_rbd_rr3_consumer = (152 / 8) # /home/saul/thundergate/include/mbox.h: 22

mb_sbd_host_producer = (256 / 8) # /home/saul/thundergate/include/mbox.h: 22

mb_sbd_nic_producer = (896 / 8) # /home/saul/thundergate/include/mbox.h: 22

# /home/saul/thundergate/include/mbox.h: 33
class struct_mailbox(Structure):
    pass

struct_mailbox.__slots__ = [
    'hi',
    'low',
]
struct_mailbox._fields_ = [
    ('hi', u32),
    ('low', u32),
]

# /home/saul/thundergate/include/mbox.h: 38
class struct_hpmb_regs(Structure):
    pass

struct_hpmb_regs.__slots__ = [
    'box',
]
struct_hpmb_regs._fields_ = [
    ('box', struct_mailbox * (512 / 8)),
]

# /home/saul/thundergate/include/mbox.h: 42
class struct_lpmb_regs(Structure):
    pass

struct_lpmb_regs.__slots__ = [
    'box',
]
struct_lpmb_regs._fields_ = [
    ('box', struct_mailbox * (512 / 8)),
]

# /home/saul/thundergate/include/mbuf.h: 24
class struct_mbuf_hdr(Structure):
    pass

struct_mbuf_hdr.__slots__ = [
    'length',
    'next_mbuf',
    'reserved',
    'f',
    'c',
]
struct_mbuf_hdr._fields_ = [
    ('length', u32, 7),
    ('next_mbuf', u32, 16),
    ('reserved', u32, 7),
    ('f', u32, 1),
    ('c', u32, 1),
]

# /home/saul/thundergate/include/mbuf.h: 42
class struct_mbuf_frame_desc(Structure):
    pass

struct_mbuf_frame_desc.__slots__ = [
    'status_ctrl',
    'len',
    'reserved',
    'qids',
    'tcp_udp_hdr_start',
    'ip_hdr_start',
    'vlan_id',
    'data_start',
    'tcp_udp_checksum',
    'ip_checksum',
    'checksum_status',
    'pseudo_checksum',
    'rupt',
    'rule_class',
    'rule_match',
    'mbuf',
    'reserved2',
    'reserved3',
    'reserved4',
]
struct_mbuf_frame_desc._fields_ = [
    ('status_ctrl', u32),
    ('len', u16),
    ('reserved', u8),
    ('qids', u8),
    ('tcp_udp_hdr_start', u16),
    ('ip_hdr_start', u16),
    ('vlan_id', u16),
    ('data_start', u16),
    ('tcp_udp_checksum', u16),
    ('ip_checksum', u16),
    ('checksum_status', u16),
    ('pseudo_checksum', u16),
    ('rupt', u8),
    ('rule_class', u8),
    ('rule_match', u16),
    ('mbuf', u16),
    ('reserved2', u16),
    ('reserved3', u32),
    ('reserved4', u32),
]

# /home/saul/thundergate/include/mbuf.h: 102
class union_anon_3(Union):
    pass

union_anon_3.__slots__ = [
    'frame',
    'word',
    'byte',
]
union_anon_3._fields_ = [
    ('frame', struct_mbuf_frame_desc),
    ('word', u32 * 30),
    ('byte', u8 * 120),
]

# /home/saul/thundergate/include/mbuf.h: 99
class struct_mbuf(Structure):
    pass

struct_mbuf.__slots__ = [
    'hdr',
    'next_frame_ptr',
    'data',
]
struct_mbuf._fields_ = [
    ('hdr', struct_mbuf_hdr),
    ('next_frame_ptr', u32),
    ('data', union_anon_3),
]

# /home/saul/thundergate/include/msi.h: 22
class struct_msi_mode(Structure):
    pass

struct_msi_mode.__slots__ = [
    'priority',
    'msix_fix_pcie_client',
    'reserved',
    'msi_message',
    'msix_multi_vector_mode',
    'msi_byte_swap_enable',
    'msi_single_shot_disable',
    'pci_parity_error_attn',
    'pci_master_abort_attn',
    'pci_target_abort_attn',
    'enable',
    'reset',
]
struct_msi_mode._fields_ = [
    ('priority', u32, 2),
    ('msix_fix_pcie_client', u32, 1),
    ('reserved', u32, 18),
    ('msi_message', u32, 3),
    ('msix_multi_vector_mode', u32, 1),
    ('msi_byte_swap_enable', u32, 1),
    ('msi_single_shot_disable', u32, 1),
    ('pci_parity_error_attn', u32, 1),
    ('pci_master_abort_attn', u32, 1),
    ('pci_target_abort_attn', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/msi.h: 37
class struct_msi_status(Structure):
    pass

struct_msi_status.__slots__ = [
    'reserved',
    'pci_parity_error',
    'pci_master_abort',
    'pci_target_abort',
    'reserved2',
    'msi_pci_request',
]
struct_msi_status._fields_ = [
    ('reserved', u32, 27),
    ('pci_parity_error', u32, 1),
    ('pci_master_abort', u32, 1),
    ('pci_target_abort', u32, 1),
    ('reserved2', u32, 1),
    ('msi_pci_request', u32, 1),
]

# /home/saul/thundergate/include/msi.h: 46
class struct_msi_regs(Structure):
    pass

struct_msi_regs.__slots__ = [
    'mode',
    'status',
]
struct_msi_regs._fields_ = [
    ('mode', struct_msi_mode),
    ('status', struct_msi_status),
]

# /home/saul/thundergate/include/nrdma.h: 24
class struct_nrdma_mode(Structure):
    pass

struct_nrdma_mode.__slots__ = [
    'reserved26',
    'addr_oflow_err_log_en',
    'reserved18',
    'pci_req_burst_len',
    'reserved14',
    'attn_ens',
    'enable',
    'reset',
]
struct_nrdma_mode._fields_ = [
    ('reserved26', u32, 6),
    ('addr_oflow_err_log_en', u32, 1),
    ('reserved18', u32, 7),
    ('pci_req_burst_len', u32, 2),
    ('reserved14', u32, 2),
    ('attn_ens', u32, 12),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/nrdma.h: 35
class struct_nrdma_status(Structure):
    pass

struct_nrdma_status.__slots__ = [
    'reserved11',
    'malformed_or_poison_tlp_err_det',
    'rdma_local_mem_wr_longer_than_dma_len_err',
    'rdma_pci_fifo_oflow_err',
    'rdma_pci_fifo_urun_err',
    'rdma_pci_fifo_orun_err',
    'rdma_pci_host_addr_oflow_err',
    'dma_rd_comp_to',
    'comp_abort_err',
    'unsupp_req_err_det',
    'reserved0',
]
struct_nrdma_status._fields_ = [
    ('reserved11', u32, 21),
    ('malformed_or_poison_tlp_err_det', u32, 1),
    ('rdma_local_mem_wr_longer_than_dma_len_err', u32, 1),
    ('rdma_pci_fifo_oflow_err', u32, 1),
    ('rdma_pci_fifo_urun_err', u32, 1),
    ('rdma_pci_fifo_orun_err', u32, 1),
    ('rdma_pci_host_addr_oflow_err', u32, 1),
    ('dma_rd_comp_to', u32, 1),
    ('comp_abort_err', u32, 1),
    ('unsupp_req_err_det', u32, 1),
    ('reserved0', u32, 2),
]

# /home/saul/thundergate/include/nrdma.h: 49
class struct_nrdma_programmable_ipv6_extension_header(Structure):
    pass

struct_nrdma_programmable_ipv6_extension_header.__slots__ = [
    'hdr_type2_en',
    'hdr_type1_en',
    'reserved16',
    'hdr_type2',
    'hdr_type1',
]
struct_nrdma_programmable_ipv6_extension_header._fields_ = [
    ('hdr_type2_en', u32, 1),
    ('hdr_type1_en', u32, 1),
    ('reserved16', u32, 14),
    ('hdr_type2', u32, 8),
    ('hdr_type1', u32, 8),
]

# /home/saul/thundergate/include/nrdma.h: 57
class struct_nrdma_rstates_debug(Structure):
    pass

struct_nrdma_rstates_debug.__slots__ = [
    'reserved11',
    'sdi_dr_wr',
    'dr_sdi_wr_ack',
    'non_lso_sel',
    'non_lso_q_full',
    'non_lso_busy',
    'rstate3',
    'reserved3',
    'rstate1',
]
struct_nrdma_rstates_debug._fields_ = [
    ('reserved11', u32, 21),
    ('sdi_dr_wr', u32, 1),
    ('dr_sdi_wr_ack', u32, 1),
    ('non_lso_sel', u32, 1),
    ('non_lso_q_full', u32, 1),
    ('non_lso_busy', u32, 1),
    ('rstate3', u32, 2),
    ('reserved3', u32, 1),
    ('rstate1', u32, 3),
]

# /home/saul/thundergate/include/nrdma.h: 69
class struct_nrdma_rstate2_debug(Structure):
    pass

struct_nrdma_rstate2_debug.__slots__ = [
    'reserved5',
    'rstate2',
]
struct_nrdma_rstate2_debug._fields_ = [
    ('reserved5', u32, 27),
    ('rstate2', u32, 5),
]

# /home/saul/thundergate/include/nrdma.h: 74
class struct_nrdma_bd_status_debug(Structure):
    pass

struct_nrdma_bd_status_debug.__slots__ = [
    'reserved3',
    'bd_non_mbuf',
    'fst_bd_mbuf',
    'lst_bd_mbuf',
]
struct_nrdma_bd_status_debug._fields_ = [
    ('reserved3', u32, 29),
    ('bd_non_mbuf', u32, 1),
    ('fst_bd_mbuf', u32, 1),
    ('lst_bd_mbuf', u32, 1),
]

# /home/saul/thundergate/include/nrdma.h: 81
class struct_nrdma_req_ptr_debug(Structure):
    pass

struct_nrdma_req_ptr_debug.__slots__ = [
    'ih_dmad_length',
    'reserved13',
    'txmbuf_left',
    'rh_dmad_load_en',
    'rftq_d_dmad_pnt',
    'reserved0',
]
struct_nrdma_req_ptr_debug._fields_ = [
    ('ih_dmad_length', u32, 16),
    ('reserved13', u32, 3),
    ('txmbuf_left', u32, 8),
    ('rh_dmad_load_en', u32, 1),
    ('rftq_d_dmad_pnt', u32, 2),
    ('reserved0', u32, 2),
]

# /home/saul/thundergate/include/nrdma.h: 90
class struct_nrdma_hold_d_dmad_debug(Structure):
    pass

struct_nrdma_hold_d_dmad_debug.__slots__ = [
    'reserved2',
    'rhold_d_dmad',
]
struct_nrdma_hold_d_dmad_debug._fields_ = [
    ('reserved2', u32, 30),
    ('rhold_d_dmad', u32, 2),
]

# /home/saul/thundergate/include/nrdma.h: 95
class struct_nrdma_length_and_address_debug(Structure):
    pass

struct_nrdma_length_and_address_debug.__slots__ = [
    'rdma_rd_length',
    'reserved6',
    'mbuf_addr_idx',
]
struct_nrdma_length_and_address_debug._fields_ = [
    ('rdma_rd_length', u32, 16),
    ('reserved6', u32, 10),
    ('mbuf_addr_idx', u32, 6),
]

# /home/saul/thundergate/include/nrdma.h: 101
class struct_nrdma_mbuf_byte_count_debug(Structure):
    pass

struct_nrdma_mbuf_byte_count_debug.__slots__ = [
    'reserved4',
    'rmbuf_byte_cnt',
]
struct_nrdma_mbuf_byte_count_debug._fields_ = [
    ('reserved4', u32, 28),
    ('rmbuf_byte_cnt', u32, 4),
]

# /home/saul/thundergate/include/nrdma.h: 106
class struct_nrdma_pcie_debug_status(Structure):
    pass

struct_nrdma_pcie_debug_status.__slots__ = [
    'lt_term',
    'reserved27',
    'lt_too_lg',
    'lt_dma_reload',
    'lt_dma_good',
    'cur_trans_active',
    'drpcireq',
    'dr_pci_word_swap',
    'dr_pci_byte_swap',
    'new_slow_core_clk_mode',
    'rbd_non_mbuf',
    'rfst_bd_mbuf',
    'rlst_bd_mbuf',
    'dr_pci_len',
]
struct_nrdma_pcie_debug_status._fields_ = [
    ('lt_term', u32, 4),
    ('reserved27', u32, 1),
    ('lt_too_lg', u32, 1),
    ('lt_dma_reload', u32, 1),
    ('lt_dma_good', u32, 1),
    ('cur_trans_active', u32, 1),
    ('drpcireq', u32, 1),
    ('dr_pci_word_swap', u32, 1),
    ('dr_pci_byte_swap', u32, 1),
    ('new_slow_core_clk_mode', u32, 1),
    ('rbd_non_mbuf', u32, 1),
    ('rfst_bd_mbuf', u32, 1),
    ('rlst_bd_mbuf', u32, 1),
    ('dr_pci_len', u32, 16),
]

# /home/saul/thundergate/include/nrdma.h: 123
class struct_nrdma_pcie_dma_read_req_debug(Structure):
    pass

struct_nrdma_pcie_dma_read_req_debug.__slots__ = [
    'dr_pci_ad_hi',
    'dr_pci_ad_lo',
]
struct_nrdma_pcie_dma_read_req_debug._fields_ = [
    ('dr_pci_ad_hi', u32, 16),
    ('dr_pci_ad_lo', u32, 16),
]

# /home/saul/thundergate/include/nrdma.h: 128
class struct_nrdma_pcie_dma_req_length_debug(Structure):
    pass

struct_nrdma_pcie_dma_req_length_debug.__slots__ = [
    'reserved16',
    'rdma_len',
]
struct_nrdma_pcie_dma_req_length_debug._fields_ = [
    ('reserved16', u32, 16),
    ('rdma_len', u32, 16),
]

# /home/saul/thundergate/include/nrdma.h: 133
class struct_nrdma_fifo1_debug(Structure):
    pass

struct_nrdma_fifo1_debug.__slots__ = [
    'reserved9',
    'c_write_addr',
]
struct_nrdma_fifo1_debug._fields_ = [
    ('reserved9', u32, 23),
    ('c_write_addr', u32, 9),
]

# /home/saul/thundergate/include/nrdma.h: 138
class struct_nrdma_fifo2_debug(Structure):
    pass

struct_nrdma_fifo2_debug.__slots__ = [
    'reserved18',
    'rlctrl_in',
    'c_read_addr',
]
struct_nrdma_fifo2_debug._fields_ = [
    ('reserved18', u32, 14),
    ('rlctrl_in', u32, 9),
    ('c_read_addr', u32, 9),
]

# /home/saul/thundergate/include/nrdma.h: 144
class struct_nrdma_post_proc_pkt_req_cnt(Structure):
    pass

struct_nrdma_post_proc_pkt_req_cnt.__slots__ = [
    'reserved8',
    'pkt_req_cnt',
]
struct_nrdma_post_proc_pkt_req_cnt._fields_ = [
    ('reserved8', u32, 24),
    ('pkt_req_cnt', u32, 8),
]

# /home/saul/thundergate/include/nrdma.h: 149
class struct_nrdma_mbuf_addr_debug(Structure):
    pass

struct_nrdma_mbuf_addr_debug.__slots__ = [
    'reserved26',
    'mactq_full',
    'txfifo_almost_urun',
    'tde_fifo_entry',
    'rcmp_head',
]
struct_nrdma_mbuf_addr_debug._fields_ = [
    ('reserved26', u32, 6),
    ('mactq_full', u32, 1),
    ('txfifo_almost_urun', u32, 1),
    ('tde_fifo_entry', u32, 8),
    ('rcmp_head', u32, 16),
]

# /home/saul/thundergate/include/nrdma.h: 157
class struct_nrdma_tce_debug1(Structure):
    pass

struct_nrdma_tce_debug1.__slots__ = [
    'odi_state_out',
    'odi_state_in',
    'fifo_odi_data_code',
    'fifo_odi_data',
]
struct_nrdma_tce_debug1._fields_ = [
    ('odi_state_out', u32, 4),
    ('odi_state_in', u32, 4),
    ('fifo_odi_data_code', u32, 2),
    ('fifo_odi_data', u32, 22),
]

# /home/saul/thundergate/include/nrdma.h: 164
class struct_nrdma_tce_debug2(Structure):
    pass

struct_nrdma_tce_debug2.__slots__ = [
    'det_abort_cnt',
    'reserved0',
]
struct_nrdma_tce_debug2._fields_ = [
    ('det_abort_cnt', u32, 8),
    ('reserved0', u32, 24),
]

# /home/saul/thundergate/include/nrdma.h: 169
class struct_nrdma_tce_debug3(Structure):
    pass

struct_nrdma_tce_debug3.__slots__ = [
    'reserved28',
    'tx_pkt_cnt',
    'reserved17',
    'tce_ma_req',
    'tce_ma_cmd_len',
    'reserved0',
]
struct_nrdma_tce_debug3._fields_ = [
    ('reserved28', u32, 4),
    ('tx_pkt_cnt', u32, 8),
    ('reserved17', u32, 2),
    ('tce_ma_req', u32, 1),
    ('tce_ma_cmd_len', u32, 3),
    ('reserved0', u32, 12),
]

# /home/saul/thundergate/include/nrdma.h: 178
class struct_nrdma_reserved_control(Structure):
    pass

struct_nrdma_reserved_control.__slots__ = [
    'txmbuf_margin_nlso',
    'reserved20',
    'fifo_high_mark',
    'fifo_low_mark',
    'slow_clock_fix_dis',
    'en_hw_fix_25155',
    'reserved1',
    'select_fed_enable',
]
struct_nrdma_reserved_control._fields_ = [
    ('txmbuf_margin_nlso', u32, 11),
    ('reserved20', u32, 1),
    ('fifo_high_mark', u32, 8),
    ('fifo_low_mark', u32, 8),
    ('slow_clock_fix_dis', u32, 1),
    ('en_hw_fix_25155', u32, 1),
    ('reserved1', u32, 1),
    ('select_fed_enable', u32, 1),
]

# /home/saul/thundergate/include/nrdma.h: 189
class struct_nrdma_flow_reserved_control(Structure):
    pass

struct_nrdma_flow_reserved_control.__slots__ = [
    'reserved24',
    'fifo_threshold_mbuf_req_msb',
    'mbuf_threshold_mbuf_req',
    'reserved4',
    'fifo_hi_mark',
    'fifo_lo_mark',
    'reserved1',
    'fifo_threshold_mbuf_req_lmsb',
]
struct_nrdma_flow_reserved_control._fields_ = [
    ('reserved24', u32, 8),
    ('fifo_threshold_mbuf_req_msb', u32, 8),
    ('mbuf_threshold_mbuf_req', u32, 8),
    ('reserved4', u32, 4),
    ('fifo_hi_mark', u32, 1),
    ('fifo_lo_mark', u32, 1),
    ('reserved1', u32, 1),
    ('fifo_threshold_mbuf_req_lmsb', u32, 1),
]

# /home/saul/thundergate/include/nrdma.h: 200
class struct_nrdma_corruption_enable_control(Structure):
    pass

struct_nrdma_corruption_enable_control.__slots__ = [
    'lcrc_dr_fix_en',
    'new_length_fix_en',
    'reserved22',
    'cq51816_nlso_fix_en',
    'cq51036_nlso_fix_en',
    'reserved15',
    'sbd_8b_less_fix_en3',
    'sbd_8b_less_fix_en2',
    'mem_too_large_fix_en2',
    'mem_too_large_fix_en1',
    'mem_too_large_fix_en',
    'sbd_9b_less_fix_en_fast_return',
    'sbd_9b_less_fix_en',
    'cq35774_hw_fix_en',
    'reserved',
]
struct_nrdma_corruption_enable_control._fields_ = [
    ('lcrc_dr_fix_en', u32, 1),
    ('new_length_fix_en', u32, 1),
    ('reserved22', u32, 8),
    ('cq51816_nlso_fix_en', u32, 1),
    ('cq51036_nlso_fix_en', u32, 1),
    ('reserved15', u32, 5),
    ('sbd_8b_less_fix_en3', u32, 1),
    ('sbd_8b_less_fix_en2', u32, 1),
    ('mem_too_large_fix_en2', u32, 1),
    ('mem_too_large_fix_en1', u32, 1),
    ('mem_too_large_fix_en', u32, 1),
    ('sbd_9b_less_fix_en_fast_return', u32, 1),
    ('sbd_9b_less_fix_en', u32, 1),
    ('cq35774_hw_fix_en', u32, 1),
    ('reserved', u32, 7),
]

# /home/saul/thundergate/include/nrdma.h: 218
class struct_nrdma_regs(Structure):
    pass

struct_nrdma_regs.__slots__ = [
    'mode',
    'status',
    'programmable_ipv6_extension_header',
    'rstates_debug',
    'rstate2_debug',
    'bd_status_debug',
    'req_ptr_debug',
    'hold_d_dmad_debug',
    'len_and_addr_debug',
    'mbuf_byte_cnt_debug',
    'pcie_debug_status',
    'pcie_dma_read_req_debug',
    'pcie_dma_req_length_debug',
    'fifo1_debug',
    'fifo2_debug',
    'ofs_3c',
    'post_proc_pkt_req_cnt',
    'ofs_44',
    'ofs_48',
    'ofs_4c',
    'ofs_50',
    'ofs_54',
    'ofs_58',
    'ofs_5c',
    'mbuf_addr_debug',
    'tce_debug1',
    'tce_debug2',
    'tce_debug3',
    'reserved_control',
    'flow_reserved_control',
    'corruption_enable_control',
]
struct_nrdma_regs._fields_ = [
    ('mode', struct_nrdma_mode),
    ('status', struct_nrdma_status),
    ('programmable_ipv6_extension_header', struct_nrdma_programmable_ipv6_extension_header),
    ('rstates_debug', struct_nrdma_rstates_debug),
    ('rstate2_debug', struct_nrdma_rstate2_debug),
    ('bd_status_debug', struct_nrdma_bd_status_debug),
    ('req_ptr_debug', struct_nrdma_req_ptr_debug),
    ('hold_d_dmad_debug', struct_nrdma_hold_d_dmad_debug),
    ('len_and_addr_debug', struct_nrdma_length_and_address_debug),
    ('mbuf_byte_cnt_debug', struct_nrdma_mbuf_byte_count_debug),
    ('pcie_debug_status', struct_nrdma_pcie_debug_status),
    ('pcie_dma_read_req_debug', struct_nrdma_pcie_dma_read_req_debug),
    ('pcie_dma_req_length_debug', struct_nrdma_pcie_dma_req_length_debug),
    ('fifo1_debug', struct_nrdma_fifo1_debug),
    ('fifo2_debug', struct_nrdma_fifo2_debug),
    ('ofs_3c', u32),
    ('post_proc_pkt_req_cnt', struct_nrdma_post_proc_pkt_req_cnt),
    ('ofs_44', u32),
    ('ofs_48', u32),
    ('ofs_4c', u32),
    ('ofs_50', u32),
    ('ofs_54', u32),
    ('ofs_58', u32),
    ('ofs_5c', u32),
    ('mbuf_addr_debug', struct_nrdma_mbuf_addr_debug),
    ('tce_debug1', struct_nrdma_tce_debug1),
    ('tce_debug2', struct_nrdma_tce_debug2),
    ('tce_debug3', struct_nrdma_tce_debug3),
    ('reserved_control', struct_nrdma_reserved_control),
    ('flow_reserved_control', struct_nrdma_flow_reserved_control),
    ('corruption_enable_control', struct_nrdma_corruption_enable_control),
]

# /home/saul/thundergate/include/nvram.h: 35
class struct_nvram_dir_item(Structure):
    pass

struct_nvram_dir_item.__slots__ = [
    'sram_start',
    'typelen',
    'nvram_start',
]
struct_nvram_dir_item._fields_ = [
    ('sram_start', u32),
    ('typelen', u32),
    ('nvram_start', u32),
]

# /home/saul/thundergate/include/nvram.h: 45
class struct_anon_4(Structure):
    pass

struct_anon_4.__slots__ = [
    'mgaic',
    'bc_sram_start',
    'bc_words',
    'bc_nvram_start',
    'crc',
]
struct_anon_4._fields_ = [
    ('mgaic', u32),
    ('bc_sram_start', u32),
    ('bc_words', u32),
    ('bc_nvram_start', u32),
    ('crc', u32),
]

# /home/saul/thundergate/include/nvram.h: 53
class struct_anon_5(Structure):
    pass

struct_anon_5.__slots__ = [
    'len',
    'dir_cksum',
    'rev',
    '_unused',
    'mac_address',
    'partno',
    'partrev',
    'bc_rev',
    'mfg_date',
    'mba_vlan_p1',
    'mba_vlan_p2',
    'pci_did',
    'pci_vid',
    'pci_ssid',
    'pci_svid',
    'cpu_mhz',
    'smbus_addr1',
    'smbus_addr0',
    'mac_backup',
    'mac_backup_p2',
    'power_dissipated',
    'power_consumed',
    'feat_cfg',
    'hw_cfg',
    'mac_address_p2',
    'feat_cfg_p2',
    'hw_cfg_p2',
    'shared_cfg',
    'power_budget_0',
    'power_budget_1',
    'serworks_use',
    'serdes_override',
    'tpm_nvram_size',
    'mac_nvram_size',
    'power_budget_2',
    'power_budget_3',
    'crc',
]
struct_anon_5._fields_ = [
    ('len', u16),
    ('dir_cksum', u8),
    ('rev', u8),
    ('_unused', u32),
    ('mac_address', u8 * 8),
    ('partno', c_char * 16),
    ('partrev', c_char * 2),
    ('bc_rev', u16),
    ('mfg_date', u8 * 4),
    ('mba_vlan_p1', u16),
    ('mba_vlan_p2', u16),
    ('pci_did', u16),
    ('pci_vid', u16),
    ('pci_ssid', u16),
    ('pci_svid', u16),
    ('cpu_mhz', u16),
    ('smbus_addr1', u8),
    ('smbus_addr0', u8),
    ('mac_backup', u8 * 8),
    ('mac_backup_p2', u8 * 8),
    ('power_dissipated', u32),
    ('power_consumed', u32),
    ('feat_cfg', u32),
    ('hw_cfg', u32),
    ('mac_address_p2', u8 * 8),
    ('feat_cfg_p2', u32),
    ('hw_cfg_p2', u32),
    ('shared_cfg', u32),
    ('power_budget_0', u32),
    ('power_budget_1', u32),
    ('serworks_use', u32),
    ('serdes_override', u32),
    ('tpm_nvram_size', u16),
    ('mac_nvram_size', u16),
    ('power_budget_2', u32),
    ('power_budget_3', u32),
    ('crc', u32),
]

# /home/saul/thundergate/include/nvram.h: 44
class struct_nvram_header(Structure):
    pass

struct_nvram_header.__slots__ = [
    'bs',
    'directory',
    'mfg',
]
struct_nvram_header._fields_ = [
    ('bs', struct_anon_4),
    ('directory', struct_nvram_dir_item * 8),
    ('mfg', struct_anon_5),
]

# /home/saul/thundergate/include/nvram.h: 95
class struct_nvram_command(Structure):
    pass

struct_nvram_command.__slots__ = [
    'policy_error',
    'atmel_page_size',
    'reserved1',
    'reserved2',
    'reserved3',
    'reserved4',
    'wrsr',
    'ewsr',
    'write_disable_command',
    'write_enable_command',
    'reserved5',
    'atmel_power_of_2_pg_sz',
    'atmel_pg_sz_rd',
    'last',
    'first',
    'erase',
    'wr',
    'doit',
    'done',
    'reserved6',
    'reset',
]
struct_nvram_command._fields_ = [
    ('policy_error', u32, 4),
    ('atmel_page_size', u32, 1),
    ('reserved1', u32, 4),
    ('reserved2', u32, 1),
    ('reserved3', u32, 1),
    ('reserved4', u32, 1),
    ('wrsr', u32, 1),
    ('ewsr', u32, 1),
    ('write_disable_command', u32, 1),
    ('write_enable_command', u32, 1),
    ('reserved5', u32, 5),
    ('atmel_power_of_2_pg_sz', u32, 1),
    ('atmel_pg_sz_rd', u32, 1),
    ('last', u32, 1),
    ('first', u32, 1),
    ('erase', u32, 1),
    ('wr', u32, 1),
    ('doit', u32, 1),
    ('done', u32, 1),
    ('reserved6', u32, 2),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/nvram.h: 119
class struct_nvram_status(Structure):
    pass

struct_nvram_status.__slots__ = [
    'reserved',
    'spi_at_read_state',
    'spi_at_write_state',
    'spi_st_read_state',
    'spi_st_write_state',
    'seq_fsm_state',
    'see_fsm_state',
]
struct_nvram_status._fields_ = [
    ('reserved', u32, 1),
    ('spi_at_read_state', u32, 5),
    ('spi_at_write_state', u32, 6),
    ('spi_st_read_state', u32, 4),
    ('spi_st_write_state', u32, 6),
    ('seq_fsm_state', u32, 4),
    ('see_fsm_state', u32, 6),
]

# /home/saul/thundergate/include/nvram.h: 129
class struct_nvram_software_arbitration(Structure):
    pass

struct_nvram_software_arbitration.__slots__ = [
    'reserved',
    'req3',
    'req2',
    'req1',
    'req0',
    'arb_won3',
    'arb_won2',
    'arb_won1',
    'arb_won0',
    'req_clr3',
    'req_clr2',
    'req_clr1',
    'req_clr0',
    'req_set3',
    'req_set2',
    'req_set1',
    'req_set0',
]
struct_nvram_software_arbitration._fields_ = [
    ('reserved', u32, 16),
    ('req3', u32, 1),
    ('req2', u32, 1),
    ('req1', u32, 1),
    ('req0', u32, 1),
    ('arb_won3', u32, 1),
    ('arb_won2', u32, 1),
    ('arb_won1', u32, 1),
    ('arb_won0', u32, 1),
    ('req_clr3', u32, 1),
    ('req_clr2', u32, 1),
    ('req_clr1', u32, 1),
    ('req_clr0', u32, 1),
    ('req_set3', u32, 1),
    ('req_set2', u32, 1),
    ('req_set1', u32, 1),
    ('req_set0', u32, 1),
]

# /home/saul/thundergate/include/nvram.h: 149
class struct_nvram_access(Structure):
    pass

struct_nvram_access.__slots__ = [
    'reserved',
    'st_lockup_fix_enable',
    'disable_auto_eeprom_reset',
    'eprom_sda_oe_mode',
    'ate_mode',
    'write_enable',
    'enable',
]
struct_nvram_access._fields_ = [
    ('reserved', u32, 26),
    ('st_lockup_fix_enable', u32, 1),
    ('disable_auto_eeprom_reset', u32, 1),
    ('eprom_sda_oe_mode', u32, 1),
    ('ate_mode', u32, 1),
    ('write_enable', u32, 1),
    ('enable', u32, 1),
]

# /home/saul/thundergate/include/nvram.h: 159
class struct_nvram_write1(Structure):
    pass

struct_nvram_write1.__slots__ = [
    'reserved',
    'disable_command',
    'enable_command',
]
struct_nvram_write1._fields_ = [
    ('reserved', u32, 16),
    ('disable_command', u32, 8),
    ('enable_command', u32, 8),
]

# /home/saul/thundergate/include/nvram.h: 165
class struct_nvram_arbitration_watchdog(Structure):
    pass

struct_nvram_arbitration_watchdog.__slots__ = [
    'reserved_31_28',
    'reserved_27_24',
    'reserved_23_8',
    'reserved_7',
    'reserved_6',
    'reserved_5',
    'reserved_4_0',
]
struct_nvram_arbitration_watchdog._fields_ = [
    ('reserved_31_28', u32, 4),
    ('reserved_27_24', u32, 4),
    ('reserved_23_8', u32, 16),
    ('reserved_7', u32, 1),
    ('reserved_6', u32, 1),
    ('reserved_5', u32, 1),
    ('reserved_4_0', u32, 5),
]

# /home/saul/thundergate/include/nvram.h: 175
class struct_nvram_auto_sense_status(Structure):
    pass

struct_nvram_auto_sense_status.__slots__ = [
    'reserved21',
    'device_id',
    'reserved13',
    'state',
    'reserved6',
    'successful',
    'enable',
    'reserved1',
    'busy',
]
struct_nvram_auto_sense_status._fields_ = [
    ('reserved21', u32, 11),
    ('device_id', u32, 5),
    ('reserved13', u32, 3),
    ('state', u32, 5),
    ('reserved6', u32, 2),
    ('successful', u32, 1),
    ('enable', u32, 1),
    ('reserved1', u32, 3),
    ('busy', u32, 1),
]

# /home/saul/thundergate/include/nvram.h: 187
class struct_nvram_regs(Structure):
    pass

struct_nvram_regs.__slots__ = [
    'command',
    'status',
    'write_data',
    'data_address',
    'read_data',
    'config1',
    'config2',
    'config3',
    'sw_arb',
    'access',
    'write1',
    'arbitration_watchdog_timer_register',
    'address_lockout_boundary',
    'address_lockout_address_counter_debug',
    'auto_sense_status',
]
struct_nvram_regs._fields_ = [
    ('command', struct_nvram_command),
    ('status', struct_nvram_status),
    ('write_data', u32),
    ('data_address', u32),
    ('read_data', u32),
    ('config1', u32),
    ('config2', u32),
    ('config3', u32),
    ('sw_arb', struct_nvram_software_arbitration),
    ('access', struct_nvram_access),
    ('write1', struct_nvram_write1),
    ('arbitration_watchdog_timer_register', struct_nvram_arbitration_watchdog),
    ('address_lockout_boundary', u32),
    ('address_lockout_address_counter_debug', u32),
    ('auto_sense_status', struct_nvram_auto_sense_status),
]

# /home/saul/thundergate/include/otp.h: 24
class struct_otp_mode(Structure):
    pass

struct_otp_mode.__slots__ = [
    'reserved',
    'mode',
]
struct_otp_mode._fields_ = [
    ('reserved', u32, 31),
    ('mode', u32, 1),
]

# /home/saul/thundergate/include/otp.h: 29
class struct_otp_control(Structure):
    pass

struct_otp_control.__slots__ = [
    'bypass_otp_clk',
    'reserved',
    'cpu_debug_sel',
    'burst_stat_sel',
    'access_mode',
    'otp_prog_en',
    'otp_debug_mode',
    'wrp_continue_on_fail',
    'wrp_time_margin',
    'wrp_sadbyp',
    'unused',
    'wrp_pbyp',
    'wrp_pcount',
    'wrp_vsel',
    'wrp_prog_sel',
    'command',
    'start',
]
struct_otp_control._fields_ = [
    ('bypass_otp_clk', u32, 1),
    ('reserved', u32, 2),
    ('cpu_debug_sel', u32, 4),
    ('burst_stat_sel', u32, 1),
    ('access_mode', u32, 2),
    ('otp_prog_en', u32, 1),
    ('otp_debug_mode', u32, 1),
    ('wrp_continue_on_fail', u32, 1),
    ('wrp_time_margin', u32, 3),
    ('wrp_sadbyp', u32, 1),
    ('unused', u32, 1),
    ('wrp_pbyp', u32, 1),
    ('wrp_pcount', u32, 3),
    ('wrp_vsel', u32, 4),
    ('wrp_prog_sel', u32, 1),
    ('command', u32, 4),
    ('start', u32, 1),
]

# /home/saul/thundergate/include/otp.h: 49
class struct_otp_status(Structure):
    pass

struct_otp_status.__slots__ = [
    'reserved',
    'control_error',
    'wrp_error',
    'invalid_command',
    'otp_stby_reg',
    'init_wait_done',
    'prog_blocked',
    'invalid_prog_req',
    'wrp_fail',
    'wrp_busy',
    'wrp_dout',
    'wrp_data_read',
    'command_done',
]
struct_otp_status._fields_ = [
    ('reserved', u32, 20),
    ('control_error', u32, 1),
    ('wrp_error', u32, 1),
    ('invalid_command', u32, 1),
    ('otp_stby_reg', u32, 1),
    ('init_wait_done', u32, 1),
    ('prog_blocked', u32, 1),
    ('invalid_prog_req', u32, 1),
    ('wrp_fail', u32, 1),
    ('wrp_busy', u32, 1),
    ('wrp_dout', u32, 1),
    ('wrp_data_read', u32, 1),
    ('command_done', u32, 1),
]

# /home/saul/thundergate/include/otp.h: 65
class struct_otp_addr(Structure):
    pass

struct_otp_addr.__slots__ = [
    'reserved',
    'address',
]
struct_otp_addr._fields_ = [
    ('reserved', u32, 16),
    ('address', u32, 16),
]

# /home/saul/thundergate/include/otp.h: 70
class struct_otp_soft_reset(Structure):
    pass

struct_otp_soft_reset.__slots__ = [
    'reserved',
    'reset',
]
struct_otp_soft_reset._fields_ = [
    ('reserved', u32, 31),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/otp.h: 75
class struct_otp_regs(Structure):
    pass

struct_otp_regs.__slots__ = [
    'mode',
    'control',
    'status',
    'address',
    'write_data',
    'read_data',
    'soft_reset',
]
struct_otp_regs._fields_ = [
    ('mode', struct_otp_mode),
    ('control', struct_otp_control),
    ('status', struct_otp_status),
    ('address', struct_otp_addr),
    ('write_data', u32),
    ('read_data', u32),
    ('soft_reset', struct_otp_soft_reset),
]

# /home/saul/thundergate/include/pcie_alt.h: 22
class struct_pcie_pl_lo_regs(Structure):
    pass

struct_pcie_pl_lo_regs.__slots__ = [
    'phyctl0',
    'phyctl1',
    'phyctl2',
    'phyctl3',
    'phyctl4',
    'phyctl5',
]
struct_pcie_pl_lo_regs._fields_ = [
    ('phyctl0', u32),
    ('phyctl1', u32),
    ('phyctl2', u32),
    ('phyctl3', u32),
    ('phyctl4', u32),
    ('phyctl5', u32),
]

# /home/saul/thundergate/include/pcie_alt.h: 31
class struct_pcie_dl_lo_ftsmax(Structure):
    pass

struct_pcie_dl_lo_ftsmax.__slots__ = [
    'unknown',
    'val',
]
struct_pcie_dl_lo_ftsmax._fields_ = [
    ('unknown', u32, 24),
    ('val', u32, 8),
]

# /home/saul/thundergate/include/pcie_alt.h: 36
class struct_pcie_dl_lo_regs(Structure):
    pass

struct_pcie_dl_lo_regs.__slots__ = [
    'unknown0',
    'unknown4',
    'unknown8',
    'ftsmax',
]
struct_pcie_dl_lo_regs._fields_ = [
    ('unknown0', u32),
    ('unknown4', u32),
    ('unknown8', u32),
    ('ftsmax', struct_pcie_dl_lo_ftsmax),
]

# /home/saul/thundergate/include/pcie_alt.h: 43
class struct_pcie_alt_regs(Structure):
    pass

# /home/saul/thundergate/include/pcie.h: 22
class struct_pcie_tl_tlp_ctrl(Structure):
    pass

struct_pcie_tl_tlp_ctrl.__slots__ = [
    'excessive_current_fix_en',
    'reserved30',
    'int_mode_fix_en',
    'reserved28',
    'unexpected_completion_err_fix_en',
    'type1_vendor_defined_msg_fix_en',
    'data_fifo_protect',
    'address_check_en',
    'tc0_check_en',
    'crc_swap',
    'ca_err_dis',
    'ur_err_dis',
    'rsv_err_dis',
    'mps_chk_en',
    'ep_err_dis',
    'bytecount_chk_en',
    'reserved14',
    'dma_read_traffic_class',
    'dma_write_traffic_class',
    'reserved6',
    'completion_timeout',
]
struct_pcie_tl_tlp_ctrl._fields_ = [
    ('excessive_current_fix_en', u32, 1),
    ('reserved30', u32, 1),
    ('int_mode_fix_en', u32, 1),
    ('reserved28', u32, 1),
    ('unexpected_completion_err_fix_en', u32, 1),
    ('type1_vendor_defined_msg_fix_en', u32, 1),
    ('data_fifo_protect', u32, 1),
    ('address_check_en', u32, 1),
    ('tc0_check_en', u32, 1),
    ('crc_swap', u32, 1),
    ('ca_err_dis', u32, 1),
    ('ur_err_dis', u32, 1),
    ('rsv_err_dis', u32, 1),
    ('mps_chk_en', u32, 1),
    ('ep_err_dis', u32, 1),
    ('bytecount_chk_en', u32, 1),
    ('reserved14', u32, 2),
    ('dma_read_traffic_class', u32, 3),
    ('dma_write_traffic_class', u32, 3),
    ('reserved6', u32, 2),
    ('completion_timeout', u32, 6),
]

# /home/saul/thundergate/include/pcie.h: 46
class struct_pcie_tl_transaction_config(Structure):
    pass

struct_pcie_tl_transaction_config.__slots__ = [
    'retry_buffer_timining_mod_en',
    'reserved30',
    'one_shot_msi_en',
    'reserved28',
    'select_core_clock_override',
    'cq9139_fix_en',
    'cmpt_pwr_check_en',
    'cq12696_fix_en',
    'device_serial_no_override',
    'cq12455_fix_en',
    'tc_vc_filtering_check_en',
    'dont_gen_hot_plug_msg',
    'ignore_hot_plug_msg',
    'msi_multimsg_cap',
    'data_select_limit',
    'pcie_1_1_pl_en',
    'pcie_1_1_dl_en',
    'pcie_1_1_tl_en',
    'reserved7',
    'pcie_power_budget_cap_en',
    'lom_configuration',
    'concate_select',
    'ur_status_bit_fix_en',
    'vendor_defined_msg_fix_en',
    'power_state_write_mem_enable',
    'reserved0',
]
struct_pcie_tl_transaction_config._fields_ = [
    ('retry_buffer_timining_mod_en', u32, 1),
    ('reserved30', u32, 1),
    ('one_shot_msi_en', u32, 1),
    ('reserved28', u32, 1),
    ('select_core_clock_override', u32, 1),
    ('cq9139_fix_en', u32, 1),
    ('cmpt_pwr_check_en', u32, 1),
    ('cq12696_fix_en', u32, 1),
    ('device_serial_no_override', u32, 1),
    ('cq12455_fix_en', u32, 1),
    ('tc_vc_filtering_check_en', u32, 1),
    ('dont_gen_hot_plug_msg', u32, 1),
    ('ignore_hot_plug_msg', u32, 1),
    ('msi_multimsg_cap', u32, 3),
    ('data_select_limit', u32, 4),
    ('pcie_1_1_pl_en', u32, 1),
    ('pcie_1_1_dl_en', u32, 1),
    ('pcie_1_1_tl_en', u32, 1),
    ('reserved7', u32, 2),
    ('pcie_power_budget_cap_en', u32, 1),
    ('lom_configuration', u32, 1),
    ('concate_select', u32, 1),
    ('ur_status_bit_fix_en', u32, 1),
    ('vendor_defined_msg_fix_en', u32, 1),
    ('power_state_write_mem_enable', u32, 1),
    ('reserved0', u32, 1),
]

# /home/saul/thundergate/include/pcie.h: 75
class struct_pcie_tl_wdma_len_byte_en_req_diag(Structure):
    pass

struct_pcie_tl_wdma_len_byte_en_req_diag.__slots__ = [
    'request_length',
    'byte_enables',
    'reserved1',
    'raw_request',
]
struct_pcie_tl_wdma_len_byte_en_req_diag._fields_ = [
    ('request_length', u32, 16),
    ('byte_enables', u32, 8),
    ('reserved1', u32, 7),
    ('raw_request', u32, 1),
]

# /home/saul/thundergate/include/pcie.h: 82
class struct_pcie_tl_rdma_len_req_diag(Structure):
    pass

struct_pcie_tl_rdma_len_req_diag.__slots__ = [
    'request_length',
    'reserved1',
    'raw_request',
]
struct_pcie_tl_rdma_len_req_diag._fields_ = [
    ('request_length', u32, 16),
    ('reserved1', u32, 15),
    ('raw_request', u32, 1),
]

# /home/saul/thundergate/include/pcie.h: 88
class struct_pcie_tl_msi_len_req_diag(Structure):
    pass

struct_pcie_tl_msi_len_req_diag.__slots__ = [
    'request_length',
    'reserved1',
    'raw_request',
]
struct_pcie_tl_msi_len_req_diag._fields_ = [
    ('request_length', u32, 16),
    ('reserved1', u32, 15),
    ('raw_request', u32, 1),
]

# /home/saul/thundergate/include/pcie.h: 94
class struct_pcie_tl_slave_req_len_type_diag(Structure):
    pass

struct_pcie_tl_slave_req_len_type_diag.__slots__ = [
    'reg_slv_len_req',
    'request_length',
    'reserved2',
    'request_type',
    'raw_request',
]
struct_pcie_tl_slave_req_len_type_diag._fields_ = [
    ('reg_slv_len_req', u32, 6),
    ('request_length', u32, 10),
    ('reserved2', u32, 14),
    ('request_type', u32, 1),
    ('raw_request', u32, 1),
]

# /home/saul/thundergate/include/pcie.h: 102
class struct_pcie_tl_flow_control_inputs_diag(Structure):
    pass

struct_pcie_tl_flow_control_inputs_diag.__slots__ = [
    'reg_fc_input',
    'non_posted_header_avail',
    'posted_header_avail',
    'completion_header_avail',
    'posted_data_avail',
    'completion_data_avail',
]
struct_pcie_tl_flow_control_inputs_diag._fields_ = [
    ('reg_fc_input', u32, 5),
    ('non_posted_header_avail', u32, 1),
    ('posted_header_avail', u32, 1),
    ('completion_header_avail', u32, 1),
    ('posted_data_avail', u32, 12),
    ('completion_data_avail', u32, 12),
]

# /home/saul/thundergate/include/pcie.h: 111
class struct_pcie_tl_xmt_state_machines_gated_reqs_diag(Structure):
    pass

struct_pcie_tl_xmt_state_machines_gated_reqs_diag.__slots__ = [
    'reg_sm_r0_r3',
    'tlp_tx_data_state_machine',
    'tlp_tx_arb_state_machine',
    'reserved4',
    'slave_dma_gated_req',
    'msi_dma_gated_req',
    'read_dma_gated_req',
    'write_dma_gated_req',
]
struct_pcie_tl_xmt_state_machines_gated_reqs_diag._fields_ = [
    ('reg_sm_r0_r3', u32, 1),
    ('tlp_tx_data_state_machine', u32, 3),
    ('tlp_tx_arb_state_machine', u32, 4),
    ('reserved4', u32, 20),
    ('slave_dma_gated_req', u32, 1),
    ('msi_dma_gated_req', u32, 1),
    ('read_dma_gated_req', u32, 1),
    ('write_dma_gated_req', u32, 1),
]

# /home/saul/thundergate/include/pcie.h: 122
class struct_pcie_tl_tlp_bdf(Structure):
    pass

struct_pcie_tl_tlp_bdf.__slots__ = [
    'reserved17',
    'config_write_indicator',
    'bus',
    'device',
    'function',
]
struct_pcie_tl_tlp_bdf._fields_ = [
    ('reserved17', u32, 15),
    ('config_write_indicator', u32, 1),
    ('bus', u32, 8),
    ('device', u32, 5),
    ('function', u32, 3),
]

# /home/saul/thundergate/include/pcie.h: 130
class struct_pcie_tl_regs(Structure):
    pass

struct_pcie_tl_regs.__slots__ = [
    'tlp_ctrl',
    'transaction_config',
    'ofs_08',
    'ofs_0c',
    'wdma_req_upper_addr_diag',
    'wdma_req_lower_addr_diag',
    'wdma_len_byte_en_req_diag',
    'rdma_req_upper_addr_diag',
    'rdma_req_lower_addr_diag',
    'rdma_len_req_diag',
    'msi_dma_req_upper_addr_diag',
    'msi_dma_req_lower_addr_diag',
    'msi_dma_len_req_diag',
    'slave_req_len_type_diag',
    'flow_control_inputs_diag',
    'xmt_state_machines_gated_reqs_diag',
    'address_ack_xfer_count_and_arb_length_diag',
    'dma_completion_header_diag_0',
    'dma_completion_header_diag_1',
    'dma_completion_header_diag_2',
    'dma_completion_misc_diag_0',
    'dma_completion_misc_diag_1',
    'dma_completion_misc_diag_2',
    'split_controller_req_length_address_ack_remaining_diag',
    'split_controller_misc_diag_0',
    'split_controller_misc_diag_1',
    'bdf',
    'tlp_debug',
    'retry_buffer_free',
    'target_debug_1',
    'target_debug_2',
    'target_debug_3',
    'target_debug_4',
]
struct_pcie_tl_regs._fields_ = [
    ('tlp_ctrl', struct_pcie_tl_tlp_ctrl),
    ('transaction_config', struct_pcie_tl_transaction_config),
    ('ofs_08', u32),
    ('ofs_0c', u32),
    ('wdma_req_upper_addr_diag', u32),
    ('wdma_req_lower_addr_diag', u32),
    ('wdma_len_byte_en_req_diag', struct_pcie_tl_wdma_len_byte_en_req_diag),
    ('rdma_req_upper_addr_diag', u32),
    ('rdma_req_lower_addr_diag', u32),
    ('rdma_len_req_diag', struct_pcie_tl_rdma_len_req_diag),
    ('msi_dma_req_upper_addr_diag', u32),
    ('msi_dma_req_lower_addr_diag', u32),
    ('msi_dma_len_req_diag', struct_pcie_tl_msi_len_req_diag),
    ('slave_req_len_type_diag', struct_pcie_tl_slave_req_len_type_diag),
    ('flow_control_inputs_diag', struct_pcie_tl_flow_control_inputs_diag),
    ('xmt_state_machines_gated_reqs_diag', struct_pcie_tl_xmt_state_machines_gated_reqs_diag),
    ('address_ack_xfer_count_and_arb_length_diag', u32),
    ('dma_completion_header_diag_0', u32),
    ('dma_completion_header_diag_1', u32),
    ('dma_completion_header_diag_2', u32),
    ('dma_completion_misc_diag_0', u32),
    ('dma_completion_misc_diag_1', u32),
    ('dma_completion_misc_diag_2', u32),
    ('split_controller_req_length_address_ack_remaining_diag', u32),
    ('split_controller_misc_diag_0', u32),
    ('split_controller_misc_diag_1', u32),
    ('bdf', struct_pcie_tl_tlp_bdf),
    ('tlp_debug', u32),
    ('retry_buffer_free', u32),
    ('target_debug_1', u32),
    ('target_debug_2', u32),
    ('target_debug_3', u32),
    ('target_debug_4', u32),
]

# /home/saul/thundergate/include/pcie.h: 174
class struct_pcie_dl_ctrl(Structure):
    pass

struct_pcie_dl_ctrl.__slots__ = [
    'reserved19',
    'pll_refsel_sw',
    'reserved17',
    'power_management_ctrl_en',
    'power_down_serdes_transmitter',
    'power_down_serdes_pll',
    'power_down_serdes_receiver',
    'enable_beacon',
    'automatic_timer_threshold_en',
    'dllp_timeout_mech_en',
    'chk_rcv_flow_ctrl_credits',
    'link_enable',
    'power_management_ctrl',
]
struct_pcie_dl_ctrl._fields_ = [
    ('reserved19', u32, 13),
    ('pll_refsel_sw', u32, 1),
    ('reserved17', u32, 1),
    ('power_management_ctrl_en', u32, 1),
    ('power_down_serdes_transmitter', u32, 1),
    ('power_down_serdes_pll', u32, 1),
    ('power_down_serdes_receiver', u32, 1),
    ('enable_beacon', u32, 1),
    ('automatic_timer_threshold_en', u32, 1),
    ('dllp_timeout_mech_en', u32, 1),
    ('chk_rcv_flow_ctrl_credits', u32, 1),
    ('link_enable', u32, 1),
    ('power_management_ctrl', u32, 8),
]

# /home/saul/thundergate/include/pcie.h: 190
class struct_pcie_dl_status(Structure):
    pass

struct_pcie_dl_status.__slots__ = [
    'reserved26',
    'phy_link_state',
    'power_management_state',
    'power_management_substate',
    'data_link_up',
    'reserved11',
    'pme_turn_off_status_in_d0',
    'flow_ctrl_update_timeout',
    'flow_ctrl_recv_oflow',
    'flow_ctrl_proto_err',
    'data_link_proto_err',
    'replay_rollover',
    'replay_timeout',
    'nak_recvd',
    'dllp_error',
    'bad_tlp_seq_no',
    'tlp_error',
]
struct_pcie_dl_status._fields_ = [
    ('reserved26', u32, 6),
    ('phy_link_state', u32, 3),
    ('power_management_state', u32, 4),
    ('power_management_substate', u32, 2),
    ('data_link_up', u32, 1),
    ('reserved11', u32, 5),
    ('pme_turn_off_status_in_d0', u32, 1),
    ('flow_ctrl_update_timeout', u32, 1),
    ('flow_ctrl_recv_oflow', u32, 1),
    ('flow_ctrl_proto_err', u32, 1),
    ('data_link_proto_err', u32, 1),
    ('replay_rollover', u32, 1),
    ('replay_timeout', u32, 1),
    ('nak_recvd', u32, 1),
    ('dllp_error', u32, 1),
    ('bad_tlp_seq_no', u32, 1),
    ('tlp_error', u32, 1),
]

# /home/saul/thundergate/include/pcie.h: 210
class struct_pcie_dl_attn(Structure):
    pass

struct_pcie_dl_attn.__slots__ = [
    'reserved5',
    'data_link_layer_attn_ind',
    'nak_rcvd_cntr_attn_ind',
    'dllp_err_cntr_attn_ind',
    'tlp_bad_seq_cntr_attn_ind',
    'tlp_err_cntr_attn_ind',
]
struct_pcie_dl_attn._fields_ = [
    ('reserved5', u32, 27),
    ('data_link_layer_attn_ind', u32, 1),
    ('nak_rcvd_cntr_attn_ind', u32, 1),
    ('dllp_err_cntr_attn_ind', u32, 1),
    ('tlp_bad_seq_cntr_attn_ind', u32, 1),
    ('tlp_err_cntr_attn_ind', u32, 1),
]

# /home/saul/thundergate/include/pcie.h: 219
class struct_pcie_dl_attn_mask(Structure):
    pass

struct_pcie_dl_attn_mask.__slots__ = [
    'reserved8',
    'attn_mask',
    'data_link_layer_attn_mask',
    'nak_rcvd_cntr_attn_mask',
    'dllp_err_cntr_attn_mask',
    'tlp_bad_seq_cntr_attn_mask',
    'tlp_err_cntr_attn_mask',
]
struct_pcie_dl_attn_mask._fields_ = [
    ('reserved8', u32, 24),
    ('attn_mask', u32, 3),
    ('data_link_layer_attn_mask', u32, 1),
    ('nak_rcvd_cntr_attn_mask', u32, 1),
    ('dllp_err_cntr_attn_mask', u32, 1),
    ('tlp_bad_seq_cntr_attn_mask', u32, 1),
    ('tlp_err_cntr_attn_mask', u32, 1),
]

# /home/saul/thundergate/include/pcie.h: 229
class struct_pcie_dl_seq_no(Structure):
    pass

struct_pcie_dl_seq_no.__slots__ = [
    'reserved12',
    'value',
]
struct_pcie_dl_seq_no._fields_ = [
    ('reserved12', u32, 20),
    ('value', u32, 12),
]

# /home/saul/thundergate/include/pcie.h: 234
class struct_pcie_dl_replay(Structure):
    pass

struct_pcie_dl_replay.__slots__ = [
    'reserved23',
    'timeout_value',
    'buffer_size',
]
struct_pcie_dl_replay._fields_ = [
    ('reserved23', u32, 9),
    ('timeout_value', u32, 13),
    ('buffer_size', u32, 10),
]

# /home/saul/thundergate/include/pcie.h: 240
class struct_pcie_dl_ack_timeout(Structure):
    pass

struct_pcie_dl_ack_timeout.__slots__ = [
    'reserved11',
    'value',
]
struct_pcie_dl_ack_timeout._fields_ = [
    ('reserved11', u32, 21),
    ('value', u32, 11),
]

# /home/saul/thundergate/include/pcie.h: 245
class struct_pcie_dl_pm_threshold(Structure):
    pass

struct_pcie_dl_pm_threshold.__slots__ = [
    'reserved24',
    'l0_stay_time',
    'l1_stay_time',
    'l1_threshold',
    'l0s_threshold',
]
struct_pcie_dl_pm_threshold._fields_ = [
    ('reserved24', u32, 8),
    ('l0_stay_time', u32, 4),
    ('l1_stay_time', u32, 4),
    ('l1_threshold', u32, 8),
    ('l0s_threshold', u32, 8),
]

# /home/saul/thundergate/include/pcie.h: 253
class struct_pcie_dl_retry_buffer_ptr(Structure):
    pass

struct_pcie_dl_retry_buffer_ptr.__slots__ = [
    'reserved11',
    'value',
]
struct_pcie_dl_retry_buffer_ptr._fields_ = [
    ('reserved11', u32, 21),
    ('value', u32, 11),
]

# /home/saul/thundergate/include/pcie.h: 258
class struct_pcie_dl_test(Structure):
    pass

struct_pcie_dl_test.__slots__ = [
    'reserved16',
    'store_recv_tlps',
    'disable_tlps',
    'disable_dllps',
    'force_phy_link_up',
    'bypass_flow_ctrl',
    'ram_core_clock_margin_test_en',
    'ram_overstress_test_en',
    'ram_read_margin_test_en',
    'speed_up_completion_timer',
    'speed_up_replay_timer',
    'speed_up_ack_latency_timer',
    'speed_up_pme_service_timer',
    'force_purge',
    'force_retry',
    'invert_crc',
    'send_bad_crc_bit',
]
struct_pcie_dl_test._fields_ = [
    ('reserved16', u32, 16),
    ('store_recv_tlps', u32, 1),
    ('disable_tlps', u32, 1),
    ('disable_dllps', u32, 1),
    ('force_phy_link_up', u32, 1),
    ('bypass_flow_ctrl', u32, 1),
    ('ram_core_clock_margin_test_en', u32, 1),
    ('ram_overstress_test_en', u32, 1),
    ('ram_read_margin_test_en', u32, 1),
    ('speed_up_completion_timer', u32, 1),
    ('speed_up_replay_timer', u32, 1),
    ('speed_up_ack_latency_timer', u32, 1),
    ('speed_up_pme_service_timer', u32, 1),
    ('force_purge', u32, 1),
    ('force_retry', u32, 1),
    ('invert_crc', u32, 1),
    ('send_bad_crc_bit', u32, 1),
]

# /home/saul/thundergate/include/pcie.h: 278
class struct_pcie_dl_packet_bist(Structure):
    pass

struct_pcie_dl_packet_bist.__slots__ = [
    'reserved24',
    'packet_checker_loaded',
    'recv_mismatch',
    'rand_tlp_len_en',
    'tlp_len',
    'random_ipg_len_en',
    'ipg_len',
    'transmit_start',
    'packet_generator_test_mode_en',
]
struct_pcie_dl_packet_bist._fields_ = [
    ('reserved24', u32, 8),
    ('packet_checker_loaded', u32, 1),
    ('recv_mismatch', u32, 1),
    ('rand_tlp_len_en', u32, 1),
    ('tlp_len', u32, 11),
    ('random_ipg_len_en', u32, 1),
    ('ipg_len', u32, 7),
    ('transmit_start', u32, 1),
    ('packet_generator_test_mode_en', u32, 1),
]

# /home/saul/thundergate/include/pcie.h: 290
class struct_pcie_dl_regs(Structure):
    pass

struct_pcie_dl_regs.__slots__ = [
    'dl_ctrl',
    'dl_status',
    'dl_attn',
    'dl_attn_mask',
    'next_transmit_seq_no',
    'acked_transmit_seq_no',
    'purged_transmit_seq_no',
    'receive_req_no',
    'replay',
    'ack_timeout',
    'power_mgmt_threshold',
    'retry_buffer_write_ptr',
    'retry_buffer_read_ptr',
    'retry_buffer_purged_ptr',
    'retry_buffer_read_write_port',
    'error_count_threshold',
    'tlp_error_counter',
    'dllp_error_counter',
    'nak_received_counter',
    'test',
    'packet_bist',
    'link_pcie_1_1_control',
]
struct_pcie_dl_regs._fields_ = [
    ('dl_ctrl', struct_pcie_dl_ctrl),
    ('dl_status', struct_pcie_dl_status),
    ('dl_attn', struct_pcie_dl_attn),
    ('dl_attn_mask', struct_pcie_dl_attn_mask),
    ('next_transmit_seq_no', struct_pcie_dl_seq_no),
    ('acked_transmit_seq_no', struct_pcie_dl_seq_no),
    ('purged_transmit_seq_no', struct_pcie_dl_seq_no),
    ('receive_req_no', struct_pcie_dl_seq_no),
    ('replay', struct_pcie_dl_replay),
    ('ack_timeout', struct_pcie_dl_ack_timeout),
    ('power_mgmt_threshold', struct_pcie_dl_pm_threshold),
    ('retry_buffer_write_ptr', struct_pcie_dl_retry_buffer_ptr),
    ('retry_buffer_read_ptr', struct_pcie_dl_retry_buffer_ptr),
    ('retry_buffer_purged_ptr', struct_pcie_dl_retry_buffer_ptr),
    ('retry_buffer_read_write_port', u32),
    ('error_count_threshold', u32),
    ('tlp_error_counter', u32),
    ('dllp_error_counter', u32),
    ('nak_received_counter', u32),
    ('test', struct_pcie_dl_test),
    ('packet_bist', struct_pcie_dl_packet_bist),
    ('link_pcie_1_1_control', u32),
]

# /home/saul/thundergate/include/pcie.h: 320
class struct_pcie_pl_regs(Structure):
    pass

struct_pcie_pl_regs.__slots__ = [
    'phy_mode',
    'phy_link_status',
    'phy_link_ltssm_control',
    'phy_link_training_link_number',
    'phy_link_training_lane_number',
    'phy_link_training_n_fts',
    'phy_attention',
    'phy_attention_mask',
    'phy_receive_error_counter',
    'phy_receive_framing_error_counter',
    'phy_receive_error_threshold',
    'phy_test_control',
    'phy_serdes_control_override',
    'phy_timing_parameter_override',
    'phy_hardware_diag_1',
    'phy_hardware_diag_2',
]
struct_pcie_pl_regs._fields_ = [
    ('phy_mode', u32),
    ('phy_link_status', u32),
    ('phy_link_ltssm_control', u32),
    ('phy_link_training_link_number', u32),
    ('phy_link_training_lane_number', u32),
    ('phy_link_training_n_fts', u32),
    ('phy_attention', u32),
    ('phy_attention_mask', u32),
    ('phy_receive_error_counter', u32),
    ('phy_receive_framing_error_counter', u32),
    ('phy_receive_error_threshold', u32),
    ('phy_test_control', u32),
    ('phy_serdes_control_override', u32),
    ('phy_timing_parameter_override', u32),
    ('phy_hardware_diag_1', u32),
    ('phy_hardware_diag_2', u32),
]

# /home/saul/thundergate/include/pci.h: 22
class struct_pci_status(Structure):
    pass

# /home/saul/thundergate/include/pci.h: 43
class struct_pci_command(Structure):
    pass

# /home/saul/thundergate/include/pci.h: 63
class struct_pci_pm_cap(Structure):
    pass

struct_pci_pm_cap.__slots__ = [
    'pme_support',
    'd2_support',
    'd1_support',
    'aux_current',
    'dsi',
    'reserved6',
    'pme_clock',
    'version',
    'next_cap',
    'cap_id',
]
struct_pci_pm_cap._fields_ = [
    ('pme_support', u32, 5),
    ('d2_support', u32, 1),
    ('d1_support', u32, 1),
    ('aux_current', u32, 3),
    ('dsi', u32, 1),
    ('reserved6', u32, 1),
    ('pme_clock', u32, 1),
    ('version', u32, 3),
    ('next_cap', u32, 8),
    ('cap_id', u32, 8),
]

# /home/saul/thundergate/include/pci.h: 76
class struct_pci_pm_ctrl_status(Structure):
    pass

struct_pci_pm_ctrl_status.__slots__ = [
    'pm_data',
    'reserved7',
    'pme_status',
    'data_scale',
    'data_select',
    'pme_enable',
    'reserved8',
    'no_soft_reset',
    'reserved9',
    'power_state',
]
struct_pci_pm_ctrl_status._fields_ = [
    ('pm_data', u32, 8),
    ('reserved7', u32, 8),
    ('pme_status', u32, 1),
    ('data_scale', u32, 2),
    ('data_select', u32, 4),
    ('pme_enable', u32, 1),
    ('reserved8', u32, 4),
    ('no_soft_reset', u32, 1),
    ('reserved9', u32, 1),
    ('power_state', u32, 2),
]

# /home/saul/thundergate/include/pci.h: 89
class struct_pci_msi_cap_hdr(Structure):
    pass

struct_pci_msi_cap_hdr.__slots__ = [
    'msi_control',
    'msi_pvmask_capable',
    'sixty_four_bit_addr_capable',
    'multiple_message_enable',
    'multiple_message_capable',
    'msi_enable',
    'next_cap',
    'cap_id',
]
struct_pci_msi_cap_hdr._fields_ = [
    ('msi_control', u32, 7),
    ('msi_pvmask_capable', u32, 1),
    ('sixty_four_bit_addr_capable', u32, 1),
    ('multiple_message_enable', u32, 3),
    ('multiple_message_capable', u32, 3),
    ('msi_enable', u32, 1),
    ('next_cap', u32, 8),
    ('cap_id', u32, 8),
]

# /home/saul/thundergate/include/pci.h: 100
class struct_pci_misc_host_ctrl(Structure):
    pass

struct_pci_misc_host_ctrl.__slots__ = [
    'asic_rev_id',
    'unused',
    'enable_tagged_status_mode',
    'mask_interrupt_mode',
    'enable_indirect_access',
    'enable_register_word_swap',
    'enable_clock_control_register_rw_cap',
    'enable_pci_state_register_rw_cap',
    'enable_endian_word_swap',
    'enable_endian_byte_swap',
    'mask_interrupt',
    'clear_interrupt',
]
struct_pci_misc_host_ctrl._fields_ = [
    ('asic_rev_id', u32, 16),
    ('unused', u32, 6),
    ('enable_tagged_status_mode', u32, 1),
    ('mask_interrupt_mode', u32, 1),
    ('enable_indirect_access', u32, 1),
    ('enable_register_word_swap', u32, 1),
    ('enable_clock_control_register_rw_cap', u32, 1),
    ('enable_pci_state_register_rw_cap', u32, 1),
    ('enable_endian_word_swap', u32, 1),
    ('enable_endian_byte_swap', u32, 1),
    ('mask_interrupt', u32, 1),
    ('clear_interrupt', u32, 1),
]

# /home/saul/thundergate/include/pci.h: 115
class struct_pci_dma_rw_ctrl(Structure):
    pass

struct_pci_dma_rw_ctrl.__slots__ = [
    'reserved25',
    'cr_write_watermark',
    'dma_write_watermark',
    'reserved10',
    'card_reader_dma_read_mrrs',
    'dma_read_mrrs_for_slow_speed',
    'reserved1',
    'disable_cache_alignment',
]
struct_pci_dma_rw_ctrl._fields_ = [
    ('reserved25', u32, 7),
    ('cr_write_watermark', u32, 3),
    ('dma_write_watermark', u32, 3),
    ('reserved10', u32, 9),
    ('card_reader_dma_read_mrrs', u32, 3),
    ('dma_read_mrrs_for_slow_speed', u32, 3),
    ('reserved1', u32, 3),
    ('disable_cache_alignment', u32, 1),
]

# /home/saul/thundergate/include/pci.h: 126
class struct_pci_state(Structure):
    pass

struct_pci_state.__slots__ = [
    'reserved20',
    'generate_reset_pulse',
    'ape_ps_wr_en',
    'ape_shm_wr_en',
    'ape_ctrl_reg_wr_en',
    'config_retry',
    'reserved15',
    'pci_vaux_present',
    'max_retry',
    'flat_view',
    'vpd_available',
    'rom_retry_enable',
    'rom_enable',
    'bus_32_bit',
    'bus_speed_hi',
    'conv_pci_mode',
    'int_not_active',
    'force_reset',
]
struct_pci_state._fields_ = [
    ('reserved20', u32, 12),
    ('generate_reset_pulse', u32, 1),
    ('ape_ps_wr_en', u32, 1),
    ('ape_shm_wr_en', u32, 1),
    ('ape_ctrl_reg_wr_en', u32, 1),
    ('config_retry', u32, 1),
    ('reserved15', u32, 2),
    ('pci_vaux_present', u32, 1),
    ('max_retry', u32, 3),
    ('flat_view', u32, 1),
    ('vpd_available', u32, 1),
    ('rom_retry_enable', u32, 1),
    ('rom_enable', u32, 1),
    ('bus_32_bit', u32, 1),
    ('bus_speed_hi', u32, 1),
    ('conv_pci_mode', u32, 1),
    ('int_not_active', u32, 1),
    ('force_reset', u32, 1),
]

# /home/saul/thundergate/include/pci.h: 152
class struct_pci_device_id(Structure):
    pass

struct_pci_device_id.__slots__ = [
    'did',
    'vid',
]
struct_pci_device_id._fields_ = [
    ('did', u32, 16),
    ('vid', u32, 16),
]

# /home/saul/thundergate/include/pci.h: 157
class struct_pci_class_code_rev_id(Structure):
    pass

struct_pci_class_code_rev_id.__slots__ = [
    'class_code',
    'rev_id',
]
struct_pci_class_code_rev_id._fields_ = [
    ('class_code', u32, 24),
    ('rev_id', u32, 8),
]

# /home/saul/thundergate/include/pci.h: 162
class struct_pci_regs(Structure):
    pass

struct_pci_regs.__slots__ = [
    'class_code_rev_id',
    'bar0_hi',
    'bar0_low',
    'bar1_hi',
    'bar1_low',
    'bar2_hi',
    'bar2_low',
    'cardbus_cis_ptr',
    'rombar',
    'reserved2',
    'int_mailbox',
    'pm_cap',
    'pm_ctrl_status',
    'unknown2',
    'msi_cap_hdr',
    'msi_lower_address',
    'msi_upper_address',
    'msi_data',
    'misc_host_ctrl',
    'dma_rw_ctrl',
    'state',
    'reset_counters_initial_values',
    'reg_base_addr',
    'mem_base_addr',
    'reg_data',
    'mem_data',
    'unknown3',
    'misc_local_control',
    'unknown4',
    'std_ring_prod_ci_hi',
    'std_ring_prod_ci_low',
    'recv_ret_ring_ci_hi',
    'recv_ret_ring_ci_low',
]
struct_pci_regs._fields_ = [
    ('class_code_rev_id', struct_pci_class_code_rev_id),
    ('bar0_hi', u32),
    ('bar0_low', u32),
    ('bar1_hi', u32),
    ('bar1_low', u32),
    ('bar2_hi', u32),
    ('bar2_low', u32),
    ('cardbus_cis_ptr', u32),
    ('rombar', u32),
    ('reserved2', u32),
    ('int_mailbox', u64),
    ('pm_cap', struct_pci_pm_cap),
    ('pm_ctrl_status', struct_pci_pm_ctrl_status),
    ('unknown2', u32 * 2),
    ('msi_cap_hdr', struct_pci_msi_cap_hdr),
    ('msi_lower_address', u32),
    ('msi_upper_address', u32),
    ('msi_data', u32),
    ('misc_host_ctrl', struct_pci_misc_host_ctrl),
    ('dma_rw_ctrl', struct_pci_dma_rw_ctrl),
    ('state', struct_pci_state),
    ('reset_counters_initial_values', u32),
    ('reg_base_addr', u32),
    ('mem_base_addr', u32),
    ('reg_data', u32),
    ('mem_data', u32),
    ('unknown3', u32 * 2),
    ('misc_local_control', u32),
    ('unknown4', u32),
    ('std_ring_prod_ci_hi', u32),
    ('std_ring_prod_ci_low', u32),
    ('recv_ret_ring_ci_hi', u32),
    ('recv_ret_ring_ci_low', u32),
]

# /home/saul/thundergate/include/rbdc.h: 22
class struct_rbdc_mode(Structure):
    pass

# /home/saul/thundergate/include/rbdc.h: 31
class struct_rbdc_status(Structure):
    pass

struct_rbdc_status.__slots__ = [
    'reserved',
    'error',
    'reserved2',
]
struct_rbdc_status._fields_ = [
    ('reserved', u32, 29),
    ('error', u32, 1),
    ('reserved2', u32, 2),
]

# /home/saul/thundergate/include/rbdc.h: 37
class struct_rbdc_rbd_pi(Structure):
    pass

struct_rbdc_rbd_pi.__slots__ = [
    'reserved',
    'bd_pi',
]
struct_rbdc_rbd_pi._fields_ = [
    ('reserved', u32, 23),
    ('bd_pi', u32, 9),
]

# /home/saul/thundergate/include/rbdc.h: 42
class struct_rbdc_regs(Structure):
    pass

struct_rbdc_regs.__slots__ = [
    'mode',
    'status',
    'jumbo_rbd_pi',
    'std_rbd_pi',
    'mini_rbd_pi',
]
struct_rbdc_regs._fields_ = [
    ('mode', struct_rbdc_mode),
    ('status', struct_rbdc_status),
    ('jumbo_rbd_pi', struct_rbdc_rbd_pi),
    ('std_rbd_pi', struct_rbdc_rbd_pi),
    ('mini_rbd_pi', struct_rbdc_rbd_pi),
]

# /home/saul/thundergate/include/rbdi.h: 22
class struct_rbdi_mode(Structure):
    pass

# /home/saul/thundergate/include/rbdi.h: 34
class struct_rbdi_status(Structure):
    pass

struct_rbdi_status.__slots__ = [
    'reserved',
    'receive_bds_available_on_disabled_rbd_ring',
    'reserved2',
]
struct_rbdi_status._fields_ = [
    ('reserved', u32, 29),
    ('receive_bds_available_on_disabled_rbd_ring', u32, 1),
    ('reserved2', u32, 2),
]

# /home/saul/thundergate/include/rbdi.h: 40
class struct_rbdi_ring_replenish_threshold(Structure):
    pass

struct_rbdi_ring_replenish_threshold.__slots__ = [
    'reserved',
    'count',
]
struct_rbdi_ring_replenish_threshold._fields_ = [
    ('reserved', u32, 22),
    ('count', u32, 10),
]

# /home/saul/thundergate/include/rbdi.h: 45
class struct_rbdi_regs(Structure):
    pass

struct_rbdi_regs.__slots__ = [
    'mode',
    'status',
    'local_jumbo_rbd_pi',
    'local_std_rbd_pi',
    'local_mini_rbd_pi',
    'mini_ring_replenish_threshold',
    'std_ring_replenish_threshold',
    'jumbo_ring_replenish_threshold',
    'reserved',
    'std_ring_replenish_watermark',
    'jumbo_ring_replenish_watermark',
]
struct_rbdi_regs._fields_ = [
    ('mode', struct_rbdi_mode),
    ('status', struct_rbdi_status),
    ('local_jumbo_rbd_pi', u32),
    ('local_std_rbd_pi', u32),
    ('local_mini_rbd_pi', u32),
    ('mini_ring_replenish_threshold', struct_rbdi_ring_replenish_threshold),
    ('std_ring_replenish_threshold', struct_rbdi_ring_replenish_threshold),
    ('jumbo_ring_replenish_threshold', struct_rbdi_ring_replenish_threshold),
    ('reserved', u32 * (224 >> 2)),
    ('std_ring_replenish_watermark', struct_rbdi_ring_replenish_threshold),
    ('jumbo_ring_replenish_watermark', struct_rbdi_ring_replenish_threshold),
]

# /home/saul/thundergate/include/rbdrules.h: 24
class struct_rbd_rule(Structure):
    pass

struct_rbd_rule.__slots__ = [
    'enabled',
    'and_with_next',
    'p1',
    'p2',
    'p3',
    'mask',
    'discard',
    'map',
    'reserved',
    'op',
    'header',
    'frame_class',
    'offset',
]
struct_rbd_rule._fields_ = [
    ('enabled', u32, 1),
    ('and_with_next', u32, 1),
    ('p1', u32, 1),
    ('p2', u32, 1),
    ('p3', u32, 1),
    ('mask', u32, 1),
    ('discard', u32, 1),
    ('map', u32, 1),
    ('reserved', u32, 6),
    ('op', u32, 2),
    ('header', u32, 3),
    ('frame_class', u32, 5),
    ('offset', u32, 8),
]

# /home/saul/thundergate/include/rbdrules.h: 40
class struct_rbd_value_mask(Structure):
    pass

struct_rbd_value_mask.__slots__ = [
    'mask',
    'value',
]
struct_rbd_value_mask._fields_ = [
    ('mask', u16),
    ('value', u16),
]

# /home/saul/thundergate/include/rcb.h: 22
class struct_rcb_flags(Structure):
    pass

struct_rcb_flags.__slots__ = [
    'reserved',
    'disabled',
    'reserved2',
]
struct_rcb_flags._fields_ = [
    ('reserved', u16, 1),
    ('disabled', u16, 1),
    ('reserved2', u16, 14),
]

# /home/saul/thundergate/include/rcb.h: 28
class struct_rcb(Structure):
    pass

struct_rcb.__slots__ = [
    'addr_hi',
    'addr_low',
    'flags',
    'max_len',
    'nic_addr',
]
struct_rcb._fields_ = [
    ('addr_hi', u32),
    ('addr_low', u32),
    ('flags', struct_rcb_flags),
    ('max_len', u16),
    ('nic_addr', u32),
]

# /home/saul/thundergate/include/rdc.h: 22
class struct_rdc_mode(Structure):
    pass

# /home/saul/thundergate/include/rdc.h: 34
class struct_rdc_regs(Structure):
    pass

struct_rdc_regs.__slots__ = [
    'mode',
]
struct_rdc_regs._fields_ = [
    ('mode', struct_rdc_mode),
]

# /home/saul/thundergate/include/rdi.h: 22
class struct_rdi_mode(Structure):
    pass

struct_rdi_mode.__slots__ = [
    'reserved',
    'illegal_return_ring_size',
    'frame_size_too_large_for_bd',
    'reserved2',
    'enable',
    'reset',
]
struct_rdi_mode._fields_ = [
    ('reserved', u32, 27),
    ('illegal_return_ring_size', u32, 1),
    ('frame_size_too_large_for_bd', u32, 1),
    ('reserved2', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/rdi.h: 31
class struct_rdi_status(Structure):
    pass

struct_rdi_status.__slots__ = [
    'reserved',
    'illegal_return_ring_size',
    'frame_size_too_large_for_bd',
    'reserved2',
]
struct_rdi_status._fields_ = [
    ('reserved', u32, 27),
    ('illegal_return_ring_size', u32, 1),
    ('frame_size_too_large_for_bd', u32, 1),
    ('reserved2', u32, 3),
]

# /home/saul/thundergate/include/rdi.h: 38
class struct_rcb_registers(Structure):
    pass

struct_rcb_registers.__slots__ = [
    'host_addr_hi',
    'host_addr_low',
    'nic_addr',
]
struct_rcb_registers._fields_ = [
    ('host_addr_hi', u32),
    ('host_addr_low', u32),
    ('nic_addr', u32),
]

# /home/saul/thundergate/include/rdi.h: 50
class struct_rdi_regs(Structure):
    pass

struct_rdi_regs.__slots__ = [
    'mode',
    'status',
    'unknown',
    'jumbo_rcb',
    'std_rcb',
    'mini_rcb',
    'local_jumbo_rbd_ci',
    'local_std_rbd_ci',
    'local_mini_rbd_ci',
    'unknown2',
    'local_rr_pi',
    'hw_diag',
]
struct_rdi_regs._fields_ = [
    ('mode', struct_rdi_mode),
    ('status', struct_rdi_status),
    ('unknown', u32 * 14),
    ('jumbo_rcb', struct_rcb_registers),
    ('std_rcb', struct_rcb_registers),
    ('mini_rcb', struct_rcb_registers),
    ('local_jumbo_rbd_ci', u32),
    ('local_std_rbd_ci', u32),
    ('local_mini_rbd_ci', u32),
    ('unknown2', u32),
    ('local_rr_pi', u32 * 16),
    ('hw_diag', u32),
]

# /home/saul/thundergate/include/rdma.h: 24
class struct_rdma_mode(Structure):
    pass

struct_rdma_mode.__slots__ = [
    'reserved',
    'in_band_vtag_enable',
    'hardware_ipv6_post_dma_processing_enable',
    'hardware_ipv4_post_dma_processing_enable',
    'post_dma_debug_enable',
    'address_overflow_error_logging_enable',
    'mmrr_disable',
    'jumbo_2k_mmrr_mode',
    'reserved2',
    'pci_request_burst_length',
    'reserved3',
    'mbuf_sbd_corruption_attn_enable',
    'mbuf_rbd_corruption_attn_enable',
    'bd_sbd_corruption_attn_enable',
    'read_dma_pci_x_split_transaction_timeout_expired_attention_enable',
    'read_dma_local_memory_write_longer_than_dma_length_attention_enable',
    'read_dma_pci_fifo_overread_attention_enable',
    'read_dma_pci_fifo_underrun_attention_enable',
    'read_dma_pci_fifo_overrun_attention_enable',
    'read_dma_pci_host_address_overflow_error_attention_enable',
    'read_dma_pci_parity_error_attention_enable',
    'read_dma_pci_master_abort_attention_enable',
    'read_dma_pci_target_abort_attention_enable',
    'enable',
    'reset',
]
struct_rdma_mode._fields_ = [
    ('reserved', u32, 2),
    ('in_band_vtag_enable', u32, 1),
    ('hardware_ipv6_post_dma_processing_enable', u32, 1),
    ('hardware_ipv4_post_dma_processing_enable', u32, 1),
    ('post_dma_debug_enable', u32, 1),
    ('address_overflow_error_logging_enable', u32, 1),
    ('mmrr_disable', u32, 1),
    ('jumbo_2k_mmrr_mode', u32, 1),
    ('reserved2', u32, 5),
    ('pci_request_burst_length', u32, 2),
    ('reserved3', u32, 2),
    ('mbuf_sbd_corruption_attn_enable', u32, 1),
    ('mbuf_rbd_corruption_attn_enable', u32, 1),
    ('bd_sbd_corruption_attn_enable', u32, 1),
    ('read_dma_pci_x_split_transaction_timeout_expired_attention_enable', u32, 1),
    ('read_dma_local_memory_write_longer_than_dma_length_attention_enable', u32, 1),
    ('read_dma_pci_fifo_overread_attention_enable', u32, 1),
    ('read_dma_pci_fifo_underrun_attention_enable', u32, 1),
    ('read_dma_pci_fifo_overrun_attention_enable', u32, 1),
    ('read_dma_pci_host_address_overflow_error_attention_enable', u32, 1),
    ('read_dma_pci_parity_error_attention_enable', u32, 1),
    ('read_dma_pci_master_abort_attention_enable', u32, 1),
    ('read_dma_pci_target_abort_attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/rdma.h: 52
class struct_rdma_status(Structure):
    pass

struct_rdma_status.__slots__ = [
    'reserved',
    'mbuf_sbd_corruption_attention',
    'mbuf_rbd_corruption_attention',
    'bd_sbd_corruption_attention',
    'read_dma_pci_x_split_transaction_timeout_expired',
    'read_dma_local_memory_write_longer_than_dma_length_error',
    'read_dma_pci_fifo_overread_error',
    'read_dma_pci_fifo_underrun_error',
    'read_dma_pci_fifo_overrun_error',
    'read_dma_pci_host_address_overflow_error',
    'read_dma_completion_timer_timeout',
    'read_dma_completer_abort',
    'read_dma_unsupported_request',
    'reserved2',
]
struct_rdma_status._fields_ = [
    ('reserved', u32, 18),
    ('mbuf_sbd_corruption_attention', u32, 1),
    ('mbuf_rbd_corruption_attention', u32, 1),
    ('bd_sbd_corruption_attention', u32, 1),
    ('read_dma_pci_x_split_transaction_timeout_expired', u32, 1),
    ('read_dma_local_memory_write_longer_than_dma_length_error', u32, 1),
    ('read_dma_pci_fifo_overread_error', u32, 1),
    ('read_dma_pci_fifo_underrun_error', u32, 1),
    ('read_dma_pci_fifo_overrun_error', u32, 1),
    ('read_dma_pci_host_address_overflow_error', u32, 1),
    ('read_dma_completion_timer_timeout', u32, 1),
    ('read_dma_completer_abort', u32, 1),
    ('read_dma_unsupported_request', u32, 1),
    ('reserved2', u32, 2),
]

# /home/saul/thundergate/include/rdma.h: 69
class struct_rdma_programmable_ipv6_extension_header(Structure):
    pass

struct_rdma_programmable_ipv6_extension_header.__slots__ = [
    'type_2_en',
    'type_1_en',
    'reserved16',
    'ext_hdr_type_2',
    'ext_hdr_type_1',
]
struct_rdma_programmable_ipv6_extension_header._fields_ = [
    ('type_2_en', u32, 1),
    ('type_1_en', u32, 1),
    ('reserved16', u32, 14),
    ('ext_hdr_type_2', u32, 8),
    ('ext_hdr_type_1', u32, 8),
]

# /home/saul/thundergate/include/rdma.h: 77
class struct_rdma_rstates_debug(Structure):
    pass

struct_rdma_rstates_debug.__slots__ = [
    'reserved6',
    'rstate3',
    'reserved3',
    'rstate1',
]
struct_rdma_rstates_debug._fields_ = [
    ('reserved6', u32, 26),
    ('rstate3', u32, 2),
    ('reserved3', u32, 1),
    ('rstate1', u32, 3),
]

# /home/saul/thundergate/include/rdma.h: 84
class struct_rdma_rstate2_debug(Structure):
    pass

struct_rdma_rstate2_debug.__slots__ = [
    'reserved5',
    'rstate2',
]
struct_rdma_rstate2_debug._fields_ = [
    ('reserved5', u32, 27),
    ('rstate2', u32, 5),
]

# /home/saul/thundergate/include/rdma.h: 89
class struct_rdma_bd_status_debug(Structure):
    pass

struct_rdma_bd_status_debug.__slots__ = [
    'reserved3',
    'bd_non_mbuf',
    'fst_bd_mbuf',
    'lst_bd_mbuf',
]
struct_rdma_bd_status_debug._fields_ = [
    ('reserved3', u32, 29),
    ('bd_non_mbuf', u32, 1),
    ('fst_bd_mbuf', u32, 1),
    ('lst_bd_mbuf', u32, 1),
]

# /home/saul/thundergate/include/rdma.h: 96
class struct_rdma_req_ptr_debug(Structure):
    pass

struct_rdma_req_ptr_debug.__slots__ = [
    'ih_dmad_length',
    'reserved10',
    'txmbuf_left',
    'rh_dmad_load_en',
    'rftq_d_dmad_pnt',
    'rftq_b_dmad_pnt',
]
struct_rdma_req_ptr_debug._fields_ = [
    ('ih_dmad_length', u32, 16),
    ('reserved10', u32, 6),
    ('txmbuf_left', u32, 6),
    ('rh_dmad_load_en', u32, 1),
    ('rftq_d_dmad_pnt', u32, 2),
    ('rftq_b_dmad_pnt', u32, 1),
]

# /home/saul/thundergate/include/rdma.h: 105
class struct_rdma_hold_d_dmad_debug(Structure):
    pass

struct_rdma_hold_d_dmad_debug.__slots__ = [
    'reserved2',
    'rhold_d_dmad',
]
struct_rdma_hold_d_dmad_debug._fields_ = [
    ('reserved2', u32, 30),
    ('rhold_d_dmad', u32, 2),
]

# /home/saul/thundergate/include/rdma.h: 110
class struct_rdma_length_and_address_index_debug(Structure):
    pass

struct_rdma_length_and_address_index_debug.__slots__ = [
    'rdma_rd_length',
    'mbuf_addr_idx',
]
struct_rdma_length_and_address_index_debug._fields_ = [
    ('rdma_rd_length', u32, 16),
    ('mbuf_addr_idx', u32, 16),
]

# /home/saul/thundergate/include/rdma.h: 115
class struct_rdma_mbuf_byte_count_debug(Structure):
    pass

struct_rdma_mbuf_byte_count_debug.__slots__ = [
    'reserved4',
    'rmbuf_byte_cnt',
]
struct_rdma_mbuf_byte_count_debug._fields_ = [
    ('reserved4', u32, 28),
    ('rmbuf_byte_cnt', u32, 4),
]

# /home/saul/thundergate/include/rdma.h: 120
class struct_rdma_pcie_mbuf_byte_count_debug(Structure):
    pass

struct_rdma_pcie_mbuf_byte_count_debug.__slots__ = [
    'lt_term',
    'reserved27',
    'lt_too_lg',
    'lt_dma_reload',
    'lt_dma_good',
    'cur_trans_active',
    'drpcireq',
    'dr_pci_word_swap',
    'dr_pci_byte_swap',
    'new_slow_core_clk_mode',
    'rbd_non_mbuf',
    'rfst_bd_mbuf',
    'rlst_bd_mbuf',
    'dr_pci_len',
]
struct_rdma_pcie_mbuf_byte_count_debug._fields_ = [
    ('lt_term', u32, 4),
    ('reserved27', u32, 1),
    ('lt_too_lg', u32, 1),
    ('lt_dma_reload', u32, 1),
    ('lt_dma_good', u32, 1),
    ('cur_trans_active', u32, 1),
    ('drpcireq', u32, 1),
    ('dr_pci_word_swap', u32, 1),
    ('dr_pci_byte_swap', u32, 1),
    ('new_slow_core_clk_mode', u32, 1),
    ('rbd_non_mbuf', u32, 1),
    ('rfst_bd_mbuf', u32, 1),
    ('rlst_bd_mbuf', u32, 1),
    ('dr_pci_len', u32, 16),
]

# /home/saul/thundergate/include/rdma.h: 137
class struct_rdma_pcie_read_request_address_debug(Structure):
    pass

struct_rdma_pcie_read_request_address_debug.__slots__ = [
    'dr_pci_ad_hi',
    'dr_pci_ad_lo',
]
struct_rdma_pcie_read_request_address_debug._fields_ = [
    ('dr_pci_ad_hi', u32, 16),
    ('dr_pci_ad_lo', u32, 16),
]

# /home/saul/thundergate/include/rdma.h: 142
class struct_rdma_fifo1_debug(Structure):
    pass

struct_rdma_fifo1_debug.__slots__ = [
    'reserved8',
    'c_write_addr',
]
struct_rdma_fifo1_debug._fields_ = [
    ('reserved8', u32, 24),
    ('c_write_addr', u32, 8),
]

# /home/saul/thundergate/include/rdma.h: 147
class struct_rdma_fifo2_debug(Structure):
    pass

struct_rdma_fifo2_debug.__slots__ = [
    'reserved16',
    'rlctrl_in',
    'c_read_addr',
]
struct_rdma_fifo2_debug._fields_ = [
    ('reserved16', u32, 16),
    ('rlctrl_in', u32, 8),
    ('c_read_addr', u32, 8),
]

# /home/saul/thundergate/include/rdma.h: 153
class struct_rdma_packet_request_debug_1(Structure):
    pass

struct_rdma_packet_request_debug_1.__slots__ = [
    'reserved8',
    'pkt_req_cnt',
]
struct_rdma_packet_request_debug_1._fields_ = [
    ('reserved8', u32, 24),
    ('pkt_req_cnt', u32, 8),
]

# /home/saul/thundergate/include/rdma.h: 158
class struct_rdma_packet_request_debug_2(Structure):
    pass

struct_rdma_packet_request_debug_2.__slots__ = [
    'sdc_ack_cnt',
]
struct_rdma_packet_request_debug_2._fields_ = [
    ('sdc_ack_cnt', u32),
]

# /home/saul/thundergate/include/rdma.h: 162
class struct_rdma_packet_request_debug_3(Structure):
    pass

struct_rdma_packet_request_debug_3.__slots__ = [
    'cs',
    'reserved26',
    'lt_fst_seg',
    'lt_lst_seg',
    'lt_mem_ip_hdr_ofst',
    'lt_mem_tcp_hdr_ofst',
    'reserved7',
    'pre_sdcq_pkt_cnt',
]
struct_rdma_packet_request_debug_3._fields_ = [
    ('cs', u32, 4),
    ('reserved26', u32, 2),
    ('lt_fst_seg', u32, 1),
    ('lt_lst_seg', u32, 1),
    ('lt_mem_ip_hdr_ofst', u32, 8),
    ('lt_mem_tcp_hdr_ofst', u32, 8),
    ('reserved7', u32, 1),
    ('pre_sdcq_pkt_cnt', u32, 7),
]

# /home/saul/thundergate/include/rdma.h: 173
class struct_rdma_tcp_checksum_debug(Structure):
    pass

struct_rdma_tcp_checksum_debug.__slots__ = [
    'reserved30',
    'fd_addr_req',
    'lt_mem_data_ofst',
    'lt_mem_tcp_chksum',
]
struct_rdma_tcp_checksum_debug._fields_ = [
    ('reserved30', u32, 2),
    ('fd_addr_req', u32, 6),
    ('lt_mem_data_ofst', u32, 8),
    ('lt_mem_tcp_chksum', u32, 16),
]

# /home/saul/thundergate/include/rdma.h: 180
class struct_rdma_ip_tcp_header_checksum_debug(Structure):
    pass

struct_rdma_ip_tcp_header_checksum_debug.__slots__ = [
    'lt_mem_ip_chksum',
    'lt_mem_tcphdr_chksum',
]
struct_rdma_ip_tcp_header_checksum_debug._fields_ = [
    ('lt_mem_ip_chksum', u32, 16),
    ('lt_mem_tcphdr_chksum', u32, 16),
]

# /home/saul/thundergate/include/rdma.h: 185
class struct_rdma_pseudo_checksum_debug(Structure):
    pass

struct_rdma_pseudo_checksum_debug.__slots__ = [
    'lt_mem_pse_chksum_no_tcplen',
    'lt_mem_pkt_len',
]
struct_rdma_pseudo_checksum_debug._fields_ = [
    ('lt_mem_pse_chksum_no_tcplen', u32, 16),
    ('lt_mem_pkt_len', u32, 16),
]

# /home/saul/thundergate/include/rdma.h: 190
class struct_rdma_mbuf_address_debug(Structure):
    pass

struct_rdma_mbuf_address_debug.__slots__ = [
    'reserved30',
    'mbuf1_addr',
    'reserved22',
    'mbuf0_addr',
    'reserved14',
    'pre_mbuf1_addr',
    'reserved6',
    'pre_mbuf0_addr',
]
struct_rdma_mbuf_address_debug._fields_ = [
    ('reserved30', u32, 2),
    ('mbuf1_addr', u32, 6),
    ('reserved22', u32, 2),
    ('mbuf0_addr', u32, 6),
    ('reserved14', u32, 2),
    ('pre_mbuf1_addr', u32, 6),
    ('reserved6', u32, 2),
    ('pre_mbuf0_addr', u32, 6),
]

# /home/saul/thundergate/include/rdma.h: 201
class struct_rdma_misc_ctrl_1(Structure):
    pass

struct_rdma_misc_ctrl_1.__slots__ = [
    'txmbuf_margin',
    'select_fed_enable',
    'fifo_high_mark',
    'fifo_low_mark',
    'slow_clock_fix_disable',
    'cq25155_fix_en',
    'late_col_fix_en',
    'sdi_shortq_en',
]
struct_rdma_misc_ctrl_1._fields_ = [
    ('txmbuf_margin', u32, 11),
    ('select_fed_enable', u32, 1),
    ('fifo_high_mark', u32, 8),
    ('fifo_low_mark', u32, 8),
    ('slow_clock_fix_disable', u32, 1),
    ('cq25155_fix_en', u32, 1),
    ('late_col_fix_en', u32, 1),
    ('sdi_shortq_en', u32, 1),
]

# /home/saul/thundergate/include/rdma.h: 212
class struct_rdma_misc_ctrl_2(Structure):
    pass

struct_rdma_misc_ctrl_2.__slots__ = [
    'fifo_threshold_bd_req',
    'fifo_threshold_mbuf_req',
    'reserved14',
    'mbuf_threshold_mbuf_req',
    'reserved7',
    'clock_req_fix_en',
    'mbuf_threshold_clk_req',
]
struct_rdma_misc_ctrl_2._fields_ = [
    ('fifo_threshold_bd_req', u32, 8),
    ('fifo_threshold_mbuf_req', u32, 8),
    ('reserved14', u32, 2),
    ('mbuf_threshold_mbuf_req', u32, 6),
    ('reserved7', u32, 1),
    ('clock_req_fix_en', u32, 1),
    ('mbuf_threshold_clk_req', u32, 6),
]

# /home/saul/thundergate/include/rdma.h: 222
class struct_rdma_misc_ctrl_3(Structure):
    pass

struct_rdma_misc_ctrl_3.__slots__ = [
    'reserved6',
    'cq33951_fix_dis',
    'cq30888_fix1_en',
    'cq30888_fix2_en',
    'cq30808_fix_en',
    'reserved1',
    'reserved0',
]
struct_rdma_misc_ctrl_3._fields_ = [
    ('reserved6', u32, 26),
    ('cq33951_fix_dis', u32, 1),
    ('cq30888_fix1_en', u32, 1),
    ('cq30888_fix2_en', u32, 1),
    ('cq30808_fix_en', u32, 1),
    ('reserved1', u32, 1),
    ('reserved0', u32, 1),
]

# /home/saul/thundergate/include/rdma.h: 232
class struct_rdma_regs(Structure):
    pass

struct_rdma_regs.__slots__ = [
    'mode',
    'status',
    'programmable_ipv6_extension_header',
    'rstates_debug',
    'rstate2_debug',
    'bd_status_debug',
    'req_ptr_debug',
    'hold_d_dmad_debug',
    'length_and_address_index_debug',
    'mbuf_byte_count_debug',
    'pcie_mbuf_byte_count_debug',
    'pcie_read_request_address_debug',
    'pcie_dma_request_length_debug',
    'fifo1_debug',
    'fifo2_debug',
    'ofs_3c',
    'packet_request_debug_1',
    'packet_request_debug_2',
    'packet_request_debug_3',
    'tcp_checksum_debug',
    'ip_tcp_header_checksum_debug',
    'pseudo_checksum_debug',
    'mbuf_address_debug',
    'ofs_5c',
    'ofs_60',
    'ofs_64',
    'ofs_68',
    'ofs_6c',
    'ofs_70',
    'ofs_74',
    'ofs_78',
    'ofs_7c',
    'ofs_80',
    'ofs_84',
    'ofs_88',
    'ofs_8c',
    'ofs_90',
    'ofs_94',
    'ofs_98',
    'ofs_9c',
    'ofs_a0',
    'ofs_a4',
    'ofs_a8',
    'ofs_ac',
    'ofs_b0',
    'ofs_b4',
    'ofs_b8',
    'ofs_bc',
    'ofs_c0',
    'ofs_c4',
    'ofs_c8',
    'ofs_cc',
    'ofs_d0',
    'ofs_d4',
    'ofs_d8',
    'ofs_dc',
    'ofs_e0',
    'ofs_e4',
    'ofs_e8',
    'ofs_ec',
    'ofs_f0',
    'ofs_f4',
    'ofs_f8',
    'ofs_fc',
]
struct_rdma_regs._fields_ = [
    ('mode', struct_rdma_mode),
    ('status', struct_rdma_status),
    ('programmable_ipv6_extension_header', struct_rdma_programmable_ipv6_extension_header),
    ('rstates_debug', struct_rdma_rstates_debug),
    ('rstate2_debug', struct_rdma_rstate2_debug),
    ('bd_status_debug', struct_rdma_bd_status_debug),
    ('req_ptr_debug', struct_rdma_req_ptr_debug),
    ('hold_d_dmad_debug', struct_rdma_hold_d_dmad_debug),
    ('length_and_address_index_debug', struct_rdma_length_and_address_index_debug),
    ('mbuf_byte_count_debug', struct_rdma_mbuf_byte_count_debug),
    ('pcie_mbuf_byte_count_debug', struct_rdma_pcie_mbuf_byte_count_debug),
    ('pcie_read_request_address_debug', struct_rdma_pcie_read_request_address_debug),
    ('pcie_dma_request_length_debug', u32),
    ('fifo1_debug', struct_rdma_fifo1_debug),
    ('fifo2_debug', struct_rdma_fifo2_debug),
    ('ofs_3c', u32),
    ('packet_request_debug_1', struct_rdma_packet_request_debug_1),
    ('packet_request_debug_2', struct_rdma_packet_request_debug_2),
    ('packet_request_debug_3', struct_rdma_packet_request_debug_3),
    ('tcp_checksum_debug', struct_rdma_tcp_checksum_debug),
    ('ip_tcp_header_checksum_debug', struct_rdma_ip_tcp_header_checksum_debug),
    ('pseudo_checksum_debug', struct_rdma_pseudo_checksum_debug),
    ('mbuf_address_debug', struct_rdma_mbuf_address_debug),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('ofs_6c', u32),
    ('ofs_70', u32),
    ('ofs_74', u32),
    ('ofs_78', u32),
    ('ofs_7c', u32),
    ('ofs_80', u32),
    ('ofs_84', u32),
    ('ofs_88', u32),
    ('ofs_8c', u32),
    ('ofs_90', u32),
    ('ofs_94', u32),
    ('ofs_98', u32),
    ('ofs_9c', u32),
    ('ofs_a0', u32),
    ('ofs_a4', u32),
    ('ofs_a8', u32),
    ('ofs_ac', u32),
    ('ofs_b0', u32),
    ('ofs_b4', u32),
    ('ofs_b8', u32),
    ('ofs_bc', u32),
    ('ofs_c0', u32),
    ('ofs_c4', u32),
    ('ofs_c8', u32),
    ('ofs_cc', u32),
    ('ofs_d0', u32),
    ('ofs_d4', u32),
    ('ofs_d8', u32),
    ('ofs_dc', u32),
    ('ofs_e0', u32),
    ('ofs_e4', u32),
    ('ofs_e8', u32),
    ('ofs_ec', u32),
    ('ofs_f0', u32),
    ('ofs_f4', u32),
    ('ofs_f8', u32),
    ('ofs_fc', u32),
]

# /home/saul/thundergate/include/rlp.h: 22
class struct_receive_list_placement_mode(Structure):
    pass

struct_receive_list_placement_mode.__slots__ = [
    'reserved',
    'stats_overflow_attention_enable',
    'mapping_out_of_range_attention_enable',
    'class_zero_attention_enable',
    'enable',
    'reset',
]
struct_receive_list_placement_mode._fields_ = [
    ('reserved', u32, 27),
    ('stats_overflow_attention_enable', u32, 1),
    ('mapping_out_of_range_attention_enable', u32, 1),
    ('class_zero_attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/rlp.h: 31
class struct_receive_list_placement_status(Structure):
    pass

struct_receive_list_placement_status.__slots__ = [
    'reserved',
    'stats_overflow_attention',
    'mapping_out_of_range_attention',
    'class_zero_attention',
    'reserved2',
]
struct_receive_list_placement_status._fields_ = [
    ('reserved', u32, 27),
    ('stats_overflow_attention', u32, 1),
    ('mapping_out_of_range_attention', u32, 1),
    ('class_zero_attention', u32, 1),
    ('reserved2', u32, 2),
]

# /home/saul/thundergate/include/rlp.h: 39
class struct_receive_selector_not_empty_bits(Structure):
    pass

struct_receive_selector_not_empty_bits.__slots__ = [
    'reserved',
    'list_non_empty_bits',
]
struct_receive_selector_not_empty_bits._fields_ = [
    ('reserved', u32, 16),
    ('list_non_empty_bits', u32, 16),
]

# /home/saul/thundergate/include/rlp.h: 44
class struct_receive_list_placement_configuration(Structure):
    pass

struct_receive_list_placement_configuration.__slots__ = [
    'reserved',
    'default_interrupt_distribution_queue',
    'bad_frames_class',
    'number_of_active_lists',
    'number_of_lists_per_distribution_group',
]
struct_receive_list_placement_configuration._fields_ = [
    ('reserved', u32, 17),
    ('default_interrupt_distribution_queue', u32, 2),
    ('bad_frames_class', u32, 5),
    ('number_of_active_lists', u32, 5),
    ('number_of_lists_per_distribution_group', u32, 3),
]

# /home/saul/thundergate/include/rlp.h: 52
class struct_receive_list_placement_statistics_control(Structure):
    pass

struct_receive_list_placement_statistics_control.__slots__ = [
    'reserved',
    'statistics_clear',
    'reserved2',
    'statistics_enable',
]
struct_receive_list_placement_statistics_control._fields_ = [
    ('reserved', u32, 29),
    ('statistics_clear', u32, 1),
    ('reserved2', u32, 1),
    ('statistics_enable', u32, 1),
]

# /home/saul/thundergate/include/rlp.h: 59
class struct_receive_list_placement_statistics_enable_mask(Structure):
    pass

# /home/saul/thundergate/include/rlp.h: 79
class struct_receive_list_placement_statistics_increment_mask(Structure):
    pass

struct_receive_list_placement_statistics_increment_mask.__slots__ = [
    'reserved',
    'counters_increment_mask',
    'reserved2',
    'counters_increment_mask_again',
]
struct_receive_list_placement_statistics_increment_mask._fields_ = [
    ('reserved', u32, 10),
    ('counters_increment_mask', u32, 6),
    ('reserved2', u32, 15),
    ('counters_increment_mask_again', u32, 1),
]

# /home/saul/thundergate/include/rlp.h: 86
class struct_receive_list_local_statistics_counter(Structure):
    pass

struct_receive_list_local_statistics_counter.__slots__ = [
    'reserved',
    'counters_value',
]
struct_receive_list_local_statistics_counter._fields_ = [
    ('reserved', u32, 22),
    ('counters_value', u32, 10),
]

# /home/saul/thundergate/include/rlp.h: 91
class struct_receive_list_lock(Structure):
    pass

struct_receive_list_lock.__slots__ = [
    'grant',
    'request',
]
struct_receive_list_lock._fields_ = [
    ('grant', u32, 16),
    ('request', u32, 16),
]

# /home/saul/thundergate/include/rlp.h: 107
class struct_anon_6(Structure):
    pass

struct_anon_6.__slots__ = [
    'list_head',
    'list_tail',
    'list_count',
    'unknown',
]
struct_anon_6._fields_ = [
    ('list_head', u32),
    ('list_tail', u32),
    ('list_count', u32),
    ('unknown', u32),
]

# /home/saul/thundergate/include/rlp.h: 96
class struct_rlp_regs(Structure):
    pass

struct_rlp_regs.__slots__ = [
    'mode',
    'status',
    'lock',
    'selector_not_empty_bits',
    'config',
    'stats_control',
    'stats_enable_mask',
    'stats_increment_mask',
    'unknown',
    'rx_selector',
    'stat_counter',
]
struct_rlp_regs._fields_ = [
    ('mode', struct_receive_list_placement_mode),
    ('status', struct_receive_list_placement_status),
    ('lock', struct_receive_list_lock),
    ('selector_not_empty_bits', struct_receive_selector_not_empty_bits),
    ('config', struct_receive_list_placement_configuration),
    ('stats_control', struct_receive_list_placement_statistics_control),
    ('stats_enable_mask', struct_receive_list_placement_statistics_enable_mask),
    ('stats_increment_mask', struct_receive_list_placement_statistics_increment_mask),
    ('unknown', u32 * 56),
    ('rx_selector', struct_anon_6 * 16),
    ('stat_counter', struct_receive_list_local_statistics_counter * 23),
]

# /home/saul/thundergate/include/rss.h: 22
class struct_rss_ind_table_1(Structure):
    pass

struct_rss_ind_table_1.__slots__ = [
    'reserved30',
    'table_entry0',
    'reserved26',
    'table_entry1',
    'reserved22',
    'table_entry2',
    'reserved18',
    'table_entry3',
    'reserved14',
    'table_entry4',
    'reserved10',
    'table_entry5',
    'reserved6',
    'table_entry6',
    'reserved2',
    'table_entry7',
]
struct_rss_ind_table_1._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry0', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry1', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry2', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry3', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry4', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry5', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry6', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry7', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 40
class struct_rss_ind_table_2(Structure):
    pass

struct_rss_ind_table_2.__slots__ = [
    'reserved30',
    'table_entry8',
    'reserved26',
    'table_entry9',
    'reserved22',
    'table_entry10',
    'reserved18',
    'table_entry11',
    'reserved14',
    'table_entry12',
    'reserved10',
    'table_entry13',
    'reserved6',
    'table_entry14',
    'reserved2',
    'table_entry15',
]
struct_rss_ind_table_2._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry8', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry9', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry10', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry11', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry12', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry13', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry14', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry15', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 58
class struct_rss_ind_table_3(Structure):
    pass

struct_rss_ind_table_3.__slots__ = [
    'reserved30',
    'table_entry16',
    'reserved26',
    'table_entry17',
    'reserved22',
    'table_entry18',
    'reserved18',
    'table_entry19',
    'reserved14',
    'table_entry20',
    'reserved10',
    'table_entry21',
    'reserved6',
    'table_entry22',
    'reserved2',
    'table_entry23',
]
struct_rss_ind_table_3._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry16', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry17', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry18', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry19', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry20', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry21', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry22', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry23', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 76
class struct_rss_ind_table_4(Structure):
    pass

struct_rss_ind_table_4.__slots__ = [
    'reserved30',
    'table_entry24',
    'reserved26',
    'table_entry25',
    'reserved22',
    'table_entry26',
    'reserved18',
    'table_entry27',
    'reserved14',
    'table_entry28',
    'reserved10',
    'table_entry29',
    'reserved6',
    'table_entry30',
    'reserved2',
    'table_entry31',
]
struct_rss_ind_table_4._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry24', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry25', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry26', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry27', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry28', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry29', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry30', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry31', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 94
class struct_rss_ind_table_5(Structure):
    pass

struct_rss_ind_table_5.__slots__ = [
    'reserved30',
    'table_entry32',
    'reserved26',
    'table_entry33',
    'reserved22',
    'table_entry34',
    'reserved18',
    'table_entry35',
    'reserved14',
    'table_entry36',
    'reserved10',
    'table_entry37',
    'reserved6',
    'table_entry38',
    'reserved2',
    'table_entry39',
]
struct_rss_ind_table_5._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry32', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry33', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry34', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry35', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry36', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry37', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry38', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry39', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 112
class struct_rss_ind_table_6(Structure):
    pass

struct_rss_ind_table_6.__slots__ = [
    'reserved30',
    'table_entry40',
    'reserved26',
    'table_entry41',
    'reserved22',
    'table_entry42',
    'reserved18',
    'table_entry43',
    'reserved14',
    'table_entry44',
    'reserved10',
    'table_entry45',
    'reserved6',
    'table_entry46',
    'reserved2',
    'table_entry47',
]
struct_rss_ind_table_6._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry40', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry41', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry42', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry43', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry44', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry45', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry46', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry47', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 130
class struct_rss_ind_table_7(Structure):
    pass

struct_rss_ind_table_7.__slots__ = [
    'reserved30',
    'table_entry48',
    'reserved26',
    'table_entry49',
    'reserved22',
    'table_entry50',
    'reserved18',
    'table_entry51',
    'reserved14',
    'table_entry52',
    'reserved10',
    'table_entry53',
    'reserved6',
    'table_entry54',
    'reserved2',
    'table_entry55',
]
struct_rss_ind_table_7._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry48', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry49', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry50', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry51', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry52', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry53', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry54', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry55', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 148
class struct_rss_ind_table_8(Structure):
    pass

struct_rss_ind_table_8.__slots__ = [
    'reserved30',
    'table_entry56',
    'reserved26',
    'table_entry57',
    'reserved22',
    'table_entry58',
    'reserved18',
    'table_entry59',
    'reserved14',
    'table_entry60',
    'reserved10',
    'table_entry61',
    'reserved6',
    'table_entry62',
    'reserved2',
    'table_entry63',
]
struct_rss_ind_table_8._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry56', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry57', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry58', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry59', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry60', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry61', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry62', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry63', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 166
class struct_rss_ind_table_9(Structure):
    pass

struct_rss_ind_table_9.__slots__ = [
    'reserved30',
    'table_entry64',
    'reserved26',
    'table_entry65',
    'reserved22',
    'table_entry66',
    'reserved18',
    'table_entry67',
    'reserved14',
    'table_entry68',
    'reserved10',
    'table_entry69',
    'reserved6',
    'table_entry70',
    'reserved2',
    'table_entry71',
]
struct_rss_ind_table_9._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry64', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry65', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry66', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry67', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry68', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry69', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry70', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry71', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 185
class struct_rss_ind_table_10(Structure):
    pass

struct_rss_ind_table_10.__slots__ = [
    'reserved30',
    'table_entry72',
    'reserved26',
    'table_entry73',
    'reserved22',
    'table_entry74',
    'reserved18',
    'table_entry75',
    'reserved14',
    'table_entry76',
    'reserved10',
    'table_entry77',
    'reserved6',
    'table_entry78',
    'reserved2',
    'table_entry79',
]
struct_rss_ind_table_10._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry72', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry73', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry74', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry75', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry76', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry77', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry78', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry79', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 203
class struct_rss_ind_table_11(Structure):
    pass

struct_rss_ind_table_11.__slots__ = [
    'reserved30',
    'table_entry80',
    'reserved26',
    'table_entry81',
    'reserved22',
    'table_entry82',
    'reserved18',
    'table_entry83',
    'reserved14',
    'table_entry84',
    'reserved10',
    'table_entry85',
    'reserved6',
    'table_entry86',
    'reserved2',
    'table_entry87',
]
struct_rss_ind_table_11._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry80', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry81', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry82', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry83', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry84', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry85', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry86', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry87', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 221
class struct_rss_ind_table_12(Structure):
    pass

struct_rss_ind_table_12.__slots__ = [
    'reserved30',
    'table_entry88',
    'reserved26',
    'table_entry89',
    'reserved22',
    'table_entry90',
    'reserved18',
    'table_entry91',
    'reserved14',
    'table_entry92',
    'reserved10',
    'table_entry93',
    'reserved6',
    'table_entry94',
    'reserved2',
    'table_entry95',
]
struct_rss_ind_table_12._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry88', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry89', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry90', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry91', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry92', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry93', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry94', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry95', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 239
class struct_rss_ind_table_13(Structure):
    pass

struct_rss_ind_table_13.__slots__ = [
    'reserved30',
    'table_entry96',
    'reserved26',
    'table_entry97',
    'reserved22',
    'table_entry98',
    'reserved18',
    'table_entry99',
    'reserved14',
    'table_entry100',
    'reserved10',
    'table_entry101',
    'reserved6',
    'table_entry102',
    'reserved2',
    'table_entry103',
]
struct_rss_ind_table_13._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry96', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry97', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry98', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry99', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry100', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry101', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry102', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry103', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 257
class struct_rss_ind_table_14(Structure):
    pass

struct_rss_ind_table_14.__slots__ = [
    'reserved30',
    'table_entry104',
    'reserved26',
    'table_entry105',
    'reserved22',
    'table_entry106',
    'reserved18',
    'table_entry107',
    'reserved14',
    'table_entry108',
    'reserved10',
    'table_entry109',
    'reserved6',
    'table_entry110',
    'reserved2',
    'table_entry111',
]
struct_rss_ind_table_14._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry104', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry105', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry106', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry107', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry108', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry109', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry110', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry111', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 275
class struct_rss_ind_table_15(Structure):
    pass

struct_rss_ind_table_15.__slots__ = [
    'reserved30',
    'table_entry112',
    'reserved26',
    'table_entry113',
    'reserved22',
    'table_entry114',
    'reserved18',
    'table_entry115',
    'reserved14',
    'table_entry116',
    'reserved10',
    'table_entry117',
    'reserved6',
    'table_entry118',
    'reserved2',
    'table_entry119',
]
struct_rss_ind_table_15._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry112', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry113', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry114', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry115', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry116', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry117', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry118', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry119', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 293
class struct_rss_ind_table_16(Structure):
    pass

struct_rss_ind_table_16.__slots__ = [
    'reserved30',
    'table_entry120',
    'reserved26',
    'table_entry121',
    'reserved22',
    'table_entry122',
    'reserved18',
    'table_entry123',
    'reserved14',
    'table_entry124',
    'reserved10',
    'table_entry125',
    'reserved6',
    'table_entry126',
    'reserved2',
    'table_entry127',
]
struct_rss_ind_table_16._fields_ = [
    ('reserved30', u32, 2),
    ('table_entry120', u32, 2),
    ('reserved26', u32, 2),
    ('table_entry121', u32, 2),
    ('reserved22', u32, 2),
    ('table_entry122', u32, 2),
    ('reserved18', u32, 2),
    ('table_entry123', u32, 2),
    ('reserved14', u32, 2),
    ('table_entry124', u32, 2),
    ('reserved10', u32, 2),
    ('table_entry125', u32, 2),
    ('reserved6', u32, 2),
    ('table_entry126', u32, 2),
    ('reserved2', u32, 2),
    ('table_entry127', u32, 2),
]

# /home/saul/thundergate/include/rss.h: 311
class struct_rss_hash_key(Structure):
    pass

struct_rss_hash_key.__slots__ = [
    'byte1',
    'byte2',
    'byte3',
    'byte4',
]
struct_rss_hash_key._fields_ = [
    ('byte1', u32, 8),
    ('byte2', u32, 8),
    ('byte3', u32, 8),
    ('byte4', u32, 8),
]

# /home/saul/thundergate/include/rss.h: 317
class struct_rmac_programmable_ipv6_extension_header(Structure):
    pass

struct_rmac_programmable_ipv6_extension_header.__slots__ = [
    'hdr_type2_en',
    'hdr_type1_en',
    'reserved16',
    'hdr_type2',
    'hdr_type1',
]
struct_rmac_programmable_ipv6_extension_header._fields_ = [
    ('hdr_type2_en', u32, 1),
    ('hdr_type1_en', u32, 1),
    ('reserved16', u32, 14),
    ('hdr_type2', u32, 8),
    ('hdr_type1', u32, 8),
]

# /home/saul/thundergate/include/rss.h: 325
class struct_rss_regs(Structure):
    pass

struct_rss_regs.__slots__ = [
    'ofs_00',
    'ofs_04',
    'ofs_08',
    'ofs_0c',
    'ofs_10',
    'ofs_14',
    'ofs_18',
    'ofs_1c',
    'ofs_20',
    'ofs_24',
    'ofs_28',
    'ofs_2c',
    'ind_table_1',
    'ind_table_2',
    'ind_table_3',
    'ind_table_4',
    'ind_table_5',
    'ind_table_6',
    'ind_table_7',
    'ind_table_8',
    'ind_table_9',
    'ind_table_10',
    'ind_table_11',
    'ind_table_12',
    'ind_table_13',
    'ind_table_14',
    'ind_table_15',
    'ind_table_16',
    'hash_key_0',
    'hash_key_1',
    'hash_key_2',
    'hash_key_3',
    'hash_key_4',
    'hash_key_5',
    'hash_key_6',
    'hash_key_7',
    'hash_key_8',
    'hash_key_9',
    'ofs_98',
    'ofs_9c',
    'rmac_ipv6_ext_hdr',
]
struct_rss_regs._fields_ = [
    ('ofs_00', u32),
    ('ofs_04', u32),
    ('ofs_08', u32),
    ('ofs_0c', u32),
    ('ofs_10', u32),
    ('ofs_14', u32),
    ('ofs_18', u32),
    ('ofs_1c', u32),
    ('ofs_20', u32),
    ('ofs_24', u32),
    ('ofs_28', u32),
    ('ofs_2c', u32),
    ('ind_table_1', struct_rss_ind_table_1),
    ('ind_table_2', struct_rss_ind_table_2),
    ('ind_table_3', struct_rss_ind_table_3),
    ('ind_table_4', struct_rss_ind_table_4),
    ('ind_table_5', struct_rss_ind_table_5),
    ('ind_table_6', struct_rss_ind_table_6),
    ('ind_table_7', struct_rss_ind_table_7),
    ('ind_table_8', struct_rss_ind_table_8),
    ('ind_table_9', struct_rss_ind_table_9),
    ('ind_table_10', struct_rss_ind_table_10),
    ('ind_table_11', struct_rss_ind_table_11),
    ('ind_table_12', struct_rss_ind_table_12),
    ('ind_table_13', struct_rss_ind_table_13),
    ('ind_table_14', struct_rss_ind_table_14),
    ('ind_table_15', struct_rss_ind_table_15),
    ('ind_table_16', struct_rss_ind_table_16),
    ('hash_key_0', struct_rss_hash_key),
    ('hash_key_1', struct_rss_hash_key),
    ('hash_key_2', struct_rss_hash_key),
    ('hash_key_3', struct_rss_hash_key),
    ('hash_key_4', struct_rss_hash_key),
    ('hash_key_5', struct_rss_hash_key),
    ('hash_key_6', struct_rss_hash_key),
    ('hash_key_7', struct_rss_hash_key),
    ('hash_key_8', struct_rss_hash_key),
    ('hash_key_9', struct_rss_hash_key),
    ('ofs_98', u32),
    ('ofs_9c', u32),
    ('rmac_ipv6_ext_hdr', struct_rmac_programmable_ipv6_extension_header),
]

# /home/saul/thundergate/include/rtsdi.h: 24
class struct_rtsdi_mode(Structure):
    pass

struct_rtsdi_mode.__slots__ = [
    'reserved',
    'multiple_segment_enable',
    'pre_dma_debug',
    'hardware_pre_dma_enable',
    'stats_overflow_attention_enable',
    'enable',
    'reset',
]
struct_rtsdi_mode._fields_ = [
    ('reserved', u32, 26),
    ('multiple_segment_enable', u32, 1),
    ('pre_dma_debug', u32, 1),
    ('hardware_pre_dma_enable', u32, 1),
    ('stats_overflow_attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/rtsdi.h: 34
class struct_rtsdi_status(Structure):
    pass

struct_rtsdi_status.__slots__ = [
    'reserved',
    'stats_overflow_attention',
    'reserved2',
]
struct_rtsdi_status._fields_ = [
    ('reserved', u32, 29),
    ('stats_overflow_attention', u32, 1),
    ('reserved2', u32, 2),
]

# /home/saul/thundergate/include/rtsdi.h: 40
class struct_rtsdi_statistics_control(Structure):
    pass

struct_rtsdi_statistics_control.__slots__ = [
    'reserved',
    'zap_statistics',
    'flush_statistics',
    'statistics_clear',
    'faster_update',
    'statistics_enable',
]
struct_rtsdi_statistics_control._fields_ = [
    ('reserved', u32, 27),
    ('zap_statistics', u32, 1),
    ('flush_statistics', u32, 1),
    ('statistics_clear', u32, 1),
    ('faster_update', u32, 1),
    ('statistics_enable', u32, 1),
]

# /home/saul/thundergate/include/rtsdi.h: 49
class struct_rtsdi_statistics_mask(Structure):
    pass

struct_rtsdi_statistics_mask.__slots__ = [
    'reserved',
    'counters_enable_mask',
]
struct_rtsdi_statistics_mask._fields_ = [
    ('reserved', u32, 31),
    ('counters_enable_mask', u32, 1),
]

# /home/saul/thundergate/include/rtsdi.h: 54
class struct_rtsdi_statistics_increment_mask(Structure):
    pass

struct_rtsdi_statistics_increment_mask.__slots__ = [
    'reserved',
    'counters_increment_mask_1',
    'reserved2',
    'counters_increment_mask_2',
]
struct_rtsdi_statistics_increment_mask._fields_ = [
    ('reserved', u32, 8),
    ('counters_increment_mask_1', u32, 5),
    ('reserved2', u32, 3),
    ('counters_increment_mask_2', u32, 16),
]

# /home/saul/thundergate/include/rtsdi.h: 61
class struct_rtsdi_regs(Structure):
    pass

struct_rtsdi_regs.__slots__ = [
    'mode',
    'status',
    'statistics_control',
    'statistics_mask',
    'statistics_increment_mask',
    'ofs_14',
    'ofs_18',
    'ofs_1c',
    'av_fetch_delay',
    'av_fetch_cx_comp',
    'av_fetch_l1_comp',
]
struct_rtsdi_regs._fields_ = [
    ('mode', struct_rtsdi_mode),
    ('status', struct_rtsdi_status),
    ('statistics_control', struct_rtsdi_statistics_control),
    ('statistics_mask', struct_rtsdi_statistics_mask),
    ('statistics_increment_mask', struct_rtsdi_statistics_increment_mask),
    ('ofs_14', u32),
    ('ofs_18', u32),
    ('ofs_1c', u32),
    ('av_fetch_delay', u32),
    ('av_fetch_cx_comp', u32),
    ('av_fetch_l1_comp', u32),
]

# /home/saul/thundergate/include/sbdc.h: 24
class struct_sbdc_mode(Structure):
    pass

struct_sbdc_mode.__slots__ = [
    'reserved',
    'attention_enable',
    'enable',
    'reset',
]
struct_sbdc_mode._fields_ = [
    ('reserved', u32, 29),
    ('attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/sbdc.h: 31
class struct_sbdc_debug(Structure):
    pass

struct_sbdc_debug.__slots__ = [
    'reserved',
    'rstate',
]
struct_sbdc_debug._fields_ = [
    ('reserved', u32, 29),
    ('rstate', u32, 3),
]

# /home/saul/thundergate/include/sbdc.h: 36
class struct_sbdc_regs(Structure):
    pass

struct_sbdc_regs.__slots__ = [
    'mode',
    'debug',
]
struct_sbdc_regs._fields_ = [
    ('mode', struct_sbdc_mode),
    ('debug', struct_sbdc_debug),
]

# /home/saul/thundergate/include/sbdi.h: 24
class struct_sbdi_mode(Structure):
    pass

struct_sbdi_mode.__slots__ = [
    'reserved',
    'multi_txq_en',
    'pass_bit',
    'rupd_enable',
    'attention_enable',
    'enable',
    'reset',
]
struct_sbdi_mode._fields_ = [
    ('reserved', u32, 26),
    ('multi_txq_en', u32, 1),
    ('pass_bit', u32, 1),
    ('rupd_enable', u32, 1),
    ('attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/sbdi.h: 34
class struct_sbdi_status(Structure):
    pass

struct_sbdi_status.__slots__ = [
    'reserved',
    'error',
    'reserved2',
]
struct_sbdi_status._fields_ = [
    ('reserved', u32, 29),
    ('error', u32, 1),
    ('reserved2', u32, 2),
]

# /home/saul/thundergate/include/sbdi.h: 40
class struct_sbdi_regs(Structure):
    pass

struct_sbdi_regs.__slots__ = [
    'mode',
    'status',
    'prod_idx',
]
struct_sbdi_regs._fields_ = [
    ('mode', struct_sbdi_mode),
    ('status', struct_sbdi_status),
    ('prod_idx', u32 * 16),
]

# /home/saul/thundergate/include/sbds.h: 22
class struct_sbds_mode(Structure):
    pass

struct_sbds_mode.__slots__ = [
    'reserved',
    'attention_enable',
    'enable',
    'reset',
]
struct_sbds_mode._fields_ = [
    ('reserved', u32, 29),
    ('attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/sbds.h: 29
class struct_sbds_status(Structure):
    pass

struct_sbds_status.__slots__ = [
    'reserved',
    'error',
    'reserved2',
]
struct_sbds_status._fields_ = [
    ('reserved', u32, 29),
    ('error', u32, 1),
    ('reserved2', u32, 2),
]

# /home/saul/thundergate/include/sbds.h: 35
class struct_sbds_local_nic_send_bd_consumer_idx(Structure):
    pass

struct_sbds_local_nic_send_bd_consumer_idx.__slots__ = [
    'reserved',
    'index',
]
struct_sbds_local_nic_send_bd_consumer_idx._fields_ = [
    ('reserved', u32, 23),
    ('index', u32, 9),
]

# /home/saul/thundergate/include/sbds.h: 40
class struct_sbds_regs(Structure):
    pass

struct_sbds_regs.__slots__ = [
    'mode',
    'status',
    'hardware_diagnostics',
    'local_nic_send_bd_consumer_idx',
    'unknown',
    'con_idx',
]
struct_sbds_regs._fields_ = [
    ('mode', struct_sbds_mode),
    ('status', struct_sbds_status),
    ('hardware_diagnostics', u32),
    ('local_nic_send_bd_consumer_idx', struct_sbds_local_nic_send_bd_consumer_idx),
    ('unknown', u32 * 12),
    ('con_idx', u32 * 16),
]

# /home/saul/thundergate/include/sdc.h: 24
class struct_sdc_mode(Structure):
    pass

struct_sdc_mode.__slots__ = [
    'reserved',
    'cdelay',
    'reserved2',
    'enable',
    'reset',
]
struct_sdc_mode._fields_ = [
    ('reserved', u32, 27),
    ('cdelay', u32, 1),
    ('reserved2', u32, 2),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/sdc.h: 32
class struct_sdc_pre_dma_command_exchange(Structure):
    pass

struct_sdc_pre_dma_command_exchange.__slots__ = [
    'pass_flag',
    'skip_flag',
    'end_of_frag',
    'reserved',
    'head_txmbuf_ptr',
    'tail_txmbuf_ptr',
]
struct_sdc_pre_dma_command_exchange._fields_ = [
    ('pass_flag', u32, 1),
    ('skip_flag', u32, 1),
    ('end_of_frag', u32, 1),
    ('reserved', u32, 13),
    ('head_txmbuf_ptr', u32, 8),
    ('tail_txmbuf_ptr', u32, 8),
]

# /home/saul/thundergate/include/sdc.h: 41
class struct_sdc_regs(Structure):
    pass

struct_sdc_regs.__slots__ = [
    'mode',
    'unknown',
    'pre_dma_command_exchange',
]
struct_sdc_regs._fields_ = [
    ('mode', struct_sdc_mode),
    ('unknown', u32),
    ('pre_dma_command_exchange', struct_sdc_pre_dma_command_exchange),
]

# /home/saul/thundergate/include/sdi.h: 24
class struct_sdi_mode(Structure):
    pass

struct_sdi_mode.__slots__ = [
    'reserved',
    'multiple_segment_enable',
    'pre_dma_debug',
    'hardware_pre_dma_enable',
    'stats_overflow_attention_enable',
    'enable',
    'reset',
]
struct_sdi_mode._fields_ = [
    ('reserved', u32, 26),
    ('multiple_segment_enable', u32, 1),
    ('pre_dma_debug', u32, 1),
    ('hardware_pre_dma_enable', u32, 1),
    ('stats_overflow_attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/sdi.h: 34
class struct_sdi_status(Structure):
    pass

struct_sdi_status.__slots__ = [
    'reserved',
    'stats_overflow_attention',
    'reserved2',
]
struct_sdi_status._fields_ = [
    ('reserved', u32, 29),
    ('stats_overflow_attention', u32, 1),
    ('reserved2', u32, 2),
]

# /home/saul/thundergate/include/sdi.h: 40
class struct_sdi_statistics_control(Structure):
    pass

struct_sdi_statistics_control.__slots__ = [
    'reserved',
    'zap_statistics',
    'flush_statistics',
    'statistics_clear',
    'faster_update',
    'statistics_enable',
]
struct_sdi_statistics_control._fields_ = [
    ('reserved', u32, 27),
    ('zap_statistics', u32, 1),
    ('flush_statistics', u32, 1),
    ('statistics_clear', u32, 1),
    ('faster_update', u32, 1),
    ('statistics_enable', u32, 1),
]

# /home/saul/thundergate/include/sdi.h: 49
class struct_sdi_statistics_mask(Structure):
    pass

struct_sdi_statistics_mask.__slots__ = [
    'reserved',
    'counters_enable_mask',
]
struct_sdi_statistics_mask._fields_ = [
    ('reserved', u32, 31),
    ('counters_enable_mask', u32, 1),
]

# /home/saul/thundergate/include/sdi.h: 54
class struct_sdi_statistics_increment_mask(Structure):
    pass

struct_sdi_statistics_increment_mask.__slots__ = [
    'reserved',
    'counters_increment_mask_1',
    'reserved2',
    'counters_increment_mask_2',
]
struct_sdi_statistics_increment_mask._fields_ = [
    ('reserved', u32, 8),
    ('counters_increment_mask_1', u32, 5),
    ('reserved2', u32, 3),
    ('counters_increment_mask_2', u32, 16),
]

# /home/saul/thundergate/include/sdi.h: 61
class struct_sdi_regs(Structure):
    pass

struct_sdi_regs.__slots__ = [
    'mode',
    'status',
    'statistics_control',
    'statistics_mask',
    'statistics_increment_mask',
    'unknown',
    'local_statistics',
]
struct_sdi_regs._fields_ = [
    ('mode', struct_sdi_mode),
    ('status', struct_sdi_status),
    ('statistics_control', struct_sdi_statistics_control),
    ('statistics_mask', struct_sdi_statistics_mask),
    ('statistics_increment_mask', struct_sdi_statistics_increment_mask),
    ('unknown', u32 * 27),
    ('local_statistics', u32 * 18),
]

# /home/saul/thundergate/include/stats.h: 22
class struct_mac_stats_regs(Structure):
    pass

struct_mac_stats_regs.__slots__ = [
    'ifHCOutOctets',
    'ofs_04',
    'etherStatsCollisions',
    'outXonSent',
    'outXoffSent',
    'ofs_14',
    'dot3StatsInternalMacTransmitErrors',
    'dot3StatsSingleCollisionFrames',
    'dot3StatsMultipleCollisionFrames',
    'dot3StatsDeferredTransmissions',
    'ofs_28',
    'dot3StatsExcessiveTransmissions',
    'dot3StatsLateCollisions',
    'ofs_34',
    'ofs_38',
    'ofs_3c',
    'ofs_40',
    'ofs_44',
    'ofs_48',
    'ofs_4c',
    'ofs_50',
    'ofs_54',
    'ofs_58',
    'ofs_5c',
    'ofs_60',
    'ofs_64',
    'ofs_68',
    'iHCOutUcastPkts',
    'iHCOutMulticastPkts',
    'iHCOutBroadcastPkts',
    'ofs_78',
    'ofs_7c',
    'iHCOOutOctets',
    'ofs_84',
    'etherStatsFragments',
    'ifHCInUcastPkts',
    'ifHCInMulticastPkts',
    'ifHCInBroadcastPkts',
    'dot3StatsFCSErrors',
    'dot3StatsAlignmentErrors',
    'xonPauseFrameReceived',
    'xoffPauseFrameReceived',
    'macControlFramesReceived',
    'xoffStateEntered',
    'dot3StatsFramesTooLongs',
    'etherStatsJabbers',
    'etherStatsUndersizePkts',
    'ofs_bc',
]
struct_mac_stats_regs._fields_ = [
    ('ifHCOutOctets', u32),
    ('ofs_04', u32),
    ('etherStatsCollisions', u32),
    ('outXonSent', u32),
    ('outXoffSent', u32),
    ('ofs_14', u32),
    ('dot3StatsInternalMacTransmitErrors', u32),
    ('dot3StatsSingleCollisionFrames', u32),
    ('dot3StatsMultipleCollisionFrames', u32),
    ('dot3StatsDeferredTransmissions', u32),
    ('ofs_28', u32),
    ('dot3StatsExcessiveTransmissions', u32),
    ('dot3StatsLateCollisions', u32),
    ('ofs_34', u32),
    ('ofs_38', u32),
    ('ofs_3c', u32),
    ('ofs_40', u32),
    ('ofs_44', u32),
    ('ofs_48', u32),
    ('ofs_4c', u32),
    ('ofs_50', u32),
    ('ofs_54', u32),
    ('ofs_58', u32),
    ('ofs_5c', u32),
    ('ofs_60', u32),
    ('ofs_64', u32),
    ('ofs_68', u32),
    ('iHCOutUcastPkts', u32),
    ('iHCOutMulticastPkts', u32),
    ('iHCOutBroadcastPkts', u32),
    ('ofs_78', u32),
    ('ofs_7c', u32),
    ('iHCOOutOctets', u32),
    ('ofs_84', u32),
    ('etherStatsFragments', u32),
    ('ifHCInUcastPkts', u32),
    ('ifHCInMulticastPkts', u32),
    ('ifHCInBroadcastPkts', u32),
    ('dot3StatsFCSErrors', u32),
    ('dot3StatsAlignmentErrors', u32),
    ('xonPauseFrameReceived', u32),
    ('xoffPauseFrameReceived', u32),
    ('macControlFramesReceived', u32),
    ('xoffStateEntered', u32),
    ('dot3StatsFramesTooLongs', u32),
    ('etherStatsJabbers', u32),
    ('etherStatsUndersizePkts', u32),
    ('ofs_bc', u32),
]

# /home/saul/thundergate/include/status_block.h: 24
class struct_status_block(Structure):
    pass

# /home/saul/thundergate/include/tcp_seg_ctrl.h: 22
class struct_tsc_length_offset(Structure):
    pass

struct_tsc_length_offset.__slots__ = [
    'reserved23',
    'mbuf_offset',
    'length',
]
struct_tsc_length_offset._fields_ = [
    ('reserved23', u32, 9),
    ('mbuf_offset', u32, 7),
    ('length', u32, 16),
]

# /home/saul/thundergate/include/tcp_seg_ctrl.h: 28
class struct_tsc_dma_flags(Structure):
    pass

struct_tsc_dma_flags.__slots__ = [
    'reserved20',
    'mbuf_offset_valid',
    'last_fragment',
    'no_word_swap',
    'status_dma',
    'mac_source_addr_sel',
    'mac_source_addr_ins',
    'tcp_udp_cksum_en',
    'ip_cksum_en',
    'force_raw_cksum_en',
    'data_only',
    'header',
    'vlan_tag_present',
    'force_interrupt',
    'last_bd_in_frame',
    'coalesce_now',
    'mbuf',
    'invoke_processor',
    'dont_generate_crc',
    'no_byte_swap',
]
struct_tsc_dma_flags._fields_ = [
    ('reserved20', u32, 12),
    ('mbuf_offset_valid', u32, 1),
    ('last_fragment', u32, 1),
    ('no_word_swap', u32, 1),
    ('status_dma', u32, 1),
    ('mac_source_addr_sel', u32, 2),
    ('mac_source_addr_ins', u32, 1),
    ('tcp_udp_cksum_en', u32, 1),
    ('ip_cksum_en', u32, 1),
    ('force_raw_cksum_en', u32, 1),
    ('data_only', u32, 1),
    ('header', u32, 1),
    ('vlan_tag_present', u32, 1),
    ('force_interrupt', u32, 1),
    ('last_bd_in_frame', u32, 1),
    ('coalesce_now', u32, 1),
    ('mbuf', u32, 1),
    ('invoke_processor', u32, 1),
    ('dont_generate_crc', u32, 1),
    ('no_byte_swap', u32, 1),
]

# /home/saul/thundergate/include/tcp_seg_ctrl.h: 51
class struct_tsc_vlan_tag(Structure):
    pass

struct_tsc_vlan_tag.__slots__ = [
    'reserved16',
    'vlan_tag',
]
struct_tsc_vlan_tag._fields_ = [
    ('reserved16', u32, 16),
    ('vlan_tag', u32, 16),
]

# /home/saul/thundergate/include/tcp_seg_ctrl.h: 56
class struct_tsc_pre_dma_cmd_xchng(Structure):
    pass

struct_tsc_pre_dma_cmd_xchng.__slots__ = [
    'ready',
    'pass_bit',
    'skip',
    'unsupported_mss',
    'reserved7',
    'bd_index',
]
struct_tsc_pre_dma_cmd_xchng._fields_ = [
    ('ready', u32, 1),
    ('pass_bit', u32, 1),
    ('skip', u32, 1),
    ('unsupported_mss', u32, 1),
    ('reserved7', u32, 21),
    ('bd_index', u32, 7),
]

# /home/saul/thundergate/include/tcp_seg_ctrl.h: 65
class struct_tcp_seg_ctrl_regs(Structure):
    pass

struct_tcp_seg_ctrl_regs.__slots__ = [
    'lower_host_addr',
    'upper_host_addr',
    'length_offset',
    'dma_flags',
    'vlan_tag',
    'pre_dma_cmd_xchng',
]
struct_tcp_seg_ctrl_regs._fields_ = [
    ('lower_host_addr', u32),
    ('upper_host_addr', u32),
    ('length_offset', struct_tsc_length_offset),
    ('dma_flags', struct_tsc_dma_flags),
    ('vlan_tag', struct_tsc_vlan_tag),
    ('pre_dma_cmd_xchng', struct_tsc_pre_dma_cmd_xchng),
]

# /home/saul/thundergate/include/wdma.h: 24
class struct_wdma_mode(Structure):
    pass

struct_wdma_mode.__slots__ = [
    'reserved',
    'status_tag_fix_enable',
    'reserved2',
    'swap_test_en',
    'hc_byte_swap',
    'hc_word_swap',
    'bd_byte_swap',
    'bd_word_swap',
    'data_byte_swap',
    'data_word_swap',
    'software_byte_swap_control',
    'receive_accelerate_mode',
    'write_dma_local_memory',
    'write_dma_pci_fifo_overwrite_attention_enable',
    'write_dma_pci_fifo_underrun_attention_enable',
    'write_dma_pci_fifo_overrun_attention_enable',
    'write_dma_pci_host_address_overflow_error_attention_enable',
    'write_dma_pci_parity_error_attention_enable',
    'write_dma_pci_master_abort_attention_enable',
    'write_dma_pci_target_abort_attention_enable',
    'enable',
    'reset',
]
struct_wdma_mode._fields_ = [
    ('reserved', u32, 2),
    ('status_tag_fix_enable', u32, 1),
    ('reserved2', u32, 10),
    ('swap_test_en', u32, 1),
    ('hc_byte_swap', u32, 1),
    ('hc_word_swap', u32, 1),
    ('bd_byte_swap', u32, 1),
    ('bd_word_swap', u32, 1),
    ('data_byte_swap', u32, 1),
    ('data_word_swap', u32, 1),
    ('software_byte_swap_control', u32, 1),
    ('receive_accelerate_mode', u32, 1),
    ('write_dma_local_memory', u32, 1),
    ('write_dma_pci_fifo_overwrite_attention_enable', u32, 1),
    ('write_dma_pci_fifo_underrun_attention_enable', u32, 1),
    ('write_dma_pci_fifo_overrun_attention_enable', u32, 1),
    ('write_dma_pci_host_address_overflow_error_attention_enable', u32, 1),
    ('write_dma_pci_parity_error_attention_enable', u32, 1),
    ('write_dma_pci_master_abort_attention_enable', u32, 1),
    ('write_dma_pci_target_abort_attention_enable', u32, 1),
    ('enable', u32, 1),
    ('reset', u32, 1),
]

# /home/saul/thundergate/include/wdma.h: 49
class struct_wdma_status(Structure):
    pass

struct_wdma_status.__slots__ = [
    'reserved',
    'write_dma_local_memory_read_longer_than_dma_length_error',
    'write_dma_pci_fifo_overwrite_error',
    'write_dma_pci_fifo_underrun_error',
    'write_dma_pci_fifo_overrun_error',
    'write_dma_pci_host_address_overflow_error',
    'reserved1',
]
struct_wdma_status._fields_ = [
    ('reserved', u32, 22),
    ('write_dma_local_memory_read_longer_than_dma_length_error', u32, 1),
    ('write_dma_pci_fifo_overwrite_error', u32, 1),
    ('write_dma_pci_fifo_underrun_error', u32, 1),
    ('write_dma_pci_fifo_overrun_error', u32, 1),
    ('write_dma_pci_host_address_overflow_error', u32, 1),
    ('reserved1', u32, 5),
]

# /home/saul/thundergate/include/wdma.h: 59
class struct_wdma_regs(Structure):
    pass

struct_wdma_regs.__slots__ = [
    'mode',
    'status',
]
struct_wdma_regs._fields_ = [
    ('mode', struct_wdma_mode),
    ('status', struct_wdma_status),
]

dmar_tbl_hdr = struct_dmar_tbl_hdr # /home/saul/thundergate/include/acpi.h: 32

dmar_dev_scope = struct_dmar_dev_scope # /home/saul/thundergate/include/acpi.h: 47

dmar_drhd = struct_dmar_drhd # /home/saul/thundergate/include/acpi.h: 59

dmar_rmrr = struct_dmar_rmrr # /home/saul/thundergate/include/acpi.h: 68

dmar_atsr = struct_dmar_atsr # /home/saul/thundergate/include/acpi.h: 78

dmar_rhsa = struct_dmar_rhsa # /home/saul/thundergate/include/acpi.h: 87

dmar_andd = struct_dmar_andd # /home/saul/thundergate/include/acpi.h: 95

acpi_sdt_hdr = struct_acpi_sdt_hdr # /home/saul/thundergate/include/acpi.h: 103

xsdt = struct_xsdt # /home/saul/thundergate/include/acpi.h: 115

rsdp_t = struct_rsdp_t # /home/saul/thundergate/include/acpi.h: 120

rsdp2_t = struct_rsdp2_t # /home/saul/thundergate/include/acpi.h: 128

asf_control = struct_asf_control # /home/saul/thundergate/include/asf.h: 24

asf_smbus_input = struct_asf_smbus_input # /home/saul/thundergate/include/asf.h: 44

asf_smbus_output = struct_asf_smbus_output # /home/saul/thundergate/include/asf.h: 53

asf_watchdog_timer = struct_asf_watchdog_timer # /home/saul/thundergate/include/asf.h: 71

asf_heartbeat_timer = struct_asf_heartbeat_timer # /home/saul/thundergate/include/asf.h: 76

asf_poll_timer = struct_asf_poll_timer # /home/saul/thundergate/include/asf.h: 81

asf_poll_legacy_timer = struct_asf_poll_legacy_timer # /home/saul/thundergate/include/asf.h: 86

asf_retransmission_timer = struct_asf_retransmission_timer # /home/saul/thundergate/include/asf.h: 91

asf_time_stamp_counter = struct_asf_time_stamp_counter # /home/saul/thundergate/include/asf.h: 96

asf_smbus_driver_select = struct_asf_smbus_driver_select # /home/saul/thundergate/include/asf.h: 100

asf_regs = struct_asf_regs # /home/saul/thundergate/include/asf.h: 111

sbd_flags = struct_sbd_flags # /home/saul/thundergate/include/bd.h: 24

sbd = struct_sbd # /home/saul/thundergate/include/bd.h: 69

rbd_flags = struct_rbd_flags # /home/saul/thundergate/include/bd.h: 91

rbd_error_flags = struct_rbd_error_flags # /home/saul/thundergate/include/bd.h: 113

rbd = struct_rbd # /home/saul/thundergate/include/bd.h: 137

rbd_ex = struct_rbd_ex # /home/saul/thundergate/include/bd.h: 152

bdrdma_mode = struct_bdrdma_mode # /home/saul/thundergate/include/bdrdma.h: 24

bdrdma_status = struct_bdrdma_status # /home/saul/thundergate/include/bdrdma.h: 36

bdrdma_len_dbg = struct_bdrdma_len_dbg # /home/saul/thundergate/include/bdrdma.h: 50

bdrdma_rstates_dbg = struct_bdrdma_rstates_dbg # /home/saul/thundergate/include/bdrdma.h: 55

bdrdma_rstate2_dbg = struct_bdrdma_rstate2_dbg # /home/saul/thundergate/include/bdrdma.h: 61

bdrdma_bd_status_dbg = struct_bdrdma_bd_status_dbg # /home/saul/thundergate/include/bdrdma.h: 66

bdrdma_req_ptr_dbg = struct_bdrdma_req_ptr_dbg # /home/saul/thundergate/include/bdrdma.h: 88

bdrdma_hold_d_dmad_dbg = struct_bdrdma_hold_d_dmad_dbg # /home/saul/thundergate/include/bdrdma.h: 97

bdrdma_len_and_addr_idx_dbg = struct_bdrdma_len_and_addr_idx_dbg # /home/saul/thundergate/include/bdrdma.h: 103

bdrdma_addr_idx_dbg = struct_bdrdma_addr_idx_dbg # /home/saul/thundergate/include/bdrdma.h: 108

bdrdma_pcie_dbg_status = struct_bdrdma_pcie_dbg_status # /home/saul/thundergate/include/bdrdma.h: 113

bdrdma_pcie_dma_rd_req_addr_dbg = struct_bdrdma_pcie_dma_rd_req_addr_dbg # /home/saul/thundergate/include/bdrdma.h: 130

bdrdma_pcie_dma_req_len_dbg = struct_bdrdma_pcie_dma_req_len_dbg # /home/saul/thundergate/include/bdrdma.h: 135

bdrdma_fifo1_dbg = struct_bdrdma_fifo1_dbg # /home/saul/thundergate/include/bdrdma.h: 140

bdrdma_fifo2_dbg = struct_bdrdma_fifo2_dbg # /home/saul/thundergate/include/bdrdma.h: 145

bdrdma_rsvrd_ctrl = struct_bdrdma_rsvrd_ctrl # /home/saul/thundergate/include/bdrdma.h: 151

bdrdma_regs = struct_bdrdma_regs # /home/saul/thundergate/include/bdrdma.h: 161

bufman_mode = struct_bufman_mode # /home/saul/thundergate/include/bufman.h: 22

bufman_status = struct_bufman_status # /home/saul/thundergate/include/bufman.h: 38

bufman_mbuf_pool_bar = struct_bufman_mbuf_pool_bar # /home/saul/thundergate/include/bufman.h: 46

bufman_mbuf_pool_length = struct_bufman_mbuf_pool_length # /home/saul/thundergate/include/bufman.h: 51

bufman_rdma_mbuf_low_watermark = struct_bufman_rdma_mbuf_low_watermark # /home/saul/thundergate/include/bufman.h: 56

bufman_dma_mbuf_low_watermark = struct_bufman_dma_mbuf_low_watermark # /home/saul/thundergate/include/bufman.h: 61

bufman_mbuf_high_watermark = struct_bufman_mbuf_high_watermark # /home/saul/thundergate/include/bufman.h: 66

bufman_risc_mbuf_cluster_allocation_request = struct_bufman_risc_mbuf_cluster_allocation_request # /home/saul/thundergate/include/bufman.h: 71

bufman_risc_mbuf_cluster_allocation_response = struct_bufman_risc_mbuf_cluster_allocation_response # /home/saul/thundergate/include/bufman.h: 76

bufman_hardware_diagnostic_1 = struct_bufman_hardware_diagnostic_1 # /home/saul/thundergate/include/bufman.h: 80

bufman_hardware_diagnostic_2 = struct_bufman_hardware_diagnostic_2 # /home/saul/thundergate/include/bufman.h: 89

bufman_hardware_diagnostic_3 = struct_bufman_hardware_diagnostic_3 # /home/saul/thundergate/include/bufman.h: 97

bufman_receive_flow_threshold = struct_bufman_receive_flow_threshold # /home/saul/thundergate/include/bufman.h: 104

bufman_regs = struct_bufman_regs # /home/saul/thundergate/include/bufman.h: 109

cfg_port_cap_ctrl = struct_cfg_port_cap_ctrl # /home/saul/thundergate/include/cfg_port.h: 22

cfg_port_bar_ctrl = struct_cfg_port_bar_ctrl # /home/saul/thundergate/include/cfg_port.h: 30

cfg_port_pci_id = struct_cfg_port_pci_id # /home/saul/thundergate/include/cfg_port.h: 38

cfg_port_pci_sid = struct_cfg_port_pci_sid # /home/saul/thundergate/include/cfg_port.h: 48

cfg_port_pci_class = struct_cfg_port_pci_class # /home/saul/thundergate/include/cfg_port.h: 58

cfg_port_regs = struct_cfg_port_regs # /home/saul/thundergate/include/cfg_port.h: 70

cpmu_control = struct_cpmu_control # /home/saul/thundergate/include/cpmu.h: 22

cpmu_clock = struct_cpmu_clock # /home/saul/thundergate/include/cpmu.h: 55

cpmu_override = struct_cpmu_override # /home/saul/thundergate/include/cpmu.h: 63

cpmu_status = struct_cpmu_status # /home/saul/thundergate/include/cpmu.h: 69

cpmu_clock_status = struct_cpmu_clock_status # /home/saul/thundergate/include/cpmu.h: 85

cpmu_pcie_status = struct_cpmu_pcie_status # /home/saul/thundergate/include/cpmu.h: 100

cpmu_gphy_control_status = struct_cpmu_gphy_control_status # /home/saul/thundergate/include/cpmu.h: 109

cpmu_ram_control = struct_cpmu_ram_control # /home/saul/thundergate/include/cpmu.h: 127

cpmu_cr_idle_det_debounce_ctrl = struct_cpmu_cr_idle_det_debounce_ctrl # /home/saul/thundergate/include/cpmu.h: 153

cpmu_core_idle_det_debounce_ctrl = struct_cpmu_core_idle_det_debounce_ctrl # /home/saul/thundergate/include/cpmu.h: 158

cpmu_pcie_idle_det_debounce_ctrl = struct_cpmu_pcie_idle_det_debounce_ctrl # /home/saul/thundergate/include/cpmu.h: 163

cpmu_energy_det_debounce_ctrl = struct_cpmu_energy_det_debounce_ctrl # /home/saul/thundergate/include/cpmu.h: 168

cpmu_dll_lock_timer = struct_cpmu_dll_lock_timer # /home/saul/thundergate/include/cpmu.h: 180

cpmu_chip_id = struct_cpmu_chip_id # /home/saul/thundergate/include/cpmu.h: 186

cpmu_mutex = struct_cpmu_mutex # /home/saul/thundergate/include/cpmu.h: 193

cpmu_padring_control = struct_cpmu_padring_control # /home/saul/thundergate/include/cpmu.h: 205

cpmu_regs = struct_cpmu_regs # /home/saul/thundergate/include/cpmu.h: 237

cpu_mode = struct_cpu_mode # /home/saul/thundergate/include/cpu.h: 22

cpu_status = struct_cpu_status # /home/saul/thundergate/include/cpu.h: 44

cpu_event_mask = struct_cpu_event_mask # /home/saul/thundergate/include/cpu.h: 74

cpu_breakpoint = struct_cpu_breakpoint # /home/saul/thundergate/include/cpu.h: 92

cpu_last_branch_address = struct_cpu_last_branch_address # /home/saul/thundergate/include/cpu.h: 103

cpu_regs = struct_cpu_regs # /home/saul/thundergate/include/cpu.h: 114

cr_port_regs = struct_cr_port_regs # /home/saul/thundergate/include/cr_port.h: 22

dmac_mode = struct_dmac_mode # /home/saul/thundergate/include/dmac.h: 22

dmac_regs = struct_dmac_regs # /home/saul/thundergate/include/dmac.h: 33

dma_desc = struct_dma_desc # /home/saul/thundergate/include/dma.h: 22

emac_mode = struct_emac_mode # /home/saul/thundergate/include/emac.h: 24

emac_status = struct_emac_status # /home/saul/thundergate/include/emac.h: 57

emac_event_enable = struct_emac_event_enable # /home/saul/thundergate/include/emac.h: 71

emac_led_control = struct_emac_led_control # /home/saul/thundergate/include/emac.h: 86

transmit_mac_mode = struct_transmit_mac_mode # /home/saul/thundergate/include/emac.h: 112

transmit_mac_status = struct_transmit_mac_status # /home/saul/thundergate/include/emac.h: 135

transmit_mac_lengths = struct_transmit_mac_lengths # /home/saul/thundergate/include/emac.h: 150

receive_mac_mode = struct_receive_mac_mode # /home/saul/thundergate/include/emac.h: 157

receive_mac_status = struct_receive_mac_status # /home/saul/thundergate/include/emac.h: 189

emac_mac_addr = struct_emac_mac_addr # /home/saul/thundergate/include/emac.h: 205

emac_rx_rule_control = struct_emac_rx_rule_control # /home/saul/thundergate/include/emac.h: 225

receive_mac_rules_configuration = struct_receive_mac_rules_configuration # /home/saul/thundergate/include/emac.h: 246

emac_low_watermark_max_receive_frame = struct_emac_low_watermark_max_receive_frame # /home/saul/thundergate/include/emac.h: 252

emac_mii_status = struct_emac_mii_status # /home/saul/thundergate/include/emac.h: 258

emac_mii_mode = struct_emac_mii_mode # /home/saul/thundergate/include/emac.h: 265

emac_autopolling_status = struct_emac_autopolling_status # /home/saul/thundergate/include/emac.h: 279

emac_mii_communication = struct_emac_mii_communication # /home/saul/thundergate/include/emac.h: 284

emac_regulator_voltage_control = struct_emac_regulator_voltage_control # /home/saul/thundergate/include/emac.h: 295

emac_regs = struct_emac_regs # /home/saul/thundergate/include/emac.h: 320

frame = struct_frame # /home/saul/thundergate/include/frame.h: 24

vlan_frame = struct_vlan_frame # /home/saul/thundergate/include/frame.h: 31

ftq_reset = struct_ftq_reset # /home/saul/thundergate/include/ftq.h: 22

ftq_enqueue_dequeue = struct_ftq_enqueue_dequeue # /home/saul/thundergate/include/ftq.h: 48

ftq_write_peek = struct_ftq_write_peek # /home/saul/thundergate/include/ftq.h: 60

ftq_queue_regs = struct_ftq_queue_regs # /home/saul/thundergate/include/ftq.h: 74

ftq_regs = struct_ftq_regs # /home/saul/thundergate/include/ftq.h: 81

gencomm = struct_gencomm # /home/saul/thundergate/include/gencomm.h: 24

grc_mode = struct_grc_mode # /home/saul/thundergate/include/grc.h: 22

grc_misc_config = struct_grc_misc_config # /home/saul/thundergate/include/grc.h: 56

grc_misc_local_control = struct_grc_misc_local_control # /home/saul/thundergate/include/grc.h: 80

grc_cpu_event = struct_grc_cpu_event # /home/saul/thundergate/include/grc.h: 111

grc_cpu_semaphore = struct_grc_cpu_semaphore # /home/saul/thundergate/include/grc.h: 151

grc_pcie_misc_status = struct_grc_pcie_misc_status # /home/saul/thundergate/include/grc.h: 156

grc_cpu_event_enable = struct_grc_cpu_event_enable # /home/saul/thundergate/include/grc.h: 175

grc_secfg_1 = struct_grc_secfg_1 # /home/saul/thundergate/include/grc.h: 215

grc_secfg_2 = struct_grc_secfg_2 # /home/saul/thundergate/include/grc.h: 235

grc_bond_id = struct_grc_bond_id # /home/saul/thundergate/include/grc.h: 243

grc_clock_ctrl = struct_grc_clock_ctrl # /home/saul/thundergate/include/grc.h: 260

grc_misc_control = struct_grc_misc_control # /home/saul/thundergate/include/grc.h: 288

grc_fastboot_program_counter = struct_grc_fastboot_program_counter # /home/saul/thundergate/include/grc.h: 305

grc_power_management_debug = struct_grc_power_management_debug # /home/saul/thundergate/include/grc.h: 315

grc_seeprom_addr = struct_grc_seeprom_addr # /home/saul/thundergate/include/grc.h: 337

grc_seeprom_ctrl = struct_grc_seeprom_ctrl # /home/saul/thundergate/include/grc.h: 348

grc_mdi_ctrl = struct_grc_mdi_ctrl # /home/saul/thundergate/include/grc.h: 358

grc_exp_rom_addr = struct_grc_exp_rom_addr # /home/saul/thundergate/include/grc.h: 366

grc_regs = struct_grc_regs # /home/saul/thundergate/include/grc.h: 371

hc_mode = struct_hc_mode # /home/saul/thundergate/include/hc.h: 24

hc_status = struct_hc_status # /home/saul/thundergate/include/hc.h: 43

hc_flow_attention = struct_hc_flow_attention # /home/saul/thundergate/include/hc.h: 49

hc_regs = struct_hc_regs # /home/saul/thundergate/include/hc.h: 71

ma_mode = struct_ma_mode # /home/saul/thundergate/include/ma.h: 22

ma_status = struct_ma_status # /home/saul/thundergate/include/ma.h: 64

ma_regs = struct_ma_regs # /home/saul/thundergate/include/ma.h: 85

mailbox = struct_mailbox # /home/saul/thundergate/include/mbox.h: 33

hpmb_regs = struct_hpmb_regs # /home/saul/thundergate/include/mbox.h: 38

lpmb_regs = struct_lpmb_regs # /home/saul/thundergate/include/mbox.h: 42

mbuf_hdr = struct_mbuf_hdr # /home/saul/thundergate/include/mbuf.h: 24

mbuf_frame_desc = struct_mbuf_frame_desc # /home/saul/thundergate/include/mbuf.h: 42

mbuf = struct_mbuf # /home/saul/thundergate/include/mbuf.h: 99

msi_mode = struct_msi_mode # /home/saul/thundergate/include/msi.h: 22

msi_status = struct_msi_status # /home/saul/thundergate/include/msi.h: 37

msi_regs = struct_msi_regs # /home/saul/thundergate/include/msi.h: 46

nrdma_mode = struct_nrdma_mode # /home/saul/thundergate/include/nrdma.h: 24

nrdma_status = struct_nrdma_status # /home/saul/thundergate/include/nrdma.h: 35

nrdma_programmable_ipv6_extension_header = struct_nrdma_programmable_ipv6_extension_header # /home/saul/thundergate/include/nrdma.h: 49

nrdma_rstates_debug = struct_nrdma_rstates_debug # /home/saul/thundergate/include/nrdma.h: 57

nrdma_rstate2_debug = struct_nrdma_rstate2_debug # /home/saul/thundergate/include/nrdma.h: 69

nrdma_bd_status_debug = struct_nrdma_bd_status_debug # /home/saul/thundergate/include/nrdma.h: 74

nrdma_req_ptr_debug = struct_nrdma_req_ptr_debug # /home/saul/thundergate/include/nrdma.h: 81

nrdma_hold_d_dmad_debug = struct_nrdma_hold_d_dmad_debug # /home/saul/thundergate/include/nrdma.h: 90

nrdma_length_and_address_debug = struct_nrdma_length_and_address_debug # /home/saul/thundergate/include/nrdma.h: 95

nrdma_mbuf_byte_count_debug = struct_nrdma_mbuf_byte_count_debug # /home/saul/thundergate/include/nrdma.h: 101

nrdma_pcie_debug_status = struct_nrdma_pcie_debug_status # /home/saul/thundergate/include/nrdma.h: 106

nrdma_pcie_dma_read_req_debug = struct_nrdma_pcie_dma_read_req_debug # /home/saul/thundergate/include/nrdma.h: 123

nrdma_pcie_dma_req_length_debug = struct_nrdma_pcie_dma_req_length_debug # /home/saul/thundergate/include/nrdma.h: 128

nrdma_fifo1_debug = struct_nrdma_fifo1_debug # /home/saul/thundergate/include/nrdma.h: 133

nrdma_fifo2_debug = struct_nrdma_fifo2_debug # /home/saul/thundergate/include/nrdma.h: 138

nrdma_post_proc_pkt_req_cnt = struct_nrdma_post_proc_pkt_req_cnt # /home/saul/thundergate/include/nrdma.h: 144

nrdma_mbuf_addr_debug = struct_nrdma_mbuf_addr_debug # /home/saul/thundergate/include/nrdma.h: 149

nrdma_tce_debug1 = struct_nrdma_tce_debug1 # /home/saul/thundergate/include/nrdma.h: 157

nrdma_tce_debug2 = struct_nrdma_tce_debug2 # /home/saul/thundergate/include/nrdma.h: 164

nrdma_tce_debug3 = struct_nrdma_tce_debug3 # /home/saul/thundergate/include/nrdma.h: 169

nrdma_reserved_control = struct_nrdma_reserved_control # /home/saul/thundergate/include/nrdma.h: 178

nrdma_flow_reserved_control = struct_nrdma_flow_reserved_control # /home/saul/thundergate/include/nrdma.h: 189

nrdma_corruption_enable_control = struct_nrdma_corruption_enable_control # /home/saul/thundergate/include/nrdma.h: 200

nrdma_regs = struct_nrdma_regs # /home/saul/thundergate/include/nrdma.h: 218

nvram_dir_item = struct_nvram_dir_item # /home/saul/thundergate/include/nvram.h: 35

nvram_header = struct_nvram_header # /home/saul/thundergate/include/nvram.h: 44

nvram_command = struct_nvram_command # /home/saul/thundergate/include/nvram.h: 95

nvram_status = struct_nvram_status # /home/saul/thundergate/include/nvram.h: 119

nvram_software_arbitration = struct_nvram_software_arbitration # /home/saul/thundergate/include/nvram.h: 129

nvram_access = struct_nvram_access # /home/saul/thundergate/include/nvram.h: 149

nvram_write1 = struct_nvram_write1 # /home/saul/thundergate/include/nvram.h: 159

nvram_arbitration_watchdog = struct_nvram_arbitration_watchdog # /home/saul/thundergate/include/nvram.h: 165

nvram_auto_sense_status = struct_nvram_auto_sense_status # /home/saul/thundergate/include/nvram.h: 175

nvram_regs = struct_nvram_regs # /home/saul/thundergate/include/nvram.h: 187

otp_mode = struct_otp_mode # /home/saul/thundergate/include/otp.h: 24

otp_control = struct_otp_control # /home/saul/thundergate/include/otp.h: 29

otp_status = struct_otp_status # /home/saul/thundergate/include/otp.h: 49

otp_addr = struct_otp_addr # /home/saul/thundergate/include/otp.h: 65

otp_soft_reset = struct_otp_soft_reset # /home/saul/thundergate/include/otp.h: 70

otp_regs = struct_otp_regs # /home/saul/thundergate/include/otp.h: 75

pcie_pl_lo_regs = struct_pcie_pl_lo_regs # /home/saul/thundergate/include/pcie_alt.h: 22

pcie_dl_lo_ftsmax = struct_pcie_dl_lo_ftsmax # /home/saul/thundergate/include/pcie_alt.h: 31

pcie_dl_lo_regs = struct_pcie_dl_lo_regs # /home/saul/thundergate/include/pcie_alt.h: 36

pcie_alt_regs = struct_pcie_alt_regs # /home/saul/thundergate/include/pcie_alt.h: 43

pcie_tl_tlp_ctrl = struct_pcie_tl_tlp_ctrl # /home/saul/thundergate/include/pcie.h: 22

pcie_tl_transaction_config = struct_pcie_tl_transaction_config # /home/saul/thundergate/include/pcie.h: 46

pcie_tl_wdma_len_byte_en_req_diag = struct_pcie_tl_wdma_len_byte_en_req_diag # /home/saul/thundergate/include/pcie.h: 75

pcie_tl_rdma_len_req_diag = struct_pcie_tl_rdma_len_req_diag # /home/saul/thundergate/include/pcie.h: 82

pcie_tl_msi_len_req_diag = struct_pcie_tl_msi_len_req_diag # /home/saul/thundergate/include/pcie.h: 88

pcie_tl_slave_req_len_type_diag = struct_pcie_tl_slave_req_len_type_diag # /home/saul/thundergate/include/pcie.h: 94

pcie_tl_flow_control_inputs_diag = struct_pcie_tl_flow_control_inputs_diag # /home/saul/thundergate/include/pcie.h: 102

pcie_tl_xmt_state_machines_gated_reqs_diag = struct_pcie_tl_xmt_state_machines_gated_reqs_diag # /home/saul/thundergate/include/pcie.h: 111

pcie_tl_tlp_bdf = struct_pcie_tl_tlp_bdf # /home/saul/thundergate/include/pcie.h: 122

pcie_tl_regs = struct_pcie_tl_regs # /home/saul/thundergate/include/pcie.h: 130

pcie_dl_ctrl = struct_pcie_dl_ctrl # /home/saul/thundergate/include/pcie.h: 174

pcie_dl_status = struct_pcie_dl_status # /home/saul/thundergate/include/pcie.h: 190

pcie_dl_attn = struct_pcie_dl_attn # /home/saul/thundergate/include/pcie.h: 210

pcie_dl_attn_mask = struct_pcie_dl_attn_mask # /home/saul/thundergate/include/pcie.h: 219

pcie_dl_seq_no = struct_pcie_dl_seq_no # /home/saul/thundergate/include/pcie.h: 229

pcie_dl_replay = struct_pcie_dl_replay # /home/saul/thundergate/include/pcie.h: 234

pcie_dl_ack_timeout = struct_pcie_dl_ack_timeout # /home/saul/thundergate/include/pcie.h: 240

pcie_dl_pm_threshold = struct_pcie_dl_pm_threshold # /home/saul/thundergate/include/pcie.h: 245

pcie_dl_retry_buffer_ptr = struct_pcie_dl_retry_buffer_ptr # /home/saul/thundergate/include/pcie.h: 253

pcie_dl_test = struct_pcie_dl_test # /home/saul/thundergate/include/pcie.h: 258

pcie_dl_packet_bist = struct_pcie_dl_packet_bist # /home/saul/thundergate/include/pcie.h: 278

pcie_dl_regs = struct_pcie_dl_regs # /home/saul/thundergate/include/pcie.h: 290

pcie_pl_regs = struct_pcie_pl_regs # /home/saul/thundergate/include/pcie.h: 320

pci_status = struct_pci_status # /home/saul/thundergate/include/pci.h: 22

pci_command = struct_pci_command # /home/saul/thundergate/include/pci.h: 43

pci_pm_cap = struct_pci_pm_cap # /home/saul/thundergate/include/pci.h: 63

pci_pm_ctrl_status = struct_pci_pm_ctrl_status # /home/saul/thundergate/include/pci.h: 76

pci_msi_cap_hdr = struct_pci_msi_cap_hdr # /home/saul/thundergate/include/pci.h: 89

pci_misc_host_ctrl = struct_pci_misc_host_ctrl # /home/saul/thundergate/include/pci.h: 100

pci_dma_rw_ctrl = struct_pci_dma_rw_ctrl # /home/saul/thundergate/include/pci.h: 115

pci_state = struct_pci_state # /home/saul/thundergate/include/pci.h: 126

pci_device_id = struct_pci_device_id # /home/saul/thundergate/include/pci.h: 152

pci_class_code_rev_id = struct_pci_class_code_rev_id # /home/saul/thundergate/include/pci.h: 157

pci_regs = struct_pci_regs # /home/saul/thundergate/include/pci.h: 162

rbdc_mode = struct_rbdc_mode # /home/saul/thundergate/include/rbdc.h: 22

rbdc_status = struct_rbdc_status # /home/saul/thundergate/include/rbdc.h: 31

rbdc_rbd_pi = struct_rbdc_rbd_pi # /home/saul/thundergate/include/rbdc.h: 37

rbdc_regs = struct_rbdc_regs # /home/saul/thundergate/include/rbdc.h: 42

rbdi_mode = struct_rbdi_mode # /home/saul/thundergate/include/rbdi.h: 22

rbdi_status = struct_rbdi_status # /home/saul/thundergate/include/rbdi.h: 34

rbdi_ring_replenish_threshold = struct_rbdi_ring_replenish_threshold # /home/saul/thundergate/include/rbdi.h: 40

rbdi_regs = struct_rbdi_regs # /home/saul/thundergate/include/rbdi.h: 45

rbd_rule = struct_rbd_rule # /home/saul/thundergate/include/rbdrules.h: 24

rbd_value_mask = struct_rbd_value_mask # /home/saul/thundergate/include/rbdrules.h: 40

rcb_flags = struct_rcb_flags # /home/saul/thundergate/include/rcb.h: 22

rcb = struct_rcb # /home/saul/thundergate/include/rcb.h: 28

rdc_mode = struct_rdc_mode # /home/saul/thundergate/include/rdc.h: 22

rdc_regs = struct_rdc_regs # /home/saul/thundergate/include/rdc.h: 34

rdi_mode = struct_rdi_mode # /home/saul/thundergate/include/rdi.h: 22

rdi_status = struct_rdi_status # /home/saul/thundergate/include/rdi.h: 31

rcb_registers = struct_rcb_registers # /home/saul/thundergate/include/rdi.h: 38

rdi_regs = struct_rdi_regs # /home/saul/thundergate/include/rdi.h: 50

rdma_mode = struct_rdma_mode # /home/saul/thundergate/include/rdma.h: 24

rdma_status = struct_rdma_status # /home/saul/thundergate/include/rdma.h: 52

rdma_programmable_ipv6_extension_header = struct_rdma_programmable_ipv6_extension_header # /home/saul/thundergate/include/rdma.h: 69

rdma_rstates_debug = struct_rdma_rstates_debug # /home/saul/thundergate/include/rdma.h: 77

rdma_rstate2_debug = struct_rdma_rstate2_debug # /home/saul/thundergate/include/rdma.h: 84

rdma_bd_status_debug = struct_rdma_bd_status_debug # /home/saul/thundergate/include/rdma.h: 89

rdma_req_ptr_debug = struct_rdma_req_ptr_debug # /home/saul/thundergate/include/rdma.h: 96

rdma_hold_d_dmad_debug = struct_rdma_hold_d_dmad_debug # /home/saul/thundergate/include/rdma.h: 105

rdma_length_and_address_index_debug = struct_rdma_length_and_address_index_debug # /home/saul/thundergate/include/rdma.h: 110

rdma_mbuf_byte_count_debug = struct_rdma_mbuf_byte_count_debug # /home/saul/thundergate/include/rdma.h: 115

rdma_pcie_mbuf_byte_count_debug = struct_rdma_pcie_mbuf_byte_count_debug # /home/saul/thundergate/include/rdma.h: 120

rdma_pcie_read_request_address_debug = struct_rdma_pcie_read_request_address_debug # /home/saul/thundergate/include/rdma.h: 137

rdma_fifo1_debug = struct_rdma_fifo1_debug # /home/saul/thundergate/include/rdma.h: 142

rdma_fifo2_debug = struct_rdma_fifo2_debug # /home/saul/thundergate/include/rdma.h: 147

rdma_packet_request_debug_1 = struct_rdma_packet_request_debug_1 # /home/saul/thundergate/include/rdma.h: 153

rdma_packet_request_debug_2 = struct_rdma_packet_request_debug_2 # /home/saul/thundergate/include/rdma.h: 158

rdma_packet_request_debug_3 = struct_rdma_packet_request_debug_3 # /home/saul/thundergate/include/rdma.h: 162

rdma_tcp_checksum_debug = struct_rdma_tcp_checksum_debug # /home/saul/thundergate/include/rdma.h: 173

rdma_ip_tcp_header_checksum_debug = struct_rdma_ip_tcp_header_checksum_debug # /home/saul/thundergate/include/rdma.h: 180

rdma_pseudo_checksum_debug = struct_rdma_pseudo_checksum_debug # /home/saul/thundergate/include/rdma.h: 185

rdma_mbuf_address_debug = struct_rdma_mbuf_address_debug # /home/saul/thundergate/include/rdma.h: 190

rdma_misc_ctrl_1 = struct_rdma_misc_ctrl_1 # /home/saul/thundergate/include/rdma.h: 201

rdma_misc_ctrl_2 = struct_rdma_misc_ctrl_2 # /home/saul/thundergate/include/rdma.h: 212

rdma_misc_ctrl_3 = struct_rdma_misc_ctrl_3 # /home/saul/thundergate/include/rdma.h: 222

rdma_regs = struct_rdma_regs # /home/saul/thundergate/include/rdma.h: 232

receive_list_placement_mode = struct_receive_list_placement_mode # /home/saul/thundergate/include/rlp.h: 22

receive_list_placement_status = struct_receive_list_placement_status # /home/saul/thundergate/include/rlp.h: 31

receive_selector_not_empty_bits = struct_receive_selector_not_empty_bits # /home/saul/thundergate/include/rlp.h: 39

receive_list_placement_configuration = struct_receive_list_placement_configuration # /home/saul/thundergate/include/rlp.h: 44

receive_list_placement_statistics_control = struct_receive_list_placement_statistics_control # /home/saul/thundergate/include/rlp.h: 52

receive_list_placement_statistics_enable_mask = struct_receive_list_placement_statistics_enable_mask # /home/saul/thundergate/include/rlp.h: 59

receive_list_placement_statistics_increment_mask = struct_receive_list_placement_statistics_increment_mask # /home/saul/thundergate/include/rlp.h: 79

receive_list_local_statistics_counter = struct_receive_list_local_statistics_counter # /home/saul/thundergate/include/rlp.h: 86

receive_list_lock = struct_receive_list_lock # /home/saul/thundergate/include/rlp.h: 91

rlp_regs = struct_rlp_regs # /home/saul/thundergate/include/rlp.h: 96

rss_ind_table_1 = struct_rss_ind_table_1 # /home/saul/thundergate/include/rss.h: 22

rss_ind_table_2 = struct_rss_ind_table_2 # /home/saul/thundergate/include/rss.h: 40

rss_ind_table_3 = struct_rss_ind_table_3 # /home/saul/thundergate/include/rss.h: 58

rss_ind_table_4 = struct_rss_ind_table_4 # /home/saul/thundergate/include/rss.h: 76

rss_ind_table_5 = struct_rss_ind_table_5 # /home/saul/thundergate/include/rss.h: 94

rss_ind_table_6 = struct_rss_ind_table_6 # /home/saul/thundergate/include/rss.h: 112

rss_ind_table_7 = struct_rss_ind_table_7 # /home/saul/thundergate/include/rss.h: 130

rss_ind_table_8 = struct_rss_ind_table_8 # /home/saul/thundergate/include/rss.h: 148

rss_ind_table_9 = struct_rss_ind_table_9 # /home/saul/thundergate/include/rss.h: 166

rss_ind_table_10 = struct_rss_ind_table_10 # /home/saul/thundergate/include/rss.h: 185

rss_ind_table_11 = struct_rss_ind_table_11 # /home/saul/thundergate/include/rss.h: 203

rss_ind_table_12 = struct_rss_ind_table_12 # /home/saul/thundergate/include/rss.h: 221

rss_ind_table_13 = struct_rss_ind_table_13 # /home/saul/thundergate/include/rss.h: 239

rss_ind_table_14 = struct_rss_ind_table_14 # /home/saul/thundergate/include/rss.h: 257

rss_ind_table_15 = struct_rss_ind_table_15 # /home/saul/thundergate/include/rss.h: 275

rss_ind_table_16 = struct_rss_ind_table_16 # /home/saul/thundergate/include/rss.h: 293

rss_hash_key = struct_rss_hash_key # /home/saul/thundergate/include/rss.h: 311

rmac_programmable_ipv6_extension_header = struct_rmac_programmable_ipv6_extension_header # /home/saul/thundergate/include/rss.h: 317

rss_regs = struct_rss_regs # /home/saul/thundergate/include/rss.h: 325

rtsdi_mode = struct_rtsdi_mode # /home/saul/thundergate/include/rtsdi.h: 24

rtsdi_status = struct_rtsdi_status # /home/saul/thundergate/include/rtsdi.h: 34

rtsdi_statistics_control = struct_rtsdi_statistics_control # /home/saul/thundergate/include/rtsdi.h: 40

rtsdi_statistics_mask = struct_rtsdi_statistics_mask # /home/saul/thundergate/include/rtsdi.h: 49

rtsdi_statistics_increment_mask = struct_rtsdi_statistics_increment_mask # /home/saul/thundergate/include/rtsdi.h: 54

rtsdi_regs = struct_rtsdi_regs # /home/saul/thundergate/include/rtsdi.h: 61

sbdc_mode = struct_sbdc_mode # /home/saul/thundergate/include/sbdc.h: 24

sbdc_debug = struct_sbdc_debug # /home/saul/thundergate/include/sbdc.h: 31

sbdc_regs = struct_sbdc_regs # /home/saul/thundergate/include/sbdc.h: 36

sbdi_mode = struct_sbdi_mode # /home/saul/thundergate/include/sbdi.h: 24

sbdi_status = struct_sbdi_status # /home/saul/thundergate/include/sbdi.h: 34

sbdi_regs = struct_sbdi_regs # /home/saul/thundergate/include/sbdi.h: 40

sbds_mode = struct_sbds_mode # /home/saul/thundergate/include/sbds.h: 22

sbds_status = struct_sbds_status # /home/saul/thundergate/include/sbds.h: 29

sbds_local_nic_send_bd_consumer_idx = struct_sbds_local_nic_send_bd_consumer_idx # /home/saul/thundergate/include/sbds.h: 35

sbds_regs = struct_sbds_regs # /home/saul/thundergate/include/sbds.h: 40

sdc_mode = struct_sdc_mode # /home/saul/thundergate/include/sdc.h: 24

sdc_pre_dma_command_exchange = struct_sdc_pre_dma_command_exchange # /home/saul/thundergate/include/sdc.h: 32

sdc_regs = struct_sdc_regs # /home/saul/thundergate/include/sdc.h: 41

sdi_mode = struct_sdi_mode # /home/saul/thundergate/include/sdi.h: 24

sdi_status = struct_sdi_status # /home/saul/thundergate/include/sdi.h: 34

sdi_statistics_control = struct_sdi_statistics_control # /home/saul/thundergate/include/sdi.h: 40

sdi_statistics_mask = struct_sdi_statistics_mask # /home/saul/thundergate/include/sdi.h: 49

sdi_statistics_increment_mask = struct_sdi_statistics_increment_mask # /home/saul/thundergate/include/sdi.h: 54

sdi_regs = struct_sdi_regs # /home/saul/thundergate/include/sdi.h: 61

mac_stats_regs = struct_mac_stats_regs # /home/saul/thundergate/include/stats.h: 22

status_block = struct_status_block # /home/saul/thundergate/include/status_block.h: 24

tsc_length_offset = struct_tsc_length_offset # /home/saul/thundergate/include/tcp_seg_ctrl.h: 22

tsc_dma_flags = struct_tsc_dma_flags # /home/saul/thundergate/include/tcp_seg_ctrl.h: 28

tsc_vlan_tag = struct_tsc_vlan_tag # /home/saul/thundergate/include/tcp_seg_ctrl.h: 51

tsc_pre_dma_cmd_xchng = struct_tsc_pre_dma_cmd_xchng # /home/saul/thundergate/include/tcp_seg_ctrl.h: 56

tcp_seg_ctrl_regs = struct_tcp_seg_ctrl_regs # /home/saul/thundergate/include/tcp_seg_ctrl.h: 65

wdma_mode = struct_wdma_mode # /home/saul/thundergate/include/wdma.h: 24

wdma_status = struct_wdma_status # /home/saul/thundergate/include/wdma.h: 49

wdma_regs = struct_wdma_regs # /home/saul/thundergate/include/wdma.h: 59

# No inserted files

