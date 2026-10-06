"""Pruebas del radar. No tocan la red ni llaman a yt-dlp: usan fixtures con la forma de su salida -J."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import radar  # noqa: E402

AHORA = datetime(2026, 10, 7, tzinfo=timezone.utc)
CUENTA = json.loads((AQUI / "fixtures" / "cuenta.json").read_text(encoding="utf-8"))
VIDEO = json.loads((AQUI / "fixtures" / "video.json").read_text(encoding="utf-8"))


def videos():
    return [radar.normalizar(e, "cuenta demo") for e in CUENTA["entries"] if e]


def test_normalizar_toma_los_campos_de_ytdlp():
    v = radar.normalizar(CUENTA["entries"][0], "cuenta demo")
    assert v["cuenta"] == "demo"
    assert v["vistas"] == 120000 and v["compartidos"] == 6000 and v["guardados"] == 3000
    assert v["url"].endswith("/video/1") and v["fecha"].startswith("2026-10-06")


def test_normalizar_no_inventa_lo_que_falta():
    v = radar.normalizar({"webpage_url": "u"}, "url u")
    assert v["vistas"] is None and v["compartidos"] is None and v["fecha"] is None


def test_filtrar_saca_viejos_pocas_vistas_y_duplicados():
    lista = videos() + [radar.normalizar(VIDEO, "url x")]
    ids = [v["url"].rsplit("/", 1)[1] for v in radar.filtrar(lista, 7, 20000, AHORA)]
    assert ids == ["1", "2", "5"]


def test_ordenar_por_porcentaje_de_compartidos_y_respeta_top():
    elegidos = radar.ordenar(radar.filtrar(videos(), 7, 20000, AHORA), 2)
    assert [v["url"].rsplit("/", 1)[1] for v in elegidos] == ["1", "5"]  # 5% y 2%; el 2 (1%) queda fuera


def test_gancho_sin_hashtags_y_corto():
    g = radar.gancho({"texto": "Mi jefe se calificó solo #liderazgo #ia"})
    assert "#" not in g and g.startswith("Mi jefe")
    largo = radar.gancho({"texto": " ".join(["palabra"] * 20)})
    assert largo.endswith("...") and len(largo.split()) == 13


def test_texto_vtt_sin_tiempos_ni_repetidos():
    vtt = "WEBVTT\n\n1\n00:00:00.000 --> 00:00:01.000\nHola <b>gente</b>\n\n2\n00:00:01.000 --> 00:00:02.000\nHola gente\nchau\n"
    assert radar.texto_vtt(vtt) == "Hola gente chau"


def test_elegir_subtitulo_prefiere_espanol():
    assert radar.elegir_subtitulo(CUENTA["entries"][4]) == "https://x/sub.vtt"
    assert radar.elegir_subtitulo({"subtitles": {"en": [{"ext": "vtt", "url": "e"}]}}) is None


def test_main_escribe_md_y_json_y_anota_la_fuente_que_falla(tmp_path):
    fuentes = tmp_path / "fuentes.json"
    fuentes.write_text(json.dumps({"cuentas": ["demo", "rota"], "hashtags": [], "urls": [],
                                   "dias": 7, "min_vistas": 20000, "top": 15}), encoding="utf-8")

    def runner(base, url, n, cookies):
        if url.endswith("@rota"):
            raise RuntimeError("TikTok bloqueo la cuenta")
        return [e for e in CUENTA["entries"] if e]

    codigo = radar.main(["--fuentes", str(fuentes), "--semanas-dir", str(tmp_path / "s"),
                         "--salidas-dir", str(tmp_path / "o")],
                        runner=runner, transcriptor=lambda info: "texto hablado", ahora=AHORA)
    assert codigo == 0
    md = (tmp_path / "s" / "2026-S41-radar.md").read_text(encoding="utf-8")
    filas = [l for l in md.splitlines() if l.startswith("| ") and l[2].isdigit()]
    assert len(filas) == 3 and "5.0%" in filas[0]
    assert "cuenta rota: TikTok bloqueo la cuenta" in md
    datos = json.loads((tmp_path / "o" / "2026-S41.json").read_text(encoding="utf-8"))
    assert datos["elegidos"][0]["transcripcion"] == "texto hablado"


def test_main_sale_con_1_si_fallan_todas(tmp_path):
    fuentes = tmp_path / "fuentes.json"
    fuentes.write_text(json.dumps({"cuentas": ["rota"]}), encoding="utf-8")

    def runner(*_):
        raise RuntimeError("sin red")

    assert radar.main(["--fuentes", str(fuentes), "--semanas-dir", str(tmp_path),
                       "--salidas-dir", str(tmp_path)], runner=runner, ahora=AHORA) == 1


def test_correr_ytdlp_convierte_null_en_error_legible(monkeypatch):
    class R:
        returncode, stdout, stderr = 1, "null\n", "ERROR: [TikTok] Unable to download webpage: 403\n"

    monkeypatch.setattr(radar.subprocess, "run", lambda *a, **k: R())
    try:
        radar.correr_ytdlp(["yt-dlp"], "https://www.tiktok.com/@x", 5, None)
        assert False, "tenia que fallar"
    except RuntimeError as e:
        assert "Unable to download webpage: 403" in str(e)


def test_main_sin_fuentes_sale_con_2(tmp_path):
    assert radar.main(["--fuentes", str(tmp_path / "no-existe.json")]) == 2
