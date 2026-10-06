---
id: NNN
formato: la-oficina | amazon-soda | sistema-semana | cual-soy-yo
titulo:
idea: O1 | A1 | …      # fila de ideas.md
estado: guion | grabado | editado | publicado
uso_ia: ninguno | voz-personaje | voz-clon | gemelo
duracion_objetivo_s: 45
fecha_publicacion:
url:
---

# NNN · Título

## Gancho (0–3 s)
**Dice:**
**Texto en pantalla:** (se tiene que entender sin sonido)

## Desarrollo
Una línea por toma. Marcar la energía: `[CALMA]` o `[ACELERA]`.

## Giro / lección

## Cierre
La pregunta que provoca comentarios, o el «mandáselo a…».

## Pantalla y B-roll
Qué se ve en cada tramo. Capturas siempre **difuminadas**.

## Piezas con IA
| Pieza | Herramienta | Texto exacto | ID de voz / avatar (`config/estudio.json`) |
|---|---|---|---|

## Caption (TikTok)
Gancho + 3 a 5 hashtags. Sacarlo con el skill `social-copy-generator`.

## Fuente de cada dato
| Dato que se dice | Fuente |
|---|---|

---

## QA antes de publicar (todas marcadas o no sale)

- [ ] El gancho se entiende **sin sonido** (texto en pantalla en los primeros 3 s)
- [ ] Cero jerga: pasó el glosario de `CANON.md`
- [ ] Ningún nombre de cliente o persona; ninguna llave, correo ni dato en pantalla (revisado cuadro por cuadro)
- [ ] Todo número tiene fuente en la tabla de arriba
- [ ] Ninguna venta: ni precios, ni «agendá», ni pitch de Semi
- [ ] Si hay HeyGen o ElevenLabs: etiqueta «contenido generado por IA» activada
- [ ] Si hay gemelo o voz clonada: pasó `revisar-video` (deriva de la cara, labios, manos)
- [ ] Duración ≤ 45 s, o la razón está escrita aquí: ______
- [ ] Fila creada en `medicion/registro.csv`
