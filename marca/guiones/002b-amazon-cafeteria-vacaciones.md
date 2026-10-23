---
id: 002b
tipo: insignia   # ESTRATEGIA.md §3. Primero se prueba como volumen (voz + motion graphics, $0); la que gane va con el gemelo
paso: pasarlo   # guardado y compartido (ESTRATEGIA.md §1)
formato: amazon-soda
titulo: Si tu cafetería recién abierta no sobrevive a tus vacaciones
idea: A1   # variante del 002 (Kenneth, 19-oct): la soda se queda y se prueba también con cafetería recién abierta
estado: guion
uso_ia: voz-clon | gemelo
duracion_objetivo_s: 45
fecha_publicacion:
url:
---

# 002b · Si tu cafetería recién abierta no sobrevive a tus vacaciones

> Variante del [`002`](002-amazon-soda-vacaciones.md) para **cafetería recién abierta**. Misma idea, mismos datos y el gancho que
> ganó en la prueba del 002 (`produccion/002/PRUEBA-GANCHO.md`). Sirve para medir qué escenario trae más seguidores
> por cada 1.000 vistas: la soda, la cafetería, el restaurante o el emprendedor.

## Gancho (0–2 s)
**Dice:** «En Amazon nadie era indispensable. Ni el jefe.»
**Texto en pantalla:** `Nadie era indispensable. Ni el jefe.` (tipografía grande, a pantalla completa)

## Desarrollo
1. `[CALMA]` «Trabajé en una operación que nunca se apagó. Ni un día.»   <!-- sin «catorce años» (Kenneth, 20-oct) -->
2. `[CALMA]` «Son las 6:40. La cafetería abre a las 7, y la única persona que sabe calibrar la máquina sos vos.»
3. «Si tu cafetería cierra el día que vos te enfermás, no tenés un negocio. Tenés un trabajo con máquina de espresso.»
4. «Y casi siempre es por lo mismo: el estándar vive en tu cabeza. Cuántos gramos lleva el espresso, cómo se calienta la leche del capuchino, qué se hace si se acaba el pan a las 10.»

## Giro / lección
5. `[ACELERA]` «Tres cosas para mañana:
   **Uno**, escribí las tres cosas que solo vos sabés. En una hoja, pegada al lado de la máquina.
   **Dos**, un solo número que veás todos los días. Cuántos cafés salieron, por ejemplo.
   **Tres**, quince minutos los lunes para ver ese número con tu gente.»

## Cierre
6. `[CALMA]` «Un negocio que te necesita todos los días no es un negocio. Es una dependencia. Guardá este video y
   mañana hacé la hoja.»   <!-- fuera «mañana te cuento qué va en ella»: el día 3 no sale eso -->
**Texto en pantalla:** `1 hoja · 1 número · 15 min los lunes` y el sello `Día N de 30` en una esquina, si el reto está en marcha.

## Pantalla y B-roll
- Una barra de café vacía antes de abrir, la máquina, una taza. Tomas de banco o animación: nunca un local reconocible.
- Toma 5: los tres pasos aparecen escritos a mano, uno por uno.

## Piezas con IA
| Pieza | Herramienta | Texto exacto | ID de voz / avatar (`config/estudio.json`) |
|---|---|---|---|
| Voz | ElevenLabs (`eleven_v4`) | todo el guion | `elevenlabs.voz_kenneth` |
| Cara (solo si gana como volumen) | HeyGen, gemelo | tramos 1, 3 y 6 | `heygen.avatar_id` |

## Caption (TikTok)
Borrador: *Abriste la cafetería y ahora no podés faltar ni un día. 3 cosas para mañana.* `#cafeteria #emprendimiento #negocios #costarica #amazon`

## Fuente de cada dato
| Dato que se dice | Fuente |
|---|---|
| Operación que nunca se apagó | portafolio («Built inside an operation that never stopped running»); CV: «24/7 environment» |
| «Nadie era indispensable» | portafolio, §The method; prueba de gancho del 002 |
| «El estándar vive en tu cabeza» | portafolio, §The method |
| «Es una dependencia» | portafolio, §Once it runs |
| Revisión de los lunes | caso del anfiteatro: revisión semanal de los lunes |
| La escena del tramo 2 | Es un ejemplo, no un caso: no se presenta como algo que le pasó a alguien con nombre |

---

## QA antes de publicar

- [ ] El gancho se entiende **sin sonido**
- [ ] Cierra con una razón para seguir («mañana te cuento…»)
- [ ] Cero jerga
- [ ] Ningún local, rótulo ni persona reconocible
- [ ] Todo dato tiene fuente
- [ ] Ninguna venta
- [ ] Si va con el gemelo: prueba de gancho con total ≥ 70, gancho ≥ 60 y «sostiene» ≥ 90
- [ ] Etiqueta de IA activada
- [ ] Duración ≤ 45 s; si pasa, recortar el tramo 4
- [ ] Fila creada en `medicion/registro.csv`
