# Encargo E001 — Radar semanal de virales para la marca personal

| Campo | Valor |
|---|---|
| Proyecto | kennethpicado (marca personal) |
| Persona | personal |
| Repo | `C:\Users\Picado\kennethpicado` |
| Rama base | `claude/personal-brand-video-strategy-j90cvq` |
| Escrito por | claude-code |
| Fecha | 2026-10-06 (v2: fuente yt-dlp en vez de Apify) |
| Modo sugerido | seguro |

## Objetivo

Con un comando, Kenneth obtiene cada lunes, en `marca/semanas/AAAA-SNN-radar.md`, la lista de los videos de TikTok más compartidos de la última semana de sus cuentas de referencia, con su texto.

## Contexto mínimo

- `marca/CICLO.md`: dónde encaja el radar (etapa 1) y qué viene después.
- `marca/README.md` §1 Idea: el radar alimenta el banco de ideas.
- `torre/protocolo/INDICE-CODIGO.md`: consultalo antes de escribir.
- **Fuente: yt-dlp, no Apify** (la cuenta de Apify está bloqueada). Antes de escribir el código, verificá con la versión instalada qué devuelve yt-dlp para una página de usuario de TikTok y para un video (`--dump-json`). Los nombres de campos salen de esa salida real, no de memoria.

## Plan

1. `marca/radar/fuentes.json`: `cuentas` (usuarios de TikTok, sin @), `urls` (videos sueltos que Kenneth quiera sumar a mano), `dias` (7), `min_vistas` (20000), `top` (15), `por_cuenta` (30). Dejalo con 2 cuentas de ejemplo; Kenneth lo llena.
2. `marca/radar/radar.py` (Python 3.10+, solo biblioteca estándar; llama a `yt-dlp` como proceso):
   - Si `yt-dlp` no está instalado, salir con código 2 y el comando para instalarlo (`pip install -U yt-dlp`), sin traza de error.
   - Por cuenta: listar los últimos `por_cuenta` videos (`https://www.tiktok.com/@<cuenta>`, lista plana) y después leer los metadatos de cada video sin descargarlo. Si TikTok bloquea la lista de una cuenta, anotarlo y seguir; ofrecer `--cookies-from-browser <navegador>` como opción del script.
   - Sumar los videos de `urls`.
   - Normalizar cada video a: `url`, `cuenta`, `fecha`, `vistas`, `likes`, `comentarios`, `compartidos`, `duracion_s`, `texto` (descripción) y `transcripcion` (subtítulos en español si yt-dlp los encuentra; si no, vacío). Si falta un campo, va `null`; no se inventa.
   - Filtrar: últimos `dias` y `vistas >= min_vistas`. Sacar duplicados por `url`.
   - Ordenar por `compartidos / vistas` (descendente) y desempatar por `vistas`. Quedarse con `top`.
   - Escribir el JSON crudo en `marca/radar/salidas/AAAA-SNN.json` (ignorado por git) y la tabla en `marca/semanas/AAAA-SNN-radar.md`, con estas columnas: #, cuenta, vistas, % compartidos, duración, gancho (primeras 12 palabras del texto o de la transcripción), url. Al final, una lista de las cuentas que fallaron.
3. Funciones puras separadas del proceso externo (`normalizar`, `filtrar`, `ordenar`, `render_md`) y pruebas con pytest en `marca/radar/test_radar.py`, usando JSON de muestra en `marca/radar/fixtures/` copiado de una salida real de yt-dlp. Las pruebas no tocan la red ni llaman a yt-dlp.
4. Agregar `marca/radar/salidas/` a `.gitignore`.
5. Una sección corta en `marca/README.md` §1 Idea: cómo se corre (`python marca\radar\radar.py`).

## Alcance

**Puede tocar:**
- `marca/radar/**`
- `marca/README.md` (solo §1 Idea)
- `.gitignore`

**Fuera de alcance (tocarlo invalida la entrega):**
- **El repo `torre` COMPLETO: es solo lectura.** Lo consultás (`INDICE-CODIGO.md`) y no escribís nada ahí: ni ledger, ni evento, ni puente, ni commits. Un encargo no es una sesión de TORRE; el bookkeeping lo escribe quien audita (MAESTRO §Ejecutores y bookkeeping).
- `main`, el sitio (`index.html`, `case/`, `assets/`), `.vercelignore`.
- Llaves de cualquier tipo, y cookies: si se usan, solo se leen del navegador en el momento y nunca se escriben a un archivo.
- Descargar videos. Publicar nada en ninguna red.

## Criterios de aceptación

- [ ] `python -m pytest marca/radar -q` en verde, sin red.
- [ ] Sin yt-dlp instalado, el script termina con código 2 y dice cómo instalarlo.
- [ ] El md generado con la muestra tiene a lo sumo `top` filas, ordenadas por % de compartidos.
- [ ] Una cuenta que falla no detiene las demás y queda anotada en el md.
- [ ] Una corrida real con las 2 cuentas de ejemplo, con su salida pegada en el reporte (o el error exacto de TikTok, si bloquea).

## Compuertas

```
python -m pytest marca/radar -q
```

## Restricciones

- No `git push`, no merge, no deploy.
- Ninguna dependencia de Python nueva aparte de `pytest` para las pruebas. yt-dlp se usa como programa externo.

## Formato de retorno

El de la constitución del runner (VEREDICTO / QUÉ HICE / ARCHIVOS TOCADOS / COMPUERTAS / SUPUESTOS / LO QUE NO HICE Y POR QUÉ).
