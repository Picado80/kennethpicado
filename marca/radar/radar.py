"""Radar semanal de virales de TikTok para la marca personal (encargo E001).

Trae los videos de la ultima semana de las cuentas y hashtags de fuentes.json con
yt-dlp (gratis, sin llave), los ordena por porcentaje de compartidos y deja:
  - marca/semanas/AAAA-SNN-radar.md   (la tabla que se lee el lunes)
  - marca/radar/salidas/AAAA-SNN.json (los datos crudos; git los ignora)

Uso, desde la raiz de kennethpicado:
  python marca/radar/radar.py
  python marca/radar/radar.py --cookies-from-browser chrome   # si TikTok bloquea
  python marca/radar/radar.py --sin-transcripcion             # mas rapido

Codigos de salida: 0 bien, 1 fallaron todas las fuentes, 2 falta yt-dlp o fuentes.json.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MARCA = AQUI.parent
FUENTES = AQUI / "fuentes.json"
SALIDAS = AQUI / "salidas"
SEMANAS = MARCA / "semanas"


# ---------------------------------------------------------------- funciones puras

def semana_iso(fecha: datetime) -> str:
    anio, semana, _ = fecha.isocalendar()
    return f"{anio}-S{semana:02d}"


def normalizar(info: dict, fuente: str) -> dict:
    """Un video de yt-dlp (salida de -J) a nuestras columnas. Lo que falta va como None."""
    ts = info.get("timestamp")
    return {
        "url": info.get("webpage_url") or info.get("url"),
        "cuenta": info.get("uploader") or info.get("channel"),
        "fuente": fuente,
        "fecha": datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() if ts else None,
        "vistas": info.get("view_count"),
        "likes": info.get("like_count"),
        "comentarios": info.get("comment_count"),
        "compartidos": info.get("repost_count"),
        "guardados": info.get("save_count"),
        "duracion_s": info.get("duration"),
        "texto": (info.get("description") or "").strip(),
        "transcripcion": "",
    }


def filtrar(videos: list[dict], dias: int, min_vistas: int, ahora: datetime) -> list[dict]:
    """Ultimos `dias`, con al menos `min_vistas`, sin repetir url."""
    limite = ahora - timedelta(days=dias)
    vistos, salida = set(), []
    for v in videos:
        if not v.get("url") or v["url"] in vistos:
            continue
        if not v.get("fecha") or datetime.fromisoformat(v["fecha"]) < limite:
            continue
        if (v.get("vistas") or 0) < min_vistas:
            continue
        vistos.add(v["url"])
        salida.append(v)
    return salida


def pct(parte, total) -> float:
    return (parte or 0) / total if total else 0.0


def ordenar(videos: list[dict], top: int) -> list[dict]:
    """Por % de compartidos (un compartido es un acto de identidad), desempate por vistas."""
    return sorted(
        videos,
        key=lambda v: (pct(v.get("compartidos"), v.get("vistas")), v.get("vistas") or 0),
        reverse=True,
    )[:top]


def gancho(v: dict, palabras: int = 12) -> str:
    base = v.get("transcripcion") or v.get("texto") or ""
    base = re.sub(r"#\S+", "", base)  # los hashtags no son gancho
    trozos = base.split()
    corto = " ".join(trozos[:palabras])
    return (corto + (" ..." if len(trozos) > palabras else "")).replace("|", "/")


def texto_vtt(vtt: str) -> str:
    """Subtitulos WebVTT a texto corrido, sin tiempos ni lineas repetidas."""
    lineas = []
    for linea in vtt.splitlines():
        linea = linea.strip()
        if not linea or linea == "WEBVTT" or "-->" in linea or linea.isdigit():
            continue
        if linea.startswith(("NOTE", "STYLE", "Kind:", "Language:")):
            continue
        linea = re.sub(r"<[^>]+>", "", linea)
        if not lineas or lineas[-1] != linea:
            lineas.append(linea)
    return " ".join(lineas)


def elegir_subtitulo(info: dict) -> str | None:
    """URL del subtitulo en espanol, si yt-dlp lo encontro."""
    subs = info.get("subtitles") or {}
    for idioma in sorted(subs, key=lambda k: (not k.startswith("es"), k)):
        if not idioma.startswith("es"):
            break
        for s in subs[idioma]:
            if s.get("url") and s.get("ext", "vtt") in ("vtt", "webvtt"):
                return s["url"]
    return None


def render_md(semana: str, videos: list[dict], fallas: list[str], fuentes: dict) -> str:
    l = [
        f"# Radar {semana}",
        "",
        f"Fuentes: {len(fuentes.get('cuentas', []))} cuentas, {len(fuentes.get('hashtags', []))} hashtags, "
        f"{len(fuentes.get('urls', []))} URLs sueltas · últimos {fuentes.get('dias', 7)} días · "
        f"mínimo {fuentes.get('min_vistas', 0):,} vistas".replace(",", "."),
        "",
        "Ordenado por % de compartidos. Para cada uno: las 7 preguntas del playbook antes de copiar nada.",
        "",
        "| # | Cuenta | Vistas | % compartidos | % guardados | Duración | Gancho | Video |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for i, v in enumerate(videos, 1):
        vistas = v.get("vistas") or 0
        dur = f"{v['duracion_s']} s" if v.get("duracion_s") else "—"
        guard = f"{pct(v.get('guardados'), vistas):.1%}" if v.get("guardados") is not None else "—"
        l.append(
            f"| {i} | @{v.get('cuenta') or '?'} | {vistas:,} | {pct(v.get('compartidos'), vistas):.1%} | {guard} "
            f"| {dur} | {gancho(v)} | [ver]({v['url']}) |".replace(",", ".")
        )
    if not videos:
        l.append("| — | Nada pasó los filtros esta semana | | | | | | |")
    if fallas:
        l += ["", "## Fuentes que fallaron", ""] + [f"- {f}" for f in fallas]
    return "\n".join(l) + "\n"


# ---------------------------------------------------------------- yt-dlp

def comando_ytdlp() -> list[str] | None:
    if importlib.util.find_spec("yt_dlp"):
        return [sys.executable, "-m", "yt_dlp"]
    exe = shutil.which("yt-dlp")
    return [exe] if exe else None


def correr_ytdlp(base: list[str], url: str, por_fuente: int, cookies: str | None) -> list[dict]:
    """Metadatos (sin descargar video) de una cuenta, hashtag o video. Lanza RuntimeError si falla."""
    cmd = base + ["-J", "--skip-download", "--no-warnings", "--ignore-errors",
                  "--playlist-end", str(por_fuente), url]
    if cookies:
        cmd[len(base):len(base)] = ["--cookies-from-browser", cookies]
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=600, env=env)
    ultima = (r.stderr.strip().splitlines() or ["sin detalle"])[-1][:200]
    try:
        datos = json.loads(r.stdout) if r.stdout.strip() else None
    except json.JSONDecodeError:
        datos = None
    # Con --ignore-errors, yt-dlp imprime "null" cuando no pudo leer nada
    if not isinstance(datos, dict):
        raise RuntimeError(ultima)
    entradas = datos.get("entries") if "entries" in datos else [datos]
    return [e for e in (entradas or []) if e]


def bajar_transcripcion(info: dict) -> str:
    url = elegir_subtitulo(info)
    if not url:
        return ""
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return texto_vtt(r.read().decode("utf-8", "replace"))
    except Exception:
        return ""


def url_de(fuente: str, valor: str) -> str:
    if fuente == "cuenta":
        return f"https://www.tiktok.com/@{valor.lstrip('@')}"
    if fuente == "hashtag":
        return f"https://www.tiktok.com/tag/{valor.lstrip('#')}"
    return valor


# ---------------------------------------------------------------- principal

def main(argv: list[str] | None = None, runner=correr_ytdlp, transcriptor=bajar_transcripcion,
         ahora: datetime | None = None) -> int:
    p = argparse.ArgumentParser(description="Radar semanal de virales de TikTok")
    p.add_argument("--fuentes", type=Path, default=FUENTES)
    p.add_argument("--cookies-from-browser", dest="cookies", default=None,
                   help="chrome, edge o firefox, si TikTok bloquea sin sesion")
    p.add_argument("--sin-transcripcion", action="store_true")
    p.add_argument("--semanas-dir", type=Path, default=SEMANAS)
    p.add_argument("--salidas-dir", type=Path, default=SALIDAS)
    a = p.parse_args(argv)

    if not a.fuentes.exists():
        print(f"No encuentro {a.fuentes}.", file=sys.stderr)
        return 2
    fuentes = json.loads(a.fuentes.read_text(encoding="utf-8"))

    base = comando_ytdlp() if runner is correr_ytdlp else ["yt-dlp"]
    if base is None:
        print("Falta yt-dlp. Instalalo con:  python -m pip install -U yt-dlp", file=sys.stderr)
        return 2

    ahora = ahora or datetime.now(timezone.utc)
    pedidos = ([("cuenta", c) for c in fuentes.get("cuentas", [])]
               + [("hashtag", h) for h in fuentes.get("hashtags", [])]
               + [("url", u) for u in fuentes.get("urls", [])])
    if not pedidos:
        print("fuentes.json no tiene cuentas, hashtags ni urls.", file=sys.stderr)
        return 2

    crudos, fallas, normales = [], [], []
    for tipo, valor in pedidos:
        etiqueta = f"{tipo} {valor}"
        try:
            infos = runner(base, url_de(tipo, valor), int(fuentes.get("por_fuente", 30)), a.cookies)
        except Exception as e:  # una fuente que falla no detiene las demas
            fallas.append(f"{etiqueta}: {e}")
            print(f"  FALLA  {etiqueta}: {e}")
            continue
        print(f"  ok     {etiqueta}: {len(infos)} videos")
        for info in infos:
            crudos.append(info)
            normales.append((normalizar(info, etiqueta), info))

    elegidos = ordenar(filtrar([n for n, _ in normales], int(fuentes.get("dias", 7)),
                               int(fuentes.get("min_vistas", 0)), ahora), int(fuentes.get("top", 15)))
    if not a.sin_transcripcion:
        por_url = {n["url"]: info for n, info in normales}
        for v in elegidos:
            v["transcripcion"] = transcriptor(por_url.get(v["url"], {}))

    semana = semana_iso(ahora.astimezone())
    a.semanas_dir.mkdir(parents=True, exist_ok=True)
    a.salidas_dir.mkdir(parents=True, exist_ok=True)
    md = a.semanas_dir / f"{semana}-radar.md"
    md.write_text(render_md(semana, elegidos, fallas, fuentes), encoding="utf-8")
    (a.salidas_dir / f"{semana}.json").write_text(
        json.dumps({"semana": semana, "elegidos": elegidos, "fallas": fallas, "crudos": crudos},
                   ensure_ascii=False, indent=1, default=str), encoding="utf-8")

    print(f"\n{len(elegidos)} videos en {md}")
    return 1 if len(fallas) == len(pedidos) else 0


if __name__ == "__main__":
    sys.exit(main())
