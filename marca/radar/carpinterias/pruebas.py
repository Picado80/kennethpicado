"""El motor de las pruebas reales con IA. Reusable: el mismo todos los días.

Cada prueba le da a una IA una TAREA REAL (de la casa o del trabajo de Kenneth) y
guarda la respuesta tal cual. La salida es la evidencia de que la prueba existe y
de que quedó guardada; también es el material crudo de la pieza.

**Por qué es un motor y no un script por día:** el 26-oct el agente dejó un
`pruebas_2026-10-26.py`. Mañana habría un `pruebas_2026-10-27.py`, y en un mes
treinta archivos que nobody va a leer. Las TASAS van en un JSON; el motor es uno solo.

Uso:
    # 1. el agente escribe las tareas del día
    #    marca/radar/carpinterias/pruebas/AAAA-MM-DD/tareas.json
    # 2. se corren
    python marca/radar/carpinterias/pruebas.py --fecha 2026-10-27

El JSON de tareas es un objeto: clave -> tarea.
```json
{
  "C-001": {
    "titulo": "El WhatsApp al casero por la gotera",
    "serie": "¿La IA puede…?",
    "tarea": "Escribi un mensaje de WhatsApp para mandarle al dueño de la casa…",
    "por_que": "El molde es una carambada: le pedís una cosa y te dan otra."
  }
}
```

La llave de la API se lee del entorno (`MINIMAX_API_KEY`). Si no está, no se
prueba: se avisa y se sigue. Nunca se inventa una respuesta.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PRUEBAS = AQUI / "pruebas"

URL = "https://api.minimax.io/v1/chat/completions"
MODELOS = ("MiniMax-M3", "MiniMax-M2.7")

# MiniMax-M3 gasta tokens en razonar antes de responder: con muy pocos, la
# respuesta llega VACÍA (pasó el 26-oct con 700). 2.500 deja responder.
MAX_TOKENS = 2500


def quitar_pensamiento(texto: str) -> str:
    """Saca el bloque de razonamiento que devuelve el modelo."""
    limpio = re.sub(r"<think>.*?</think>", "", texto, flags=re.DOTALL)
    limpio = re.sub(r"^<think>.*", "", limpio, flags=re.DOTALL)
    return limpio.strip()


def llamar(tarea: str, max_tokens: int = MAX_TOKENS) -> tuple[str, str, str]:
    """(texto limpio, json crudo, modelo que respondió).

    Si nada sale, el texto trae el motivo entre corchetes y el json crudo viene
    vacío: la prueba queda marcada como NO HECHA, nunca como respuesta.
    """
    llave = os.environ.get("MINIMAX_API_KEY", "")
    if not llave:
        raise SystemExit("No esta MINIMAX_API_KEY en el entorno: no se puede probar.")
    ultimo = ""
    for modelo in MODELOS:
        cuerpo = {
            "model": modelo,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": tarea}],
        }
        req = urllib.request.Request(
            URL, data=json.dumps(cuerpo).encode("utf-8"),
            headers={"Authorization": f"Bearer {llave}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                bruto = r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            ultimo = (f"[NO SE PUDO HACER LA PRUEBA] HTTP {e.code}: "
                      f"{e.read().decode('utf-8', 'replace')[:200]}")
            continue
        except Exception as e:
            ultimo = f"[NO SE PUDO HACER LA PRUEBA] {type(e).__name__}: {e}"
            continue
        try:
            datos = json.loads(bruto)
        except json.JSONDecodeError:
            ultimo = "[NO SE PUDO HACER LA PRUEBA] respuesta que no es JSON"
            continue
        texto = (datos.get("choices") or [{}])[0].get("message", {}).get("content", "")
        if not texto:
            ultimo = "[RESPUESTA VACIA: el modelo gasto todos los tokens razonando]"
            continue
        return quitar_pensamiento(texto), bruto, modelo
    return ultimo, "", MODELOS[0]


def correr(fecha: str, tareas: dict, destino: Path, max_tokens: int = MAX_TOKENS) -> list[dict]:
    """Corre las pruebas de un día. Devuelve un resumen de lo que pasó."""
    destino.mkdir(parents=True, exist_ok=True)
    raw = destino / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    resumen = []
    for clave, p in tareas.items():
        if clave.startswith("_"):
            # Las claves con guion bajo son notas del archivo, no tareas.
            continue
        if not p.get("tarea"):
            print(f"--- {clave}: sin tarea, se salta ---", flush=True)
            continue
        print(f"--- {clave}: {p.get('titulo', '')} ---", flush=True)
        texto, bruto, modelo = llamar(p["tarea"], max_tokens=max_tokens)
        if bruto:
            (raw / f"{clave}.json").write_text(bruto, encoding="utf-8")
        cuerpo = [
            f"# Prueba real · {clave} · {p.get('titulo', '')}",
            "",
            f"- **Serie:** {p.get('serie', '')}",
            f"- **Modelo:** {modelo}",
            f"- **Fecha:** {fecha}",
            f"- **Por qué esta prueba:** {p.get('por_que', '')}",
            f"- **Respuesta cruda (JSON):** `raw/{clave}.json`",
            "",
            "## Lo que le pedí (la tarea real)",
            "",
            "```",
            p["tarea"],
            "```",
            "",
            "## Lo que me respondió (guardado tal cual, sin el razonamiento del modelo)",
            "",
            "```",
            texto,
            "```",
            "",
        ]
        (destino / f"{clave}.md").write_text("\n".join(cuerpo), encoding="utf-8")
        hecha = bool(bruto)
        resumen.append({"clave": clave, "hecha": hecha, "modelo": modelo,
                        "chars": len(texto), "nota": "" if hecha else texto[:120]})
        print(f"    -> {clave}.md ({len(texto)} chars, modelo {modelo}, "
              f"{'OK' if hecha else 'NO SE PUDO'})", flush=True)
    return resumen


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Corre las pruebas reales con IA del dia")
    p.add_argument("--fecha", default=date.today().isoformat(),
                   help="AAAA-MM-DD. Por defecto, hoy.")
    p.add_argument("--tareas", type=Path, default=None,
                   help="El JSON de tareas. Por defecto, pruebas/<fecha>/tareas.json")
    p.add_argument("--max-tokens", type=int, default=MAX_TOKENS)
    a = p.parse_args(argv)

    ruta = a.tareas or (PRUEBAS / a.fecha / "tareas.json")
    if not ruta.exists():
        print(f"No encuentro {ruta}.", flush=True)
        return 2
    tareas = json.loads(ruta.read_text(encoding="utf-8"))
    destino = PRUEBAS / a.fecha

    resumen = correr(a.fecha, tareas, destino, max_tokens=a.max_tokens)
    (destino / "resumen.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if all(r["hecha"] for r in resumen) else 1


if __name__ == "__main__":
    raise SystemExit(main())
