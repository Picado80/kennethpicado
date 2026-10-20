// Biblioteca de efectos de motion graphics de la marca, en estilo Editorial (marca/ESTILO.md).
// Cada efecto arma su DOM dentro de un contenedor y devuelve { pintar(t) }: t son los segundos desde que empieza
// la escena. pintar(t) solo depende de t (nada de Date ni azar sin semilla), así el render cuadro por cuadro de
// Lemo-Opuscar sale igual cada vez. El cuadro es de 1080×1920.

export const C = {
  tinta: '#16233F', noche: '#101B33', vitela: '#E8E6DE', oro: '#C9A45C',
  grafito: '#23262A', rojo: '#B22B3F', gris: '#9AA3B5', blanco: '#FFFFFF',
};
export const FW = 1080, FH = 1920;

export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const tramo = (t, a, b) => clamp((t - a) / (b - a));
export const mezcla = (a, b, p) => a + (b - a) * p;
export const E = {
  sale: x => 1 - Math.pow(1 - x, 3),
  expo: x => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x)),
  atras: (x, s = 1.7) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2),
  entra: x => x * x * x,
  // resorte: x en segundos desde que arranca; llega a 1 con un rebote corto
  resorte: x => (x <= 0 ? 0 : 1 - Math.exp(-7 * x) * Math.cos(11 * x)),
};

// Azar con semilla, para que las posiciones «sueltas» sean siempre las mismas
export function azar(semilla = 7) {
  let s = semilla >>> 0;
  return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
}

export function el(tag, estilo = {}, padre = null, html = null) {
  const e = document.createElement(tag);
  Object.assign(e.style, estilo);
  if (html != null) e.innerHTML = html;
  if (padre) padre.appendChild(e);
  return e;
}
const SVG = 'http://www.w3.org/2000/svg';
export function svg(tag, attrs = {}, padre = null) {
  const e = document.createElementNS(SVG, tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (padre) padre.appendChild(e);
  return e;
}

// Números con punto de miles, como se escribe en Costa Rica: 1.658
export const miles = n => Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');

// Texto con una sola palabra en oro e itálica (la regla del estilo Editorial)
export const conOro = (texto, oro) => !oro ? texto
  : texto.replace(oro, `<span style="color:${C.oro};font-style:italic">${oro}</span>`);

// Fuentes y estilos base. Las fuentes viven en ./fuentes (las copia preparar.sh desde marca/estilo/fuentes).
export async function instalar() {
  const css = `
  @font-face{font-family:"Instrument Serif";font-style:normal;src:url(fuentes/instrument-serif-latin-400-normal.woff2) format("woff2")}
  @font-face{font-family:"Instrument Serif";font-style:italic;src:url(fuentes/instrument-serif-latin-400-italic.woff2) format("woff2")}
  @font-face{font-family:"Archivo";font-weight:600;src:url(fuentes/archivo-latin-600-normal.woff2) format("woff2")}
  @font-face{font-family:"Archivo";font-weight:900;src:url(fuentes/archivo-latin-900-normal.woff2) format("woff2")}
  @font-face{font-family:"JetBrains Mono";font-weight:500;src:url(fuentes/jetbrains-mono-latin-500-normal.woff2) format("woff2")}
  html,body{margin:0;width:${FW}px;height:${FH}px;overflow:hidden;background:${C.tinta}}
  .mono{font-family:"JetBrains Mono",monospace;font-weight:500;text-transform:uppercase;letter-spacing:.14em}
  .serif{font-family:"Instrument Serif",serif;font-weight:400}
  .archivo{font-family:"Archivo",sans-serif;font-weight:600}`;
  el('style', {}, document.head, css);
  await Promise.all(['400 40px "Instrument Serif"', 'italic 400 40px "Instrument Serif"', '600 40px Archivo',
    '900 40px Archivo', '500 40px "JetBrains Mono"'].map(f => document.fonts.load(f)));
}

// ───────────────────────────────────────── 1 · la curva de crecimiento (el contador del reto)
// o: { valores: [seguidores por día], meta: número final, titulo, dia, ejemplo: true si los datos son de muestra }
export function curva(padre, o) {
  const v = o.valores, base = v[0], meta = o.meta, ult = v[v.length - 1];
  const raiz = el('div', { position: 'absolute', inset: '0', background: C.tinta, color: C.vitela }, padre);
  el('div', { position: 'absolute', left: '90px', top: '330px', fontSize: '30px', color: C.oro }, raiz, o.titulo || 'Seguidores').className = 'mono';
  const num = el('div', { position: 'absolute', left: '80px', top: '380px', font: '900 250px Archivo', letterSpacing: '-.04em',
    fontVariantNumeric: 'tabular-nums', lineHeight: '1' }, raiz);
  const sub = el('div', { position: 'absolute', left: '90px', top: '660px', font: '400 60px "Instrument Serif"' }, raiz,
    conOro(`Meta: ${miles(meta)} el Día 30`, miles(meta)));
  // la gráfica
  const X0 = 90, Y0 = 820, W = 900, H = 820;
  const g = svg('svg', { width: FW, height: FH, style: 'position:absolute;left:0;top:0' }, raiz);
  const y = val => Y0 + H - (val - base) / (meta - base) * H;
  const x = i => X0 + i / 29 * W;                           // 30 días a lo ancho
  svg('line', { x1: X0, y1: Y0 + H, x2: X0 + W, y2: Y0 + H, stroke: C.gris, 'stroke-width': 2, opacity: .5 }, g);
  const lineaMeta = svg('line', { x1: X0, y1: y(meta), x2: X0 + W, y2: y(meta), stroke: C.oro, 'stroke-width': 4,
    'stroke-dasharray': '18 14' }, g);
  const rotMeta = el('div', { position: 'absolute', right: '90px', top: `${y(meta) - 52}px`, fontSize: '26px', color: C.oro }, raiz, 'Meta');
  rotMeta.className = 'mono';
  const d = v.map((val, i) => `${i ? 'L' : 'M'}${x(i).toFixed(1)},${y(val).toFixed(1)}`).join(' ');
  const camino = svg('path', { d, fill: 'none', stroke: C.vitela, 'stroke-width': 10, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
  // el ritmo que hace falta: de la base del Día 1 a la meta del Día 30
  const ritmo = svg('line', { x1: x(0), y1: y(base), x2: x(29), y2: y(meta), stroke: C.gris, 'stroke-width': 3,
    'stroke-dasharray': '4 12', opacity: .7 }, g);
  const faltan = el('div', { position: 'absolute', left: '90px', top: `${Y0 + H * .38}px`, font: '400 92px/1 "Instrument Serif"' }, raiz,
    conOro(`Faltan ${miles(meta - ult)}`, miles(meta - ult)));
  const rotRitmo = el('div', { position: 'absolute', left: `${x(16)}px`, top: `${y(base + (meta - base) * 16 / 29) - 70}px`,
    fontSize: '22px', color: C.gris, transform: 'rotate(-38deg)', transformOrigin: '0 0' }, raiz, 'el ritmo para llegar');
  rotRitmo.className = 'mono';
  const punto = svg('circle', { r: 18, fill: C.oro }, g);
  const halo = svg('circle', { r: 18, fill: 'none', stroke: C.oro, 'stroke-width': 4 }, g);
  const L = camino.getTotalLength();
  camino.setAttribute('stroke-dasharray', `${L} ${L}`);
  const pie = el('div', { position: 'absolute', left: '90px', top: `${Y0 + H + 30}px`, fontSize: '26px', color: C.gris }, raiz,
    o.ejemplo ? 'Día 1 · · · Día 30 · datos de ejemplo' : 'Día 1 · · · Día 30');
  pie.className = 'mono';
  return {
    pintar(t) {
      const a = tramo(t, 0, .5), p = E.sale(tramo(t, .35, 2.2));
      num.textContent = miles(mezcla(base, ult, p));
      for (const e of [num, sub]) { e.style.opacity = a; e.style.transform = `translateY(${(1 - a) * 30}px)`; }
      lineaMeta.setAttribute('opacity', tramo(t, .2, .7));
      ritmo.setAttribute('opacity', .7 * tramo(t, .5, 1.1)); rotRitmo.style.opacity = tramo(t, .8, 1.3);
      const f = tramo(t, 2.0, 2.5); faltan.style.opacity = f; faltan.style.transform = `translateY(${(1 - E.sale(f)) * 30}px)`;
      rotMeta.style.opacity = tramo(t, .4, .9);
      camino.setAttribute('stroke-dashoffset', L * (1 - p));
      const q = camino.getPointAtLength(L * p);
      punto.setAttribute('cx', q.x); punto.setAttribute('cy', q.y);
      const pulso = (t > 2.2) ? ((t - 2.2) % 1) : 0;
      halo.setAttribute('cx', q.x); halo.setAttribute('cy', q.y);
      halo.setAttribute('r', 18 + pulso * 46); halo.setAttribute('opacity', t > 2.2 ? 1 - pulso : 0);
    },
  };
}

// ───────────────────────────────────────── 2 · el chat que toma la pantalla
// o: { titulo, estado, mensajes: [{ de: 'cliente'|'agente', texto }], inicio, cada, toma (segundo en que llena el cuadro) }
export function chat(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', background: C.noche }, padre);
  const PW = 860, PH = 1380;
  const panel = el('div', { position: 'absolute', left: `${(FW - PW) / 2}px`, top: `${(FH - PH) / 2}px`, width: `${PW}px`,
    height: `${PH}px`, background: C.vitela, borderRadius: '44px', overflow: 'hidden', boxShadow: '0 40px 90px rgba(0,0,0,.45)' }, raiz);
  const cab = el('div', { height: '150px', background: C.tinta, color: C.vitela, padding: '34px 44px', boxSizing: 'border-box' }, panel);
  el('div', { font: '600 44px Archivo' }, cab, o.titulo);
  el('div', { fontSize: '22px', color: C.oro, marginTop: '10px' }, cab, o.estado || 'en línea').className = 'mono';
  const cuerpo = el('div', { position: 'absolute', left: '0', right: '0', top: '150px', bottom: '0', padding: '40px 40px',
    display: 'flex', flexDirection: 'column', gap: '22px', boxSizing: 'border-box' }, panel);
  const inicio = o.inicio ?? .4, cada = o.cada ?? .9;
  const burbujas = o.mensajes.map((m, i) => {
    const agente = m.de === 'agente';
    const b = el('div', { alignSelf: agente ? 'flex-end' : 'flex-start', maxWidth: '78%', padding: '24px 30px', borderRadius: '30px',
      background: agente ? C.tinta : C.blanco, color: agente ? C.vitela : C.grafito, font: '600 36px/1.3 Archivo',
      boxShadow: '0 6px 18px rgba(0,0,0,.08)', transformOrigin: agente ? '100% 100%' : '0% 100%' }, cuerpo);
    if (agente) el('div', { fontSize: '18px', color: C.oro, marginBottom: '8px' }, b, o.etiquetaAgente || 'Agente de IA').className = 'mono';
    el('div', {}, b, m.texto);
    return { b, t: inicio + i * cada, agente };
  });
  const puntos = el('div', { alignSelf: 'flex-end', display: 'none', gap: '10px', padding: '26px 30px', borderRadius: '30px',
    background: C.tinta }, cuerpo);
  const ps = [0, 1, 2].map(() => el('div', { width: '14px', height: '14px', borderRadius: '50%', background: C.vitela }, puntos));
  const L0 = (FW - PW) / 2, T0 = (FH - PH) / 2;
  return {
    pintar(t) {
      let escribiendo = false;
      for (const { b, t: tb, agente } of burbujas) {
        const p = tramo(t, tb, tb + .35);
        b.style.display = t >= tb ? 'block' : 'none';
        b.style.opacity = p; b.style.transform = `translateY(${(1 - E.sale(p)) * 30}px) scale(${mezcla(.86, 1, E.atras(p))})`;
        if (agente && t >= tb - .55 && t < tb) escribiendo = true;
      }
      puntos.style.display = escribiendo ? 'flex' : 'none';
      ps.forEach((d, i) => { d.style.opacity = .35 + .65 * Math.max(0, Math.sin(t * 9 - i * .9)); });
      const k = E.expo(tramo(t, o.toma ?? 99, (o.toma ?? 99) + .55));
      const a = tramo(t, 0, .35);
      panel.style.left = `${mezcla(L0, 0, k)}px`; panel.style.top = `${mezcla(T0, 0, k)}px`;
      panel.style.width = `${mezcla(PW, FW, k)}px`; panel.style.height = `${mezcla(PH, FH, k)}px`;
      panel.style.borderRadius = `${44 * (1 - k)}px`;
      panel.style.opacity = a; panel.style.transform = `scale(${mezcla(.94, 1, E.sale(a))})`;
      cab.style.height = `${mezcla(150, 300, k)}px`; cab.style.paddingTop = `${mezcla(34, 190, k)}px`;
      cuerpo.style.top = `${mezcla(150, 300, k)}px`;
      cuerpo.style.padding = `${mezcla(40, 70, k)}px ${mezcla(40, 60, k)}px`;
    },
  };
}

// ───────────────────────────────────────── 3 · el teléfono
// o: { inicio, llenar(pantalla) -> { pintar(t) } para lo que va adentro }
export function telefono(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', background: o.fondo || C.vitela, perspective: '2200px' }, padre);
  const TW = 640, TH = 1300;
  const cuerpo = el('div', { position: 'absolute', left: `${(FW - TW) / 2}px`, top: `${(FH - TH) / 2 + 60}px`, width: `${TW}px`,
    height: `${TH}px`, borderRadius: '96px', background: '#0b0d10', boxShadow: '0 60px 120px rgba(22,35,63,.45)',
    transformStyle: 'preserve-3d' }, raiz);
  const pantalla = el('div', { position: 'absolute', inset: '20px', borderRadius: '78px', overflow: 'hidden', background: C.blanco }, cuerpo);
  el('div', { position: 'absolute', left: '50%', top: '34px', width: '170px', height: '44px', marginLeft: '-85px', borderRadius: '24px',
    background: '#0b0d10', zIndex: 5 }, cuerpo);
  const adentro = o.llenar ? o.llenar(pantalla) : null;
  const i0 = o.inicio ?? 0;
  return {
    pintar(t) {
      const p = E.expo(tramo(t, i0, i0 + 1.0));
      cuerpo.style.transform = `translateY(${(1 - p) * 1100}px) rotateX(${(1 - p) * 28}deg) rotateZ(${(1 - p) * -10}deg)` +
        ` translateY(${Math.sin(t * 1.6) * 6 * p}px)`;
      if (adentro) adentro.pintar(t - i0 - .6);
    },
  };
}

// ───────────────────────────────────────── 4 · la lista que aparece
// o: { titulo, oro, items: [texto], inicio, cada, claro }
export function lista(padre, o) {
  const claro = o.claro ?? true;
  const raiz = el('div', { position: 'absolute', inset: '0', background: claro ? C.vitela : C.tinta, color: claro ? C.tinta : C.vitela,
    padding: '0 90px', boxSizing: 'border-box' }, padre);
  const tit = el('div', { position: 'absolute', left: '90px', right: '90px', top: '360px', font: '400 108px/1.02 "Instrument Serif"' },
    raiz, conOro(o.titulo, o.oro));
  const filas = o.items.map((texto, i) => {
    const f = el('div', { position: 'absolute', left: '90px', right: '90px', top: `${820 + i * 190}px`, display: 'flex',
      alignItems: 'center', gap: '40px', transformOrigin: '0 50%' }, raiz);
    const s = svg('svg', { width: 84, height: 84, viewBox: '0 0 84 84', style: 'flex:none' }, f);
    svg('rect', { x: 4, y: 4, width: 76, height: 76, rx: 14, fill: 'none', stroke: claro ? C.tinta : C.vitela, 'stroke-width': 6 }, s);
    const v = svg('path', { d: 'M20 44 L36 60 L66 26', fill: 'none', stroke: C.oro, 'stroke-width': 10, 'stroke-linecap': 'round',
      'stroke-linejoin': 'round' }, s);
    v.setAttribute('stroke-dasharray', '70 70');
    el('div', { font: '600 54px/1.15 Archivo' }, f, texto);
    return { f, v };
  });
  const i0 = o.inicio ?? .5, cada = o.cada ?? .55;
  return {
    pintar(t) {
      const a = tramo(t, 0, .5);
      tit.style.opacity = a; tit.style.transform = `translateY(${(1 - E.sale(a)) * 40}px)`;
      filas.forEach(({ f, v }, i) => {
        const ti = i0 + i * cada, p = tramo(t, ti, ti + .4);
        f.style.opacity = p; f.style.transform = `scale(${mezcla(.6, 1, E.atras(p, 2.4))})`;
        v.setAttribute('stroke-dashoffset', 70 * (1 - E.sale(tramo(t, ti + .18, ti + .48))));
      });
    },
  };
}

// ───────────────────────────────────────── 5 · los titulares que llueven
// o: { items: [{ fuente, fecha, texto }], destacado: índice, inicio, foco (segundo del acercamiento) }
export function titulares(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', background: C.tinta, overflow: 'hidden' }, padre);
  const mesa = el('div', { position: 'absolute', inset: '0', transformOrigin: '50% 50%' }, raiz);
  const r = azar(23), n = o.items.length;
  const tarjetas = o.items.map((it, i) => {
    const c = el('div', { position: 'absolute', left: '110px', width: '860px', padding: '36px 44px', boxSizing: 'border-box',
      background: C.vitela, color: C.tinta, borderRadius: '10px', boxShadow: '0 24px 50px rgba(0,0,0,.4)' }, mesa);
    const m = el('div', { fontSize: '22px', color: C.rojo, marginBottom: '14px' }, c, `${it.fuente} · ${it.fecha}`);
    m.className = 'mono';
    el('div', { font: '400 56px/1.08 "Instrument Serif"' }, c, it.texto);
    const fin = { y: 330 + i * (1180 / Math.max(1, n - 1)), rot: (r() - .5) * 8, x: (r() - .5) * 60 };
    const ang = r() * Math.PI * 2;
    const desde = { x: Math.cos(ang) * 1400, y: Math.sin(ang) * 1700, rot: (r() - .5) * 60 };
    return { c, fin, desde };
  });
  const i0 = o.inicio ?? .2, paso = .3, foco = o.foco ?? (i0 + n * paso + .5), dest = o.destacado ?? 0;
  return {
    pintar(t) {
      tarjetas.forEach(({ c, fin, desde }, i) => {
        const p = E.expo(tramo(t, i0 + i * paso, i0 + i * paso + .7));
        c.style.top = `${fin.y}px`;
        c.style.transform = `translate(${mezcla(desde.x, fin.x, p)}px, ${mezcla(desde.y, 0, p)}px) rotate(${mezcla(desde.rot, fin.rot, p)}deg)`;
        c.style.opacity = tramo(t, i0 + i * paso, i0 + i * paso + .15);
        const k = E.sale(tramo(t, foco, foco + .6));
        c.style.filter = i === dest ? 'none' : `brightness(${1 - .55 * k})`;
        c.style.outline = i === dest ? `${Math.round(8 * k)}px solid ${C.oro}` : 'none';
        c.style.zIndex = i === dest && k > 0 ? 10 : i;
      });
      const k = E.sale(tramo(t, foco, foco + .6)), d = tarjetas[dest].fin;
      const cy = d.y + 120;
      mesa.style.transform = `translate(0, ${(FH / 2 - cy) * k}px) scale(${mezcla(1, 1.18, k)})`;
    },
  };
}

// ───────────────────────────────────────── 6 · el recorte de papel que se sale del cuadro
// o: { src: PNG con fondo transparente (si falta, una silueta de boceto), inicio, rotulo }
export function recorte(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', background: C.vitela }, padre);
  const MX = 140, MY = 640, MW = 800, MH = 960;
  const marco = el('div', { position: 'absolute', left: `${MX}px`, top: `${MY}px`, width: `${MW}px`, height: `${MH}px`,
    background: C.tinta, borderRadius: '6px' }, raiz);
  // la figura se corta solo por abajo (el borde de abajo del cuadro): por arriba se escapa
  const caja = el('div', { position: 'absolute', left: `${MX}px`, top: '0', width: `${MW}px`, height: `${MY + MH}px`,
    clipPath: 'inset(0 -200px 0 -200px)' }, raiz);
  const papel = 'drop-shadow(7px 0 0 #fff) drop-shadow(-7px 0 0 #fff) drop-shadow(0 7px 0 #fff) drop-shadow(0 -7px 0 #fff) drop-shadow(0 26px 30px rgba(0,0,0,.45))';
  let fig;
  if (o.src) {
    fig = el('img', { position: 'absolute', left: '50%', bottom: '0', height: '1250px', transform: 'translateX(-50%)', filter: papel }, caja);
    fig.src = o.src;
  } else {
    fig = el('div', { position: 'absolute', left: '50%', bottom: '0', width: '640px', height: '1150px', marginLeft: '-320px', filter: papel,
      zoom: '1.22' }, caja);
    const s = svg('svg', { width: 640, height: 1150, viewBox: '0 0 640 1150' }, fig);
    svg('circle', { cx: 320, cy: 300, r: 175, fill: C.grafito }, s);
    svg('path', { d: 'M40 1150 C40 760 170 560 320 560 C470 560 600 760 600 1150 Z', fill: C.grafito }, s);
    el('div', { position: 'absolute', left: '0', right: '0', top: '640px', textAlign: 'center', fontSize: '26px', color: C.vitela }, fig,
      o.rotulo || '[recorte del gemelo]').className = 'mono';
  }
  const i0 = o.inicio ?? .3;
  return {
    pintar(t) {
      const a = tramo(t, 0, .4);
      marco.style.opacity = a;
      const p = tramo(t, i0, i0 + .75);
      const sube = mezcla(560, 0, E.atras(p, 1.4));
      fig.style.transform = `${o.src ? 'translateX(-50%) ' : ''}translateY(${sube}px) rotate(${mezcla(4, -2.5, E.sale(p))}deg)`;
      fig.style.transformOrigin = '50% 100%';
    },
  };
}

// ───────────────────────────────────────── 7 · el golpe de zoom (snap zoom) sobre cualquier elemento
// o: { t0, escala, origen } — se llama dentro del pintar de la escena con el elemento ya armado
export function golpe(objetivo, o) {
  const destello = o.destello ? el('div', { position: 'absolute', inset: '0', background: C.blanco, opacity: 0, pointerEvents: 'none' },
    o.destello) : null;
  objetivo.style.transformOrigin = o.origen || '50% 50%';
  return {
    pintar(t) {
      const p = tramo(t, o.t0, o.t0 + .16);
      const s = mezcla(1, o.escala ?? 1.4, E.atras(p, 2.6));
      objetivo.style.transform = `scale(${s})`;
      objetivo.style.filter = `blur(${Math.sin(p * Math.PI) * 5}px)`;
      if (destello) destello.style.opacity = .22 * Math.sin(tramo(t, o.t0, o.t0 + .12) * Math.PI);
    },
  };
}

// Tipografía de golpe: una frase que entra palabra por palabra y remata con el golpe de zoom en la palabra de oro
// o: { texto, oro, cada, golpeEn, tiempos: [segundo en que entra cada palabra] (opcional, para colgarla de la voz) }
export function frase(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', background: C.tinta, color: C.vitela, display: 'flex', alignItems: 'center',
    padding: '0 90px', boxSizing: 'border-box' }, padre);
  const caja = el('div', { font: '400 128px/1.02 "Instrument Serif"', width: '100%' }, raiz);
  const palabras = o.texto.split(' ').map(w => {
    const s = el('span', { display: 'inline-block', marginRight: '.24em' }, caja, w);
    const limpio = x => x.normalize('NFD').replace(/[^\p{L}\p{N}]/gu, '').toLowerCase();
    if (o.oro && limpio(w) === limpio(o.oro)) { s.style.color = C.oro; s.style.fontStyle = 'italic'; }
    return s;
  });
  const g = golpe(caja, { t0: o.golpeEn ?? 1.6, escala: 1.12, origen: '30% 50%', destello: raiz });
  const cada = o.cada ?? .16;
  return {
    pintar(t) {
      palabras.forEach((s, i) => {
        const ti = o.tiempos ? o.tiempos[i] : .1 + i * cada;          // con voz: cada palabra entra cuando se dice
        const p = tramo(t, ti, ti + .22);
        s.style.opacity = p; s.style.transform = `translateY(${(1 - E.sale(p)) * 50}px)`;
      });
      g.pintar(t);
    },
  };
}
