# Llaves de la marca

## La regla: en este repo no vive ninguna llave

`Picado80/kennethpicado` es un repo **público** en GitHub y Vercel publica lo que hay en él.
Una llave que entra acá es una llave publicada. Por eso se sigue tu propia regla de TORRE
(`torre/protocolo/LLAVES.md`): **todas las llaves viven en un solo archivo,
`C:\Users\Picado\torre\.env`, cada una con su ficha.** Ningún `.env` suelto por proyecto.

Lo que sí vive en esta carpeta son las **llaves creativas**: el ID de tu avatar, los IDs de las
voces y el formato de render, en [`config/estudio.json`](config/estudio.json). Sin la llave
secreta esos IDs no sirven para nada, así que se pueden commitear sin riesgo.

---

## HeyGen: dónde va (la respuesta corta)

1. Sacá la llave en HeyGen: **Settings → API**.
2. Abrí `C:\Users\Picado\torre\.env` con el bloc de notas.
3. Pegá esto al final y poné tu llave después del `=`:

```
# HeyGen — gemelo digital (avatar) y traducción de video de la marca personal.
# Llave de la cuenta: app.heygen.com → Settings → API. Persona: personal.
# La usan los scripts de kennethpicado/marca. No va a Vercel: el sitio no la usa.
# Endpoint https://api.heygen.com · header X-Api-Key. Se rota en el mismo panel.
HEYGEN_API_KEY=
```

4. Para cerrar el ciclo de TORRE: la misma ficha, **con el valor vacío**, va en
   `torre/.env.example`, y una fila en la tabla de `torre/protocolo/LLAVES.md`:

```
| `HEYGEN_API_KEY` | HeyGen | gemelo digital y traducción de video de la marca personal | `https://api.heygen.com` · header `X-Api-Key` | app.heygen.com → Settings → API |
```

> Revisá si tu plan de HeyGen trae créditos de API. Históricamente el API se cobra aparte
> del plan web: puede que la llave funcione y aun así no te deje generar nada.

**Cómo se comprueba sin imprimir la llave** (las dos, HeyGen y ElevenLabs):

```powershell
cd C:\Users\Picado\kennethpicado
powershell -ExecutionPolicy Bypass -File marca\scripts\verificar-llaves.ps1
```

[`scripts/verificar-llaves.ps1`](scripts/verificar-llaves.ps1) busca solo esas dos llaves con
el mismo buscador de TORRE (`Get-ProveedorKey`), hace lecturas que no gastan créditos (cuota y
avatares en HeyGen; plan y voces en ElevenLabs), avisa si la llave de la marca es la misma que la
de Semi y de cada llave muestra solo el largo y los últimos 4 caracteres. Las listas completas
de avatares y voces quedan en `marca/salidas/`, que git ignora. Corre en tu máquina: desde el
entorno en la nube, el proxy bloquea `api.heygen.com` y `api.elevenlabs.io`.

---

## ElevenLabs: lo que sigue (y no conviene reusar la llave que ya tenés)

`ELEVENLABS_API_KEY` **ya existe** en `torre/.env`: es la llave del producto Semi (la voz del
agente en E134, la que también está subida a Vercel). **Mi recomendación es no reusarla para la marca:**

1. **Cuota compartida.** Si una semana de videos se come los créditos, la voz del agente de
   Semi se queda muda en medio de una demo con un cliente.
2. **Tu voz clonada.** Si tu clon vive en la misma cuenta que la llave que está en Vercel,
   cualquiera que obtenga esa llave puede hacer que tu voz diga lo que quiera.
   Una persona, una llave.
3. **Rotación.** Si tenés que cambiar una llave, no se rompe la otra.

**La ficha que propongo** (va en `torre/.env`, igual que la de HeyGen):

```
# ElevenLabs (marca personal) — voz clonada de Kenneth y voces de los personajes de La Oficina.
# Llave aparte de ELEVENLABS_API_KEY (esa es del producto Semi). Persona: personal.
# elevenlabs.io → Profile → API keys. Si el panel lo permite: límite de créditos por llave.
# Endpoint https://api.elevenlabs.io · header xi-api-key. Se rota en el mismo panel.
ELEVENLABS_MARCA_API_KEY=
```

**Hay que decidir una cosa antes de pegarla:** ¿en qué cuenta de ElevenLabs está la llave de
Semi? Si es la cuenta de `trysemi.com`, tu clon debería vivir en tu cuenta personal
(`aquilesmaximus@gmail.com`), con su propia llave.

---

## Buffer: publicar en IG, YouTube y LinkedIn (plan Free)

Herramienta elegida para la etapa 4 (`CICLO.md` §Alternativas para publicar). Postiz quedó
descartado por precio. El plan Free da **3 canales** (Instagram + YouTube + LinkedIn), 10 posts
programados por canal y **1 llave de API** (3.000 llamadas/mes, **sin MCP**). TikTok se sigue
subiendo a mano por los sonidos nativos.

```
# Buffer (marca personal) — programar IG, YouTube y LinkedIn (plan Free). Persona: personal.
# publish.buffer.com → Settings → Developers/API. La usan los scripts de kennethpicado/marca.
# No va a Vercel: el sitio no la usa. Docs: developers.buffer.com (confirmar endpoint y header ahi).
BUFFER_API_KEY=
```

**Cómo se comprueba sin imprimir la llave:** una llamada de solo lectura que liste los canales
conectados (según `developers.buffer.com`), mostrando solo el largo y los últimos 4 caracteres de
la llave. Queda pendiente hasta que Kenneth pegue la llave en `torre/.env`.

> La ficha de TORRE (`torre/.env.example` + fila en `torre/protocolo/LLAVES.md`) la agrega la
> sesión de la nube.

---

## El cuadro completo

| Qué | Nombre | Dónde | ¿Es secreto? |
|---|---|---|---|
| Llave de HeyGen | `HEYGEN_API_KEY` | `torre/.env` | **Sí** |
| Llave de ElevenLabs (marca) | `ELEVENLABS_MARCA_API_KEY` | `torre/.env` | **Sí** |
| Llave de Buffer (marca) | `BUFFER_API_KEY` | `torre/.env` | **Sí** |
| ID del gemelo en HeyGen | `heygen.avatar_id` | `config/estudio.json` | No |
| ID de tu voz clonada | `elevenlabs.voz_kenneth` | `config/estudio.json` | No |
| IDs de las voces de La Oficina | `elevenlabs.elenco.*` | `config/estudio.json` | No |
