"""Le hace el mismo pedido a varios modelos de inteligencia artificial y guarda las respuestas reales («lo probé por vos»).

Uso (desde la raíz de kennethpicado):
    python marca/scripts/probar.py <carpeta> <clave> "<pedido>" [<clave> "<pedido>" ...]
Escribe <carpeta>/respuestas.json ({"<modelo>:<clave>": {pedido, texto, segundos, modelo, uso}}); lo que ya está no se
vuelve a pedir. Mismos modelos que el PR1 (MiniMax, Kimi, DeepSeek). Las llaves se leen de torre\\.env y de
~/.minimax_key, y nunca se imprimen.
"""
import json
import sys
from pathlib import Path

MARCA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MARCA / "produccion" / "dia2" / "pr1"))
from prueba import IAS, pedir  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 4 or len(sys.argv) % 2:
        sys.exit(__doc__)
    carpeta = Path(sys.argv[1]); carpeta.mkdir(parents=True, exist_ok=True)
    pedidos = list(zip(sys.argv[2::2], sys.argv[3::2]))
    salida = carpeta / "respuestas.json"
    res = json.loads(salida.read_text(encoding="utf-8")) if salida.exists() else {}
    for ia, (url, modelo, k) in IAS.items():
        for clave, texto in pedidos:
            c = f"{ia}:{clave}"
            if c in res:
                continue
            try:
                res[c] = {"pedido": texto, **pedir(url, modelo, k(), texto)}
            except Exception as e:  # un modelo caído no frena a los otros
                print(c, "falló:", str(e)[:160]); continue
            salida.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
            print(c, res[c]["segundos"], "s ·", res[c]["texto"][:300].replace("\n", " / "))
    return 0


if __name__ == "__main__":
    sys.exit(main())
