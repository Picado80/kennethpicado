"""Arma el guion gráfico barato de un lote: una página por día, una fila por pieza, con bocetos en vez de renders.

Es lo que Kenneth aprueba ANTES de producir cualquier pieza (ESTRATEGIA.md §3: siempre, primero el guion gráfico).

Uso (desde la raíz de kennethpicado):
    python marca/scripts/lote.py marca/produccion/lote-s1/lote.json --salida marca/salidas/lote-s1

Cada cuadro es un boceto en HTML: el texto que va en pantalla y, entre corchetes, la toma o el dato que falta.
Saca las páginas en PNG y WEBP con Edge o Chrome sin ventana y ffmpeg. No llama a ninguna API ni gasta nada.
"""
import argparse
import html
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

FUENTES = Path(__file__).resolve().parents[1] / "estilo" / "fuentes"

CSS = """
@font-face { font-family: "Instrument Serif"; font-style: normal; src: url("fuentes/instrument-serif-latin-400-normal.woff2") format("woff2"); }
@font-face { font-family: "Instrument Serif"; font-style: italic; src: url("fuentes/instrument-serif-latin-400-italic.woff2") format("woff2"); }
@font-face { font-family: "Archivo"; font-weight: 600; src: url("fuentes/archivo-latin-600-normal.woff2") format("woff2"); }
@font-face { font-family: "Archivo"; font-weight: 900; src: url("fuentes/archivo-latin-900-normal.woff2") format("woff2"); }
@font-face { font-family: "JetBrains Mono"; font-weight: 500; src: url("fuentes/jetbrains-mono-latin-500-normal.woff2") format("woff2"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { width: 1080px; background: #101B33; color: #E8E6DE; font-family: "Archivo", sans-serif; font-weight: 600; }
.mono { font-family: "JetBrains Mono", monospace; font-weight: 500; text-transform: uppercase; letter-spacing: 0.12em; }
.barra { background: #E8E6DE; color: #16233F; display: flex; justify-content: space-between; padding: 16px 32px; font-size: 18px; }
.cabeza { padding: 24px 32px 18px; }
.cabeza h1 { font-family: "Instrument Serif", serif; font-weight: 400; font-size: 50px; line-height: 1.05; }
.cabeza .meta { font-size: 16px; opacity: 0.6; margin-top: 10px; }
.fila { display: flex; gap: 24px; padding: 20px 32px; border-top: 1px solid rgba(232,230,222,0.14); }
.cuadros { display: flex; gap: 8px; flex: none; width: 672px; }
.cuadro { width: 160px; flex: none; }
.cinco .cuadro { width: 128px; }
.cinco .lienzo { height: 228px; }
.lienzo { position: relative; width: 100%; height: 284px; border: 1.5px dashed rgba(232,230,222,0.45); border-radius: 6px;
  background: #16233F; padding: 50px 26px 76px 9px;  /* lo que dice va dentro de la zona segura (SEGURA) */ display: flex; flex-direction: column; justify-content: center; gap: 7px; overflow: hidden; }
.lienzo.claro { background: #E8E6DE; color: #16233F; border-color: rgba(22,35,63,0.5); }
.sello { position: absolute; top: 34px; left: 8px; font-size: 9px; color: #C9A45C; z-index: 2; }
.zona { position: absolute; background: repeating-linear-gradient(45deg, rgba(178,43,63,.16) 0 4px, transparent 4px 9px); pointer-events: none; }
.lienzo.claro .sello { color: #8a6a2a; }
.dice { font-family: "Instrument Serif", serif; font-size: 20px; line-height: 1.06; }
.dice.grande { font-size: 27px; }
.cinco .dice { font-size: 17px; }
.cinco .dice.grande { font-size: 21px; }
.dice .oro { color: #C9A45C; font-style: italic; }
.lienzo.claro .dice .oro { color: #8a6a2a; }
.toma { font-size: 12px; line-height: 1.25; color: #9AA3B5; border: 1px solid rgba(154,163,181,0.45); border-radius: 4px; padding: 5px; font-style: italic; }
.lienzo.claro .toma { color: #5b6476; }
.cuadro .t { font-size: 11px; opacity: 0.55; margin-top: 5px; }
.notas { flex: 1; min-width: 0; }
.linea { font-size: 14px; opacity: 0.75; display: flex; gap: 12px; flex-wrap: wrap; }
.linea .n { color: #C9A45C; opacity: 1; }
.titulo { font-family: "Instrument Serif", serif; font-size: 31px; line-height: 1.1; margin-top: 8px; }
.pasa { margin-top: 8px; font-size: 17px; line-height: 1.3; color: #C7CBD6; list-style: none; }
.pasa li { margin-bottom: 3px; }
.pasa li::before { content: "• "; color: #C9A45C; }
.etiq { margin-top: 8px; display: flex; gap: 8px; flex-wrap: wrap; font-size: 11px; }
.etiq span { border: 1px solid rgba(232,230,222,0.3); border-radius: 99px; padding: 3px 9px; }
.etiq .ins { border-color: #C9A45C; color: #C9A45C; }
.pie { padding: 16px 32px 22px; font-size: 13px; opacity: 0.5; display: flex; justify-content: space-between; border-top: 1px solid rgba(232,230,222,0.14); }
"""


def con_oro(texto, oro):
    """Escapa el texto y pinta de oro la palabra marcada (una por pantalla, ESTILO.md)."""
    t = html.escape(texto)
    if oro:
        o = html.escape(oro)
        t = t.replace(o, f'<span class="oro">{o}</span>', 1)
    return t


def cuadro(c, dia, claro):
    partes = []
    for b in c.get("bloques", []):
        if b.get("toma"):
            partes.append(f'<div class="toma">[{html.escape(b["toma"])}]</div>')
        else:
            # El texto largo se achica para que entre en la zona segura: si a este tamaño no entra, tampoco va a entrar en el video
            base = 27 if b.get("grande") else 20
            tam = base if len(b["dice"]) <= 34 else max(13, round(base * (34 / len(b["dice"])) ** 0.6, 1))
            partes.append(f'<div class="dice" style="font-size:{tam}px">{con_oro(b["dice"], b.get("oro"))}</div>')
    fondo = " claro" if c.get("claro", claro) else ""
    # Zonas que tapa TikTok (las mismas de marca/efectos/efectos.js, SEGURA, a la escala del boceto): rayadas en rojo
    zonas = ('<div class="zona" style="left:0;right:0;top:0;height:11.5%"></div>'
             '<div class="zona" style="left:0;right:0;bottom:0;height:26%"></div>'
             '<div class="zona" style="right:0;top:11.5%;bottom:26%;width:14.8%"></div>')
    return (f'<div class="cuadro"><div class="lienzo{fondo}">{zonas}<div class="sello mono">Día {dia} de 30</div>{"".join(partes)}</div>'
            f'<div class="t mono">{html.escape(c.get("t", ""))}</div></div>')


def fila(p, dia):
    cuadros = "".join(cuadro(c, dia, p.get("claro", False)) for c in p["cuadros"])
    pasa = "".join(f"<li>{html.escape(x)}</li>" for x in p.get("pasa", []))
    tipo = '<span class="ins">Insignia</span>' if p.get("insignia") else "<span>Volumen</span>"
    etiq = f'{tipo}<span>Paso: {html.escape(p["paso"])}</span><span>{html.escape(p["costo"])}</span>'
    if p.get("estado"):
        etiq += f'<span>{html.escape(p["estado"])}</span>'
    return f"""
<div class="fila">
  <div class="cuadros{' cinco' if len(p['cuadros']) > 4 else ''}">{cuadros}</div>
  <div class="notas">
    <div class="linea mono"><span class="n">{html.escape(p["codigo"])}</span><span>{html.escape(p["serie"])}</span><span>{html.escape(p["formato"])}</span></div>
    <div class="titulo">{html.escape(p["titulo"])}</div>
    <ul class="pasa">{pasa}</ul>
    <div class="etiq mono">{etiq}</div>
  </div>
</div>"""


def navegador():
    for ruta in (
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ):
        if Path(ruta).exists():
            return ruta
    return shutil.which("msedge") or shutil.which("chrome")


def recortar(png):
    """El alto de la ventana se calcula de más; se corta el fondo vacío de abajo."""
    from PIL import Image
    im = Image.open(png).convert("RGB")
    fondo = im.getpixel((im.width - 1, im.height - 1))
    y = im.height - 1
    while y > 0 and all(im.getpixel((x, y)) == fondo for x in range(0, im.width, 7)):
        y -= 1
    im.crop((0, 0, im.width, min(im.height, y + 24))).save(png)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("lote")
    ap.add_argument("--salida", required=True)
    a = ap.parse_args()

    d = json.loads(Path(a.lote).read_text(encoding="utf-8"))
    out = Path(a.salida)
    out.mkdir(parents=True, exist_ok=True)
    if (out / "fuentes").exists():
        shutil.rmtree(out / "fuentes")
    shutil.copytree(FUENTES, out / "fuentes")

    nav = navegador()
    total = len(d["dias"])
    for n, dia in enumerate(d["dias"], 1):
        filas = "".join(fila(p, dia["dia"]) for p in dia["piezas"])
        vol = sum(1 for p in dia["piezas"] if not p.get("insignia"))
        ins = len(dia["piezas"]) - vol
        meta = f'{vol} de volumen' + (f' · {ins} insignia' if ins else "") + f' · {dia["costo"]}'
        doc = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="barra mono"><span>{html.escape(d["titulo"])}</span><span>{html.escape(d["version"])}</span></div>
<div class="cabeza"><h1>Día {dia["dia"]} · {html.escape(dia["fecha"])}</h1><div class="meta mono">{html.escape(dia["nota"])} · {html.escape(meta)}</div></div>
{filas}
<div class="pie mono"><span>Guion gráfico barato: se aprueba antes de producir</span><span>{n} / {total}</span></div>
</body></html>"""
        h = out / f"dia-{dia['dia']}.html"
        h.write_text(doc, encoding="utf-8")
        if not nav:
            continue
        alto = 260 + 480 * len(dia["piezas"])
        png = (out / f"dia-{dia['dia']}.png").resolve()
        if png.exists():
            png.unlink()
        subprocess.run([nav, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size=1080,{alto}",
                        f"--screenshot={png}", h.resolve().as_uri()], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):  # el navegador escribe el PNG después de devolver el control
            if png.exists() and png.stat().st_size > 0:
                break
            time.sleep(0.5)
        recortar(png)
        webp = png.with_suffix(".webp")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(png), "-quality", "82", str(webp)], check=True)
        print("día", dia["dia"], "->", webp)
    if not nav:
        print("No encontré Edge ni Chrome: quedaron los .html en", out)


if __name__ == "__main__":
    main()
