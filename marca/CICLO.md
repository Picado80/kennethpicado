# El ciclo autónomo: investigar → adaptar → crear → publicar → medir → repetir

> Tomado del experimento de @Morfeo («Le di a Claude 100 dólares para hacerme viral»), con
> nuestras piezas. Es el proceso de `README.md`, pero con máquinas en cada etapa.

## Tres cambios respecto a lo de Morfeo

1. **La meta no son vistas: son conversaciones con empresas.** Un millón de vistas de gente
   que no contrata es ruido. Se mide lo que dice `README.md` §Medición.
2. **Kenneth aprueba antes de publicar.** Quien produce no publica solo: es la regla de TORRE
   («quien ejecuta no se revisa a sí mismo»). Después de 30 videos aprobados sin rechazos, los
   formatos ya probados pueden publicarse solos.
3. **Se copia el mecanismo, nunca el contenido** (`viral-content-machine/VIRAL_CONTENT_PLAYBOOK.md` §1).

## La versión grande: el experimento es el contenido

**Episodio 0 de *La Oficina*: «Le di a mi oficina de siete IAs $100 y 30 días para conseguirme
un cliente.»** Morfeo buscó vistas; vos buscás un cliente de verdad. Hay un video por semana
con el avance (la serie retiene) y al final, con cliente o sin él, queda un caso real para
LinkedIn y para mostrarle a empresas.

## Las etapas

| # | Etapa | Qué hace | Con qué | Estado | Encargo |
|---|---|---|---|---|---|
| 1 | **Radar** | Cada lunes trae los videos más compartidos de la semana en una lista de cuentas, con su texto | yt-dlp (gratis, sin llave). Apify queda para después, si hace falta escala | falta la lista de cuentas | [`E001`](encargos/E001-radar-de-virales.md) |
| 2 | **Análisis** | Las 7 preguntas del playbook; elige los formatos que se repiten y suma 5 ideas puntuadas a `ideas.md` | Claude, en sesión | listo (playbook + `ideas.md`) | — |
| 3 | **Producción** | Guion → tu voz (ElevenLabs, `eleven_v4`) → video (gemelo de HeyGen con ese audio, o grabación real) → edición | ElevenLabs + HeyGen + CapCut | falta el clon y el gemelo | E002 (después del clon) |
| 4 | **Publicación** | Sube a TikTok con caption y etiqueta de IA, a la hora del plan | Postiz (`DIRECT_POST`) | falta cuenta de Postiz con TikTok conectado y `POSTIZ_API_KEY` | E003 |
| 5 | **Medición** | A las 48 h y a los 7 días, números al registro; el lunes, el formato ganador se repite con otro gancho y el perdedor se mata | Postiz / TikTok Studio → `medicion/registro.csv` | plantilla lista | E004 |

**Tope de gasto:** $100 al mes entre todas las herramientas. Cada gasto queda anotado en la revisión del lunes.
