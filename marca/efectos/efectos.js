// Biblioteca de efectos de motion graphics de la marca, en estilo Editorial (marca/ESTILO.md).
// Cada efecto arma su DOM dentro de un contenedor y devuelve { pintar(t) }: t son los segundos desde que empieza
// la escena. pintar(t) solo depende de t (nada de Date ni azar sin semilla), así el render cuadro por cuadro de
// Lemo-Opuscar sale igual cada vez. El cuadro es de 1080×1920.

export const C = {
  tinta: '#16233F', noche: '#101B33', vitela: '#E8E6DE', oro: '#C9A45C',
  grafito: '#23262A', rojo: '#B22B3F', gris: '#9AA3B5', blanco: '#FFFFFF',
};
// La paleta clara (Kenneth, 20-oct-2026: «el azul está muy oscuro; mejor colores más claros, a la gente le gusta más»).
// Fondo de papel, texto en tinta, un celeste suave para no perder el azul de la marca y el amarillo de resaltador.
// En fondo claro el oro de siempre no se lee: va el oro oscuro.
export const K = {
  papel: '#F7F4EC', crema: '#EEE7D8', celeste: '#DDE8F6', cielo: '#C3D6F0', tinta: '#16233F', tinta2: '#4A5675',
  resalte: '#F5CF4E', oro: '#8A6A2A', rojo: '#C2364B', blanco: '#FFFFFF', sombra: 'rgba(22,35,63,.16)',
};
export const FW = 1080, FH = 1920;
// Zona segura común a TikTok, Instagram Reels, Facebook Reels y YouTube Shorts en 1080×1920, en píxeles (la medida en
// píxeles es la fuente; ver la fila 202 del índice de TORRE). Sale de la guía de anuncios de cada red, la única publicada
// (20-oct-2026, Kenneth: «que estén en la zona segura de todas las redes»): todo lo que se lee va de x 120 a 888 y de
// y 288 a 1248. Además, de y 840 para abajo TikTok pone su columna de botones: ahí nada pasa de x 780.
export const SEGURA = { arriba: 288, abajo: 672, derecha: 192, izquierda: 120 };
export const BOTONES = { desde: 840, derecha: 300 };   // de y 840 para abajo, el margen derecho es 300 (hasta x 780)

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
export const conOro = (texto, oro, color = C.oro) => !oro ? texto
  : texto.replace(oro, `<span style="color:${color};font-style:italic">${oro}</span>`);
// Una palabra con resaltador amarillo; el trazo se anima con resaltar(span, p)
export const conResalte = (texto, palabra) => !palabra ? texto : texto.replace(palabra, `<span class="resalte">${palabra}</span>`);
export const resaltar = (span, p) => { span.style.backgroundSize = `${(E.sale(clamp(p)) * 100).toFixed(1)}% 42%`; };

// Fuentes y estilos base. Las fuentes viven en ./fuentes (las copia preparar.sh desde marca/estilo/fuentes).
export async function instalar(o = {}) {
  const css = `
  @font-face{font-family:"Instrument Serif";font-style:normal;src:url(fuentes/instrument-serif-latin-400-normal.woff2) format("woff2")}
  @font-face{font-family:"Instrument Serif";font-style:italic;src:url(fuentes/instrument-serif-latin-400-italic.woff2) format("woff2")}
  @font-face{font-family:"Archivo";font-weight:600;src:url(fuentes/archivo-latin-600-normal.woff2) format("woff2")}
  @font-face{font-family:"Archivo";font-weight:900;src:url(fuentes/archivo-latin-900-normal.woff2) format("woff2")}
  @font-face{font-family:"JetBrains Mono";font-weight:500;src:url(fuentes/jetbrains-mono-latin-500-normal.woff2) format("woff2")}
  @font-face{font-family:"Marcador";src:url(fuentes/ArchitectsDaughter-Regular.ttf)}
  html,body{margin:0;width:${FW}px;height:${FH}px;overflow:hidden;background:${o.fondo || C.tinta}}
  .resalte{background-image:linear-gradient(${K.resalte},${K.resalte});background-repeat:no-repeat;background-position:0 88%;
    background-size:0% 42%;padding:0 .06em;margin:0 -.06em}
  .mono{font-family:"JetBrains Mono",monospace;font-weight:500;text-transform:uppercase;letter-spacing:.14em}
  .serif{font-family:"Instrument Serif",serif;font-weight:400}
  .archivo{font-family:"Archivo",sans-serif;font-weight:600}`;
  el('style', {}, document.head, css);
  await Promise.all(['400 40px "Instrument Serif"', 'italic 400 40px "Instrument Serif"', '600 40px Archivo',
    '900 40px Archivo', '500 40px "JetBrains Mono"', '40px Marcador'].map(f => document.fonts.load(f)));
}

// ───────────────────────────────────────── 1 · la curva de crecimiento (el contador del reto)
// o: { valores: [seguidores por día], meta: número final, titulo, dia, ejemplo: true si los datos son de muestra }
export function curva(padre, o) {
  const P = o.oscuro ? { f: C.tinta, x: C.vitela, a: C.oro, s: C.gris } : { f: K.papel, x: K.tinta, a: K.oro, s: K.tinta2 };
  const v = o.valores, base = v[0], meta = o.meta, ult = v[v.length - 1];
  const raiz = el('div', { position: 'absolute', inset: '0', background: P.f, color: P.x }, padre);
  el('div', { position: 'absolute', left: '90px', top: '330px', fontSize: '30px', color: P.a }, raiz, o.titulo || 'Seguidores').className = 'mono';
  const num = el('div', { position: 'absolute', left: '80px', top: '380px', font: '900 250px Archivo', letterSpacing: '-.04em',
    fontVariantNumeric: 'tabular-nums', lineHeight: '1' }, raiz);
  const sub = el('div', { position: 'absolute', left: '90px', top: '660px', font: '400 60px "Instrument Serif"' }, raiz,
    conOro(`Meta: ${miles(meta)} el Día 30`, miles(meta), P.a));
  // la gráfica
  const X0 = 90, Y0 = 760, W = FW - 90 - SEGURA.derecha - 20, H = FH - SEGURA.abajo - 90 - 760;   // el eje y su rótulo, sobre la zona de abajo
  const g = svg('svg', { width: FW, height: FH, style: 'position:absolute;left:0;top:0' }, raiz);
  const y = val => Y0 + H - (val - base) / (meta - base) * H;
  const x = i => X0 + i / 29 * W;                           // 30 días a lo ancho
  svg('line', { x1: X0, y1: Y0 + H, x2: X0 + W, y2: Y0 + H, stroke: P.s, 'stroke-width': 2, opacity: .5 }, g);
  const lineaMeta = svg('line', { x1: X0, y1: y(meta), x2: X0 + W, y2: y(meta), stroke: P.a, 'stroke-width': 4,
    'stroke-dasharray': '18 14' }, g);
  const rotMeta = el('div', { position: 'absolute', right: `${SEGURA.derecha + 20}px`, top: `${y(meta) - 52}px`, fontSize: '26px', color: P.a }, raiz, 'Meta');
  rotMeta.className = 'mono';
  const d = v.map((val, i) => `${i ? 'L' : 'M'}${x(i).toFixed(1)},${y(val).toFixed(1)}`).join(' ');
  const camino = svg('path', { d, fill: 'none', stroke: P.x, 'stroke-width': 10, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
  // el ritmo que hace falta: de la base del Día 1 a la meta del Día 30
  const ritmo = svg('line', { x1: x(0), y1: y(base), x2: x(29), y2: y(meta), stroke: P.s, 'stroke-width': 3,
    'stroke-dasharray': '4 12', opacity: .7 }, g);
  const faltan = el('div', { position: 'absolute', left: '90px', top: `${Y0 + H * .38}px`, font: '400 92px/1 "Instrument Serif"' }, raiz,
    conOro(`Faltan ${miles(meta - ult)}`, miles(meta - ult), P.a));
  const rotRitmo = el('div', { position: 'absolute', left: `${x(16)}px`, top: `${y(base + (meta - base) * 16 / 29) - 70}px`,
    fontSize: '22px', color: P.s, transform: 'rotate(-38deg)', transformOrigin: '0 0' }, raiz, 'el ritmo para llegar');
  rotRitmo.className = 'mono';
  const punto = svg('circle', { r: 18, fill: P.a }, g);
  const halo = svg('circle', { r: 18, fill: 'none', stroke: P.a, 'stroke-width': 4 }, g);
  const L = camino.getTotalLength();
  camino.setAttribute('stroke-dasharray', `${L} ${L}`);
  const pie = el('div', { position: 'absolute', left: '90px', top: `${Y0 + H + 30}px`, fontSize: '26px', color: P.s }, raiz,
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
  const P = o.oscuro
    ? { fondo: C.noche, panel: C.vitela, cab: C.tinta, cabTxt: C.vitela, estado: C.oro, agente: C.tinta, agenteTxt: C.vitela, cliente: C.blanco, clienteTxt: C.grafito, sombra: '0 40px 90px rgba(0,0,0,.45)' }
    : { fondo: `linear-gradient(160deg, ${K.papel}, ${K.celeste})`, panel: K.blanco, cab: K.papel, cabTxt: K.tinta, estado: K.oro, agente: K.tinta,
        agenteTxt: K.papel, cliente: '#EEF2F8', clienteTxt: K.tinta, sombra: '0 40px 90px rgba(22,35,63,.22)' };
  const raiz = el('div', { position: 'absolute', inset: '0', background: P.fondo }, padre);
  const PW = 860, PH = 1380;
  const panel = el('div', { position: 'absolute', left: `${(FW - PW) / 2}px`, top: `${(FH - PH) / 2}px`, width: `${PW}px`,
    height: `${PH}px`, background: P.panel, borderRadius: '44px', overflow: 'hidden', boxShadow: P.sombra }, raiz);
  const cab = el('div', { height: '150px', background: P.cab, color: P.cabTxt, padding: '34px 44px', boxSizing: 'border-box' }, panel);
  el('div', { font: '600 44px Archivo' }, cab, o.titulo);
  el('div', { fontSize: '22px', color: P.estado, marginTop: '10px' }, cab, o.estado || 'en línea').className = 'mono';
  const cuerpo = el('div', { position: 'absolute', left: '0', right: '0', top: '150px', bottom: '0', padding: '40px 40px',
    display: 'flex', flexDirection: 'column', gap: '22px', boxSizing: 'border-box' }, panel);
  const inicio = o.inicio ?? .4, cada = o.cada ?? .9;
  const burbujas = o.mensajes.map((m, i) => {
    const agente = m.de === 'agente';
    const b = el('div', { alignSelf: agente ? 'flex-end' : 'flex-start', maxWidth: '78%', padding: '24px 30px', borderRadius: '30px',
      background: agente ? P.agente : P.cliente, color: agente ? P.agenteTxt : P.clienteTxt, font: '600 36px/1.3 Archivo',
      boxShadow: '0 6px 18px rgba(0,0,0,.08)', transformOrigin: agente ? '100% 100%' : '0% 100%' }, cuerpo);
    if (agente) el('div', { fontSize: '18px', color: C.oro, marginBottom: '8px' }, b, o.etiquetaAgente || 'Agente de IA').className = 'mono';
    el('div', {}, b, m.texto);
    return { b, t: inicio + i * cada, agente };
  });
  const puntos = el('div', { alignSelf: 'flex-end', display: 'none', gap: '10px', padding: '26px 30px', borderRadius: '30px',
    background: P.agente }, cuerpo);
  const ps = [0, 1, 2].map(() => el('div', { width: '14px', height: '14px', borderRadius: '50%', background: P.agenteTxt }, puntos));
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
      cab.style.height = `${mezcla(150, SEGURA.arriba + 150, k)}px`; cab.style.paddingTop = `${mezcla(34, SEGURA.arriba + 30, k)}px`;
      cuerpo.style.top = `${mezcla(150, SEGURA.arriba + 150, k)}px`;
      cuerpo.style.padding = `${mezcla(40, 70, k)}px ${mezcla(40, SEGURA.derecha + 10, k)}px ${mezcla(40, SEGURA.abajo, k)}px ${mezcla(40, SEGURA.izquierda, k)}px`;
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
    boxSizing: 'border-box' }, padre);
  const tit = el('div', { position: 'absolute', left: '90px', right: `${SEGURA.derecha + 10}px`, top: '360px', font: '400 108px/1.02 "Instrument Serif"' },
    raiz, conOro(o.titulo, o.oro));
  const filas = o.items.map((texto, i) => {
    const f = el('div', { position: 'absolute', left: '90px', right: `${SEGURA.derecha + 10}px`, top: `${820 + i * 190}px`, display: 'flex',
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
  const P = o.oscuro ? { fondo: C.tinta, tarjeta: C.vitela, sombra: '0 24px 50px rgba(0,0,0,.4)', acento: C.oro }
    : { fondo: `linear-gradient(170deg, ${K.celeste}, ${K.papel})`, tarjeta: K.blanco, sombra: '0 24px 50px rgba(22,35,63,.18)', acento: K.resalte };
  const raiz = el('div', { position: 'absolute', inset: '0', background: P.fondo, overflow: 'hidden' }, padre);
  const mesa = el('div', { position: 'absolute', inset: '0', transformOrigin: '50% 50%' }, raiz);
  const r = azar(23), n = o.items.length;
  const tarjetas = o.items.map((it, i) => {
    const c = el('div', { position: 'absolute', left: `${SEGURA.izquierda + 20}px`, width: `${FW - SEGURA.izquierda - 20 - SEGURA.derecha - 20}px`, padding: '36px 44px', boxSizing: 'border-box',
      background: P.tarjeta, color: C.tinta, borderRadius: '10px', boxShadow: P.sombra }, mesa);
    const m = el('div', { fontSize: '22px', color: C.rojo, marginBottom: '14px' }, c, `${it.fuente} · ${it.fecha}`);
    m.className = 'mono';
    el('div', { font: '400 56px/1.08 "Instrument Serif"' }, c, it.texto);
    const fin = { y: SEGURA.arriba + 60 + i * ((FH - SEGURA.arriba - SEGURA.abajo - 260) / Math.max(1, n - 1)), rot: (r() - .5) * 6, x: (r() - .5) * 30 };
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
        c.style.filter = i === dest ? 'none' : o.oscuro ? `brightness(${1 - .55 * k})` : `blur(${(2.5 * k).toFixed(2)}px) opacity(${(1 - .5 * k).toFixed(3)})`;
        c.style.outline = i === dest ? `${Math.round(8 * k)}px solid ${P.acento}` : 'none';
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
    background: o.marco ?? K.cielo, borderRadius: '6px' }, raiz);
  // la figura se corta solo por abajo (el borde de abajo del cuadro): por arriba se escapa
  const caja = el('div', { position: 'absolute', left: `${MX}px`, top: '0', width: `${MW}px`, height: `${MY + MH}px`,
    clipPath: 'inset(0 -200px 0 -200px)' }, raiz);
  const papel = 'drop-shadow(7px 0 0 #fff) drop-shadow(-7px 0 0 #fff) drop-shadow(0 7px 0 #fff) drop-shadow(0 -7px 0 #fff) drop-shadow(0 26px 30px rgba(0,0,0,.45))';
  let fig;
  if (o.foto) {   // una foto común: se recorta la silueta de cabeza y hombros, con el borde blanco del papel
    fig = el('div', { position: 'absolute', left: '50%', bottom: '0', width: '720px', height: '1150px', marginLeft: '-360px', filter: papel }, caja);
    const sil = el('div', { position: 'absolute', inset: '0', overflow: 'hidden',
      clipPath: "path('M0 1150 L0 980 C0 860 120 800 240 770 L250 700 A235 345 0 1 1 470 700 L480 770 C600 800 720 860 720 980 L720 1150 Z')" }, fig);
    const im = el('img', { position: 'absolute', left: `${o.dx ?? -130}px`, top: `${o.dy ?? -140}px`, width: '980px', height: '1742px', objectFit: 'cover' }, sil);
    im.src = o.foto;
  } else if (o.src) {
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
      fig.style.transform = `${o.src && !o.foto ? 'translateX(-50%) ' : ''}translateY(${sube}px) rotate(${mezcla(4, -2.5, E.sale(p))}deg)`;
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
  const raiz = el('div', { position: 'absolute', inset: '0', background: (o.claro ?? true) ? K.papel : C.tinta, color: (o.claro ?? true) ? K.tinta : C.vitela,
    display: 'flex', alignItems: 'center',
    padding: `0 ${BOTONES.derecha}px 0 ${SEGURA.izquierda + 10}px`, boxSizing: 'border-box' }, padre);
  const caja = el('div', { font: '400 128px/1.02 "Instrument Serif"', width: '100%' }, raiz);
  const palabras = o.texto.split(' ').map(w => {
    const s = el('span', { display: 'inline-block', marginRight: '.24em' }, caja, w);
    const limpio = x => x.normalize('NFD').replace(/[^\p{L}\p{N}]/gu, '').toLowerCase();
    if (o.oro && limpio(w) === limpio(o.oro)) { s.style.color = (o.claro ?? true) ? K.oro : C.oro; s.style.fontStyle = 'italic'; }
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

// ───────────────────────────────────────── 8 · la cámara: acercar, alejar, ángulos y movimiento
// Mueve una capa como si fuera una cámara. claves: [{ t, x, y, z, giro, inclina, ladea, curva }] —x e y en px, z el zoom
// (1 = normal; más es acercar), giro en el plano, inclina (rotateX) y ladea (rotateY) dan el ángulo en 3D.
// curva: 'io' (por omisión), 's' (sale), 'e' (expo, para golpes), 'a' (con rebote) o 'l' (lineal).
// o: { deriva: px de movimiento de mano, perspectiva, origen, desenfoque: true para el barrido cuando se mueve rápido }
const CURVAS = { l: x => x, s: E.sale, e: E.expo, a: x => E.atras(x, 1.4),
  io: x => (x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2) };
export function camara(capa, claves, o = {}) {
  const ks = claves.map(k => ({ x: 0, y: 0, z: 1, giro: 0, inclina: 0, ladea: 0, curva: 'io', ...k }));
  capa.style.transformOrigin = o.origen || '50% 50%';
  if (capa.parentElement) capa.parentElement.style.perspective = `${o.perspectiva || 2400}px`;
  const en = t => {
    let i = 0; while (i < ks.length - 1 && t >= ks[i + 1].t) i++;
    const a = ks[i], b = ks[Math.min(i + 1, ks.length - 1)];
    const p = a === b ? 0 : CURVAS[b.curva](tramo(t, a.t, b.t));
    const v = {}; for (const c of ['x', 'y', 'z', 'giro', 'inclina', 'ladea']) v[c] = mezcla(a[c], b[c], p);
    const d = o.deriva || 0;   // la mano: una deriva lenta, siempre igual para el mismo t
    v.x += d * Math.sin(t * .71 + .4); v.y += d * .8 * Math.cos(t * .53);
    return v;
  };
  return {
    en,
    pintar(t) {
      const v = en(t);
      capa.style.transform = `translate(${v.x.toFixed(2)}px, ${v.y.toFixed(2)}px) scale(${v.z.toFixed(4)}) ` +
        `rotateZ(${v.giro.toFixed(3)}deg) rotateX(${v.inclina.toFixed(3)}deg) rotateY(${v.ladea.toFixed(3)}deg)`;
      if (o.desenfoque) {   // barrido: desenfoque según la velocidad, como un obturador de cine
        const w = en(t - 1 / 30), vel = Math.hypot(v.x - w.x, v.y - w.y) + Math.abs(Math.log(v.z / w.z)) * 900;
        capa.style.filter = vel > 6 ? `blur(${Math.min(9, vel / 9).toFixed(2)}px)` : 'none';
      }
    },
  };
}

// ───────────────────────────────────────── 9 · los cortes entre escenas
// Cambia de la escena a a la b en el segundo t0. Cada escena es una capa a pantalla completa (la cámara va adentro).
// tipo: 'zoom' (se mete en a y sale en b, sin cortar el empuje), 'barrido' (paneo rápido de lado), 'gira' (ángulo en 3D)
// o 'golpe' (corte seco con destello). o: { dur, dir: 1 o -1 }
export function corte(a, b, t, t0, o = {}) {
  const d = o.dur ?? .42, tipo = o.tipo || 'zoom', dir = o.dir ?? 1;
  const p0 = tramo(t, t0 - d / 2, t0), p1 = tramo(t, t0, t0 + d / 2);
  const antes = t < t0;
  a.style.visibility = antes ? 'visible' : 'hidden';
  b.style.visibility = antes ? 'hidden' : 'visible';
  if (b.parentElement) b.parentElement.style.perspective = '2400px';
  if (tipo === 'zoom') {
    a.style.transform = `scale(${1 + 1.4 * E.entra(p0)})`; a.style.filter = `blur(${(14 * p0).toFixed(2)}px)`;
    b.style.transform = `scale(${1.5 - .5 * E.sale(p1)})`; b.style.filter = `blur(${(14 * (1 - p1)).toFixed(2)}px)`;
  } else if (tipo === 'barrido') {
    a.style.transform = `translateX(${-dir * FW * E.entra(p0)}px)`; a.style.filter = `blur(${(18 * p0).toFixed(2)}px)`;
    b.style.transform = `translateX(${dir * FW * (1 - E.sale(p1))}px)`; b.style.filter = `blur(${(18 * (1 - p1)).toFixed(2)}px)`;
  } else if (tipo === 'gira') {
    a.style.transformOrigin = dir > 0 ? '0 50%' : '100% 50%'; b.style.transformOrigin = dir > 0 ? '100% 50%' : '0 50%';
    a.style.transform = `rotateY(${-dir * 80 * E.entra(p0)}deg) scale(${1 - .15 * p0})`;
    b.style.transform = `rotateY(${dir * 80 * (1 - E.sale(p1))}deg) scale(${.85 + .15 * p1})`;
    a.style.filter = b.style.filter = 'none';
  } else {
    a.style.transform = b.style.transform = 'none';
    b.style.filter = `brightness(${1 + .6 * (1 - E.sale(tramo(t, t0, t0 + .18)))})`;
  }
  if (t >= t0 + d / 2) { b.style.transform = 'none'; b.style.filter = 'none'; }
}

// ───────────────────────────────────────── 10 · B-roll: una foto que se mueve sola
// Llena el cuadro (o va en una ventana, «B-roll overlay») y se mueve: acercamiento lento, paneo o ángulo, con la cámara.
// o: { src, claves (las de camara), marco: { left, top, width, height, radio } para la ventana, tono: filtro CSS opcional,
//      entra: segundo en que aparece la ventana }. Antes de pintar, esperar .listo (la foto decodificada).
export function broll(padre, o) {
  const raiz = el('div', { position: 'absolute', overflow: 'hidden', ...(o.marco
    ? { left: `${o.marco.left}px`, top: `${o.marco.top}px`, width: `${o.marco.width}px`, height: `${o.marco.height}px`,
        borderRadius: `${o.marco.radio ?? 36}px`, boxShadow: `0 40px 80px ${K.sombra}, 0 0 0 10px ${K.blanco}` }
    : { inset: '0' }) }, padre);
  const capa = el('div', { position: 'absolute', inset: '-6%' }, raiz);   // margen para que el movimiento no muestre bordes
  const img = el('img', { width: '100%', height: '100%', objectFit: 'cover', display: 'block', filter: o.tono || 'none' }, capa);
  img.src = o.src;
  const cam = camara(capa, o.claves || [{ t: 0, z: 1 }, { t: o.dur ?? 6, z: 1.12, curva: 'l' }], { deriva: o.deriva ?? 4 });
  const e0 = o.entra;
  return {
    raiz, listo: img.decode().catch(() => {}),
    pintar(t) {
      cam.pintar(t);
      if (o.marco && e0 != null) {
        const p = tramo(t, e0, e0 + .5);
        raiz.style.opacity = tramo(t, e0, e0 + .12);
        raiz.style.transform = `translateY(${(1 - E.atras(p, 1.6)) * 140}px) scale(${mezcla(.86, 1, E.sale(p))}) rotate(${mezcla(-4, -1.2, E.sale(p))}deg)`;
      }
    },
  };
}

// ───────────────────────────────────────── 11 · fichas que saltan (checklist pop en chiquito)
// Etiquetas que entran una por una con rebote. o: { items: [texto], inicio, cada, estilo (de la caja) }
export function fichas(padre, o) {
  const caja = el('div', { display: 'flex', flexWrap: 'wrap', gap: '14px', ...o.estilo }, padre);
  const fs = o.items.map(txt => el('span', { font: '600 34px/1 Archivo', color: K.tinta, background: K.blanco, padding: '14px 22px',
    borderRadius: '99px', boxShadow: `0 8px 20px ${K.sombra}`, border: `2px solid ${K.cielo}`, display: 'inline-block' }, caja, txt));
  const i0 = o.inicio ?? 0, cada = o.cada ?? .12;
  return {
    caja,
    pintar(t, fuera = 1) {
      fs.forEach((f, i) => { const p = tramo(t, i0 + i * cada, i0 + i * cada + .35);
        f.style.opacity = Math.min(1, p * 3) * fuera; f.style.transform = `scale(${mezcla(.4, 1, E.atras(p, 2.2))})`; });
    },
  };
}

// ───────────────────────────────────────── 12 · órbita: palabras que giran alrededor de algo
// o: { centro: html, items: [texto], cx, cy, rx, ry, vel (vueltas por segundo), inicio, fondo }
export function orbita(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', background: o.fondo ?? K.papel, color: K.tinta, overflow: 'hidden' }, padre);
  const cx = o.cx ?? 480, cy = o.cy ?? 690, rx = o.rx ?? 300, ry = o.ry ?? 185;
  const g = svg('svg', { width: FW, height: FH, style: 'position:absolute;left:0;top:0' }, raiz);
  const anillo = svg('ellipse', { cx, cy, rx, ry, fill: 'none', stroke: K.cielo, 'stroke-width': 3, 'stroke-dasharray': '4 14' }, g);
  const centro = el('div', { position: 'absolute', left: `${cx}px`, top: `${cy}px`, zIndex: 50, font: '400 116px/1 "Instrument Serif"',
    textAlign: 'center', whiteSpace: 'nowrap' }, raiz, o.centro);
  const items = o.items.map(txt => el('div', { position: 'absolute', left: '0', top: '0', font: '600 40px/1 Archivo', color: K.tinta,
    background: K.blanco, padding: '14px 22px', borderRadius: '99px', boxShadow: `0 10px 24px ${K.sombra}`, border: `2px solid ${K.cielo}`,
    whiteSpace: 'nowrap' }, raiz, txt));
  const n = items.length, i0 = o.inicio ?? .3, vel = o.vel ?? .08;
  return {
    pintar(t) {
      const a0 = tramo(t, 0, .5);
      centro.style.opacity = a0;
      centro.style.transform = `translate(-50%,-50%) scale(${mezcla(.8, 1, E.atras(a0, 1.6)).toFixed(3)})`;
      anillo.setAttribute('opacity', tramo(t, .2, .7));
      anillo.setAttribute('stroke-dashoffset', (-t * 30).toFixed(1));
      items.forEach((it, i) => {
        const ang = i / n * Math.PI * 2 + t * vel * Math.PI * 2 - Math.PI / 2;
        const ti = i0 + i * .08, p = E.sale(tramo(t, ti, ti + .7));
        const r = mezcla(2.4, 1, p);
        const x = cx + Math.cos(ang) * rx * r, y = cy + Math.sin(ang) * ry * r;
        const prof = Math.sin(ang);                       // −1 atrás del centro, 1 adelante
        it.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) translate(-50%,-50%) scale(${(.74 + .34 * (prof + 1) / 2).toFixed(3)})`;
        it.style.opacity = (tramo(t, ti, ti + .2) * (.5 + .5 * (prof + 1) / 2)).toFixed(3);
        it.style.zIndex = prof > 0 ? 60 : 10;
        it.style.filter = prof < -.3 ? `blur(${((-prof - .3) * 2.2).toFixed(2)}px)` : 'none';
      });
    },
  };
}

// ───────────────────────────────────────── 13 · el póster que no alcanza (frame escape)
// Un póster con foto y una palabra grande: la palabra crece y se sale del marco por arriba y por los lados; por abajo
// sigue adentro. o: { src, palabra, t0, fondo }
export function escapeMarco(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', background: o.fondo ?? K.crema, overflow: 'hidden' }, padre);
  const capa = el('div', { position: 'absolute', inset: '0' }, raiz);
  const MX = 190, MY = 470, MW = 640, MH = 760, B = 22;
  const poster = el('div', { position: 'absolute', left: `${MX}px`, top: `${MY}px`, width: `${MW}px`, height: `${MH}px`, background: K.blanco,
    boxShadow: `0 40px 90px ${K.sombra}` }, capa);
  const ventana = el('div', { position: 'absolute', left: `${B}px`, top: `${B}px`, right: `${B}px`, bottom: `${B}px`, overflow: 'hidden' }, poster);
  const foto = el('img', { width: '100%', height: '100%', objectFit: 'cover', display: 'block', transformOrigin: '50% 60%' }, ventana);
  foto.src = o.src;
  // la palabra va en una capa recortada solo por el borde de abajo de la ventana: puede salirse por arriba y por los lados
  const suelta = el('div', { position: 'absolute', inset: '0', clipPath: `inset(0 0 ${FH - (MY + MH - B)}px 0)` }, capa);
  const palabra = el('div', { position: 'absolute', left: `${MX}px`, width: `${MW}px`, top: `${MY + MH - B - 250}px`, textAlign: 'center',
    font: '900 170px/.86 Archivo', letterSpacing: '-.045em', color: K.blanco, transformOrigin: '50% 100%' }, suelta, o.palabra);
  const t0 = o.t0 ?? 1.1;
  const cam = camara(capa, [{ t: 0, z: .96, ladea: 8 }, { t: 3.6, z: 1.04, ladea: -5, curva: 'l' }], { deriva: 3 });
  return {
    pintar(t) {
      cam.pintar(t);
      const a = tramo(t, 0, .45);
      poster.style.opacity = a; poster.style.transform = `translateY(${((1 - E.sale(a)) * 60).toFixed(1)}px)`;
      foto.style.transform = `scale(${mezcla(1.15, 1.02, E.sale(tramo(t, 0, 3))).toFixed(4)})`;
      const p = tramo(t, t0, t0 + .7);
      palabra.style.opacity = tramo(t, .35, .7);
      palabra.style.transform = `translateY(${(-E.atras(p, 1.5) * 210).toFixed(1)}px) scale(${mezcla(1, 1.42, E.atras(p, 1.5)).toFixed(4)})`;
      palabra.style.textShadow = `0 ${(10 + 30 * p).toFixed(0)}px ${(24 + 40 * p).toFixed(0)}px rgba(0,0,0,${(.25 + .2 * p).toFixed(2)})`;
    },
  };
}

// ───────────────────────────────────────── 14 · el portal: la cámara se mete por un hueco y sale en la otra escena
// Corte entre a y b. El hueco está en a (por ejemplo, la «O» de una palabra): x, y y r en px de pantalla.
export function portal(a, b, t, t0, o = {}) {
  const d = o.dur ?? .9, x = o.x ?? 540, y = o.y ?? 960, r0 = o.r ?? 60;
  const p = tramo(t, t0, t0 + d), smax = 1250 / r0, s = Math.pow(smax, E.entra(p));
  a.style.visibility = p < 1 ? 'visible' : 'hidden';
  b.style.visibility = t >= t0 ? 'visible' : 'hidden';
  a.style.transformOrigin = b.style.transformOrigin = `${x}px ${y}px`;
  a.style.transform = `scale(${s.toFixed(4)})`; a.style.filter = `blur(${(8 * p).toFixed(2)}px)`;
  b.style.clipPath = p < 1 ? `circle(${(r0 * s).toFixed(1)}px at ${x}px ${y}px)` : 'none';
  b.style.transform = `scale(${mezcla(1.6, 1, E.sale(p)).toFixed(4)})`;
  if (t < t0) { a.style.transform = 'none'; a.style.filter = 'none'; }
}

// ───────────────────────────────────────── 15 · el estudio: se prenden las luces y aparece el objeto (studio reveal)
// o: { html (lo que se presenta; por omisión, una hoja), ancho, alto }
export function estudio(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', overflow: 'hidden', perspective: '2000px',
    background: 'radial-gradient(ellipse at 50% 36%, #FFFFFF 0%, #EFEAE0 42%, #D8D0C1 100%)' }, padre);
  const cx = 504, piso = 1080, W = o.ancho ?? 560, H = o.alto ?? 700;
  el('div', { position: 'absolute', left: '-10%', right: '-10%', top: `${piso}px`, bottom: '0',
    background: 'linear-gradient(#E6DFD2, #CEC5B4)' }, raiz);
  const sombra = el('div', { position: 'absolute', left: `${cx - 300}px`, top: `${piso - 34}px`, width: '600px', height: '80px', borderRadius: '50%',
    background: 'radial-gradient(rgba(22,35,63,.38), rgba(22,35,63,0) 70%)' }, raiz);
  const html = o.html ?? `<div style="font:400 78px/1.02 'Instrument Serif';color:${K.tinta}">Manual<br>de apertura</div>` +
    `<div class="mono" style="font-size:20px;color:${K.oro};margin:18px 0 26px">Cafetería · v1</div>` +
    [92, 80, 88, 64, 84, 70].map(w => `<div style="height:16px;width:${w}%;border-radius:8px;background:rgba(22,35,63,.14);margin-top:20px"></div>`).join('');
  const hacer = () => el('div', { position: 'absolute', left: `${cx - W / 2}px`, top: `${piso - H}px`, width: `${W}px`, height: `${H}px`, boxSizing: 'border-box',
    padding: '48px 44px', background: K.blanco, borderRadius: '22px', boxShadow: '0 30px 60px rgba(22,35,63,.22)', transformOrigin: '50% 100%' }, raiz, html);
  const reflejo = hacer();
  reflejo.style.boxShadow = 'none';
  reflejo.style.webkitMaskImage = 'linear-gradient(to top, rgba(0,0,0,.5), rgba(0,0,0,0) 45%)';
  const objeto = hacer();
  const luz = el('div', { position: 'absolute', left: '50%', top: '-260px', width: '1100px', height: '1700px', marginLeft: '-550px',
    background: 'radial-gradient(ellipse at 50% 0%, rgba(255,255,255,.95), rgba(255,255,255,0) 62%)', transformOrigin: '50% 0',
    mixBlendMode: 'screen', pointerEvents: 'none' }, raiz);
  return {
    pintar(t) {
      // las luces: arranca a oscuras, un parpadeo y se prende
      const on = E.sale(tramo(t, .25, .9)), parpadeo = t > .3 && t < .42 ? .55 : 1;
      raiz.style.filter = `brightness(${(mezcla(.22, 1, on) * parpadeo).toFixed(3)})`;
      luz.style.transform = `rotate(${mezcla(-38, 0, E.sale(tramo(t, .2, 1.4))).toFixed(2)}deg)`;
      luz.style.opacity = mezcla(.2, .9, on);
      // el objeto sube y gira sobre sí mismo hasta quedar de frente
      const p = tramo(t, .7, 1.6), giro = mezcla(42, 0, E.sale(tramo(t, .7, 2.4))) + Math.sin(t * 1.3) * 3 * tramo(t, 2.4, 3);
      const sube = (1 - E.atras(p, 1.3)) * 260;
      objeto.style.opacity = tramo(t, .7, .9);
      objeto.style.transform = `translateY(${sube.toFixed(1)}px) rotateY(${giro.toFixed(2)}deg)`;
      reflejo.style.opacity = (.35 * tramo(t, .9, 1.4)).toFixed(3);
      reflejo.style.transform = `translateY(${(H - sube).toFixed(1)}px) scaleY(-1) rotateY(${(-giro).toFixed(2)}deg)`;
      reflejo.style.transformOrigin = '50% 0';
      sombra.style.opacity = tramo(t, .9, 1.5);
    },
  };
}

// ───────────────────────────────────────── 16 · el vértigo (dolly zoom): el fondo se viene encima y el texto no se mueve
// o: { src, texto, oro, t0, t1 }
export function dolly(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', overflow: 'hidden', background: K.tinta }, padre);
  const fondo = el('div', { position: 'absolute', inset: '0', transformOrigin: '50% 45%' }, raiz);
  const img = el('img', { width: '100%', height: '100%', objectFit: 'cover', display: 'block' }, fondo);
  img.src = o.src;
  // las líneas de fuga refuerzan la profundidad
  const g = svg('svg', { width: FW, height: FH, style: 'position:absolute;left:0;top:0;opacity:.35' }, fondo);
  for (let i = 0; i < 28; i++) {
    const a = i / 28 * Math.PI * 2;
    svg('line', { x1: 540, y1: 864, x2: 540 + Math.cos(a) * 1800, y2: 864 + Math.sin(a) * 1800, stroke: K.blanco, 'stroke-width': 2 }, g);
  }
  const vineta = el('div', { position: 'absolute', inset: '0', pointerEvents: 'none' }, raiz);
  const frente = el('div', { position: 'absolute', left: `${SEGURA.izquierda + 10}px`, right: `${BOTONES.derecha}px`, top: '730px',
    font: '400 112px/1.0 "Instrument Serif"', color: K.blanco, textShadow: '0 10px 40px rgba(0,0,0,.55)' }, raiz,
    conOro(o.texto, o.oro, K.resalte));
  const t0 = o.t0 ?? .4, t1 = o.t1 ?? 3.2;
  return {
    pintar(t) {
      const p = CURVAS.io(tramo(t, t0, t1));
      fondo.style.transform = `scale(${mezcla(1, 1.85, p).toFixed(4)})`;
      img.style.filter = `blur(${(p * 3).toFixed(2)}px) brightness(${mezcla(.95, .7, p).toFixed(3)})`;
      vineta.style.boxShadow = `inset 0 0 ${(120 + 260 * p).toFixed(0)}px rgba(0,0,0,${(.35 + .4 * p).toFixed(2)})`;
      const a = E.sale(tramo(t, 0, .4));
      frente.style.opacity = a;
      frente.style.transform = `scale(${mezcla(1.04, .97, p).toFixed(4)})`;   // casi quieto: es lo que no se mueve
    },
  };
}

// ───────────────────────────────────────── 17 · la portada de revista (magazine cover)
// o: { src, cabecera, numero, lineas: [{ n, txt }], color (de la cabecera) }
export function revista(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', overflow: 'hidden', background: K.crema, perspective: '2400px' }, padre);
  const tapa = el('div', { position: 'absolute', inset: '0', overflow: 'hidden', transformOrigin: '50% 55%', boxShadow: '0 50px 100px rgba(22,35,63,.35)' }, raiz);
  const foto = el('img', { position: 'absolute', inset: '0', width: '100%', height: '100%', objectFit: 'cover' }, tapa);
  foto.src = o.src;
  el('div', { position: 'absolute', inset: '0', background: 'linear-gradient(rgba(0,0,0,.08), rgba(0,0,0,0) 30%, rgba(0,0,0,0) 45%, rgba(10,14,24,.62) 100%)' }, tapa);
  const L = SEGURA.izquierda + 10;
  const cab = el('div', { position: 'absolute', left: `${L - 6}px`, right: `${SEGURA.derecha}px`, top: '290px', font: '400 178px/.9 "Instrument Serif"',
    letterSpacing: '-.025em', color: o.color ?? K.rojo, whiteSpace: 'nowrap' }, tapa);
  const letras = [...(o.cabecera ?? 'NEGOCIOS')].map(c => el('span', { display: 'inline-block' }, cab, c));
  const num = el('div', { position: 'absolute', left: `${L}px`, top: '462px', fontSize: '22px', color: K.tinta }, tapa, o.numero ?? 'N.º 1 · Octubre 2026');
  num.className = 'mono';
  const lineas = (o.lineas ?? []).map((l, i) => {
    const f = el('div', { position: 'absolute', left: `${L}px`, right: `${BOTONES.derecha + 40}px`, top: `${860 + i * 118}px`, color: K.blanco }, tapa,
      `<span style="font:400 64px/1 'Instrument Serif';color:${K.resalte};font-style:italic;margin-right:14px">${l.n}</span>` +
      `<span style="font:800 36px/1.1 Archivo;text-transform:uppercase;letter-spacing:.01em">${l.txt}</span>`);
    f.style.textShadow = '0 4px 18px rgba(0,0,0,.45)';
    return f;
  });
  const codigo = el('div', { position: 'absolute', left: '640px', top: '1130px', width: '128px', height: '84px', background: K.blanco, padding: '8px',
    boxSizing: 'border-box', display: 'flex', gap: '2px', alignItems: 'stretch' }, tapa);
  const r = azar(5); for (let i = 0; i < 26; i++) el('div', { flex: 'none', width: `${1 + Math.floor(r() * 3)}px`, background: '#111' }, codigo);
  return {
    pintar(t) {
      foto.style.transform = `scale(${mezcla(1.12, 1.0, E.sale(tramo(t, 0, 1.2))).toFixed(4)})`;
      letras.forEach((s, i) => { const p = tramo(t, .15 + i * .05, .15 + i * .05 + .35);
        s.style.opacity = p; s.style.transform = `translateY(${((1 - E.atras(p, 1.8)) * -90).toFixed(1)}px)`; });
      num.style.opacity = tramo(t, .6, .9);
      lineas.forEach((f, i) => { const p = tramo(t, .8 + i * .18, .8 + i * .18 + .4);
        f.style.opacity = p; f.style.transform = `translateX(${((1 - E.sale(p)) * -80).toFixed(1)}px)`; });
      codigo.style.opacity = tramo(t, 1.5, 1.7);
      // al final la portada se vuelve una revista sobre la mesa
      const k = CURVAS.io(tramo(t, 2.3, 3.4));
      tapa.style.transform = `scale(${mezcla(1, .8, k).toFixed(4)}) rotateY(${(-16 * k).toFixed(2)}deg) rotateX(${(7 * k).toFixed(2)}deg) rotateZ(${(-2 * k).toFixed(2)}deg)`;
      tapa.style.borderRadius = `${(10 * k).toFixed(1)}px`;
    },
  };
}

// ───────────────────────────────────────── 18 · el vidrio líquido: un lente pasa, crece y te lleva a la otra escena
// o: { a, b (las dos escenas), t0, dur, x, y }. Se llama pintar(t) después de pintar las dos escenas.
export function vidrio(padre, o) {
  const x = o.x ?? 504, y = o.y ?? 768, t0 = o.t0 ?? 1.5, d = o.dur ?? 1.0;
  const lente = el('div', { position: 'absolute', left: `${x}px`, top: `${y}px`, width: '320px', height: '320px', marginLeft: '-160px', marginTop: '-160px',
    borderRadius: '50%', background: 'rgba(255,255,255,.10)', zIndex: 40, pointerEvents: 'none',
    boxShadow: 'inset 0 3px 2px rgba(255,255,255,.85), inset 0 -18px 40px rgba(255,255,255,.28), inset 0 0 0 1.5px rgba(255,255,255,.6), 0 30px 70px rgba(22,35,63,.28)' }, padre);
  const brillo = el('div', { position: 'absolute', left: '12%', top: '8%', width: '55%', height: '32%', borderRadius: '50%',
    background: 'linear-gradient(160deg, rgba(255,255,255,.75), rgba(255,255,255,0))', filter: 'blur(4px)' }, lente);
  return {
    pintar(t) {
      const ent = tramo(t, t0 - .7, t0), cre = tramo(t, t0, t0 + d * .55), sal = tramo(t, t0 + d * .45, t0 + d);
      const s = E.atras(ent, 1.6) * Math.pow(9, cre * cre);
      lente.style.transform = `scale(${s.toFixed(4)})`;
      lente.style.opacity = ent > 0 ? (1 - E.sale(sal)).toFixed(3) : 0;
      const blur = 26 * (1 - sal);
      lente.style.backdropFilter = lente.style.webkitBackdropFilter = `blur(${blur.toFixed(1)}px) saturate(1.7) brightness(1.06)`;
      brillo.style.opacity = (1 - cre).toFixed(3);
      const cambio = t >= t0 + d * .45;
      o.a.style.visibility = cambio ? 'hidden' : 'visible';
      o.b.style.visibility = cambio ? 'visible' : 'hidden';
      o.a.style.transform = `scale(${mezcla(1, 1.25, E.entra(cre)).toFixed(4)})`;
      o.b.style.transform = `scale(${mezcla(1.25, 1, E.sale(sal)).toFixed(4)})`;
    },
  };
}

// ───────────────────────────────────────── 19 · el marco que se rompe (green screen frame break)
// Un video o foto en un cuadro con borde; el borde se rompe en pedazos y la imagen se agranda a pantalla completa.
// o: { src, t0 }. Para video, cambiar img.src por cuadro desde afuera (devuelve img).
export function rompeMarco(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', overflow: 'hidden', background: o.fondo ?? K.papel }, padre);
  const R0 = { x: 210, y: 470, w: 600, h: 760 }, B = 26;
  const caja = el('div', { position: 'absolute', overflow: 'hidden', background: '#000' }, raiz);
  const img = el('img', { width: '100%', height: '100%', objectFit: 'cover', display: 'block' }, caja);
  img.src = o.src;
  const borde = el('div', { position: 'absolute', left: `${R0.x - B}px`, top: `${R0.y - B}px`, width: `${R0.w + 2 * B}px`, height: `${R0.h + 2 * B}px`,
    boxSizing: 'border-box', border: `${B}px solid ${K.blanco}`, boxShadow: `0 40px 80px ${K.sombra}` }, raiz);
  // los pedazos del borde: 18 tramos alrededor del cuadro, cada uno sale disparado con su giro
  const r = azar(11), pedazos = [];
  const lado = (x0, y0, x1, y1, n) => { for (let i = 0; i < n; i++) {
    const a = i / n, b = (i + 1) / n;
    const px = mezcla(x0, x1, a), py = mezcla(y0, y1, a), qx = mezcla(x0, x1, b), qy = mezcla(y0, y1, b);
    const w = Math.max(B * 2.2, Math.abs(qx - px)), h = Math.max(B * 2.2, Math.abs(qy - py));
    const j = () => (r() * 18).toFixed(0);   // astilla: un cuadrilátero irregular
    const e = el('div', { position: 'absolute', left: `${Math.min(px, qx) - B * .6}px`, top: `${Math.min(py, qy) - B * .6}px`, width: `${w}px`, height: `${h}px`,
      background: K.blanco, opacity: 0, filter: 'drop-shadow(0 8px 14px rgba(22,35,63,.28))',
      clipPath: `polygon(${j()}% ${j()}%, ${100 - j()}% ${j()}%, ${100 - j()}% ${100 - j()}%, ${j()}% ${100 - j()}%)` }, raiz);
    const cxp = Math.min(px, qx) + w / 2 - 510, cyp = Math.min(py, qy) + h / 2 - 850;
    const n0 = Math.hypot(cxp, cyp) || 1;
    pedazos.push({ e, vx: cxp / n0 * (500 + r() * 600), vy: cyp / n0 * (500 + r() * 600) - 300, giro: (r() - .5) * 720 });
  } };
  lado(R0.x - B, R0.y - B, R0.x + R0.w + B, R0.y - B, 5);          // arriba
  lado(R0.x + R0.w, R0.y, R0.x + R0.w, R0.y + R0.h, 4);              // derecha
  lado(R0.x - B, R0.y + R0.h, R0.x + R0.w + B, R0.y + R0.h, 5);      // abajo
  lado(R0.x - B, R0.y, R0.x - B, R0.y + R0.h, 4);                    // izquierda
  const destello = el('div', { position: 'absolute', inset: '0', background: K.blanco, opacity: 0, pointerEvents: 'none' }, raiz);
  const t0 = o.t0 ?? 1.4;
  return {
    img,
    pintar(t) {
      const a = tramo(t, 0, .4), roto = t >= t0;
      const k = E.expo(tramo(t, t0, t0 + .6));
      const R = { x: mezcla(R0.x, 0, k), y: mezcla(R0.y, 0, k), w: mezcla(R0.w, FW, k), h: mezcla(R0.h, FH, k) };
      Object.assign(caja.style, { left: `${R.x}px`, top: `${R.y}px`, width: `${R.w}px`, height: `${R.h}px`, opacity: a });
      const temblor = t > t0 - .35 && t < t0 ? Math.sin(t * 90) * 4 : 0;     // el marco tiembla antes de romperse
      borde.style.opacity = roto ? 0 : a;
      borde.style.transform = caja.style.transform = `translateX(${temblor.toFixed(1)}px)`;
      const dt = Math.max(0, t - t0);
      pedazos.forEach(p => {
        p.e.style.opacity = roto ? (1 - tramo(dt, .5, .9)).toFixed(3) : 0;
        p.e.style.transform = `translate(${(p.vx * dt).toFixed(1)}px, ${(p.vy * dt + 1400 * dt * dt).toFixed(1)}px) rotate(${(p.giro * dt).toFixed(1)}deg)`;
      });
      destello.style.opacity = (.5 * (1 - tramo(t, t0, t0 + .25)) * (roto ? 1 : 0)).toFixed(3);
      img.style.transform = `scale(${mezcla(1.08, 1, k).toFixed(4)})`;
    },
  };
}

// ───────────────────────────────────────── 20 · el zoom digital («mejorá la imagen»)
// Sobre una foto: aparece el visor, la cámara salta a ×2 y a ×4 con pixelado que se aclara, rayas de monitor y datos.
// o: { src, foco: { x, y } (punto de la pantalla al que va), pasos: [2, 4], en: [segundos de cada salto] }
export function zoomDigital(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', overflow: 'hidden', background: '#000' }, padre);
  const lienzo = el('canvas', { position: 'absolute', inset: '0', width: `${FW}px`, height: `${FH}px` }, raiz);
  lienzo.width = FW; lienzo.height = FH;
  const ctx = lienzo.getContext('2d');
  const base = document.createElement('canvas'); base.width = FW; base.height = FH;
  const chico = document.createElement('canvas');
  const img = new Image(); img.src = o.src;
  const listo = img.decode().then(() => {   // la foto ajustada al cuadro (cover) una sola vez
    const s = Math.max(FW / img.naturalWidth, FH / img.naturalHeight), w = img.naturalWidth * s, h = img.naturalHeight * s;
    base.getContext('2d').drawImage(img, (FW - w) / 2, (FH - h) / 2, w, h);
  }).catch(() => {});
  el('div', { position: 'absolute', inset: '0', pointerEvents: 'none', opacity: .22,
    background: 'repeating-linear-gradient(0deg, rgba(0,0,0,.55) 0 2px, transparent 2px 5px)' }, raiz);
  const f = o.foco ?? { x: 540, y: 900 }, pasos = o.pasos ?? [2, 4], en = o.en ?? [.9, 1.9];
  const visor = el('div', { position: 'absolute', left: `${f.x - 170}px`, top: `${f.y - 120}px`, width: '340px', height: '240px' }, raiz);
  const esq = (l, tp, bl, bt) => el('div', { position: 'absolute', width: '46px', height: '46px', [l]: '0', [tp]: '0',
    [bl]: `5px solid ${K.resalte}`, [bt]: `5px solid ${K.resalte}` }, visor);
  esq('left', 'top', 'borderLeft', 'borderTop'); esq('right', 'top', 'borderRight', 'borderTop');
  esq('left', 'bottom', 'borderLeft', 'borderBottom'); esq('right', 'bottom', 'borderRight', 'borderBottom');
  const hud = el('div', { position: 'absolute', left: `${SEGURA.izquierda + 10}px`, top: `${SEGURA.arriba + 14}px`, fontSize: '28px', color: K.resalte,
    background: 'rgba(0,0,0,.5)', padding: '8px 14px', borderRadius: '8px' }, raiz, 'ZOOM ×1');
  hud.className = 'mono';
  const datos = el('div', { position: 'absolute', left: `${SEGURA.izquierda + 10}px`, top: '1190px', fontSize: '22px', color: K.blanco, opacity: .85 }, raiz,
    `X ${f.x} · Y ${f.y} · REC`);
  datos.className = 'mono';
  return {
    listo,
    pintar(t) {
      let z = 1, pix = 1;
      en.forEach((te, i) => {
        const p = tramo(t, te, te + .22);
        if (t >= te) { z = mezcla(i ? pasos[i - 1] : 1, pasos[i], E.expo(p)); pix = Math.max(pix, Math.round(mezcla(28, 1, tramo(t, te + .15, te + .7)))); }
      });
      const sw = FW / z, sh = FH / z;
      const sx = Math.min(FW - sw, Math.max(0, f.x - sw / 2)), sy = Math.min(FH - sh, Math.max(0, f.y - sh / 2));
      if (pix > 1) {
        chico.width = Math.ceil(FW / pix); chico.height = Math.ceil(FH / pix);
        const c2 = chico.getContext('2d'); c2.imageSmoothingEnabled = true;
        c2.drawImage(base, sx, sy, sw, sh, 0, 0, chico.width, chico.height);
        ctx.imageSmoothingEnabled = false; ctx.drawImage(chico, 0, 0, FW, FH);
      } else { ctx.imageSmoothingEnabled = true; ctx.drawImage(base, sx, sy, sw, sh, 0, 0, FW, FH); }
      const v = E.atras(tramo(t, .2, .55), 1.4);
      visor.style.opacity = tramo(t, .2, .3) * (t > en[0] + .1 ? .9 : 1);
      visor.style.transform = `scale(${mezcla(1.6, 1, v).toFixed(3)})`;
      hud.textContent = `ZOOM ×${t >= en[1] + .2 ? pasos[1] : t >= en[0] + .2 ? pasos[0] : 1}`;
      datos.style.opacity = Math.sin(t * 6) > -.6 ? .85 : .2;
    },
  };
}

// ───────────────────────────────────────── 21 · el marcador: notas a mano que se dibujan solas
// Círculos, subrayados y flechas de marcador sobre cualquier escena, más una nota escrita.
// o: { trazos: [{ tipo: 'circulo'|'subraya'|'flecha', x, y, w, h, t0, color }], notas: [{ texto, x, y, t0, rot, color }] }
export function marcador(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', pointerEvents: 'none', zIndex: 30 }, padre);
  const g = svg('svg', { width: FW, height: FH, style: 'position:absolute;left:0;top:0;overflow:visible' }, raiz);
  const r = azar(19);
  const trazos = (o.trazos ?? []).map(tz => {
    let d;
    if (tz.tipo === 'circulo') {          // dos vueltas un poco corridas, como a mano
      const pts = []; for (let i = 0; i <= 60; i++) { const a = -2.2 + i / 60 * Math.PI * 2.15, j = 1 + (r() - .5) * .05;
        pts.push([tz.x + tz.w / 2 + Math.cos(a) * tz.w / 2 * j, tz.y + tz.h / 2 + Math.sin(a) * tz.h / 2 * j]); }
      d = pts.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ');
    } else if (tz.tipo === 'subraya') {
      d = `M${tz.x},${tz.y} C${tz.x + tz.w * .3},${tz.y + 10} ${tz.x + tz.w * .6},${tz.y - 8} ${tz.x + tz.w},${tz.y + 4}`;
    } else {                               // flecha curva de (x, y) a (x + w, y + h)
      const x1 = tz.x + tz.w, y1 = tz.y + tz.h, a = Math.atan2(tz.h, tz.w);
      d = `M${tz.x},${tz.y} Q${tz.x + tz.w * .15},${tz.y + tz.h * .85} ${x1},${y1}` +
        ` M${x1 - 34 * Math.cos(a - .5)},${y1 - 34 * Math.sin(a - .5)} L${x1},${y1} L${x1 - 34 * Math.cos(a + .5)},${y1 - 34 * Math.sin(a + .5)}`;
    }
    const p = svg('path', { d, fill: 'none', stroke: tz.color ?? K.rojo, 'stroke-width': tz.grosor ?? 9, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
    const L = p.getTotalLength(); p.setAttribute('stroke-dasharray', `${L} ${L}`); p.setAttribute('stroke-dashoffset', L);
    return { p, L, t0: tz.t0 ?? 0, dur: tz.dur ?? .45 };
  });
  const notas = (o.notas ?? []).map(n => {
    const e = el('div', { position: 'absolute', left: `${n.x}px`, top: `${n.y}px`, font: `${n.tam ?? 54}px/1.1 Marcador`, color: n.color ?? K.rojo,
      transform: `rotate(${n.rot ?? -4}deg)`, whiteSpace: 'nowrap' }, raiz, n.texto);
    return { e, t0: n.t0 ?? 0 };
  });
  return {
    pintar(t) {
      trazos.forEach(z => z.p.setAttribute('stroke-dashoffset', (z.L * (1 - E.sale(tramo(t, z.t0, z.t0 + z.dur)))).toFixed(1)));
      notas.forEach(n => { const p = tramo(t, n.t0, n.t0 + .6);
        n.e.style.clipPath = `inset(-20px ${((1 - p) * 100).toFixed(1)}% -20px -10px)`; });
    },
  };
}

// ───────────────────────────────────────── Estilo Vox (Kenneth, 21-oct: «vox style animation»)
// Papel con grano, recortes con fotos en semitono, documentos con una frase marcada con resaltador amarillo y
// movimiento «de a dos» (12 cuadros por segundo), como stop-motion.
export const aDos = t => Math.floor(t * 12) / 12;   // el tiempo en saltos de 1/12 s: el movimiento de stop-motion

// 22 · el grano del papel: una capa encima de todo, que tiembla de a dos
const GRANO = 'url("data:image/svg+xml;utf8,' + encodeURIComponent(
  '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>' +
  '<feColorMatrix values="0 0 0 0 .35  0 0 0 0 .3  0 0 0 0 .25  0 0 0 .55 0"/></filter><rect width="300" height="300" filter="url(#g)"/></svg>') + '")';
export function textura(padre, o = {}) {
  const capa = el('div', { position: 'absolute', inset: '-40px', backgroundImage: GRANO, opacity: o.fuerza ?? .32, mixBlendMode: 'multiply',
    pointerEvents: 'none', zIndex: 90 }, padre);
  return { pintar(t) { const q = Math.floor(t * 12), r = azar(q + 3); capa.style.transform = `translate(${(r() * 40 - 20).toFixed(0)}px, ${(r() * 40 - 20).toFixed(0)}px)`; } };
}

// Borde de papel rasgado: un polígono con dientes chicos y desparejos (para clip-path)
export function rasgado(semilla = 3, dientes = 26, prof = 2.2) {
  const r = azar(semilla), p = [];
  for (let i = 0; i <= dientes; i++) p.push(`${(i / dientes * 100).toFixed(2)}% ${(r() * prof).toFixed(2)}%`);
  for (let i = 0; i <= dientes; i++) p.push(`${(100 - r() * prof * .6).toFixed(2)}% ${(i / dientes * 100).toFixed(2)}%`);
  for (let i = dientes; i >= 0; i--) p.push(`${(i / dientes * 100).toFixed(2)}% ${(100 - r() * prof).toFixed(2)}%`);
  for (let i = dientes; i >= 0; i--) p.push(`${(r() * prof * .6).toFixed(2)}% ${(i / dientes * 100).toFixed(2)}%`);
  return `polygon(${p.join(',')})`;
}

// 23 · el documento con la frase resaltada (lo más Vox): un recorte de papel, la cámara va a la frase, el resaltador
// la marca y lo demás se apaga. o: { titulo, fuente, lineas: [texto], marcada: índice, t0 (cuando marca) }
export function documento(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', overflow: 'hidden', background: o.fondo ?? '#E9E2D2' }, padre);
  const capa = el('div', { position: 'absolute', inset: '0' }, raiz);
  const hoja = el('div', { position: 'absolute', left: '150px', top: '360px', width: '780px', padding: '70px 64px 90px', boxSizing: 'border-box',
    background: '#FBF8F1', clipPath: rasgado(o.semilla ?? 4), transform: 'rotate(-2.2deg)' }, capa);
  el('div', { fontSize: '22px', color: K.rojo, marginBottom: '22px' }, hoja, o.fuente ?? 'Fuente · fecha').className = 'mono';
  el('div', { font: '400 66px/1.04 "Instrument Serif"', color: K.tinta, marginBottom: '34px' }, hoja, o.titulo ?? '');
  const filas = (o.lineas ?? []).map((txt, i) => el('div', { font: '400 34px/1.5 Georgia, serif', color: '#2a2f3c' }, hoja,
    i === o.marcada ? `<span class="resalte">${txt}</span>` : txt));
  const raya = hoja.querySelector('.resalte');
  if (raya) raya.style.backgroundSize = '0% 80%';
  const t0 = o.t0 ?? 1.2;
  const cam = camara(capa, o.claves ?? [{ t: 0, z: .86, giro: 4, y: 40 }, { t: t0 - .2, z: 1, curva: 's' },
    { t: t0 + .6, z: 1.22, y: -60, x: 20, curva: 'io' }, { t: 4.5, z: 1.26, y: -70, x: 20, curva: 'l' }], { deriva: 0 });
  const grano = textura(raiz);
  return {
    hoja,
    pintar(t) {
      cam.pintar(aDos(t));
      const p = tramo(t, t0, t0 + .5);
      if (raya) raya.style.backgroundSize = `${(E.sale(p) * 100).toFixed(1)}% 80%`;
      filas.forEach((f, i) => { f.style.opacity = i === o.marcada ? 1 : mezcla(1, .35, tramo(t, t0 + .3, t0 + .8)); });
      grano.pintar(t);
    },
  };
}

// 24 · el collage: fotos recortadas en semitono, papeles de color y movimiento de a dos
// o: { fotos: [{ src, x, y, w, h, rot, t0, tinte }], bloques: [{ x, y, w, h, color, rot, t0 }], titulo: { texto, x, y, t0 } }
export function collage(padre, o) {
  const raiz = el('div', { position: 'absolute', inset: '0', overflow: 'hidden', background: o.fondo ?? '#EFE8D8' }, padre);
  const piezas = [];
  (o.bloques ?? []).forEach((b, i) => piezas.push({ e: el('div', { position: 'absolute', left: `${b.x}px`, top: `${b.y}px`, width: `${b.w}px`, height: `${b.h}px`,
    background: b.color ?? K.resalte, clipPath: rasgado(30 + i, 18, 1.8) }, raiz), rot: b.rot ?? 0, t0: b.t0 ?? 0 }));
  (o.fotos ?? []).forEach((f, i) => {
    const c = el('div', { position: 'absolute', left: `${f.x}px`, top: `${f.y}px`, width: `${f.w}px`, height: `${f.h}px`, background: '#fff', padding: '14px',
      boxSizing: 'border-box', clipPath: rasgado(10 + i, 22, 1.6) }, raiz);
    const v = el('div', { position: 'relative', width: '100%', height: '100%', overflow: 'hidden' }, c);
    const im = el('img', { width: '100%', height: '100%', objectFit: 'cover', display: 'block', filter: 'grayscale(1) contrast(1.35) brightness(1.05)' }, v);
    im.src = f.src;
    // el semitono: una trama de puntos encima de la foto en blanco y negro, y un tinte de color de papel
    el('div', { position: 'absolute', inset: '0', mixBlendMode: 'screen', opacity: .5,
      backgroundImage: 'radial-gradient(circle, rgba(0,0,0,0) 38%, rgba(255,255,255,1) 44%)', backgroundSize: '9px 9px' }, v);
    el('div', { position: 'absolute', inset: '0', mixBlendMode: 'multiply', background: f.tinte ?? 'rgba(195,214,240,.6)' }, v);
    piezas.push({ e: c, rot: f.rot ?? 0, t0: f.t0 ?? 0 });
  });
  const tit = o.titulo ? el('div', { position: 'absolute', left: `${o.titulo.x ?? 140}px`, top: `${o.titulo.y ?? 980}px`, maxWidth: `${FW - (o.titulo.x ?? 140) - BOTONES.derecha}px`,
    font: '400 86px/1 "Instrument Serif"', color: K.tinta, background: '#FBF8F1', padding: '16px 26px 22px', clipPath: rasgado(77, 14, 2.4),
    transform: 'rotate(-2deg)' }, raiz, o.titulo.texto) : null;
  const grano = textura(raiz);
  return {
    pintar(t) {
      const q = aDos(t);
      piezas.forEach((p, i) => {
        const k = tramo(q, p.t0, p.t0 + .25), r = azar(Math.floor(t * 6) + i);   // tiembla un poco, de a dos
        p.e.style.opacity = k > 0 ? 1 : 0;
        p.e.style.transform = `translate(${((1 - E.sale(k)) * (i % 2 ? 160 : -160) + r() * 3).toFixed(1)}px, ${((1 - E.sale(k)) * 40 + r() * 3).toFixed(1)}px) rotate(${(p.rot + (1 - k) * 8).toFixed(2)}deg) scale(${mezcla(1.15, 1, k).toFixed(3)})`;
      });
      if (tit) { const k = tramo(q, o.titulo.t0 ?? 1.2, (o.titulo.t0 ?? 1.2) + .25); tit.style.opacity = k > 0 ? 1 : 0;
        tit.style.transform = `rotate(-2deg) scale(${mezcla(1.3, 1, E.sale(k)).toFixed(3)})`; }
      grano.pintar(t);
    },
  };
}

// ───────────────────────────────────────── 25 · el sello que golpea (stamp on): «APROBADO», lo que hace Kenneth
// Cae desde arriba girado, golpea con un temblor y deja la tinta un poco despareja. o: { texto, x, y, t0, color, rot }
export function sello(padre, o) {
  const color = o.color ?? K.rojo, rot = o.rot ?? -9;
  const s = el('div', { position: 'absolute', left: `${o.x ?? 300}px`, top: `${o.y ?? 760}px`, zIndex: 40, padding: '18px 34px 14px',
    border: `9px solid ${color}`, borderRadius: '18px', color, font: '900 96px/1 Archivo', letterSpacing: '.06em', textTransform: 'uppercase',
    opacity: 0, transformOrigin: '50% 50%', mixBlendMode: 'multiply',
    WebkitMaskImage: 'url("data:image/svg+xml;utf8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="220" height="220"><filter id="m"><feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.4 2.1"/></filter><rect width="220" height="220" filter="url(#m)"/></svg>') + '")' },
    padre, o.texto ?? 'Aprobado');
  const t0 = o.t0 ?? .6;
  return {
    pintar(t) {
      const p = tramo(t, t0 - .18, t0), k = tramo(t, t0, t0 + .35);
      s.style.opacity = t < t0 - .18 ? 0 : 1;
      const esc = t < t0 ? mezcla(2.6, 1, E.entra(p)) : 1 + .05 * Math.sin(k * Math.PI) * (1 - k);
      s.style.transform = `rotate(${(rot - (1 - p) * 14).toFixed(2)}deg) scale(${esc.toFixed(4)})`;
      s.style.filter = t < t0 ? `blur(${((1 - p) * 6).toFixed(2)}px)` : 'none';
      // el golpe sacude lo que está debajo
      if (o.sacude) { const g = t >= t0 ? Math.exp(-14 * (t - t0)) * Math.sin((t - t0) * 70) * 10 : 0; o.sacude.style.translate = `${g.toFixed(1)}px ${(g * .6).toFixed(1)}px`; }
    },
  };
}

// ───────────────────────────────────────── 26 · la máquina de escribir: el texto sale letra por letra con cursor
// o: { texto, x, y, ancho, t0, cps (letras por segundo), estilo }
export function maquina(padre, o) {
  const caja = el('div', { position: 'absolute', left: `${o.x ?? SEGURA.izquierda + 10}px`, top: `${o.y ?? 700}px`,
    width: `${o.ancho ?? 650}px`, font: '500 44px/1.4 "JetBrains Mono"', color: K.tinta, ...o.estilo }, padre);
  const txt = el('span', {}, caja), cursor = el('span', { display: 'inline-block', width: '.55em', height: '1.05em', marginLeft: '2px',
    verticalAlign: '-.15em', background: K.rojo }, caja);
  const t0 = o.t0 ?? .2, cps = o.cps ?? 22;
  return {
    pintar(t) {
      const n = Math.max(0, Math.min(o.texto.length, Math.floor((t - t0) * cps)));
      txt.textContent = o.texto.slice(0, n);
      cursor.style.opacity = (n < o.texto.length || Math.floor(t * 2.4) % 2 === 0) ? 1 : 0;
    },
  };
}
