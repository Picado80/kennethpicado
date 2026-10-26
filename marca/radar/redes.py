"""Adquisición de datos por red social para el radar diario de la marca personal.

Esta capa consigue METADATOS (números, fecha, texto, url) de videos y posts de
cuatro redes: TikTok, Instagram, X y YouTube. No decide qué entra al radar, no
arma la carpintería y no publica nada: solo trae los datos y los deja en el
formato de columnas que consume la capa de arriba.

De dónde sale cada red (verificado en esta máquina):
  - TikTok y YouTube: yt-dlp (subprocess, `-J --skip-download`). Sí trae
    vistas, likes, comentarios, compartidos, guardados, duración y fecha.
  - X: el HTML público del perfil. X se sirve renderizado desde el servidor y
    ahí van los contadores exactos de cada estado (likes, respuestas, reposts).
  - Instagram: se parsea el DOM renderizado del perfil (reels y posts). Hoy
    Instagram devuelve un muro de login al que no se le puede pedir sesión
    desde este entorno, así que suele volver vacío: la función devuelve []
    en vez de inventar números.

Regla que no se negocia: lo que no se pudo leer va en None. Cero es un dato
("lo vi y es cero"); None es "no lo sé". Nunca se inventa un número.

Uso:
    from redes import REDES, COLUMNAS, disponibles, obtener, senal, url_cuenta
    disponibles()                       # {'tiktok': True, 'instagram': ..., ...}
    videos = obtener("tiktok", "dotcsv", n=30)
    if videos:
        valor, tipo = senal(videos[0])   # (0.06, 'compartidos')

Ninguna función de esta capa levanta excepciones por culpa de la red: si una
red falla, `obtener` devuelve [] y el resto del radar sigue.
"""
from __future__ import annotations

import html as htmllib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

import chrome  # noqa: E402  (mismo directorio, import relativo no disponible)

# Las redes que esta capa sabe leer.
REDES: list[str] = ["tiktok", "instagram", "x", "youtube"]

# Las columnas que la capa de arriba espera, en este orden exacto.
COLUMNAS: list[str] = [
    "url", "red", "cuenta", "fuente", "fecha", "vistas", "likes", "comentarios",
    "compartidos", "guardados", "duracion_s", "texto", "transcripcion",
    "señal", "señal_tipo",
]

# La URL pública de cada cuenta.
URL_CUENTA: dict[str, str] = {
    "tiktok": "https://www.tiktok.com/@{usuario}",
    "instagram": "https://www.instagram.com/{usuario}/",
    "x": "https://x.com/{usuario}",
    "youtube": "https://www.youtube.com/@{usuario}/shorts",
}

# Cuánto espera el navegador a cada red (Instagram y X son lentas).
TIMEOUT_DOM = 60
BUDGET_DOM = 25000

# TikTok y YouTube no avisan cuando les ponés freno: contestan con la lista vacía
# en menos de dos segundos y sin mensaje de error. Verificado el 26-oct-2026: la
# misma cuenta que devolvía 0 videos volvía con 10 después de 25 s de espera.
# Por eso, cuando la captura viene vacía, se reintenta con espera en vez de
# tomar el vacío por respuesta buena.
REINTENTOS_YTDLP = 4
ESPERA_YTDLP = 20  # segundos entre intento e intento

# Cada red aguanta un pedido y frena al siguiente. Antes de pedirle otra cosa a la
# MISMA red se espera este rato, para no perder la cuenta entera por preguntar
# demasiado seguido.
ESPERA_ENTRE_CUENTAS = 15  # segundos entre dos cuentas de la misma red
_ultima_peticion: dict[str, float] = {}

# TikTok no siempre deja sacar el "secUid" (el identificador interno de la cuenta)
# de la página de perfil: esa página devuelve un reto anti-bot y a veces no lo pasa.
# Verificado el 26-oct-2026: la misma cuenta daba 0 videos o 5 videos, al azar.
# Cuando ya se tiene el secUid, la ruta `tiktokuser:<secUid>` va directo a la API
# y no vuelve a pasar por la página de perfil. Por eso se guarda en una cache
# local (esta carpeta la ignora git).
SECUIDS = AQUI / "salidas" / "secuids.json"

# Con qué navegador se pide el HTML público cuando el headless no sirve.
UA_ESCRITORIO = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                 "(KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36")

# Multiplicadores de los números abreviados ("1.2K", "3.4M").
MULTIPLICADORES = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}


# ---------------------------------------------------------------- funciones puras

def listar_redes() -> list[str]:
    """Las redes que esta capa maneja."""
    return list(REDES)


def _cuenta(usuario: str) -> str:
    """El usuario sin arroba, sin espacios y sin barras."""
    return str(usuario or "").strip().lstrip("@").strip().strip("/")


def url_cuenta(red: str, usuario: str) -> str:
    """La URL pública del perfil. "" si la red no existe."""
    plantilla = URL_CUENTA.get(str(red or "").strip().lower())
    if plantilla is None:
        return ""
    return plantilla.format(usuario=_cuenta(usuario))


def _entero(valor) -> int | None:
    """Un número que venga como int, float o texto ("1,234", "1.2K"). None si no es número."""
    if valor is None or isinstance(valor, bool):
        return None
    if isinstance(valor, int):
        return valor
    if isinstance(valor, float):
        return int(valor)
    texto = str(valor).strip().replace(",", "")
    m = re.fullmatch(r"([\d.]+)\s*([KMB])?", texto, re.IGNORECASE)
    if not m:
        return None
    try:
        numero = float(m.group(1))
    except ValueError:
        return None
    return int(numero * MULTIPLICADORES.get((m.group(2) or "").lower(), 1))


def _marca_iso(valor) -> str | None:
    """Una marca de tiempo (segundos o milisegundos) en ISO 8601 con timezone."""
    if not isinstance(valor, (int, float)) or isinstance(valor, bool) or valor <= 0:
        return None
    if valor > 100_000_000_000:  # viene en milisegundos
        valor = valor / 1000
    try:
        return datetime.fromtimestamp(valor, tz=timezone.utc).isoformat()
    except (OverflowError, OSError, ValueError):
        return None


def _fecha_iso(info: dict) -> str | None:
    """La fecha en ISO 8601 con timezone. None si el post no dice cuándo se publicó."""
    for clave in ("timestamp", "release_timestamp", "created_at_ms"):
        fecha = _marca_iso(info.get(clave))
        if fecha:
            return fecha
    fecha = info.get("upload_date")
    if isinstance(fecha, str) and re.fullmatch(r"\d{8}", fecha.strip()):
        try:
            return datetime.strptime(fecha.strip(), "%Y%m%d").replace(
                tzinfo=timezone.utc).isoformat()
        except ValueError:
            return None
    return None


def senal(v: dict) -> tuple[float, str]:
    """La métrica con la que se rankea: (valor, tipo de señal).

    TikTok: compartidos/vistas cuando hay compartidos; si no, (likes+comentarios)/vistas.
    Instagram, YouTube y X: (likes+comentarios)/vistas.
    Sin vistas no hay señal: 0.0.
    """
    red = str(v.get("red") or "").strip().lower()
    vistas = v.get("vistas")
    likes = v.get("likes") or 0
    comentarios = v.get("comentarios") or 0
    compartidos = v.get("compartidos")
    if red == "tiktok" and compartidos is not None:
        tipo, numerador = "compartidos", compartidos
    else:
        tipo, numerador = "interaccion", likes + comentarios
    if not isinstance(vistas, (int, float)) or isinstance(vistas, bool) or vistas <= 0:
        return 0.0, tipo
    return float(numerador) / float(vistas), tipo


def normalizar(red: str, info: dict) -> dict:
    """Un metadato crudo (de yt-dlp o del DOM) a nuestras columnas.

    Lo que no se sepa va en None. Nunca se inventa un número.
    """
    info = info or {}
    cuenta = info.get("cuenta") or info.get("uploader") or info.get("channel") or ""
    texto = info.get("texto") or info.get("description") or info.get("title") or ""
    url = info.get("webpage_url") or info.get("original_url") or info.get("url") or ""
    # TikTok devuelve la URL con el id interno de la cuenta (@MS4wLjABAAAA...).
    # Cuando ya sabemos cómo se llama, se deja la URL legible.
    if red == "tiktok" and cuenta and "@MS4wLjAB" in url:
        url = re.sub(r"@MS4wLjAB[\w-]+", "@" + cuenta, url, count=1)
    v = {
        "url": url,
        "red": red,
        "cuenta": cuenta,
        "fuente": info.get("fuente") or f"{red} @{cuenta}".strip(),
        "fecha": _fecha_iso(info),
        "vistas": _entero(info.get("view_count")),
        "likes": _entero(info.get("like_count")),
        "comentarios": _entero(info.get("comment_count")),
        "compartidos": _entero(info.get("repost_count")),
        "guardados": _entero(info.get("save_count")),
        "duracion_s": _entero(info.get("duration")),
        "texto": str(texto).strip(),
        "transcripcion": "",
    }
    v["señal"], v["señal_tipo"] = senal(v)
    return {columna: v[columna] for columna in COLUMNAS}


# ---------------------------------------------------------------- lectura del DOM

def _a_texto(html: str) -> str:
    """El HTML sin tags, con entidades resueltas y espacios ordenados."""
    limpio = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    limpio = re.sub(r"(?s)<[^>]+>", " ", limpio)
    limpio = htmllib.unescape(limpio)
    return re.sub(r"\s+", " ", limpio).strip()


def _numero_cerca(texto: str) -> int | None:
    """El primer número del texto ("1,234", "1.2K"). None si no hay."""
    m = re.search(r"(\d[\d.,]*\s?[KMB]?)", texto, re.IGNORECASE)
    return _entero(m.group(1)) if m else None


def _metrica_por_palabra(texto: str, palabras: tuple[str, ...]) -> int | None:
    """Un contador del texto escrito ("3 replies", "1.2K likes"). None si no está."""
    for palabra in palabras:
        m = re.search(r"([\d][\d.,]*\s?[KMB]?)\s*" + palabra + r"\b", texto, re.IGNORECASE)
        if m:
            valor = _entero(m.group(1))
            if valor is not None:
                return valor
    return None


def _ultimo_numero(texto: str, clave: str) -> int | None:
    """El último valor de una clave JSON ("favorite_count":12). None si no está."""
    valores = re.findall(rf'"{clave}":\s*"?(\d+)"?', texto)
    return _entero(valores[-1]) if valores else None


def _ultimo_texto(texto: str, patron: str) -> str | None:
    """El último texto que casa con el patrón. None si no hay ninguno."""
    encontrados = re.findall(patron, texto, re.S)
    return encontrados[-1] if encontrados else None


def _desescapar(texto: str) -> str:
    """Suelta los escapes de JSON de un texto que venía dentro de un string."""
    limpio = texto.replace('\\"', '"').replace("\\n", " ").replace("\\t", " ").replace("\\/", "/")
    return re.sub(r"\s+", " ", limpio).strip()


def _celdas(html: str, patron: re.Pattern) -> list[tuple[str, str]]:
    """Parte el HTML en trozos: (href, trozo de HTML desde el enlace hasta el siguiente)."""
    encontradas = list(patron.finditer(html))
    salida = []
    for i, m in enumerate(encontradas):
        fin = encontradas[i + 1].start() if i + 1 < len(encontradas) else len(html)
        salida.append((m.group(1), html[m.start():fin]))
    return salida


# Instagram pone el usuario dentro del href: "/machillo.puravida/reel/De7pfWfO0f5/".
# Por eso el patrón no puede exigir que el href EMPIECE en "/reel/".
RE_REEL = re.compile(r'href="([^"]*/reel/[^"]+)"')
RE_POST = re.compile(r'href="([^"]*/p/[^"]+)"')
RE_ARTICLE = re.compile(r'(?is)<article\b[^>]*data-testid="tweet".*?</article>')
RE_STATUS = re.compile(r'href="/[^"]*/status/(\d+)"')
RE_TWEET = re.compile(r'entry_id":"tweet-(\d+)')


def _parse_instagram(html: str, n: int) -> list[dict]:
    """Los reels (y, si no hay reels, los posts) del perfil, con lo que se pudo leer."""
    celdas = _celdas(html, RE_REEL)
    tipo = "reel"
    if not celdas:
        celdas = _celdas(html, RE_POST)
        tipo = "post"
    salida = []
    for ruta, trozo in celdas:
        if len(salida) >= n:
            break
        codigo = ruta.strip("/").split("/")[-1]
        if not codigo:
            continue
        alt = re.search(r'alt="([^"]*)"', trozo)
        texto = htmllib.unescape(alt.group(1)).strip() if alt else ""
        if not texto:
            texto = _a_texto(trozo)[:300]
        likes = _metrica_por_palabra(_a_texto(trozo), ("likes", "like"))
        if likes is None:
            likes = _metrica_por_palabra(trozo, ("likes", "like"))
        salida.append({
            "webpage_url": f"https://www.instagram.com/{tipo}/{codigo}/",
            "view_count": None,
            "like_count": likes,
            "comment_count": None,
            "texto": texto,
        })
    return salida


def _x_desde_trozo(estado: str, trozo: str) -> dict:
    """Un estado de X a partir del trozo de HTML que lo contiene."""
    texto = _ultimo_texto(trozo, r'"full_text":"((?:[^"\\]|\\.)*)"')
    vistas = _ultimo_numero(trozo, "view_count")
    if vistas is None:
        crudo = _ultimo_texto(trozo, r'"views":\{"count":"(\d+)"')
        vistas = _entero(crudo) if crudo else None
    return {
        "webpage_url": f"https://x.com/i/status/{estado}",
        "view_count": vistas,
        "like_count": _ultimo_numero(trozo, "favorite_count"),
        "comment_count": _ultimo_numero(trozo, "reply_count"),
        "repost_count": _ultimo_numero(trozo, "retweet_count"),
        "save_count": _ultimo_numero(trozo, "bookmark_count"),
        "created_at_ms": _ultimo_numero(trozo, "created_at_ms"),
        "texto": _desescapar(texto) if texto else "",
    }


def _contador_por_testid(fragmento: str, testid: str, palabras: tuple[str, ...]) -> int | None:
    """El contador que cuelga de un data-testid ("reply", "retweet", "like").

    Primero se busca la palabra del contador ("18 replies"); si no está, se toma
    el primer número que sigue a la marca.
    """
    m = re.search(rf'data-testid="{testid}"(.{{0,500}})', fragmento, re.S)
    if not m:
        return None
    ventana = re.sub(r"<[^>]+>", " ", m.group(1))
    valor = _metrica_por_palabra(ventana, palabras)
    return valor if valor is not None else _numero_cerca(ventana)


def _x_desde_dom(html: str, n: int) -> list[dict]:
    """Los estados que se ven en el DOM ya renderizado.

    Los contadores se leen de los atributos aria-label ("18 replies") o de lo que
    cuelga del data-testid correspondiente. Si no están, None.
    """
    articulos = RE_ARTICLE.findall(html)
    if not articulos:
        articulos = [t for _, t in _celdas(html, RE_STATUS)]
    salida, vistos = [], set()
    for articulo in articulos:
        if len(salida) >= n:
            break
        m = RE_STATUS.search(articulo)
        if not m:
            continue
        estado = m.group(1)
        if estado in vistos:
            continue
        vistos.add(estado)
        texto = _a_texto(articulo)
        etiquetas = " ".join(re.findall(r'aria-label="([^"]*)"', articulo))
        cuerpo = re.search(r'(?is)data-testid="tweetText"[^>]*>(.*?)</div>', articulo)
        salida.append({
            "webpage_url": f"https://x.com/i/status/{estado}",
            "view_count": (_metrica_por_palabra(etiquetas, ("views", "view"))
                           or _metrica_por_palabra(texto, ("views", "view"))),
            "like_count": (_metrica_por_palabra(etiquetas, ("likes",))
                           or _contador_por_testid(articulo, "like", ("likes",))
                           or _metrica_por_palabra(texto, ("likes",))),
            "comment_count": (_metrica_por_palabra(etiquetas, ("replies", "reply"))
                              or _contador_por_testid(articulo, "reply", ("replies", "reply"))
                              or _metrica_por_palabra(texto, ("replies", "reply"))),
            "repost_count": (_metrica_por_palabra(etiquetas, ("reposts", "repost"))
                             or _contador_por_testid(articulo, "retweet", ("reposts", "repost"))
                             or _metrica_por_palabra(texto, ("reposts", "repost"))),
            "texto": _a_texto(cuerpo.group(1)) if cuerpo else texto[:300],
        })
    return salida


def _parse_x(html: str, n: int) -> list[dict]:
    """Los estados de la timeline de X.

    X se sirve renderizado desde el servidor: en el HTML viene el payload con los
    contadores exactos de cada estado. Si no está, se busca en el DOM ya pintado.
    """
    texto = html.replace('\\"', '"')
    marcas = list(RE_TWEET.finditer(texto))
    if marcas:
        salida = []
        for i, m in enumerate(marcas):
            if len(salida) >= n:
                break
            inicio = marcas[i - 1].end() if i else 0
            salida.append(_x_desde_trozo(m.group(1), texto[inicio:m.start()]))
        return salida
    return _x_desde_dom(html, n)


def _parsear(red: str, html: str, n: int) -> list[dict]:
    """El HTML de una red a sus metadatos crudos."""
    if not html:
        return []
    if red == "instagram":
        return _parse_instagram(html, n)
    if red == "x":
        return _parse_x(html, n)
    return []


# ---------------------------------------------------------------- lectura por red

def _comando_ytdlp() -> list[str] | None:
    """El comando para correr yt-dlp. None si no está instalado."""
    if importlib.util.find_spec("yt_dlp"):
        return [sys.executable, "-m", "yt_dlp"]
    exe = shutil.which("yt-dlp")
    return [exe] if exe else None


def _ytdlp_json(url: str, n: int, cookies: str | None) -> tuple[list[dict], dict]:
    """Una llamada a yt-dlp: (los videos, la respuesta completa).

    Si viene vacía, se reintenta con espera: TikTok y YouTube contestan con la
    lista vacía cuando la misma IP pidió muy seguido, y eso no es lo mismo que
    "la cuenta no tiene videos". Ver `REINTENTOS_YTDLP`.
    """
    base = _comando_ytdlp()
    if not base:
        return [], {}
    cmd = base + ["-J", "--skip-download", "--no-warnings", "--ignore-errors",
                  "--playlist-end", str(max(1, n)), url]
    if cookies:
        cmd[len(base):len(base)] = ["--cookies-from-browser", cookies]
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    red = url.split("/")[2] if "//" in url else ""
    for intento in range(REINTENTOS_YTDLP):
        # No pedirle dos cosas seguidas a la misma red: la segunda vuelve vacía.
        anterior = _ultima_peticion.get(red)
        if anterior is not None:
            faltan = ESPERA_ENTRE_CUENTAS - (time.monotonic() - anterior)
            if faltan > 0:
                time.sleep(faltan)
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=300, env=env)
        except (subprocess.TimeoutExpired, OSError):
            r = None
        # La cuenta arranca a contar cuando termina el pedido anterior: si no, un
        # pedido de 30 s dejaría al siguiente sin espera ninguna.
        _ultima_peticion[red] = time.monotonic()
        datos: dict = {}
        entradas: list[dict] = []
        if r is not None:
            try:
                maybe = json.loads(r.stdout) if r.stdout.strip() else None
            except json.JSONDecodeError:
                maybe = None
            if isinstance(maybe, dict):
                datos = maybe
                crudas = maybe.get("entries") if "entries" in maybe else [maybe]
                entradas = [e for e in (crudas or []) if isinstance(e, dict)]
        if entradas:
            return entradas, datos
        # Venía vacía: se espera y se reintenta. El último intento no espera.
        if intento < REINTENTOS_YTDLP - 1:
            time.sleep(ESPERA_YTDLP)
    return [], {}


def _leer_secuids() -> dict:
    """La cache de secUid por cuenta. {} si no hay o si no se puede leer."""
    try:
        datos = json.loads(SECUIDS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return datos if isinstance(datos, dict) else {}


def _guardar_sec_uid(cuenta: str, sec_uid: str) -> None:
    """Guarda el secUid de una cuenta para no volver a pedirlo."""
    if not sec_uid:
        return
    datos = _leer_secuids()
    if datos.get(cuenta) == sec_uid:
        return
    datos[cuenta] = sec_uid
    try:
        SECUIDS.parent.mkdir(parents=True, exist_ok=True)
        SECUIDS.write_text(json.dumps(datos, ensure_ascii=False, indent=1),
                           encoding="utf-8")
    except OSError:
        pass


def _semillas_tiktok(cuenta: str) -> list[str]:
    """URLs de videos de la cuenta, para sacarle el secUid sin pasar por el perfil.

    Vienen de `fuentes.json` (`redes.tiktok.semillas`): un video cualquiera de la
    cuenta. De un video, yt-dlp devuelve el `channel_id`, que ES el secUid.
    """
    try:
        fuentes = json.loads((AQUI / "fuentes.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    semillas = ((fuentes.get("redes") or {}).get("tiktok") or {}).get("semillas") or []
    return [s for s in semillas if f"/@{cuenta}/" in str(s)]


def _de_la_cuenta(videos: list[dict], cuenta: str) -> list[dict]:
    """Se queda solo con los videos que son de esta cuenta.

    El id interno (secUid) puede quedar pegado a la cuenta equivocada si la
    semilla apuntaba a otro video. Con este filtro eso no pasa: si no coincide,
    se descarta la tanda y se sigue por el camino de perfil.
    """
    de_esta = []
    for v in videos:
        uploader = str(v.get("uploader") or v.get("channel") or "").strip().lower()
        if not uploader or uploader == cuenta.lower():
            de_esta.append(v)
    return de_esta


def _por_ytdlp_tiktok(cuenta: str, n: int, cookies: str | None) -> list[dict]:
    """Los videos de una cuenta de TikTok.

    Tres caminos, del más seguro al menos:
      1. Con el secUid en la cache: `tiktokuser:<secUid>` va directo a la API.
      2. Sin secUid: se saca de un video de la cuenta (semilla de `fuentes.json`).
      3. Si tampoco: se pide la página de perfil (con reintentos).
    """
    sec_uid = _leer_secuids().get(cuenta)
    if sec_uid:
        videos, _ = _ytdlp_json(f"tiktokuser:{sec_uid}", n, cookies)
        de_esta = _de_la_cuenta(videos, cuenta)
        if de_esta:
            return de_esta

    for semilla in _semillas_tiktok(cuenta):
        videos, _ = _ytdlp_json(semilla, 1, cookies)
        if not videos:
            continue
        nuevo = videos[0].get("channel_id")
        if not nuevo:
            continue
        _guardar_sec_uid(cuenta, nuevo)
        videos, _ = _ytdlp_json(f"tiktokuser:{nuevo}", n, cookies)
        de_esta = _de_la_cuenta(videos, cuenta)
        if de_esta:
            return de_esta

    videos, datos = _ytdlp_json(url_cuenta("tiktok", cuenta), n, cookies)
    de_esta = _de_la_cuenta(videos, cuenta)
    if de_esta:
        nuevo = de_esta[0].get("channel_id") or datos.get("channel_id")
        if nuevo:
            _guardar_sec_uid(cuenta, nuevo)
    return de_esta


def _por_ytdlp(red: str, cuenta: str, n: int, cookies: str | None) -> list[dict]:
    """Los metadatos que da yt-dlp para una cuenta."""
    if red == "tiktok":
        return _por_ytdlp_tiktok(cuenta, n, cookies)
    videos, _ = _ytdlp_json(url_cuenta(red, cuenta), n, cookies)
    return videos




def _cabecera_cookies(ruta: str, host: str) -> str:
    """Convierte un cookies.txt (formato Netscape) en una cabecera Cookie."""
    try:
        lineas = Path(ruta).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    pares = []
    for linea in lineas:
        if not linea.strip() or linea.startswith("#"):
            continue
        campos = linea.split("\t")
        if len(campos) < 7:
            continue
        dominio, nombre, valor = campos[0], campos[5], campos[6]
        if dominio.lstrip(".") and host.endswith(dominio.lstrip(".")):
            pares.append(f"{nombre}={valor}")
    return "; ".join(pares)


def _html_publico(url: str, cookies: str | None = None) -> str:
    """El HTML de una página pública, pedido por HTTP simple.

    Es el plan B del navegador headless: a veces la página ya viene con los datos
    en el HTML que manda el servidor.
    """
    cabeceras = {"User-Agent": UA_ESCRITORIO, "Accept-Language": "en-US,en;q=0.9",
                 "Accept": "text/html,application/xhtml+xml,*/*;q=0.8"}
    if cookies and Path(cookies).is_file():
        cabecera = _cabecera_cookies(cookies, urllib.parse.urlparse(url).hostname or "")
        if cabecera:
            cabeceras["Cookie"] = cabecera
    peticion = urllib.request.Request(url, headers=cabeceras)
    try:
        with urllib.request.urlopen(peticion, timeout=30) as r:
            return r.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, OSError, ValueError):
        return ""


def _por_dom(red: str, cuenta: str, n: int, cookies: str | None = None) -> list[dict]:
    """Los metadatos del perfil: primero el navegador headless, y si no sirve,
    la misma página pedida por HTTP simple."""
    url = url_cuenta(red, cuenta)
    if not url:
        return []
    try:
        html = chrome.dom(url, timeout=TIMEOUT_DOM, budget=BUDGET_DOM)
    except Exception:
        html = ""
    crudos = _parsear(red, html, n)
    if crudos:
        return crudos
    html = _html_publico(url, cookies)
    return _parsear(red, html, n)


# ---------------------------------------------------------------- disponibilidad

def _ytdlp_responde() -> bool:
    """True si yt-dlp está instalado y arranca. Chequeo barato: no barre videos."""
    base = _comando_ytdlp()
    if not base:
        return False
    try:
        r = subprocess.run(base + ["--version"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60)
    except (subprocess.TimeoutExpired, OSError):
        return False
    return r.returncode == 0 and bool(r.stdout.strip())


def disponibles() -> dict[str, bool]:
    """Qué redes se pueden leer en ESTA máquina ahora mismo.

    Chequeo barato: no barre 30 videos ni descarga nada.
    """
    hay_ytdlp = _ytdlp_responde()
    hay_chrome = chrome.chrome_disponible()
    return {
        "tiktok": hay_ytdlp,
        "instagram": hay_chrome,
        "x": hay_chrome,
        "youtube": hay_ytdlp,
    }


# ---------------------------------------------------------------- principal

def obtener(red: str, usuario: str, n: int = 30, cookies: str | None = None) -> list[dict]:
    """Los últimos `n` posts de `usuario` en `red`, en nuestras columnas.

    `cookies` es el nombre del navegador para yt-dlp (TikTok y YouTube) y el
    caminho a un cookies.txt para las redes que se leen por HTTP (Instagram y X).

    Si la red falla, devuelve [] y no levanta excepción: una red caída no puede
    tumbar el radar.
    """
    red = str(red or "").strip().lower()
    if red not in REDES:
        return []
    cuenta = _cuenta(usuario)
    if not cuenta:
        return []
    try:
        if red in ("tiktok", "youtube"):
            crudos = _por_ytdlp(red, cuenta, n, cookies)
        else:
            crudos = _por_dom(red, cuenta, n, cookies)
    except Exception:
        return []
    salida = []
    for info in crudos:
        v = normalizar(red, info)
        v["cuenta"] = cuenta
        v["fuente"] = f"{red} @{cuenta}"
        v["señal"], v["señal_tipo"] = senal(v)
        salida.append(v)
    return salida
