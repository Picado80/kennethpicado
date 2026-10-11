# Guion gráfico · NNN · Título

> Va **antes** de gastar en el gemelo y de renderizar. Kenneth lo aprueba o lo corrige con una frase
> («más oscuro», «el tramo 4 con portada», «corte más apretado»). Sin su visto bueno no se produce.

## Cómo se arma (así lo ve Kenneth)

1. Los tramos se escriben en `produccion/NNN/tramos.json`: tiempo, tipo de toma, la frase, qué pasa, énfasis, oro y sonido.
2. Se arma el borrador en HyperFrames con **una foto fija de Kenneth** donde va el gemelo: no se gasta nada.
3. `python marca/scripts/storyboard.py produccion/NNN/tramos.json --video <borrador.mp4> --salida marca/salidas/guion-grafico-NNN`
   saca las páginas en PNG: cada tramo con sus cuadros y sus notas, como el guion gráfico de @justyn.ai.
4. Kenneth las ve y corrige con una frase. **Recién ahí** se genera el gemelo y el video final.

La tabla de abajo es la versión en texto, para cuando todavía no hay borrador.

**Estilo:** Editorial (`ESTILO.md`) · **Duración:** __ s · **Kenneth en pantalla:** __ s · **Costo estimado:** $__

| # | Tiempo | Recurso | Qué se ve | Qué dice | Oro / golpe | Sonido |
|---|---|---|---|---|---|---|
| 1 | 0,0–2,7 | Titular detrás de la cabeza | | | | |
| 2 | | | | | | |

**Reglas que se revisan aquí:**
- [ ] El recurso cambia cada 2 a 4 segundos, y hay al menos 6 recursos distintos.
- [ ] Una sola palabra en oro por pantalla.
- [ ] Kenneth en pantalla: 25 s o menos (meta de $2.00).
- [ ] Todo número que aparece tiene fuente en el guion.
- [ ] Los primeros 3 segundos dicen para quién es.
