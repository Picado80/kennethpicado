"""Arma el guion gráfico de un video: una fila por tramo, con sus cuadros y sus notas.

Es lo que Kenneth aprueba ANTES de gastar en el gemelo (marca/ESTILO.md).

Uso (desde la raíz de kennethpicado):
    python marca/scripts/storyboard.py marca/produccion/002/tramos-v4.json \
        --video marca/salidas/002-final-v4.mp4 --salida marca/salidas/guion-grafico-002-v4

--video es el render (o el borrador con una foto fija de Kenneth en vez del gemelo).
El JSON puede traer "acento": el nombre de la fila del color que resalta (por omisión, "Oro").
Saca los cuadros con ffmpeg y las páginas en PNG con Edge o Chrome sin ventana.
No llama a ninguna API ni gasta nada.
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
POR_PAGINA = 5
ALTO_FILA = 372
ALTO_CABEZA = 250

CSS = """
@font-face { font-family: "Instrument Serif"; font-style: normal; src: url("fuentes/instrument-serif-latin-400-normal.woff2") format("woff2"); }
@font-face { font-family: "Instrument Serif"; font-style: italic; src: url("fuentes/instrument-serif-latin-400-italic.woff2") format("woff2"); }
@font-face { font-family: "Archivo"; font-weight: 600; src: url("fuentes/archivo-latin-600-normal.woff2") format("woff2"); }
@font-face { font-family: "JetBrains Mono"; font-weight: 500; src: url("fuentes/jetbrains-mono-latin-500-normal.woff2") format("woff2"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { width: 1080px; background: #101B33; color: #E8E6DE; font-family: "Archivo", sans-serif; font-weight: 600; }
.mono { font-family: "JetBrains Mono", monospace; font-weight: 500; text-transform: uppercase; letter-spacing: 0.14em; }
.barra { background: #E8E6DE; color: #16233F; display: flex; justify-content: space-between; padding: 18px 32px; font-size: 20px; }
.cabeza { height: 178px; padding: 26px 32px 0; }
.cabeza h1 { font-family: "Instrument Serif", serif; font-weight: 400; font-size: 52px; line-height: 1.05; }
.cabeza .meta { font-size: 17px; opacity: 0.6; margin-top: 14px; }
.fila { height: 372px; display: flex; gap: 28px; padding: 26px 32px; background: #16233F; border-top: 1px solid rgba(232,230,222,0.14); overflow: hidden; }
.cuadros { display: flex; gap: 12px; flex: none; }
.cuadro img { display: block; width: 160px; height: 284px; object-fit: cover; border: 1px solid rgba(232,230,222,0.2); }
.cuadro .t { font-size: 14px; opacity: 0.55; margin-top: 8px; }
.notas { flex: 1; min-width: 0; }
.linea { font-size: 17px; opacity: 0.75; display: flex; gap: 18px; flex-wrap: wrap; }
.linea .n { color: #C9A45C; opacity: 1; }
.cita { font-family: "Instrument Serif", serif; font-style: italic; font-weight: 400; font-size: 36px; line-height: 1.1; margin-top: 12px; }
.pasa { margin-top: 12px; font-size: 21px; line-height: 1.3; color: #C7CBD6; list-style: none; }
.pasa li::before { content: "• "; color: #C9A45C; }
.etiquetas { margin-top: 14px; display: grid; grid-template-columns: 110px 1fr; row-gap: 5px; font-size: 19px; }
.etiquetas .k { font-size: 14px; opacity: 0.5; padding-top: 4px; }
.etiquetas .oro { color: #C9A45C; }
.pie { padding: 16px 32px; font-size: 15px; opacity: 0.5; display: flex; justify-content: space-between; }
"""


def tiempo(s):
    return f"{int(s // 60)}:{s % 60:04.1f}"


def navegador():
    for ruta in (
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ):
        if Path(ruta).exists():
            return ruta
    return shutil.which("msedge") or shutil.which("chrome")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("tramos")
    ap.add_argument("--video", required=True)
    ap.add_argument("--salida", required=True)
    a = ap.parse_args()

    d = json.loads(Path(a.tramos).read_text(encoding="utf-8"))
    out = Path(a.salida)
    (out / "cuadros").mkdir(parents=True, exist_ok=True)
    if (out / "fuentes").exists():
        shutil.rmtree(out / "fuentes")
    shutil.copytree(FUENTES, out / "fuentes")

    filas = []
    for i, t in enumerate(d["tramos"], 1):
        dur = t["fin"] - t["ini"]
        # Cuadros hacia el final de cada tramo: ahí ya entraron los textos
        momentos = [t["ini"] + dur * 0.7] if dur < 2.2 else [t["ini"] + dur * 0.45, t["fin"] - 0.2]
        cuadros = ""
        for j, m in enumerate(momentos):
            jpg = out / "cuadros" / f"{i:02d}-{j}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{m:.2f}", "-i", a.video, "-frames:v", "1",
                            "-vf", "scale=320:568", str(jpg)], check=True)
            cuadros += f'<div class="cuadro"><img src="cuadros/{jpg.name}"><div class="t mono">{tiempo(m)}</div></div>'
        pasa = "".join(f"<li>{html.escape(p)}</li>" for p in t["pasa"])
        filas.append(f"""
<div class="fila">
  <div class="cuadros">{cuadros}</div>
  <div class="notas">
    <div class="linea mono"><span class="n">{i:02d}</span><span>{tiempo(t["ini"])}–{tiempo(t["fin"])}</span><span>{dur:.1f} s</span><span>▣ {html.escape(t["toma"])}</span></div>
    <div class="cita">«{html.escape(t["cita"])}»</div>
    <ul class="pasa">{pasa}</ul>
    <div class="etiquetas">
      <div class="k mono">Énfasis</div><div>{html.escape(t["enfasis"])}</div>
      <div class="k mono">{html.escape(d.get("acento", "Oro"))}</div><div class="oro">{html.escape(t["oro"])}</div>
      <div class="k mono">Sonido</div><div>{html.escape(t["sonido"])}</div>
    </div>
  </div>
</div>""")

    paginas = [filas[i:i + POR_PAGINA] for i in range(0, len(filas), POR_PAGINA)]
    nav = navegador()
    for n, pag in enumerate(paginas, 1):
        meta = f'Estilo {d["estilo"]} · Kenneth en pantalla {d["kenneth_s"]} s · Costo ${d["costo_usd"]:.2f}'
        doc = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="barra mono"><span>{html.escape(d["serie"])}</span><span>{d["version"]} · {len(filas)} tramos</span></div>
<div class="cabeza"><h1>{html.escape(d["titulo"])}</h1><div class="meta mono">{html.escape(meta)}</div></div>
{"".join(pag)}
<div class="pie mono"><span>Guion gráfico: se aprueba antes de producir</span><span>{n} / {len(paginas)}</span></div>
</body></html>"""
        h = out / f"pagina-{n}.html"
        h.write_text(doc, encoding="utf-8")
        if nav:
            alto = ALTO_CABEZA + len(pag) * ALTO_FILA + 60
            png = (out / f"pagina-{n}.png").resolve()
            subprocess.run([nav, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size=1080,{alto}",
                            f"--screenshot={png}", h.resolve().as_uri()], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for _ in range(60):  # el navegador escribe el PNG después de devolver el control
                if png.exists() and png.stat().st_size > 0:
                    break
                time.sleep(0.5)
            print("página", n, "->", png)
    if not nav:
        print("No encontré Edge ni Chrome: quedaron los .html en", out)


if __name__ == "__main__":
    main()
