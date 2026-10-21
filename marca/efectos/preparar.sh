#!/bin/sh
# Deja lista una carpeta para usar la biblioteca de efectos: copia efectos.js y las fuentes de la marca.
# Uso: sh marca/efectos/preparar.sh <carpeta de la pieza>     (sin carpeta, prepara el carrete de muestra)
# Después, el render: cd ~/lemo-opuscar && node core/render/video.mjs <carpeta> --fps 24 --workers 4 --size 1080x1920
set -e
AQUI=$(cd "$(dirname "$0")" && pwd)
DEST=${1:-$AQUI}
mkdir -p "$DEST/fuentes"
cp "$AQUI/../estilo/fuentes/"*.woff2 "$DEST/fuentes/"
cp "$AQUI/../estilo/fuentes/"*.ttf "$DEST/fuentes/"
[ "$DEST" = "$AQUI" ] || cp "$AQUI/efectos.js" "$DEST/"
echo "listo: $DEST"
