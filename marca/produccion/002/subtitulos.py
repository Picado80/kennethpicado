import json, html
W = json.load(open(r"C:\Users\Picado\kennethpicado\marca\salidas\002-palabras.json", encoding="utf-8"))
DUR = 50.16
VENTANAS = [(0, 5.30), (10.30, 19.90), (26.40, 36.90), (36.90, DUR)]   # donde van subtitulos
grupos = []
for a, b in VENTANAS:
    ws = [w for w in W if a <= w["s"] < b]
    g = []
    for w in ws:
        g.append(w)
        if len(g) == 3 or w["t"][-1] in ".,:?":
            grupos.append((a, b, g)); g = []
    if g: grupos.append((a, b, g))
caps = []
for i, (a, b, g) in enumerate(grupos):
    ini = g[0]["s"]
    sig = grupos[i + 1][2][0]["s"] if i + 1 < len(grupos) and grupos[i + 1][0] == a else None
    fin = min(sig if sig else g[-1]["e"] + 0.35, b)
    caps.append({"s": round(ini, 2), "e": round(fin, 2), "w": [[x["t"], round(x["s"], 2)] for x in g]})
caps_html = "\n".join(
    f'      <div class="cap" id="cap{i}">' + " ".join(f'<span id="cap{i}w{j}">{html.escape(t)}</span>' for j, (t, s) in enumerate(c["w"])) + "</div>"
    for i, c in enumerate(caps))
caps_js = json.dumps(caps, ensure_ascii=False)
tpl = open(r"C:\Users\Picado\AppData\Local\Temp\claude\C--Users-Picado-kennethpicado\1efc8ba8-f34c-4fc5-883f-0771c42ef332\scratchpad\index.tpl.html", encoding="utf-8").read()
out = tpl.replace("%%CAPS_HTML%%", caps_html).replace("%%CAPS_JS%%", caps_js)
open(r"C:\Users\Picado\kennethpicado\marca\salidas\hf\v002\index.html", "w", encoding="utf-8").write(out)
print(len(caps), "grupos de subtitulos")
