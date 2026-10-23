"""Convierte una foto real en una ilustración anime con Gemini (edición de imagen), conservando el lugar.

Uso (desde la raíz de kennethpicado):
    python marca/scripts/anime.py <foto.jpg> <salida.jpg> "<qué agregar o cuidar>" [--con-letrero] [--modelo gemini-3-pro-image]
La foto de referencia tiene que ser de licencia libre (créditos en la carpeta). La llave (GEMINI_API_KEY) se lee de
torre\\.env y nunca se imprime. Sale en 9:16.
"""
import base64
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

MARCA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MARCA / "scripts"))
from voz import llave  # noqa: E402

BASE = ("Redraw this exact photo as a hand-painted Japanese anime film still (1990s cel animation look, soft watercolor "
        "background art, warm cinematic light, crisp line art). Keep the real place recognizable: the same buildings, street, "
        "landmarks, perspective and composition. Vertical 9:16 frame. ")
SIN_TEXTO = "No text, no logos, no watermarks. "


def main():
    args = sys.argv[1:]
    modelo, sin_texto = "gemini-3-pro-image", True
    if "--con-letrero" in args:            # deja el letrero real del lugar (p. ej. «Mercado Central · fundado en 1880»)
        args.remove("--con-letrero"); sin_texto = False
    if "--modelo" in args:
        i = args.index("--modelo"); modelo = args[i + 1]; del args[i:i + 2]
    foto, salida, extra = Path(args[0]), Path(args[1]), (args[2] if len(args) > 2 else "")
    k = llave("GEMINI_API_KEY")
    cuerpo = {"contents": [{"parts": [{"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(foto.read_bytes()).decode()}},
                                      {"text": BASE + (SIN_TEXTO if sin_texto else "") + extra}]}],
              "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "9:16"}}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
    req = urllib.request.Request(url, json.dumps(cuerpo).encode(), {"x-goog-api-key": k, "Content-Type": "application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read()[:500]!r}")
    for parte in r["candidates"][0]["content"]["parts"]:
        datos = parte.get("inline_data") or parte.get("inlineData")
        if datos:
            salida.parent.mkdir(parents=True, exist_ok=True)
            salida.write_bytes(base64.b64decode(datos["data"]))
            print("ok", salida, salida.stat().st_size // 1024, "KB")
            return
    sys.exit("sin imagen: " + json.dumps(r)[:400])


if __name__ == "__main__":
    main()
