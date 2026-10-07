# Canon de la marca personal

> Es la fuente de verdad. Ningún guion, caption ni prompt sale sin pasar por acá.

## La tesis (una línea)

> **No necesitás ser técnico para trabajar con IA. Necesitás saber dirigir.**

Es el puente de toda la marca. A la gente no técnica le da permiso («esto también es para
mí»). A las empresas les dice qué vendés sin venderlo: saber dirigir es operaciones, y
operaciones es lo que Kenneth hace.

## Quién es Kenneth en la marca

Un operador, no un programador. Catorce años en una operación de Amazon que nunca se apagó,
165 personas a cargo en cuatro países. Hoy dirige una oficina de IAs con las mismas reglas con
las que dirigía personas, y construye sistemas para negocios reales de Costa Rica.

**El ángulo que nadie más tiene:** en 2026 TikTok está lleno de «el que te enseña herramientas
de IA». Nadie muestra a un jefe con oficio dirigiendo IAs como si fueran un equipo, con
bitácora, auditorías y reglas que salieron de incidentes reales. Eso es TORRE, y ya existe.

## Las audiencias

| | Quién es | Qué quiere | Qué hace con el video |
|---|---|---|---|
| **La que mira** | Gente que trabaja: empleados, supervisores, dueños de negocio pequeño. Costa Rica y LATAM, 25 a 50 años, curiosa o asustada con la IA, nada técnica | Entender qué pasa con su trabajo y no quedarse atrás | Lo comenta, lo guarda y **se lo manda al jefe** |
| **La que compra** | Dueños y gerentes de pymes y empresas medianas en Centroamérica (Semi, Cawhi) y empresas remotas que buscan un COO fraccional (fase LinkedIn) | Que su operación funcione sin ellos encima | Visita el perfil, el sitio, escribe |

**El mecanismo puente:** el empleado es el canal de distribución hacia quien decide. Todo video
debería poder terminar en «mandáselo a tu jefe» sin que suene forzado.

## Los pilares (los formatos están en `FORMATOS.md`)

1. **Dirigir IAs.** *La Oficina*: mi equipo no es humano.
2. **Operar como Amazon, en chiquito.** *Amazon en la soda*.
3. **La prueba.** *Sistema de la semana*: problema real, solución real, en horas reales.
4. **Lo que la IA puede falsificar.** *¿Cuál soy yo?*: el gemelo, en dosis bajas.

## La voz

- Directa, calmada, con humor seco. Frases cortas. Como quien le explica algo a un colega en el parqueo.
- Español de Costa Rica, sin forzar regionalismos.
- **La energía tiene dos estados**, como en el canon de LÍA: calmado por defecto, y se acelera
  cuando habla de un sistema que corre solo. Si todo el video tiene la misma energía, no hay personaje.
- Nunca «hola chicos, bienvenidos». Se arranca con el gancho.

### Glosario anti-jerga (obligatorio)

| No decir | Decir |
|---|---|
| prompt | las instrucciones que le di |
| LLM, modelo | una IA |
| agente | un empleado de IA / una IA que trabaja sola |
| API, endpoint, repo, deploy | (no se dice; se muestra el resultado) |
| workflow, pipeline | el proceso, la cadena |
| encargo / dispatch | le pasé el trabajo |
| ledger, log, eventos.jsonl | la bitácora |
| handoff / puente | la nota de relevo |
| cuota, tokens | horas de trabajo / presupuesto |

Prueba de fuego: **¿lo entiende tu tía sin preguntarte nada?**

## Límites (nunca)

1. **Nunca se vende en el video.** Ni «agendá», ni precios, ni demos. Semi aparece como «lo
   que construyo», no como oferta, y como mucho en 1 de cada 10 videos. Lo que pasa después del
   video (LinkedIn, la conversación, la llamada y la propuesta) está en `VENTA.md`.
2. **Nunca nombres de clientes ni de personas** sin permiso por escrito. «Un anfiteatro de
   800 personas», «una cooperativa de mil empleados».
3. **Nunca una pantalla con llaves, correos, datos de clientes ni conversaciones.** Toda
   captura de la bitácora o de un sistema va difuminada. Revisá cada cuadro antes de exportar.
4. **Nunca un número inventado.** Todo dato sale del CV (`resume-optimizer`) o de TORRE. Si
   no tiene fuente, no se dice.
5. **Nunca prometer resultados** («vas a ganar», «vas a ahorrar X»).
6. **Nunca burlarse de quien no sabe de tecnología.** Esa persona es la audiencia.
7. **Nunca competir con la cuenta de Cawhi.** Cawhi (`@cawhicr.com`) cubre clima, equipos y
   ventas. Kenneth cubre dirigir con IA y operaciones. Coordinar con Bernal si un tema se cruza.

## Qué es real y qué es IA

| | Por defecto | Cuándo se usa IA | Tope |
|---|---|---|---|
| **Cara** | Real, grabada con el celular | Gemelo de HeyGen solo en *¿Cuál soy yo?* y en las traducciones al inglés para LinkedIn | 1 de cada 5 videos, y **nunca antes del video 15** |
| **Voz de Kenneth** | Real | Clon de ElevenLabs para la voz en off de *Sistema de la semana* cuando no hay tiempo de grabar | Declarado siempre |
| **Voces de las IAs** | Diseñadas en ElevenLabs | Los personajes de *La Oficina* dicen su línea | Voces sintéticas, que no imiten a nadie real |

**Por qué el gemelo no va primero:** lo que vendés es confianza. Si la cara es falsa desde el
primer día, el gemelo deja de ser una sorpresa y se convierte en una sospecha. El juego de
*¿Cuál soy yo?* solo funciona cuando el público ya conoce al Kenneth real.

**Etiqueta:** cualquier video con HeyGen o ElevenLabs se publica con la etiqueta «contenido
generado por IA» de TikTok activada. Es la norma de la plataforma y es coherente con la marca.

## El elenco de La Oficina

Sale de `torre/router/`. **El número cambia:** antes de grabar «tengo siete empleados»,
contá los carriles vivos con `verificar.ps1`.

| Personaje | Rol en TORRE | Rasgo de personaje |
|---|---|---|
| **Claude** | El cerebro: planea, decide y audita | El gerente al que le prohibí teclear. Su trabajo es pensar y revisar, no hacer |
| **Codex** («el de ChatGPT») | Manos expertas, revisión técnica | El ingeniero serio. Toma el mando cuando el gerente se queda sin horas |
| **MiniMax** | El caballo de carga, un millón de palabras de contexto | Lee un manual entero de un tirón y no se cansa. Trabaja con plan fijo |
| **Kimi** | Se alterna con MiniMax, encargo por encargo | El compañero de turno rotativo |
| **DeepSeek** | El ejecutor por encargo, cobra por palabra | El contratista: le das el plan, trabaja solo en su esquina y te entrega |
| **Grok** | La segunda opinión | Otra familia, otro sesgo: el que llamás cuando algo no te cuadra |
| **Antigravity** | Interfaz y prototipos, gratis | El practicante que hace todo bonito y cubre cuando los demás no pueden |

**Las reglas de la oficina son el contenido:** quien ejecuta no se revisa a sí mismo · nada se
crea dos veces · todo trabajo deja huella · la tabla decide quién trabaja, no el capricho. Cada
una salió de un incidente real, y cada incidente es un episodio.

## Bio de TikTok (borrador)

> Operaciones de Amazon. Una oficina de IAs. Negocios de verdad.
> No necesitás ser técnico. Necesitás saber dirigir. 🇨🇷

Enlace: `kennethpicado.vercel.app` (el portafolio, no Semi). La persona primero; Semi se descubre.
