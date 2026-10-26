# El radar diario y las carpinterías

> La parte de la marca que **busca formatos virales y los vuelve copiables**.
> Lo que se arma aquí es el insumo de `estrategia` → `guionista` → la Sala.

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| `radar.py` | El radar **semanal** de TikTok que ya existía. No se toca. Sigue corriendo el lunes. |
| `diario.py` | El radar **diario** multi-red. Barre TikTok, Instagram, X y YouTube Shorts y deja el digest de una pantalla. |
| `redes.py` | La capa de captura: una función por red, con su camino propio. |
| `chrome.py` | Chrome headless, para las redes que no se leen con yt-dlp (Instagram y X). |
| `fuentes.json` | De dónde se barre: las cuentas por red y los umbrales. |
| `carpinterias/` | El modelo, el catálogo y las reglas de tropicalización. Ver `carpinterias/CARPINTERIA.md`. |
| `hoy.md` | El digest de la mañana. Lo escribe `diario.py`. |
| `salidas/` | Todo lo crudo: JSON, cuadros, perfiles de Chrome. **Git lo ignora.** |

## Las dos corridas

```
diario.py   (cada mañana, 5 a. m.)  ->  hoy.md + salidas/AAAA-MM-DD.json
radar.py    (cada lunes)            ->  semanas/AAAA-SNN-radar.md
```

El diario es el que mira **más redes y más seguido**. El semanal sigue ahí porque el lunes se lee con calma.

## La doble pasada

Es lo que Kenneth pidió el 25-oct: no mirar todo a fondo, porque eso no se puede todos los días.

1. **Pasada barata:** se barren todas las cuentas de todas las redes y se traen los metadatos.
   Cientos de videos, pocos segundos cada uno.
2. **Pasada cara:** se ordenan por la señal y **solo los 5 primeros** se miran de verdad:
   se les baja la transcripción y se les sacan 3 cuadros con ffmpeg.

Las redes que no se pueden leer se anotan como **omitidas**, con el motivo. Nunca se inventan datos
y una red caída no tumba la corrida.

## De un video a una carpintería

El radar no entrega videos: entrega **formatos**. El agente `tendencias` convierte cada candidato
en una carpintería con ficha (`carpinterias/plantilla.md`), la tropicaliza a la marca y deja el rastro
del cambio. La definición completa está en `carpinterias/CARPINTERIA.md`.

Lo que no se puede perder: **el original y el rastro van siempre juntos**. Kenneth tiene que poder
ver el video original y decidir si nuestra versión quedó muy larga.

## Las 4 redes y cómo se leen

| Red | Cómo | Estado real (25-oct-2026) |
|---|---|---|
| TikTok | `yt-dlp` | **Operativa.** Trae vistas, likes, comentarios, compartidos, guardados, duración, fecha y texto. Es la que más aporta: su señal es % de compartidos. |
| YouTube Shorts | `yt-dlp` | **Operativa.** Trae vistas, likes, comentarios, duración, fecha y texto. Compartidos y guardados vienen en `None` (yt-dlp no los expone). |
| X | HTML público que manda el servidor | **Operativa.** Trae likes, respuestas, reposts, guardados, fecha y el texto del post. **No trae vistas**: su señal queda en 0 y el ranking usa las interacciones absolutas como segunda llave. |
| Instagram | Chrome headless, DOM público | **Operativa para formatos.** Trae el reel, su URL, la fecha y el texto. **No trae likes ni vistas** sin sesión: sirve para ver formatos nuevos, no para rankear por popularidad. |

**El navegador que sirve es el Chrome del sistema** (`C:\Program Files\Google\Chrome\Application\chrome.exe`, v155).
Los tres Chrome que dejó puppeteer se cuelgan en silencio y devuelven 0 bytes, incluso con `example.com`;
Edge responde pero su HTML de Instagram no trae los reels. Por eso `ruta_chrome()` prueba los candidatos
y se queda con el que **responde y trae los datos**, no con el más nuevo. Si algún día los Chrome de
puppeteer se arreglan, se vuelven a preferir solos, sin tocar código.

**Por qué no hay cookies:** `yt-dlp --cookies-from-browser chrome` falla con «Could not copy Chrome cookie
database» porque Chrome está abierto y bloquea su base de cookies. El sistema no depende de la sesión del
navegador de Kenneth: funciona con perfiles temporales descartables, siempre.

Cuando una red no se puede leer, el radar sigue con las demás y lo dice. Esa es la diferencia entre
un radar y una dependencia frágil.

## El ciclo que lo hace aprender

```
radar diario -> carpintería -> tropicalización -> Kenneth aprueba -> se publica
     -> medición a las 48 h y a los 7 días -> la carpintería queda funcionó / no funcionó
     -> el catálogo se reordena: lo que funcionó en NUESTRA cuenta sube
```

La agenda del mes (`carpinterias/agenda.py`) sale de ahí: primero lo que ya funcionó con nosotros.

## Correrlo

```powershell
# El barrido del día, con el digest
python marca/radar/diario.py

# Solo una red
python marca/radar/diario.py --red tiktok,youtube

# Más candidatos a fondo (más lento)
python marca/radar/diario.py --top 8

# Sin bajar video: solo metadatos, rapidísimo
python marca/radar/diario.py --sin-cuadros

# Ver qué haría, sin escribir nada
python marca/radar/diario.py --dry-run
```

Las pruebas:

```powershell
python -m pytest marca/radar -q
```

## Lo que este sistema NO hace

- **No publica nada.** Lo publica Buffer, con el sí de Kenneth en la Sala.
- **No gasta plata.** Todo va por `yt-dlp` y Chrome local. Apify quedó descartado (factura impaga).
- **No baja ni reusa videos de terceros para publicar.** Solo para analizarlos.
- **No toca las cuentas de Kenneth.** Ni las cookies del navegador, ni los perfiles.
- **No inventa números.** Lo que no se pudo leer queda en `None` y se dice.
