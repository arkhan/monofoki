#!/usr/bin/env fontforge
"""
Import missing symbols into all 4 Monofoki SFD variants and fix proportions
of existing geometric glyphs.

Sources (both OFL/MIT licensed):
  - DejaVu Sans Mono  → keyboard symbols, arrows, currency (except ₿), ☆ ❤, ◆ ◇
  - Cascadia Code     → control pictures (␀ ␉ ␊ ␍) and ₿

Run with:  fontforge -script script_helper/import_symbols.py

To audit what symbols are missing from the compiled font run:
  fontforge -script script_helper/import_symbols.py --audit
"""

import fontforge
import psMat
import os
import sys

MONOFOKI_WIDTH = 575
CAP_HIGH  = 700
BASELINE  =   0
V_CENTER  = (CAP_HIGH + BASELINE) / 2   # 350

# Optical center matching ● (U+25CF): center=(287,306), size=506x505
GEOM_CX   = 287.5
GEOM_CY   = 306.0
ARROW_CY  = V_CENTER  # 350 — centrado vertical entre baseline y cap height

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')

import subprocess
DEJAVU_DIR   = os.path.dirname(subprocess.check_output(
    ['fc-match', '-f', '%{file}', 'DejaVu Sans Mono']).decode())
CASCADIA_DIR = '/home/arkhan/.guix-profile/share/fonts/truetype'

# (codepoint, source_tag)
# source_tag: 'dv'=DejaVu, 'cc'=Cascadia
SYMBOLS = [
    # Keyboard / control symbols
    (0x238B, 'dv'),   # ⎋ BROKEN CIRCLE (Escape)
    (0x2423, 'dv'),   # ␣ OPEN BOX (visible space)
    (0x2303, 'dv'),   # ⌃ UP ARROWHEAD (Ctrl)
    (0x2318, 'dv'),   # ⌘ PLACE OF INTEREST SIGN (Cmd)
    (0x2325, 'dv'),   # ⌥ OPTION KEY
    (0x21E5, 'dv'),   # ⇥ RIGHTWARDS ARROW TO BAR (Tab)
    # Control pictures
    (0x2400, 'cc'),   # ␀ SYMBOL FOR NULL
    (0x2409, 'cc'),   # ␉ SYMBOL FOR HORIZONTAL TABULATION
    (0x240A, 'cc'),   # ␊ SYMBOL FOR LINE FEED
    (0x240D, 'cc'),   # ␍ SYMBOL FOR CARRIAGE RETURN
    # Arrows
    (0x21B5, 'dv'),   # ↵ DOWNWARDS ARROW WITH CORNER LEFTWARDS
    (0x27A1, 'dv'),   # ➡ BLACK RIGHTWARDS ARROW
    (0x2794, 'dv'),   # ➔ HEAVY WIDE-HEADED RIGHTWARDS ARROW
    (0x2799, 'dv'),   # ➙ HEAVY RIGHTWARDS ARROW
    (0x279E, 'dv'),   # ➞ HEAVY TRIANGLE-HEADED RIGHTWARDS ARROW
    # Currency
    (0x20B9, 'dv'),   # ₹ INDIAN RUPEE SIGN
    (0x20BF, 'cc'),   # ₿ BITCOIN SIGN
    (0x20BA, 'dv'),   # ₺ TURKISH LIRA SIGN
    # Misc
    (0x2606, 'dv'),   # ☆ WHITE STAR
    (0x2764, 'dv'),   # ❤ HEAVY BLACK HEART
    # Diamonds (◆ ◇) — used by jj, git log, lazygit, etc.
    (0x25C6, 'dv'),   # ◆ BLACK DIAMOND
    (0x25C7, 'dv'),   # ◇ WHITE DIAMOND
    # Used by agent-shell header/icons and org-modern
    (0x27A4, 'dv'),   # ➤ BLACK RIGHTWARDS ARROWHEAD (agent-shell header separator)
    (0x26A0, 'dv'),   # ⚠ WARNING SIGN
    (0x2736, 'dv'),   # ✶ SIX POINTED BLACK STAR
    (0x2733, 'dv'),   # ✳ EIGHT SPOKED ASTERISK
    (0x2611, 'dv'),   # ☑ BALLOT BOX WITH CHECK
    (0x275D, 'dv'),   # ❝ HEAVY DOUBLE TURNED COMMA QUOTATION MARK
    (0x2023, 'dv'),   # ‣ TRIANGULAR BULLET
    (0x25C8, 'dv'),   # ◈ WHITE DIAMOND CONTAINING BLACK SMALL DIAMOND
    (0x25C9, 'dv'),   # ◉ FISHEYE
    (0x25E6, 'dv'),   # ◦ WHITE BULLET
    (0x2BC6, 'cc'),   # ⯆ BLACK MEDIUM DOWN-POINTING TRIANGLE CENTRED
    (0x2BC8, 'cc'),   # ⯈ BLACK MEDIUM RIGHT-POINTING TRIANGLE CENTRED
] + [(cp, 'br') for cp in range(0x2800, 0x2900)] + [
]

# Glyphs already in the font that need size/position correction.
# (codepoint, target_size, target_cx, target_cy)
# target_size: largest dimension scaled to this value (uniform scale).
RESCALE = [
    # ↑↓ were 717px — exceeded cap height. Scaled to 550 (tall but not clipping).
    (0x2191, 550, GEOM_CX, ARROW_CY),  # ↑ UPWARDS ARROW
    (0x2193, 550, GEOM_CX, ARROW_CY),  # ↓ DOWNWARDS ARROW
    # All 8 directional triangles unified: same height+center so ▼/▶ pairs
    # (used as expand/collapse indicators in file trees) look consistent.
    (0x25B2, 460, GEOM_CX, GEOM_CY),   # ▲ BLACK UP-POINTING TRIANGLE
    (0x25BC, 460, GEOM_CX, GEOM_CY),   # ▼ BLACK DOWN-POINTING TRIANGLE
    (0x25B6, 460, GEOM_CX, GEOM_CY),   # ▶ BLACK RIGHT-POINTING TRIANGLE
    (0x25C0, 460, GEOM_CX, GEOM_CY),   # ◀ BLACK LEFT-POINTING TRIANGLE
    (0x25B3, 460, GEOM_CX, GEOM_CY),   # △ WHITE UP-POINTING TRIANGLE
    (0x25BD, 460, GEOM_CX, GEOM_CY),   # ▽ WHITE DOWN-POINTING TRIANGLE
    (0x25B7, 460, GEOM_CX, GEOM_CY),   # ▷ WHITE RIGHT-POINTING TRIANGLE
    (0x25C1, 460, GEOM_CX, GEOM_CY),   # ◁ WHITE LEFT-POINTING TRIANGLE
    # Small triangles — same center, smaller size
    (0x25B4, 380, GEOM_CX, GEOM_CY),   # ▴ BLACK UP-POINTING SMALL TRIANGLE
    (0x25BE, 380, GEOM_CX, GEOM_CY),   # ▾ BLACK DOWN-POINTING SMALL TRIANGLE
    (0x25B5, 380, GEOM_CX, GEOM_CY),   # ▵ WHITE UP-POINTING SMALL TRIANGLE
    (0x25BF, 380, GEOM_CX, GEOM_CY),   # ▿ WHITE DOWN-POINTING SMALL TRIANGLE
]

VARIANTS = [
    ('monofoki-Regular.sfd',     'regular'),
    ('monofoki-Italic.sfd',      'regular'),
    ('monofoki-Bold.sfd',        'bold'),
    ('monofoki-Bold-Italic.sfd', 'bold'),
]

SOURCES = {
    'regular': {
        'dv': os.path.join(DEJAVU_DIR,  'DejaVuSansMono.ttf'),
        'cc': os.path.join(CASCADIA_DIR, 'CascadiaCode-Regular.ttf'),
        'br': os.path.join(CASCADIA_DIR, 'CascadiaCode-Regular.ttf'),
    },
    'bold': {
        'dv': os.path.join(DEJAVU_DIR,  'DejaVuSansMono-Bold.ttf'),
        'cc': os.path.join(CASCADIA_DIR, 'CascadiaCode-Bold.ttf'),
        # braille is not emboldened: always the Regular source
        'br': os.path.join(CASCADIA_DIR, 'CascadiaCode-Regular.ttf'),
    },
}


def fit_glyph(glyph, max_h, max_w, cx, cy):
    """Scale glyph to fit within max_h/max_w and center at (cx, cy)."""
    bb = glyph.boundingBox()
    gw, gh = bb[2]-bb[0], bb[3]-bb[1]
    if gw == 0 or gh == 0:
        glyph.width = MONOFOKI_WIDTH
        return
    scale = min(max_h / gh, max_w / gw)
    if scale < 0.99:
        glyph.transform(psMat.scale(scale))
        bb = glyph.boundingBox()
        gw, gh = bb[2]-bb[0], bb[3]-bb[1]
    glyph.transform(psMat.translate(cx - (bb[0]+gw/2), cy - (bb[1]+gh/2)))
    glyph.width = MONOFOKI_WIDTH


def rescale_glyph(glyph, target_size, cx, cy):
    """Scale glyph so its largest dimension = target_size, then center."""
    bb = glyph.boundingBox()
    gw, gh = bb[2]-bb[0], bb[3]-bb[1]
    if gw == 0 or gh == 0:
        return
    scale = target_size / max(gw, gh)
    glyph.transform(psMat.scale(scale))
    bb = glyph.boundingBox()
    gw, gh = bb[2]-bb[0], bb[3]-bb[1]
    glyph.transform(psMat.translate(cx - (bb[0]+gw/2), cy - (bb[1]+gh/2)))
    glyph.width = MONOFOKI_WIDTH


def import_glyph(dst, src_font, cp):
    """Copy glyph cp from src_font into dst. Returns True on success."""
    try:
        g = src_font[cp]
        if not g.isWorthOutputting():
            return False
    except Exception:
        return False

    src_font.selection.select(cp)
    src_font.copy()

    if cp not in [g.unicode for g in dst.glyphs()]:
        dst.createChar(cp)

    dst.selection.select(cp)
    dst.paste()

    # Geometric bullets: match ● optical center/size
    if cp in (0x25C6, 0x25C7, 0x25C8, 0x25C9):
        rescale_glyph(dst[cp], 500, GEOM_CX, GEOM_CY)
    elif cp in (0x25E6, 0x2023):
        # keep native size, only center
        bb = dst[cp].boundingBox()
        dst[cp].transform(psMat.translate(GEOM_CX - (bb[0]+bb[2])/2, GEOM_CY - (bb[1]+bb[3])/2))
        dst[cp].width = MONOFOKI_WIDTH
    elif 0x2800 <= cp <= 0x28FF:
        # keep dot grid vertical position; only fit advance width
        s = MONOFOKI_WIDTH / dst[cp].width
        dst[cp].transform(psMat.scale(s, 1))
        dst[cp].width = MONOFOKI_WIDTH
    else:
        fit_glyph(dst[cp], CAP_HIGH, MONOFOKI_WIDTH * 0.90, MONOFOKI_WIDTH / 2, V_CENTER)
    return True


def process_variant(sfd_name, weight):
    sfd_path = os.path.join(FONT_DIR, sfd_name)
    print('\n=== ' + sfd_name + ' (' + weight + ') ===')

    dst = fontforge.open(sfd_path)
    srcs = {}
    for tag, path in SOURCES[weight].items():
        srcs[tag] = fontforge.open(path)

    print('  -- imports --')
    for cp, tag in SYMBOLS:
        src = srcs[tag]
        ok = import_glyph(dst, src, cp)
        import unicodedata
        name = unicodedata.name(chr(cp), '?')
        print(('  ok ' if ok else '  FAILED ') + 'U+%04X %s  %s' % (cp, chr(cp), name))

    print('  -- rescale existing --')
    for cp, target_size, cx, cy in RESCALE:
        try:
            rescale_glyph(dst[cp], target_size, cx, cy)
            bb = dst[cp].boundingBox()
            print('  ok U+%04X %s  size=%.0fx%.0f  center=(%.0f,%.0f)' % (
                cp, chr(cp), bb[2]-bb[0], bb[3]-bb[1],
                (bb[0]+bb[2])/2, (bb[1]+bb[3])/2))
        except Exception as e:
            print('  FAILED U+%04X: ' % cp + str(e))

    for f in {id(f): f for f in srcs.values()}.values():
        f.close()

    dst.save(sfd_path)
    print('  saved -> ' + sfd_path)


# ── Audit mode ────────────────────────────────────────────────────────────────
def audit():
    """Print unicode blocks with missing glyph counts for the Regular SFD."""
    import unicodedata

    sfd_path = os.path.join(FONT_DIR, 'monofoki-Regular.sfd')
    f = fontforge.open(sfd_path)
    present = set(g.unicode for g in f.glyphs() if g.unicode >= 0 and g.isWorthOutputting())
    f.close()

    blocks = [
        ('Basic Latin',              0x0020, 0x007E),
        ('Latin-1 Supplement',       0x00A0, 0x00FF),
        ('Latin Extended-A',         0x0100, 0x017F),
        ('Latin Extended-B',         0x0180, 0x024F),
        ('Greek and Coptic',         0x0370, 0x03FF),
        ('Cyrillic',                 0x0400, 0x04FF),
        ('General Punctuation',      0x2000, 0x206F),
        ('Superscripts/Subscripts',  0x2070, 0x209F),
        ('Currency Symbols',         0x20A0, 0x20CF),
        ('Letterlike Symbols',       0x2100, 0x214F),
        ('Arrows',                   0x2190, 0x21FF),
        ('Math Operators',           0x2200, 0x22FF),
        ('Misc Technical',           0x2300, 0x23FF),
        ('Control Pictures',         0x2400, 0x243F),
        ('Enclosed Alphanumerics',   0x2460, 0x24FF),
        ('Box Drawing',              0x2500, 0x257F),
        ('Block Elements',           0x2580, 0x259F),
        ('Geometric Shapes',         0x25A0, 0x25FF),
        ('Misc Symbols',             0x2600, 0x26FF),
        ('Dingbats',                 0x2700, 0x27BF),
        ('Braille',                  0x2800, 0x28FF),
        ('Powerline PUA',            0xE0A0, 0xE0D4),
        ('Nerd Font PUA',            0xE000, 0xF8FF),
    ]

    print('\n=== Glyph coverage audit (monofoki-Regular) ===\n')
    print('%-28s  %6s  %6s  %6s  %s' % ('Block', 'Total', 'Have', 'Miss', 'Bar'))
    print('-' * 72)
    for name, lo, hi in blocks:
        total = hi - lo + 1
        have  = sum(1 for cp in range(lo, hi+1) if cp in present)
        miss  = total - have
        pct   = have / total
        bar   = ('█' * int(pct * 20)).ljust(20)
        print('%-28s  %6d  %6d  %6d  |%s| %3d%%' % (name, total, have, miss, bar, int(pct*100)))

    print('\n=== Missing critical IDE/terminal symbols ===\n')
    critical = [
        (0x25C6,'◆ BLACK DIAMOND'),        (0x25C7,'◇ WHITE DIAMOND'),
        (0x25BC,'▼ DOWN TRIANGLE'),        (0x25B2,'▲ UP TRIANGLE'),
        (0x238B,'⎋ ESCAPE'),               (0x2423,'␣ OPEN BOX'),
        (0x2303,'⌃ CTRL'),                 (0x2318,'⌘ CMD'),
        (0x2325,'⌥ OPTION'),               (0x21E5,'⇥ TAB'),
        (0x2400,'␀ NULL'),                 (0x240D,'␍ CR'),
        (0x21B5,'↵ RETURN'),               (0x27A1,'➡ ARROW'),
        (0x20B9,'₹ RUPEE'),                (0x20BF,'₿ BITCOIN'),
        (0x2606,'☆ WHITE STAR'),           (0x2764,'❤ HEART'),
        (0xE0B0,'  PL right'),             (0xE0B4,'  PL round right'),
        (0xFFFD,'▽ REPLACEMENT CHAR'),
    ]
    for cp, desc in critical:
        status = '✓' if cp in present else '✗ MISSING'
        print('  %s  U+%04X  %s' % (status, cp, desc))


# ── Entry point ───────────────────────────────────────────────────────────────
if '--audit' in sys.argv:
    audit()
else:
    for sfd_name, weight in VARIANTS:
        process_variant(sfd_name, weight)
    print('\nDone.')
