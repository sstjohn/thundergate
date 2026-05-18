#!/usr/bin/env python3
"""Embed zForth's core.zf bootstrap as a C string in forth_core.h.

The firmware has no filesystem, so the Forth bootstrap that the upstream
example would load from disk is compiled in instead. fw/Makefile runs this
when core.zf changes; the generated forth_core.h is also committed so a
checkout builds without invoking Python.
"""
import os

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "core.zf")
dst = os.path.join(here, "forth_core.h")

out = [
    "/* Generated from core.zf by embed-core.py -- do not edit by hand. */",
    "static const char forth_core[] =",
]
with open(src, "r", encoding="ascii") as f:
    for line in f:
        line = line.rstrip("\n").replace("\\", "\\\\").replace('"', '\\"')
        out.append('\t"%s\\n"' % line)
out.append("\t;")

with open(dst, "w", encoding="ascii") as f:
    f.write("\n".join(out) + "\n")

print("embed-core: wrote %s (%d source lines)" % (dst, len(out) - 3))
