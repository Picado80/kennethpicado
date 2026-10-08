# Video 002, versión 1 (8-oct-2026)

Composición de HyperFrames del primer video completo: gemelo Avatar IV en 3 partes (28 s), 2 tomas
de relleno de HeyGen Video, gráficos, efectos de ElevenLabs y subtítulos palabra por palabra.

- `index.html`: la composición que se renderizó. Los medios (`assets/`) no van a git: están en
  `marca/salidas/hf/v002/assets/`.
- `plantilla.html` + `subtitulos.py`: de donde sale `index.html` (los subtítulos se arman con los
  tiempos de cada palabra de `marca/salidas/002-palabras.json`).
- Render: `npx hyperframes render` en `marca/salidas/hf/v002` (78 s en la PC).
- Costo: $2.37 de producción. Detalle en `marca/costos/registro.csv`.
