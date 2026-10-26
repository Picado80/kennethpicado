# Reglas de tropicalización

> Las reglas en palabras, para el agente que tropicaliza. El código que las evalúa
> está en `tropicalizar.py`; el modelo completo, en `CARPINTERIA.md`.
> Fuentes: `marca/IDENTIDAD.md`, `marca/CANON.md`, `marca/CALIFICACION.md`, `marca/FORMATOS.md`.

## Qué es tropicalizar

**No es traducir.** Es tomar el molde de otro video y cambiarle la carne para que
diga lo que Kenneth tiene que decir, sin que deje de funcionar como formato.

Por ejemplo: un video de un restaurante que muestra el plato en 3 segundos y después
explica el proceso. La carpintería no es «el restaurante». La carpintería es
«el resultado primero, el proceso después, el cierre es el precio». Nuestra versión
puede ser el mismo molde con la soda de barrio y una regla de Amazon.

## El rastro es obligatorio

**Toda tropicalización deja dos cosas: el original y el camino del cambio.**

- El **original**: el link, quién lo hizo, los números y las primeras palabras textuales.
- El **cambio**: por cada dimensión (gancho, re-gancho, estructura, duración, cierre,
  planos, subtítulos, sonido), qué era en el original, qué es en el nuestro y **por qué**.

Sin el rastro, la tropicalización no cuenta. Kenneth tiene que poder ver el original y
decidir si nuestra versión quedó muy larga, muy estirada o bien.

Por eso el digest siempre muestra el original al lado de nuestra versión, y nunca
solo el resultado.

## Las 4 condiciones (si una falla, no se propone)

1. **Una tarea real** de la casa o del trabajo de un tico.
2. **Una prueba real** con inteligencia artificial, **con el resultado guardado**.
3. **El resultado o la pregunta antes del segundo 3.**
4. **Una regla de líder** al final.

Las 1, 3 y 4 se escriben. La 2 se declara y **alguien tiene que verificarla**: una
máquina no puede saber si la prueba fue real. Si no está verificada, la carpintería
queda en `en_prueba`, nunca en `funciono`.

## A qué serie va

| Serie | Hora | Le calza un molde que… |
|---|---|---|
| **Lo probé por vos** | 12:00 | tiene una TAREA real que se le puede dar a una IA y un resultado que se puede corregir |
| **Un truco en 12 s** | 19:00 | es corto y da una forma de pedir algo que se usa hoy mismo |
| **¿La IA puede…?** | 20:30 | es un EXAMEN: se prueba algo y se dice si pasó o no |
| **La Oficina** | semanal | tiene arco de equipo, chisme de oficina o una contradicción de proceso |
| **Costa Rica en anime** | sábados | muestra un antes y un después visual de algo real de acá |

`tropicalizar.py` propone hasta 3 con el porqué. No decide: elige quien tropicaliza
y lo anota en la ficha.

## Lo que hay que cambiar siempre

| Dimensión | Qué hay que respetar |
|---|---|
| Gancho | La situación o la contradicción. Sin contexto y **sin anunciar lo que se va a hacer**. |
| Re-gancho | Algo cambia entre el segundo 3 y 4, y otra vez a la mitad. |
| Duración | De 12 a 20 s. Si el molde dura más, se recorta y **se avisa en `avisos`**. |
| Cierre | Pregunta, compartilo o remate. Y al final, la tarjeta de la regla de líder. |
| Planos | No repetir la forma del gemelo de la pieza anterior (`efectos/USO.md`). |
| Subtítulos | Palabra por palabra, con la firma de la marca. |
| Tono | Tico. Como Machillo: lo tico es el chiste. Sin jerga técnica. |
| Título | Caja negra, letra blanca, sombra naranja. El sello de la serie en el mismo lugar. |

## Lo que nunca se copia

- **Vender.** Ni en el video ni en la descripción.
- **El ritmo ajeno.** Se copia la estructura, no la música ni el ritmo del original.
- **La cara o la voz de otra persona.** Solo el gemelo aprobado, con etiqueta de IA.
- **Las listas de herramientas.** «10 herramientas que no conocías» está explícitamente
  fuera (`FORMATOS.md` §"Lo que descarté, y por qué").
- **El contenido.** Se copia el mecanismo, nunca el contenido.

## El ciclo de aprendizaje

Cuando una pieza con una carpintería se publica:
1. La pieza se anota en `marca/medicion/carpinterias.csv` con su carpintería.
2. A las 48 h y a los 7 días, `resultados` pone los números.
3. La carpintería pasa a `funciono` o `no_funciono`, con **seguidores por 1.000 vistas**.
4. El catálogo se reordena solo: lo que funcionó en nuestra cuenta sube.

Un molde que se probó dos veces y no trae seguidores no se propone más. Esa es la
diferencia entre un radar y un sistema: el radar te dice qué viraliza; el sistema te
dice **qué te viraliza a vos**.
