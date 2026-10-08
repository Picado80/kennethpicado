---
id: 005
formato: la-oficina
titulo: La oficina me avisó tres veces y el que no hizo nada fui yo
idea: O5
estado: guion
uso_ia: voz-personaje
duracion_objetivo_s: 43
fecha_publicacion:
url:
---

# 005 · La oficina me avisó tres veces y el que no hizo nada fui yo

## Gancho (0–3 s)
**Dice:** «Uno de mis empleados pasó 18 días sin poder entrar a la oficina. Y el culpable fui yo.»
**Texto en pantalla:** `18 días sin poder entrar. El culpable: yo.`

## Desarrollo
1. `[CALMA]` «En mi oficina los empleados son inteligencias artificiales. A una se le venció la tarjeta para entrar.»
2. `[CALMA]` «La oficina me avisó tres veces. Y yo lo dejé para después.»
3. **Pieza IA:** la voz de Kimi: *«Sigo aquí. Entré por la puerta de atrás.»* · Kenneth se ríe.
4. `[ACELERA]` «Lo más gracioso: siguió trabajando. Entraba por la puerta de atrás, y por eso nadie sentía que algo estuviera roto.»

## Giro / lección
5. `[CALMA]` «Lo que aprendí con las escalaciones en Amazon: un aviso sin dueño y sin fecha es decoración.»
6. «Cada aviso necesita un nombre y un día. Aunque el nombre sea el tuyo.»

## Cierre
7. «¿Qué aviso tenés pendiente desde hace semanas?»
**Texto en pantalla:** `Un aviso sin dueño y sin fecha es decoración.`

## Pantalla y B-roll
- Toma 1: una tarjeta de acceso con una X roja (dibujada o un objeto real).
- Toma 2: tres notificaciones que llegan una tras otra y se deslizan sin abrir (maqueta, sin datos reales).
- Toma 4: la bitácora **difuminada**, con trabajo que sigue apareciendo.

## Piezas con IA
| Pieza | Herramienta | Texto exacto | ID de voz / avatar (`config/estudio.json`) |
|---|---|---|---|
| Línea de Kimi | ElevenLabs (voz diseñada: tranquila, un poco despistada) | «Sigo aquí. Entré por la puerta de atrás.» | `elevenlabs.elenco.kimi` |

## Caption (TikTok)
Borrador: *Mi oficina me avisó tres veces. Y el que no hizo nada fui yo.* `#liderazgo #inteligenciaartificial #trabajo #costarica #productividad`

## Fuente de cada dato
| Dato que se dice | Fuente |
|---|---|
| A un empleado de IA se le venció la tarjeta (llave rechazada) | `torre/router/CAPACIDADES.md`, ficha de Kimi: `401` desde el 17-ago-2026 |
| 18 días | ídem, recalibración del 2026-09-04 («día 18 con el mismo `401`») |
| Avisó tres veces y no se hizo nada | ídem: recalibraciones del 17-ago, 21-ago y 4-sep («la rotación que se le pidió a Kenneth no se hizo») |
| Siguió trabajando por la puerta de atrás | ídem, 21-ago («kimi ejecutó 8 eventos esta semana con la llave rechazada»: trabajó por la app) |
| Escalaciones en Amazon | CV: «Escalation & Root-Cause Resolution» |

---

## QA antes de publicar

- [ ] El gancho se entiende **sin sonido**
- [ ] Cero jerga (ni «llave», ni «API», ni «401»: es «la tarjeta para entrar»)
- [ ] Bitácora difuminada; las notificaciones son maqueta, sin datos reales
- [ ] Todo dato tiene fuente
- [ ] Ninguna venta
- [ ] Etiqueta «contenido generado por IA» activada (por la voz de Kimi)
- [ ] Duración ≤ 45 s; si pasa, recortar la toma 4
- [ ] Fila creada en `medicion/registro.csv`
