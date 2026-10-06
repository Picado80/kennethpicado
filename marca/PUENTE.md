# Puente — marca personal (6-oct-2026, tarde)

> Corre **en la PC de Kenneth**. Desde ahí Claude llega a `torre/.env`, a TikTok, a ElevenLabs y a HeyGen.
> Cómo contestarle a Kenneth: `CLAUDE.md` (qué hice / qué falta / qué hacés vos, una vez, nada más).

## Dónde está todo

- **Rama de trabajo:** `claude/marca-voz-y-radar` (PR en borrador). Antes: `claude/personal-brand-video-strategy-j90cvq` (PR #1, ya mergeado en main).
- **Rama vieja borrada:** `minimax/E001-radar-de-virales`, local y remota. Estaba vacía (todo su contenido ya estaba en main).
- **Llaves:** `HEYGEN_API_KEY` y `ELEVENLABS_MARCA_API_KEY` en `C:\Users\Picado\torre\.env`, las dos verificadas. Plan de ElevenLabs: **creator** (0 de 186.000 caracteres usados).

## Qué funciona (probado en la PC, 6-oct)

| Pieza | Cómo se corre | Estado |
|---|---|---|
| Verificar llaves | `powershell -ExecutionPolicy Bypass -File marca\scripts\verificar-llaves.ps1` | verde. HeyGen: 20 avatares. ElevenLabs: 30 voces, 9 propias |
| Probar la voz clonada | `powershell -ExecutionPolicy Bypass -File marca\scripts\probar-voz.ps1 -VozId jntdbfQTWPMmzXt1UxCu` | mp3 generado OK. **Falta que Kenneth lo escuche y confirme si suena a él** |
| Radar de virales | `python marca\radar\radar.py` | 13 pruebas en verde. Corre, pero sin cuentas en `fuentes.json` da 0 |

### Voz clonada
- No hay clon *instantáneo*; el clon de Kenneth es **profesional** (categoría `professional`, no `cloned`), por eso `probar-voz.ps1` sin `-VozId` no lo encontraba.
- Es **"Picado"**, ID `jntdbfQTWPMmzXt1UxCu`. El mp3 de prueba quedó en `marca\salidas\` (no va a git).
- Cuando Kenneth diga que suena a él, guardar el ID en `config\estudio.json` → `elevenlabs.voz_kenneth`.

### Radar — hallazgo importante
- yt-dlp (2026.08.19) tiene **roto el extractor de hashtags de TikTok** ("No working app info is available"). Los hashtags de `fuentes.json` devuelven 0 pase lo que pase. No es cosa de cookies (chrome queda bloqueado en Windows; edge falla DPAPI; firefox descifra pero igual 0).
- yt-dlp **sí lee cuentas** (`@usuario`): probado, devuelve videos con vistas. El radar funcionará apenas haya cuentas en `fuentes.json`.
- Arreglo hecho en `radar.py`: un extractor roto ahora se reporta como **FALLA** en la tabla, no como "ok 0 videos" silencioso (antes engañaba). Dos pruebas nuevas cubren esto.

## Lo que espera una decisión de Kenneth

- **Las 5 a 10 cuentas de TikTok de referencia** para `marca\radar\fuentes.json` → es lo que destraba el radar (los hashtags no sirven hoy).
- Confirmar si el mp3 de la voz suena a él (para guardar el ID).
- Episodio 0: *«Le di a mi oficina de siete IAs $100 y 30 días para conseguirme un cliente»* (`CICLO.md`).
- El gemelo de HeyGen: grabar 2 minutos a cámara y el consentimiento.
- Postiz: abrir la cuenta y conectar TikTok, para la publicación (E003).

## Siguientes encargos (en orden)

- **E002 · Producción:** guion → audio con el clon (`eleven_v4`, voz `jntdbfQTWPMmzXt1UxCu`) → video con el gemelo de HeyGen (API v3; leer `https://developers.heygen.com/llms.txt` antes de escribir nada) → mp4 en `marca\salidas\`.
- **E003 · Publicación:** Postiz → TikTok con `DIRECT_POST` y etiqueta de IA, solo con la aprobación de Kenneth.
- **E004 · Medición:** métricas a `medicion\registro.csv` a las 48 h y a los 7 días.
