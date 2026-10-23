"""Anima una imagen con MiniMax (Hailuo, imagen a video) y baja el clip.

Uso (desde la raíz de kennethpicado):
    python marca/scripts/video_minimax.py <imagen.jpg> <salida.mp4> "<qué se mueve y cómo se mueve la cámara>" [--modelo MiniMax-Hailuo-02] [--seg 6]
Usa solo la llave del plan (~/.minimax_key), nunca la de pago por uso. La llave nunca se imprime.
"""
import base64
import json
import sys
import time
import urllib.request
from pathlib import Path

API = "https://api.minimax.io/v1"


def pedir(k, url, cuerpo=None):
    h = {"Authorization": "Bearer " + k}
    if cuerpo is not None:
        h["Content-Type"] = "application/json"
    return json.load(urllib.request.urlopen(urllib.request.Request(url, json.dumps(cuerpo).encode() if cuerpo is not None else None, h), timeout=120))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    modelo, seg = "MiniMax-Hailuo-02", 6
    for op in ("--modelo", "--seg"):
        if op in args:
            i = args.index(op); v = args[i + 1]; del args[i:i + 2]
            modelo, seg = (v, seg) if op == "--modelo" else (modelo, int(v))
    img, salida, prompt = Path(args[0]), Path(args[1]), args[2]
    k = (Path.home() / ".minimax_key").read_text(encoding="utf-8").strip()
    b64 = "data:image/jpeg;base64," + base64.b64encode(img.read_bytes()).decode()
    r = pedir(k, f"{API}/video_generation", {"model": modelo, "prompt": prompt, "first_frame_image": b64, "duration": seg, "resolution": "768P"})
    estado = r.get("base_resp", {})
    if estado.get("status_code") not in (0, None) or not r.get("task_id"):
        sys.exit(f"no se pudo pedir: {estado}")
    tarea = r["task_id"]; print("tarea", tarea, flush=True)
    for _ in range(120):                                   # hasta 20 minutos
        time.sleep(10)
        q = pedir(k, f"{API}/query/video_generation?task_id={tarea}")
        if q.get("status") == "Success":
            f = pedir(k, f"{API}/files/retrieve?file_id={q['file_id']}")["file"]
            salida.parent.mkdir(parents=True, exist_ok=True)
            salida.write_bytes(urllib.request.urlopen(f["download_url"], timeout=300).read())
            print("ok", salida, salida.stat().st_size // 1024, "KB"); return
        if q.get("status") == "Fail":
            sys.exit(f"falló: {q}")
    sys.exit("se pasó de 20 minutos")


if __name__ == "__main__":
    main()
