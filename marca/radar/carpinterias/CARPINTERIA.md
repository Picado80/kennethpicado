# La carpintería: el formato como pieza de trabajo

> Una carpintería no es un video. Es el **molde** de un video: la estructura que hace que
> la gente frene, se quede y lo pase. Se copia el molde, nunca el contenido.

## Por qué existe esto

El radar de la marca (`marca/radar/radar.py`) ya trae los videos más compartidos de la semana.
Eso está bien. Pero un video no se puede copiar: se puede copiar **la forma en que está hecho**.

Hasta ahora esa forma vivía en párrafos sueltos dentro de `.md` sueltos. Sin eso no se puede:
- decir que la carpintería C-007 ya se probó y no funcionó;
- decir que la C-012 funcionó y hay que repetirla con otro gancho;
- generar la agenda del mes sin que alguien lea 12 archivos a mano.

Una **carpintería** es el molde con ficha. Tiene número (`C-001`), gramática (cómo está armado),
evidencia (cuánto viralizó en el mundo) y **nuestra** evidencia (cuánto viralizó en *tu* cuenta).

## Las dos pruebas

| Prueba | Pregunta | Quién la contesta |
|---|---|---|
| **Global** | ¿Esto viraliza en el mundo? | El radar: vistas, compartidos, señal |
| **Nuestra** | ¿Esto viraliza en *nuestra* cuenta? | La medición: seguidores por 1.000 vistas |

La global dice que el molde existe. La nuestra dice si nos sirve. **Cuando las dos hay, manda la
nuestra** (`ESTRATEGIA.md` §1: en la fase 1 la métrica que manda son los seguidores, no las vistas).
Por eso el catálogo tiene dos campos de señal y no uno.

## La ficha

Una carpintería vive en `catalogo.json`. Los campos, en orden:

### Identidad
| Campo | Qué es |
|---|---|
| `id` | `C-001`. Nunca se reutiliza ni se renumera. |
| `nombre` | Cómo se le dice al molde, en una frase. Sin jerga de marketing. |
| `estado` | `nuevo` → `en_prueba` → `funciono` \| `no_funciono` → `descartada` |
| `creada` | Fecha. |

### El original (siempre con su fuente)
| Campo | Qué es |
|---|---|
| `original.url` | El link. Sin esto la ficha no existe. |
| `original.cuenta` | De quién es. |
| `original.fecha` | Cuándo se publicó. |
| `original.vistas` / `likes` / `compartidos` | Los números, tal cual vinieron. |
| `original.señal` / `señal_tipo` | La métrica con la que se rankeó y cuál fue (`compartidos` o `interaccion`). |
| `original.duracion_s` | Duración en segundos. |
| `original.gancho_literal` | Las primeras palabras, **textuales**. Nointerpretadas. |
| `original.cuadros` | Rutas de los 3 cuadros extraídos. Sirven para ver el diseño. |

### La gramática (el molde)
| Campo | Qué es |
|---|---|
| `tipo_gancho` | `pregunta` · `resultado_primero` · `afirmacion_incomoda` · `historia` · `comparacion` · `en_vivo` · `reto` |
| `gancho_0_3s` | Qué pasa en los primeros 3 segundos, en una frase. |
| `re_gancho_s` | En qué segundo vuelve a agarrar al que scrollea. |
| `re_gancho` | Cómo lo hace. |
| `estructura` | Lista de bloques, en orden, con lo que hace cada uno. |
| `banda_duracion` | La franja donde el formato funciona (`6-15 s`). |
| `subtitulos` | `palabra_por_palabra` · `frase_corta` · `ninguno` |
| `plano` | `a_camara` · `b_roll` · `pantalla` · `mixto` |
| `ritmo_cortes` | Cuántos cortes en el video. |
| `sonido` | El sonido y qué papel juega. |
| `cierre` | `pregunta` · `compartilo` · `remate` · `cliffhanger` · `ninguno` |
| `mecanica_comentarios` | Qué hace que la gente comente. |

### La tropicalización (lo nuestro)
| Campo | Qué es |
|---|---|
| `encaja` | ¿Pasa las 4 condiciones de `IDENTIDAD.md`? Si no, no se propone. |
| `serie` | A cuál de las líneas de `CALENDARIO.md` §"Las series y su objetivo" pertenece. |
| `pieza` | Cómo se llamaría nuestra versión. |
| `tarea_real` | La tarea real de casa o trabajo que le da carne. |
| `regla_lider` | La regla numerada que cierra (`IDENTIDAD.md`). |
| `cambios` | **La lista de cambios**, uno por dimensión: qué era en el original, qué es en el nuestro y por qué. |
| `avisos` | Lo que quedó estirado, lo que no cabe, lo que hay que recortar. |

### Lo nuestro (el aprendizaje)
| Campo | Qué es |
|---|---|
| `nuestro.piezas` | Los códigos de las piezas donde se usó. |
| `nuestro.seguidores_por_1000` | La métrica que manda. `null` si no se ha probado. |
| `nuestro.notas` | Qué pasó. |

## La regla de oro del rastro

Toda tropicalización deja el rastro completo: **el original y el camino del cambio**.
Kenneth tiene que poder ver el video original, ver de dónde salió nuestra versión y decidir si
quedó muy larga, muy estirada o bien. Por eso `cambios` es obligatorio y por eso el digest
muestra el original al lado de nuestra versión, nunca solo el resultado.

Si el rastro no está, la tropicalización no cuenta.

## Las 4 condiciones de `IDENTIDAD.md`

Una tropicalización solo se propone si pasa las cuatro:

1. Una **tarea real** de la casa o del trabajo.
2. Una **prueba real** con inteligencia artificial.
3. El **resultado antes del segundo 3**.
4. Una **regla de líder** numerada al final.

Las evalúa `tropicalizar.py` de forma mecánica y dice cuál falló y por qué. Lo que no se puede
evaluar a máquina (¿la tarea es real? ¿la prueba es real?) se marca a mano y el sistema no lo
da por aprobado.

## El ciclo

```
radar diario (raw)  →  agente tendencias  →  carpintería (ficha)
                                              ↓
                                   tropicalizar.py (reglas)
                                              ↓
                                    nuestra versión + rastro
                                              ↓
                                    Kenneth aprueba en la Sala
                                              ↓
                                     se publica (Buffer)
                                              ↓
                              medición a las 48 h y a los 7 días
                                              ↓
                            estado = funciono / no_funciono  +  nuestro.seguidores_por_1000
                                              ↓
                                   el catálogo se reordena solo
```

El paso del final es el que hace que el sistema mejore: después de un mes, el catálogo no
ordena por lo que viraliza en el mundo, ordena por **lo que viralizó en tu cuenta**.

## Archivos

| Archivo | Qué es |
|---|---|
| `catalogo.json` | Todas las carpinterías. La fuente de verdad. |
| `plantilla.md` | La ficha en blanco, para crear una a mano. |
| `carpinterias.py` | Alta, edición, validación y orden del catálogo. |
| `tropicalizar.py` | Las reglas: condiciones, series y esqueleto de tropicalización. |
| `reglas-tropicalizacion.md` | Las mismas reglas en palabras, para el agente. |
| `LEEME.md` | Cómo se usa todo junto. |

Y afuera de esta carpeta:

| Archivo | Qué es |
|---|---|
| `marca/medicion/carpinterias.csv` | Qué pieza usó qué carpintería y qué dio. |
| `marca/radar/hoy.md` | El digest de cada mañana (lo escribe `diario.py`). |
| `marca/radar/carpinterias/AAAA-MM-DD.md` | Las carpinterías del día (lo escribe el agente). |
