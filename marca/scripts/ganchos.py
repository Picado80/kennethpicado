"""La máquina de ganchos, paso 1: junta los primeros segundos de los videos que mejor funcionan en cuentas del tema.

Uso (desde la raíz de kennethpicado):
    python marca/scripts/ganchos.py                       # las cuentas de marca/radar/fuentes.json
    python marca/scripts/ganchos.py --cuentas dotcsv javadex --top 10 --por-cuenta 40

Por cada cuenta trae los últimos videos con yt-dlp (gratis, sin llave), se queda con los más vistos y saca lo que se
dice en los primeros segundos de los subtítulos automáticos de TikTok, con su tiempo. Deja el banco en
marca/salidas/ganchos-AAAA-MM-DD.json y .md: queda fuera del repo porque son textos de otros. Lo que se publica en
el repo son los patrones y las variaciones propias (marca/ganchos/). No llama a ninguna API paga.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

MARCA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MARCA / "radar"))
import radar  # noqa: E402  (reusa yt-dlp y la elección de subtítulos del radar)

SALIDAS = MARCA / "salidas"
SEGUNDOS = 4.0     # lo que se dice antes de esto es el gancho
AUDIO_S = 7        # cuando no hay subtítulos, se transcriben estos primeros segundos


def a_segundos(marca: str) -> float:
    partes = marca.replace(",", ".").split(":")
    s = 0.0
    for p in partes:
        s = s * 60 + float(p)
    return s


def cues_vtt(vtt: str) -> list[tuple[float, float, str]]:
    """Subtítulos WebVTT a (inicio, fin, texto), sin repetir líneas."""
    cues, ini, fin, texto = [], None, None, []
    for linea in vtt.splitlines() + [""]:
        linea = linea.strip()
        m = re.match(r"([\d:.,]+)\s*-->\s*([\d:.,]+)", linea)
        if m:
            ini, fin, texto = a_segundos(m.group(1)), a_segundos(m.group(2)), []
        elif linea and ini is not None:
            texto.append(re.sub(r"<[^>]+>", "", linea))
        elif not linea and ini is not None:
            t = " ".join(texto).strip()
            if t and (not cues or cues[-1][2] != t):
                cues.append((ini, fin, t))
            ini = None
    return cues


def gancho_de(cues: list[tuple[float, float, str]], hasta: float = SEGUNDOS) -> str:
    frase = " ".join(t for i, _, t in cues if i < hasta)
    return re.sub(r"\s+", " ", frase).strip()


def bajar_vtt(info: dict) -> str:
    url = radar.elegir_subtitulo(info)
    if not url:
        return ""
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return r.read().decode("utf-8", "replace")
    except Exception:
        return ""


def oir_inicio(base: list[str], url: str) -> list[tuple[float, float, str]]:
    """Baja solo los primeros segundos de audio y los transcribe con ElevenLabs (scribe). Devuelve cues por palabra."""
    sys.path.insert(0, str(MARCA / "scripts"))
    from voz import llave, pedir  # la llave se lee de torre\.env y nunca se imprime
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run(base + ["-q", "--no-warnings", "-f", "ba/b", "--download-sections", f"*0-{AUDIO_S}",
                                   "-x", "--audio-format", "mp3", "-o", f"{d}/a.%(ext)s", url],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
        mp3 = Path(d) / "a.mp3"
        if r.returncode or not mp3.exists():
            return []
        b = uuid.uuid4().hex
        campo = lambda n, v: f'--{b}\r\nContent-Disposition: form-data; name="{n}"\r\n\r\n{v}\r\n'.encode()
        cuerpo = (campo("model_id", "scribe_v1") + campo("timestamps_granularity", "word")
                  + f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode()
                  + mp3.read_bytes() + f"\r\n--{b}--\r\n".encode())
        res = json.loads(pedir("https://api.elevenlabs.io/v1/speech-to-text", cuerpo,
                               {"xi-api-key": llave("ELEVENLABS_MARCA_API_KEY"), "Content-Type": f"multipart/form-data; boundary={b}"}))
    return [(w["start"], w["end"], w["text"]) for w in res.get("words", []) if w.get("type") == "word"]


def fila(info: dict, cuenta: str) -> dict:
    vtt = bajar_vtt(info)
    cues = cues_vtt(vtt)
    vistas = info.get("view_count") or 0
    comp = info.get("repost_count") or 0
    return {
        "cuenta": cuenta,
        "url": info.get("webpage_url"),
        "vistas": vistas,
        "me_gusta": info.get("like_count") or 0,
        "comentarios": info.get("comment_count") or 0,
        "compartidos": comp,
        "compartidos_por_mil": round(1000 * comp / vistas, 2) if vistas else 0,
        "duracion": info.get("duration"),
        "gancho": gancho_de(cues),
        "primeros_8s": gancho_de(cues, 8.0),
        "descripcion": re.sub(r"#\S+", "", info.get("description") or info.get("title") or "").strip()[:200],
    }


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    fuentes = json.loads((MARCA / "radar" / "fuentes.json").read_text(encoding="utf-8"))
    ap = argparse.ArgumentParser()
    ap.add_argument("--cuentas", nargs="*", default=fuentes.get("cuentas", []))
    ap.add_argument("--por-cuenta", type=int, default=40)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--cookies-from-browser")
    ap.add_argument("--audio", type=int, default=0,
                    help="a los N videos más vistos sin subtítulos se les transcribe el inicio (ElevenLabs, unos segundos cada uno)")
    a = ap.parse_args()

    base = radar.comando_ytdlp()
    if not base:
        print("Falta yt-dlp.")
        return 2

    def una(cuenta: str):
        try:
            videos = radar.correr_ytdlp(base, radar.url_de("cuenta", cuenta), a.por_cuenta, a.cookies_from_browser)
        except RuntimeError as e:
            return cuenta, [], str(e)
        mejores = sorted(videos, key=lambda v: v.get("view_count") or 0, reverse=True)[: a.top]
        return cuenta, [fila(v, cuenta) for v in mejores], None

    banco, fallas = [], []
    with ThreadPoolExecutor(max_workers=4) as ex:
        for cuenta, filas, error in ex.map(una, a.cuentas):
            if error:
                fallas.append(f"{cuenta}: {error}")
            banco += filas
            print(f"{cuenta}: {len(filas)} videos" + (f" (falló: {error})" if error else ""))

    sin = sorted([f for f in banco if not f["gancho"]], key=lambda x: x["vistas"], reverse=True)[: a.audio]
    for f in sin:
        cues = oir_inicio(base, f["url"])
        f["gancho"], f["primeros_8s"], f["origen"] = gancho_de(cues), gancho_de(cues, 8.0), "audio"
        print(f"oído: {f['cuenta']} {f['vistas']:,} · {f['gancho'][:70]}")

    hoy = date.today().isoformat()
    SALIDAS.mkdir(exist_ok=True)
    (SALIDAS / f"ganchos-{hoy}.json").write_text(json.dumps(banco, ensure_ascii=False, indent=1), encoding="utf-8")
    md = [f"# Banco de ganchos · {hoy}", "", "Los más vistos de cada cuenta; «gancho» es lo que se dice en los primeros "
          f"{SEGUNDOS:.0f} s según los subtítulos de TikTok.", "",
          "| Cuenta | Vistas | Compartidos por mil | Gancho | Video |", "|---|---|---|---|---|"]
    for f in sorted(banco, key=lambda x: x["vistas"], reverse=True):
        g = (f["gancho"] or f"(sin subtítulos) {f['descripcion'][:80]}").replace("|", "/")
        md.append(f"| {f['cuenta']} | {f['vistas']:,} | {f['compartidos_por_mil']} | {g} | {f['url']} |")
    if fallas:
        md += ["", "**Fallaron:** " + "; ".join(fallas)]
    (SALIDAS / f"ganchos-{hoy}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{len(banco)} ganchos -> {SALIDAS / f'ganchos-{hoy}.md'}")
    return 0 if banco else 1


if __name__ == "__main__":
    sys.exit(main())
