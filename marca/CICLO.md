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
| 1 | **Radar** | Cada lunes trae los videos más compartidos de la semana en una lista de cuentas, con su texto | yt-dlp (gratis, sin llave) | **hecho** (`radar/radar.py`); 4 cuentas verificadas en `fuentes.json` para que taches. Los hashtags están rotos en yt-dlp | [`E001`](encargos/E001-radar-de-virales.md) |
| 2 | **Análisis** | Las 7 preguntas del playbook; elige los formatos que se repiten y suma 5 ideas puntuadas a `ideas.md` | Claude, en sesión | listo (playbook + `ideas.md`) | — |
| 3 | **Producción** | Guion → tu voz (ElevenLabs, `eleven_v4`) → video (gemelo de HeyGen con ese audio, o grabación real) → edición | ElevenLabs + HeyGen + CapCut | falta el clon y el gemelo | E002 (después del clon) |
| 4 | **Publicación** | TikTok a mano (sonido y texto nativos); IG, YouTube y LinkedIn programados con caption y etiqueta de IA | TikTok nativo + **Buffer Free** | falta abrir Buffer y conectar las redes | E003 |
| 5 | **Medición** | A las 48 h y a los 7 días, números al registro; el lunes, el formato ganador se repite con otro gancho y el perdedor se mata | Postiz / TikTok Studio → `medicion/registro.csv` | plantilla lista | E004 |

**Tope de gasto:** $100 al mes entre todas las herramientas. Cada gasto queda anotado en la revisión del lunes.

## Alternativas a Apify para el radar

| Opción | Costo | A favor | En contra |
|---|---|---|---|
| **yt-dlp** (lo que ya está andando) | $0 | Sin cuenta ni llave; también trae hashtags | TikTok a veces pide sesión: se resuelve con `--cookies-from-browser` |
| **Scrape Creators** (lo que usó Morfeo) | Pago por uso | API simple para TikTok, Instagram y LinkedIn | Otra cuenta y otra llave |
| **Bright Data** (el plugin ya está instalado en tu Claude) | Pago por uso | Datos de TikTok a escala | Más caro y más complejo de lo que hace falta hoy |
| **TinyFish** (ya conectado en tu Claude) | Por uso | Navega las páginas como una persona | Lento para muchas cuentas |
| **API oficial de TikTok** (Display API) | $0 | Métricas oficiales de **tus** videos | No sirve para mirar a otros: sirve para la etapa 5 (medición) |
| **Apify** | Plan Free con $5 al mes | Ya estaba integrado en viral-content-machine | Cuenta bloqueada por la factura de junio |

**Decisión:** yt-dlp ahora. Si TikTok lo bloquea seguido, Scrape Creators. La API oficial de TikTok queda para medir tus propios videos.

## Alternativas para publicar

Postiz quedó descartado por precio. La herramienta elegida es **Buffer Free** para IG, YouTube y LinkedIn; TikTok se sube a mano (sonido y texto nativos, como dice `README.md` §4).

| Opción | Costo | A favor | En contra |
|---|---|---|---|
| **Buffer Free** (elegida) | **$0** | 3 canales (IG + YouTube + LinkedIn), 10 posts programados por canal (se recargan), 1 llave de API (3.000 llamadas/mes) | **sin MCP**; TikTok no entra en los 3 gratis; tope de 10 programados por canal a la vez |
| **Publora** | $4–6 por red | barato por red, muchas plataformas | se paga por cada red |
| **Buffer Essentials** | $6 por red (1–10) | posts programados ilimitados, analítica, API 7.500/mes | de pago; baja a $4/red con 11+ |
| **Postiz** | $29/mes | `DIRECT_POST` a TikTok, autohospedable | caro para arrancar (descartado) |

**Decisión:** Buffer Free para IG/YouTube/LinkedIn ($0); TikTok a mano. Si más adelante hace falta programar TikTok o pasar de 10 posts por red, se evalúa Buffer Essentials o Publora.
