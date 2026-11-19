#!/usr/bin/env fontforge
"""
Import Powerline Extra separators (U+E0B4–U+E0D4) from CascadiaCodeNF
into all 4 Monofoki SFD variants.

The existing Powerline glyphs in Monofoki span the full cell:
  x: 0 → 575   (advance width)
  y: -250 → 900  (full OS/2 Win ascent/descent)

New glyphs are scaled to match this exactly so separators tile seamlessly.

Run with:  fontforge -script script_helper/import_powerline_extra.py
"""

import fontforge
import psMat
import os

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')

CASCADIA_REG  = '/home/arkhan/.guix-profile/share/fonts/truetype/CascadiaCodeNF-Regular.ttf'
CASCADIA_BOLD = '/home/arkhan/.guix-profile/share/fonts/truetype/CascadiaCodeNF-Bold.ttf'

# Target cell dimensions — must match existing E0B0/E0B2 in Monofoki
TARGET_W      = 575
TARGET_Y_MIN  = -250
TARGET_Y_MAX  =  900
TARGET_H      = TARGET_Y_MAX - TARGET_Y_MIN   # 1150

# All 33 codepoints in the Powerline Extra block
POWERLINE_EXTRA = list(range(0xE0B4, 0xE0D5))

VARIANTS = [
    ('monofoki-Regular.sfd',     CASCADIA_REG),
    ('monofoki-Italic.sfd',      CASCADIA_REG),
    ('monofoki-Bold.sfd',        CASCADIA_BOLD),
    ('monofoki-Bold-Italic.sfd', CASCADIA_BOLD),
]


def fit_to_cell(glyph):
    """Scale and position a Powerline glyph to exactly fill the Monofoki cell."""
    bb = glyph.boundingBox()   # (xmin, ymin, xmax, ymax)
    gw = bb[2] - bb[0]
    gh = bb[3] - bb[1]
    if gw == 0 or gh == 0:
        glyph.width = TARGET_W
        return

    # Scale uniformly to fill cell height; cap by width if result overflows
    scale = TARGET_H / gh
    if gw * scale > TARGET_W:
        scale = TARGET_W / gw
    glyph.transform(psMat.scale(scale))

    bb = glyph.boundingBox()
    gw = bb[2] - bb[0]

    # After height-scaling, center horizontally within TARGET_W
    # (some separators are naturally narrower, e.g. thin variants)
    cx = bb[0] + gw / 2
    shift_x = TARGET_W / 2 - cx

    # Align bottom to TARGET_Y_MIN
    shift_y = TARGET_Y_MIN - bb[1]

    glyph.transform(psMat.translate(shift_x, shift_y))
    glyph.width = TARGET_W


def import_powerline(sfd_name, src_path):
    sfd_path = os.path.join(FONT_DIR, sfd_name)
    print('\n=== ' + sfd_name + ' ===')

    dst = fontforge.open(sfd_path)
    src = fontforge.open(src_path)

    imported = 0
    skipped  = 0

    for cp in POWERLINE_EXTRA:
        try:
            g = src[cp]
            if not g.isWorthOutputting():
                print('  skip (empty)  U+%04X' % cp)
                skipped += 1
                continue
        except Exception:
            print('  skip (absent) U+%04X' % cp)
            skipped += 1
            continue

        src.selection.select(cp)
        src.copy()

        if cp not in [g.unicode for g in dst.glyphs()]:
            dst.createChar(cp)

        dst.selection.select(cp)
        dst.paste()

        fit_to_cell(dst[cp])
        imported += 1
        print('  ok  U+%04X' % cp)

    src.close()
    dst.save(sfd_path)
    print('  imported %d, skipped %d  →  saved %s' % (imported, skipped, sfd_path))


for sfd_name, src_path in VARIANTS:
    import_powerline(sfd_name, src_path)

print('\nDone.')
