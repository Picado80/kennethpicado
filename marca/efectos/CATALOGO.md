# Catálogo de la biblioteca de efectos

Todo vive en [`efectos.js`](efectos.js) y se ve funcionando en el carrete de muestra ([`demo.js`](demo.js), una escena por
efecto, en claro). Cada efecto arma su DOM dentro de un contenedor y devuelve `{ pintar(t) }`; el render es cuadro por
cuadro con Lemo-Opuscar (`node core/render/video.mjs <carpeta> --size 1080x1920`).

## Reglas (Kenneth, 20 y 21-oct-2026)

- **Claro por omisión:** fondo de papel, texto en tinta, celeste suave y resaltador amarillo (`K`). El estilo oscuro de
  antes queda con `oscuro: true`, pero no se usa.
- **Cada video cambia algo cada 1,5 a 2 s** (cámara, corte, B-roll o un elemento nuevo) y lleva un sonido en cada golpe.
- **Cada video nuevo suma al menos un efecto nuevo a la biblioteca** y se agrega como escena al carrete. Las ideas
  salen de la lista de abajo, de [prompt-motion.com](https://prompt-motion.com) y de las plantillas de Artlist (solo
  como ideas: son de pago y para After Effects, Premiere, DaVinci o Final Cut, que no usamos).
- Todo lo que se lee va en la zona segura común de las 4 redes (`SEGURA` y `BOTONES`).

## Lo que hay (36 efectos y la cámara)

| # | Efecto | Función | Para qué sirve |
|---|---|---|---|
| 1 | Snap zoom · tipografía de golpe | `frase`, `golpe` | Ganchos: la frase entra palabra por palabra y remata con un golpe de zoom |
| 2 | Checklist pop | `lista` | Las 3 cosas para mañana; pasos (`tiempos` para que cada ítem salte con la voz) |
| 3 | Growth curve | `curva` | El contador del reto |
| 4 | Chat takeover | `chat` | Una conversación que crece hasta llenar la pantalla |
| 5 | Phone mock-up | `telefono` | Mostrar respuestas o apps en un teléfono que entra girando |
| 6 | Headline storm | `titulares` | Noticias: titulares que caen y la cámara va al importante |
| 7 | Orbit | `orbita` | Cosas que giran alrededor de algo (la oficina alrededor de Kenneth) |
| 8 | Frame escape | `escapeMarco` | Una palabra que se sale del póster |
| 9 | Zoom portal | `portal` | Corte: la cámara entra por un hueco (la O de una palabra) y sale en otra escena |
| 10 | Studio reveal | `estudio` | Se prenden las luces y aparece el objeto girando, con reflejo |
| 11 | B-roll overlay | `broll` con `marco` | Una foto en ventana sobre la escena, moviéndose |
| 12 | Dolly zoom | `dolly` | El fondo se viene encima y el texto queda quieto: tensión |
| 13 | Magazine cover | `revista` | El gemelo en una portada que termina sobre una mesa |
| 14 | Liquid glass zoom-through | `vidrio` | Corte: un lente de vidrio crece y te lleva a la otra escena |
| 15 | Green screen frame break | `rompeMarco` | El cuadro del gemelo se rompe en pedazos y pasa a pantalla completa |
| 16 | Digital zoom | `zoomDigital` | «Mejorá la imagen»: saltos ×2 y ×4 con pixelado, visor y datos |
| 17 | Paper cutout | `recorte` (con `foto`) | El gemelo recortado en papel sale del cuadro |
| 18 | Marker notes | `marcador` | Círculos, flechas y notas a mano que se dibujan solas |
| 19 | Vox · el documento resaltado | `documento` | Un recorte de papel, la frase marcada en amarillo y lo demás se apaga |
| 20 | Vox · collage | `collage` | Fotos en semitono recortadas, papeles de color, movimiento de a dos |
| 21 | Vox · grano y papel rasgado | `textura`, `rasgado`, `aDos` | Textura y bordes para cualquier escena; el tiempo de stop-motion |
| 22 | Stamp on · el sello | `sello` | «Aprobado»: lo que hace Kenneth en el reto |
| 23 | Typewriter | `maquina` | El pedido que se le escribe a la IA |
| 24 | Fichas que saltan | `fichas` | Las 7 IAs, etiquetas |
| 25 | Resaltador | `conResalte`, `resaltar` | Una palabra marcada en amarillo, con el trazo animado |
| 26 | Cortes | `corte` (zoom, barrido, gira, golpe) | Entre escenas |
| 27 | Brillo y temas de color | `brillo`, `TEMAS`, `usarTema` | Manchas de luz que flotan, un destello que cruza; 7 fondos con degradado (papel, cielo, menta, durazno, océano, noche, bosque) |
| 28 | Burbuja que se escribe | `burbuja` | Los tres puntitos y el texto letra por letra (chats, pedidos) |
| 29 | Barra de comentarios | `comentario` | El cierre que invita a comentar: cursor, texto que se escribe y el corazón |
| 30 | Escenas encadenadas | `secuencia` | Cada escena con su tema y su corte (zoom, barrido, gira, golpe, portal, vidrio) |
| 31 | Candado con PIN | `candado` | Se llenan los 4 puntos y el candado se cierra con un golpe: privacidad, seguridad |
| 32 | Mapa con ruta | `ruta` | La línea avanza por las calles y cae el pin del destino |
| 33 | Glitch | `glitch` | La imagen se corta, se corre y se separa en colores: «se escapó», una falla |
| 34 | La corrección | `correccion` | La palabra se equivoca, tiembla, sale el subrayado rojo ondulado y se corrige a mano con «^» |
| 35 | Antes y después | `antesDespues` | Dos imágenes en una tarjeta; la manija barre la vieja y deja la nueva |
| 36 | El gemelo en la escena | `gemelo` (en `dia3/j2/index.html`) | Los cuadros del video de HeyGen detrás de los gráficos, con acercamiento lento |
| — | La cámara | `camara` | Acercar, alejar, ángulo en 3D, paneo, mano y desenfoque de movimiento |

## Por agregar (de a uno por video)

De prompt-motion.com y de Artlist:

- **Un elemento que une todas las escenas** (como el punto naranja de «Orange dot motion system»): por ejemplo el punto
  del resaltador que pasa de escena en escena.
- **Palabras con oficio** («Speech built as architecture»): las palabras arman la escena; la frase final se para sobre
  lo que construyeron las anteriores.
- **Cambio de luz:** golpe de claro a oscuro y de vuelta, en el momento fuerte.
- **Recibo o receta paso a paso** («recipe motion graphic»): ingredientes que entran, para procesos.
- **Teatro de sombras en papel** (vertical, 9:16).
- **Morph de formas:** un botón que se vuelve gráfico, que se vuelve tarjeta.
- **Infografías de vidrio de colores** y **pósters de tipografía en vidrio líquido** (Artlist).
- **Transiciones de película y «sin señal»** (Artlist: Fast Film, No Signal).
- **Títulos con pintura en aerosol, tinta que fluye, tipografía antigravedad** (Artlist).
- **Lower thirds** con el nombre y el cargo para cuando hable alguien.
