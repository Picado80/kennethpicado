// Carrete de muestra de la biblioteca: un efecto por escena, con el uso que tiene en las piezas. Todo en claro.
// Es el catálogo que Kenneth mira para elegir; los datos y textos son de ejemplo. Se agrega una escena por cada efecto
// nuevo (ver CATALOGO.md). Fotos: muestras/soda.jpg (MiniMax, la del P1) y muestras/gemelo.jpg (un cuadro del G0).
import * as F from './efectos.js';
const { el, K, E, tramo, mezcla, SEGURA, BOTONES } = F;
const SODA = 'muestras/soda.jpg', GEMELO = 'muestras/gemelo.jpg';
const L = SEGURA.izquierda + 10;
const papel = (r, fondo = K.papel) => el('div', { position: 'absolute', inset: '0', background: fondo, overflow: 'hidden' }, r);
const lineasDe = n => Array.from({ length: n }, (_, i) => `<div style="height:16px;width:${[92, 78, 86, 64, 80][i % 5]}%;border-radius:8px;background:rgba(22,35,63,.13);margin-top:20px"></div>`).join('');

const ESCENAS = [
  { nombre: 'Snap zoom · tipografía de golpe', uso: 'Ganchos: el 002 y las posturas', dur: 3.0,
    hacer: r => F.frase(r, { texto: 'En Amazon nadie era indispensable.', oro: 'indispensable', golpeEn: 1.35 }) },
  { nombre: 'Checklist pop', uso: 'Las 3 cosas para mañana (002b, L1)', dur: 3.6,
    hacer: r => F.lista(r, { titulo: 'Tres cosas para mañana', oro: 'mañana', items: ['Una hoja con lo que solo vos sabés', 'Un número, todos los días', '15 minutos los lunes'] }) },
  { nombre: 'Growth curve', uso: 'El contador del reto', dur: 4.0,
    hacer: r => F.curva(r, { titulo: 'Seguidores · ejemplo', valores: [1659, 1672, 1690, 1715, 1741], meta: 2659, ejemplo: true }) },
  { nombre: 'Chat takeover', uso: 'PR1 y el agente que contesta', dur: 5.0,
    hacer: r => F.chat(r, { titulo: 'Soda La Esquina', estado: 'Agente de IA · en línea', inicio: .4, cada: .8, toma: 4.0, mensajes: [
      { de: 'cliente', texto: '¿Qué casado hay hoy?' },
      { de: 'agente', texto: 'Pollo en salsa, ₡2.800. ¿Se lo apartamos?' },
      { de: 'cliente', texto: 'Sí, dos para la 1:00.' },
      { de: 'agente', texto: 'Listo: dos a nombre de Ana.' }] }) },
  { nombre: 'Phone mock-up', uso: 'PR1: las respuestas de las 3 IAs', dur: 3.8,
    hacer: r => F.telefono(r, { inicio: .1, fondo: `linear-gradient(160deg, ${K.papel}, ${K.celeste})`, llenar: pantalla => {
      const tarjetas = ['MiniMax', 'Kimi', 'DeepSeek'].map((n, i) => {
        const c = el('div', { position: 'absolute', left: '36px', right: '36px', top: `${140 + i * 340}px`, height: '300px', borderRadius: '28px',
          background: i === 1 ? K.tinta : '#F1F4F9', padding: '30px', boxSizing: 'border-box' }, pantalla);
        el('div', { fontSize: '24px', color: i === 1 ? K.resalte : K.oro }, c, n).className = 'mono';
        for (let k = 0; k < 4; k++) el('div', { height: '22px', marginTop: '22px', borderRadius: '11px', width: `${92 - k * 14}%`,
          background: i === 1 ? 'rgba(247,244,236,.35)' : 'rgba(22,35,63,.16)' }, c);
        return c;
      });
      return { pintar(t) { tarjetas.forEach((c, i) => { const p = F.tramo(t, i * .35, i * .35 + .4);
        c.style.opacity = p; c.style.transform = `translateX(${((1 - F.E.sale(p)) * (i % 2 ? 80 : -80)).toFixed(1)}px)`; }); } };
    } }) },
  { nombre: 'Headline storm', uso: 'Las noticias: RN y NS', dur: 4.2,
    hacer: r => F.titulares(r, { destacado: 2, items: [
      { fuente: 'Ejemplo', fecha: '21 oct', texto: 'Un titular de ejemplo, el primero' },
      { fuente: 'Ejemplo', fecha: '21 oct', texto: 'Otro titular que cae girando' },
      { fuente: 'Ejemplo', fecha: '21 oct', texto: 'La noticia del día, sin jerga' },
      { fuente: 'Ejemplo', fecha: '21 oct', texto: 'Un cuarto titular de relleno' }] }) },
  { nombre: 'Orbit', uso: 'D2: la oficina alrededor tuyo', dur: 3.8,
    hacer: r => F.orbita(r, { centro: 'Kenneth', items: ['Claude', 'Codex', 'MiniMax', 'Kimi', 'DeepSeek', 'Grok', 'Antigravity'] }) },
  { nombre: 'Frame escape', uso: 'Posturas: P2, P3', dur: 3.4,
    hacer: r => F.escapeMarco(r, { src: SODA, palabra: 'SIN VOS', t0: 1.0 }) },
  { nombre: 'Zoom portal', uso: 'Pasar de una idea a la siguiente', dur: 3.4,
    hacer: r => {
      const a = papel(r);
      const pal = el('div', { position: 'absolute', left: '0', right: '0', top: '690px', textAlign: 'center', font: '900 150px/1 Archivo',
        letterSpacing: '-.04em', color: K.tinta }, a, `NEG<span style="color:${K.oro}">O</span>CIO`);
      el('div', { position: 'absolute', left: '0', right: '0', top: '880px', textAlign: 'center', fontSize: '28px', color: K.tinta2 }, a,
        'Entrá por la O').className = 'mono';
      const b = el('div', { position: 'absolute', inset: '0' }, r);
      const br = F.broll(b, { src: SODA, claves: [{ t: 0, z: 1.1 }, { t: 4, z: 1.0, curva: 'l' }] });
      const o = pal.querySelector('span'); let c = null;
      return { pintar(t) {
        if (!c) { const q = o.getBoundingClientRect(); c = { x: q.left + q.width / 2, y: q.top + q.height * .52, r: q.width * .2 }; }
        br.pintar(t); F.portal(a, b, t, 1.3, { ...c, dur: 1.0 });
      } };
    } },
  { nombre: 'Studio reveal', uso: 'PR3: el manual de apertura', dur: 3.8, hacer: r => F.estudio(r, {}) },
  { nombre: 'B-roll overlay', uso: '002b: la cafetería a las 6:40', dur: 3.4,
    hacer: r => {
      const a = papel(r);
      const tx = el('div', { position: 'absolute', left: `${L}px`, right: `${SEGURA.derecha}px`, top: '420px', font: '400 100px/1 "Instrument Serif"', color: K.tinta }, a,
        F.conOro('Son las 6:40.', '6:40', K.oro));
      const br = F.broll(a, { src: SODA, marco: { left: 180, top: 640, width: 590, height: 560 }, entra: .7,
        claves: [{ t: 0, z: 1.05, x: -20 }, { t: 3.4, z: 1.18, x: 20, curva: 'l' }] });
      return { pintar(t) { tx.style.opacity = tramo(t, 0, .4); br.pintar(t); } };
    } },
  { nombre: 'Dolly zoom', uso: 'El momento de tensión (002)', dur: 3.6,
    hacer: r => F.dolly(r, { src: SODA, texto: '¿Y si mañana no llegás?', oro: 'no llegás' }) },
  { nombre: 'Magazine cover', uso: 'Insignias: tu gemelo en portada', dur: 3.8,
    hacer: r => F.revista(r, { src: GEMELO, cabecera: 'NEGOCIOS', lineas: [{ n: '7', txt: 'IAs en una oficina' }, { n: '30', txt: 'días de reto' },
      { n: '+1.000', txt: 'seguidores' }] }) },
  { nombre: 'Liquid glass zoom-through', uso: 'Corte elegante entre escenas', dur: 3.4,
    hacer: r => {
      const a = papel(r, `linear-gradient(160deg, ${K.papel}, ${K.celeste})`);
      el('div', { position: 'absolute', left: `${L}px`, right: `${SEGURA.derecha}px`, top: '560px', font: '400 104px/1.02 "Instrument Serif"', color: K.tinta }, a,
        F.conOro('Lo que pasa adentro de tu negocio.', 'adentro', K.oro));
      const b = el('div', { position: 'absolute', inset: '0', visibility: 'hidden' }, r);
      const br = F.broll(b, { src: SODA, claves: [{ t: 0, z: 1.12 }, { t: 3.4, z: 1.02, curva: 'l' }] });
      const v = F.vidrio(r, { a, b, t0: 1.5, dur: 1.0 });
      return { pintar(t) { br.pintar(t); v.pintar(t); } };
    } },
  { nombre: 'Green screen frame break', uso: 'G0 y los videos del gemelo', dur: 3.4,
    hacer: r => F.rompeMarco(r, { src: GEMELO, t0: 1.3 }) },
  { nombre: 'Digital zoom', uso: 'Mostrar un detalle (PR2: el inventario)', dur: 3.4,
    hacer: r => F.zoomDigital(r, { src: SODA, foco: { x: 470, y: 1010 }, en: [.9, 1.9] }) },
  { nombre: 'Paper cutout', uso: 'El gemelo sale del cuadro', dur: 3.2, hacer: r => F.recorte(r, { inicio: .5, foto: GEMELO }) },
  { nombre: 'Marker notes', uso: 'Señalar lo importante en cualquier pieza', dur: 3.4,
    hacer: r => {
      const a = papel(r);
      const tx = el('div', { position: 'absolute', left: `${L}px`, right: `${SEGURA.derecha + 30}px`, top: '540px', font: '400 92px/1.08 "Instrument Serif"', color: K.tinta }, a,
        'Si tu negocio no sobrevive a tus <span>vacaciones</span>, no es un negocio.');
      const q = tx.querySelector('span').getBoundingClientRect();
      const m = F.marcador(a, { trazos: [
        { tipo: 'circulo', x: q.left - 26, y: q.top - 8, w: q.width + 52, h: q.height + 14, t0: .5 },
        { tipo: 'flecha', x: 330, y: 1150, w: 120, h: -100, t0: 1.3 }],
        notas: [{ texto: '¡esto!', x: 470, y: 1110, t0: 1.6, rot: -6 }] });
      return { pintar(t) { tx.style.opacity = tramo(t, 0, .3); m.pintar(t); } };
    } },
  { nombre: 'Vox · el documento resaltado', uso: 'Noticias y datos con su fuente', dur: 4.2,
    hacer: r => F.documento(r, { fuente: 'Ejemplo · documento', titulo: 'Nadie era indispensable', marcada: 3, t0: 1.3, lineas: [
      'En una operación que no se apaga,', 'cada puesto tiene a alguien', 'que lo cubre cuando falta.', 'El estándar está escrito,', 'no en la cabeza de nadie.'] }) },
  { nombre: 'Vox · collage', uso: 'Historias: Amazon en la soda', dur: 3.8,
    hacer: r => F.collage(r, {
      bloques: [{ x: 120, y: 380, w: 380, h: 220, rot: -8, t0: 0 }, { x: 560, y: 980, w: 300, h: 220, color: K.cielo, rot: 6, t0: .35 }],
      fotos: [{ src: SODA, x: 150, y: 420, w: 520, h: 600, rot: -4, t0: .15 }, { src: GEMELO, x: 470, y: 600, w: 400, h: 460, rot: 5, t0: .6, tinte: 'rgba(245,207,78,.55)' }],
      titulo: { texto: 'Amazon en la soda', x: 150, y: 1050, t0: 1.1 } }) },
  { nombre: 'Stamp on · el sello', uso: '«Yo solo apruebo»', dur: 3.0,
    hacer: r => {
      const a = papel(r, `linear-gradient(170deg, ${K.papel}, ${K.crema})`);
      const hoja = el('div', { position: 'absolute', left: '190px', top: '470px', width: '600px', height: '700px', boxSizing: 'border-box', padding: '50px 46px',
        background: K.blanco, borderRadius: '16px', boxShadow: `0 30px 60px ${K.sombra}`, transform: 'rotate(-2deg)' }, a,
        `<div style="font:400 58px/1.05 'Instrument Serif';color:${K.tinta}">Menú de la semana</div><div class="mono" style="font-size:20px;color:${K.oro};margin:14px 0 10px">Lo propuso la oficina</div>` + lineasDe(9));
      const s = F.sello(a, { texto: 'Aprobado', x: 260, y: 820, t0: 1.0, sacude: hoja });
      return { pintar(t) { hoja.style.opacity = tramo(t, 0, .3); s.pintar(t); } };
    } },
  { nombre: 'Typewriter', uso: 'El pedido que se le escribe a la IA', dur: 3.6,
    hacer: r => {
      const a = papel(r, `linear-gradient(160deg, ${K.papel}, ${K.celeste})`);
      el('div', { position: 'absolute', left: `${L}px`, top: '600px', fontSize: '26px', color: K.tinta2 }, a, 'Le escribís a la IA:').className = 'mono';
      const caja = el('div', { position: 'absolute', left: `${L}px`, top: '660px', width: '650px', minHeight: '400px', boxSizing: 'border-box', padding: '34px 36px',
        background: K.blanco, borderRadius: '28px', boxShadow: `0 24px 50px ${K.sombra}`, border: `2px solid ${K.cielo}` }, a);
      const m = F.maquina(caja, { texto: 'Tengo una soda en San José. Haceme el menú de la semana: 5 casados, a no más de ₡3.500.', x: 0, y: 0, ancho: 578, t0: .3, cps: 30,
        estilo: { position: 'relative', font: '500 38px/1.45 "JetBrains Mono"' } });
      return { pintar(t) { m.pintar(t); } };
    } },
  { nombre: 'Cámara: acercar, alejar y ángulo', uso: 'Todas las piezas', dur: 3.6,
    hacer: r => {
      const a = papel(r);
      const capa = el('div', { position: 'absolute', inset: '0' }, a);
      el('div', { position: 'absolute', left: `${L}px`, top: '420px', font: '900 200px/1 Archivo', letterSpacing: '-.045em', color: K.tinta }, capa, '7 IAs');
      el('div', { position: 'absolute', left: `${L}px`, right: `${BOTONES.derecha}px`, top: '660px', font: '400 70px/1.05 "Instrument Serif"', color: K.tinta }, capa,
        F.conOro('y una sola persona que aprueba.', 'aprueba', K.oro));
      F.fichas(capa, { items: ['Claude', 'Codex', 'MiniMax', 'Kimi', 'DeepSeek', 'Grok', 'Antigravity'], estilo: { position: 'absolute', left: `${L}px`, right: `${BOTONES.derecha}px`, top: '880px' } }).pintar(9);
      const cam = F.camara(capa, [{ t: 0, z: 1.3, x: 120, y: 330, ladea: 16, inclina: 5 }, { t: 1.2, z: 1.3, x: 110, y: 320, ladea: 10, curva: 'l' },
        { t: 1.9, z: 1, curva: 'e' }, { t: 2.8, z: 1.02, ladea: -4, curva: 'l' }, { t: 3.6, z: 1.02, ladea: 4, curva: 'io' }], { deriva: 3 });
      return { pintar(t) { cam.pintar(t); } };
    } },
  { nombre: 'Cortes: zoom, barrido y giro', uso: 'Entre escenas', dur: 4.2,
    hacer: r => {
      const panel = (txt, fondo) => { const p = papel(r, fondo); el('div', { position: 'absolute', left: '0', right: '0', top: '700px', textAlign: 'center',
        font: '400 150px/1 "Instrument Serif"', color: K.tinta }, p, txt); return p; };
      const [A, B, Cc, D] = [panel('Zoom', K.papel), panel('Barrido', K.celeste), panel('Giro', K.crema), panel('Listo.', K.papel)];
      return { pintar(t) {
        for (const p of [A, B, Cc, D]) { p.style.visibility = 'hidden'; }
        if (t < 1.5) F.corte(A, B, t, 1.0, { tipo: 'zoom' });
        else if (t < 2.5) F.corte(B, Cc, t, 2.0, { tipo: 'barrido' });
        else F.corte(Cc, D, t, 3.0, { tipo: 'gira' });
      } };
    } },
];

export async function armar(escenario) {
  await F.instalar({ fondo: K.papel });
  let t0 = 0;
  const armadas = ESCENAS.map((e, i) => {
    const r = el('div', { position: 'absolute', inset: '0', overflow: 'hidden' }, escenario);   // visible mientras se arma (algunas miden)
    const efecto = e.hacer(r);
    const rot = el('div', { position: 'absolute', left: '40px', top: '60px', right: '40px', zIndex: 100, fontSize: '23px', color: K.tinta, lineHeight: '1.55',
      background: 'rgba(255,255,255,.9)', padding: '12px 18px', borderRadius: '14px', boxShadow: `0 8px 20px ${K.sombra}` }, r,
      `Efecto ${i + 1} de ${ESCENAS.length} · ${e.nombre}<br><span style="color:${K.tinta2}">Se usa en: ${e.uso}</span>`);
    rot.className = 'mono';
    r.style.display = 'none';
    const a = { r, efecto, t0, dur: e.dur };
    t0 += e.dur;
    return a;
  });
  await Promise.all([...escenario.querySelectorAll('img')].map(i => i.decode().catch(() => {})));
  await Promise.all(armadas.map(a => a.efecto.listo).filter(Boolean));
  return {
    dur: t0,
    pintar(t) {
      for (const a of armadas) {
        const activa = t >= a.t0 && t < a.t0 + a.dur;
        a.r.style.display = activa ? 'block' : 'none';
        if (activa) a.efecto.pintar(t - a.t0);
      }
    },
  };
}
