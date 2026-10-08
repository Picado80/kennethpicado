import re, sys
sp = sys.argv[1]
t = open(sp + "/index2.tpl.html", encoding="utf-8").read()
split = open(sp + "/split.html", encoding="utf-8").read()
esc = open(sp + "/escenas.html", encoding="utf-8").read()
sjs = open(sp + "/split.js", encoding="utf-8").read()
ejs = open(sp + "/escenas.js", encoding="utf-8").read()

def cortar(t, desde, hasta):
    a = t.index(desde); b = t.index(hasta, a)
    return t[:a] + t[b:]

# Lunes (36.9-40.9) va a pantalla completa (e4): menos segundos de gemelo
split = split[:split.index('      <div id="s5"')] + split[split.index('      <div id="s6"'):]
sjs = re.sub(r'      // s5:.*\n(?:      tl\.fromTo\("#s5.*\n)+', '', sjs)

css = """      .abajo { position: absolute; left: 0; top: 960px; width: 1080px; height: 960px; overflow: hidden; }
      video.avs.clip { inset: auto; left: 0; top: -160px; width: 1080px; height: 1920px; transform-origin: 50% 35%; }
      .arriba-svg { position: absolute; left: 0; top: 0; }
      .clip.mitad-texto { inset: 0 0 auto 0; height: 960px; background: #1B2230; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; padding: 0 90px; }
      .tenue2 { color: #9AA0AA; }
      .divisor { position: absolute; left: 0; top: 954px; width: 1080px; height: 12px; background: #F5B700; }
      .cap { top: 905px !important; font-size: 50px !important; -webkit-text-stroke: 0 !important; text-shadow: none !important; left: auto !important; right: auto !important;
             width: 1080px; padding: 0 60px; }
      .cap span { background: #000; padding: 4px 10px; border-radius: 8px; }
    </style>"""
t = t.replace("    </style>", css, 1)
t = cortar(t, "      <!-- Kenneth (gemelo, Avatar IV)", "      <!-- B-roll -->")
t = cortar(t, "      <!-- B-roll -->", "      <!-- Escenas de graficos -->")
t = cortar(t, '      <div id="e5"', "      <!-- Tarjetas sobre el B-roll -->")
t = cortar(t, "      <!-- Textos arriba de Kenneth -->", "      <!-- Subtitulos -->")
t = t.replace("      <!-- Escenas de graficos -->", split + '      <div class="divisor"></div>\n\n      <!-- Escenas de graficos -->', 1)
t = t.replace("      <!-- Tarjetas sobre el B-roll -->", esc + "\n      <!-- Tarjetas sobre el B-roll -->", 1)
for pat in [r'      // Kenneth: acercamiento lento dentro de la tarjeta\n(?:      tl\.fromTo\("#av3?[ab0-9]*".*\n)+',
            r'      // B-roll: Ken Burns\n.*\n.*\n',
            r'      tl\.fromTo\("#e5[ab]".*\n', r'      tl\.fromTo\("#o[1236]a".*\n']:
    t = re.sub(pat, "", t)
t = t.replace('      tl.fromTo("#e1a"', sjs + ejs + '      tl.fromTo("#e1a"', 1)
t = re.sub(r'      <audio id="sfx13".*\n', "", t)
for x in ["#av1", "#s8-avion", "#pb-lapiz", "#e1a", "divisor", 'id="e4"', "#e4a"]:
    assert x in t, x
for x in ["#br1", "#o1a", "#s5-cal", "broll-hoja", 'id="av3a"', 'id="e5"']:
    assert x not in t, x
open(sp + "/index5.tpl.html", "w", encoding="utf-8").write(t)
print("ok")
