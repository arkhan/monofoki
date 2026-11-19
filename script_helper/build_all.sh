#!/usr/bin/env bash
# Full pipeline; runs inside the container (or locally with the same env vars).
# Ligatures are baked into src/*.sfd by add_ligatures.py (no-op when present).
set -euo pipefail
cd "$(dirname "$0")/.."

fontforge -lang=py -script script_helper/import_symbols.py
fontforge -lang=py -script script_helper/add_ligatures.py
./create_font.sh
./post_create_nerdfonts.sh
