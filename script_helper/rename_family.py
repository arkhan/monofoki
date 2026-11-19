#!/usr/bin/env python3
"""Rename a patched font family in place: rename_family.py NAME FILE..."""
import sys

from fontTools.ttLib import TTFont

new = sys.argv[1]
for path in sys.argv[2:]:
    f = TTFont(path)
    names = f['name']
    style = names.getDebugName(2)  # Regular / Italic / Bold / Bold Italic
    full = new if style == 'Regular' else '%s %s' % (new, style)
    ps = '%s-%s' % (new, style.replace(' ', ''))
    for n in list(names.names):
        if n.nameID in (1, 16):
            n.string = new
        elif n.nameID in (4,):
            n.string = full
        elif n.nameID == 6:
            n.string = ps
        elif n.nameID == 3:
            n.string = '%s;%s' % (new, ps)
        elif n.nameID == 17:
            n.string = style
        elif n.nameID in (21, 22):
            names.removeNames(nameID=n.nameID)
    if 'CFF ' in f:
        f['CFF '].cff.fontNames = [ps]
    f.save(path)
    print(path, '->', full)
