---
id: 003
formato: la-oficina
titulo: Le prohibí trabajar a mi mejor empleado
idea: O2
estado: guion
uso_ia: voz-personaje
duracion_objetivo_s: 44
fecha_publicacion:
url:
---

# 003 · Le prohibí trabajar a mi mejor empleado

## Gancho (0–3 s)
**Dice:** «A mi mejor empleado le prohibí trabajar.»
**Texto en pantalla:** `Le prohibí trabajar a mi mejor empleado`

## Desarrollo
1. `[CALMA]` «En mi oficina los empleados son inteligencias artificiales. Una es la más capaz. Y la más cara.»
2. `[CALMA]` «Al principio le pedía todo a ella, y sus horas se iban en lo que cualquiera podía hacer.»
3. **Pieza IA:** la voz de Claude: *«Yo no escribo. Yo decido y reviso.»* · Kenneth asiente.
4. `[ACELERA]` «Ahora la regla es esta: la más capaz no teclea. Piensa qué hay que hacer, se lo pasa a otra, y revisa lo que vuelve.»

## Giro / lección
5. `[CALMA]` «En Amazon formé supervisores. Al que ascendés le pasa igual: si sigue haciendo el trabajo, nadie lo revisa a él.»
6. «Tu mejor persona no es la que más hace. Es la que decide y revisa.»

## Cierre
7. «¿En tu negocio quién hace todo? ¿Sos vos?»
**Texto en pantalla:** `El mejor no hace todo: decide y revisa.`

> **Kenneth:** la toma 5 tiene que ser tuya. Si no lo viviste así formando supervisores, cambiala por lo que sí viviste.

## Pantalla y B-roll
- Tomas 1–2: la bitácora de TORRE en el monitor, **difuminada**; encima, un contador de horas que baja.
- Toma 4: en el cuaderno, tres cajas: «piensa → pasa → revisa».
- Toma 6: Kenneth suelta el lapicero sobre la mesa.

## Piezas con IA
| Pieza | Herramienta | Texto exacto | ID de voz / avatar (`config/estudio.json`) |
|---|---|---|---|
| Línea de Claude | ElevenLabs (voz diseñada: calmada, grave, de gerente) | «Yo no escribo. Yo decido y reviso.» | `elevenlabs.elenco.claude` |

## Caption (TikTok)
Borrador: *Le prohibí trabajar a mi mejor empleado. Esta es la regla.* `#liderazgo #inteligenciaartificial #emprendimiento #costarica #delegar`

## Fuente de cada dato
| Dato que se dice | Fuente |
|---|---|
| La más capaz y la más cara | `torre/router/EJECUTORES.md` §2 («la cuota de Claude Code es el recurso más caro y más escaso del sistema») |
| Sus horas se iban en lo que cualquiera podía hacer | ídem («cada token que Claude Code gasta escribiendo código repetitivo es un token que no está disponible para la decisión») |
| La regla: no teclea; piensa, pasa el trabajo y revisa | ídem («Claude Code y Codex no teclean. Piensan, planean y auditan») · `torre/CLAUDE.md` §Política de ejecución |
| Formó supervisores en Amazon | CV: «designed a manager development pipeline that generated 50%+ of internal promotions» |

---

## QA antes de publicar

- [ ] El gancho se entiende **sin sonido**
- [ ] Cero jerga (ni «modelo», ni «tokens», ni «código»)
- [ ] Bitácora difuminada, revisada cuadro por cuadro
- [ ] Todo dato tiene fuente
- [ ] Ninguna venta
- [ ] Etiqueta «contenido generado por IA» activada (por la voz de Claude)
- [ ] Duración ≤ 45 s; si pasa, recortar la toma 2
- [ ] Fila creada en `medicion/registro.csv`
