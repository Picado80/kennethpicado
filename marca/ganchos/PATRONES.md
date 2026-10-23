# La máquina de ganchos · patrones (20-oct-2026)

> Kenneth (20-oct), sobre el video de @kallaway.marketing: «dale con lo que hay que hacer para aplicar lo del video».
> La máquina estudia los videos que mejor funcionan, saca sus primeros segundos y escribe variaciones propias.

**Cómo se corre:** `python marca/scripts/ganchos.py --cuentas <cuentas> --top 10 --audio 25`. Trae los videos más
vistos de cada cuenta con yt-dlp y transcribe sus primeros 7 segundos (ElevenLabs, unos segundos por video). El banco
crudo queda en `marca/salidas/ganchos-AAAA-MM-DD.*`, fuera del repo, porque son textos de otros. Acá van solo los
patrones, escritos con palabras propias.

**Banco del 20-oct:** 40 videos de 4 cuentas de IA (3 en español, 1 en inglés), 25 con el inicio transcrito.
La medida que más pesa es **compartidos por cada 1.000 vistas** (el paso «pasarlo» de la estrategia).

## Lo que funciona (de más a menos compartido)

| Patrón | Qué hace | Compartidos por mil en el banco | Cómo suena en la marca |
|---|---|---|---|
| **Tu situación** | Arranca con algo que el que mira tiene o vive hoy | el más alto (~34) | «Si mañana te enfermás, ¿tu negocio abre?» |
| **De mucho a poco** | Una promesa medible: de una hora a un minuto, tres cosas | ~34 | «Tres cosas para que tu negocio sobreviva a tus vacaciones» |
| **Lo que casi nadie sabe** | Un secreto o una regla de adentro | ~28 | «En Amazon había una regla que casi ningún dueño conoce» |
| **El aviso** | «Cuidado» o «ojalá lo hubiera sabido antes»: miedo a perder | ~28 | «Si tu negocio depende de vos, esto te va a doler» |
| **La escena** | Arranca en medio de un diálogo, sin presentación | ~12 a ~30 | «—¿Mañana abrimos? —Si yo no vengo, no.» |
| **El antes y después** | Cómo era hace años contra cómo es hoy | ~4 | Funciona para noticias de IA, no para reglas |
| **«Hoy vamos a…»** | Presentar el tema | 4 a 7 (el más bajo) | **No usar** |

## Las reglas que salen de ahí

1. **El que mira es el protagonista desde la primera palabra:** «tu negocio», «si mañana», no «yo trabajé…».
2. **La credencial va segunda.** «14 años en Amazon» sostiene, pero no engancha: en la prueba del 002 la credencial
   al principio sacó 31 de gancho, y la frase fuerte, 41.
3. **Una sola idea en 3 segundos,** con letra grande en pantalla (en las 3 pruebas del 002, el pico fue siempre la frase
   en tipografía grande).
4. **Nunca abrir presentando el tema** («hoy vamos a hablar de…»).
5. **Un número concreto** cuando lo hay, y verdadero (CANON: sin datos inventados).
