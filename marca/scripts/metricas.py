"""Trae de Buffer los números de cada publicación de la marca y los deja en una tabla.

Lee los envíos de cada día (marca/produccion/dia*/publicar.enviado.json), pide a Buffer el estado y las métricas de
cada publicación (vistas, alcance, reacciones, comentarios, compartidos, tiempo visto…) y escribe
marca/medicion/metricas-<fecha>.csv. También busca publicaciones de los canales que no estén en esos archivos (por
ejemplo, las que se suben a mano) en las fechas del reto.

Uso (desde la raíz de kennethpicado):  python marca/scripts/metricas.py [--desde 2026-10-21]
La llave (BUFFER_API_KEY) se lee de torre\\.env y nunca se imprime.
"""
import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path

MARCA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MARCA / "scripts"))
from publicar import CANALES, gql  # noqa: E402
from voz import llave  # noqa: E402

UNA = """query($id: PostId!) { post(input: { id: $id }) { id status dueAt sentAt externalLink text
  metrics { type value } } }"""


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--desde", default="2026-10-21")
    a = ap.parse_args()
    k = llave("BUFFER_API_KEY")
    filas, tipos = [], set()
    for env in sorted(MARCA.glob("produccion/dia*/publicar.enviado.json")):
        dia = env.parent.name
        for clave, v in json.loads(env.read_text(encoding="utf-8")).items():
            codigo, canal = clave.split(":")
            r = gql(k, UNA, {"id": v["id"]})
            if r.get("errors"):
                print(clave, "error:", r["errors"][0].get("message", "")[:200]); continue
            p = r["data"]["post"]
            m = {x["type"]: x["value"] for x in (p.get("metrics") or [])}
            tipos |= set(m)
            filas.append({"dia": dia, "codigo": codigo, "canal": canal, "estado": p["status"], "salio": p.get("sentAt") or p.get("dueAt"),
                          "link": p.get("externalLink") or "", **m})
    cols = ["dia", "codigo", "canal", "estado", "salio", "link"] + sorted(tipos)
    hoy = dt.date.today().isoformat()
    salida = MARCA / "medicion" / f"metricas-{hoy}.csv"
    with salida.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(filas)
    for f in filas:
        print(f["dia"], f["codigo"], f["canal"], f["estado"], f["salio"], {t: f.get(t) for t in sorted(tipos)})
    print("tabla:", salida)


if __name__ == "__main__":
    main()
