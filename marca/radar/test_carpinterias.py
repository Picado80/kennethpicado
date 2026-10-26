"""Pruebas del catálogo de carpinterías y de las reglas de tropicalización.

Se prueban sin red y sin archivos reales: todo va en memoria o en tmp_path.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# El módulo vive junto a este archivo.
sys.path.insert(0, str(Path(__file__).resolve().parent / "carpinterias"))

import carpinterias as cp  # noqa: E402
import tropicalizar as tr  # noqa: E402


def carpinteria_de_ejemplo() -> dict:
    """Una carpintería completa y válida, con los números de una viral real."""
    c = cp.carpinteria_vacia()
    c["id"] = "C-001"
    c["nombre"] = "El remate antes del segundo 3"
    c["original"].update({
        "url": "https://www.tiktok.com/@ejemplo/video/123",
        "cuenta": "@ejemplo",
        "red": "tiktok",
        "fecha": "2026-10-20",
        "vistas": 412000,
        "likes": 21000,
        "compartidos": 33000,
        "duracion_s": 12,
        "señal": 0.0801,
        "señal_tipo": "compartidos",
        "gancho_literal": "el que hace el trabajo no lo revisa",
    })
    c["gramatica"].update({
        "tipo_gancho": "afirmacion_incomoda",
        "gancho_0_3s": "texto grande con la regla, sin contexto",
        "re_gancho_s": 4,
        "re_gancho": "un ejemplo real que se ve en pantalla",
        "estructura": ["la regla", "el ejemplo", "la regla de líder"],
        "banda_duracion": "6-15 s",
        "subtitulos": "palabra_por_palabra",
        "plano": "a_camara",
        "ritmo_cortes": 6,
        "sonido": "el de la casa",
        "cierre": "pregunta",
        "mecanica_comentarios": "pregunta abierta",
    })
    c["tropicalizacion"].update({
        "encaja": True,
        "serie": "Un truco en 12 s",
        "pieza": "La regla que le falta al que revisa",
        "tarea_real": "revisar una nota de voz de mi suegra",
        "prueba_real_ia": True,
        "prueba_guardada": True,
        "resultado_o_pregunta_3s": "el resultado de la IA en pantalla, de entrada",
        "regla_lider": "Regla de líder #7: el que hace el trabajo no lo revisa.",
        "cambios": [
            {"que": "Gancho", "original": "el que hace el trabajo no lo revisa",
             "nuestro": "el que hace el trabajo no lo revisa, y se nota",
             "porque": "La contradicción entra sola, sin contexto."},
        ],
    })
    return c


# ---------------------------------------------------------------- catálogo

def test_catalogo_vacio_tiene_la_estructura():
    cat = cp.catalogo_vacio()
    assert cat["carpinterias"] == []
    assert "version" in cat


def test_guardar_escribe_utf8_sin_bom(tmp_path):
    ruta = tmp_path / "catalogo.json"
    cp.guardar(cp.catalogo_vacio(), ruta)
    crudo = ruta.read_bytes()
    assert not crudo.startswith(b"\xef\xbb\xbf")
    assert json.loads(crudo.decode("utf-8"))["carpinterias"] == []


def test_agregar_asigna_id_en_orden(tmp_path):
    cat = cp.catalogo_vacio()
    cp.agregar(cp.carpinteria_vacia(), cat)
    cp.agregar(cp.carpinteria_vacia(), cat)
    assert [c["id"] for c in cat["carpinterias"]] == ["C-001", "C-002"]


def test_siguiente_id_no_reutiliza_numero():
    cat = cp.catalogo_vacio()
    cp.agregar(cp.carpinteria_vacia(), cat)
    cat["carpinterias"][0]["id"] = "C-007"
    assert cp.siguiente_id(cat) == "C-008"


def test_buscar_y_por_estado():
    cat = cp.catalogo_vacio()
    c = cp.agregar(cp.carpinteria_vacia(), cat)
    c["estado"] = "funciono"
    assert cp.buscar("C-001", cat) is c
    assert cp.buscar("C-999", cat) is None
    assert cp.por_estado("funciono", cat) == [c]


def test_actualizar_hace_merge_de_un_nivel():
    cat = cp.catalogo_vacio()
    c = cp.agregar(cp.carpinteria_vacia(), cat)
    cp.actualizar("C-001", {"original": {"vistas": 1000}, "nombre": "X"}, cat)
    assert c["original"]["vistas"] == 1000
    assert c["original"]["cuenta"] == ""       # no se borró lo demás
    assert c["nombre"] == "X"


def test_actualizar_falla_con_id_inexistente():
    with pytest.raises(KeyError):
        cp.actualizar("C-999", {"nombre": "X"}, cp.catalogo_vacio())


# ---------------------------------------------------------------- validación

def test_una_carpinteria_completa_no_tiene_errores():
    assert cp.validar(carpinteria_de_ejemplo()) == []


def test_falta_el_rastro_del_cambio():
    c = carpinteria_de_ejemplo()
    c["tropicalizacion"]["cambios"] = []
    errores = cp.validar(c)
    assert any("cambios" in e for e in errores)


def test_falta_cada_cambio_obligatorio():
    c = carpinteria_de_ejemplo()
    c["tropicalizacion"]["cambios"] = [{"que": "Gancho", "original": "a", "nuestro": "b"}]
    errores = cp.validar(c)
    assert any("porque" in e for e in errores)


def test_falta_la_prueba_real_con_ia():
    c = carpinteria_de_ejemplo()
    c["tropicalizacion"]["prueba_real_ia"] = False
    errores = cp.validar(c)
    assert any("prueba_real_ia" in e for e in errores)


def test_falta_el_original():
    c = carpinteria_de_ejemplo()
    c["original"]["url"] = ""
    errores = cp.validar(c)
    assert any("original.url" in e for e in errores)


def test_estado_invalido():
    c = carpinteria_de_ejemplo()
    c["estado"] = "inventado"
    assert any("estado inválido" in e for e in errores_de(c))


def errores_de(c):
    return cp.validar(c)


# ---------------------------------------------------------------- señales

def test_senal_nuestra_normaliza_a_30_por_mil():
    c = carpinteria_de_ejemplo()
    c["nuestro"]["seguidores_por_1000"] = 30
    assert cp.señal_nuestra(c) == 1.0
    c["nuestro"]["seguidores_por_1000"] = 15
    assert cp.señal_nuestra(c) == 0.5


def test_senal_nuestra_sin_prueba_es_cero():
    c = carpinteria_de_ejemplo()
    c["nuestro"]["seguidores_por_1000"] = None
    assert cp.señal_nuestra(c) == 0.0


def test_nuestra_señal_pesa_mas_que_la_global():
    """Una carpintería que funcionó en nuestra cuenta va arriba de una que solo
    viralizó en el mundo."""
    cat = cp.catalogo_vacio()
    a = cp.agregar(cp.carpinteria_vacia(), cat)
    a["tropicalizacion"]["encaja"] = True
    a["original"]["señal"] = 0.08          # viralizó en el mundo
    a["estado"] = "nuevo"

    b = cp.agregar(cp.carpinteria_vacia(), cat)
    b["tropicalizacion"]["encaja"] = True
    b["original"]["señal"] = 0.01          # viralizó poco en el mundo
    b["nuestro"]["seguidores_por_1000"] = 25.0   # pero funcionó con nosotros
    b["estado"] = "funciono"

    orden = [c["id"] for c in cp.ordenar(cat)]
    assert orden[0] == b["id"]


def test_lo_que_no_encaja_no_se_propone():
    c = carpinteria_de_ejemplo()
    c["tropicalizacion"]["encaja"] = False
    assert cp.prioridad(c) == -999.0
    assert cp.encaja(c) is False


def test_no_funciono_baja_en_el_orden():
    cat = cp.catalogo_vacio()
    a = cp.agregar(cp.carpinteria_vacia(), cat)
    a["tropicalizacion"]["encaja"] = True
    a["estado"] = "funciono"
    b = cp.agregar(cp.carpinteria_vacia(), cat)
    b["tropicalizacion"]["encaja"] = True
    b["estado"] = "no_funciono"
    assert cp.prioridad(a) > cp.prioridad(b)


def test_marcar_resultado_cambia_el_estado():
    cat = cp.catalogo_vacio()
    c = cp.agregar(cp.carpinteria_vacia(), cat)
    cp.marcar_resultado("C-001", ["D5-1"], 12.5, 830.0, "trajo seguidores", cat)
    assert c["estado"] == "funciono"
    assert c["nuestro"]["seguidores_por_1000"] == 12.5
    cp.marcar_resultado("C-001", ["D6-1"], 0.0, 1200.0, "no trajo", cat)
    assert c["estado"] == "no_funciono"


# ---------------------------------------------------------------- tropicalizar

def test_las_cuatro_condiciones_cumplen():
    cond = tr.condiciones(carpinteria_de_ejemplo())
    assert len(cond) == 4
    assert all(c["estado"] == "cumple" for c in cond)


def test_condiciones_cuando_falta_la_tarea():
    c = carpinteria_de_ejemplo()
    c["tropicalizacion"]["tarea_real"] = ""
    cond = {x["id"]: x for x in tr.condiciones(c)}
    assert cond["tarea_real"]["estado"] == "falta"
    assert cond["regla_lider"]["estado"] == "cumple"


def test_la_prueba_con_ia_queda_a_mano():
    c = carpinteria_de_ejemplo()
    c["tropicalizacion"]["prueba_guardada"] = False
    cond = {x["id"]: x for x in tr.condiciones(c)}
    assert cond["prueba_real_ia"]["estado"] == "falta"
    assert cond["prueba_real_ia"]["a_mano"] is True


def test_serie_sugerida_devuelve_candidatos_con_porque():
    c = carpinteria_de_ejemplo()
    c["tropicalizacion"]["cambios"] = []
    c["gramatica"]["estructura"] = ["la pregunta al jefe sobre el equipo de la oficina"]
    c["gramatica"]["cierre"] = "pregunta"
    c["original"]["duracion_s"] = 35
    candidatos = tr.serie_sugerida(c)
    assert candidatos
    assert all("porque" in c2 and c2["porque"] for c2 in candidatos)
    assert candidatos[0]["id"] in {s["id"] for s in tr.SERIES}


def test_esqueleto_trae_el_original_al_lado():
    esq = tr.esqueleto(carpinteria_de_ejemplo())
    dimensiones = {e["dimension"] for e in esq}
    assert "Gancho (0 a 3 s)" in dimensiones
    assert all(e["decidir"] for e in esq)


def test_estiramientos_avisa_de_lo_largo():
    c = carpinteria_de_ejemplo()
    c["original"]["duracion_s"] = 60
    avisos = tr.estiramientos(c)
    assert any("recortar" in a for a in avisos)


def test_estiramientos_avisa_si_el_molde_vende():
    c = carpinteria_de_ejemplo()
    c["original"]["gancho_literal"] = "compra ahora con descuento en el link"
    assert any("vende" in a.lower() for a in tr.estiramientos(c))


def test_digest_muestra_el_original_y_el_cambio():
    texto = tr.montar_digest([carpinteria_de_ejemplo()], "2026-10-25")
    assert "Original" in texto
    assert "Cómo lo tropicalizamos" in texto
    assert "el que hace el trabajo no lo revisa" in texto
    assert "Por qué" in texto
    assert "Regla de líder" in texto


def test_digest_sin_carpinterias_no_inventa():
    texto = tr.montar_digest([], "2026-10-25")
    assert "no salió ninguna" in texto.lower()


def test_numero_en_formato_costarricense():
    assert tr.numero(412000) == "412.000"
    assert tr.numero(8.1) == "8,1"
    assert tr.numero(None) == "—"
    assert tr.pct(0.081) == "8,1%"


# ---------------------------------------------------------------- el motor de pruebas

def test_el_motor_de_pruebas_escribe_la_evidencia(tmp_path, monkeypatch):
    """`pruebas.py` corre las tareas de un día y guarda la respuesta cruda.
    Se prueba sin red: la llamada se sustituye."""
    import pruebas as motor

    llamadas = []

    def llamar_falso(tarea, max_tokens=2500):
        llamadas.append(tarea)
        return "la respuesta de la IA", '{"choices": []}', "MiniMax-M3"

    monkeypatch.setattr(motor, "llamar", llamar_falso)

    tareas = {"C-001": {"titulo": "La prueba", "serie": "¿La IA puede…?",
                        "tarea": "hacé algo", "por_que": "porque sí"}}
    destino = tmp_path / "2026-10-26"
    resumen = motor.correr("2026-10-26", tareas, destino)

    assert len(llamadas) == 1
    assert (destino / "C-001.md").exists()
    assert (destino / "raw" / "C-001.json").exists()
    assert "la respuesta de la IA" in (destino / "C-001.md").read_text(encoding="utf-8")
    assert resumen[0]["hecha"] is True


def test_el_motor_avisa_cuando_la_prueba_no_se_pudo_hacer(tmp_path, monkeypatch):
    """Si la llamada falla, la prueba queda MARCADA como no hecha. Nunca hay
    una respuesta inventada."""
    import pruebas as motor

    def llamar_falso(tarea, max_tokens=2500):
        return "[NO SE PUDO HACER LA PRUEBA] HTTP 429", "", "MiniMax-M3"

    monkeypatch.setattr(motor, "llamar", llamar_falso)

    tareas = {"C-001": {"titulo": "La prueba", "serie": "¿La IA puede…?",
                        "tarea": "hacé algo", "por_que": "porque sí"}}
    destino = tmp_path / "2026-10-26"
    resumen = motor.correr("2026-10-26", tareas, destino)

    assert resumen[0]["hecha"] is False
    assert "NO SE PUDO" in (destino / "C-001.md").read_text(encoding="utf-8")
    assert not (destino / "raw" / "C-001.json").exists()


def test_el_motor_no_deja_la_respuesta_vacia(tmp_path, monkeypatch):
    """MiniMax-M3 con pocos tokens responde vacío: el motor avisa y no inventa."""
    import pruebas as motor

    def llamar_falso(tarea, max_tokens=2500):
        return "[RESPUESTA VACIA: el modelo gasto todos los tokens razonando]", "", "MiniMax-M3"

    monkeypatch.setattr(motor, "llamar", llamar_falso)
    tareas = {"C-001": {"titulo": "P", "serie": "S", "tarea": "t", "por_que": "p"}}
    resumen = motor.correr("2026-10-26", tareas, tmp_path / "d")
    assert resumen[0]["hecha"] is False
    assert motor.MAX_TOKENS >= 2500


def test_las_tareas_del_primer_dia_estan_en_json():
    """El 26-oct el agente dejó un script con fecha. Las tareas quedan en JSON
    para que el motor sea el mismo todos los días."""
    ruta = (Path(__file__).resolve().parent / "carpinterias" / "pruebas"
            / "2026-10-26" / "tareas.json")
    assert ruta.exists()
    tareas = json.loads(ruta.read_text(encoding="utf-8"))
    reales = {k: v for k, v in tareas.items() if not k.startswith("_")}
    assert len(reales) == 6
    for clave, t in reales.items():
        assert t["tarea"].strip()
        assert t["serie"].strip()
        assert t["por_que"].strip()
