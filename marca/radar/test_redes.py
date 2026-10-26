"""Pruebas de la capa de redes. No pegan a internet salvo la de integración, que va con skip."""
import sys
from pathlib import Path

import pytest

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import redes  # noqa: E402


# ---------------------------------------------------------------- datos sintéticos

TIKTOK = {
    "webpage_url": "https://www.tiktok.com/@dotcsv/video/7696559496658685206",
    "uploader": "dotcsv",
    "title": "El mayor hito de la IA aplicada a las matemáticas",
    "description": "El mayor hito de la IA aplicada a las matemáticas #dotcsv #IA",
    "view_count": 7968,
    "like_count": 374,
    "comment_count": 10,
    "repost_count": 11,
    "save_count": 41,
    "upload_date": "20261014",
    "duration": 99,
}

YOUTUBE = {
    "webpage_url": "https://www.youtube.com/shorts/abc123",
    "channel": "TIFF in Tech",
    "title": "How AI actually works",
    "view_count": 120000,
    "like_count": 5400,
    "comment_count": 210,
    "upload_date": "20261020",
    "duration": 42,
}

INSTAGRAM = {
    "webpage_url": "https://www.instagram.com/reel/ABC123/",
    "cuenta": "dotcsv",
    "texto": "Como leer un reel sin credenciales",
    "view_count": None,
    "like_count": 1250,
    "comment_count": None,
}

X = {
    "webpage_url": "https://x.com/i/status/1900000000000000000",
    "cuenta": "rourke",
    "texto": "El mejor libro de operaciones que leí",
    "view_count": 15000,
    "like_count": 320,
    "comment_count": 18,
    "repost_count": 47,
}


# ---------------------------------------------------------------- normalizar y señal

def test_normalizar_tiktok_trae_los_campos_de_ytdlp():
    v = redes.normalizar("tiktok", TIKTOK)
    assert list(v.keys()) == redes.COLUMNAS
    assert v["url"].endswith("/video/7696559496658685206")
    assert v["red"] == "tiktok" and v["cuenta"] == "dotcsv"
    assert v["vistas"] == 7968 and v["likes"] == 374 and v["comentarios"] == 10
    assert v["compartidos"] == 11 and v["guardados"] == 41
    assert v["duracion_s"] == 99
    assert v["fecha"].startswith("2026-10-14")
    assert v["señal_tipo"] == "compartidos"
    assert v["señal"] == pytest.approx(11 / 7968)


def test_normalizar_no_inventa_lo_que_falta():
    v = redes.normalizar("instagram", {"webpage_url": "u"})
    assert v["vistas"] is None and v["likes"] is None and v["comentarios"] is None
    assert v["compartidos"] is None and v["guardados"] is None
    assert v["fecha"] is None
    assert v["señal"] == 0.0


def test_normalizar_cero_no_es_none():
    v = redes.normalizar("x", {"webpage_url": "u", "view_count": 100, "like_count": 0})
    assert v["likes"] == 0 and v["vistas"] == 100
    assert v["señal"] == 0.0


def test_normalizar_fecha_desde_timestamp():
    v = redes.normalizar("tiktok", {"webpage_url": "u", "timestamp": 1791244800})
    assert v["fecha"] == "2026-10-06T00:00:00+00:00"


def test_normalizar_usa_release_timestamp_si_no_hay_timestamp():
    v = redes.normalizar("x", {"webpage_url": "u", "release_timestamp": 1791244800})
    assert v["fecha"].startswith("2026-10-06")


def test_normalizar_youtube_usa_interaccion():
    v = redes.normalizar("youtube", YOUTUBE)
    assert v["vistas"] == 120000 and v["señal_tipo"] == "interaccion"
    assert v["señal"] == pytest.approx((5400 + 210) / 120000)


def test_normalizar_instagram_con_likes_sin_vistas():
    v = redes.normalizar("instagram", INSTAGRAM)
    assert v["likes"] == 1250 and v["vistas"] is None
    assert v["señal"] == 0.0 and v["señal_tipo"] == "interaccion"


def test_normalizar_x_con_reposts():
    v = redes.normalizar("x", X)
    assert v["compartidos"] == 47 and v["señal_tipo"] == "interaccion"
    assert v["señal"] == pytest.approx((320 + 18) / 15000)


# ---------------------------------------------------------------- señal

def test_senal_tiktok_con_compartidos_usa_compartidos():
    valor, tipo = redes.senal({"red": "tiktok", "vistas": 1000, "likes": 900,
                               "comentarios": 100, "compartidos": 50})
    assert tipo == "compartidos" and valor == pytest.approx(0.05)


def test_senal_tiktok_sin_compartidos_cae_a_interaccion():
    valor, tipo = redes.senal({"red": "tiktok", "vistas": 1000, "likes": 90,
                               "comentarios": 10, "compartidos": None})
    assert tipo == "interaccion" and valor == pytest.approx(0.1)


def test_senal_otras_redes_siempre_interaccion():
    for red in ("instagram", "youtube", "x"):
        valor, tipo = redes.senal({"red": red, "vistas": 1000, "likes": 50,
                                   "comentarios": 10, "compartidos": 999})
        assert tipo == "interaccion" and valor == pytest.approx(0.06)


def test_senal_sin_vistas_es_cero():
    assert redes.senal({"red": "tiktok", "vistas": None, "likes": 10,
                        "comentarios": 1, "compartidos": 5}) == (0.0, "compartidos")
    assert redes.senal({"red": "x", "vistas": 0, "likes": 10}) == (0.0, "interaccion")


def test_senal_usa_none_como_cero_pero_no_lo_confunde():
    valor, tipo = redes.senal({"red": "x", "vistas": 100, "likes": None, "comentarios": None})
    assert valor == 0.0 and tipo == "interaccion"


# ---------------------------------------------------------------- urls y disponibilidad

def test_url_cuenta_de_las_cuatro_redes():
    assert redes.url_cuenta("tiktok", "dotcsv") == "https://www.tiktok.com/@dotcsv"
    assert redes.url_cuenta("instagram", "dotcsv") == "https://www.instagram.com/dotcsv/"
    assert redes.url_cuenta("x", "rourke") == "https://x.com/rourke"
    assert redes.url_cuenta("youtube", "tiffintech") == "https://www.youtube.com/@tiffintech/shorts"


def test_url_cuenta_quita_el_arroba():
    assert redes.url_cuenta("tiktok", "@dotcsv") == "https://www.tiktok.com/@dotcsv"


def test_url_cuenta_de_red_que_no_existe():
    assert redes.url_cuenta("myspace", "dotcsv") == ""


def test_listar_redes():
    assert redes.listar_redes() == ["tiktok", "instagram", "x", "youtube"]


def test_disponibles_devuelve_las_cuatro_claves():
    d = redes.disponibles()
    assert set(d.keys()) == {"tiktok", "instagram", "x", "youtube"}
    assert all(isinstance(v, bool) for v in d.values())


# ---------------------------------------------------------------- obtener sin red

def test_obtener_devuelve_lista_vacia_si_la_red_no_existe():
    assert redes.obtener("myspace", "dotcsv") == []


def test_obtener_devuelve_lista_vacia_si_el_usuario_no_existe():
    assert redes.obtener("tiktok", "") == []


def test_obtener_no_levanta_cuando_falla_ytdlp(monkeypatch):
    def revienta(*_a, **_k):
        raise RuntimeError("TikTok bloquea la cuenta")

    monkeypatch.setattr(redes, "_por_ytdlp", revienta)
    assert redes.obtener("tiktok", "dotcsv") == []


def test_obtener_no_levanta_cuando_falla_el_navegador(monkeypatch):
    def revienta(*_a, **_k):
        raise RuntimeError("Chrome no esta")

    monkeypatch.setattr(redes, "_por_dom", revienta)
    assert redes.obtener("instagram", "dotcsv") == []


def test_obtener_no_levanta_si_el_dom_esta_vacio(monkeypatch):
    monkeypatch.setattr(redes.chrome, "dom", lambda *_a, **_k: "")
    monkeypatch.setattr(redes, "_html_publico", lambda *_a, **_k: "")
    assert redes.obtener("x", "rourke") == []


def test_obtener_devuelve_las_columnas_exactas(monkeypatch):
    monkeypatch.setattr(redes, "_por_ytdlp", lambda *_a, **_k: [TIKTOK])
    videos = redes.obtener("tiktok", "dotcsv")
    assert len(videos) == 1
    v = videos[0]
    assert list(v.keys()) == redes.COLUMNAS
    assert v["cuenta"] == "dotcsv" and v["fuente"] == "tiktok @dotcsv"
    assert v["red"] == "tiktok"
    assert v["señal_tipo"] == "compartidos"


# ---------------------------------------------------------------- parsers del DOM (puros)

def test_parse_instagram_saca_los_reels_y_los_likes():
    html = (
        '<a href="/reel/AAA111/"><img alt="Un reel de prueba" src="x.jpg"></a>'
        '<span>1,234 likes</span>'
        '<a href="/reel/BBB222/"><img alt="Otro reel" src="y.jpg"></a>'
        '<span>99 likes</span>'
    )
    raws = redes._parse_instagram(html, 10)
    assert len(raws) == 2
    assert raws[0]["webpage_url"] == "https://www.instagram.com/reel/AAA111/"
    assert raws[0]["like_count"] == 1234
    assert raws[0]["texto"] == "Un reel de prueba"
    assert raws[1]["like_count"] == 99
    assert raws[0]["view_count"] is None


def test_parse_instagram_sin_contadores_no_inventa():
    raws = redes._parse_instagram('<a href="/reel/AAA111/"><img alt="x" src="y"></a>', 10)
    assert raws[0]["like_count"] is None and raws[0]["view_count"] is None


def test_parse_x_saca_los_estados_y_los_contadores():
    html = (
        '<article data-testid="tweet"><a href="/rourke/status/1900000000000000000">ver</a>'
        '<div data-testid="tweetText">El mejor libro de operaciones</div>'
        '<span>18 replies</span><span>47 reposts</span><span>320 likes</span>'
        '<span>15K views</span></article>'
    )
    raws = redes._parse_x(html, 10)
    assert len(raws) == 1
    r = raws[0]
    assert r["webpage_url"] == "https://x.com/i/status/1900000000000000000"
    assert r["like_count"] == 320 and r["comment_count"] == 18
    assert r["repost_count"] == 47 and r["view_count"] == 15000
    assert "operaciones" in r["texto"]


def test_parse_x_sin_contadores_no_inventa():
    html = '<article data-testid="tweet"><a href="/rourke/status/1900000000000000000">v</a></article>'
    raws = redes._parse_x(html, 10)
    assert raws[0]["like_count"] is None and raws[0]["view_count"] is None


def test_parse_x_lee_el_payload_que_manda_el_servidor():
    # X se sirve renderizado: los contadores van escapados dentro del HTML y el
    # contenido de cada estado va ANTES de su marca entry_id.
    html = (
        '\\"counts\\":{\\"bookmark_count\\":3,\\"favorite_count\\":120,'
        '\\"quote_count\\":0,\\"reply_count\\":7,\\"retweet_count\\":5},'
        '\\"details\\":{\\"created_at_ms\\":1767225600000,'
        '\\"full_text\\":\\"El mejor libro de operaciones que le\\u00ed\\"},'
        '\\"entry_id\\":\\"tweet-1900000000000000000\\"'
    )
    raws = redes._parse_x(html, 10)
    assert len(raws) == 1
    r = raws[0]
    assert r["webpage_url"] == "https://x.com/i/status/1900000000000000000"
    assert r["like_count"] == 120 and r["comment_count"] == 7
    assert r["repost_count"] == 5 and r["save_count"] == 3
    assert r["view_count"] is None
    assert "libro de operaciones" in r["texto"]
    assert r["created_at_ms"] == 1767225600000


def test_parse_x_une_cada_estado_con_sus_contadores():
    # Dos estados seguidos: cada uno con sus números, sin mezclarlos.
    html = (
        '\\"counts\\":{\\"favorite_count\\":1,\\"reply_count\\":2,\\"retweet_count\\":3},'
        '\\"full_text\\":\\"primero\\"},\\"entry_id\\":\\"tweet-111\\"'
        '\\"counts\\":{\\"favorite_count\\":40,\\"reply_count\\":50,\\"retweet_count\\":60},'
        '\\"full_text\\":\\"segundo\\"},\\"entry_id\\":\\"tweet-222\\"'
    )
    raws = redes._parse_x(html, 10)
    assert [r["webpage_url"] for r in raws] == ["https://x.com/i/status/111",
                                                "https://x.com/i/status/222"]
    assert raws[0]["like_count"] == 1 and raws[1]["like_count"] == 40
    assert raws[1]["texto"] == "segundo"


def test_x_desde_el_dom_pintado_usa_el_aria_label():
    html = (
        '<article data-testid="tweet"><a href="/rourke/status/1900000000000000000">v</a>'
        '<div data-testid="tweetText">Hola</div>'
        '<span aria-label="18 replies">18</span><span>320 likes</span></article>'
    )
    raws = redes._parse_x(html, 10)
    assert raws[0]["comment_count"] == 18 and raws[0]["like_count"] == 320


def test_x_desde_el_dom_pintado_usa_el_data_testid():
    # Cuando no hay aria-label, el contador cuelga del data-testid.
    html = (
        '<article data-testid="tweet"><a href="/rourke/status/1900000000000000000">v</a>'
        '<div data-testid="reply"><span>18</span></div>'
        '<div data-testid="like"><span>320</span></div></article>'
    )
    raws = redes._parse_x(html, 10)
    assert raws[0]["comment_count"] == 18 and raws[0]["like_count"] == 320


def test_desescapar_suelta_los_escapes_de_json():
    assert redes._desescapar('hola\\"mundo\\"') == 'hola"mundo"'
    assert redes._desescapar("linea\\nnueva") == "linea nueva"


def test_ultimo_numero_toma_el_ultimo_valor():
    assert redes._ultimo_numero('"favorite_count":1 "favorite_count":9', "favorite_count") == 9
    assert redes._ultimo_numero("nada aqui", "favorite_count") is None


# ---------------------------------------------------------------- integración (opcional)

@pytest.mark.skipif(not redes.disponibles()["tiktok"],
                    reason="yt-dlp no esta disponible en esta maquina")
def test_integracion_tiktok_devuelve_tres_videos():
    """Opcional: si la red no responde, se salta. Si responde, trae 3 videos con las columnas."""
    videos = redes.obtener("tiktok", "dotcsv", n=3)
    if not videos:
        pytest.skip("TikTok no respondio (sin red o bloqueado)")
    assert len(videos) == 3
    for v in videos:
        assert list(v.keys()) == redes.COLUMNAS
        assert v["red"] == "tiktok" and v["cuenta"] == "dotcsv"
        assert v["url"].startswith("https://www.tiktok.com/")
