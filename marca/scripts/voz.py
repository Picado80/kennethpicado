"""Voz clonada de Kenneth (ElevenLabs) con los tiempos de cada palabra.

Uso (desde la raíz de kennethpicado):
    python marca/scripts/voz.py marca/produccion/j1/voz a "Texto que dice la voz." [b "Otro tramo." ...]

Por cada tramo escribe <carpeta>/<id>.mp3 (no va a git) y deja en <carpeta>/palabras.json los tiempos de cada
palabra, en segundos desde el inicio de ese tramo: {"a": [["Prompt", 0.12, 0.61], ...], "b": [...]}.
La voz y el modelo salen de marca/config/estudio.json. La llave se lee de C:\\Users\\Picado\\torre\\.env y nunca se imprime.
"""
import json
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ENV = Path(r"C:\Users\Picado\torre\.env")
API = "https://api.elevenlabs.io/v1"


def llave(nombre):
    for linea in ENV.read_text(encoding="utf-8").splitlines():
        t = linea.strip()
        if t and not t.startswith("#") and "=" in t:
            k, v = t.split("=", 1)
            if k.strip() == nombre:
                return v.strip().strip('"').strip("'")
    raise SystemExit("falta " + nombre + " en torre\\.env")


def pedir(url, cuerpo, cabeceras):
    try:
        return urllib.request.urlopen(urllib.request.Request(url, cuerpo, cabeceras), timeout=180).read()
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read()[:300]!r}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 4 or len(sys.argv) % 2:
        raise SystemExit(__doc__)
    carpeta = Path(sys.argv[1])
    carpeta.mkdir(parents=True, exist_ok=True)
    tramos = list(zip(sys.argv[2::2], sys.argv[3::2]))
    estudio = json.loads((RAIZ / "marca/config/estudio.json").read_text(encoding="utf-8"))["elevenlabs"]
    voz, modelo = estudio["voz_kenneth"], estudio.get("modelo", "eleven_v4")
    el = llave("ELEVENLABS_MARCA_API_KEY")
    ruta = carpeta / "palabras.json"
    palabras = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}
    for ident, texto in tramos:
        mp3 = pedir(f"{API}/text-to-speech/{voz}?output_format=mp3_44100_128",
                    json.dumps({"text": texto, "model_id": modelo}).encode("utf-8"),
                    {"xi-api-key": el, "Content-Type": "application/json", "Accept": "audio/mpeg"})
        (carpeta / f"{ident}.mp3").write_bytes(mp3)
        b = uuid.uuid4().hex
        campo = lambda n, v: f'--{b}\r\nContent-Disposition: form-data; name="{n}"\r\n\r\n{v}\r\n'.encode()
        cuerpo = (campo("model_id", "scribe_v1") + campo("language_code", "spa") + campo("timestamps_granularity", "word")
                  + f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="{ident}.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode()
                  + mp3 + f"\r\n--{b}--\r\n".encode())
        d = json.loads(pedir(f"{API}/speech-to-text", cuerpo, {"xi-api-key": el, "Content-Type": f"multipart/form-data; boundary={b}"}))
        ws = [[w["text"], round(w["start"], 3), round(w["end"], 3)] for w in d.get("words", []) if w.get("type") == "word"]
        palabras[ident] = ws
        print(f"{ident}: {len(texto)} caracteres, {len(ws)} palabras, {ws[-1][2] if ws else 0} s")
        print("   " + " ".join(f"{w[0]}@{w[1]}" for w in ws))
    ruta.write_text(json.dumps(palabras, ensure_ascii=False, indent=0), encoding="utf-8")


if __name__ == "__main__":
    main()
