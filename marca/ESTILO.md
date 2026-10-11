# Estilo: variado y elegante

> Kenneth (11-oct-2026), sobre el video de @justyn.ai («I didn't edit a single second of this video»):
> «me encanta, y los quiero así de variados y elegantes». Aquí está qué hace ese video, qué copiamos
> (el mecanismo, nunca el contenido) y cómo queda nuestro sistema.

## Qué hace ese video (58 s, revisado cuadro por cuadro)

**Por qué se ve elegante: pocas reglas, siempre las mismas.**

| Regla | En el video |
|---|---|
| **Tres colores y nada más** | Verde oscuro para los fondos, crema para el texto y dorado para la palabra que importa |
| **Tres letras, cada una con un trabajo** | Serif alta y en mayúsculas para los titulares (como una revista) · serif cursiva dorada para el énfasis («Claude *did.*») · sans gruesa para el golpe («SECOND», «BIGGER») · monoespaciada chiquita para los detalles («NO. 01 · OCTOBER 2026») |
| **El titular va detrás de la cabeza** | Lo recortan a él del fondo y el título queda entre el fondo y la persona. Es lo que hace que parezca portada de revista |
| **Subtítulos discretos** | Serif chica, crema sobre una cajita verde, de 2 a 4 palabras. La palabra que viene se ve apagada y se enciende cuando la dice |
| **Los detalles de imprenta** | Marco fino dorado, línea de número y fecha, código de barras, código de tiempo. No dicen nada, pero dan oficio |

**Por qué se ve variado: cada 2 a 4 segundos cambia el recurso, no solo la toma.** En 58 segundos usa 14:

1. Titular gigante detrás de la cabeza, sobre fondo de color.
2. Íconos tachados encima de la cabeza (lo que **no** usa).
3. Una «píldora» de mensaje que se escribe sola («make it more aesthetic») y se envía.
4. Otra toma: cerca, media, sentado lejos, agachado, de pie. Cinco o seis encuadres reales.
5. Tarjetas que entran flotando e inclinadas (sus mejores videos).
6. La portada de revista: marco, cabecera, número, código de barras.
7. Paneles de pantalla: la línea de tiempo, el archivo, el sello «BAD TAKE», el reloj de volteo «0:54».
8. Cambio de ambiente: todo se oscurece y el subtítulo crece hasta ocupar la pantalla.
9. Un mosaico de 9 videos de otra gente, a pantalla completa.
10. El **guion gráfico** en pantalla: cada tramo con su foto, su frase y sus notas.
11. Una burbuja de comentario que se escribe.
12. Banda de color con texto grueso + cursiva dorada («BIGGER *captions.*»).
13. Tarjetas del curso con su reproductor.
14. El cierre: etiqueta con la instrucción, el comentario de ejemplo y la píldora de «seguir».

## Lo que él tiene en el proceso y nosotros no (se agrega)

| Le sirve a él | Lo que hacemos nosotros |
|---|---|
| **Guion gráfico antes de renderizar**: ve qué piensa Claude y corrige con una frase | **Se agrega como paso fijo** (`plantillas/storyboard.md`): Kenneth lo aprueba antes de gastar en el gemelo |
| **Cambios con una frase** («más estético», «más oscuro», «subtítulos más grandes», «corte más apretado») | **Se agrega**: el estilo vive en variables (colores, letras, tamaño de subtítulos). Cambiarlas es una línea |
| **Varias tomas reales** del mismo video | **Falta**: el gemelo tiene un solo encuadre. Ver «Lo que hace falta de Kenneth» |
| **Título detrás de la cabeza** | **Se agrega**: recorte del fondo en la PC (`hyperframes remove-background`), $0 |
| Material grabado con tomas malas, que Claude limpia | No aplica al gemelo. Para los videos personales: Video-Use (`HERRAMIENTAS.md`) |

**Lo que ya tenemos y se queda:** subtítulos con los tiempos de cada palabra, efectos de sonido,
animaciones con código, pantalla dividida, el registro de costos y el agente `costeo`.

## Nuestro sistema: «Editorial»

Sale de la identidad del portafolio de Kenneth (vitela, tinta, grafito), no del verde de la referencia.

| | Valor | Uso |
|---|---|---|
| Tinta | `#16233F` | Fondos y cajas |
| Vitela | `#E8E6DE` | Texto |
| Oro | `#C9A45C` | La palabra que importa, en cursiva. **Una por pantalla** |
| Grafito | `#23262A` | Texto sobre vitela |
| Rojo | `#B22B3F` | Tachones y avisos |
| Titulares | Instrument Serif, mayúsculas, muy grande | Detrás de la cabeza o a pantalla completa |
| Énfasis | Instrument Serif cursiva, en oro | La palabra clave |
| Golpe | Archivo 900 | Una o dos palabras |
| Detalles | JetBrains Mono, mayúsculas espaciadas | Número, fecha, serie, código de tiempo |
| Subtítulos | Instrument Serif 58 px, vitela sobre caja tinta; la palabra que viene, apagada | Siempre, salvo cuando el texto ya está en pantalla |

**Reglas:**
- El recurso cambia cada 2 a 4 segundos. **Mínimo 6 recursos distintos por video.**
- Una sola palabra en oro por pantalla.
- Nada de amarillo chillón ni de cajas con sombra dura: eso era la versión 3.
- Cada video lleva su línea de serie en monoespaciada: `N.º 002 · AMAZON EN LA SODA · OCT 2026`.

**Recursos propios (los 14 de arriba, con nuestros temas):** titular detrás de la cabeza · portada de
revista · tarjetas flotantes (notas, facturas, mensajes de WhatsApp) · píldora que se escribe sola ·
reloj de volteo · banda con golpe + cursiva · pantalla dividida · papel recortado · tachón rojo ·
mosaico · pantalla invertida (vitela con texto grafito) · cierre con píldora de «guardar» y «enviar».

**Frases que cambian todo el video:**

| Kenneth dice | Qué cambia |
|---|---|
| «Más estético» / «más cálido» | Fondos tinta → marrón cálido, oro más presente, portada de revista |
| «Más oscuro» | Fondos grafito, subtítulos más grandes, menos color |
| «Subtítulos más grandes» | De 58 a 96 px, una o dos palabras por vez |
| «Corte más apretado» | Los recursos cambian cada 1,5 a 2,5 s y se recortan los silencios |
| «Más sobrio» | Sin tarjetas flotantes ni sellos; solo titulares, subtítulos y pantalla dividida |

## Lo que hace falta de Kenneth para llegar a ese nivel

- **Más encuadres del gemelo.** La referencia cambia de toma seis veces; el gemelo «Kenneth GP» tiene un
  solo encuadre. Con 3 o 4 grabaciones más de 2 minutos (cerca, sentado más lejos, de pie, otro fondo),
  HeyGen crea un gemelo por encuadre y los videos pueden cortar entre tomas. Se graba una sola vez.
- **Sin audífono** en esas grabaciones: en el gemelo actual se ve cuando gira la cabeza.
