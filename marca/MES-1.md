# Mes 1 — el plan y el calendario (30 días = los 30 días del reto)

> Kenneth (19-oct-2026): «generemos toda la estrategia del primer mes y el calendario de contenido, y pensemos en lo
> que está pasando cada día, lo que pasa cada semana y cosas nuevas que llamen la atención: noticias,
> actualizaciones, pruebas».
> **Manda [`ESTRATEGIA.md`](ESTRATEGIA.md).** Este archivo la baja a 30 días. Si chocan, gana la estrategia.

**Fechas:** el Día 1 es el día en que Kenneth diga «arranca». En la consola va provisional el **miércoles 21 de
octubre**, y el Día 30 cae el **jueves 19 de noviembre**. Si arranca otro día, todo se corre igual.

## 1. La meta del mes

| | |
|---|---|
| **La que manda** | Seguidores nuevos por semana, TikTok + Instagram. El Día 1 fija la vara y cada semana tiene que traer más que la anterior |
| **La que decide qué se repite** | Seguidores por cada 1.000 vistas, por serie y por tipo de pieza |
| **El reto público** | «Mi oficina de siete IAs tiene que conseguirme 10.000 seguidores en 30 días. Yo solo apruebo.» Es una meta muy alta para la cuenta de hoy (576 seguidores en Instagram, 326 vistas por video en TikTok): **lo que se vende es la historia, no la cifra.** Llegue o no, el Día 30 se cuenta igual y el contador nunca se infla |
| **Para el mes 2** | Saber qué serie y qué tipo de pieza hace seguir, con números de la cuenta |

Cada pieza declara qué paso de la cadena mueve: **ver → reaccionar → pasarlo → conocerte → seguir** (`ESTRATEGIA.md` §1).

## 2. Lo que pasa cada día

| Hora | Qué | Quién |
|---|---|---|
| 7:00 | **Radar y noticias:** lo que está creciendo afuera (`radar/`) y las noticias de IA del día, en las fuentes originales (§5) | Claude |
| 8:00 | **El número del día:** los seguidores de TikTok e Instagram para el contador del reto | Kenneth, hasta que las cuentas estén conectadas (§9) |
| 9:00 | Se terminan las 3 piezas de volumen del día. Las del lote ya están aprobadas; la de noticias se aprueba ese día con un sí en la consola | Claude hace, Kenneth aprueba |
| 12:00 a 13:00 o 19:00 a 21:00 | **Se publica.** TikTok lleva las 3 de volumen. Instagram, la de volumen que mejor le fue ayer en TikTok, más las insignias | A mano hasta que esté el script de Buffer |
| A las 48 h y a los 7 días | Se leen los números de cada pieza y se cargan en la consola | Claude |

**Las 3 piezas de volumen de cada día:**
1. **V1 · El reto:** «Día N de 30». Un loop del contador o una imagen con lo que hizo la oficina. Paso: **seguir**.
2. **V2 · La pieza del día de la semana** (§3): una palabra de IA, una regla, la noticia, la prueba o una fecha del mes.
3. **V3 · La que provoca o se guarda:** una postura, una pregunta, una lista, un número o una voz sobre animación.

## 3. Lo que pasa cada semana (siempre igual)

| Día | V1 · el reto | V2 | V3 | Insignia |
|---|---|---|---|---|
| **Lunes** | Imagen: lo que decidió la oficina | **La regla** | **Pregunta** que obliga a tomar partido | — |
| **Martes** | Loop del contador | **La noticia de la semana, sin jerga** | **Postura** que divide | — |
| **Miércoles** | Loop del contador | **IA sin jerga** (pizarra) | Voz sobre animación (*Amazon en la soda*) | **Sí** |
| **Jueves** | Loop: lo que se probó | **La prueba** de la oficina | **El número** | — |
| **Viernes** | Imagen: el comentario que se va a probar | **3 noticias en 30 s** | **La lista** (carrusel) | Una semana sí y otra no |
| **Sábado** | Loop del contador | **La regla** o la **fecha del mes** | **Respuesta a un comentario** | — |
| **Domingo** | Loop: resumen de la semana | **Lo personal** (Kenneth) | **La mejor respuesta** de la semana | Una semana sí y otra no |

**Lo que pasa fuera de la pantalla, cada semana:**
- **Lunes, 30 minutos:** la revisión de `ESTRATEGIA.md` §8, con una sola decisión anotada en `semanas/`. Se impulsa con $5
  la pieza que más seguidores trajo.
- **Martes y viernes:** las noticias.
- **Jueves:** sale la prueba que la oficina hizo en la semana.
- **Domingo en la noche:** Kenneth aprueba el lote de la semana siguiente (un solo guion gráfico con las 21 piezas).

## 4. Las series del mes

| Serie | Qué es | Paso | Formato | Cada cuánto |
|---|---|---|---|---|
| **Reto · Día N de 30** | El contador real, lo que intentó la oficina, lo que falló y el comentario que se va a probar | Seguir | Loop de 3 a 8 s o imagen | Todos los días |
| **La noticia sin jerga** *(nueva)* | Una noticia de IA de la semana contada para un dueño de negocio: qué pasó, qué te cambia y qué no | Pasarlo | Voz sobre animación, 20 a 30 s | Martes |
| **3 noticias en 30 s** *(nueva)* | Las tres de la semana que le importan a un negocio, con fuente y fecha en pantalla | Ver | Voz sobre animación | Viernes |
| **La prueba** *(nueva)* | La oficina prueba algo de verdad y se muestra el resultado tal como salió | Pasarlo | Voz sobre la pantalla real | Jueves |
| **IA sin jerga** | Una palabra de IA como se la explicarías a tu tía | Ver | Pizarra (`produccion/j1/`) | Miércoles |
| **La regla** | Las reglas de la oficina, en 20 s | Pasarlo | Motion graphics | Lunes y sábado |
| **La lista** | Listas que se usan mañana | Pasarlo | Carrusel | Viernes |
| **El número** | Un dato real del CV o de un caso | Conocerte | Imagen | Jueves |
| **Postura y pregunta** | Opiniones que dividen y preguntas de sí o no (`ESTRATEGIA.md` §5) | Reaccionar | Imagen | Lunes y martes |
| **Respuesta a un comentario** y **la mejor respuesta** | La audiencia se ve en pantalla | Reaccionar | Voz o imagen | Sábado y domingo, desde la semana 2 |
| **Amazon en la soda** | El 002 en tres escenarios (cafetería, restaurante, emprendedor) y después A3, A4 y A5 | Pasarlo | Voz sobre animación | Semana 1 y miércoles |
| **Fecha del mes** | Lo que está pasando ese día, cuando sirve a la marca (§6) | Ver o reaccionar | Motion graphics | Cuando hay fecha |
| **Lo personal** | Fórmula 1, familia, cine | Conocerte | Video de Kenneth | Domingo |

**Las 4 pruebas del mes** (se hacen de verdad con la oficina de TORRE, $0):
1. **3 IAs de la oficina, el mismo pedido vago y después completo** (jueves de la semana 1). Muestra el `J1` funcionando.
2. **¿Una IA puede contar el inventario de una soda con una foto?** (semana 2). Con una foto real y su permiso.
3. **Le pedí a la oficina el manual de apertura de una cafetería** (semana 3). Conecta con el `002b`.
4. **La que pidieron en los comentarios** (semana 4): la tarea más votada en la pregunta del lunes 9.

## 5. Las noticias: cómo se eligen y se verifican

- **El filtro:** ¿le cambia algo esta semana a alguien que dirige un negocio en Costa Rica? Si no, no entra.
- **Siempre de la fuente original:** el blog o el anuncio de la empresa. Los boletines y resúmenes solo sirven para enterarse.
- **En pantalla:** la fuente y la fecha. Ningún número que no esté en la fuente.
- **Nunca:** política, rumores ni «se filtró». Nada que nombre a SEMI o venda algo.
- **Si en la semana no hay una noticia que pase el filtro,** ese lugar lo toma una pieza del banco (`CALENDARIO.md`).
- **Las semanas con eventos ya tienen dónde mirar** (§6): GitHub Universe, Web Summit, Adobe MAX y Microsoft Ignite.

## 6. Lo que pasa en el mundo este mes

Fechas revisadas el 19-oct en las fuentes de abajo; se confirman en el sitio oficial antes de usarlas en un video.

| Fecha | Qué | Cómo entra |
|---|---|---|
| 23 al 25 de octubre | GP de Fórmula 1 en Austin | `F1A`: «Un pit stop dura 2 segundos porque nadie es indispensable» (sábado 24) |
| 28 y 29 de octubre | GitHub Universe, en San Francisco | Mira de noticias para el viernes 30 |
| 30 de octubre al 1 de noviembre | GP de México | El video personal de Kenneth (domingo 1) |
| **31 de octubre** | **Día de la Mascarada Tradicional Costarricense** y Halloween | `HAL`: «Lo que de verdad asusta en un negocio: que todo dependa de vos», con mascaradas de papel y con respeto |
| 1 y 2 de noviembre | Día de Todos los Santos y Día de los Difuntos | No se usa: no es tema para la marca |
| 6 al 8 de noviembre | GP de São Paulo | Puede ser el video personal |
| 9 al 12 de noviembre | Web Summit, en Lisboa | Mira de noticias para el martes 10 |
| 10 al 12 de noviembre | Adobe MAX, en Miami Beach | Ídem |
| 17 al 20 de noviembre | Microsoft Ignite, en San Francisco | Mira de noticias para el martes 17 |
| 19 al 21 de noviembre | GP de Las Vegas | Cae en el Día 30 |
| 27 de noviembre | Black Friday | La última semana lo prepara sin vender: `Q4` «¿Tu negocio aguanta un día de locos sin vos?» y `L5` |

En noviembre no hay feriados nacionales en Costa Rica.

## 7. Las 12 insignias del mes

| Día | Insignia | Paso |
|---|---|---|
| 1 | `G0` El gemelo se presenta y lanza el reto | Seguir |
| 3 | `002` Si tu negocio no sobrevive a tus vacaciones, con el gancho nuevo | Pasarlo |
| 5 | `001` Mi empleado se calificó su propio examen | Reaccionar |
| 8 | `003` Le prohibí trabajar a mi mejor empleado | Pasarlo |
| 10 | `AMX` El escenario de *Amazon en la soda* que va ganando, con Kenneth | Pasarlo |
| 12 | `004` Un anfiteatro para 800 personas al 25 % | Pasarlo |
| 15 | `DIA15` Mitad del reto | Seguir |
| 17 | `005` La oficina me avisó tres veces | Reaccionar |
| 19 | `TOP1` La pieza de volumen que más seguidores trajo, con Kenneth | Seguir |
| 22 | `O6` Cuando el gerente se queda sin horas, ¿quién manda? | Reaccionar |
| 26 | `TOP2` La segunda que más seguidores trajo, con Kenneth | Seguir |
| 30 | `DIA30` ¿Llegamos? Se cuenta igual | Seguir |

Cada una pasa por guion gráfico y prueba de gancho (70 / 60 / 90) antes de gastar en el gemelo. Si no llega, se rehace
el gancho, que es barato.

## 8. Cómo se decide en el mes

| Cuándo | Qué se decide |
|---|---|
| Cada lunes (días 6, 13, 20 y 27) | La revisión de `ESTRATEGIA.md` §8: qué serie se duplica, cuál cambia de gancho, qué paso se trabaja y qué pieza se impulsa |
| Día 9 | El escenario de *Amazon en la soda* que va con el gemelo el Día 10 |
| Día 15 | La mitad del reto: qué series siguen en la segunda mitad |
| Domingos (días 5, 12, 19 y 26) | Kenneth aprueba el lote de la semana siguiente |
| Día 30 | El cierre: seguidores ganados, qué convirtió y el plan del mes 2 |

**Reglas que corren solas:** 5 piezas de una serie por debajo de la mitad del promedio → se le cambia el gancho; 10 → se
mata. Después de 30 piezas de volumen sin rechazos, el volumen se publica sin pedir permiso.

## 9. Las cuentas: qué se lee solo y qué no

- **Buffer ya está conectado** a TikTok e Instagram y, por su API, da los números de **cada publicación**, aunque se
  haya subido a mano: vistas, alcance, me gusta, comentarios, compartidos y, en TikTok, el tiempo visto (revisado el
  19-oct). Eso alcanza para leer la cadena pieza por pieza.
- **Lo que Buffer no da: el total de seguidores** de la cuenta, y es el número que manda y el del contador. Para leerlo
  solo hay que conectar las APIs oficiales, que son gratis:
  - TikTok: una app de desarrollador (developers.tiktok.com) con permiso de estadísticas del usuario.
  - Instagram: una app de Meta (developers.facebook.com) con la API de Instagram, que también da los seguidores que
    trajo cada publicación y las visitas al perfil.
  - Crear las dos cuentas de desarrollador le toca a Kenneth. Lo demás lo arma Claude.
- **Mientras tanto,** Kenneth pasa los dos números cada mañana (TikTok Studio e Instagram): 30 segundos.
- **Facebook** entra como tercera red de Buffer cuando exista la página «Kenneth Picado».

## 10. El presupuesto del mes

| Rubro | Costo |
|---|---|
| Volumen: 90 piezas | $0 |
| Insignias: 12, a unos $3 | unos $36 |
| Voz clonada (ElevenLabs, plan fijo) | $22 |
| Impulso: la pieza que más seguidores trajo cada semana, $5 × 4 | $20 |
| **Total** | **unos $78**, bajo el tope de $100 |

HeyGen tiene $2.88: hay que cargar unos $40 antes del Día 1.

## 11. Si el reto es que no

El lugar de V1 lo toma **La bitácora de la oficina**: el mismo formato diario sin la meta de los 10.000 (qué hizo la
oficina hoy, qué falló, qué se prueba mañana). `G0`, `DIA15` y `DIA30` se cambian por insignias del banco
(`CALENDARIO.md`). Todo lo demás del mes queda igual.

## 12. El calendario, día por día

Lo mismo está en la consola, como calendario. Se genera con `python marca/consola/sembrar.py`.

| Día | Fecha | V1 · el reto | V2 | V3 | Insignia |
|---|---|---|---|---|---|
| 1 | Mié 21 oct | `D1` El contador en el número real | `J1` «Prompt» son las instrucciones que le di | `P1` Si tu negocio no sobrevive a tus vacaciones, no es un negocio | `G0` El gemelo se presenta y lanza el reto (Día 1) |
| 2 | Jue 22 oct | `D2` El plan de la oficina: quién hace qué | `PR1` 3 IAs de la oficina: el mismo pedido vago y después completo | `002b` Si tu cafetería recién abierta no sobrevive a tus vacaciones | — |
| 3 | Vie 23 oct | `D3` El contador y lo que falló | `RN1` Las 3 noticias de IA de la semana | `L1` La reunión de los lunes en 15 minutos | `002` Si tu negocio no sobrevive a tus vacaciones (con el gancho nuevo) |
| 4 | Sáb 24 oct | `D4` El comentario que se va a probar | `F1A` Un pit stop dura 2 segundos porque nadie es indispensable | `002c` Si tu restaurante recién abierto no sobrevive a tus vacaciones | — |
| 5 | Dom 25 oct | `D5` Resumen de los primeros 5 días | `PER1` Video personal | `Q1` ¿Le darías la caja a una IA? Sí o no. | `001` Mi empleado se calificó su propio examen |
| 6 | Lun 26 oct | `D6` Lo que decidió la oficina el lunes | `R2` Un sistema que te necesita es una dependencia | `002d` Si acabás de emprender y tu negocio no sobrevive a tus vacaciones | — |
| 7 | Mar 27 oct | `D7` El contador | `NS1` La noticia de la semana, sin jerga | `P2` Tu mejor empleado es el que menos debería hacer | — |
| 8 | Mié 28 oct | `D8` El contador: una semana | `J2` Un «agente» es un empleado de IA | `N2` 800 personas de capacidad, 25 % de uso | `003` Le prohibí trabajar a mi mejor empleado |
| 9 | Jue 29 oct | `D9` El contador y lo que se probó | `PR2` ¿Una IA puede contar el inventario de una soda con una foto? | `N1` 165 personas, 4 países | — |
| 10 | Vie 30 oct | `D10` El comentario que se va a probar | `RN2` Las 3 noticias de IA de la semana | `L2` Las 3 cosas que solo vos sabés | `AMX` El escenario que va ganando, ahora con Kenneth |
| 11 | Sáb 31 oct | `D11` El contador | `HAL` Lo que de verdad asusta en un negocio: que todo dependa de vos | `RC1` Respuesta a un comentario | — |
| 12 | Dom 1 nov | `D12` Resumen de la semana 2 | `PER2` Video personal | `MR1` La mejor respuesta de la semana | `004` Un anfiteatro para 800 personas al 25 % |
| 13 | Lun 2 nov | `D13` Lo que decidió la oficina el lunes | `R1` El que hace el trabajo no lo revisa | `Q2` ¿Qué tarea de tu negocio le darías mañana a una IA? | — |
| 14 | Mar 3 nov | `D14` El contador | `NS2` La noticia de la semana, sin jerga | `P3` La IA no te va a quitar el trabajo: te lo va a quitar el compañero que la usa | — |
| 15 | Mié 4 nov | `D15` Mitad del reto: cuánto falta | `J3` Un «modelo» es una IA | `A3` La reunión de los lunes | `DIA15` Mitad del reto: cuánto llevamos y qué cambió |
| 16 | Jue 5 nov | `D16` El contador y lo que se probó | `PR3` Le pedí a la oficina el manual de apertura de una cafetería | `N4` 12 semanas, sin contratar a un gerente | — |
| 17 | Vie 6 nov | `D17` El comentario que se va a probar | `RN3` Las 3 noticias de IA de la semana | `L3` Apertura y cierre del local | `005` La oficina me avisó tres veces |
| 18 | Sáb 7 nov | `D18` El contador | `R5` Nada se hace dos veces | `RC2` Respuesta a un comentario | — |
| 19 | Dom 8 nov | `D19` Resumen de la semana 3 | `PER3` Video personal | `MR2` La mejor respuesta de la semana | `TOP1` La pieza de volumen que más seguidores trajo, ahora con Kenneth |
| 20 | Lun 9 nov | `D20` Lo que decidió la oficina el lunes | `R6` Lo que no se escribe no pasó | `Q3` ¿Cuál es la tarea que más odiás de tu negocio? La oficina prueba la más votada | — |
| 21 | Mar 10 nov | `D21` El contador | `NS3` La noticia de la semana, sin jerga | `P4` Si tenés que estar para que funcione, no lo construiste: lo cargás | — |
| 22 | Mié 11 nov | `D22` El contador: faltan 8 días | `J4` Un «workflow» es la cadena de pasos | `A4` Escribí el titular del día en que ya lo lograste | `O6` Cuando el gerente se queda sin horas, ¿quién manda? |
| 23 | Jue 12 nov | `D23` El contador y lo que se probó | `PR4` La prueba que pidieron en los comentarios | `N3` 14 años en una operación que no se apagó | — |
| 24 | Vie 13 nov | `D24` El comentario que se va a probar | `RN4` Las 3 noticias de IA de la semana | `L4` Lo que tu negocio tiene que saber hacer sin vos | — |
| 25 | Sáb 14 nov | `D25` El contador | `R7` La tabla decide quién trabaja, no el capricho | `RC3` Respuesta a un comentario | — |
| 26 | Dom 15 nov | `D26` Resumen de la semana 4 | `PER4` Video personal | `MR3` La mejor respuesta de la semana | `TOP2` La segunda pieza que más seguidores trajo, ahora con Kenneth |
| 27 | Lun 16 nov | `D27` Lo que decidió la oficina para el cierre | `J5` Los «tokens» son horas de trabajo | `Q4` ¿Tu negocio aguanta un día de locos sin vos? | — |
| 28 | Mar 17 nov | `D28` El contador: faltan 3 días | `NS4` La noticia de la semana, sin jerga | `L5` Para un día de locos: 5 cosas que se dejan escritas | — |
| 29 | Mié 18 nov | `D29` El contador: faltan 24 horas | `J6` El «handoff» es la nota de relevo | `A5` Una evaluación que no dispara nada no sirve | — |
| 30 | Jue 19 nov | `D30` El número final | `FIN` Lo que aprendió la oficina en 30 días, en 30 segundos | `RC4` Respuesta a un comentario | `DIA30` Día 30: ¿llegamos? Se cuenta igual |

**Las piezas del reto** (`D1` a `D30`, `FIN`, `G0`, `DIA15` y `DIA30`) esperan el sí de Kenneth (§11).

### Fuentes de las fechas (§6)

- Fórmula 1: [Formula 1 reveals calendar for 2026 season](https://www.formula1.com/en/latest/article/formula-1-reveals-calendar-for-2026-season.YctbMZWqBvrgyddrnauo8).
- GitHub Universe: [GitHub Universe 2026](https://gracker.ai/events/github-universe-2026/).
- Web Summit: [Web Summit 2026 Lisbon](https://websummit.bnetwork.com/Home/AboutTheEvent).
- Adobe MAX: [Adobe MAX 2026, Miami Beach](https://www.miamiandbeaches.com/event/adobe-max-2026/39729).
- Microsoft Ignite: [Microsoft Ignite 2026](https://www.uctoday.com/events/microsoft-ignite-2026/).
- Día de la Mascarada: [Teletica, 31-oct-2025](https://www.teletica.com/entretenimiento/dia-de-la-mascarada-costarricense-una-herencia-viva-de-color-humor-y-tradicion_396314).
- Feriados de Costa Rica 2026: [El Observador](https://observador.cr/estos-son-los-4-feriados-que-le-quedan-a-costa-rica-en-el-2026-solo-2-son-de-pago-obligatorio/).
