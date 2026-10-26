"""Radar diario multi-red de la marca personal de Kenneth Picado.

Barre TikTok, Instagram, X y YouTube en DOS PASADAS y deja un digest de una pantalla:

  - marca/radar/salidas/AAAA-MM-DD.json  (lo crudo; git lo ignora)
  - marca/radar/hoy.md                   (el digest que Kenneth lee en 3 minutos)

Pasada 1 (barata): una llamada al runner por cuenta; se juntan los videos, se deduplica
por url y se quedan los recientes con vistas suficientes.
Pasada 2 (cara): se ordenan por la metrica "senal" y a los mejores se les baja la
transcripcion y tres cuadros del video (solo TikTok y YouTube: Instagram y X bloquean
la descarga, se anotan y se siguen).

La captura de cada red vive en redes.py (otra pieza); aca se inyecta con `runner` para
poder probar sin red.

Uso, desde la raiz de kennethpicado:
  python marca/radar/diario.py
  python marca/radar/diario.py --red tiktok,youtube
  python marca/radar/diario.py --top 8
  python marca/radar/diario.py --sin-cuadros
  python marca/radar/diario.py --cookies edge
  python marca/radar/diario.py --dry-run

Codigos de salida: 0 bien, 1 fallaron todas las fuentes, 2 falta yt-dlp o fuentes.json.
"""
from __future__ import annotations

import argparse
import functools
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

AQUI = Path(__file__).resolve().parent
MARCA = AQUI.parent
RAIZ = MARCA.parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

import radar  # noqa: E402  (funciones puras ya probadas: no se reimplementan)

FUENTES = AQUI / "fuentes.json"
SALIDAS = AQUI / "salidas"
HOY = AQUI / "hoy.md"

# Instagram y X no dejan descargar el video: no se intenta, se anota y se sigue.
REDES_CON_VIDEO = ("tiktok", "youtube")

# Redes sin ruta de yt-dlp: ni se les busca transcripcion ni se les baja video.
REDES_SIN_YTDLP = ("instagram", "x")

# Como se escriben las redes en el digest (no "Tiktok" ni "Youtube").
NOMBRES_RED = {"tiktok": "TikTok", "instagram": "Instagram", "x": "X", "youtube": "YouTube"}

Runner = Callable[..., list[dict]]


# ------------------------------------------------------------------ funciones puras

def numero_cr(valor) -> str:
    """412000 -> '412.000' (punto de miles, como se escribe en Costa Rica)."""
    if valor is None:
        return "—"
    try:
        return f"{int(valor):,}".replace(",", ".")
    except (TypeError, ValueError):
        return str(valor)


def decimal_cr(valor, decimales: int = 1) -> str:
    """0.081 -> '0,081' (coma decimal)."""
    if valor is None:
        return "—"
    try:
        return f"{float(valor):.{decimales}f}".replace(".", ",")
    except (TypeError, ValueError):
        return str(valor)


def porcentaje_cr(parte, total) -> str:
    """% de compartidos en formato costarricense: '8,1%'."""
    return f"{radar.pct(parte, total) * 100:.1f}%".replace(".", ",")


def duracion_texto(video: dict) -> str:
    """12 -> '12 s' (o '—' si el video no trae duracion)."""
    dur = video.get("duracion_s")
    if isinstance(dur, bool) or not isinstance(dur, (int, float)):
        return "—"
    if float(dur).is_integer():
        return f"{int(dur)} s"
    return f"{dur} s"


def senal_texto(video: dict) -> str:
    """La metrica "senal" de redes.py, tal cual (sin inventarle unidades)."""
    valor = video.get("señal")
    if valor is None:
        return "—"
    if isinstance(valor, bool):
        return str(valor)
    if isinstance(valor, int):
        return numero_cr(valor)
    if isinstance(valor, float):
        return f"{valor:.3f}".rstrip("0").rstrip(".").replace(".", ",")
    return str(valor)


def valor_senal(video: dict) -> float:
    """La metrica "senal" como numero, para ordenar (0 si no viene)."""
    try:
        return float(video.get("señal"))
    except (TypeError, ValueError):
        return 0.0


def _interacciones(video: dict) -> int:
    """Las interacciones sumadas: likes + comentarios + compartidos.

    X no publica vistas en su HTML publico, asi que su senal queda en 0 y sus
    posts se hundirían al final del ranking. Con esta segunda llave, un post de X
    con 3.000 reacciones compite con uno de TikTok que tiene 3% de compartidos.
    """
    total = 0
    for campo in ("likes", "comentarios", "compartidos"):
        valor = video.get(campo)
        if isinstance(valor, (int, float)) and not isinstance(valor, bool):
            total += int(valor)
    return total


def _dura(video: dict) -> float | None:
    """La duracion del video en segundos. None si no se sabe.

    Si no se sabe, el video NO se filtra: en Instagram y X la duracion no se lee
    del DOM, y descartar a ciegas seria peor que dejar pasar de mas.
    """
    d = video.get("duracion_s")
    if isinstance(d, bool) or not isinstance(d, (int, float)):
        return None
    return float(d)


def _slug(texto: str) -> str:
    """Un nombre de archivo seguro a partir del url."""
    limpio = re.sub(r"[^0-9A-Za-z]+", "-", texto or "").strip("-")
    return (limpio[:40] or "video").lower()


def _nombre_red(red: str) -> str:
    """'tiktok' -> 'TikTok' (para el digest)."""
    return NOMBRES_RED.get((red or "").lower(), (red or "?").capitalize())


def _imprimir(texto: str, err: bool = False) -> None:
    """Imprime aunque la consola no sepa de acentos (cp1252 en Windows)."""
    flujo = sys.stderr if err else sys.stdout
    codigo = getattr(flujo, "encoding", None) or "utf-8"
    try:
        print(texto, file=flujo)
    except UnicodeEncodeError:
        print(texto.encode(codigo, "replace").decode(codigo, "replace"), file=flujo)


def _ruta_relativa(path: Path) -> str:
    """Ruta desde la raiz del repo, para que el JSON crudo sea portable."""
    try:
        return str(path.resolve().relative_to(RAIZ))
    except ValueError:
        return str(path)


# ------------------------------------------------------------------ E/S (red y disco)

def _ahora_utc(ahora: datetime | None) -> datetime:
    """Si no viene hora, la de ahora en UTC; si viene naive, se asume UTC."""
    if ahora is None:
        return datetime.now(timezone.utc)
    return ahora if ahora.tzinfo else ahora.replace(tzinfo=timezone.utc)


def _fecha_iso_aware(video: dict) -> None:
    """Deja la fecha con zona horaria (asi se puede comparar con `ahora`)."""
    fecha = video.get("fecha")
    if not fecha:
        return
    if isinstance(fecha, (int, float)) and not isinstance(fecha, bool):
        video["fecha"] = datetime.fromtimestamp(fecha, tz=timezone.utc).isoformat()
        return
    try:
        momento = datetime.fromisoformat(str(fecha))
    except ValueError:
        return
    if momento.tzinfo is None:
        video["fecha"] = momento.replace(tzinfo=timezone.utc).isoformat()


def _disponibles() -> dict[str, bool]:
    """Que redes se pueden capturar hoy. Si redes.py no esta, se asumen todas."""
    try:
        import redes  # noqa: F401  (lo escribe la otra pieza del radar)
    except Exception:
        return {}
    try:
        return dict(redes.disponibles() or {})
    except Exception:
        return {}


def _runner_por_defecto(red: str, usuario: str, n: int = 30,
                        cookies: str | None = None) -> list[dict]:
    """Puente a redes.obtener (la otra pieza del radar)."""
    import redes

    return redes.obtener(red, usuario, n=n, cookies=cookies)


def _info_video(url: str, cookies: str | None = None) -> dict | None:
    """Metadatos de un video (yt-dlp, sin descargar). None si no se pudo leer."""
    if not url:
        return None
    base = radar.comando_ytdlp()
    if base is None:
        return None
    try:
        infos = radar.correr_ytdlp(base, url, 1, cookies)
    except Exception:
        return None
    for info in infos:
        if isinstance(info, dict) and info:
            return info
    return None


def _descargar_video(url: str, destino: Path, cookies: str | None) -> Path:
    """Baja el video a `destino` con yt-dlp y devuelve el archivo."""
    base = radar.comando_ytdlp()
    if base is None:
        raise RuntimeError("falta yt-dlp")
    cmd = base + ["--no-warnings", "--no-playlist",
                  # TikTok solo ofrece formatos verticales (576x1024, 720x1280) y sin
                  # separar el audio: por eso el corte tiene que ser por ancho, no por
                  # alto, o no encuentra nada. Verificado el 26-oct-2026.
                  "-f", "b[height<=720]/b[width<=720]/b",
                  "--merge-output-format", "mp4",
                  "-o", str(destino / "video.%(ext)s"), url]
    if cookies:
        cmd[len(base):len(base)] = ["--cookies-from-browser", cookies]
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=900, env=env)
    archivos = [p for p in sorted(destino.glob("video.*"))
                if not p.name.endswith((".part", ".ytdl"))]
    if not archivos:
        detalle = (r.stderr.strip().splitlines() or ["sin detalle"])[-1][:200]
        raise RuntimeError(f"no se pudo bajar el video: {detalle}")
    return archivos[0]


def _extraer_cuadros(video: dict, cookies: str | None = None,
                     info: dict | None = None) -> list[str]:
    """Baja el video (TikTok/YouTube) y saca tres cuadros con ffmpeg."""
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("falta ffmpeg")
    url = video.get("url")
    if not url:
        return []
    duracion = (info or {}).get("duration") or video.get("duracion_s") or 0
    destino = SALIDAS / "cuadros" / _fecha_de(video)
    destino.mkdir(parents=True, exist_ok=True)
    rutas: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        archivo = _descargar_video(url, Path(tmp), cookies)
        for i, fraccion in enumerate((0.10, 0.50, 0.90), start=1):
            segundo = max(0.0, float(duracion) * fraccion)
            salida = destino / f"{i:02d}-{video.get('red') or 'video'}-{_slug(url)}.jpg"
            cmd = [ffmpeg, "-y", "-loglevel", "error", "-ss", f"{segundo:.2f}",
                   "-i", str(archivo), "-frames:v", "1", "-q:v", "3", str(salida)]
            subprocess.run(cmd, capture_output=True, timeout=180)
            if salida.exists():
                rutas.append(_ruta_relativa(salida))
    return rutas


def _fecha_de(video: dict) -> str:
    """Fecha (YYYY-MM-DD) de un video, para carpetas y nombres."""
    fecha = video.get("fecha")
    if not fecha:
        return "sin-fecha"
    try:
        return datetime.fromisoformat(str(fecha)).date().isoformat()
    except ValueError:
        return "sin-fecha"


# ------------------------------------------------------------------ el runner

def barrer(fuentes: dict, redes: list[str] | None = None, ahora: datetime | None = None,
           runner: Runner | None = None, top: int = 5, por_red: int = 30,
           cookies: str | None = None, cuadros: bool = True) -> dict:
    """Barre las redes pedidas en dos pasadas y devuelve el resultado crudo.

    Pasada 1 (barata): una llamada al runner por cuenta; se juntan los videos, se
    deduplica por url y se quedan los recientes con al menos `min_vistas` de su red.
    Pasada 2 (cara): se ordenan por la metrica "senal" (desempate por vistas) y a los
    mejores se les baja la transcripcion y tres cuadros del video.

    - runner: se inyecta para probar sin red; por defecto es redes.obtener.
    - cookies: navegador del que yt-dlp saca cookies (chrome, edge, firefox).
    - cuadros: False = no se baja video (mas rapido).

    Devuelve: fecha, redes, vistos, candidatos, fallas, omitidas.
    "vistos" son los videos distintos por url que trajo cada red (ya deduplicados).
    "omitidas" son las redes que no se pudieron leer: sin acceso (no disponibles),
    sin cuentas o sin captura (no devolvieron nada). Nunca son fallas.
    """
    ahora = _ahora_utc(ahora)
    config_redes = fuentes.get("redes") or {}
    pedidas = list(redes) if redes is not None else list(config_redes)
    dias = int(fuentes.get("dias", 7))
    min_global = int(fuentes.get("min_vistas", 0))
    # Las piezas de la marca duran de 12 a 20 s. Por defecto se aceptan hasta 60 s:
    # una carpinteria se puede estirar un poco, un tutorial de dos minutos no.
    dur_max_global = int(fuentes.get("duracion_max_s", 60))
    top = max(0, int(top))
    disponibles = _disponibles()
    corrida = runner if runner is not None else functools.partial(
        _runner_por_defecto, cookies=cookies)

    recolectados: list[dict] = []
    vistos: dict[str, int] = {}
    fallas: list[str] = []
    omitidas: list[dict] = []

    # ---- PASADA 1 (barata): todas las redes y todas sus cuentas.
    for red in pedidas:
        cfg = config_redes.get(red) or {}
        if not disponibles.get(red, True):
            omitidas.append({"red": red, "motivo": "sin acceso"})
            vistos[red] = 0
            continue
        cuentas = cfg.get("cuentas") or []
        if not cuentas:
            omitidas.append({"red": red, "motivo": "sin cuentas"})
            vistos[red] = 0
            continue
        cuenta_videos: set[str] = set()
        fallo = False
        for usuario in cuentas:
            try:
                videos = corrida(red, usuario, n=por_red)
            except Exception as e:  # una red que falla no detiene la corrida
                fallas.append(f"{red}@{usuario}: {e}")
                fallo = True
                continue
            for video in videos or []:
                item = dict(video)
                item.setdefault("red", red)
                _fecha_iso_aware(item)
                recolectados.append(item)
                if item.get("url"):
                    cuenta_videos.add(item["url"])
        vistos[red] = len(cuenta_videos)
        # Una red que no devolvio nada tampoco se leyó: se anota como omitida,
        # nunca como falla que tumbe la corrida.
        if not cuenta_videos and not fallo:
            omitidas.append({"red": red, "motivo": "sin captura"})

    # ---- Dedupe por url y filtro de recientes + min_vistas de cada red.
    unicos: dict[str, dict] = {}
    for video in recolectados:
        url = video.get("url")
        if not url or url in unicos:
            continue
        unicos[url] = video

    filtrados: list[dict] = []
    for red in pedidas:
        cfg_red = config_redes.get(red) or {}
        min_red = int(cfg_red.get("min_vistas", min_global))
        # Una pieza de la marca dura de 12 a 20 s. Un tutorial de dos minutos no es
        # una carpinteria tropicalizable: se filtra por duracion antes de rankear.
        dur_max = cfg_red.get("duracion_max_s", dur_max_global)
        de_red = [v for v in unicos.values() if v.get("red") == red]
        de_red = [v for v in de_red if _dura(v) is None or _dura(v) <= dur_max]
        filtrados.extend(radar.filtrar(de_red, dias, min_red, ahora))

    # ---- PASADA 2 (cara): solo los mejores, con transcripcion y tres cuadros.
    ordenados = sorted(filtrados, key=lambda v: (valor_senal(v), _interacciones(v),
                                                  v.get("vistas") or 0),
                       reverse=True)[:top]
    candidatos: list[dict] = []
    for video in ordenados:
        item = dict(video)
        item["cuadros"] = []
        item["nota"] = ""
        info = None
        if item.get("red") not in REDES_SIN_YTDLP:
            info = _info_video(item.get("url", ""), cookies)
            if not item.get("transcripcion") and info:
                item["transcripcion"] = radar.bajar_transcripcion(info)
        if not cuadros:
            item["nota"] = "sin cuadros (--sin-cuadros)"
        elif item.get("red") not in REDES_CON_VIDEO:
            item["nota"] = f"{item.get('red') or 'esa red'} bloquea la descarga; sin cuadros"
        else:
            try:
                item["cuadros"] = _extraer_cuadros(item, cookies, info)
            except Exception as e:
                item["nota"] = f"sin cuadros: {e}"
        if item.get("vistas") is None and not valor_senal(item):
            # Instagram y X no publican vistas: sirven para ver FORMATOS nuevos,
            # pero no para rankear por popularity. Que quede dicho.
            item["nota"] = ((item["nota"] + "; ") if item["nota"] else "") + \
                "sin metrica publica: esta red no deja rankear por senal"
        candidatos.append(item)

    return {
        "fecha": ahora.astimezone(timezone.utc).date().isoformat(),
        "redes": pedidas,
        "vistos": vistos,
        "candidatos": candidatos,
        "fallas": fallas,
        "omitidas": omitidas,
    }


# ------------------------------------------------------------------ digest y escritura

def render_digest(resultado: dict) -> str:
    """El digest de una pantalla: top 3 para probar + tabla de las 5 mejores."""
    fecha = resultado.get("fecha", "")
    candidatos = resultado.get("candidatos") or []
    vistos = resultado.get("vistos") or {}
    omitidas = resultado.get("omitidas") or []

    resumen = [f"{len(resultado.get('redes') or [])} redes",
               f"{sum(vistos.values())} videos vistos",
               f"{len(candidatos)} a fondo"]
    if omitidas:
        resumen.append("omitidas: " + ", ".join(
            f"{_nombre_red(o.get('red') or '?')} ({o.get('motivo') or 'sin motivo'})"
            for o in omitidas))

    lineas = [f"# Radar diario · {fecha}", "", "Barrido: " + " · ".join(resumen), ""]
    if not candidatos:
        lineas.append("Hoy no hay candidatos que pasen los filtros.")
        return "\n".join(lineas) + "\n"

    lineas.append("## Top 3 para probar")
    for i, v in enumerate(candidatos[:3], 1):
        lineas.append(
            f"{i}. **{radar.gancho(v)}** — @{v.get('cuenta') or '?'} · "
            f"{numero_cr(v.get('vistas'))} vistas · "
            f"{porcentaje_cr(v.get('compartidos'), v.get('vistas'))} compartidos · "
            f"{duracion_texto(v)}")
        lineas.append(f"   Original: {v.get('url')}")

    lineas += ["", "## Las 5 mejores",
               "| # | Cuenta | Red | Vistas | Señal | Duración | Gancho | Video |",
               "|---|--------|-----|--------|-------|----------|--------|-------|"]
    for i, v in enumerate(candidatos[:5], 1):
        lineas.append(
            f"| {i} | @{v.get('cuenta') or '?'} | {_nombre_red(v.get('red') or '?')} | "
            f"{numero_cr(v.get('vistas'))} | {senal_texto(v)} | {duracion_texto(v)} | "
            f"{radar.gancho(v)} | [ver]({v.get('url')}) |")
    return "\n".join(lineas) + "\n"


def escribir(resultado: dict, salidas_dir: Path, hoy_md: Path) -> tuple[Path, Path]:
    """Deja el JSON crudo y el digest de una pantalla. UTF-8 sin BOM."""
    salidas_dir = Path(salidas_dir)
    hoy_md = Path(hoy_md)
    salidas_dir.mkdir(parents=True, exist_ok=True)
    hoy_md.parent.mkdir(parents=True, exist_ok=True)
    crudo = salidas_dir / f"{resultado.get('fecha') or 'diario'}.json"
    crudo.write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=str),
                      encoding="utf-8")
    hoy_md.write_text(render_digest(resultado), encoding="utf-8")
    return crudo, hoy_md


def _fallaron_todas(resultado: dict) -> bool:
    """True si no quedo ninguna red leida (todas fallaron o quedaron omitidas)."""
    fallas = resultado.get("fallas") or []
    omitidas = {o.get("red") for o in resultado.get("omitidas") or []}
    con_falla = {f.split("@", 1)[0] for f in fallas}
    leidas = [r for r in (resultado.get("redes") or [])
              if r not in con_falla and r not in omitidas]
    if leidas:
        return False
    return bool(fallas) or bool(omitidas)


# ------------------------------------------------------------------ principal

def main(argv: list[str] | None = None, runner: Runner | None = None,
         ahora: datetime | None = None) -> int:
    p = argparse.ArgumentParser(description="Radar diario multi-red")
    p.add_argument("--fuentes", type=Path, default=FUENTES)
    p.add_argument("--red", default=None,
                   help="redes separadas por coma (tiktok,youtube)")
    p.add_argument("--top", type=int, default=None,
                   help="cuantos videos se miran a fondo")
    p.add_argument("--sin-cuadros", action="store_true",
                   help="no baja video (mas rapido)")
    p.add_argument("--cookies", default=None,
                   help="chrome, edge o firefox, si alguna red lo pide")
    p.add_argument("--dry-run", action="store_true",
                   help="no escribe nada, solo muestra el resumen")
    p.add_argument("--salidas-dir", type=Path, default=SALIDAS)
    p.add_argument("--hoy", type=Path, default=HOY)
    a = p.parse_args(argv)

    if not a.fuentes.exists():
        print(f"No encuentro {a.fuentes}.", file=sys.stderr)
        return 2
    try:
        fuentes = json.loads(a.fuentes.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"{a.fuentes} no es JSON valido: {e}", file=sys.stderr)
        return 2

    config_redes = fuentes.get("redes") or {}
    if not config_redes:
        print(f"{a.fuentes} no tiene la seccion 'redes'.", file=sys.stderr)
        return 2

    pedidas = list(config_redes)
    if a.red:
        pedidas = [r.strip() for r in a.red.split(",") if r.strip()]
        for r in [r for r in pedidas if r not in config_redes]:
            print(f"  AVISO  red desconocida: {r}", file=sys.stderr)
        pedidas = [r for r in pedidas if r in config_redes]
        if not pedidas:
            print("Ninguna red valida en --red.", file=sys.stderr)
            return 2

    if runner is None:
        if radar.comando_ytdlp() is None:
            print("Falta yt-dlp. Instalalo con:  python -m pip install -U yt-dlp",
                  file=sys.stderr)
            return 2
        try:
            import redes  # noqa: F401
        except Exception:
            print("Falta marca/radar/redes.py (la pieza de captura de redes).",
                  file=sys.stderr)
            return 2

    top = a.top if a.top is not None else int(fuentes.get("top", 5))
    por_red = int(fuentes.get("por_fuente", 30))
    resultado = barrer(fuentes, redes=pedidas, ahora=ahora, runner=runner, top=top,
                       por_red=por_red, cookies=a.cookies,
                       cuadros=not (a.sin_cuadros or a.dry_run))

    for red, cantidad in resultado["vistos"].items():
        print(f"  {red}: {cantidad} videos vistos")
    for f in resultado["fallas"]:
        _imprimir(f"  FALLA  {f}", err=True)

    if a.dry_run:
        _imprimir(render_digest(resultado))
        print("[dry-run] no se escribio nada.")
    else:
        crudo, md = escribir(resultado, a.salidas_dir, a.hoy)
        print(f"{len(resultado['candidatos'])} a fondo · crudo: {crudo}")
        print(f"Digest: {md}")

    return 1 if _fallaron_todas(resultado) else 0


if __name__ == "__main__":
    sys.exit(main())
