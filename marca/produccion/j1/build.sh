#!/bin/sh
# J1: de cero al borrador con sonido. Uso: sh build.sh
# LIB es la carpeta de Lemo-Opuscar (por omisión, ~/lemo-opuscar). Antes hace falta la voz en voz/a.mp3 y voz/b.mp3:
#   python marca/scripts/voz.py marca/produccion/j1/voz a "<tramo a>" b "<tramo b>"   (los textos están en TREATMENT.md)
set -e
HERE=$(cd "$(dirname "$0")" && pwd -W 2>/dev/null || pwd)
LIB=${LIB:-$HOME/lemo-opuscar}
export LIB
[ -f "$LIB/core/render/video.mjs" ] || { echo "poné en LIB la carpeta de Lemo-Opuscar"; exit 1; }
PY="$LIB/.venv/Scripts/python.exe"; [ -x "$PY" ] || PY="$LIB/.venv/bin/python"
cd "$LIB"
node core/render/events.mjs "$HERE" --size 1080x1920
node core/render/video.mjs "$HERE" --fps 24 --workers 4 --size 1080x1920 --out "$HERE/out/video.mp4"
"$PY" "$HERE/mix.py" "$LIB"                                   # marcador, borrador, voz y música -> out/mix.wav
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/out/j1-borrador.mp4" 24 1
