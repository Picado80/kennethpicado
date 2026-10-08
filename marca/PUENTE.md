# Puente — marca personal (7-oct-2026): de la nube a la PC

> **Para la sesión que sigue, en la PC de Kenneth** (Claude Code local en `C:\Users\Picado\kennethpicado`,
> o la sesión de Remote Control «Marca personal: voz y radar»). Desde la PC, Claude llega a
> `torre\.env`, a TikTok, ElevenLabs, HeyGen y Buffer, y puede despachar a MiniMax. Desde la nube, no.
>
> **Cómo contestarle a Kenneth** (`CLAUDE.md`, obligatorio): un solo mensaje con tres partes, en
> este orden: **Qué hice / Qué falta / Qué hacés vos**. Cada parte una vez, sin contexto ni
> opciones que no pidió. Los eventos automáticos (CI, Vercel, recordatorios) no generan mensaje.
> Kenneth quiere que Claude **haga** el trabajo, no que se lo pase: si algo lo puede hacer Claude
> desde la PC, lo hace Claude. Y quiere ideas que lo empujen, no un sí a todo.

---

## 1. Hacia dónde vamos

**Tesis de la marca:** «No necesitás ser técnico para trabajar con IA. Necesitás saber dirigir.»

- **Audiencia:** dueños y gerentes de negocios que **no** son técnicos, primero en Costa Rica.
- **Plataformas:** TikTok primero. LinkedIn cuando haya 30 videos y 2 formatos validados.
- **Meta:** **conversaciones con empresas por mes**, no vistas. Una conversación cuenta cuando
  alguien que dirige o decide en un negocio le escribe a Kenneth por algo que vio.
- **Los 4 formatos** (`FORMATOS.md`):
  - *La Oficina*: las IAs de TORRE como empleados.
  - *Amazon en la soda*.
  - *Sistema de la semana*.
  - *¿Cuál soy yo?*: el gemelo de IA, nunca antes del video 15 y como mucho 1 de cada 5.
- **La versión grande** (`CICLO.md`), que espera el sí de Kenneth: Episodio 0 de *La Oficina*,
  «Le di a mi oficina de siete IAs $100 y 30 días para conseguirme un cliente». Hay un video por
  semana con el avance, y al final queda un caso real para LinkedIn y para empresas.
- **Tope de gasto:** $100 al mes entre todas las herramientas.

## 2. Mapa: dónde vive cada cosa

```
C:\Users\Picado\
├── kennethpicado\            repo PÚBLICO Picado80/kennethpicado (sitio en Vercel)
│   ├── CLAUDE.md             cómo contestarle a Kenneth
│   ├── .vercelignore         saca marca/ del sitio (404 confirmado)
│   └── marca\                el sistema de la marca (NUNCA llaves acá)
│       ├── README.md         el proceso en 5 etapas + ritmo semanal
│       ├── CICLO.md          el ciclo autónomo + alternativas (radar y publicación)
│       ├── CANON.md          tesis, voz, límites, qué es real y qué es IA
│       ├── FORMATOS.md       4 formatos + orden de lanzamiento
│       ├── VENTA.md          los 17 términos de psicología de venta, fuera de TikTok
│       ├── LLAVES.md         fichas de las llaves (dónde van, cómo se prueban)
│       ├── PUENTE.md         este archivo
│       ├── ideas.md          banco de ideas con puntaje U/V/T/P
│       ├── config\estudio.json  IDs de avatar y voces (no son secretos)
│       ├── guiones\          001-la-oficina-examen.md, 002-amazon-soda-vacaciones.md
│       ├── plantillas\       guion.md, semana.md
│       ├── semanas\          2026-S41-radar.md (primera corrida real)
│       ├── medicion\registro.csv
│       ├── encargos\         E001-radar-de-virales.md (hecho)
│       ├── radar\            radar.py, fuentes.json, test_radar.py (13 pruebas), fixtures\
│       └── scripts\          verificar-llaves.ps1, probar-voz.ps1, buffer-canales.ps1
├── torre\                    repo Picado80/torre: el sistema TORRE
│   ├── .env                  TODAS las llaves (HEYGEN, ELEVENLABS_MARCA, BUFFER, …)
│   ├── .env.example          fichas de cada llave
│   ├── protocolo\            LLAVES.md, eventos.jsonl (+ lint_eventos.py), INDICE-CODIGO.md
│   ├── plataformas\claude-code.md   ledger
│   └── hooks\dispatch\       despachar.ps1, proveedores.ps1 (Get-ProveedorKey)
└── (otros repos que se tocaron: Picado80/centro-comando, Picado80/viral-content-machine)
```

**El flujo de la marca y su estado:**

```
 1 RADAR ───► 2 ANÁLISIS ───► 3 PRODUCCIÓN ─────────────► 4 PUBLICACIÓN ─────► 5 MEDICIÓN
 yt-dlp        Claude +        guion → voz (ElevenLabs)    TikTok: a mano        registro.csv
 4 cuentas     playbook        → video (HeyGen o real)     IG/YT/LinkedIn:       48 h y 7 días
 [ANDA]        [LISTO]         [falta gemelo + E002]       Buffer Free [llave]   [plantilla]
    ▲                                                                                │
    └──────────────────────── revisión del lunes (1 decisión) ◄─────────────────────┘
```

## 3. Dónde estamos (verificado el 6 y 7 de octubre)

### PRs

| PR | Qué | Estado |
|---|---|---|
| Picado80/kennethpicado#1 | Toda la carpeta `marca/` | **mergeado** en main |
| Picado80/kennethpicado#2 (`claude/marca-voz-y-radar`) | Radar honesto (`9910b22`) | **mergeado** en main el 6-oct a las 18:05. El commit `25845c6` (4 cuentas, Buffer en lugar de Postiz, ficha de Buffer, primera tabla del radar) se hizo 7 minutos después y **quedó fuera de main** |
| Picado80/kennethpicado#3 | Este PUENTE.md + `25845c6` | **mergeado el 7-oct en `claude/marca-voz-y-radar`, no en main.** Lo lleva a main el PR nuevo de `claude/personal-brand-video-strategy-j90cvq` (con VENTA.md, guiones 003-005 y el script de Buffer) |
| Picado80/torre#45 | Fichas de HeyGen y ElevenLabs, verificador #95, radar #96 | **mergeado** |
| Picado80/torre#46 (`bookkeeping/20261007-buffer-marca`) | Ficha de `BUFFER_API_KEY`, ledger del 07-oct, evento `decision` | **borrador abierto**, CI verde |

### Llaves (en `C:\Users\Picado\torre\.env`; nunca se imprimen, como mucho el largo y los últimos 4)

| Llave | Estado |
|---|---|
| `HEYGEN_API_KEY` | verificada (largo 54). La API v3 responde: 20 avatares. La v2 se apaga el 2026-10-31 |
| `ELEVENLABS_MARCA_API_KEY` | verificada (largo 51). Aparte de la `ELEVENLABS_API_KEY` de Semi: **nunca pisar esa**. La API dice plan **creator** (0 de 186.000 caracteres usados) |
| `BUFFER_API_KEY` | **verificada el 7-oct** con `scripts\buffer-canales.ps1` (largo 43): la cuenta responde, 1 organización. **Conectados:** Instagram profesional y TikTok (@picado80). YouTube **no es prioridad** (Kenneth, 7-oct): lo crea cuando pueda. Hoy importan Instagram y TikTok |

### Voz

- El clon de Kenneth es **profesional** (categoría `professional`, no `cloned`). Por eso
  `probar-voz.ps1` sin `-VozId` no lo encuentra.
- Voz **«Picado»**, ID `jntdbfQTWPMmzXt1UxCu`. El mp3 de prueba quedó en `marca\salidas\prueba-voz-*.mp3` (no va a git).
- **Kenneth confirmó el 7-oct que suena a él.** El ID está en `config\estudio.json` → `elevenlabs.voz_kenneth`.
- **El gemelo ya existe:** avatar «Kenneth GP» en HeyGen (creado el 6-oct, 11 looks), en
  `config\estudio.json` → `heygen.avatar_id`. Kenneth pregunta por qué grabar si ya hay gemelo y voz:
  choca con `CANON.md` (cara real hasta el video 15). Decisión suya, §7.

### Radar

- Anda con cuentas. Primera tabla en `semanas\2026-S41-radar.md`: tres videos de @ia_hipster, de 239.800, 174.500 y 22.900 vistas.
- **Los hashtags de TikTok están rotos en yt-dlp 2026.08.19** («No working app info is available»).
  Desde el 6-oct, `radar.py` lo reporta como FALLA en vez de «ok 0».
- `fuentes.json` tiene 4 cuentas: `dotcsv`, `javadex`, `iaempresa`, `ia_hipster`.
  - **Ojo:** `iaempresa` e `ia_hipster` son estilo «fábrica de videos con IA», que es justo lo
    contrario de la marca. Sirven para estudiar ganchos, no como modelo.
  - Hay candidatas que yt-dlp no lee (error «secondary user ID»): `iafacil.es`,
    `automatiza_tu_vida`, `ia_productividad`, `techconpaula`, `prompt_master`.
  - yt-dlp no da número de seguidores (`channel_follower_count` = None).
- Cookies: Chrome queda bloqueado en Windows y Edge falla con DPAPI. **Firefox descifra.** Si
  TikTok pide sesión: `--cookies-from-browser firefox`.

### Publicación (decidido el 7-oct)

- **Buffer Free, $0:**
  - 3 canales: Instagram (cuenta profesional), TikTok y YouTube. LinkedIn después (decisión del 7-oct).
  - 10 publicaciones programadas por canal a la vez.
  - API con 250 llamadas al día y 3.000 al mes. **No trae MCP**, así que el conector de claude.ai no sirve: se usa la API desde la PC.
  - **Endpoint confirmado en developers.buffer.com:** `POST https://api.buffer.com` (GraphQL) con `Authorization: Bearer`. Primero `account { organizations { id } }`, después `channels(input: { organizationId })`. `publish.buffer.com/graphql`, el que dio 400, no es la API.
- **TikTok se sube a mano** desde el celular los primeros 30 videos, por los sonidos en tendencia.
- **Medición de TikTok:** Composio free (lista los videos con vistas, likes, comentarios y
  compartidos) cuando haya videos publicados. La retención sigue saliendo solo de TikTok Studio.
- **Descartados, con precios del 7-oct:**
  - Postiz: $29 al mes.
  - Post Bridge: $29 + $5 de API.
  - Buffer Essentials: $6 por red.
  - Publora: $4 a $6 por red.
  - Upload-Post: el plan gratis no tiene TikTok.
  - Zernio: $6 por cuenta.
- **Idea pendiente para los $5-10 que sobran:** promocionar en TikTok el video ganador de la semana entre dueños de negocio en Costa Rica.

### Sesiones y máquinas

- **Remote Control en la PC:** entorno bridge `kennethpicado` (`env_01Xfj5Cr8iKDyRoQYA7jVUSD`),
  modo same-dir. Hay que dejar abierta la ventana de PowerShell donde corre `claude remote-control`.
- **Sesión «Marca personal: voz y radar»** (`session_014Pr1ea7kTxNkdqifhv9HBJ`): corre en la PC,
  hizo el PR #2 y es la que puede seguir sin pasos nuevos.
- **La sesión de la nube** (la que escribió esto) queda sin trabajo de marca. Su recordatorio
  automático quedó cancelado.

## 4. Lo que la nube NO puede hacer (y por qué se pasa todo a la PC)

| No puede | Por qué |
|---|---|
| Llamar a TikTok, HeyGen, ElevenLabs, Buffer, Composio, Postiz o Publora | El proxy del entorno bloquea esos dominios |
| Leer `torre\.env` ni tocar archivos de la PC | El contenedor no ve la PC |
| Usar Desktop Commander, Chrome ni las cookies del navegador | Corren en el contenedor, no en la PC |
| Despachar a MiniMax o Kimi | `despachar.ps1` corre en la PC |
| Hacer que la sesión de la PC actúe sobre llaves o el .env | El guardia del modo auto de la PC frena lo que pide otra sesión: solo actúa si Kenneth lo pide ahí |

Se podría arreglar en parte con dominios permitidos y variables de entorno en el entorno «Marca
Personal», pero duplicaría las llaves fuera de `torre\.env`. **Decisión: la marca se trabaja desde la PC.**

## 5. Lo que hace falta en la PC para trabajar sin trabas

1. **Abrir Claude con la cuenta de claude.ai, no con una llave de API.** Los despachos de TORRE a
   MiniMax o DeepSeek dejan `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL` y `ANTHROPIC_MODEL` en la ventana.
   En una ventana nueva no están. Si aparecen: `Get-ChildItem Env:ANTHROPIC_*, Env:CLAUDE_CODE_* | Remove-Item`.
2. **Abrirlo dentro de la carpeta:** `cd C:\Users\Picado\kennethpicado; claude`. La primera vez
   pide aceptar la carpeta como confiable.
3. **Si dice «OAuth access token has expired»:** escribir `/login` dentro de Claude.
4. **Remote Control** (para manejarlo desde el celular): `claude remote-control` **en PowerShell,
   no dentro de Claude**, desde la carpeta del proyecto. Se elige `1` (same-dir).
5. **Ya instalado y probado:** Python 3.14 (`C:\Users\Picado\AppData\Local\Programs\Python\Python314`),
   yt-dlp 2026.08.19 (`python -m pip install -U yt-dlp`) y Firefox para las cookies.
6. **Los .ps1 van solo en ASCII** (PowerShell 5.1 lee cp1252). Se corren con `powershell -ExecutionPolicy Bypass -File …`.
7. **La TORRE de la PC tiene el árbol sucio:** 88 eventos sin commitear y 14 archivos de otras
   sesiones, en la rama de un cierre anterior (`cierre-fotobooth-20260827`). **No commitear trabajo
   ajeno.** La entrada de ledger y el evento de la sesión de la PC quedan en disco hasta que la
   sesión que cierre TORRE los suba.
8. **El hook de inicio de TORRE puede inyectar un puente de otro proyecto** (`handoffs\PUENTE.md`,
   de Codex). No es de la marca: ignorarlo para este trabajo.

## 6. Lo que no funcionó (no repetir)

| Intento | Por qué no funcionó |
|---|---|
| Radar con Apify | Cuenta bloqueada por la factura impaga #202606070150 ($29.07). Kenneth la deja para otro día |
| Despachar E001 a MiniMax (dos veces) | La primera arrancó de un commit viejo (sin `git pull`); la segunda no dejó proceso vivo. Lo hizo Claude, con evento `excepcion` en TORRE |
| HeyGen con la API v2 | 401 legacy: se usa la **v3** (`/v3/users/me`, `/v3/avatars`) |
| Llave de HeyGen con texto pegado | Se copió el «← para los scripts» de un ejemplo del chat. **Nunca dar ejemplos de .env con anotaciones en la misma línea** |
| Árbol sucio por `.pytest_cache` | El despacho no arrancaba. Ya está en `.gitignore` |
| Hashtags en el radar | Extractor roto en yt-dlp (ver §3) |
| `probar-voz.ps1` sin `-VozId` | Busca un clon «instantáneo» y el de Kenneth es profesional |
| Buffer por MCP o conector | El plan Free no trae MCP |
| Arrancar Remote Control | Cuatro tropiezos en cadena: `ANTHROPIC_AUTH_TOKEN` cargado; correrlo en `C:\Users\Picado`, que no es confiable; escribirlo dentro de Claude con el OAuth vencido; pegar el `PS C:\…>` del prompt junto con el comando |
| Pedirle a la sesión de la PC que edite el .env o use la llave de Buffer | El guardia la frena por venir de otra sesión. **Kenneth tiene que pedirlo él, en esa sesión** |

## 7. Lo que espera una decisión de Kenneth

1. ~~La voz del mp3~~: confirmada el 7-oct. ~~¿Gemelo o cara real?~~ **Decidido el 7-oct: cara real
   del video 1 al 15**, como dice `CANON.md`. Kenneth graba.
2. ~~Verificar Buffer~~: hecho el 7-oct. Instagram y TikTok conectados, que es lo que importa hoy. YouTube cuando Kenneth pueda; LinkedIn, después.
   **No volver a preguntarle por las voces de los personajes:** se diseñan en ElevenLabs al editar *La Oficina* (su voz no se toca).
3. **Las cuentas de referencia del radar:** tachar o sumar sobre las 4 de `fuentes.json`. Lo ideal
   son personas que le hablen de IA a dueños de negocio en español, no fábricas de contenido.
4. **El Episodio 0** («$100 y 30 días»): sí o no.
5. **El gemelo de HeyGen:** grabar 2 minutos a cámara y el consentimiento.
6. **Los PRs:** Kenneth autorizó el 7-oct subir y mergear a main lo de esta rama (el #3 ya entró a
   `claude/marca-voz-y-radar`). Queda Picado80/torre#46.
7. **El gasto:** confirmar los planes reales. La API de ElevenLabs dice **creator**, no Starter; el
   plan de HeyGen no está confirmado; Buffer, yt-dlp y Composio cuestan $0. Que no pase de $100 al mes.
8. **El sitio en inglés:** la bio de TikTok manda a `kennethpicado.vercel.app`, que está en inglés,
   y el público del video es tico. ¿Una página en español para ese tráfico? (`VENTA.md` §Lo que falta).

## 8. Siguientes encargos (en orden)

- **E002 · Producción** (cuando haya voz confirmada y gemelo):
  - Guion con `plantillas\guion.md`.
  - Audio con el clon: `eleven_v4`, voz `jntdbfQTWPMmzXt1UxCu`, `POST /v1/text-to-speech/{voz}`.
  - Video con el gemelo: HeyGen API v3. **Leer `https://developers.heygen.com/llms.txt` antes de escribir nada.**
  - Sale un mp4 en `marca\salidas\`.
  - Se despacha a un ejecutor según `router\RUTEO.md`. Claude audita el diff.
- **E003 · Publicación:**
  - Script que programe en Buffer (IG Reels, TikTok, YouTube Shorts) con caption y etiqueta de IA, **solo con la aprobación de Kenneth**.
  - TikTok se sigue subiendo a mano.
- **E004 · Medición:**
  - Números al `medicion\registro.csv` a las 48 h y a los 7 días.
  - TikTok por Composio free; el resto por la analítica de Buffer o de cada red.
  - El lunes sale una sola decisión.
- **Radar fijo:** cada lunes, `python marca\radar\radar.py` (con `--cookies-from-browser firefox` si
  hace falta) y 5 ideas puntuadas nuevas en `ideas.md`.

## 9. Siguiente paso exacto

> Mandarle a Kenneth **un solo mensaje** con dos preguntas: «¿Suena a vos el mp3 de
> `marca\salidas\`?» y «¿Verifico Buffer?». Con sus dos respuestas, guardar el ID de la voz, listar
> los canales de Buffer y seguir con E002.
