# Herramientas: con qué se hace cada cosa

> Comparación con la lista de @quentin_aimarketing («Automatizá tu sistema de contenido con Claude
> por $30 al mes») que Kenneth pasó el 10-oct-2026. La mayoría ya la tenemos, con otras piezas.

| Para qué | La lista del video | Lo que usamos nosotros | Estado |
|---|---|---|---|
| Conectar todo | Claude Code ($20) | Claude Code, plan Max de Kenneth | **Listo** |
| Animar | Plugkit ($0) | HyperFrames: gráficos, papel recortado y pantalla dividida, hechos con código | **Listo** ($0) |
| De HTML a video | HyperFrames ($0) | HyperFrames | **Listo** ($0) |
| Editar | Editly ($0) | HyperFrames + ffmpeg | **Listo** ($0) |
| Oír (tiempos de cada palabra) | Whisper ($0) | ElevenLabs, dentro del plan de la voz | **Listo**. Whisper queda de respaldo gratis |
| Ver videos | Video-Use ($0) | ffmpeg saca los cuadros y Claude los revisa | **Listo**. Video-Use sirve para otra cosa: ver abajo |
| Bajar videos y datos | yt-dlp ($0) | yt-dlp (`radar/radar.py`) | **Listo**; los hashtags de TikTok siguen rotos |
| Investigar transcripciones | Apify ($0) | yt-dlp, y las transcripciones que pasa Kenneth | Apify está bloqueado por una factura de $29 |
| Predecir el gancho antes de publicar | — | Virality Predictor de Higgsfield, por el conector | **Probado el 11-oct**: $0, máximo 16 s por análisis. Es paso fijo antes de producir |
| Tomas de relleno | Higgsfield ($10) | Animaciones con código ($0) y HeyGen Video ($0.015/s) | Kenneth ya tiene Higgsfield (200 créditos): **falta probarlo** |
| Publicar | Plugkit ($0) | Buffer Free: Instagram y TikTok conectados | **Falta el script que programa** (encargo E003) |
| Subtítulos y retoques | Edits de Instagram ($0) | Los subtítulos ya salen puestos en el video | No hace falta |
| Calendario de contenido | Notion ($0) | `semanas/` en este repo | Notion está conectado: se puede reflejar ahí si Kenneth lo quiere ver en Notion |
| Páginas de destino | Claude Design ($0) | — | Para SEMI, cuando toque. El sitio personal no se toca |
| Correo y lista de interesados | Resend ($0) | — | **No existe.** Hace falta desde la fase 3 del arranque, o para SEMI |

**Lo que nosotros tenemos y esa lista no:** la voz clonada (ElevenLabs, $22 al mes), el gemelo (HeyGen,
unos $2 por video) y el agente `costeo`, que mide cada video contra la meta de $2.00.

**Sobre dos nombres de la lista:**
- **Plugkit:** no lo pude identificar; no aparece como herramienta pública con ese nombre. Lo que promete
  (animar y publicar) ya lo cubren HyperFrames y Buffer.
- **Video-Use** (de Browser Use, código abierto): edita material **grabado** a partir de la transcripción.
  Corta muletillas y silencios, y pone subtítulos. No sirve para el gemelo, pero sí para los videos
  personales que Kenneth grabe con el celular.

## Estilos de video hechos con código (13-oct)

Kenneth pidió instalar los cinco «skills» del video de @Web Tactics. Se bajaron y se revisaron por dentro (qué
ejecutan, a dónde se conectan, qué llaves piden): ninguno manda datos a un lugar raro. Las copias revisadas están en
`C:/Users/Picado/Downloads/skills-video/`, fijas en la versión que se leyó.

| Skill | Qué da | Repositorio y versión revisada | Licencia | Costo y requisitos | Para la marca |
|---|---|---|---|---|---|
| **HyperFrames** | HTML que se vuelve video. Es con lo que ya se hace todo | `heygen-com/hyperframes` | Apache 2.0 | $0 | **Ya instalado** desde el 8-oct (9 skills). Es la base |
| **onetake** | Una sola toma continua: cada momento sale del anterior y la cámara nunca corta | `feitangyuan/onetake` · `4157581` (12-oct) | **PolyForm Noncommercial: prohíbe el uso comercial** | $0. Python con Playwright, numpy y scipy; ffmpeg; Node | **No para videos publicados de la marca** sin pagar la licencia comercial (onetakemotion.com). Sirve para estudiar la continuidad y aplicarla en HyperFrames |
| **gbro-collage-broll** | Tomas de relleno de 5 s en papel recortado con trama de puntos, que se arman solas | `pyang5166/gbro-collage-broll` · `a1a4ee2` (15-jul) | MIT | **Cobra por uso:** el video lo genera Gemini (hace falta `GEMINI_API_KEY`). Está en chino y pensado para Codex: la imagen fija hay que generarla con otra herramienta | Solo si el estilo vale lo que cuesta. El papel recortado de la línea A ya sale gratis con código |
| **Claude Animation Base** | Dibujos animados pintados a mano (p5.js y p5.brush) | `JohnHeibel/ClaudeAnimationBase` · `0ac8bf2` (24-sep) | MIT | $0. Node, Chrome y ffmpeg. Sin tarjeta de video dedicada, la acuarela es lenta | La técnica sí. **El personaje es Clawd, la mascota de Anthropic:** para la marca se dibuja un personaje propio |
| **Lemo-Opuscar** | 43 estilos de cine hechos solo con código (óleo, acuarela, tinta china, pizarra, plano técnico, datos, 16 bits…) | `lemomo-ai/lemo-opuscar` · `fdc46d7` (13-oct) | MIT (guías y muestras, CC BY 4.0) | $0. Node 20+, ffmpeg y Python 3.11+. La instalación de dependencias está escrita para Mac y Linux: **en Windows está sin probar** | El más útil para variar la línea A: un estilo por serie (pizarra para *IA sin jerga*, datos para *El número*, plano técnico para *Las cinco capas*) |

**Estado:** los cuatro nuevos están descargados y revisados, **sin instalar**: la sesión no tiene permiso para
escribir en la carpeta de skills de Claude (`~/.claude/skills`). Los instala Kenneth con cinco órdenes de copia.
Las dependencias de cada uno (paquetes de Node y de Python, el navegador sin ventana) se instalan la primera vez que
se use, no antes.

**Antes de actualizar cualquiera:** volver a leer lo que cambió. Lemo-Opuscar, tal como quedó, no se actualiza solo.

## Líneas de trabajo que salen de aquí

1. **Publicar solo:** el script que programa en Buffer (E003), con la aprobación de Kenneth antes de cada publicación.
2. **Probar Higgsfield** para una toma realista en la mitad de arriba, con los 200 créditos que ya hay.
3. **Video-Use** para los videos personales del arranque (`ARRANQUE.md`, regla 3).
4. **Lista de interesados** (Resend u otra), cuando haya a dónde mandar a la gente.
5. **Calendario en Notion**, solo si Kenneth lo quiere ver ahí.
