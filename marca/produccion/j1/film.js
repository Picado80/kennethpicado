// J1 · «Prompt» son las instrucciones que le di — pizarra vertical, una sola toma, sin manos.
// Tiempos en segundos. La voz manda: cada dibujo cuelga de una palabra dicha, con at(tramo, palabra).
import * as W from './engine/wb.js';
import { clamp } from '/core/lib.js';

const FW = 1080, FH = 1920;
W.setFrame(FW, FH);
const TINTA = '#16233F', AZUL = '#2A5CB3', ROJO = '#B22B3F';
export const VO = { a: 0.30, b: 12.30 };          // inicio de cada tramo de voz
export const END = 24.6;
export const BPM = 96, BEAT = 60 / BPM;

// Subtítulos: [tramo, primera palabra, cuál aparición, última palabra, cuál aparición, texto]
const SUBS = [
  ['a', 'prompt', 0, 'ingenieros', 0, '«Prompt». Suena a algo de ingenieros.'],
  ['a', 'y', 0, 'instrucciones', 0, 'Y es lo que hacés todos los días: dar instrucciones.'],
  ['a', 'si', 0, 'informe', 0, 'Si a alguien nuevo le decís «haceme un informe»,'],
  ['a', 'te', 0, 'cosa', 0, 'te trae cualquier cosa.'],
  ['b', 'si', 0, 'cuando', 0, 'Si le decís para quién es, qué tiene que decir y para cuándo,'],
  ['b', 'te', 0, 'ocupas', 0, 'te trae lo que ocupás.'],
  ['b', 'con', 0, 'igual', 0, 'Con la IA es igual.'],
  ['b', 'un', 0, 'das', 0, 'Un prompt son las instrucciones que le das.'],
];

export async function build() {
  await W.loadFont('tech', 'fonts/EMSTech.json');
  const words = await (await fetch('voz/palabras.json')).json();
  const norm = s => s.toLowerCase().normalize('NFD').replace(/[^a-z0-9]/g, '');
  const at = (id, w, k = 0, which = 1) => {        // tiempo absoluto de la k-ésima aparición de la palabra w en el tramo id
    let n = 0; for (const x of words[id]) if (norm(x[0]) === norm(w) && n++ === k) return VO[id] + Math.max(0, x[which]);
    throw new Error(`la palabra ${w} no está en el tramo ${id}`);
  };
  const atE = (id, w, k = 0) => at(id, w, k, 2);

  const tl = new W.Timeline();
  const K = new W.Pen('tinta', TINTA, { park: [1270, 2060], len: 360 });
  const B = new W.Pen('azul', AZUL, { park: [1330, 1780], len: 360 });
  const R = new W.Pen('rojo', ROJO, { park: [1240, 2190], len: 360 });
  const PRE = new W.Pen('antes', TINTA);              // lo que ya estaba escrito al empezar (no se dibuja el marcador)
  const PENS = [K, B, R];
  const T = W.text;
  const fit = (str, x, y, max, o) => {                // letra que cabe en un ancho
    let s = T(str, x, y, o); if (s.width <= max) return s;
    return T(str, x, y, { ...o, h: o.h * max / s.width });
  };

  // ───────── la pizarra (unidades de mundo; el cuadro ve 1080×1920 con zoom 1)
  const CX = 1050;                                   // eje del dibujo (un poco a la izquierda: a la derecha va la interfaz)
  const BUR = { x: 600, y: 1470, w: 900, h: 430 };   // el globo del pedido
  const CAB = [CX, 2050, 50];                        // la cabeza de quien recibe el pedido
  const HOJA = { x: 770, y: 2360, w: 560, h: 700 };  // la hoja del resultado

  // restos de clases viejas, casi borrados
  const ghosts = [];
  {
    let seed = 99; const gR = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
    const viejas = ['lun 8 am', 'ojo!', 'x = 4', 'ok', 'pág. 12', '→ 3', 'vie', '2 + 2', 'ver'];
    for (let i = 0; i < 30; i++) {
      const x = gR() * 1800 + 180, y = gR() * 4000 + 200, k = gR();
      const o = { w: 11, alpha: .045 + gR() * .045, color: gR() < .25 ? '#8aa0c8' : '#9aa0a8' };
      if (k < .34) ghosts.push(...T(viejas[i % viejas.length], x, y, { h: 44 + gR() * 34, ...o }));
      else if (k < .58) ghosts.push(W.circle(x, y, 36 + gR() * 90, o));
      else if (k < .82) ghosts.push(...W.arrow(x, y, x + (gR() - .5) * 380, y + (gR() - .5) * 260, o));
      else ghosts.push(W.line(x, y, x + 160 + gR() * 380, y + (gR() - .5) * 70, o));
    }
  }

  // 0 · el rótulo de la serie ya está escrito
  const rot = T('IA sin jerga', 602, 372, { h: 38, w: 6 });
  tl.draw(PRE, [rot, W.line(600, 392, 600 + rot.width + 6, 394, { w: 5 })], -6, { by: -4 });

  // 1 · la palabra
  tl.draw(K, fit('PROMPT', CX, 760, 880, { h: 200, align: 'center' }), 0.12, { by: atE('a', 'prompt') + .22, tag: 'palabra' });
  // garabatos de ingeniero, rápidos, arriba a la derecha
  const eng = [1465, 452];
  const dientes = []; for (let i = 0; i < 6; i++) { const a = i * Math.PI / 3 + .2; dientes.push(W.line(eng[0] + Math.cos(a) * 30, eng[1] + Math.sin(a) * 30, eng[0] + Math.cos(a) * 44, eng[1] + Math.sin(a) * 44, { w: 8, bow: 0 })); }
  tl.draw(B, T('</>', 1010, 482, { h: 60 }), at('a', 'suena') - .05, { by: at('a', 'algo') + .2, tag: 'garabato 1' });
  tl.draw(B, T('{ }', 1240, 482, { h: 60 }), at('a', 'algo') + .25, { by: at('a', 'ingenieros') + .25, tag: 'garabato 2' });
  tl.draw(B, [W.circle(eng[0], eng[1], 28, { w: 8 }), ...dientes], at('a', 'ingenieros') + .3, { by: atE('a', 'ingenieros') + .15, tag: 'engranaje' });

  // 2 · la flecha que baja (la cámara va montada) y el globo vacío
  const tFlecha = at('a', 'y');
  tl.draw(K, W.arrow(CX, 1140, CX, 1425, { w: 10, head: 40 }), tFlecha, { by: atE('a', 'dias') + .1, tag: 'flecha 1' });
  tl.draw(K, [W.roundRect(BUR.x, BUR.y, BUR.w, BUR.h, 64, { w: 10 }), W.poly([[735, 1474], [668, 1396], [820, 1470]], { w: 10, smooth: 1 })],
    at('a', 'dar') - .2, { by: atE('a', 'instrucciones') + .05, tag: 'globo' });

  // 3 · quien recibe el pedido, y el pedido vago
  tl.draw(K, [W.line(CX, 1918, CX, 1986, { w: 9 }), W.circle(...CAB, { w: 10 }), W.curve([[955, 2186], [972, 2128], [CX, 2108], [1128, 2128], [1145, 2186]], { w: 10 })],
    at('a', 'alguien') - .1, { by: at('a', 'decis') + .3, tag: 'receptor' });
  tl.draw(K, fit('haceme un informe', BUR.x + 62, 1592, 770, { h: 62 }), at('a', 'haceme') - .1, { by: atE('a', 'informe') + .05, tag: 'pedido' });

  // 4 · lo que vuelve: flecha, hoja y un enredo
  let seed = 7; const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
  const enredo = []; for (let i = 0; i < 44; i++) { const a = i * 2.4 + rnd() * .9, r = .72 + .28 * rnd(); enredo.push([CX + Math.cos(a) * r * 240, 2712 + Math.sin(a) * r * 300]); }
  const tVuelve = at('a', 'te');
  tl.draw(B, W.arrow(CX, 2215, CX, 2326, { w: 10, head: 36 }), tVuelve - .1, { by: tVuelve + .28, tag: 'flecha 2' });
  tl.draw(B, W.rect(HOJA.x, HOJA.y, HOJA.w, HOJA.h, { w: 10 }), tVuelve + .3, { by: at('a', 'cualquier') + .3, tag: 'hoja' });
  tl.draw(B, W.curve(enredo, { w: 9, jitter: 1.4, smooth: 2 }), at('a', 'cualquier') + .34, { by: atE('a', 'cosa') + .12, tag: 'enredo' });

  // 5 · el giro: silencio y el borrador deshace el enredo (queda el fantasma)
  const tBorra = atE('a', 'cosa') + .32;
  tl.erase(W.zigzag(865, 2455, 370, 510, 5), tBorra, 1.0, { width: 150, strength: .9 });

  // 6 · el mismo pedido, ahora completo: cada renglón termina en su palabra
  tl.draw(K, T('+ para quién', BUR.x + 78, 1692, { h: 46 }), at('b', 'para', 0) - .25, { by: atE('b', 'es') + .1, tag: 'quién' });
  tl.draw(K, T('+ qué dice', BUR.x + 78, 1778, { h: 46 }), at('b', 'que', 0) - .1, { by: atE('b', 'decir') + .1, tag: 'qué' });
  tl.draw(K, T('+ para cuándo', BUR.x + 78, 1864, { h: 46 }), at('b', 'y') - .05, { by: atE('b', 'cuando') + .1, tag: 'cuándo' });

  // 7 · la hoja, limpia
  const tLimpia = at('b', 'te');
  tl.draw(B, [W.line(830, 2478, 1110, 2478, { w: 15 }), W.line(830, 2610, 1270, 2612, { w: 9 }), W.line(830, 2706, 1250, 2704, { w: 9 }), W.line(830, 2802, 1140, 2803, { w: 9 })],
    tLimpia - .1, { by: at('b', 'ocupas') + .22, tag: 'hoja limpia' });
  tl.draw(R, T('✓', 1088, 2990, { h: 150, w: 15 }), at('b', 'ocupas') + .2, { by: atE('b', 'ocupas') + .12, tag: 'bien' });

  // 8 · con la IA es igual: antenitas y la sigla
  tl.draw(K, [W.line(1022, 2007, 996, 1958, { w: 8 }), W.circle(992, 1950, 7, { w: 7 }), W.line(1078, 2007, 1104, 1958, { w: 8 }), W.circle(1108, 1950, 7, { w: 7 })],
    at('b', 'con') + .1, { by: at('b', 'ia') + .05, tag: 'antenas' });
  tl.draw(R, T('IA', 1160, 2086, { h: 74 }), at('b', 'ia'), { by: atE('b', 'ia') + .2, tag: 'IA' });

  // 9 · arriba otra vez: el borrador se lleva la jerga y queda la palabra de siempre
  const tJerga = at('b', 'prompt') + .28;
  tl.erase([[1035, 452], [1500, 452]], tJerga, .5, { width: 132, strength: .9 });
  const resp = fit('= instrucciones', CX, 992, 800, { h: 90, align: 'center' });
  tl.draw(R, resp, at('b', 'las') - .05, { by: atE('b', 'instrucciones') + .05, tag: 'respuesta' });
  const tCirc = atE('b', 'das') + .12;
  tl.draw(R, W.arc(CX, 958, 465, -2.35, -2.35 + Math.PI * 2 + .28, { ry: 104, w: 9 }), tCirc, { by: tCirc + .5, tag: 'círculo 1' });
  tl.draw(R, W.arc(CX + 8, 962, 486, -2.05, -2.05 + Math.PI * 2 + .22, { ry: 120, w: 9 }), tCirc + .54, { by: tCirc + 1.02, tag: 'círculo 2' });
  const tTapa = tCirc + 1.5;
  tl.cue(tTapa, 'tapa');
  tl.cue(tBorra, 'silencio', { dur: 1.2 });
  tl.end();
  // Todo baja 260 px (la cámara nunca se sale por arriba) y, de la flecha para abajo, 150 más (aire bajo la respuesta).
  const DY = 260, DY2 = 150, extra = y => (y >= 1100 ? DY2 : 0);
  const baja = s => { const d = DY + extra(s.box[1] + s.w); for (let i = 1; i < s.pts.length; i += 2) s.pts[i] += d; s.box[1] += d; s.box[3] += d; };
  tl.ev.forEach(e => { if (e.y != null) e.y += DY + extra(e.y); });
  tl.strokes.forEach(baja); tl.erasers.forEach(e => baja(e.path));

  // ───────── cámara: nunca corta. [t, x, y, zoom, giro, curva]
  const X = 1110, cy = (y, z) => y + DY + extra(y) + 150 / z;   // el centro útil del cuadro está 150 px arriba del centro real
  const cam = new W.Camera([
    [0, X, cy(650, .93), .93],
    [tFlecha - .05, X, cy(655, 1), 1, 0, 's'],                 // empuje lento a la palabra
    [atE('a', 'dias') + .5, X, cy(1790, .95), .95, 0, 'io'],   // baja montada en la flecha
    [tVuelve - .12, X, cy(1798, .97), .97, 0, 'l'],            // quieta sobre el globo
    [tVuelve + .72, X, cy(2700, 1), 1, 0, 'io'],               // sigue la segunda flecha hasta la hoja
    [VO.b - .3, X, cy(2704, 1.02), 1.02, 0, 'l'],              // quieta: el borrador
    [VO.b + .5, X, cy(2265, .68), .68, 0, 'io'],               // retrocede: pedido y resultado en un solo cuadro
    [at('b', 'con') - .25, X, cy(2265, .72), .72, 0, 'l'],     // empuje lento mientras se completa
    [at('b', 'ia') - .05, X, cy(2040, 1), 1, 0, 'io'],         // a quien recibe el pedido
    [atE('b', 'igual') + .05, X, cy(2042, 1.04), 1.04, 0, 'l'],
    [at('b', 'prompt') - .1, X, 2030, .55, 0, 'i'],            // la pizarra entera, de paso
    [at('b', 'prompt') + .5, X, cy(770, .88), .88, 0, 'o'],    // y de vuelta a la palabra (abierto: el círculo no entra bajo los botones de TikTok)
    [END, X, cy(772, .9), .9, 0, 'l'],
  ]);

  const board = new W.Board(tl, { W: 2160, H: 4400, ghosts });
  board.objs.push({ draw: (ctx, t, c) => { for (const e of tl.erasers) W.drawEraser(ctx, { ...e, label: ROJO }, t, c); } });
  const q = new URLSearchParams(location.search);
  if (!q.has('nopens')) board.objs.push({ draw: (ctx, t, c) => { for (const p of PENS) W.drawMarker(ctx, p, W.penPose(p, t, cam), c, t); } });

  // ───────── subtítulos: etiqueta color hueso al 74 % de la altura, por encima de la interfaz de TikTok
  const subs = SUBS.map(([id, w0, k0, w1, k1, text]) => ({ t0: at(id, w0, k0) - .05, t1: atE(id, w1, k1) + .4, text }));
  for (let i = 0; i < subs.length - 1; i++) subs[i].t1 = Math.min(Math.max(subs[i].t1, subs[i].t0 + 1.4), subs[i + 1].t0 - .04);
  board.overlays.push({
    draw: (ctx, t) => {
      const s = subs.find(s => t >= s.t0 && t < s.t1); if (!s) return;
      const a = Math.min(1, (t - s.t0) / .12, (s.t1 - t) / .12);
      ctx.font = '46px AD';
      let rows = [s.text];
      if (ctx.measureText(s.text).width > 840) {    // dos renglones parejos
        const ws = s.text.split(' '); let best = 1, bd = 1e9;
        for (let i = 1; i < ws.length; i++) { const d = Math.abs(ctx.measureText(ws.slice(0, i).join(' ')).width - ctx.measureText(ws.slice(i).join(' ')).width); if (d < bd) { bd = d; best = i; } }
        rows = [ws.slice(0, best).join(' '), ws.slice(best).join(' ')];
      }
      const w = Math.max(...rows.map(r => ctx.measureText(r).width)) + 64, h = 74 + (rows.length - 1) * 56, y0 = 1395 - h, cx = 490;
      ctx.globalAlpha = a * .92; ctx.fillStyle = '#fdfcf8'; ctx.shadowColor = 'rgba(30,30,40,.18)'; ctx.shadowBlur = 18; ctx.shadowOffsetY = 4;
      ctx.beginPath(); ctx.roundRect(cx - w / 2, y0, w, h, 14); ctx.fill();
      ctx.shadowColor = 'transparent'; ctx.globalAlpha = a;
      ctx.fillStyle = ROJO; ctx.fillRect(cx - w / 2 + 22, y0 + h - 12, 36, 4);
      ctx.fillStyle = TINTA; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      rows.forEach((r, i) => ctx.fillText(r, cx, y0 + 39 + i * 56));
    }
  });
  if (q.has('nosubs')) board.overlays.length = 0;
  // el sello del reto, arriba a la izquierda dentro de la zona segura: ?dia=1
  if (q.has('dia')) board.overlays.push({ draw: ctx => {
    const txt = `DÍA ${q.get('dia')} DE 30 · VOZ CON IA`;   // la voz es el clon de Kenneth: se dice en pantalla además de la etiqueta de TikTok (CANON)
    ctx.font = '500 30px "JetBrains Mono"'; ctx.letterSpacing = '4px';
    const w = ctx.measureText(txt).width;
    ctx.globalAlpha = .94; ctx.fillStyle = '#fdfcf8'; ctx.beginPath(); ctx.roundRect(72, 236, w + 36, 58, 12); ctx.fill();   // papel detrás, por si pasa un dibujo
    ctx.globalAlpha = .9; ctx.fillStyle = TINTA; ctx.textAlign = 'left'; ctx.textBaseline = 'top'; ctx.fillText(txt, 90, 250);
  } });

  // ───────── cuadro: desenfoque de movimiento cuando la cámara corre
  const off = new OffscreenCanvas(FW, FH), oc = off.getContext('2d');
  function render(ctx, t) {
    const dt = 1 / 24, a = cam.at(t), b = cam.at(Math.max(0, t - dt));
    const sp = Math.hypot((a.x - b.x) * a.z, (a.y - b.y) * a.z) + Math.abs(Math.log(a.z / b.z)) * 900;
    const N = sp > 14 ? Math.min(12, Math.ceil(sp * .5 / 4)) : 1;       // obturador de 180°, 4 px o menos entre subcuadros
    if (N === 1) { board.render(ctx, t, cam); return; }
    const ov = board.overlays; board.overlays = [];
    for (let i = 0; i < N; i++) {
      board.render(oc, t - dt * .5 * i / (N - 1), cam);
      ctx.globalAlpha = 1 / (i + 1); ctx.drawImage(off, 0, 0);
    }
    ctx.globalAlpha = 1; board.overlays = ov;
    for (const o of ov) { ctx.save(); o.draw(ctx, t); ctx.restore(); }
  }

  const ev = [...tl.ev.filter(e => e.t >= 0), ...Object.entries(VO).map(([id, t]) => ({ t, type: 'vo', id }))].sort((a, b) => a.t - b.t);
  for (const e of ev) if (e.x != null) { const c = cam.at(e.t), [px, py] = W.toScreen(c, e.x, e.y); e.pan = +clamp((px - FW / 2) / 800, -.7, .7).toFixed(2); e.z = +c.z.toFixed(2); e.on = px > -80 && px < FW + 80 && py > -80 && py < FH + 80 ? 1 : 0; }
  const tiempos = { tFlecha, tVuelve, tBorra, tLimpia, tJerga, tCirc, tTapa, preguntas: [atE('b', 'es'), atE('b', 'decir'), atE('b', 'cuando')], bien: atE('b', 'ocupas'), ia: at('b', 'ia'), respuesta: atE('b', 'instrucciones') };
  return { dur: END, render, ev, subs, cues: { BPM, BEAT, VO, ...tiempos } };
}
