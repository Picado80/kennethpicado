"""J1: sonido de la pizarra, voz y música → out/mix.wav.

Uso:  <LIB>/.venv/Scripts/python.exe mix.py <LIB>        (LIB = la carpeta de Lemo-Opuscar)

Cada trazo suena con la curva de velocidad de la mano (despacio, rápido, despacio) y se ubica a izquierda o
derecha según dónde cae en el cuadro. Capas: sala | marcador, borrador y tapa | voz | música (más baja bajo la voz).
La técnica del marcador y del borrador viene del demo de pizarra de Lemo-Opuscar (MIT); la música es de este video.
"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

LIB = os.path.abspath(sys.argv[1])
sys.path.insert(0, LIB)
from core.audio.sfx import SR, add, bp, compress, hp, limit, lp  # noqa: E402

try:
    from core.audio.sampler import room as sala
except Exception:                                       # sin la sala de la biblioteca, queda seco
    sala = lambda x, **k: x                             # noqa: E731

AQUI = os.path.dirname(os.path.abspath(__file__))
ev = json.load(open(os.path.join(AQUI, "events.json"), encoding="utf-8"))
E, DUR = ev["ev"], ev["dur"]
C = next(e for e in E if e["type"] == "cues")
BEAT = C["BEAT"]
rng = np.random.default_rng(11)
NS = int((DUR + 1) * SR)
fol, amb, mus = (np.zeros((NS, 2), np.float32) for _ in range(3))
tt = lambda d: np.arange(int(d * SR)) / SR             # noqa: E731
db = lambda x: 10 ** (x / 20)                           # noqa: E731
dec = lambda d, tau: np.exp(-tt(d) / tau)               # noqa: E731


def put(buf, x, t, g=1.0, pan=0.0):
    if 0 <= t < DUR:
        add(buf, np.asarray(x, np.float32), t, g, pan)


# ───────── marcador sobre pizarra brillante
_banda = {}


def banda(n, lo, hi):
    k = (round(lo), round(hi))
    if k not in _banda:
        _banda[k] = bp(rng.standard_normal(SR * 8), lo, hi, 2).astype(np.float32)
    b = _banda[k]
    i = int(rng.integers(0, len(b) - n - 1))
    return b[i:i + n]


BRILLO = {"tinta": 1.0, "azul": 0.92, "rojo": 1.12}


def marcador(dur, largo, tipo, pen, z=1.0, chirrido=None):
    d = max(0.03, dur)
    n = int(d * SR)
    u = np.linspace(0, 1, n)
    v = 1 - 0.8 * np.cos(2 * np.pi * u)                 # velocidad de la mano
    a = (v / 1.8) ** 0.8 * np.minimum(1, u * d / 0.006) * np.minimum(1, (1 - u) * d / 0.012)
    br = BRILLO.get(pen, 1.0)
    siseo = banda(n, 2200 * br, 7500 * br) * (0.55 + 0.45 * v / 1.8)
    cuerpo = banda(n, 500 * br, 1500 * br) * 0.45
    grano = (rng.random(n) < 0.004 * (1 + v)) * rng.standard_normal(n) * 0.8
    x = (siseo + cuerpo + bp(grano, 1500, 6000)) * a
    quiere = chirrido if chirrido is not None else (largo > 140 and rng.random() < 0.28)
    if quiere and d > 0.12:                              # el chirrido del marcador seco
        s0 = rng.uniform(0.15, 0.5) * d
        sd = min(d - s0, rng.uniform(0.07, 0.16))
        if sd > 0.03:
            m = int(sd * SR)
            ts = np.arange(m) / SR
            f = rng.uniform(1500, 2600) * br * (1 + 0.03 * np.sin(2 * np.pi * rng.uniform(7, 13) * ts))
            sq = (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)) * np.sin(np.pi * ts / sd) ** 1.5 * 0.35
            i0 = int(s0 * SR)
            x[i0:i0 + m] += sq[:len(x) - i0]
    k = int(0.004 * SR)
    x[:k] += bp(rng.standard_normal(k), 2500, 6500) * np.linspace(1, 0, k) * 1.4      # el golpecito al apoyar
    return x * 0.32 * min(1.3, z ** 0.5)


def toque(z=1.0):
    n = int(0.03 * SR)
    return bp(rng.standard_normal(n), 1800, 6000) * dec(0.03, 0.004) * 1.2 * 0.3 * min(1.3, z ** 0.5)


def borrador(d, pasadas=5):
    n = int(d * SR)
    t = tt(d)[:n]
    base = bp(rng.standard_normal(n), 250, 2600) * 0.6 + bp(rng.standard_normal(n), 2500, 6000) * 0.15
    mod = 0.45 + 0.55 * np.abs(np.sin(np.pi * t / d * pasadas))
    return base * mod * np.minimum(1, t / 0.04) * np.minimum(1, (d - t) / 0.06) * 0.5


def soplo(d, v=1.0):                                    # aire: un marcador que llega o la cámara que corre
    n = int(d * SR)
    t = tt(d)[:n]
    return bp(rng.standard_normal(n), 300, 2400) * np.sin(np.pi * t / d) ** 2 * 0.35 * v


def anillo(fs, taus, amps, d):
    t = tt(d)
    x = np.zeros(len(t))
    for f, ta, am in zip(fs, taus, amps):
        x += np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t / ta) * am
    return x


def tapa():                                             # dos clics de plástico: el marcador se tapa
    d = 0.2
    x = np.zeros(int(d * SR))
    for k, o in enumerate([0, 0.045]):
        i = int(o * SR)
        c = bp(rng.standard_normal(int(0.006 * SR)), 2500, 9000) * np.linspace(1, 0, int(0.006 * SR))
        x[i:i + len(c)] += c * (1 - 0.4 * k)
        r = anillo([2600], [0.015], [0.4], 0.06)
        x[i:i + len(r)] += r
    return x * 0.7


t_enredo = next(e["t"] for e in E if e["type"] == "stroke" and e.get("len", 0) > 3000)
for e in E:
    ty, t = e["type"], e["t"]
    pan, z = e.get("pan", 0), e.get("z", 1)
    fuera = db(-9) if e.get("on", 1) == 0 else 1
    if ty in ("stroke", "write", "dash"):
        es_enredo = ty == "stroke" and abs(t - t_enredo) < 1e-3
        put(fol, marcador(e["dur"], e["len"], ty, e.get("pen"), z, chirrido=True if es_enredo else None), t, fuera * (0.8 if ty == "write" else 1.0) * (1.25 if es_enredo else 1), pan)
        if es_enredo:                                     # el enredo chirría varias veces
            for k in range(3):
                put(fol, marcador(e["dur"] / 3, 400, "stroke", "azul", z, chirrido=True), t + e["dur"] * k / 3, 0.7, pan)
    elif ty == "tap":
        put(fol, toque(z), t, fuera, pan)
    elif ty == "erase":
        put(fol, borrador(e["dur"], 5 if e["dur"] > 0.8 else 1), t, 1.15, 0.05)
    elif ty == "tapa":
        put(fol, tapa(), t, 1.0, 0.3)

# marcadores que llegan o se van tras una pausa larga
por_pen = {}
for e in E:
    if e["type"] in ("stroke", "write", "dash", "tap"):
        por_pen.setdefault(e["pen"], []).append(e)
for pen, L in por_pen.items():
    L.sort(key=lambda e: e["t"])
    for a, b in zip(L, L[1:]):
        if b["t"] - (a["t"] + a["dur"]) > 0.75:
            put(fol, soplo(0.38, 0.3), a["t"] + a["dur"], 1, 0.5)
            put(fol, soplo(0.42, 0.4), b["t"] - 0.42, 1, 0.4)
    put(fol, soplo(0.42, 0.4), L[0]["t"] - 0.42, 1, 0.4)

# la cámara cuando corre: baja por la flecha, va a la hoja, retrocede y vuelve arriba
for t0, d, v in [(C["tFlecha"] + 0.25, 1.4, 0.35), (C["tVuelve"], 0.8, 0.5), (C["VO"]["b"] - 0.25, 0.8, 0.45), (C["tJerga"] - 0.42, 0.75, 0.85)]:
    put(fol, soplo(d, v), t0, 1, 0)

# ───────── sala
tono = lp(rng.standard_normal(NS), 900) * 0.010 + lp(rng.standard_normal(NS), 180) * 0.012
amb[:, 0] += tono
amb[:, 1] += np.roll(tono, 311)

# ───────── voz (mp3 → 48 kHz mono), compresión suave y un poco de sala
voz = np.zeros(NS, np.float32)
for ident, t0 in C["VO"].items():
    crudo = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(AQUI, "voz", ident + ".mp3"), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                           capture_output=True, check=True).stdout
    y = np.frombuffer(crudo, np.float32)
    i = int(t0 * SR)
    voz[i:i + len(y)] += y[:NS - i]
voz = hp(voz, 70)
voz = compress(voz / (np.abs(voz).max() + 1e-9) * 0.8, thr=0.2, ratio=3.0, att=0.004, rel=0.1).astype(np.float32)
vo = np.stack([voz, voz], 1)
vo = (vo * 0.88 + sala(vo, size=0.2, mix=0.1) * 0.12).astype(np.float32)

# ───────── música: kalimba y marimba sintetizadas, 96 por minuto
MIDI = lambda n: 440 * 2 ** ((n - 69) / 12)            # noqa: E731
D3, A3, D4, E4, FS4, GS4, A4, B4, D5, FS5, D6 = 50, 57, 62, 64, 66, 68, 69, 71, 74, 78, 86


def kalimba(nota, vel=1.0, largo=1.4):
    t = tt(largo)
    f = MIDI(nota)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.55) + 0.32 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / 0.09) + 0.12 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / 0.3)
    k = int(0.003 * SR)
    x[:k] += bp(rng.standard_normal(k), 1500, 7000) * np.linspace(1, 0, k) * 0.5      # la uña en la lámina
    return x * np.minimum(1, t / 0.002) * vel * 0.5


def marimba(nota, vel=1.0, largo=1.2):
    t = tt(largo)
    f = MIDI(nota)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.32) + 0.25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t / 0.05) + 0.08 * np.sin(2 * np.pi * f * 9.2 * t) * np.exp(-t / 0.02)
    return x * np.minimum(1, t / 0.003) * vel * 0.55


CORCHEA = BEAT / 2
rejilla = lambda t: round(t / CORCHEA) * CORCHEA       # noqa: E731
t_borra, t_circ, preguntas = C["tBorra"], C["tCirc"], C["preguntas"]
t_resuelve = rejilla(t_circ + 1.02)
i = 0
t = rejilla(1.25)
while t < t_resuelve - 0.05:
    en_silencio = t_borra - 0.12 <= t < C["VO"]["b"] - 0.05
    if not en_silencio:
        if t < C["tVuelve"]:                             # el pedido vago: tres notas que no resuelven
            figura, vel = [D4, E4, A4], 0.8
        elif t < t_borra:                                # el enredo: una nota que desafina
            figura, vel = [D4, GS4, A4, GS4], 0.95
        else:                                            # el pedido completo: una nota más por cada pregunta
            figura = [D4, E4, A4] + [n for n, tp in zip([FS4, B4, D5], preguntas) if t >= tp]
            vel = 0.8 + 0.06 * (len(figura) - 3)
            if t >= C["bien"]:
                figura = [D4, FS4, A4, B4, D5, A4]
        nota = figura[i % len(figura)]
        put(mus, kalimba(nota, vel * (1.0 if i % 2 == 0 else 0.78)), t, 1, -0.25 if i % 2 == 0 else 0.25)
        if abs(t / BEAT - round(t / BEAT)) < 1e-6 and round(t / BEAT) % 2 == 0:        # bajo de marimba cada dos tiempos
            put(mus, marimba(D3 if t < t_borra or t >= preguntas[0] else A3, 0.7), t, 1, 0)
        i += 1
    else:
        i = 0
    t += CORCHEA
put(mus, kalimba(D6, 0.9, 1.6), rejilla(C["bien"]), 1, 0.2)                           # la marca de «bien»
for n, pn in zip([D3, A3, D4, FS4, A4, D5], [0, -0.3, 0.3, -0.15, 0.15, 0]):          # resuelve en el segundo círculo
    put(mus, marimba(n, 0.9, 2.4), t_resuelve, 1, pn)
    put(mus, kalimba(n + 12, 0.5, 2.4), t_resuelve + 0.02, 1, -pn)
mus = sala(mus, size=0.3, mix=0.22).astype(np.float32)

# la música baja bajo la voz
env = np.convolve(np.abs(voz), np.ones(int(0.05 * SR)) / int(0.05 * SR), "same")
hay = (env > 0.02).astype(np.float32)
att, rel = int(0.06 * SR), int(0.35 * SR)
dk = np.zeros(NS, np.float32)
g = 0.0
for j in range(0, NS, 240):
    obj = hay[j]
    g += (obj - g) * (240 / att if obj > g else 240 / rel)
    dk[j:j + 240] = g
mus = mus * (1 - (1 - db(-8)) * dk)[:, None]


# ───────── balance: voz arriba, música unos 9 dB abajo, marcador entre las dos
def rms(x):
    m = np.abs(x).max(1) > 1e-4
    return float(np.sqrt(np.mean(x[m] ** 2))) if m.any() else 1.0


rv, rm, rf = rms(vo), rms(mus), rms(fol)
mezcla = vo + mus * (rv / rm) * db(-9) + fol * (rv / rf) * db(-10) + amb
mezcla = np.stack([limit(mezcla[:, c], 0.95) for c in range(2)], 1)
os.makedirs(os.path.join(AQUI, "out"), exist_ok=True)
sf.write(os.path.join(AQUI, "out", "mix.wav"), mezcla[:int(DUR * SR)].astype(np.float32), SR)
print("rms voz/música/marcador (dB):", round(20 * np.log10(rv), 1), round(20 * np.log10(rm), 1), round(20 * np.log10(rf), 1), "· pico", round(float(np.abs(mezcla).max()), 3))
