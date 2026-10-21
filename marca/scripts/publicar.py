"""Programa en Buffer las piezas aprobadas de un día (E003). Por omisión NO publica nada: muestra lo que haría.

Uso (desde la raíz de kennethpicado):
    python marca/scripts/publicar.py marca/produccion/dia1/publicar.json            # muestra el plan
    python marca/scripts/publicar.py marca/produccion/dia1/publicar.json --enviar   # sube y programa (con el sí de Kenneth)

El plan es una lista de piezas: {"codigo", "canales": ["tiktok", "instagram"], "archivo", "tipo": "video"|"imagen",
"texto", "cuando": "2026-10-21T19:00:00-06:00", "ia": true|false, "instagram_tipo": "reel"|"post"}.
Buffer necesita una dirección pública para cada archivo: se suben como adjuntos de una «release» del repo público
(Picado80/kennethpicado), que no entran al historial de git. La etiqueta de IA de TikTok e Instagram va con «ia».
La llave (BUFFER_API_KEY) se lee de torre\\.env y nunca se imprime.
"""
import argparse
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

MARCA = Path(__file__).resolve().parents[1]
RAIZ = MARCA.parent
sys.path.insert(0, str(MARCA / "scripts"))
from voz import llave  # noqa: E402

REPO = "Picado80/kennethpicado"
CANALES = {"tiktok": "6ac6ebce6a5c39ccb649c4a2", "instagram": "6ac6eeeb6a5c39ccb649eae1"}   # Buffer, verificado el 19-oct

CREAR = """mutation($input: CreatePostInput!) { createPost(input: $input) {
  ... on PostActionSuccess { post { id status dueAt } }
  ... on NotFoundError { message } ... on UnauthorizedError { message } ... on UnexpectedError { message }
  ... on RestProxyError { message } ... on LimitReachedError { message } ... on InvalidInputError { message } } }"""


def gql(k, query, variables):
    req = urllib.request.Request("https://api.buffer.com", json.dumps({"query": query, "variables": variables}).encode(),
                                 {"Authorization": "Bearer " + k, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def subir(etiqueta, archivos):
    """Sube los archivos a la release <etiqueta> del repo público y devuelve sus direcciones."""
    existe = subprocess.run(["gh", "release", "view", etiqueta, "--repo", REPO], capture_output=True).returncode == 0
    if not existe:
        subprocess.run(["gh", "release", "create", etiqueta, "--repo", REPO, "--title", f"Contenido {etiqueta}",
                        "--notes", "Archivos de las publicaciones de la marca (los usa Buffer para publicar)."], check=True)
    subprocess.run(["gh", "release", "upload", etiqueta, "--repo", REPO, "--clobber", *map(str, archivos)], check=True)
    return {a.name: f"https://github.com/{REPO}/releases/download/{etiqueta}/{a.name}" for a in archivos}


def entrada(p, canal, url):
    tipo = "video" if p["tipo"] == "video" else "image"
    meta = {}
    if canal == "tiktok":
        meta["tiktok"] = {"isAiGenerated": bool(p.get("ia"))}
    else:
        meta["instagram"] = {"isAiGenerated": bool(p.get("ia")), "type": p.get("instagram_tipo", "reel" if tipo == "video" else "post"),
                             "shouldShareToFeed": True}
    return {"channelId": CANALES[canal], "text": p["texto"], "schedulingType": "automatic", "mode": "customScheduled",
            "dueAt": p["cuando"], "assets": [{tipo: {"url": url}}], "metadata": meta, "aiAssisted": bool(p.get("ia"))}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--enviar", action="store_true")
    a = ap.parse_args()
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    piezas = plan["piezas"]
    archivos = [RAIZ / p["archivo"] for p in piezas]
    for f in archivos:
        assert f.exists(), f"falta {f}"
    for p in piezas:
        print(f"{p['codigo']:<5} {p['cuando']}  {', '.join(p['canales']):<18} {p['tipo']:<6} IA:{'sí' if p.get('ia') else 'no'}  {p['archivo']}")
        print(f"      «{p['texto'][:110]}»")
    if not a.enviar:
        print("\nNo se envió nada. Con --enviar se sube y se programa.")
        return 0
    urls = subir(plan["etiqueta"], archivos)
    k = llave("BUFFER_API_KEY")
    for p, f in zip(piezas, archivos):
        for canal in p["canales"]:
            r = gql(k, CREAR, {"input": entrada(p, canal, urls[f.name])})
            res = (r.get("data") or {}).get("createPost") or r
            print(p["codigo"], canal, "->", res.get("post") or res.get("message") or r.get("errors"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
