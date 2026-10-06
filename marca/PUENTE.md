# Puente — marca personal (6-oct-2026)

> Para la sesión que sigue, que corre **en la PC de Kenneth** (Remote Control o Claude Desktop).
> Desde ahí Claude llega a `torre/.env`, a TikTok, a ElevenLabs y a HeyGen, y puede despachar a MiniMax.
> Cómo contestarle a Kenneth: `CLAUDE.md` (qué hice / qué falta / qué hacés vos, una vez, nada más).

## Dónde está todo

- **Rama de trabajo:** `claude/personal-brand-video-strategy-j90cvq` · PR [Picado80/kennethpicado#1](https://github.com/Picado80/kennethpicado/pull/1) (borrador).
- **Bookkeeping de TORRE:** PR [Picado80/torre#45](https://github.com/Picado80/torre/pull/45) (llaves, índice #95, ledger, evento).
- **Llaves:** `HEYGEN_API_KEY` y `ELEVENLABS_MARCA_API_KEY` en `C:\Users\Picado\torre\.env`, las dos **verificadas** (`marca\scripts\verificar-llaves.ps1`). Plan de ElevenLabs: Starter.
- **Rama vieja para borrar:** `minimax/E001-radar-de-virales`, local y remota (desde la nube no se pudo borrar). Está vacía: el radar lo hizo Claude.

## Qué funciona

| Pieza | Cómo se corre | Estado |
|---|---|---|
| Verificar llaves | `powershell -ExecutionPolicy Bypass -File marca\scripts\verificar-llaves.ps1` | verde en la PC |
| Probar la voz clonada | `powershell -ExecutionPolicy Bypass -File marca\scripts\probar-voz.ps1 [-VozId <id>]` | **sin probar**: el clon ya está listo |
| Radar de virales | `python marca\radar\radar.py` | 11 pruebas en verde; sin correr contra TikTok de verdad |

## Lo primero que hace la próxima sesión (sin pedirle nada a Kenneth)

1. `git pull` en la rama de trabajo. Borrar `minimax/E001-radar-de-virales`: `git branch -D` y `git push origin --delete`.
2. Correr `probar-voz.ps1`. Si dice que no hay clon instantáneo, listar las voces (`verificar-llaves.ps1` las muestra con ID) y probar con `-VozId`. Darle a Kenneth el mp3 para escuchar. Si suena a él, guardar el ID en `config\estudio.json` (`elevenlabs.voz_kenneth`).
3. `python -m pip install -U yt-dlp` y correr el radar. Si TikTok bloquea: `--cookies-from-browser chrome`. Pasarle a Kenneth la tabla de `semanas\AAAA-SNN-radar.md`.

## Lo que espera una decisión de Kenneth

- La lista de 5 a 10 cuentas de TikTok de referencia para `marca\radar\fuentes.json`.
- Si va con el episodio 0: *«Le di a mi oficina de siete IAs $100 y 30 días para conseguirme un cliente»* (`CICLO.md`).
- El gemelo de HeyGen: grabar 2 minutos a cámara y el consentimiento.
- Postiz: abrir la cuenta y conectar TikTok, para la publicación (E003).

## Siguientes encargos (en orden)

- **E002 · Producción:** guion → audio con el clon (`eleven_v4`) → video con el gemelo de HeyGen (API v3; leer `https://developers.heygen.com/llms.txt` antes de escribir nada) → mp4 en `marca\salidas\`.
- **E003 · Publicación:** Postiz → TikTok con `DIRECT_POST` y etiqueta de IA, solo con la aprobación de Kenneth.
- **E004 · Medición:** métricas a `medicion\registro.csv` a las 48 h y a los 7 días.
