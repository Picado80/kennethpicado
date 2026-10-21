"""Día 2: el sonido de cada pieza → <pieza>/mezcla.wav.

Capas: tu voz (una frase por escena, en el segundo en que empieza su escena), música original de kalimba sintetizada
acá (no usa muestras ni obras de terceros) que baja cuando hablás, y un sonido en cada golpe: barrido en los cortes,
«pop» en lo que aparece, teclas cuando se escribe y un golpe seco en el sello.

Uso (desde la raíz de kennethpicado):  <LIB>/.venv/Scripts/python.exe marca/produccion/dia2/mezcla.py <LIB> [pr1 d2 n1]
LIB es la carpeta de Lemo-Opuscar.
"""
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

LIB = os.path.abspath(sys.argv[1])
sys.path.insert(0, LIB)
from core.audio.sfx import SR, add, click, compress, ding, limit, lp, noise, pop, thump, whoosh  # noqa: E402

NOTAS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(n):
    return 12 * (int(n[-1]) + 1) + NOTAS[n[0]]


def kalimba(nota, dur=1.4, vel=.5):
    """Una lengüeta de kalimba: la fundamental, un parcial inarmónico que se apaga rápido y un clic de ataque."""
    f = 440 * 2 ** ((midi(nota) - 69) / 12)
    t = np.arange(int(dur * SR)) / SR
    x = np.sin(2 * np.pi * f * t) * np.exp(-t / .9) + .35 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / .08)
    x += .2 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / .4)
    ataque = np.minimum(1, t / .004)
    return (vel * ataque * x).astype(np.float32)

AQUI = os.path.dirname(os.path.abspath(__file__))


def mp3(ruta):
    crudo = subprocess.run(["ffmpeg", "-v", "error", "-i", ruta, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(crudo, np.float32).copy()


def musica(dur, bpm=96, base=.17):
    """Arpegio de kalimba sobre Do · La menor · Fa · Sol (dos compases cada uno) y un bajo suave en la fundamental."""
    buf = np.zeros((int((dur + 2) * SR), 2), np.float32)
    acordes = [("C4", "E4", "G4", "C5"), ("A3", "C4", "E4", "A4"), ("F3", "A3", "C4", "F4"), ("G3", "B3", "D4", "G4")]
    raiz = ["C2", "A1", "F2", "G2"]
    figura = [0, 1, 2, 3, 2, 1, 2, 3]
    corchea, compas = 30 / bpm, 240 / bpm
    t, i = 0.0, 0
    while t < dur:
        k = int(t // (2 * compas)) % 4
        x = kalimba(acordes[k][figura[i % 8]], 1.4, vel=.45 + .15 * (i % 4 == 0))
        add(buf, x.astype(np.float32), t, gain=base, pan=-.35 if i % 2 else .35)
        if i % 8 == 0:
            tt = np.arange(int(compas * SR)) / SR
            f = 440 * 2 ** ((midi(raiz[k]) - 69) / 12)
            b = (np.sin(2 * np.pi * f * tt) * np.exp(-tt / 1.1)).astype(np.float32)
            add(buf, b, t, gain=base * .55)
        t += corchea
        i += 1
    return buf


def bateria(dur, bpm, base=.4):
    """El beat: bombo en 1 y 3 (y un adelanto antes del 3 cada dos compases), palmas en 2 y 4, platillo cerrado en
    corcheas con acento a contratiempo. Todo sintetizado acá."""
    buf = np.zeros((int((dur + 2) * SR), 2), np.float32)
    tiempo = 60 / bpm
    tt = lambda d: np.arange(int(d * SR)) / SR  # noqa: E731
    t = tt(.35)
    bombo = (np.sin(2 * np.pi * (48 * t + 90 * (1 - np.exp(-t / .03)) * .03)) * np.exp(-t / .16)).astype(np.float32)
    t = tt(.22)
    palma = (lp(noise(.22), 4200) * np.exp(-t / .05)).astype(np.float32)
    palma = np.concatenate([palma[:int(.012 * SR)] * .6, palma])[:len(t)]
    t = tt(.06)
    plato = (np.diff(noise(.06), prepend=0) * np.exp(-t / .018)).astype(np.float32)
    k = 0
    while k * tiempo < dur:
        at, pos = k * tiempo, k % 4
        if pos in (0, 2):
            add(buf, bombo, at, gain=base * .9)
        if pos in (1, 3):
            add(buf, palma, at, gain=base * .5, pan=.1)
        if pos == 1 and (k // 4) % 2 == 1:
            add(buf, bombo, at + tiempo / 2, gain=base * .55)
        add(buf, plato, at, gain=base * .18, pan=-.3)
        add(buf, plato, at + tiempo / 2, gain=base * .28, pan=.3)
        k += 1
    return buf


def teclas(buf, desde, hasta, cps):
    t = desde
    while t < hasta:
        add(buf, click(pitch=1.4, v=.5).astype(np.float32), t, gain=.25, pan=.2)
        t += 1 / cps


def mezclar(nombre, dur, voces, golpes, bpm=96, fondo=1.0, baja=.62):
    """fondo: cuánto suena la música (1 = como el Día 2); baja: cuánto baja cuando hablás (0 a 1)."""
    n = int((dur + 1.5) * SR)
    voz = np.zeros((n, 2), np.float32)
    for ruta, t in voces:
        add(voz, mp3(ruta), t, gain=.95)
    sfx = np.zeros((n, 2), np.float32)
    for g in golpes:
        g(sfx)
    mus = (musica(dur, bpm) + bateria(dur, bpm))[:n] * fondo
    # la música baja cuando hablás (envolvente de la voz, suavizada)
    env = np.abs(voz[:, 0])
    k = int(.25 * SR)
    env = np.convolve(env, np.ones(k) / k, mode="same")
    env = env / (env.max() + 1e-9)
    mus *= (1 - baja * np.clip(env * 3, 0, 1))[:, None]
    # cuánto queda la música por debajo de la voz mientras hablás (para no adivinar)
    habla = env > .05
    rms = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
    print(f"  voz {rms(voz[habla]):.1f} dB · música bajo la voz {rms(mus[habla]):.1f} dB · música sola {rms(mus[~habla][:int(dur * SR)]):.1f} dB")
    total = voz + sfx + mus
    fin = int(dur * SR)
    rampa = np.linspace(1, 0, int(.5 * SR))
    total[fin - len(rampa):fin] *= rampa[:, None]
    total[fin:] = 0
    total = limit(np.stack([compress(total[:, 0]), compress(total[:, 1])], 1), ceil=.89)
    salida = os.path.join(AQUI, nombre, "mezcla.wav")
    sf.write(salida, total[:fin], SR)
    print(nombre, f"{dur:.1f} s", salida)


def W(t, v=.6):
    return lambda b: (add(b, whoosh(.35, v).astype(np.float32), t - .25, gain=.35), add(b, thump(.5).astype(np.float32), t, gain=.35))


def Pp(t, v=.6, pan=0):
    return lambda b: add(b, pop(v).astype(np.float32), t, gain=.35, pan=pan)


def T(t, v=.9):
    return lambda b: (add(b, thump(v).astype(np.float32), t, gain=.6), add(b, click(pitch=.7, v=.8).astype(np.float32), t, gain=.3))


def D(t):
    return lambda b: add(b, ding(.6).astype(np.float32), t, gain=.25)


def raya(t, d=.35):
    return lambda b: add(b, lp(noise(d), 2500).astype(np.float32) * np.linspace(.2, 1, int(round(d * SR))).astype(np.float32), t, gain=.12)


def inicios(durs):
    return [sum(durs[:k]) for k in range(len(durs))], sum(durs)


def pr1():
    s, dur = inicios([6.0, 6.0, 8.4, 7.8, 3.6, 2.4, 4.2, 12.6])
    v = [(os.path.join(AQUI, "pr1", "voz", f"{k}.mp3"), t) for k, t in zip("abcdefgh", s)]
    g = [W(t) for t in s[1:]]
    g += [lambda b: teclas(b, 4.25, 5.1, 18)]
    g += [Pp(s[1] + t, pan=p) for t, p in [(.45, .3), (.7, -.3), (1.6, -.3), (3.0, -.3)]]
    g += [Pp(s[2] + 1.9 + k * 1.95, .8) for k in range(3)]
    g += [Pp(s[3] + .2 + k * .3, .5) for k in range(3)] + [D(s[3] + 5.2)]
    g += [T(s[4], .6), raya(s[4] + 1.0, .5), raya(s[4] + 1.5, .3)]
    g += [T(s[5] + 1.1)] + [D(s[6] + 3.05)]
    g += [Pp(s[7] + t, .8, pan=(-1) ** k * .3) for k, t in enumerate((4.0, 5.05, 6.2, 7.4))]
    g += [T(s[7] + 8.95, .5), Pp(s[7] + 10.3, .7), Pp(s[7] + 11.6, .9), D(s[7] + 11.8)]
    mezclar("pr1", dur, v, g, bpm=100)


def d2():
    bpm = 100
    s, dur = inicios([7 * .6, 6 * .6, 5 * .6])
    v = [(os.path.join(AQUI, "d2", "voz", f"{k}.mp3"), t) for k, t in zip("abc", s)]
    g = [W(t) for t in s[1:]]
    g += [Pp(.3 + k * .08, .5, pan=(-1) ** k * .4) for k in range(7)]
    g += [Pp(s[1] + .25 + k * .16, .55) for k in range(7)]
    g += [T(s[2], .5), T(s[2] + .55)]
    g += [Pp(s[2] + 1.6, .6)]
    mezclar("d2", dur, v, g, bpm=bpm)


def n1():
    s, dur = inicios([6.0, 3.6, 2.4, 10.2, 6.6, 7.2, 3.6])
    v = [(os.path.join(AQUI, "n1", "voz", f"{k}.mp3"), t) for k, t in zip("abcdefg", s)]
    g = [W(t) for t in s[1:]]
    g += [lambda b: [add(b, click(pitch=1.1, v=.4).astype(np.float32), 1.6 + k / 12, gain=.18) for k in range(13)]]
    g += [Pp(s[1] + .1 + k * .08, .5, pan=(-1) ** k * .4) for k in range(7)]
    g += [T(s[2] + 1.55, .5)]
    g += [lambda b: teclas(b, s[3] + 1.9, s[3] + 2.8, 18), raya(s[3] + 3.0)]
    g += [Pp(s[3] + t, .7) for t in (4.0, 5.1, 6.3)] + [Pp(s[3] + 7.5, .9)]
    g += [Pp(s[4] + 1.4, .7), Pp(s[4] + 2.4, .7), T(s[4] + 5.4)]
    g += [raya(s[5] + 5.4, .5)]
    g += [Pp(s[6] + .15 + k * .05, .4) for k in range(7)]
    mezclar("n1", dur, v, g, bpm=100)


if __name__ == "__main__":
    piezas = sys.argv[2:] or ["pr1", "d2", "n1"]
    for p in piezas:
        {"pr1": pr1, "d2": d2, "n1": n1}[p]()
