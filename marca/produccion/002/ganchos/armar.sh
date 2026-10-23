#!/bin/sh
# Arma los inicios de prueba del 002: gancho nuevo (tipografía de golpe + voz) y, pegado, el mismo cuerpo del inicio C
# desde «Trabajé catorce años…» (segundo 2,60), para que la prueba de gancho compare solo el gancho. Máximo 16 s.
# Antes: python marca/scripts/voz.py marca/produccion/002/ganchos h1 "…" h2 "…" h3 "…"  y  sh marca/efectos/preparar.sh <esta carpeta>
set -e
AQUI=$(cd "$(dirname "$0")" && pwd -W 2>/dev/null || pwd)
LIB=${LIB:-$HOME/lemo-opuscar}
C="$AQUI/../../../salidas/002-v4-inicio-C.mp4"
SAL="$AQUI/../../../salidas/ganchos-002"
mkdir -p "$SAL"
for h in ${@:-h1 h2 h3}; do
  (cd "$LIB" && node core/render/video.mjs "$AQUI" --q "h=$h" --fps 30 --workers 4 --size 1080x1920 --out "$SAL/$h-video.mp4")
  ffmpeg -v error -y -i "$SAL/$h-video.mp4" -i "$AQUI/$h.mp3" -ss 2.60 -i "$C" -filter_complex \
    "[0:v]scale=720:1280,setsar=1,fps=30[v0];[1:a]aresample=48000,apad=pad_dur=0.4[a0p];[a0p]atrim=0:$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SAL/$h-video.mp4")[a0];[2:v]scale=720:1280,setsar=1,fps=30[v1];[2:a]aresample=48000[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" \
    -map "[v]" -map "[a]" -t 16 -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$SAL/002-inicio-$h.mp4"
  echo "listo: $SAL/002-inicio-$h.mp4"
done
