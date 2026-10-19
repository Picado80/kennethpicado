"""Suma el registro de costos de la marca, marca lo que pasa el tope y saca el costo por seguidor nuevo.

Uso (desde la raíz de kennethpicado):
    python marca/scripts/costeo.py

Lee marca/costos/registro.csv y marca/medicion/registro.csv. No llama a ninguna API ni gasta nada.
La métrica que manda (ESTRATEGIA.md §8.5): el costo por seguidor nuevo de cada insignia.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

TOPE = 4.00            # una insignia cuesta de $2 a $4 (ESTRATEGIA.md §3)
MARCA = Path(__file__).resolve().parents[1]
REGISTRO = MARCA / "costos" / "registro.csv"
MEDICION = MARCA / "medicion" / "registro.csv"


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

    # costo por seguidor nuevo: lo que costó la pieza contra los seguidores que trajo (la medición más nueva de cada red)
    seguidores = defaultdict(dict)
    if MEDICION.exists():
        for m in csv.DictReader(MEDICION.open(encoding="utf-8")):
            if m.get("id") and (m.get("seguidores_nuevos") or "").strip():
                seguidores[m["id"]][m.get("plataforma") or "?"] = float(m["seguidores_nuevos"])
    print()
    print("Costo por seguidor nuevo (la métrica del lunes):")
    hay = False
    for video, v in sorted(por_video.items()):
        if v["produccion"] <= 0:
            continue
        s = sum(seguidores.get(video, {}).values())
        hay = hay or s > 0
        print(f"  {video:<10} ${v['produccion']:6.2f}  " + (f"{s:5.0f} seguidores nuevos  ${v['produccion'] / s:.3f} por seguidor" if s else "sin medir todavía"))
    if not hay:
        print("  Todavía no hay seguidores medidos en marca/medicion/registro.csv.")


if __name__ == "__main__":
    main()
