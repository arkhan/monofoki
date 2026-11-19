#!/usr/bin/env fontforge
"""
Bake Fira Code ligatures into the Monofoki SFD sources (idempotent).

Uses LigatureCreator from Ligaturizer (https://github.com/ToxicFrog/Ligaturizer),
which must be checked out (FIRA_DIR = dir with FiraCode-*.otf/.ttf, default the fira submodule). Default location is the
parent repo (../../ relative to this repo when nested in Ligaturizer/fonts/).
Override with LIGATURIZER_DIR=/path.

Run:  fontforge -lang=py -script script_helper/add_ligatures.py
"""

import os
import sys

import fontforge

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIGA_DIR = os.environ.get('LIGATURIZER_DIR', os.path.abspath(os.path.join(ROOT, '..', '..')))
FIRA_DIR = os.environ.get('FIRA_DIR', os.path.join(LIGA_DIR, 'fonts/fira/distr/otf'))
sys.path.insert(0, LIGA_DIR)

from ligaturize import LigatureCreator  # noqa: E402
from ligatures import ligatures  # noqa: E402

VARIANTS = [
    ('monofoki-Regular.sfd',     'Regular'),
    ('monofoki-Italic.sfd',      'Regular'),
    ('monofoki-Bold.sfd',        'Bold'),
    ('monofoki-Bold-Italic.sfd', 'Bold'),
]
MARKER = 'calt'  # lookup name created by LigatureCreator.add_calt

for sfd, weight in VARIANTS:
    path = os.path.join(ROOT, 'src', sfd)
    font = fontforge.open(path)
    if any(MARKER in l for l in font.gsub_lookups):
        print('skip (ligatures already present): ' + sfd)
        font.close()
        continue
    base = os.path.join(FIRA_DIR, 'FiraCode-' + weight)
    fira = fontforge.open(base + '.otf' if os.path.exists(base + '.otf') else base + '.ttf')
    creator = LigatureCreator(font, fira,
                              scale_character_glyphs_threshold=0.1,
                              copy_character_glyphs=False)
    for spec in sorted(ligatures, key=lambda l: len(l['chars'])):
        creator.add_ligature(spec['chars'], spec['firacode_ligature_name'])
    font.save(path)
    print('ligatures baked into ' + sfd)
    fira.close()
    font.close()
