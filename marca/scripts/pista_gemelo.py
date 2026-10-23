"""Arma la pista de voz del gemelo con las frases que dice a cámara y anota dónde empieza cada una.

Uso (desde la raíz de kennethpicado):
    python marca/scripts/pista_gemelo.py <carpeta de la pieza> a d e [--hueco 0.4]
Junta <carpeta>/voz/<id>.mp3 en orden, con <hueco> segundos de silencio entre una y otra (y al final), y escribe
<carpeta>/gemelo-voz.mp3 y <carpeta>/gemelo.json ({"offsets": {id: segundo}, "dur": {id: segundos}, "total"}).
Después: marca/scripts/gemelo.py <carpeta>/gemelo-voz.mp3 <carpeta>/gemelo.mp4 y los cuadros con ffmpeg (30 por
segundo) en <carpeta>/gemelo/. La escena muestra el gemelo solo mientras habla: cobra por segundo.
"""
import json
import subprocess
import sys
from pathlib import Path


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout)


def main():
    args = sys.argv[1:]
    hueco = 0.4
    if "--hueco" in args:
        i = args.index("--hueco"); hueco = float(args[i + 1]); del args[i:i + 2]
    carpeta, ids = Path(args[0]), args[1:]
    entradas, filtros, offsets, durs, t = [], [], {}, {}, 0.0
    for k, i in enumerate(ids):
        p = carpeta / "voz" / f"{i}.mp3"
        d = dur(p); offsets[i] = round(t, 3); durs[i] = round(d, 3); t += d + hueco
        entradas += ["-i", str(p), "-f", "lavfi", "-t", str(hueco), "-i", "anullsrc=r=44100:cl=mono"]
        filtros += [f"[{2 * k}:a]aresample=44100,aformat=channel_layouts=mono[v{k}]", f"[v{k}][{2 * k + 1}:a]"]
    n = len(ids)
    grafo = ";".join(f for f in filtros if f.startswith("[") and "aresample" in f) + ";" + \
        "".join(f for f in filtros if "aresample" not in f) + f"concat=n={2 * n}:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *entradas, "-filter_complex", grafo, "-map", "[o]", "-c:a", "libmp3lame",
                    "-b:a", "192k", str(carpeta / "gemelo-voz.mp3")], check=True)
    info = {"offsets": offsets, "dur": durs, "total": round(t, 3)}
    (carpeta / "gemelo.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    print(info)


if __name__ == "__main__":
    main()
