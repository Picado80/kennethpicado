# Revisión del proceso antes de producir (20-oct-2026)

> Kenneth (20-oct): «Siempre vamos a chequear tres veces y, si es necesario, cuatro, antes de generar nada, y
> preguntarnos y ser críticos: ¿esto se alinea con lo que debemos estar haciendo? ¿Tiene la intención correcta y el
> soporte técnico correcto? […] Hagamos los ajustes necesarios y entonces empezamos a trabajar.»

## La regla: 4 preguntas antes de generar cualquier pieza

Se hacen sobre el guion gráfico, antes de mostrárselo a Kenneth, y otra vez antes de producir. La respuesta queda
escrita en la ficha de la pieza; no alcanza con decir que se revisó.

1. **¿Está alineada?** ¿Sirve a la meta de la fase (seguidores nuevos) y respeta `ESTRATEGIA.md` y `CANON.md`?
2. **¿Tiene la intención correcta?** ¿Qué paso de la cadena mueve (ver, reaccionar, pasarlo, conocerte, seguir) y por
   qué alguien haría eso con esta pieza?
3. **¿Funciona técnicamente?** Formato 1080×1920, nada importante en las zonas que tapa la red, texto legible en el
   celular, audio limpio, datos con fuente, etiqueta de IA si usa la voz o el gemelo.
4. **¿Tiene sentido?** ¿Por qué sí o por qué no, mirando el conjunto? Si una respuesta es «no», se ajusta antes de
   trabajar.

## Lo que encontré en nuestro propio plan (primera pasada)

| # | Problema | Pregunta que falla | Ajuste propuesto |
|---|---|---|---|
| 1 | **El gemelo choca con `CANON.md`.** La estrategia dice que «qué es real» sigue en el CANON, y el CANON dice: gemelo solo en *¿Cuál soy yo?*, nunca antes del video 15, porque «*¿Cuál soy yo?* solo funciona cuando el público ya conoce al Kenneth real». El plan pone el `G0` el Día 1 y el gemelo en las insignias de los días 3 y 5. La auditoría del 19-oct marcó el CANON como «alineado» sin ver esto | 1 y 4 | **Resuelto (Kenneth, 20-oct):** el gemelo va desde el Día 1, porque el proceso existe para que Kenneth no tenga que grabar. Se cambió el `G0`, no el plan: ya no es el juego de adivinar cuál es el real (eso pide grabarlo a él), sino el gemelo diciendo que es su IA. El CANON quedó al día |
| 2 | **Una sola idea repetida.** 6 de las 24 piezas de la semana 1 dicen lo mismo («tu negocio no sobrevive a tus vacaciones» y «un sistema que te necesita es una dependencia»): `P1`, `002`, `002b`, `002c`, `002d` y `R2` | 2 y 4 | Dejar el `002` y una sola variante por semana; las otras dos, en las semanas 2 y 3. Cambiar `R2` por otra regla |
| 3 | **Las zonas que tapa TikTok.** Ni los bocetos ni los efectos respetan la columna de botones de la derecha ni el texto de abajo. Ejemplo: el sello «Día N de 30» va abajo a la derecha, justo donde están los botones | 3 | Agregar las zonas seguras a `efectos.js` y a `lote.py` (como la fila 202 del índice de TORRE) y mover el sello arriba |
| 4 | **«7 IAs» en la bio y en el reto.** El CANON pide contar los carriles vivos de TORRE antes de decir «siete» | 1 y 3 | Contarlos con `verificar.ps1` antes del Día 1 |
| 5 | **La vara de las insignias no se puede alcanzar** (70 / 60 con el Virality Predictor: 5 versiones del 002 entre 50 y 56) | 3 y 4 | Ganarle a la mejor versión anterior; que decida la retención real (`ganchos/002.md`) |
| 6 | **El Día 1 es mañana y nada está aprobado.** Publicar 3 piezas por día a mano desde mañana, sin lote aprobado, es correr | 4 | Correr el Día 1 al día en que esté aprobado el lote y hayan pasado las 4 preguntas |

## Lo que aprendieron las sesiones de Mercadeo (20-oct)

Fuentes: las sesiones «Sistema de generación de videos» (micro-kdrama) y «Videos de Marca Diay», del 20-oct, y la
carpeta `Mercadeo` de la PC. No son de esta marca, pero el proceso es el mismo.

**Lo que se suma a nuestro proceso:**

| Aprendizaje | Cómo entra acá |
|---|---|
| **El editor:** un Artifact con línea de tiempo de varias pistas (video, voz, efectos, subtítulos) y vista previa 9:16. Kenneth recorta y mueve, toca «Copiar edición», lo pega en el chat y Claude vuelve a renderizar. Recién publicado, todavía sin uso real | Cuando funcione allá, se copia para la marca: Kenneth hace los cortes finos de cada pieza antes de publicar |
| **4 preguntas antes de publicar** en Diay: ¿frena el scroll?, ¿conserva el espíritu?, ¿vende?, ¿está bien hecho? | «¿Frena el scroll?» entra en la pregunta 2. «¿Vende?» no aplica en la fase 1: acá es «¿hace seguir?» |
| **Premisas fijas por pieza:** qué no cambia entre tomas (el mismo lugar, el mismo objeto, el mismo lado) | Cada ficha del guion gráfico lleva sus premisas fijas |
| **Lógica física:** imágenes generadas con celulares fantasma, objetos duplicados o escalas imposibles. «Esta imagen está pésima, no tiene lógica física» | Antes de aprobar una imagen generada: revisar manos, objetos, escala y texto. Mejor planos medios o cerrados que abiertos |
| **Lo caro, al final:** generar barato (480p, mudo, sin texto) y poner texto, audio y efectos en edición | Ya es nuestro camino: el volumen va con código y $0. Lo que pase por Higgsfield, igual |
| **«Los créditos de Higgsfield son oro»:** Higgsfield solo para video, consultar el costo antes y pedir el sí | El Virality Predictor no gastó créditos (verificado en el historial del 20-oct). Nada más se genera ahí sin el sí de Kenneth |
| **Subtítulos:** una sola línea, de unos 27 caracteres como máximo, que avanzan con la voz | Regla de la marca desde ya. Nuestros tiempos por palabra ayudan |
| **Voz cortada:** se arregla con estabilidad de 0,30 a 0,40, velocidad 0,95 y un silencio al final | Se prueba en la próxima voz que generemos |
| **Los pósters y carruseles estáticos hechos con IA son los que menos alcance tuvieron** en Diay | La semana 1 tiene 7 imágenes de 21 piezas. Se mantienen como prueba (la estrategia quiere medir qué tipo de pieza convierte), con un ojo puesto: si se confirma, pasan a ser loops de 5 s |
| **Gancho:** curiosidad en el segundo 1 y movimiento real | Coincide con lo que vimos en la prueba del 002 |

## Lo que ya ajusté (no depende de Kenneth)

- **Zonas que tapa la red** en `efectos/efectos.js` (constante `SEGURA`) y en los bocetos de `scripts/lote.py`: el sello
  «Día N de 30» pasa arriba a la izquierda, fuera de los botones.
- **La regla de las 4 preguntas** queda en este archivo y en la memoria de Claude.

## Lo que decide Kenneth (de a uno)

1. ~~El gemelo y el CANON~~ (resuelto el 20-oct).
2. Repartir la idea de las vacaciones en 3 semanas (problema 2).
3. La vara de las insignias (problema 5).
4. El nuevo Día 1, cuando el lote esté aprobado (problema 6).

## Las 3 reglas de Kenneth para lo que se paga (20-oct)

1. **No se gasta dinero en Higgsfield hasta que todo esté 100 % medido y acomodado**, revisado 3 o 4 veces, para no
   repetir nada por un mal prompt. (El Virality Predictor no cobra: verificado en el historial del 20-oct.)
2. **Los detalles se afinan antes con Gemini, ChatGPT o MiniMax** (imágenes y video de prueba). Higgsfield (Seedance)
   queda para la toma final. Hoy en la PC: llave de OpenAI (cobra por uso), MiniMax con el Token Plan (la generación de
   imagen y video está sin verificar en TORRE; nunca el pago por uso) y Gemini sin llave: Gemini y Google Flow van a mano.
3. **Siempre se puede usar B-roll** (de banco o del celular) para generar menos video y bajar el costo.
