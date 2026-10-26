# El equipo de agentes de la marca

Kenneth, 23-oct-2026: «tenemos que tener diferentes agentes haciendo diferentes cosas… darles acciones y funciones
específicas que nos ayuden a acelerar el proceso, pero también a asegurarnos de que no pasen estas cosas de que sale un
video y no está correctamente hecho».

Cada agente tiene sus instrucciones en `.claude/agents/<nombre>.md`.

| Agente | Qué hace | Cuándo | Qué deja |
|---|---|---|---|
| **tendencias** | Busca lo que funciona hoy (en español, en inglés y en Costa Rica) y analiza las cuentas que manda Kenneth | Cada mañana y con cada referencia | `radar/hoy.md`, `radar/referencias/<cuenta>.md` |
| **scouting** | Busca técnicas de motion graphics, formatos, ganchos y estrategias nuevas en varias redes y plataformas, y propone qué probar (Kenneth, 25-oct: «No quiero que mis videos todos se vean iguales») | Cada domingo a las 5 p. m. (tarea `scouting-semanal-marca`) | `radar/scouting/AAAA-SNN.md`, `radar/scouting/BANCO.md` y las técnicas a graficos y a «Sistema de generacion de videos» |
| **resultados** | Lee los números (Buffer, perfiles y tablero) y dice qué funcionó y dónde se cae la gente | Cada mañana; el lunes, la revisión | `medicion/lectura-<fecha>.md`, `semanas/…-revision.md` |
| **estrategia** | Decide los temas, los ganchos y la forma del gemelo; mata, cambia o duplica series | Cada tarde y el plan de la semana | `semanas/…-plan.md` |
| **guionista** | Escribe y revisa cada guion para frenar el scroll: 5 ganchos calificados, un hilo que amarra el principio con el final, 12 a 20 s y cierre para que lo pasen; aprende de los números | Cada guion nuevo y cada lunes | `guiones/…`, `ganchos/aprendido.md` |
| **generador-videos** | Produce la pieza: guion, voz, gemelo, B-roll, composición y mezcla | Con el sí del guion gráfico | `salidas/diaN/…mp4` |
| **graficos** | Diseña efectos nuevos sin repetir y sin emojis | Antes de cada video | `efectos/efectos.js`, `efectos/USO.md` |
| **auditor-calidad** | Revisa cada pieza contra todo lo que Kenneth pidió o rechazó. **Puede frenar** | Antes de la Sala y antes de Buffer | La calificación de 0 a 100 (`CALIFICACION.md`): pasa con 87 |
| **publicacion** | Revisa texto, hora, portada y marca de IA, programa con el sí de Kenneth y confirma que salió | Con el sí de la Sala y después de cada hora | `publicar.enviado.json` y el aviso si algo falló |
| **costeo** | Mide cuánto costó cada pieza y el costo por seguidor | Después de producir | `costos/` |

## El orden

```
tendencias ─┐
            ├─► estrategia ─► guionista ─► guion gráfico ($0) ─► Kenneth: sí ─► generador-videos + graficos
resultados ─┘                                                              │
     ▲                                                                     ▼
     │                                              auditor-calidad (con menos de 87, vuelve a producción)
     │                                              │
     │                                              │ 87 o más
     │                                              ▼
     └──────── publicacion ◄── Kenneth: sí en la Sala ◄── Sala de revisión
```

## Las tres reglas que no se saltan

0. **Nada se genera sin el sí de Kenneth al guion gráfico** (cuadros, voz, efectos, para qué es, texto de la
   publicación y costo, en la Sala). Así no se genera dos veces.
1. **Ninguna pieza llega a Kenneth con menos de 87 de 100** (`CALIFICACION.md`, Kenneth, 24-oct). La calificación
   se ve en la Sala. Con menos de 87 se arregla y se vuelve a auditar.
   La lista del auditor crece con cada cosa que Kenneth rechaza. Por ejemplo, el 23-oct entraron el cuerpo con brazos
   y nada de franjas oscuras.
2. **Quien produce no se revisa a sí mismo.** El auditor corre aparte y mira los cuadros del video final, no el código.

## Cómo se llaman

En una sesión nueva, por nombre: «usá el agente tendencias…».
En la sesión donde se crearon todavía no están cargados. Ahí se lanza un agente general y se le dice que lea su
archivo en `.claude/agents/` y lo siga al pie de la letra.
