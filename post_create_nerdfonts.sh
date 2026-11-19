#!/usr/bin/env bash
# Patch export/Monofoki-*.{otf,ttf} with the full Nerd Fonts set (single-width)
# and rename the family to plain "monofoki". Needs fontforge, curl, unzip and
# python3 with fonttools.
set -euo pipefail
cd "$(dirname "$0")"

PATCHER_DIR=${PATCHER_DIR:-.font-build/patcher}
if [ ! -f "$PATCHER_DIR/font-patcher" ]; then
    mkdir -p "$PATCHER_DIR"
    curl -sL -o "$PATCHER_DIR/FontPatcher.zip" \
        https://github.com/ryanoasis/nerd-fonts/releases/download/${NERD_FONTS_VERSION:-v3.5.1}/FontPatcher.zip
    unzip -qo "$PATCHER_DIR/FontPatcher.zip" -d "$PATCHER_DIR"
fi

out=export/nerd
mkdir -p "$out"
for s in Regular Italic Bold Bold-Italic; do
    for e in otf ttf; do
        fontforge -lang=py -script "$PATCHER_DIR/font-patcher" --complete --mono \
            --no-progressbars --makegroups 0 -out "$out" "export/Monofoki-$s.$e" &
    done
done
wait

# font-patcher names files MonofokiNerdFontMono-*; keep plain monofoki-* names
for f in "$out"/MonofokiNerdFontMono-*; do
    mv "$f" "$out/monofoki-${f##*MonofokiNerdFontMono-}"
done
python3 script_helper/rename_family.py monofoki "$out"/monofoki-*
