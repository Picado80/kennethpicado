"""Día 3: el sonido de cada pieza → <pieza>/mezcla.wav. Usa las mismas capas que el Día 2 (dia2/mezcla.py): tu voz,
la kalimba y la batería hechas acá, la música que baja cuando hablás y un sonido en cada golpe, en el segundo de la
palabra que lo dispara (voz/palabras.json).

Uso (desde la raíz de kennethpicado):  <LIB>/.venv/Scripts/python.exe marca/produccion/dia3/mezcla.py <LIB> [rn1 j2]
"""
import importlib.util
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("mezcla2", os.path.join(AQUI, "..", "dia2", "mezcla.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.AQUI = AQUI                       # las mezclas se escriben en dia3/<pieza>/mezcla.wav
W, Pp, T, D, raya, teclas = m.W, m.Pp, m.T, m.D, m.raya, m.teclas


def tiempos(pieza):
    d = json.load(open(os.path.join(AQUI, pieza, "tiempos.json"), encoding="utf-8"))
    s, dur = m.inicios(d["dur"])
    return s, dur, d["bpm"]


def voz(pieza, k):
    return os.path.join(AQUI, pieza, "voz", f"{k}.mp3")


def rn1():
    s, dur, bpm = tiempos("rn1")
    # la frase «e» (Netflix y lo que dice el jefe) cruza dos escenas; la «f» va con el cierre
    v = [(voz("rn1", k), s[i]) for k, i in zip("abcdef", (0, 1, 2, 3, 4, 6))]
    g = [W(t) for t in s[1:]]
    g += [Pp(.1 + k * .3, .5, pan=(-1) ** k * .3) for k in range(3)] + [T(3.35)]
    g += [Pp(s[1] + 1.9 + k * .18, .4) for k in range(4)] + [T(s[1] + 2.7, .7), Pp(s[1] + 4.1)]
    g += [raya(s[2] + 1.85), Pp(s[2] + 3.7), raya(s[2] + 5.8)]
    g += [Pp(s[3] + 4.4 + k * .85, .55, pan=(-1) ** k * .3) for k in range(3)] + [Pp(s[3] + 7.0)]
    g += [lambda b: teclas(b, s[3] + 9.0, s[3] + 10.0, 18), D(s[3] + 10.5), Pp(s[3] + 10.8, .5)]
    g += [raya(s[4] + 4.6, .5), raya(s[4] + 4.7, .5), raya(s[4] + 6.0, .3)]
    g += [T(s[5] + 1.5), Pp(s[5] + 3.35), Pp(s[5] + 4.75), raya(s[5] + 5.7, .45)]
    g += [Pp(s[6] + 1.4, .5), Pp(s[6] + 2.0), Pp(s[6] + 3.3, .8), D(s[6] + 5.2)]
    m.mezclar("rn1", dur, v, g, bpm=bpm)


def j2():
    s, dur, bpm = tiempos("j2")
    v = [(voz("j2", k), t) for k, t in zip("abcdef", s)]
    g = [W(t) for t in s[1:]]
    g += [Pp(.1, .6), Pp(1.95, .4)] + [Pp(2.4 + k * .3, .5, pan=(-1) ** k * .3) for k in range(4)] + [Pp(4.1, .7), raya(5.2, .45)]
    g += [Pp(s[1] + .1), Pp(s[1] + 1.95), T(s[1] + 2.7, .6)]
    g += [lambda b: teclas(b, s[2] + .5, s[2] + 1.37, 18), lambda b: teclas(b, s[2] + 3.0, s[2] + 4.0, 18)]
    g += [Pp(s[2] + t, .7) for t in (5.6, 6.4, 7.5)] + [D(s[2] + 7.6)]
    g += [Pp(s[3] + .3), Pp(s[3] + 3.5), raya(s[3] + 5.1), T(s[3] + 5.9)]
    g += [Pp(s[4] + t, .7) for t in (2.45, 4.35, 5.2)]
    g += [Pp(s[5] + 2.4), Pp(s[5] + 3.9, .8), D(s[5] + 5.0)]
    m.mezclar("j2", dur, v, g, bpm=bpm)


if __name__ == "__main__":
    for p in sys.argv[2:] or ["rn1", "j2"]:
        {"rn1": rn1, "j2": j2}[p]()
