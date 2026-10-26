"""Pruebas de la agenda del mes.

Se prueba con fechas fijas y un catálogo sintético: nada de red, nada de reloj.
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "carpinterias"))

import agenda as ag  # noqa: E402
import carpinterias as cp  # noqa: E402


def carpinteria(nombre: str, serie: str, estado: str = "nuevo", seg: float | None = None) -> dict:
    c = cp.carpinteria_vacia()
    c["id"] = None
    c["nombre"] = nombre
    c["estado"] = estado
    c["tropicalizacion"]["encaja"] = True
    c["tropicalizacion"]["serie"] = serie
    c["original"]["señal"] = 0.05
    c["nuestro"]["seguidores_por_1000"] = seg
    c["nuestro"]["piezas"] = ["D1-1"] if seg is not None else []
    return c


def test_agenda_vacia_sin_carpinterias():
    assert ag.agenda(cp.catalogo_vacio()) == []


def test_agenda_sin_carpinterias_que_encajen():
    cat = cp.catalogo_vacio()
    c = cp.agregar(cp.carpinteria_vacia(), cat)
    c["tropicalizacion"]["encaja"] = False
    assert ag.agenda(cat) == []


def test_agenda_reparte_una_pieza_por_dia():
    cat = cp.catalogo_vacio()
    for i, serie in enumerate(["lo_probe_por_vos", "un_truco_en_12_s", "la_ia_puede",
                                "lo_probe_por_vos", "un_truco_en_12_s", "la_ia_puede",
                                "la_oficina"]):
        cp.agregar(cp.carpinteria_vacia(), cat)
        c = cat["carpinterias"][-1]
        c["nombre"] = f"Carpintería {i}"
        c["tropicalizacion"]["encaja"] = True
        c["tropicalizacion"]["serie"] = serie
        c["original"]["señal"] = 0.05
    plan = ag.agenda(cat, inicio=date(2026, 11, 2), dias=7)
    assert len(plan) == 7
    assert plan[0]["fecha"] == "2026-11-02"
    assert plan[0]["dia"] == "Lunes"


def test_la_agenda_no_repite_la_misma_carpinteria_en_la_semana():
    cat = cp.catalogo_vacio()
    for i in range(6):
        cp.agregar(cp.carpinteria_vacia(), cat)
        c = cat["carpinterias"][-1]
        c["nombre"] = f"Carpintería {i}"
        c["tropicalizacion"]["encaja"] = True
        c["tropicalizacion"]["serie"] = "lo_probe_por_vos"
        c["original"]["señal"] = 0.05
    plan = ag.agenda(cat, inicio=date(2026, 11, 2), dias=6)
    semana = [p["carpinteria"] for p in plan]
    assert len(semana) == len(set(semana))


def test_la_agenda_respeta_el_tope_semanal_de_cada_serie():
    cat = cp.catalogo_vacio()
    for i in range(10):
        cp.agregar(cp.carpinteria_vacia(), cat)
        c = cat["carpinterias"][-1]
        c["nombre"] = f"Carpintería {i}"
        c["tropicalizacion"]["encaja"] = True
        c["tropicalizacion"]["serie"] = "un_truco_en_12_s"
        c["original"]["señal"] = 0.05
    plan = ag.agenda(cat, inicio=date(2026, 11, 2), dias=7)
    de_truco = [p for p in plan if p["serie"] == "un_truco_en_12_s"]
    assert len(de_truco) <= ag.TOPES_SEMANA["un_truco_en_12_s"]


def test_lo_que_ya_funciono_va_primero():
    cat = cp.catalogo_vacio()
    nueva = cp.agregar(cp.carpinteria_vacia(), cat)
    nueva["nombre"] = "Nueva"
    nueva["tropicalizacion"]["encaja"] = True
    nueva["tropicalizacion"]["serie"] = "lo_probe_por_vos"
    nueva["original"]["señal"] = 0.09

    probada = cp.agregar(cp.carpinteria_vacia(), cat)
    probada["nombre"] = "Ya funcionó"
    probada["tropicalizacion"]["encaja"] = True
    probada["tropicalizacion"]["serie"] = "lo_probe_por_vos"
    probada["original"]["señal"] = 0.01
    probada["estado"] = "funciono"
    probada["nuestro"] = {"piezas": ["D3-1"], "seguidores_por_1000": 25.0,
                           "vistas_promedio": 900.0, "notas": ""}

    plan = ag.agenda(cat, inicio=date(2026, 11, 2), dias=7)
    primera = plan[0]["carpinteria"]
    assert primera == probada["id"]


def test_el_por_que_dice_que_ya_funciono():
    cat = cp.catalogo_vacio()
    c = cp.agregar(cp.carpinteria_vacia(), cat)
    c["nombre"] = "Probada"
    c["tropicalizacion"]["encaja"] = True
    c["tropicalizacion"]["serie"] = "lo_probe_por_vos"
    c["estado"] = "funciono"
    c["nuestro"] = {"piezas": ["D3-1"], "seguidores_por_1000": 25.0,
                    "vistas_promedio": 900.0, "notas": ""}
    plan = ag.agenda(cat, inicio=date(2026, 11, 2), dias=7)
    assert "25 seguidores" in plan[0]["por_que"]


def test_render_sin_plan_lo_dice():
    texto = ag.render([], "2026-11")
    assert "No hay carpinterías" in texto


def test_render_con_plan_tiene_tabla():
    cat = cp.catalogo_vacio()
    c = cp.agregar(cp.carpinteria_vacia(), cat)
    c["nombre"] = "Una"
    c["tropicalizacion"]["encaja"] = True
    c["tropicalizacion"]["serie"] = "lo_probe_por_vos"
    plan = ag.agenda(cat, inicio=date(2026, 11, 2), dias=7)
    texto = ag.render(plan, "2026-11")
    assert "| Día | Fecha | Serie |" in texto
    assert "Una" in texto
