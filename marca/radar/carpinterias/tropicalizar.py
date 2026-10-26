"""Las reglas de tropicalización: cómo un molde ajeno entra en la marca de Kenneth.

De dónde salen las reglas:
- `marca/IDENTIDAD.md` — el filtro de las 4 condiciones y las 4 series con su hilo.
- `marca/CANON.md` — lo que está fuera (vender, listas de herramientas, «14 años en Amazon»).
- `marca/CALIFICACION.md` — la vara: pasa con 87.

La tropicalización NO es un texto que se escribe solo: es un esqueleto con las
decisiones que hay que tomar y el rastro de cada cambio. Este módulo arma ese
esqueleto, evalúa las condiciones de forma mecánica y deja el digest con el original
al lado de nuestra versión, para que Kenneth pueda decir «esto quedó muy largo».

Lo que la máquina NO puede judge: si la tarea es realmente real o si la prueba con IA
fue real. Eso lo declara quien tropicaliza, y el módulo se lo marca como «a verificar».

Uso:
    from tropicalizar import condiciones, serie_sugerida, esqueleto, montar_digest
"""
from __future__ import annotations

import re

# Las 4 series con su hilo (IDENTIDAD.md §"Las series"). La hora es la de publicación.
SERIES = [
    {
        "id": "lo_probe_por_vos",
        "nombre": "Lo probé por vos",
        "hora": "12:00",
        "que_es": "Le doy un trabajo real a la inteligencia artificial, reviso lo que hizo y muestro qué corregí.",
        "cuando": "el molde tiene una TAREA real que se le puede dar a una IA y un resultado que se puede corregir",
        "palabras": ["pruebo", "tarea", "encargo", "trabajo", "corregi", "corregir",
                     "resultado", "asistente", "le pedi", "le pedí", "memoria"],
    },
    {
        "id": "un_truco_en_12_s",
        "nombre": "Un truco en 12 s",
        "hora": "19:00",
        "que_es": "Una forma de pedirle algo que podés usar hoy.",
        "cuando": "el molde es corto y da una forma de pedir algo que se usa hoy mismo",
        "palabras": ["truco", "tip", "forma de", "como pedir", "atajo", "en 12",
                     "atajito", "hack", "prompt"],
    },
    {
        "id": "la_ia_puede",
        "nombre": "¿La IA puede…?",
        "hora": "20:30",
        "que_es": "El examen: ¿se le puede confiar esto? Pasa o no pasa.",
        "cuando": "el molde es un EXAMEN: se prueba algo y se dice si pasó o no",
        "palabras": ["prueba", "examen", "pasa", "falla", "falso", "confiar", "verificar",
                     "estafa", "engaño", "puede", "detectar", "ciudadano"],
    },
    {
        "id": "la_oficina",
        "nombre": "La Oficina",
        "hora": "semanal",
        "que_es": "Detrás de cámaras de mi oficina de siete IAs: cómo las dirijo en mi trabajo de verdad.",
        "cuando": "el molde tiene arco de equipo, chisme de oficina o una contradicción de proceso",
        "palabras": ["oficina", "equipo", "empleado", "empleados", "jefe", "reunion",
                     "reunión", "cliente", "turno", "agente", "equipo", "reporte", "jefa"],
    },
    {
        "id": "costa_rica_en_anime",
        "nombre": "Costa Rica en anime",
        "hora": "sábados",
        "que_es": "Capítulo de «Lo probé por vos»: una imagen fiel a una foto real de acá.",
        "cuando": "el mouldo muestra un antes y un después visual de algo real de Costa Rica",
        "palabras": ["anime", "ilustracion", "ilustración", "dibujo", "estilo", "foto",
                     "imagen", "avatar", "retrato", "paisaje", "paisaje"],
    },
]

CONDICIONES = [
    ("tarea_real", "Una tarea real de la casa o del trabajo de un tico"),
    ("prueba_real_ia", "Una prueba real con inteligencia artificial, con el resultado guardado"),
    ("resultado_o_pregunta_3s", "El resultado o la pregunta antes del segundo 3"),
    ("regla_lider", "Una regla de líder al final"),
]

# Lo que un molde puede traer de más y estira nuestra versión.
ESTIRAMIENTOS = [
    ("dura_mas_30s", "dura más de 30 s", "nuestras piezas duran de 12 a 20 s (CALIFICACION.md)"),
    ("vende", "vende o anuncia algo", "no se vende en los videos (CANON.md)"),
    ("es_promo", "es una promoción o un giveaway", "no hay promos ni sorteos en la marca"),
    ("sin_regla", "no deja una regla de líder", "toda pieza cierra con la regla de líder (IDENTIDAD.md)"),
    ("ingles", "está en inglés", "en los videos no se habla en inglés (IDENTIDAD.md)"),
    ("cara_gratis", "usa una cara o voz de otra persona real", "solo el gemelo aprobado, con etiqueta de IA"),
]


# ---------------------------------------------------------------- formato

def numero(valor) -> str:
    """Número en formato costarricense: 412.000 y 8,1."""
    if valor is None:
        return "—"
    try:
        n = float(valor)
    except (TypeError, ValueError):
        return str(valor)
    if n != int(n):
        return f"{n:,.1f}".replace(",", " ").replace(".", ",").replace(" ", ".")
    return f"{int(n):,}".replace(",", ".")


def pct(valor) -> str:
    """0.081 -> '8,1%'."""
    if valor is None:
        return "—"
    try:
        return f"{float(valor) * 100:.1f}".replace(".", ",") + "%"
    except (TypeError, ValueError):
        return str(valor)


# ---------------------------------------------------------------- condiciones

def condiciones(carp: dict) -> list[dict]:
    """Evalúa las 4 condiciones de IDENTIDAD.md sobre la tropicalización.

    Cada una queda en 'cumple', 'falta' o 'a_verificar' (lo que una máquina no
    puede judge: que la tarea y la prueba sean de verdad).
    """
    trop = carp.get("tropicalizacion", {}) or {}
    salida = []

    tarea = str(trop.get("tarea_real") or "").strip()
    salida.append({
        "id": "tarea_real",
        "estado": "cumple" if tarea else "falta",
        "nota": tarea or "Falta decir qué tarea real de casa o trabajo le da carne.",
        "a_mano": False,
    })

    if trop.get("prueba_real_ia"):
        estado = "cumple" if trop.get("prueba_guardada") else "falta"
        nota = ("Prueba con IA declarada y resultado guardado."
                if estado == "cumple"
                else "La prueba con IA está, pero falta guardar el resultado.")
    else:
        estado = "falta"
        nota = "Falta la prueba real con inteligencia artificial."
    salida.append({
        "id": "prueba_real_ia",
        "estado": estado,
        "nota": nota,
        "a_mano": True,
    })

    tres = str(trop.get("resultado_o_pregunta_3s") or "").strip()
    salida.append({
        "id": "resultado_o_pregunta_3s",
        "estado": "cumple" if tres else "falta",
        "nota": tres or "Falta el resultado o la pregunta del segundo 0 al 3.",
        "a_mano": False,
    })

    regla = str(trop.get("regla_lider") or "").strip()
    salida.append({
        "id": "regla_lider",
        "estado": "cumple" if regla else "falta",
        "nota": regla or "Falta la regla de líder que cierra la pieza.",
        "a_mano": False,
    })
    return salida


def condiciones_pasan(carp: dict) -> bool:
    """True si las 4 condiciones quedan 'cumple'."""
    return all(c["estado"] == "cumple" for c in condiciones(carp))


# ---------------------------------------------------------------- series

def _texto(carp: dict) -> str:
    """Todo el texto del molde, en minúscula, para buscar pistas."""
    pedazo = [
        str(carp.get("original", {}).get("gancho_literal") or ""),
        str(carp.get("gramatica", {}).get("gancho_0_3s") or ""),
        str(carp.get("gramatica", {}).get("re_gancho") or ""),
        str(carp.get("gramatica", {}).get("cierre") or ""),
        " ".join(str(b) for b in carp.get("gramatica", {}).get("estructura") or []),
        " ".join(str(c) for c in carp.get("tropicalizacion", {}).get("cambios") or []),
    ]
    return " ".join(pedazo).lower()


def serie_sugerida(carp: dict, limite: int = 3) -> list[dict]:
    """Las series que mejor calzan con este molde, con el porqué.

    No decide: propone. Quien tropicaliza elige de acá y escribe el porqué en la ficha.
    """
    texto = _texto(carp)
    gramatica = carp.get("gramatica", {}) or {}
    duracion = carp.get("original", {}).get("duracion_s")
    cierre = str(gramatica.get("cierre") or "").lower()
    plano = str(gramatica.get("plano") or "").lower()
    tipo = str(gramatica.get("tipo_gancho") or "").lower()

    candidatos = []
    for serie in SERIES:
        puntos = 0.0
        porque = []
        for palabra in serie["palabras"]:
            if palabra in texto:
                puntos += 1.0
                porque.append(f"el molde habla de «{palabra}»")
        if serie["id"] == "un_truco_en_12_s":
            if isinstance(duracion, (int, float)) and duracion <= 12:
                puntos += 1.5
                porque.append(f"dura {duracion} s: cabe en 12 s")
        if serie["id"] == "la_oficina":
            if isinstance(duracion, (int, float)) and duracion >= 30:
                puntos += 1.0
                porque.append(f"dura {duracion} s: hay tiempo para el arco de oficina")
            if "pregunta" in cierre:
                puntos += 0.5
                porque.append("el cierre pregunta: es el mecanismo de La Oficina")
        if serie["id"] == "la_ia_puede":
            if "pregunta" in cierre or tipo == "pregunta":
                puntos += 0.5
                porque.append("el gancho es una pregunta: es el examen")
        if serie["id"] == "lo_probe_por_vos":
            if plano == "pantalla":
                puntos += 0.8
                porque.append("se ve una pantalla: hay una prueba que revisar")
        if serie["id"] == "costa_rica_en_anime":
            if plano in ("b_roll", "mixto"):
                puntos += 0.3
                porque.append("el molde es visual: cabe como antes/después")
        if puntos > 0:
            candidatos.append({
                "id": serie["id"], "nombre": serie["nombre"], "hora": serie["hora"],
                "que_es": serie["que_es"], "cuando": serie["cuando"],
                "puntos": puntos, "porque": porque[:3],
            })
    candidatos.sort(key=lambda c: c["puntos"], reverse=True)
    return candidatos[:limite]


# ---------------------------------------------------------------- esqueleto

def esqueleto(carp: dict) -> list[dict]:
    """Las decisiones que hay que tomar para tropicalizar este molde.

    Cada fila trae lo que trae el original, para que la decisión se tome al lado
    de la referencia y no de memoria.
    """
    g = carp.get("gramatica", {}) or {}
    o = carp.get("original", {}) or {}
    return [
        {"dimension": "Gancho (0 a 3 s)", "original": g.get("gancho_0_3s") or o.get("gancho_literal") or "",
         "decidir": "La situación o la contradicción, sin contexto y sin anunciar el tema."},
        {"dimension": "Re-gancho", "original": f"a los {g.get('re_gancho_s')} s: {g.get('re_gancho') or '—'}",
         "decidir": "Qué cambia entre el segundo 3 y 4 para que no se vaya la gente."},
        {"dimension": "Estructura", "original": " · ".join(str(b) for b in g.get("estructura") or []) or "—",
         "decidir": "Los mismos bloques, con nuestra historia de carne."},
        {"dimension": "Duración", "original": f"{o.get('duracion_s')} s (banda {g.get('banda_duracion') or '—'})",
         "decidir": "De 12 a 20 s. Si el molde es más largo, hay que recortar y avisarlo."},
        {"dimension": "Cierre", "original": g.get("cierre") or "—",
         "decidir": "Pregunta, compartilo o remate. La regla de líder va al final, siempre."},
        {"dimension": "Planos", "original": g.get("plano") or "—",
         "decidir": "No repetir la forma del gemelo de la pieza anterior (efectos/USO.md)."},
        {"dimension": "Subtítulos", "original": g.get("subtitulos") or "—",
         "decidir": "Palabra por palabra, con la firma de la marca."},
        {"dimension": "Sonido", "original": g.get("sonido") or "—",
         "decidir": "El de la casa, si el sonido en tendencia no es lo nuestro."},
    ]


def estiramientos(carp: dict) -> list[str]:
    """Las cosas del molde que quedan estiradas si lo copiamos tal cual."""
    avisos = []
    texto = _texto(carp)
    duracion = carp.get("original", {}).get("duracion_s")
    if isinstance(duracion, (int, float)) and duracion > 30:
        avisos.append(f"Dura {duracion} s y nuestras piezas duran de 12 a 20 s: hay que recortar.")
    for clave, que, porque in ESTIRAMIENTOS:
        if clave == "dura_mas_30s":
            continue
        if clave == "ingles" and re.search(r"\b(the|and|with|this|your)\b", texto):
            avisos.append(f"{que}: {porque}.")
        elif clave == "vende" and re.search(r"\b(compra|descuento|precio|link en bio|patrocinado)\b", texto):
            avisos.append(f"{que}: {porque}.")
        elif clave == "es_promo" and re.search(r"\b(sorteo|giveaway|regalo|gana)\b", texto):
            avisos.append(f"{que}: {porque}.")
        elif clave == "sin_regla" and not (carp.get("tropicalizacion", {}) or {}).get("regla_lider"):
            avisos.append(f"{que}: {porque}.")
        elif clave == "cara_gratis" and re.search(r"\b(ceo|famoso|celebridad|actor|modelo)\b", texto):
            avisos.append(f"{que}: {porque}.")
    return avisos


# ---------------------------------------------------------------- digest

def _bloque(carp: dict) -> list[str]:
    """Una carpintería en el digest: el original y cómo lo tropicalizamos."""
    o = carp.get("original", {}) or {}
    g = carp.get("gramatica", {}) or {}
    t = carp.get("tropicalizacion", {}) or {}
    lineas = []

    lineas.append(f"### {carp.get('id')} · {carp.get('nombre')}")
    lineas.append("")
    lineas.append(f"**Original** — {o.get('cuenta') or '?'} · {o.get('red') or '?'} · "
                  f"{numero(o.get('vistas'))} vistas · {pct(o.get('señal'))} {o.get('señal_tipo') or 'señal'} · "
                  f"{o.get('duracion_s') or '?'} s")
    if o.get("url"):
        lineas.append(f"<{o['url']}>")
    if o.get("gancho_literal"):
        lineas.append(f"Empieza así: «{o['gancho_literal']}»")
    cuadros = o.get("cuadros") or []
    if cuadros:
        lineas.append(f"Cuadros: {len(cuadros)} (locales, en `marca/radar/salidas/`)")
    lineas.append("")
    lineas.append(f"**Cómo lo tropicalizamos** — {t.get('serie') or 'sin serie'}"
                  + (f" · «{t['pieza']}»" if t.get("pieza") else ""))
    cambios = t.get("cambios") or []
    if cambios:
        lineas.append("")
        lineas.append("| | Original | Nuestro | Por qué |")
        lineas.append("|---|---|---|---|")
        for c in cambios:
            lineas.append(f"| {c.get('que', '')} | {c.get('original', '')} | {c.get('nuestro', '')} | {c.get('porque', '')} |")
    lineas.append("")
    if t.get("tarea_real"):
        lineas.append(f"- **Tarea real:** {t['tarea_real']}")
    if t.get("resultado_o_pregunta_3s"):
        lineas.append(f"- **En el segundo 0 al 3:** {t['resultado_o_pregunta_3s']}")
    if t.get("regla_lider"):
        lineas.append(f"- **Regla de líder:** {t['regla_lider']}")
    avisos = list(t.get("avisos") or []) + estiramientos(carp)
    if avisos:
        lineas.append(f"- **Avisos:** {' '.join(avisos)}")
    lineas.append("")
    return lineas


def montar_digest(carpinterias: list[dict], fecha: str, top: int = 3) -> str:
    """El digest de las carpinterías del día: el original al lado de nuestra versión.

    Es lo que Kenneth lee. Corto: las 3 de arriba en detalle, las demás en una línea.
    """
    lineas = [f"# Carpinterías · {fecha}", ""]
    if not carpinterias:
        lineas.append("Hoy no salió ninguna carpintería que pase el filtro.")
        return "\n".join(lineas) + "\n"

    lineas.append(f"{len(carpinterias)} carpinterías. El original de cada una y cómo lo tropicalizamos.")
    lineas.append("")
    lineas.append("## Las 3 para probar")
    lineas.append("")
    for i, c in enumerate(carpinterias[:top], 1):
        o = c.get("original", {}) or {}
        t = c.get("tropicalizacion", {}) or {}
        lineas.append(f"{i}. **{c.get('nombre')}** — {t.get('serie') or 'sin serie'} · "
                      f"{numero(o.get('vistas'))} vistas · {o.get('duracion_s') or '?'} s · "
                      f"{o.get('cuenta') or '?'}")
        if o.get("url"):
            lineas.append(f"   Original: <{o['url']}>")
    lineas.append("")

    for c in carpinterias:
        lineas += _bloque(c)
    return "\n".join(lineas).rstrip() + "\n"
