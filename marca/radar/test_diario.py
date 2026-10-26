"""Pruebas del radar diario. No tocan la red, ni yt-dlp, ni ffmpeg, ni redes.py:
todo entra por un runner falso (inyeccion de dependencias)."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import diario  # noqa: E402
import radar  # noqa: E402

AHORA = datetime(2026, 10, 25, 8, 0, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def _sin_red(monkeypatch):
    """redes.py lo escribe otra persona: aca no existe (o no decide nada).
    Tampoco se corre yt-dlp ni ffmpeg: las dos piezas caras quedan fuera."""
    monkeypatch.setattr(diario, "_disponibles", lambda: {})
    monkeypatch.setattr(diario, "_info_video", lambda url, cookies=None: None)
    monkeypatch.setattr(diario, "_extraer_cuadros", lambda video, cookies=None, info=None: [])


def video(url, *, red="tiktok", cuenta="demo", vistas=100000, likes=5000, compartidos=8000,
          fecha="2026-10-24T12:00:00+00:00", senal=0.08, duracion=12,
          transcripcion="", texto="Un video sobre IA"):
    """Un video con las columnas que devuelve redes.obtener."""
    return {
        "url": url, "red": red, "cuenta": cuenta, "fuente": f"cuenta {cuenta}",
        "fecha": fecha, "vistas": vistas, "likes": likes, "comentarios": 100,
        "compartidos": compartidos, "guardados": 200, "duracion_s": duracion,
        "texto": texto, "transcripcion": transcripcion,
        "señal": senal, "señal_tipo": "compartidos",
    }


def config(**kwargs):
    """La config de fuentes.json, recortada a lo que las pruebas necesitan."""
    base = {
        "redes": {
            "tiktok": {"cuentas": ["dotcsv"], "urls": [], "min_vistas": 20000},
            "instagram": {"cuentas": ["machillo.puravida"], "urls": [], "min_vistas": 5000},
        },
        "hashtags": [], "urls": [], "dias": 7, "min_vistas": 20000,
        "top": 15, "por_fuente": 30,
    }
    base.update(kwargs)
    return base


# ------------------------------------------------------------------ la doble pasada

def test_ve_todos_los_videos_y_deja_los_top_por_senal():
    """Pasada 1: un runner que devuelve 100 videos. Pasada 2: los mejores por señal."""
    videos = [video(f"https://www.tiktok.com/@dotcsv/video/{i}",
                    senal=round(0.01 * i, 2), vistas=1000 * i) for i in range(1, 101)]

    def runner(red, usuario, n=30):
        return videos

    fuentes = config(redes={"tiktok": {"cuentas": ["dotcsv"], "urls": [], "min_vistas": 0}})
    res = diario.barrer(fuentes, ahora=AHORA, runner=runner, top=5)

    assert res["vistos"]["tiktok"] == 100          # los vio todos
    assert res["redes"] == ["tiktok"]
    assert res["fecha"] == "2026-10-25"
    senales = [c["señal"] for c in res["candidatos"]]
    assert len(res["candidatos"]) == 5              # solo los mejores a fondo
    assert senales == sorted(senales, reverse=True)
    assert senales[0] == 1.0


def test_el_desempate_es_por_vistas():
    """Misma señal: gana el que tiene más vistas."""
    vidos = [video("https://x/1", senal=0.5, vistas=100),
             video("https://x/2", senal=0.5, vistas=9000)]

    def runner(red, usuario, n=30):
        return vidos

    fuentes = config(redes={"tiktok": {"cuentas": ["a"], "urls": [], "min_vistas": 0}})
    res = diario.barrer(fuentes, ahora=AHORA, runner=runner, top=2)
    assert [c["url"] for c in res["candidatos"]] == ["https://x/2", "https://x/1"]


def test_dedupe_por_url_no_repite_el_mismo_video():
    """El mismo video en dos cuentas es un video, no dos."""
    mismo = video("https://www.tiktok.com/@dotcsv/video/9", senal=0.4)

    def runner(red, usuario, n=30):
        return [mismo, dict(mismo)]

    fuentes = config(redes={"tiktok": {"cuentas": ["a", "b"], "urls": [], "min_vistas": 0}})
    res = diario.barrer(fuentes, ahora=AHORA, runner=runner, top=5)
    assert len(res["candidatos"]) == 1
    assert res["vistos"]["tiktok"] == 1


# ------------------------------------------------------------------ filtros

def test_filtra_viejos_y_de_pocas_vistas():
    """Con `ahora` fijo: fuera los viejos y los que no llegan al mínimo."""
    videos = [
        video("https://x/reciente", vistas=50000, fecha="2026-10-24T00:00:00+00:00"),
        video("https://x/viejo", vistas=50000, fecha="2026-08-01T00:00:00+00:00"),
        video("https://x/pocas", vistas=100, fecha="2026-10-24T00:00:00+00:00"),
    ]

    def runner(red, usuario, n=30):
        return videos

    fuentes = config(redes={"tiktok": {"cuentas": ["a"], "urls": [], "min_vistas": 20000}})
    res = diario.barrer(fuentes, ahora=AHORA, runner=runner, top=5)
    assert [c["url"] for c in res["candidatos"]] == ["https://x/reciente"]
    assert res["vistos"]["tiktok"] == 3              # los vio, aunque no califican


def test_el_min_vistas_de_cada_red_manda_sobre_el_global():
    """Instagram con 6.000 vistas pasa con su mínimo de 5.000, no con el global de 20.000."""
    def runner(red, usuario, n=30):
        return [video("https://www.instagram.com/reel/1", red="instagram",
                      cuenta="machillo.puravida", vistas=6000, senal=0.3)]

    fuentes = config(redes={"instagram": {"cuentas": ["machillo.puravida"], "urls": [],
                                         "min_vistas": 5000}})
    res = diario.barrer(fuentes, ahora=AHORA, runner=runner, top=5)
    assert len(res["candidatos"]) == 1


# ------------------------------------------------------------------ fallas y omitidas

def test_una_red_que_falla_no_tumba_la_corrida():
    def runner(red, usuario, n=30):
        if red == "instagram":
            raise RuntimeError("Instagram bloqueo la captura")
        return [video("https://www.tiktok.com/@dotcsv/video/1")]

    res = diario.barrer(config(), ahora=AHORA, runner=runner, top=5)
    assert len(res["fallas"]) == 1
    assert "instagram@machillo.puravida" in res["fallas"][0]
    assert len(res["candidatos"]) == 1                # la otra red sigue


def test_una_red_sin_acceso_queda_omitida_y_no_es_falla(monkeypatch):
    monkeypatch.setattr(diario, "_disponibles", lambda: {"instagram": False})

    def runner(red, usuario, n=30):
        return [video("https://www.tiktok.com/@dotcsv/video/1")]

    res = diario.barrer(config(), ahora=AHORA, runner=runner, top=5)
    assert res["omitidas"] == [{"red": "instagram", "motivo": "sin acceso"}]
    assert res["fallas"] == []
    assert res["vistos"]["instagram"] == 0
    assert len(res["candidatos"]) == 1


def test_una_red_que_no_devuelve_nada_queda_omitida_y_no_es_falla():
    """redes.obtener nunca lanza: una red caída devuelve [] y se anota como omitida."""
    def runner(red, usuario, n=30):
        if red == "instagram":
            return []
        return [video("https://www.tiktok.com/@dotcsv/video/1")]

    res = diario.barrer(config(), ahora=AHORA, runner=runner, top=5)
    assert res["omitidas"] == [{"red": "instagram", "motivo": "sin captura"}]
    assert res["fallas"] == []
    assert res["vistos"]["instagram"] == 0
    assert len(res["candidatos"]) == 1


def test_main_sale_con_1_si_ninguna_red_se_puede_leer(tmp_path):
    """Todas las redes devuelven []: no hay nada que leer, se sale con 1."""
    fuentes = tmp_path / "fuentes.json"
    fuentes.write_text(json.dumps(config()), encoding="utf-8")

    def runner(*_a, **_k):
        return []

    codigo = diario.main(["--fuentes", str(fuentes),
                           "--salidas-dir", str(tmp_path / "salidas"),
                           "--hoy", str(tmp_path / "hoy.md"), "--dry-run"],
                          runner=runner, ahora=AHORA)
    assert codigo == 1


# ------------------------------------------------------------------ main

def test_main_sale_con_1_si_fallan_todas(tmp_path):
    fuentes = tmp_path / "fuentes.json"
    fuentes.write_text(json.dumps(config()), encoding="utf-8")

    def runner(*_a, **_k):
        raise RuntimeError("sin red")

    codigo = diario.main(["--fuentes", str(fuentes),
                           "--salidas-dir", str(tmp_path / "salidas"),
                           "--hoy", str(tmp_path / "hoy.md"), "--dry-run"],
                          runner=runner, ahora=AHORA)
    assert codigo == 1


def test_main_sale_con_0_si_una_falla_pero_otra_anda(tmp_path):
    fuentes = tmp_path / "fuentes.json"
    fuentes.write_text(json.dumps(config()), encoding="utf-8")

    def runner(red, usuario, n=30):
        if red == "instagram":
            raise RuntimeError("Instagram bloqueo la captura")
        return [video("https://www.tiktok.com/@dotcsv/video/1")]

    codigo = diario.main(["--fuentes", str(fuentes),
                           "--salidas-dir", str(tmp_path / "salidas"),
                           "--hoy", str(tmp_path / "hoy.md"), "--dry-run"],
                          runner=runner, ahora=AHORA)
    assert codigo == 0


def test_main_sin_fuentes_sale_con_2(tmp_path):
    assert diario.main(["--fuentes", str(tmp_path / "no-existe.json")]) == 2


def test_main_escribe_el_json_y_el_digest(tmp_path):
    fuentes = tmp_path / "fuentes.json"
    fuentes.write_text(json.dumps(config()), encoding="utf-8")

    def runner(red, usuario, n=30):
        return [video("https://www.tiktok.com/@dotcsv/video/1", vistas=412000,
                      compartidos=33372, senal=0.081, cuenta="dotcsv",
                      transcripcion="Mi jefe se califico solo y nadie le pidio pruebas")]

    codigo = diario.main(["--fuentes", str(fuentes),
                           "--salidas-dir", str(tmp_path / "salidas"),
                           "--hoy", str(tmp_path / "hoy.md")],
                          runner=runner, ahora=AHORA)
    assert codigo == 0
    crudo = tmp_path / "salidas" / "2026-10-25.json"
    md = tmp_path / "hoy.md"
    assert crudo.exists() and md.exists()

    datos = json.loads(crudo.read_text(encoding="utf-8"))
    assert datos["fecha"] == "2026-10-25"
    assert datos["candidatos"][0]["url"] == "https://www.tiktok.com/@dotcsv/video/1"
    assert datos["candidatos"][0]["cuadros"] == []

    lineas = md.read_text(encoding="utf-8").splitlines()
    assert len(lineas) < 60, "el digest es de una pantalla"


def test_el_json_se_escribe_sin_bom(tmp_path):
    fuentes = tmp_path / "fuentes.json"
    fuentes.write_text(json.dumps(config()), encoding="utf-8")

    def runner(red, usuario, n=30):
        return [video("https://www.tiktok.com/@dotcsv/video/1", cuenta="dotcsv")]

    diario.main(["--fuentes", str(fuentes),
                 "--salidas-dir", str(tmp_path / "salidas"),
                 "--hoy", str(tmp_path / "hoy.md")],
                runner=runner, ahora=AHORA)
    crudo = (tmp_path / "salidas" / "2026-10-25.json").read_bytes()
    assert crudo[:3] != b"\xef\xbb\xbf"


# ------------------------------------------------------------------ el digest

def test_el_digest_usa_punto_de_miles_y_coma_decimal():
    res = {"fecha": "2026-10-25", "redes": ["tiktok"], "vistos": {"tiktok": 138},
           "omitidas": [{"red": "instagram", "motivo": "sin acceso"}], "fallas": [],
           "candidatos": [video("https://www.tiktok.com/@dotcsv/video/1", cuenta="dotcsv",
                                vistas=412000, compartidos=33372, senal=0.081, duracion=12,
                                transcripcion="Mi jefe se califico solo y nadie le pidio pruebas")]}
    md = diario.render_digest(res)
    assert "412.000 vistas" in md
    assert "8,1% compartidos" in md
    assert "412.000" in md and "412,000" not in md
    assert "omitidas: Instagram (sin acceso)" in md
    assert "138 videos vistos" in md
    assert "1 a fondo" in md


def test_el_digest_sale_en_utf8_y_con_el_nombre_de_marca_de_las_redes():
    res = {"fecha": "2026-10-25", "redes": ["tiktok"], "vistos": {"tiktok": 138},
           "omitidas": [{"red": "instagram", "motivo": "sin acceso"}], "fallas": [],
           "candidatos": [video("https://www.tiktok.com/@dotcsv/video/1", red="tiktok",
                                cuenta="dotcsv", senal=0.081)]}
    md = diario.render_digest(res)
    assert "·" in md                      # separador del digest
    assert "Señal" in md                  # acento de la cabecera
    assert "| TikTok |" in md
    assert "omitidas: Instagram (sin acceso)" in md


def test_el_digest_avisa_cuando_no_hay_candidatos():
    res = {"fecha": "2026-10-25", "redes": ["tiktok"], "vistos": {"tiktok": 30},
           "omitidas": [], "fallas": [], "candidatos": []}
    md = diario.render_digest(res)
    assert "no hay candidatos" in md.lower()
    assert "## Top 3" not in md
    assert len(md.splitlines()) < 10


def test_el_gancho_del_digest_no_tiene_hashtags():
    res = {"fecha": "2026-10-25", "redes": ["tiktok"], "vistos": {"tiktok": 1},
           "omitidas": [], "fallas": [],
           "candidatos": [video("https://x/1", cuenta="demo",
                                texto="Mi jefe se califico solo #liderazgo #ia")]}
    md = diario.render_digest(res)
    assert "#liderazgo" not in md
    assert "Mi jefe se califico solo" in md


def test_los_cuadros_solo_se_piden_a_tiktok_y_youtube(monkeypatch):
    pedidos = []

    def cuadros(video, cookies=None, info=None):
        pedidos.append(video["red"])
        return [f"marca/radar/salidas/cuadros/{video['url']}.jpg"]

    monkeypatch.setattr(diario, "_extraer_cuadros", cuadros)

    def runner(red, usuario, n=30):
        return [video(f"https://{red}/1", red=red, cuenta="demo")]

    fuentes = config(redes={"tiktok": {"cuentas": ["a"], "urls": [], "min_vistas": 0},
                            "instagram": {"cuentas": ["b"], "urls": [], "min_vistas": 0}})
    res = diario.barrer(fuentes, ahora=AHORA, runner=runner, top=5)
    assert pedidos == ["tiktok"]
    por_red = {c["red"]: c for c in res["candidatos"]}
    assert por_red["tiktok"]["cuadros"]
    assert por_red["instagram"]["cuadros"] == []
    assert "bloquea la descarga" in por_red["instagram"]["nota"]


def test_baja_la_transcripcion_cuando_el_runner_no_la_traia(monkeypatch):
    monkeypatch.setattr(diario, "_info_video", lambda url, cookies=None: {"id": "x"})
    monkeypatch.setattr(radar, "bajar_transcripcion", lambda info: "texto hablado")

    def runner(red, usuario, n=30):
        return [video("https://www.tiktok.com/@dotcsv/video/1", transcripcion="")]

    fuentes = config(redes={"tiktok": {"cuentas": ["a"], "urls": [], "min_vistas": 0}})
    res = diario.barrer(fuentes, ahora=AHORA, runner=runner, top=5)
    assert res["candidatos"][0]["transcripcion"] == "texto hablado"


def test_el_digest_dice_que_red_se_omitio():
    def runner(red, usuario, n=30):
        return [video("https://www.tiktok.com/@dotcsv/video/1")] if red == "tiktok" else []

    fuentes = config(redes={"tiktok": {"cuentas": ["a"], "urls": [], "min_vistas": 0},
                            "instagram": {"cuentas": ["b"], "urls": [], "min_vistas": 0}})
    res = diario.barrer(fuentes, ahora=AHORA, runner=runner, top=5)
    texto = diario.render_digest(res)
    assert "omitidas" in texto
    assert "Instagram" in texto


def test_filtra_los_videos_muy_largos():
    """Una pieza de la marca dura de 12 a 20 s. Un tutorial de dos minutos no es
    una carpinteria tropicalizable: se filtra antes de rankear."""
    largos = [video("https://x/tutorial", vistas=50000, duracion=145),
              video("https://x/corto", vistas=50000, duracion=14)]

    def runner(red, usuario, n=30):
        return largos

    fuentes = config(redes={"tiktok": {"cuentas": ["a"], "urls": [], "min_vistas": 0,
                                        "duracion_max_s": 60}})
    res = diario.barrer(fuentes, ahora=AHORA, runner=runner, top=5)
    assert [c["url"] for c in res["candidatos"]] == ["https://x/corto"]


def test_el_filtro_de_duracion_no_tira_lo_que_no_se_sabe():
    """En Instagram y X la duracion no se lee del DOM: lo que no se sabe, pasa."""
    def runner(red, usuario, n=30):
        return [video("https://www.instagram.com/reel/1", red="instagram", duracion=None)]

    fuentes = config(redes={"instagram": {"cuentas": ["b"], "urls": [], "min_vistas": 0,
                                          "duracion_max_s": 60}})
    res = diario.barrer(fuentes, ahora=AHORA, runner=runner, top=5)
    assert len(res["candidatos"]) == 1


def test_los_posts_de_x_se_rankean_por_interacciones():
    """X no trae vistas, asi que su senal es 0. Sin la segunda llave, sus posts
    se hundirian al final del ranking; con ella, compiten de verdad."""
    def runner(red, usuario, n=30):
        return [video("https://x/chico", red="x", senal=0.0, vistas=None, likes=10),
                video("https://x/grande", red="x", senal=0.0, vistas=None, likes=5000)]

    fuentes = config(redes={"x": {"cuentas": ["rourke"], "urls": [], "min_vistas": 0}})
    res = diario.barrer(fuentes, ahora=AHORA, runner=runner, top=5)
    assert [c["url"] for c in res["candidatos"]] == ["https://x/grande", "https://x/chico"]


def test_avisa_cuando_la_red_no_deja_rankear():
    """Instagram y X sirven para ver formatos nuevos, pero no traen vistas:
    el digest tiene que decirlo, no dejar que parezcan los mas virales."""
    def runner(red, usuario, n=30):
        return [video("https://www.instagram.com/reel/1", red="instagram",
                      senal=0.0, vistas=None)]

    fuentes = config(redes={"instagram": {"cuentas": ["b"], "urls": [], "min_vistas": 0}})
    res = diario.barrer(fuentes, ahora=AHORA, runner=runner, top=5)
    assert "no deja rankear" in res["candidatos"][0]["nota"]
