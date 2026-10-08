# Tarifas: lo que cuesta cada pieza de un video

> Tope: **$3 por video**. **Meta nueva: $2.00** (Kenneth, 8-oct-2026), con unos 25 s de él en pantalla.
> Cada gasto real va a [`registro.csv`](registro.csv). El agente `costeo` (`.claude/agents/costeo.md`)
> lee las dos cosas y dice dónde recortar.

## Lo que se paga por uso

| Pieza | Proveedor | Tarifa | Fuente |
|---|---|---|---|
| Gemelo de video, Avatar V | HeyGen API | $0.12 / s | Captura de precios de la API, 8-oct |
| Gemelo de video, Avatar IV | HeyGen API | $0.0805 / s | ídem; el 002 de 50 s costó exacto $4.03 |
| Avatar de foto, Avatar IV | HeyGen API | $0.0385 / s | ídem (acepta `motion_prompt`) |
| Gemelo de video, Avatar III | HeyGen API | $0.01 / s | ídem. A Kenneth no le gustó: «se ve demasiado IA» |
| Toma de relleno, 768p | HeyGen Video (`heygen-video-1`) | $0.015 / s | Captura, 8-oct. **Promoción de lanzamiento: 50 % menos**; la lista es el doble |
| Toma de relleno, 480p | HeyGen Video | $0.01 / s | ídem |
| Toma de relleno, 1080p | HeyGen Video | 3 veces la de 768p | docs de HeyGen Video |

**El `motion_prompt` (mover ojos y cabeza) no se acepta en gemelos de video**, solo en avatares de foto:
`motion_prompt is not supported for video avatars` (HeyGen, 8-oct).

## Lo que ya está pagado (costo extra $0)

| Pieza | Plan | Costo fijo |
|---|---|---|
| Voz clonada, transcripción y efectos de sonido | ElevenLabs Creator | $22 / mes (186.000 caracteres) |
| Gráficos, subtítulos, montaje y render | HyperFrames (Apache 2.0, corre en la PC) | $0 |
| Guion, dirección y armado | Claude, plan Max de Kenneth | ya pagado; sin uso extra activado |

## La alternativa más barata para el gemelo

**HeyGen Creator en la web: $29 / mes = 600 créditos.** El gemelo con Avatar IV gasta 31 créditos
por minuto: unos **19,4 min al mes, $1.49 / min**, contra $4.83 / min por la API. Con Avatar V son 48
créditos por minuto (12,5 min). La web no se maneja por API: se arma en el navegador.
Fuente: investigación del 8-oct (help.heygen.com, artículos 15126059 y 10060327).

Otras opciones revisadas el 8-oct (Hedra, Kling Avatar 2.0, OmniHuman, Seedance, Higgsfield,
Artlist, sync.so, código abierto): ninguna salió más barata con la misma calidad. Kling Avatar 2.0
no lista el español para el movimiento de labios.
