"""Arma los archivos del tablero «Reto 30 días · Vistas y seguidores» (https://claude.ai/artifact/M7uWMsSAm39KCW6bEGqKBg).

Lee la última tabla de Buffer (medicion/metricas-<fecha>.csv, de metricas.py), los títulos y duraciones
(medicion/piezas.json) y los seguidores (medicion/seguidores.csv); suma una medición a medicion/vistas-historial.csv y
escribe en medicion/tablero/: publicaciones.json, seguidores.json e historial.json. Después se suben al tablero.

Uso (desde la raíz de kennethpicado):  python marca/scripts/metricas.py && python marca/scripts/tablero.py
"""
import csv
import datetime as dt
import json
from pathlib import Path

MED = Path(__file__).resolve().parents[1] / "medicion"
CR = dt.timezone(dt.timedelta(hours=-6))
RED = {"tiktok": "TikTok", "instagram": "Instagram"}


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    tabla = sorted(MED.glob("metricas-*.csv"))[-1]
    piezas = json.loads((MED / "piezas.json").read_text(encoding="utf-8"))
    medido = dt.datetime.fromtimestamp(tabla.stat().st_mtime, CR).isoformat(timespec="minutes")
    pubs = []
    for f in csv.DictReader(tabla.open(encoding="utf-8")):
        if f["estado"] != "sent":
            continue
        salio = dt.datetime.fromisoformat(f["salio"].replace("Z", "+00:00")).astimezone(CR)
        p = piezas.get(f["codigo"], {})
        dur, prom = p.get("duracion_s"), num(f.get("averageTimeWatched"))
        pubs.append({
            "codigo": f["codigo"], "red": RED.get(f["canal"], f["canal"]), "dia": int(f["dia"].replace("dia", "")),
            "fecha": salio.date().isoformat(), "hora": salio.strftime("%H:%M"), "pieza": f"{f['codigo']} · {p.get('titulo', '')}",
            "duracion_s": dur, "vistas": int(num(f.get("views")) or 0), "prom_visto_s": prom,
            "visto": round(prom / dur, 3) if prom is not None and dur else None,
            "reacciones": int(num(f.get("reactions")) or 0), "comentarios": int(num(f.get("comments")) or 0),
            "compartidos": int(num(f.get("shares")) or 0), "guardados": int(num(f.get("saves")) or 0) if f.get("saves") else None,
            "medido": medido,
        })
    seg = [{"fecha": r["fecha"], "tiktok": int(r["tiktok"]), "instagram": int(r["instagram"]),
            "total": int(r["tiktok"]) + int(r["instagram"])} for r in csv.DictReader((MED / "seguidores.csv").open(encoding="utf-8"))]
    # una medición por red: el total de vistas acumuladas de todo lo publicado hasta ese momento
    hist_csv = MED / "vistas-historial.csv"
    filas = list(csv.DictReader(hist_csv.open(encoding="utf-8"))) if hist_csv.exists() else []
    filas = [r for r in filas if r["medido"] != medido]
    for red in ("TikTok", "Instagram"):
        mias = [p for p in pubs if p["red"] == red]
        filas.append({"medido": medido, "red": red, "vistas": str(sum(p["vistas"] for p in mias)), "publicaciones": str(len(mias))})
    with hist_csv.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, ["medido", "red", "vistas", "publicaciones"]); w.writeheader(); w.writerows(filas)
    hist = [{"medido": r["medido"], "red": r["red"], "vistas": int(r["vistas"]), "publicaciones": int(r["publicaciones"])} for r in filas]
    out = MED / "tablero"; out.mkdir(exist_ok=True)
    for nombre, datos in (("publicaciones", pubs), ("seguidores", seg), ("historial", hist)):
        (out / f"{nombre}.json").write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(pubs)} publicaciones, {len(seg)} mediciones de seguidores, {len(hist)} filas de historial · medido {medido}")


if __name__ == "__main__":
    main()
