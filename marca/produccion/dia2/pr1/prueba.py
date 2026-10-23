"""PR1 · la prueba real: el mismo pedido a 3 IAs de la oficina, primero vago y después completo.

Lo que contestan se guarda tal cual en respuestas.json; el video cuenta lo que salió, no lo que se esperaba.
Usa las APIs compatibles con Anthropic de MiniMax (plan fijo), Kimi y DeepSeek: menos de un centavo en total.
Las llaves se leen de torre\\.env y de ~/.minimax_key, y nunca se imprimen.

Uso (desde la raíz de kennethpicado):  python marca/produccion/dia2/pr1/prueba.py
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[2] / "scripts"))
from voz import llave  # noqa: E402

IAS = {
    "MiniMax": ("https://api.minimax.io/anthropic/v1/messages", "MiniMax-M3", lambda: (Path.home() / ".minimax_key").read_text(encoding="utf-8").strip()),
    "Kimi": ("https://api.moonshot.ai/anthropic/v1/messages", "kimi-k3", lambda: llave("KIMI_API_KEY")),
    "DeepSeek": ("https://api.deepseek.com/anthropic/v1/messages", "deepseek-flash", lambda: llave("DEEPSEEK_API_KEY")),
}
# El completo lleva lo del J1: para quién, qué dice y para cuándo
PEDIDOS = {
    "vago": "Haceme un menú.",
    "completo": ("Tengo una soda en San José, Costa Rica. Haceme el menú del almuerzo de la semana que viene: un casado distinto "
                 "para cada día, de lunes a viernes, para la gente que trabaja en las oficinas de enfrente. Ningún plato puede "
                 "pasar de 3.500 colones y tiene que salir en menos de 5 minutos. Ponelo listo para escribirlo en la pizarra."),
}


def pedir(url, modelo, k, texto):
    cuerpo = {"model": modelo, "max_tokens": 16000, "messages": [{"role": "user", "content": texto}]}
    req = urllib.request.Request(url, json.dumps(cuerpo).encode(), {"x-api-key": k, "anthropic-version": "2023-06-01",
                                                                     "content-type": "application/json"})
    t = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=300))
    texto = "".join(b.get("text", "") for b in r.get("content", []) if b.get("type") == "text")
    return {"texto": texto, "segundos": round(time.time() - t, 1), "modelo": r.get("model"), "uso": r.get("usage")}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    salida = AQUI / "respuestas.json"
    res = json.loads(salida.read_text(encoding="utf-8")) if salida.exists() else {}
    for ia, (url, modelo, k) in IAS.items():
        for tipo, texto in PEDIDOS.items():
            clave = f"{ia}:{tipo}"
            if clave in res:
                continue
            res[clave] = {"pedido": texto, **pedir(url, modelo, k(), texto)}
            salida.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
            print(clave, res[clave]["segundos"], "s", len(res[clave]["texto"]), "caracteres")
    return 0


if __name__ == "__main__":
    sys.exit(main())
