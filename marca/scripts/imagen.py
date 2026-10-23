"""Genera imágenes con MiniMax (image-01) para el B-roll y las series de la marca.

Uso (desde la raíz de kennethpicado):
    python marca/scripts/imagen.py <carpeta> <nombre> "<prompt>" [<nombre> "<prompt>" ...] [--formato 9:16]
Guarda <carpeta>/<nombre>.jpg y anota el prompt en <carpeta>/imagenes.json; lo que ya existe no se vuelve a pedir.
Usa la llave del plan (~/.minimax_key), que nunca se imprime.
"""
import json
import sys
import urllib.request
from pathlib import Path

API = "https://api.minimax.io/v1/image_generation"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    formato = "9:16"
    if "--formato" in args:
        i = args.index("--formato"); formato = args[i + 1]; del args[i:i + 2]
    if len(args) < 3 or len(args) % 2 == 0:
        sys.exit(__doc__)
    carpeta = Path(args[0]); carpeta.mkdir(parents=True, exist_ok=True)
    registro = carpeta / "imagenes.json"
    hechas = json.loads(registro.read_text(encoding="utf-8")) if registro.exists() else {}
    k = (Path.home() / ".minimax_key").read_text(encoding="utf-8").strip()
    for nombre, prompt in zip(args[1::2], args[2::2]):
        destino = carpeta / f"{nombre}.jpg"
        if destino.exists():
            continue
        cuerpo = {"model": "image-01", "prompt": prompt, "aspect_ratio": formato, "response_format": "url", "n": 1, "prompt_optimizer": False}
        req = urllib.request.Request(API, json.dumps(cuerpo).encode(), {"Authorization": "Bearer " + k, "Content-Type": "application/json"})
        r = json.load(urllib.request.urlopen(req, timeout=300))
        estado = r.get("base_resp", {})
        if estado.get("status_code") not in (0, None):
            print(nombre, "falló:", estado); continue
        url = r["data"]["image_urls"][0]
        destino.write_bytes(urllib.request.urlopen(url, timeout=120).read())
        hechas[nombre] = {"prompt": prompt, "formato": formato}
        registro.write_text(json.dumps(hechas, ensure_ascii=False, indent=2), encoding="utf-8")
        print(nombre, "ok", destino.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
