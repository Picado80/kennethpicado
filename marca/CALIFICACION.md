# La calificación: de 0 a 100, pasa con 87

> Kenneth (24-oct-2026): «Tenemos que empezar a tener parámetros que nos determinen si algo está llegando a lo que
> necesitamos hacer, al objetivo, no solamente cuando sale, sino antes de que salga… Todos los guiones, todos los
> videos, todas las animaciones y todas las informaciones tienen que tener un buen score… se revise bien y que
> se devuelva lo que no está a la altura… El score mínimo para que sí pueda pasar es 87… Primero desarrollemos cuáles
> son los parámetros para los guiones, las ideas y los conceptos que se alineen a la estrategia madre».

> La meta de todo: **más vistas**, y que esas vistas se vuelvan seguidores (`ESTRATEGIA.md`, `IDENTIDAD.md`).

Califica el agente **auditor-calidad**, nunca el que hizo la pieza. Se califica tres veces:
- la idea, antes de escribir el guion (solo el paso 0);
- el guion, antes de mostrárselo a Kenneth en la Sala;
- el video, antes de programarlo.

## Paso 0 · ¿Se alinea con la estrategia madre?

Si falla una sola, **no se califica:** se devuelve con lo que hay que cambiar para acercarla.

1. **El tema** es dirigir la inteligencia artificial como a un colaborador: qué pedirle, cómo revisarla o cuándo no
   fiarse.
2. **Una tarea real** de la casa o del trabajo de un tico de 25 a 50 años.
3. **Una prueba real,** con el resultado guardado.
4. **Deja una regla de líder** que sale de la historia.
5. **No es nada de lo que está fuera:** vender, listas de herramientas, paseos con presupuesto, cumpleaños o «14 años
   en Amazon».
6. **Sirve para la meta:** puede traer vistas de gente que no conoce a Kenneth.

## Paso 1 · Los 100 puntos

| # | Qué se mira | Puntos | Se gana todo si… |
|---|---|---|---|
| 1 | **Para qué es** | 10 | Dice qué tiene que lograr la pieza (que frene el scroll, que la vean entera, que la manden), para quién es y qué se lleva el que mira. **No es un resumen del video.** |
| 2 | **El gancho (0 a 3 s)** | 20 | Voz, texto grande y visual están en el cuadro 0. No da nada por sabido: la situación o la contradicción se entiende sin saber nada. En la prueba en frío, la persona de 35 años se queda. |
| 3 | **La retención (del segundo 3 al final)** | 15 | Hay un re-gancho a los 3–4 s y otro a la mitad. Algo cambia cada 1 a 1,5 s. Dura de 12 a 20 s y paga lo que prometió el gancho. |
| 4 | **La claridad** | 15 | Trae el objetivo en una frase y la historia en 5 frases. Es una sola historia. En la prueba en frío, el joven de 12 años la cuenta entera y no marca nada confuso. |
| 5 | **El valor** | 10 | Deja algo que se usa hoy. La regla de líder sale de la historia, no se pega. |
| 6 | **Que se comparta** | 10 | Hay una razón concreta para mandárselo a alguien concreto, y el cierre sale de la historia. |
| 7 | **La verdad** | 10 | La prueba es real, las citas son textuales y cada dato tiene su fuente. |
| 8 | **La forma y la marca** | 10 | Lleva la firma (título, sello, regla de líder y cierre) y las palabras de la marca: colaboradores, líder, joven de 12. La voz clonada va sin «IA» y sin voseo, el gemelo con un look aprobado, sin emojis ni cajitas básicas. **No se ve igual a las anteriores:** la forma del gemelo no repite la de la pieza anterior con gemelo, suma al menos una técnica nueva y no repite fondo ni efecto principal de las últimas 3 (`efectos/USO.md`). **En el video:** sonido a −14 LUFS, subtítulos en la zona segura, brazos y boca del gemelo bien. |

**Pasa con 87 o más.** 87 no es perfecto, pero es aceptable. Con menos de 87 se devuelve con lo que falta.

**Se devuelve aunque sume 87 o más si:**

- falla el paso 0;
- hay una cita o un dato falso;
- sale un look del gemelo que no está aprobado;
- vende.

## Paso 2 · Lo que entrega el auditor, por pieza

1. **La calificación:** el total y los puntos de cada uno de los 8.
2. **Para qué es,** en 2 o 3 frases: qué tiene que lograr, para quién y qué se lleva el que mira.
3. **El guion:** el archivo.
4. **Los defectos:** cada uno con los puntos que resta y el cambio concreto que lo arregla.
5. **¿Trae más vistas?:** sí o no y por qué. Dice el segundo en que se iría la gente.
6. **El veredicto:** PASA (87 o más) o SE DEVUELVE (menos de 87), con lo que falta para llegar.

**Dónde queda:**

- en `marca/auditorias/AAAA-MM-DD-<código>.md`;
- en la Sala, en el campo `calificacion` del documento, para que Kenneth la vea y la escuche.

Forma del campo: `{ "total": 91, "veredicto": "Pasa", "puntos": [["Para qué es", 9, 10], …], "defectos": ["…"],
"vistas": "…" }`.

## Paso 3 · ¿Acertamos? (el lunes)

El agente **resultados** pone la calificación de cada pieza al lado de lo que pasó: vistas, retención a los 3 s,
compartidos y seguidores.

- Si una pieza de 90 trajo menos que una de 80, la vara está mal calibrada.
- En ese caso se cambian los pesos o lo que pide cada punto, y queda anotado aquí abajo con la fecha.

## Cambios a la vara

- **25-oct:** el punto 8 pide variedad (Kenneth: «No quiero que mis videos todos se vean iguales»; LP1, IP1 y LP2 usaron la
  misma ventana chica).
- **24-oct:** se crea. Pesos iniciales: gancho 20, retención 15, claridad 15 y los demás 10. Salen de la autopsia del
  23-oct (la gente se iba entre los 2,4 y los 7,4 s) y del LP2 v1, que no se entendía.
