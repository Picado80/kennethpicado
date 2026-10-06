# Encargo E001 — Radar semanal de virales para la marca personal

| Campo | Valor |
|---|---|
| Proyecto | kennethpicado (marca personal) |
| Persona | personal |
| Repo | `C:\Users\Picado\kennethpicado` |
| Rama base | `claude/personal-brand-video-strategy-j90cvq` |
| Escrito por | claude-code |
| Fecha | 2026-10-06 |
| Modo sugerido | seguro |

## Objetivo

Con un comando, Kenneth obtiene cada lunes la lista de los videos de TikTok más compartidos de la última semana, en sus cuentas y hashtags de referencia, con su texto, en `marca/semanas/AAAA-SNN-radar.md`.

## Contexto mínimo

- `marca/CICLO.md`: dónde encaja el radar (etapa 1) y qué viene después.
- `marca/README.md` §1 Idea: el radar alimenta el banco de ideas.
- `marca/scripts/verificar-llaves.ps1`: cómo se lee **una sola** llave de `torre/.env` sin cargar el archivo entero. El radar hace lo mismo con `APIFY_API_TOKEN`.
- `torre/protocolo/INDICE-CODIGO.md`: consultalo antes de escribir. No hay módulo de Apify registrado.
- La ficha del actor `clockworks/free-tiktok-scraper` en apify.com: **verificá el esquema de entrada y salida ahí antes de usarlo**; no supongas nombres de campos.

## Plan

1. `marca/radar/fuentes.json`: `cuentas` (lista de usuarios de TikTok, sin @), `hashtags`, `dias` (7), `min_vistas` (20000), `top` (15). Dejalo con 2 cuentas y 3 hashtags de ejemplo; Kenneth lo llena.
2. `marca/radar/radar.py` (Python 3.10+, solo biblioteca estándar más `requests`):
   - Leer `APIFY_API_TOKEN` de `%TORRE_DIR%\.env`, o de `%USERPROFILE%\torre\.env` si `TORRE_DIR` no existe. Leer solo esa línea, recortar lo que vaya después de un espacio y **nunca imprimir el valor**.
   - Correr el actor una vez por cuenta y una vez por hashtag, con el endpoint *run-sync-get-dataset-items* de Apify y un tiempo límite de 180 s por corrida. Si una corrida falla, seguir con las demás y anotarlo.
   - Normalizar cada video a: `url`, `cuenta`, `fecha`, `vistas`, `likes`, `comentarios`, `compartidos`, `guardados`, `duracion_s`, `texto` (caption), `transcripcion` (subtítulos en español si el actor los trae; si no, vacío).
   - Filtrar: últimos `dias` y `vistas >= min_vistas`. Sacar duplicados por `url`.
   - Ordenar por `compartidos / vistas` (descendente) y desempatar por `vistas`. Quedarse con `top`.
   - Escribir el JSON crudo en `marca/radar/salidas/AAAA-SNN.json` (ignorado por git) y la tabla en `marca/semanas/AAAA-SNN-radar.md`, con estas columnas: #, cuenta, vistas, % compartidos, duración, gancho (primeras 12 palabras del texto o de la transcripción), url.
3. Funciones puras separadas de la red (`normalizar`, `filtrar`, `ordenar`, `render_md`) y pruebas con pytest en `marca/radar/test_radar.py`, usando un JSON de muestra en `marca/radar/fixtures/`. Las pruebas no tocan la red.
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
- Cualquier llave: no se crea, no se imprime, no se escribe en ningún archivo.
- Publicar nada en ninguna red.

## Criterios de aceptación

- [ ] `python -m pytest marca/radar -q` en verde, sin red.
- [ ] Sin `APIFY_API_TOKEN`, el script termina con código 2 y un mensaje que dice dónde ponerla, sin traza de error.
- [ ] Ninguna salida (consola, JSON, md) contiene la llave. Hay una prueba que lo verifica.
- [ ] El md generado con la muestra tiene a lo sumo `top` filas, ordenadas por % de compartidos.
- [ ] Una corrida que falla para una cuenta no detiene las demás, y queda anotada en el md.

## Compuertas

```
python -m pytest marca/radar -q
```

## Restricciones

- No `git push`, no merge, no deploy.
- La única dependencia nueva permitida es `requests`. Si hace falta otra, decilo en el reporte y no la instales.

## Formato de retorno

El de la constitución del runner (VEREDICTO / QUÉ HICE / ARCHIVOS TOCADOS / COMPUERTAS / SUPUESTOS / LO QUE NO HICE Y POR QUÉ).
