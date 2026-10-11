import json, html, re, sys
sp = sys.argv[1]
W = json.load(open(r"C:\Users\Picado\kennethpicado\marca\salidas\002-palabras.json", encoding="utf-8"))
DUR = 50.16
# (inicio, fin, alto del subtitulo en px)
VENTANAS = [(0, 5.30, 1210), (10.30, 16.00, 896), (16.00, 19.90, 1500), (26.40, 36.90, 1600), (40.90, 43.55, 1210), (46.20, DUR, 1500)]
grupos = []
for a, b, top in VENTANAS:
    ws = [w for w in W if a <= w["s"] < b]
    g = []
    for w in ws:
        g.append(w)
        if len(g) == 4 or w["t"][-1] in ".,:?":
            grupos.append((a, b, top, g)); g = []
    if g: grupos.append((a, b, top, g))
caps = []
for i, (a, b, top, g) in enumerate(grupos):
    sig = grupos[i + 1][3][0]["s"] if i + 1 < len(grupos) and grupos[i + 1][0] == a else None
    fin = min(sig if sig else g[-1]["e"] + 0.35, b)
    caps.append({"s": round(g[0]["s"], 2), "e": round(fin, 2), "top": top, "w": [[x["t"], round(x["s"], 2)] for x in g]})
caps_html = "\n".join(
    f'      <div class="cap" id="cap{i}" style="top: {c["top"]}px"><div class="caja">'
    + " ".join(f'<span id="cap{i}w{j}">{html.escape(t)}</span>' for j, (t, s) in enumerate(c["w"])) + "</div></div>"
    for i, c in enumerate(caps))

split = open(sp + "/split.html", encoding="utf-8").read()
a = split.index('      <div id="s2"'); b = split.index('      <div id="s3"')
soda = split[a:b]
sjs = open(sp + "/split.js", encoding="utf-8").read()
soda_js = "".join(l + "\n" for l in sjs.splitlines() if '"#s2-' in l)
papel = open(sp + "/escenas.html", encoding="utf-8").read()
papel_js = open(sp + "/escenas.js", encoding="utf-8").read()

t = open(sp + "/editorial.tpl.html", encoding="utf-8").read()
for k, v in {"%%SODA%%": soda, "%%SODA_JS%%": soda_js, "%%PAPEL%%": papel, "%%PAPEL_JS%%": papel_js,
             "%%CAPS_HTML%%": caps_html, "%%CAPS_JS%%": json.dumps(caps, ensure_ascii=False)}.items():
    assert k in t, k
    t = t.replace(k, v)
open(r"C:\Users\Picado\kennethpicado\marca\salidas\hf\v002d\index.html", "w", encoding="utf-8").write(t)
print(len(caps), "grupos de subtitulos")
