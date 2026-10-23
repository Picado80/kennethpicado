"""Día 4 (sábado 24-oct): el sonido de cada pieza → <pieza>/mezcla.wav. Mismas capas que el Día 2 (dia2/mezcla.py), con la
música de fondo del Día 3 (unos 15 dB bajo la voz) y un sonido en cada golpe, en el segundo de la palabra que lo dispara.

Uso (desde la raíz de kennethpicado):  <LIB>/.venv/Scripts/python.exe marca/produccion/dia4/mezcla.py <LIB> [s1 s2 s3]
"""
import importlib.util
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("mezcla2", os.path.join(AQUI, "..", "dia2", "mezcla.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.AQUI = AQUI
W, Pp, T, D, raya, teclas = m.W, m.Pp, m.T, m.D, m.raya, m.teclas
FONDO, BAJA = .2, .85     # Kenneth, 21-oct: la música de fondo


def tiempos(pieza):
    d = json.load(open(os.path.join(AQUI, pieza, "tiempos.json"), encoding="utf-8"))
    s, dur = m.inicios(d["dur"])
    return s, dur, d["bpm"]


def voces(pieza, ids, s):
    return [(os.path.join(AQUI, pieza, "voz", f"{k}.mp3"), t) for k, t in zip(ids, s)]


def s1():
    s, dur, bpm = tiempos("s1")
    g = [W(t) for t in s[1:]]
    g += [Pp(0, .4), Pp(.05, .5), Pp(3.3, .6)]
    g += [Pp(s[1], .4), lambda b: teclas(b, s[1] + .4, s[1] + 3.85, 18), T(s[1] + .5, .6), Pp(s[1] + 3.4, .5)]
    g += [Pp(s[2] + .1, .5), raya(s[2] + 1.0, .35), Pp(s[2] + 1.0, .4), Pp(s[2] + 1.9, .5), Pp(s[2] + 2.9, .4), Pp(s[2] + 3.8, .6), Pp(s[2] + 4.9, .4)]
    g += [raya(s[2] + t, .35) for t in (5.76, 7.08, 7.9)] + [T(s[2] + 8.1, .7)]
    g += [Pp(s[3], .4), Pp(s[3] + .9, .6), raya(s[3] + 1.66, .35), raya(s[3] + 2.76, .35)]
    g += [Pp(s[4], .4), Pp(s[4] + 1.45, .7), raya(s[4] + 1.6, .6), D(s[4] + 2.9)]
    m.mezclar("s1", dur, voces("s1", "abcde", s), g, bpm=bpm, fondo=FONDO, baja=BAJA)


def s2():
    s, dur, bpm = tiempos("s2")
    v = voces("s2", "abc", [s[0], s[1], s[5]])
    g = [W(t) for t in s[1:]]
    g += [Pp(0, .4), Pp(2.4, .6)] + [Pp(t + .15, .5) for t in s[1:5]]
    g += [Pp(s[5] + .1 + k * .15, .45, pan=(-1) ** k * .3) for k in range(4)] + [Pp(s[5] + 3.0, .7), D(s[5] + 3.2)]
    m.mezclar("s2", dur, v, g, bpm=bpm, fondo=FONDO, baja=BAJA)


def s3():
    s, dur, bpm = tiempos("s3")
    g = [W(t) for t in s[1:]]
    g += [Pp(0, .4), Pp(.05, .5)] + [Pp(2.9 + k * .2, .45, pan=(-1) ** k * .3) for k in range(3)] + [T(3.4, .7)]
    g += [raya(s[1] + 1.9, .5)]
    g += [Pp(s[2] + .1, .5), raya(s[2] + .85, .35), T(s[2] + 1.0, .6), Pp(s[2] + 1.85, .5), Pp(s[2] + 2.3, .5)]
    g += [raya(s[2] + t, .35) for t in (3.82, 5.08, 5.88)]
    g += [Pp(s[3], .4), lambda b: teclas(b, s[3] + 1.5, s[3] + 4.3, 18)]
    g += [Pp(s[4] + .1, .5), T(s[4] + 1.9, .5), raya(s[4] + 2.6, .35), lambda b: teclas(b, s[4] + 2.85, s[4] + 3.5, 16), Pp(s[4] + 3.4, .6), D(s[4] + 3.6)]
    g += [Pp(s[5], .4), Pp(s[5] + 2.2, .5), lambda b: teclas(b, s[5] + 2.7, s[5] + 3.4, 10), Pp(s[5] + 3.3, .7), D(s[5] + 3.4)]
    m.mezclar("s3", dur, voces("s3", "abcdef", s), g, bpm=bpm, fondo=FONDO, baja=BAJA)


if __name__ == "__main__":
    for p in sys.argv[2:] or ["s1", "s2", "s3"]:
        {"s1": s1, "s2": s2, "s3": s3}[p]()
