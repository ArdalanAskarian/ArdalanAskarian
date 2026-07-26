#!/bin/bash
# Fetch the two typefaces build_svg.py outlines from. Both are OFL, which
# permits converting glyphs to paths and redistributing the result - which is
# what the committed SVGs contain. The font files themselves are gitignored.
#
#   ./tools/fetch_fonts.sh && python3 tools/build_svg.py
#
# Archivo is variable; build_svg.py instantiates it at wdth=125 (Expanded).
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)/fonts"
GF="https://raw.githubusercontent.com/google/fonts/main/ofl"
mkdir -p "$DIR"

fetch() {
  echo "  $2"
  curl -sfL --retry 3 -o "$DIR/$2" "$1"
}

echo "fetching fonts into tools/fonts/"
fetch "$GF/archivo/Archivo%5Bwdth%2Cwght%5D.ttf" "Archivo.ttf"
fetch "$GF/ibmplexmono/IBMPlexMono-Regular.ttf" "PlexMono-Reg.ttf"
fetch "$GF/ibmplexmono/IBMPlexMono-SemiBold.ttf" "PlexMono-SBd.ttf"
fetch "$GF/archivo/OFL.txt" "OFL-archivo.txt"
fetch "$GF/ibmplexmono/OFL.txt" "OFL-plexmono.txt"
echo "done. now: python3 tools/build_svg.py  (needs fonttools)"
