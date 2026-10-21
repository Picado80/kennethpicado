"""Genera un video del gemelo de Kenneth (HeyGen API v3, Avatar IV) a partir de una pista de voz ya hecha.

Uso (desde la raíz de kennethpicado):
    python marca/scripts/gemelo.py <voz.mp3> <salida.mp4> [--titulo "marca G0"]

Usa el look y el motion prompt de marca/config/estudio.json. La llave (HEYGEN_API_KEY) se lee de torre\\.env y nunca se
imprime. Cobra por segundo (unos $0.08): imprime el saldo antes y después. Antes de correrlo, la pieza tiene que haber
pasado las 4 preguntas de marca/REVISION-PROCESO.md y la prueba de gancho.
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

MARCA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MARCA / "scripts"))
from voz import llave  # noqa: E402

API = "https://api.heygen.com/v3"


def pedir(url, k, data=None, cabeceras=None):
    h = {"x-api-key": k, **(cabeceras or {})}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h), timeout=180) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} en {url.split('?')[0]}: {e.read()[:400]!r}")


def saldo(k):
    d = json.loads(pedir(f"{API}/users/me", k))
    return (d.get("data") or d)["wallet"]["remaining_balance"]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("voz")
    ap.add_argument("salida")
    ap.add_argument("--titulo", default="marca")
    a = ap.parse_args()
    cfg = json.loads((MARCA / "config" / "estudio.json").read_text(encoding="utf-8"))["heygen"]
    k = llave("HEYGEN_API_KEY")
    s0 = saldo(k)
    print("saldo antes:", s0, flush=True)
    b = uuid.uuid4().hex
    cuerpo = (f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="voz.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode()
              + Path(a.voz).read_bytes() + f"\r\n--{b}--\r\n".encode())
    asset = json.loads(pedir(f"{API}/assets", k, cuerpo, {"Content-Type": f"multipart/form-data; boundary={b}"}))
    asset_id = (asset.get("data") or asset)["asset_id"]
    req = {"type": "avatar", "avatar_id": cfg["look_gemelo_video"], "audio_asset_id": asset_id, "aspect_ratio": "9:16",
           "resolution": "1080p", "title": a.titulo, "engine": {"type": "avatar_iv"}, "expressiveness": "medium",
           "motion_prompt": cfg["motion_prompt"]}
    try:
        v = json.loads(pedir(f"{API}/videos", k, json.dumps(req).encode(), {"Content-Type": "application/json"}))
    except SystemExit as e:
        # algunos looks del gemelo son «video avatars» y no aceptan motion_prompt ni expressiveness: se pide sin ellos
        if "motion_prompt" not in str(e) and "expressiveness" not in str(e):
            raise
        print("este look no acepta motion_prompt: se pide sin él", flush=True)
        for clave in ("motion_prompt", "expressiveness"):
            req.pop(clave, None)
        v = json.loads(pedir(f"{API}/videos", k, json.dumps(req).encode(), {"Content-Type": "application/json"}))
    vid = (v.get("data") or v)["video_id"]
    print("pedido:", vid, flush=True)
    while True:
        time.sleep(15)
        d = json.loads(pedir(f"{API}/videos/{vid}", k))
        d = d.get("data") or d
        if d.get("status") in ("completed", "success"):
            Path(a.salida).write_bytes(pedir(d["video_url"], k))
            print("listo:", a.salida, "duración", d.get("duration"), flush=True)
            break
        if d.get("status") in ("failed", "error"):
            raise SystemExit(f"falló: {d.get('failure_message') or d.get('error')}")
    s1 = saldo(k)
    print("saldo después:", s1, "| gasto:", round(s0 - s1, 4))


if __name__ == "__main__":
    main()
