"""El catálogo de carpinterías: alta, edición, validación y orden.

Una carpintería es el molde de un formato viral, con ficha: qué se vio, cómo está
armado, cómo lo tropicalizamos a la marca de Kenneth y qué dio en NUESTRA cuenta.
La definición completa está en `CARPINTERIA.md`.

Lo que manda en el orden es nuestra señal, no la global: una carpintería que funcionó
en la cuenta vale más que una que solo viralizó en el mundo (ESTRATEGIA.md §1).

Uso:
    from carpinterias import cargar, guardar, agregar, ordenar
    cat = cargar()
    agregar(nueva_carpinteria(), cat)
    guardar(cat)
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CATALOGO = AQUI / "catalogo.json"

ESTADOS = ("nuevo", "en_prueba", "funciono", "no_funciono", "descartada")

# Cuánto pesa cada estado en el orden del catálogo.
BONO_ESTADO = {
    "funciono": 1.0,
    "en_prueba": 0.4,
    "nuevo": 0.0,
    "no_funciono": -1.5,
    "descartada": -999.0,
}

# Seguidores por cada 1.000 vistas que valen "1.0" de señal nuestra.
# 30 por mil es una pieza buena en la fase 1 (meta de 10.000 seguidores en 30 días).
REFERENCIA_SEGUIDORES = 30.0

RE_ID = re.compile(r"^C-(\d{3,})$")
RE_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")

CAMPOS_OBLIGATORIOS_ORIGINAL = ("url", "cuenta", "fecha")
CAMPOS_OBLIGATORIOS_GRAMATICA = ("tipo_gancho", "estructura")
CAMPOS_OBLIGATORIOS_CAMBIO = ("que", "original", "nuestro", "porque")


# ---------------------------------------------------------------- datos base

def catalogo_vacio() -> dict:
    """Un catálogo nuevo, con su nota de qué es."""
    return {
        "_nota": "Las carpinterías de la marca. Ver CARPINTERIA.md. "
                "Una carpintería es un molde de formato, no un video.",
        "version": 1,
        "actualizado": date.today().isoformat(),
        "carpinterias": [],
    }


def carpinteria_vacia() -> dict:
    """Una ficha en blanco con todas las claves, para llenar a mano."""
    return {
        "id": None,
        "nombre": "",
        "estado": "nuevo",
        "creada": date.today().isoformat(),
        "original": {
            "url": "", "cuenta": "", "red": "", "fecha": "", "vistas": None,
            "likes": None, "compartidos": None, "duracion_s": None,
            "señal": None, "señal_tipo": None, "gancho_literal": "", "cuadros": [],
        },
        "gramatica": {
            "tipo_gancho": "", "gancho_0_3s": "", "re_gancho_s": None, "re_gancho": "",
            "estructura": [], "banda_duracion": "", "subtitulos": "", "plano": "",
            "ritmo_cortes": None, "sonido": "", "cierre": "", "mecanica_comentarios": "",
        },
        "tropicalizacion": {
            "encaja": False, "serie": "", "pieza": "", "tarea_real": "",
            "prueba_real_ia": False, "prueba_guardada": False,
            "resultado_o_pregunta_3s": "", "regla_lider": "", "cambios": [], "avisos": [],
        },
        "nuestro": {
            "piezas": [], "seguidores_por_1000": None, "vistas_promedio": None, "notas": "",
        },
    }


# ---------------------------------------------------------------- archivo

def cargar(path: Path = CATALOGO) -> dict:
    """Lee el catálogo. Si no existe, devuelve uno vacío (no revienta)."""
    if not Path(path).exists():
        return catalogo_vacio()
    datos = json.loads(Path(path).read_text(encoding="utf-8"))
    if "carpinterias" not in datos:
        datos = catalogo_vacio()
    return datos


def guardar(catalogo: dict, path: Path = CATALOGO) -> Path:
    """Escribe el catálogo en UTF-8 SIN BOM. Devuelve la ruta."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    catalogo["actualizado"] = date.today().isoformat()
    texto = json.dumps(catalogo, ensure_ascii=False, indent=2)
    path.write_text(texto, encoding="utf-8")
    return path


# ---------------------------------------------------------------- consulta

def buscar(id_carp: str, catalogo: dict) -> dict | None:
    """La carpintería con ese ID, o None."""
    for c in catalogo.get("carpinterias", []):
        if c.get("id") == id_carp:
            return c
    return None


def por_estado(estado: str, catalogo: dict) -> list[dict]:
    """Las carpinterías en ese estado."""
    return [c for c in catalogo.get("carpinterias", []) if c.get("estado") == estado]


def siguientes_ids(catalogo: dict, cantidad: int = 1) -> list[str]:
    """Los próximos IDs libres, en orden."""
    usados = {c.get("id") for c in catalogo.get("carpinterias", [])}
    numeros = [int(m.group(1)) for i in usados if i and (m := RE_ID.match(i))]
    siguiente = max(numeros) + 1 if numeros else 1
    return [f"C-{n:03d}" for n in range(siguiente, siguiente + cantidad)]


def siguiente_id(catalogo: dict) -> str:
    """El próximo ID libre."""
    return siguientes_ids(catalogo, 1)[0]


# ---------------------------------------------------------------- señales

def encaja(carp: dict) -> bool:
    """¿Esta carpintería se puede proponer? Si no encaja, no se propone."""
    return bool(carp.get("tropicalizacion", {}).get("encaja"))


def señal_global(carp: dict) -> float:
    """La señal que trae el radar (0 a 1)."""
    v = carp.get("original", {}).get("señal")
    try:
        return max(0.0, min(1.0, float(v)))
    except (TypeError, ValueError):
        return 0.0


def señal_nuestra(carp: dict) -> float:
    """Nuestra señal: seguidores por cada 1.000 vistas, normalizada a 0-1.

    Es la que manda (ESTRATEGIA.md §1: en la fase 1 la métrica son los seguidores).
    """
    v = carp.get("nuestro", {}).get("seguidores_por_1000")
    try:
        if v is None:
            return 0.0
        return max(0.0, min(1.0, float(v) / REFERENCIA_SEGUIDORES))
    except (TypeError, ValueError):
        return 0.0


def prioridad(carp: dict) -> float:
    """El número con el que se ordena el catálogo.

    Nuestra señal pesa el doble que la global, porque lo que funcionó en NUESTRA
    cuenta es lo que vamos a repetir. El estado agrega o resta.
    """
    if not encaja(carp):
        return -999.0
    base = 2.0 * señal_nuestra(carp) + 1.0 * señal_global(carp)
    return base + BONO_ESTADO.get(carp.get("estado", "nuevo"), 0.0)


def ordenar(catalogo: dict) -> list[dict]:
    """El catálogo ordenado por prioridad: lo que primero conviene repetir."""
    return sorted(catalogo.get("carpinterias", []), key=prioridad, reverse=True)


# ---------------------------------------------------------------- validación

def validar(carp: dict) -> list[str]:
    """Los problemas que tiene la ficha. Lista vacía = la ficha está bien."""
    errores: list[str] = []
    if not carp.get("id") or not RE_ID.match(str(carp.get("id"))):
        errores.append("falta el id con el formato C-000")
    if not (carp.get("nombre") or "").strip():
        errores.append("falta el nombre")
    if carp.get("estado") not in ESTADOS:
        errores.append(f"estado inválido: {carp.get('estado')!r}; use uno de {', '.join(ESTADOS)}")

    original = carp.get("original", {})
    for campo in CAMPOS_OBLIGATORIOS_ORIGINAL:
        if not str(original.get(campo) or "").strip():
            errores.append(f"falta original.{campo}")
    fecha = str(original.get("fecha") or "")
    if fecha and not RE_FECHA.match(fecha):
        errores.append("original.fecha tiene que ser AAAA-MM-DD")
    señal = original.get("señal")
    if señal is not None:
        try:
            if not 0.0 <= float(señal) <= 1.0:
                errores.append("original.señal tiene que estar entre 0 y 1")
        except (TypeError, ValueError):
            errores.append("original.señal no es un número")

    gramatica = carp.get("gramatica", {})
    for campo in CAMPOS_OBLIGATORIOS_GRAMATICA:
        if not gramatica.get(campo):
            errores.append(f"falta gramatica.{campo}")
    if gramatica.get("estructura") and not isinstance(gramatica["estructura"], list):
        errores.append("gramatica.estructura tiene que ser una lista")

    trop = carp.get("tropicalizacion", {})
    if trop.get("encaja"):
        for campo in ("serie", "tarea_real", "resultado_o_pregunta_3s", "regla_lider"):
            if not str(trop.get(campo) or "").strip():
                errores.append(f"falta tropicalizacion.{campo}")
        if not trop.get("prueba_real_ia"):
            errores.append("falta tropicalizacion.prueba_real_ia (la prueba real con IA)")
        if not trop.get("prueba_guardada"):
            errores.append("falta tropicalizacion.prueba_guardada (el resultado guardado)")
        cambios = trop.get("cambios") or []
        if not cambios:
            errores.append("falta tropicalizacion.cambios: el rastro del cambio es obligatorio")
        for i, cambio in enumerate(cambios, 1):
            for campo in CAMPOS_OBLIGATORIOS_CAMBIO:
                if not str(cambio.get(campo) or "").strip():
                    errores.append(f"tropicalizacion.cambios[{i}] sin {campo}")

    nuestro = carp.get("nuestro", {})
    if nuestro.get("seguidores_por_1000") is not None:
        try:
            if float(nuestro["seguidores_por_1000"]) < 0:
                errores.append("nuestro.seguidores_por_1000 no puede ser negativo")
        except (TypeError, ValueError):
            errores.append("nuestro.seguidores_por_1000 no es un número")
        if not nuestro.get("piezas"):
            errores.append("nuestro.seguidores_por_1000 sin nuestro.piezas: falta la evidencia")
    return errores


# ---------------------------------------------------------------- escritura

def agregar(carp: dict, catalogo: dict) -> dict:
    """Agrega una carpintería al catálogo. Le pone id si no lo tiene.

    Devuelve la ficha ya guardada en el catálogo.
    """
    if not carp.get("id"):
        carp["id"] = siguiente_id(catalogo)
    carp.setdefault("creada", date.today().isoformat())
    carp.setdefault("estado", "nuevo")
    catalogo.setdefault("carpinterias", []).append(carp)
    return carp


def actualizar(id_carp: str, cambios: dict, catalogo: dict) -> dict:
    """Cambia campos de una carpintería existente (merge de un nivel)."""
    carp = buscar(id_carp, catalogo)
    if carp is None:
        raise KeyError(f"No existe la carpintería {id_carp}")
    for clave, valor in cambios.items():
        if isinstance(valor, dict) and isinstance(carp.get(clave), dict):
            carp[clave].update(valor)
        else:
            carp[clave] = valor
    return carp


def marcar_resultado(id_carp: str, piezas: list[str], seguidores_por_1000: float | None,
                     vistas_promedio: float | None, notas: str, catalogo: dict) -> dict:
    """Cierra el ciclo: una carpintería se probó y ya tenemos nuestro número.

    El estado se deduce del número: si trajo seguidores, funcionó; si no, no.
    """
    carp = actualizar(id_carp, {"nuestro": {
        "piezas": piezas,
        "seguidores_por_1000": seguidores_por_1000,
        "vistas_promedio": vistas_promedio,
        "notas": notas,
    }}, catalogo)
    if seguidores_por_1000 is None:
        carp["estado"] = "en_prueba"
    elif seguidores_por_1000 > 0:
        carp["estado"] = "funciono"
    else:
        carp["estado"] = "no_funciono"
    return carp
