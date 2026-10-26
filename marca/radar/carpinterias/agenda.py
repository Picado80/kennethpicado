"""La agenda del mes: qué se va a probar, en qué orden y por qué.

La agenda no se escribe a mano: sale del catálogo de carpinterías, ordenadas por
prioridad (nuestra señal primero) y repartidas según la mezcla de series de
`IDENTIDAD.md`.

La regla que manda: **primero lo que ya funcionó en nuestra cuenta.** Si una
carpintería tiene estado `funciono`, va antes que una que solo viralizó en el mundo.
Si no hay ninguna probada todavía, la agenda lo dice, en vez de fingir certeza.

Uso:
    from agenda import agenda, render
    plan = agenda(cargar())
    print(render(plan, "2026-11"))
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

import carpinterias as cp  # noqa: E402

# La mezcla de una semana normal: los tres diarios y La Oficina el domingo.
# `IDENTIDAD.md` §"Las series".
MEZCLA_SEMANAL = {
    1: "lo_probe_por_vos",     # lunes
    2: "un_truco_en_12_s",     # martes
    3: "la_ia_puede",          # miércoles
    4: "lo_probe_por_vos",     # jueves
    5: "un_truco_en_12_s",     # viernes
    6: "la_ia_puede",          # sábado
    0: "la_oficina",           # domingo
}

# Cuántas piezas de la misma serie caben en una semana, para no repetir más de lo debido.
# Los topes suman 7: una pieza por día, con La Oficina el domingo.
TOPES_SEMANA = {
    "lo_probe_por_vos": 2,
    "un_truco_en_12_s": 2,
    "la_ia_puede": 2,
    "la_oficina": 1,
    "costa_rica_en_anime": 1,
}

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def _estado_legible(estado: str) -> str:
    return {
        "funciono": "ya funcionó con nosotros",
        "en_prueba": "en prueba",
        "nuevo": "nunca se ha probado",
        "no_funciono": "ya falló con nosotros",
        "descartada": "descartada",
    }.get(estado, estado)


def agenda(catalogo: dict, inicio: date | None = None, dias: int = 30) -> list[dict]:
    """Arma el mes: una pieza por día, con su carpintería y el porqué.

    Cada serie tiene su tope semanal, y una misma carpintería no se repite dentro
    de la misma semana (para poder compararlas con calma).
    """
    inicio = inicio or date.today()
    candidatas = [c for c in cp.ordenar(catalogo) if cp.encaja(c)]
    if not candidatas:
        return []

    plan: list[dict] = []
    por_serie: dict[str, int] = {}
    usadas_en_semana: dict[int, set] = {}

    for n in range(dias):
        dia = inicio + timedelta(days=n)
        semana = dia.isocalendar()[1]
        usadas_en_semana.setdefault(semana, set())
        serie_del_dia = MEZCLA_SEMANAL.get(dia.weekday(), "lo_probe_por_vos")

        # Hasta el tope de la semana para esa serie.
        if por_serie.get(serie_del_dia, 0) >= TOPES_SEMANA.get(serie_del_dia, 1):
            # Ya se usó lo que tocaba de esa serie: se busca la siguiente serie libre.
            serie_del_dia = _siguiente_serie_libre(por_serie, dia)
            if serie_del_dia is None:
                continue

        elegida = _elegir(candidatas, serie_del_dia, usadas_en_semana[semana])
        if elegida is None:
            elegida = _elegir(candidatas, None, usadas_en_semana[semana])
        if elegida is None:
            continue

        usadas_en_semana[semana].add(elegida["id"])
        por_serie[serie_del_dia] = por_serie.get(serie_del_dia, 0) + 1
        plan.append({
            "fecha": dia.isoformat(),
            "dia": DIAS[dia.weekday()],
            "serie": serie_del_dia,
            "carpinteria": elegida["id"],
            "nombre": elegida.get("nombre", ""),
            "estado": elegida.get("estado", "nuevo"),
            "por_que": _por_que(elegida),
        })
    return plan


def _siguiente_serie_libre(por_serie: dict, dia: date) -> str | None:
    """La primera serie que todavía tiene cupo en la semana."""
    for serie, tope in TOPES_SEMANA.items():
        if por_serie.get(serie, 0) < tope:
            return serie
    return None


def _elegir(candidatas: list[dict], serie: str | None, usadas: set) -> dict | None:
    """La primera carpintería libre que calza con la serie (o cualquiera, si no hay)."""
    for c in candidatas:
        if c["id"] in usadas:
            continue
        if serie is None:
            return c
        if c.get("tropicalizacion", {}).get("serie") == serie:
            return c
    return None


def _por_que(carp: dict) -> str:
    """Por qué esta carpintería va hoy, en una frase."""
    n = carp.get("nuestro", {}).get("seguidores_por_1000")
    estado = carp.get("estado", "nuevo")
    if estado == "funciono" and n is not None:
        return f"ya funcionó con nosotros: {_entero(n)} seguidores por cada 1.000 vistas"
    if estado == "no_funciono":
        return "ya falló con nosotros: no la repetimos"
    if estado == "en_prueba":
        return "ya se está probando: repetimos con otro gancho"
    return f"nunca se ha probado con nosotros; en el mundo tiene {carp.get('original', {}).get('señal') or '?'} de señal"


def _entero(valor) -> str:
    """25.0 -> '25'; 25.5 -> '25.5'."""
    try:
        n = float(valor)
    except (TypeError, ValueError):
        return str(valor)
    return str(int(n)) if n == int(n) else str(n)


def render(plan: list[dict], mes: str) -> str:
    """La agenda en markdown, lista para leerse y para pegarse en el plan."""
    lineas = [f"# Agenda de carpinterías · {mes}", ""]
    if not plan:
        lineas.append("No hay carpinterías que encajen todavía. Hay que cerrar las del radar primero.")
        return "\n".join(lineas) + "\n"

    lineas.append(f"{len(plan)} piezas. Lo que ya funcionó con nosotros va primero.")
    lineas.append("")
    lineas.append("| Día | Fecha | Serie | Carpintería | Por qué |")
    lineas.append("|---|---|---|---|---|")
    for p in plan:
        lineas.append(f"| {p['dia']} | {p['fecha']} | {p['serie']} | **{p['carpinteria']}** {p['nombre']} | {p['por_que']} |")
    lineas.append("")
    return "\n".join(lineas) + "\n"
