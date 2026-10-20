// Carrete de muestra de la biblioteca: un efecto por escena, con el uso que tiene en la semana 1.
// Es el guion gráfico de los efectos: se aprueba antes de usarlos en piezas reales. Los datos son de ejemplo.
import * as F from './efectos.js';
const { el, C } = F;

const ESCENAS = [
  { nombre: 'Curva de crecimiento', uso: 'El contador del reto, D1 a D30', dur: 4.2,
    hacer: r => F.curva(r, { titulo: 'Seguidores · TikTok + Instagram', valores: [1658, 1671, 1690, 1712, 1730], meta: 2658, ejemplo: true }) },
  { nombre: 'Tipografía de golpe', uso: 'Ganchos: el 002 y las posturas', dur: 3.2,
    hacer: r => F.frase(r, { texto: 'En Amazon nadie era indispensable.', oro: 'indispensable', golpeEn: 1.35 }) },
  { nombre: 'El chat toma la pantalla', uso: 'El agente que contesta; PR1', dur: 5.2,
    hacer: r => F.chat(r, { titulo: 'Gina', estado: 'Agente de IA · en línea', inicio: .4, cada: .85, toma: 4.2, mensajes: [
      { de: 'cliente', texto: '¿Tienen los tenis blancos en talla 38?' },
      { de: 'agente', texto: 'Sí hay en 38. ¿Se los enviamos mañana?' },
      { de: 'cliente', texto: 'Envíenmelos a Escazú.' },
      { de: 'agente', texto: 'Listo. Le dejo el número de SINPE.' }] }) },
  { nombre: 'El teléfono', uso: 'PR1: las respuestas de las 3 IAs', dur: 4.2,
    hacer: r => F.telefono(r, { inicio: .1, llenar: pantalla => {
      const tarjetas = ['IA 1', 'IA 2', 'IA 3'].map((n, i) => {
        const c = el('div', { position: 'absolute', left: '40px', right: '40px', top: `${150 + i * 330}px`, height: '290px', borderRadius: '28px',
          background: i === 1 ? C.tinta : '#F1EFE9', padding: '30px', boxSizing: 'border-box' }, pantalla);
        el('div', { fontSize: '22px', color: i === 1 ? C.oro : C.rojo }, c, `${n} · «Haceme un menú»`).className = 'mono';
        for (let k = 0; k < 4; k++) el('div', { height: '22px', marginTop: '22px', borderRadius: '11px', width: `${92 - k * 14}%`,
          background: i === 1 ? 'rgba(232,230,222,.35)' : 'rgba(22,35,63,.18)' }, c);
        return c;
      });
      return { pintar(t) { tarjetas.forEach((c, i) => { const p = F.tramo(t, i * .35, i * .35 + .4);
        c.style.opacity = p; c.style.transform = `translateY(${(1 - F.E.sale(p)) * 40}px)`; }); } };
    } }) },
  { nombre: 'La lista que aparece', uso: 'L1 y el cierre del 002b, c y d', dur: 4.0,
    hacer: r => F.lista(r, { titulo: 'Tres cosas para mañana', oro: 'mañana', items: ['Escribí las 3 cosas que solo vos sabés', 'Un solo número que mirás todos los días', '15 minutos los lunes con tu gente'] }) },
  { nombre: 'Titulares que llueven', uso: 'Las noticias: RN1 y NS1', dur: 4.6,
    hacer: r => F.titulares(r, { destacado: 2, items: [
      { fuente: 'Fuente', fecha: 'Fecha', texto: '[Titular de ejemplo uno]' },
      { fuente: 'Fuente', fecha: 'Fecha', texto: '[Titular de ejemplo dos]' },
      { fuente: 'Fuente', fecha: 'Fecha', texto: '[La noticia del día, sin jerga]' },
      { fuente: 'Fuente', fecha: 'Fecha', texto: '[Titular de ejemplo cuatro]' }] }) },
  { nombre: 'Recorte de papel', uso: 'G0: el gemelo sale del cuadro', dur: 3.6,
    hacer: r => F.recorte(r, { inicio: .5 }) },
];

export async function armar(escenario) {
  await F.instalar();
  let t0 = 0;
  const armadas = ESCENAS.map((e, i) => {
    const r = el('div', { position: 'absolute', inset: '0', overflow: 'hidden', display: 'none' }, escenario);
    const efecto = e.hacer(r);
    // rótulos del carrete: qué efecto es y dónde se usa, más el sello del reto que llevan todas las piezas
    const rot = el('div', { position: 'absolute', left: '60px', top: '70px', right: '60px', zIndex: 50, fontSize: '24px',
      color: C.oro, lineHeight: '1.6' }, r, `Efecto ${i + 1} de ${ESCENAS.length} · ${e.nombre}<br><span style="color:${C.gris}">Se usa en: ${e.uso}</span>`);
    rot.className = 'mono';
    const sello = el('div', { position: 'absolute', right: '60px', bottom: '70px', zIndex: 50, fontSize: '24px', color: C.oro }, r, 'Día 3 de 30');
    sello.className = 'mono';
    const a = { r, efecto, t0, dur: e.dur };
    t0 += e.dur;
    return a;
  });
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
