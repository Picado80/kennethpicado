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

## Líneas de trabajo que salen de aquí

1. **Publicar solo:** el script que programa en Buffer (E003), con la aprobación de Kenneth antes de cada publicación.
2. **Probar Higgsfield** para una toma realista en la mitad de arriba, con los 200 créditos que ya hay.
3. **Video-Use** para los videos personales del arranque (`ARRANQUE.md`, regla 3).
4. **Lista de interesados** (Resend u otra), cuando haya a dónde mandar a la gente.
5. **Calendario en Notion**, solo si Kenneth lo quiere ver ahí.
