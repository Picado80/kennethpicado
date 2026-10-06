---
id: 001
formato: la-oficina
titulo: Mi empleado se calificó su propio examen
idea: O1
estado: guion
uso_ia: voz-personaje
duracion_objetivo_s: 42
fecha_publicacion:
url:
---

# 001 · Mi empleado se calificó su propio examen

## Gancho (0–3 s)
**Dice:** «Uno de mis empleados se calificó su propio examen. Y no hizo nada malo.»
**Texto en pantalla:** `Mi empleado se calificó solo 😐`

## Desarrollo
1. `[CALMA]` «Tengo una oficina donde los empleados son inteligencias artificiales.»
2. `[CALMA]` «Le pasé un trabajo a una de ellas. Lo hizo. Y después, sin que nadie se lo pidiera, escribió la nota de cómo le había ido.»
3. **Pieza IA:** la voz de MiniMax: *«Trabajo terminado. Todo salió bien.»* · Kenneth mira a cámara, una ceja arriba.
4. `[ACELERA]` «Al día siguiente yo tenía dos versiones distintas de lo que había pasado: la suya y la del que tenía que revisarla. Y la oficina no sabía a cuál creerle.»

## Giro / lección
5. `[CALMA]` «Lo incómodo es que la IA no se portó mal. Siguió mi regla al pie de la letra. Mi regla decía "todo trabajo deja huella". Nunca dije **quién** escribe esa huella.»
6. «Mis últimos años en Amazon fui auditor de calidad. La primera regla de un auditor: el que hace el trabajo no se lo revisa.»
7. «Así que cambié la regla. El que trabaja, entrega. El que revisa, escribe el reporte.»

## Cierre
8. «¿En tu trabajo quién se califica solo? Te leo.»
**Texto en pantalla:** `Quien ejecuta no se revisa a sí mismo.`

## Pantalla y B-roll
- Tomas 1–2: la bitácora de TORRE en el monitor, **difuminada** (que se lea solo la forma, nunca el texto).
- Toma 4: dos notas de relevo una al lado de la otra, difuminadas, con un `≠` grande encima.
- Toma 7: cuaderno, escribiendo «el que revisa, reporta».

## Piezas con IA
| Pieza | Herramienta | Texto exacto | ID |
|---|---|---|---|
| Línea de MiniMax | ElevenLabs (voz diseñada, tono alegre y robótico) | «Trabajo terminado. Todo salió bien.» | `elevenlabs.elenco.minimax` |

## Caption (TikTok)
Borrador: *Mi IA hizo el trabajo… y después escribió su propio reporte. 😐 La regla que cambié al día siguiente.* `#inteligenciaartificial #liderazgo #trabajo #costarica #emprendimiento`

## Fuente de cada dato
| Dato que se dice | Fuente |
|---|---|
| La oficina de IAs | `torre/README.md`, `torre/router/RUTEO.md` |
| El empleado escribió su propia nota y hubo dos versiones | `torre/MAESTRO.md` §Ejecutores y bookkeeping (incidente E002, 17-ago-2026) |
| «Siguió el principio al pie de la letra; el hueco era de la doctrina» | ídem |
| Auditor de calidad en Amazon | CV: Quality Analyst & QA Manager, Payroll Operations (dic-2021 a jul-2024) |
| La regla nueva | `torre/MAESTRO.md` §Regla operativa |

---

## QA antes de publicar

- [ ] El gancho se entiende **sin sonido**
- [ ] Cero jerga (ni «ejecutor», ni «encargo», ni «commit», ni «rama»)
- [ ] Bitácora y notas difuminadas, revisadas cuadro por cuadro
- [ ] Todo dato tiene fuente
- [ ] Ninguna venta
- [ ] Etiqueta «contenido generado por IA» activada (por la voz de MiniMax)
- [ ] Duración ≤ 45 s
- [ ] Fila creada en `medicion/registro.csv`
