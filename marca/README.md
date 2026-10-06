# Marca personal — el sistema

> Esta carpeta es el sistema operativo de la marca personal de Kenneth.
> Persona TORRE: **personal**. Primero TikTok, después LinkedIn.

La marca se maneja con el mismo sistema de cinco capas que Kenneth le instala a sus clientes.
Si no corre igual cuando Kenneth está ocupado, no es un sistema: es una dependencia.

| Capa | Dónde vive |
|---|---|
| 1 · Políticas: qué somos y qué nunca hacemos | [`CANON.md`](CANON.md) · [`FORMATOS.md`](FORMATOS.md) |
| 2 · Métricas: qué se mide de cada video | [`medicion/registro.csv`](medicion/registro.csv) |
| 3 · Auditorías: control de calidad antes de publicar | la lista de QA en [`plantillas/guion.md`](plantillas/guion.md) |
| 4 · Tablero: cómo vamos | el registro + la revisión semanal |
| 5 · Revisión del lunes: qué decidimos | [`plantillas/semana.md`](plantillas/semana.md) → `semanas/` |

**La revisión del lunes alimenta el banco de ideas. El ciclo completo es el sistema.**

---

## El proceso: cinco etapas

```
 1 IDEA ──► 2 PLAN ──► 3 GENERACIÓN ──► 4 POSTEO ──► 5 MEDICIÓN
   ▲                                                     │
   └──────────────── revisión del lunes ◄────────────────┘
```

Cada etapa tiene entrada, salida y una condición para pasar a la siguiente (igual que el Flujo Cawhi).

### 1 · Idea

- **Entrada:** la bitácora real del trabajo, no la inspiración del momento.
  - `torre/protocolo/eventos.jsonl`: la bitácora de tus IAs (1.438 entradas al 6-oct-2026). Cada incidente puede ser un episodio de *La Oficina*.
  - Trabajo con clientes, siempre **anónimo** («un anfiteatro de 800 personas», nunca el nombre).
  - Comentarios y preguntas del público (después de la semana 2, la fuente principal).
  - Virales ajenos: transcribilos con ClipStep y analizalos con las 7 preguntas de `viral-content-machine/VIRAL_CONTENT_PLAYBOOK.md` §4. Se copia el mecanismo, nunca el contenido.
- **Salida:** una fila en [`ideas.md`](ideas.md) con su puntaje.
- **Condición para pasar:** **15/20 o más** (Universal · Verdad · Tensión · Puente, de 1 a 5 cada uno).

### 2 · Plan

- **Entrada:** el banco de ideas y la revisión del lunes.
- **Salida:** `semanas/AAAA-SNN.md` con los 5 videos de la semana, cada uno con formato y día.
- **Condición para pasar:** la mezcla respeta el orden de lanzamiento de `FORMATOS.md`, y nunca hay dos *Gemelos* en la misma semana.

### 3 · Generación

| Paso | Quién / con qué | Salida |
|---|---|---|
| Guion | Claude saca el borrador con [`plantillas/guion.md`](plantillas/guion.md); Kenneth lo dice en voz alta y le pone su voz | `guiones/NNN-slug.md` |
| Grabación | Kenneth, celular vertical, **un bloque semanal** (5 videos, luz de mañana) | crudos → Drive |
| Piezas con IA | ElevenLabs (voces de los personajes, voz clonada) · HeyGen (gemelo) — ver [`LLAVES.md`](LLAVES.md) | audios / clips → Drive |
| Edición | Video Pipeline (preedición local, $0) → CapCut | final 1080×1920 → Drive |
| QA | la lista del guion + skill `revisar-video` en todo lo generado | casillas marcadas |

- **Los videos no van al repo.** Van a Drive: `Marca personal/Videos/NNN-slug/` (`crudo/`, `ia/`, `final.mp4`). El repo guarda texto: guiones, registro y decisiones.
- **Condición para pasar:** todas las casillas de QA del guion marcadas.

### 4 · Posteo

- **Cuenta personal de creador en TikTok, no cuenta de empresa.** Las cuentas de empresa solo tienen la biblioteca de música comercial; perdés los sonidos en tendencia.
- **Los primeros 30 videos se suben a mano desde el celular**, para aprender la herramienta y usar texto y sonidos nativos. Cuando el formato esté estable, se programan con Postiz.
- Caption con el skill `social-copy-generator` (TikTok): gancho + 3 a 5 hashtags.
- **Si hay HeyGen o ElevenLabs en el video, se activa la etiqueta «contenido generado por IA».** Sin excepción.
- **La primera hora después de publicar:** responder cada comentario. Fijar el comentario que abre conversación.
- **Condición para pasar:** el video tiene fila en el registro, con su fecha y su URL.

### 5 · Medición

- **A las 48 horas y a los 7 días:** copiar los números de TikTok Analytics a [`medicion/registro.csv`](medicion/registro.csv), una fila por corte (`corte` = `48h` o `7d`).
- **Lunes, 20 minutos:** revisión con [`plantillas/semana.md`](plantillas/semana.md). Sale **una sola decisión**.
- **La métrica que manda:** `conversaciones con empresas por mes`. Una conversación cuenta cuando alguien que dirige o decide en un negocio te escribe por DM, correo o LinkedIn por algo que vio. Las vistas son el medio.

---

## El ritmo semanal (bloques de 5:00 AM)

| Día | Bloque | Qué |
|---|---|---|
| Lunes | 5:30–6:00 | Revisión + plan de la semana |
| Lunes | 6:00–6:45 | Guiones (Claude hace el borrador, Kenneth lo corrige) |
| Miércoles | 5:00–6:30 | Grabación en bloque |
| Jueves | 5:00–6:30 | Edición, piezas con IA, QA |
| Lunes a viernes | hora fija | Publicar + la primera hora de comentarios |

Horas de publicación para empezar: **12:00–13:00** y **19:00–21:00** (Costa Rica). Es una hipótesis: después de 3 semanas manda el dato de tu cuenta.

## Quién hace qué

- **Kenneth:** decide, graba, aprueba, responde comentarios. Nadie más publica.
- **Claude:** borradores de guion y caption, análisis del registro el lunes (pasale el CSV).
- **HeyGen / ElevenLabs:** solo lo que dice `CANON.md` §Real vs. IA.

## Después: LinkedIn

Cuando TikTok tenga 30 videos y 2 formatos validados:
1. La lección de cada *Oficina* y cada *Amazon en la soda* se convierte en un post de LinkedIn (texto + el mismo video).
2. Los 5 mejores se traducen al inglés con la traducción de video de HeyGen (tu cara y tu voz en inglés), para empresas remotas de EE. UU.
3. Al cerrar la temporada 1 (30 episodios de *La Oficina*): un artículo, *«Lo que aprendí dirigiendo siete IAs durante 30 días»*. Ese artículo es el que se le manda a una empresa.

## Mapa de la carpeta

```
marca/
├── README.md            ← estás aquí: el proceso
├── LLAVES.md            ← dónde van HeyGen y ElevenLabs (respuesta corta adentro)
├── CANON.md             ← tesis, audiencia, voz, límites, qué es real y qué es IA
├── FORMATOS.md          ← los 4 formatos y el orden de lanzamiento
├── ideas.md             ← banco de ideas con puntaje
├── config/estudio.json  ← IDs de avatar y de voces (no son secretos)
├── scripts/             ← verificar-llaves.ps1 (prueba HeyGen y ElevenLabs sin mostrar las llaves)
├── plantillas/          ← guion.md · semana.md
├── guiones/             ← un archivo por video (001, 002, …)
├── semanas/             ← una revisión y un plan por semana
└── medicion/            ← registro.csv
```
