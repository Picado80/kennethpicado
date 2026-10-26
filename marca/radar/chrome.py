"""Chrome o Edge headless para leer el DOM público de las redes que yt-dlp no alcanza.

Por qué existe: yt-dlp no sabe leer perfiles de Instagram ni timelines de X. Lo que
sí funciona es abrir la página en un navegador headless y quedarse con el DOM ya
renderizado. Solo lectura pública de páginas: nada de cookies del perfil real, nada
de descargar videos, nada de publicar nada.

Las dos trampas que ya se pagaron (no repetirlas):

1. Chrome headless se cuelga si su stdout va por una TUBERÍA, porque los procesos
   hijos del navegador mantienen el pipe abierto y `subprocess.run(capture_output=True)`
   se queda esperando para siempre. Por eso la salida va SIEMPRE a un archivo
   temporal y el stderr a DEVNULL. En Windows el exit code puede ser 4294967295
   aunque la operación sirva, así que el resultado se decide por el CONTENIDO del
   archivo, nunca por el exit code.

2. En esta máquina los Chrome que dejó Puppeteer (152.0.7977.75, .42 y
   147.0.7727.57) se cuelgan en silencio: devuelven 0 bytes y no dicen por qué.
   Solo Edge responde. Por eso `ruta_chrome()` no se queda con el más nuevo a
   ciegas: los prueba en orden y se queda con el primero que devuelve el DOM.

Uso:
    from chrome import chrome_disponible, dom, captura, ruta_chrome
    chrome_disponible()                      # True si hay un navegador utilizable
    html = dom("https://www.instagram.com/cuenta/")   # "" si no se pudo leer
    captura("https://x.com/cuenta", Path("marca/radar/salidas/x.png"))  # True si hay PNG
"""
from __future__ import annotations

import contextlib
import re
import subprocess
import tempfile
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SALIDAS = AQUI / "salidas"

# Chrome que dejó Puppeteer en la máquina. Se buscan dinámicamente y el Edge
# queda como plan B.
PUPPETEER_CHROME = Path.home() / ".cache" / "puppeteer" / "chrome"
# El Chrome instalado en el sistema. Va PRIMERO en la lista de preferencia: es el
# que responde en esta máquina (los de Puppeteer se cuelgan en silencio) y el suyo
# sí trae los reels de Instagram, que Edge no trae.
CHROME_SISTEMA = (
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
)
EDGE = (
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
)

# Flags que mantienen el navegador callado y sin colgarse.
FLAGS = (
    "--disable-gpu",
    "--no-sandbox",
    "--no-first-run",
    "--hide-scrollbars",
    "--disable-extensions",
    "--disable-background-networking",
    "--disable-component-update",
    "--disable-sync",
    "--disable-default-apps",
    "--disable-breakpad",
    "--no-default-browser-check",
    "--disable-features=Translate,BackForwardCache",
)


# ---------------------------------------------------------------- perfil temporal

@contextlib.contextmanager
def _perfil_temporal() -> Iterator[Path]:
    """Perfil de navegador descartable. Nunca el perfil real del usuario.

    Vive en marca/radar/salidas/ (ignorado por git) y, si esa carpeta no se puede
    usar, cae al temporal del sistema. Al salir lo borra.

    Ojo con la estructura: este generador tiene que CEDER UNA SOLA VEZ. Si el
    error del bloque que usa el perfil se-catching-acá, el generador cede otra vez
    y `contextlib` revienta con «generator didn't stop». Por eso la carpeta se
    crea ANTES de ceder el control, y el error del cuerpo solo llega al `finally`.
    """
    with contextlib.suppress(OSError):
        SALIDAS.mkdir(parents=True, exist_ok=True)
    tmp: tempfile.TemporaryDirectory | None = None
    for base in (SALIDAS, None):
        try:
            tmp = tempfile.TemporaryDirectory(prefix="radar_chrome_", dir=str(base) if base else None)
            break
        except OSError:
            continue
    if tmp is None:
        tmp = tempfile.TemporaryDirectory(prefix="radar_chrome_")
    try:
        yield Path(tmp.name) / "perfil"
    finally:
        with contextlib.suppress(OSError):
            tmp.cleanup()


# ---------------------------------------------------------------- proceso

def _matar_arbol(pid: int) -> None:
    """Mata el proceso y a sus hijos. Sin esto, un Chrome colgado se queda vivo
    quemando CPU y poisoned la lectura siguiente."""
    for comando in (["taskkill", "/T", "/F", "/PID", str(pid)],
                    ["taskkill", "/F", "/PID", str(pid)]):
        with contextlib.suppress(OSError, subprocess.SubprocessError):
            subprocess.run(comando, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=30)


def _correr(args: list[str], salida: Path | None, timeout: int) -> int:
    """Corre el navegador. La salida va al archivo `salida` (nunca a una tubería).

    Devuelve el exit code del navegador; en Windows puede ser 4294967295 aunque
    la operación sirva, así que el resultado se decide por el contenido.
    """
    fh = open(salida, "wb") if salida is not None else subprocess.DEVNULL
    try:
        p = subprocess.Popen(args, stdout=fh, stderr=subprocess.DEVNULL,
                             stdin=subprocess.DEVNULL)
    except OSError:
        if salida is not None:
            fh.close()
        return -1
    try:
        return p.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        _matar_arbol(p.pid)
        with contextlib.suppress(subprocess.TimeoutExpired):
            p.wait(timeout=15)
        return -1
    finally:
        if salida is not None:
            fh.close()


# ---------------------------------------------------------------- binario

def _version(carpeta: str) -> tuple[int, ...]:
    """Version numérica de una carpeta tipo `win64-152.0.7977.75`."""
    m = re.search(r"(\d+(?:\.\d+)*)$", carpeta)
    return tuple(int(p) for p in m.group(1).split(".")) if m else ()


def _candidatos() -> list[Path]:
    """Los binarios que hay, en orden de preferencia.

    Primero el Chrome instalado en el sistema: es el que responde en esta máquina
    (los que dejó Puppeteer se cuelgan en silencio y devuelven 0 bytes), y el suyo
    sí trae los reels de Instagram, que Edge no trae. Después los Chrome de
    Puppeteer, del más nuevo al más viejo, y al final el Edge, que es el plan B.

    El orden es de preferencia, no de versión: `ruta_chrome()` prueba cada uno y se
    queda con el primero que responde de verdad.
    """
    encontrados: list[tuple[tuple[int, ...], Path]] = []
    if PUPPETEER_CHROME.is_dir():
        for carpeta in PUPPETEER_CHROME.iterdir():
            exe = carpeta / "chrome-win64" / "chrome.exe"
            if exe.is_file():
                encontrados.append((_version(carpeta.name), exe))
    encontrados.sort(key=lambda c: c[0], reverse=True)
    sistema = [exe for exe in CHROME_SISTEMA if exe.is_file()]
    puppeteer = [exe for _v, exe in encontrados]
    return sistema + puppeteer + [edge for edge in EDGE if edge.is_file()]


def _responde(exe: Path, timeout: int = 8) -> bool:
    """True si el navegador abre una página y devuelve el DOM. Es la única forma
    de saber si el binario sirve: el cuelgue no dice nada, solo no contesta.

    La prueba es `about:blank`: no depende de la red y responde en menos de un
    segundo cuando el navegador está sano.
    """
    with _perfil_temporal() as perfil:
        salida = perfil.parent / "dom.html"
        args = [str(exe), "--headless=new", *FLAGS, "--virtual-time-budget=2000",
                f"--user-data-dir={perfil}", "--dump-dom", "about:blank"]
        _correr(args, salida, timeout)
        try:
            return salida.stat().st_size > 20
        except OSError:
            return False


_ELEGIDO: str | None = None
_PROBADO = False


def ruta_chrome() -> str | None:
    """El navegador que sirve: el de mayor versión QUE ADEMÁS RESPONDE.

    Ojo: en esta máquina los Chrome de Puppeteer (152.0.7977.75, .42 y
    147.0.7727.57) se cuelgan en silencio y devuelven 0 bytes; el Edge sí
    responde. Por eso no basta con el más nuevo: se prueban en orden y se queda
    con el primero que devuelve el DOM. El resultado se cachea.
    """
    global _ELEGIDO, _PROBADO
    if _PROBADO:
        return _ELEGIDO
    _PROBADO = True
    candidatos = _candidatos()
    if not candidatos:
        return None
    # Se prueban todos a la vez: cada uno con su perfil y colgar uno no debe
    # hacer esperar a los demás.
    with ThreadPoolExecutor(max_workers=len(candidatos)) as pool:
        respuestas = list(pool.map(lambda exe: _responde(exe), candidatos))
    for exe, responde in zip(candidatos, respuestas):
        if responde:
            _ELEGIDO = str(exe)
            return _ELEGIDO
    return None


def chrome_disponible() -> bool:
    """True si hay un navegador headless utilizable en esta máquina."""
    exe = ruta_chrome()
    return bool(exe) and Path(exe).is_file()


# ---------------------------------------------------------------- lecturas

def dom(url: str, timeout: int = 60, budget: int = 25000) -> str:
    """El DOM renderizado de `url`. "" si el navegador no existe o no escribió nada.

    Si el navegador se cuelga pero alcanzó a escribir el DOM, se devuelve ese DOM
    parcial: lo que se leyó es válido, lo que falte queda en None.
    """
    exe = ruta_chrome()
    if not exe:
        return ""
    with _perfil_temporal() as perfil:
        salida = perfil.parent / "dom.html"
        args = [exe, "--headless=new", *FLAGS, f"--virtual-time-budget={budget}",
                f"--user-data-dir={perfil}", "--dump-dom", url]
        _correr(args, salida, timeout)
        try:
            return salida.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            return ""


def captura(url: str, destino: Path, timeout: int = 60) -> bool:
    """Guarda una captura de pantalla de `url` en `destino`. True si se escribió el PNG."""
    exe = ruta_chrome()
    if not exe:
        return False
    destino = Path(destino)
    try:
        destino.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        return False
    with _perfil_temporal() as perfil:
        args = [exe, "--headless=new", *FLAGS, "--virtual-time-budget=15000",
                "--window-size=1280,1600", f"--user-data-dir={perfil}",
                f"--screenshot={destino}", url]
        _correr(args, None, timeout)
    try:
        return destino.is_file() and destino.stat().st_size > 0
    except OSError:
        return False
