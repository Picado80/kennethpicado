# Formato dividido: Kenneth abajo, animación arriba

> Tomado del video de @itsolelehmann que Kenneth pasó el 8-oct-2026 (65 s, «Claude Opus 5.5 hace
> animaciones»). Primera versión propia: video 002 v3 (`produccion/002/`).

## Cómo está armado el video de referencia (cuadro por cuadro)

| Tramo | Qué se ve | Para qué |
|---|---|---|
| 0–5 s | **Dividido**: arriba, ejemplos de animación que cambian cada segundo; abajo, él hablando. Título fijo en la línea del medio | El gancho: muestra el resultado antes de explicar |
| 5–9 s | **Cara completa**, con dibujos que aparecen al lado de la cabeza y palabras tachadas («extra tools», «MCP») | Cuando dice algo personal o niega algo |
| 9–15 s | **Dividido**: arriba, «ejemplo real» | Prueba |
| 15–26 s | **Animación a pantalla completa**; él, recortado y chiquito en una esquina | La historia («la fábrica de atardeceres») |
| 27–33 s | **Dividido**: arriba, la pantalla de Claude o una lista que se arma (1, 2, 3, 4) | Los pasos |
| 34–47 s | **Pantalla completa** con la instrucción resaltada parte por parte; él, recortado abajo | La demostración |
| 48–60 s | Cara completa, dividido otra vez con dos ejemplos, y cara completa para cerrar | El cierre y la llamada a la acción |

**Reglas que se repiten:**
- Los subtítulos van **en la línea del medio**: chicos, blancos, con fondo negro, de a 2 o 3 palabras.
- Arriba cambia algo **cada 1 a 3 segundos**. Abajo, él no cambia.
- La cara completa se usa poco: para el gancho personal, para negar algo y para cerrar.
- Todo lo de arriba es animación hecha con código o capturas, no tomas de banco.

## Lo que cambia para Kenneth: su cara cuesta por segundo

Él sale gratis porque es él grabado. El gemelo de Kenneth cuesta **$0.0805 por segundo** por la API
(Avatar IV). Por eso, cuando la voz sigue pero la idea se puede contar con una animación, va
**animación a pantalla completa** y el gemelo no se paga.

| Video | Cara en pantalla | Costo |
|---|---|---|
| 002 v3 (50 s) | 24,2 s | **$1.94** (las animaciones cuestan $0) |
| 90 s con la API, a $1.50 | 18,6 s como máximo (20 %) | $1.50 |
| 90 s con HeyGen Creator en la web ($29/mes, 20 videos/mes) | unos 58 s (65 %) | **$1.45** |

**Conclusión:** el formato de la referencia con videos de 1 minuto y medio a $1.50 solo cierra con el
plan web de HeyGen. Por la API, a $1.50 la cara sale como mucho el 20 % del video.

## Cómo se arma (lo que ya existe)

- Las escenas son SVG + GSAP dentro de HyperFrames (`produccion/002/split.html`, `escenas.html` y sus `.js`).
- El gemelo va recortado en la mitad de abajo: el mismo video de 1080×1920, corrido 160 px hacia arriba.
- Línea amarilla de 12 px en el medio. Subtítulos con los tiempos de cada palabra de ElevenLabs.
