"""Suma el registro de costos de la marca y marca los videos que pasan el tope.

Uso (desde la raíz de kennethpicado):
    python marca/scripts/costeo.py

Lee marca/costos/registro.csv. No llama a ninguna API ni gasta nada.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

TOPE = 3.00
REGISTRO = Path(__file__).resolve().parents[1] / "costos" / "registro.csv"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    filas = list(csv.DictReader(REGISTRO.open(encoding="utf-8")))
    por_video = defaultdict(lambda: {"produccion": 0.0, "prueba": 0.0, "piezas": defaultdict(float)})
    for f in filas:
        costo = float(f["costo_usd"] or 0)
        v = por_video[f["video"]]
        v[f["tipo"]] += costo
        if f["tipo"] == "produccion":
            v["piezas"][f["pieza"]] += costo
    for video, v in sorted(por_video.items()):
        estado = "PASA EL TOPE" if v["produccion"] > TOPE else "ok"
        print(f"\n{video}: producción ${v['produccion']:.2f} ({estado}, tope ${TOPE:.2f}) · pruebas ${v['prueba']:.2f}")
        total = v["produccion"] or 1
        for pieza, c in sorted(v["piezas"].items(), key=lambda x: -x[1]):
            print(f"  {pieza:<28} ${c:6.2f}  {100 * c / total:5.1f} %")


if __name__ == "__main__":
    main()
