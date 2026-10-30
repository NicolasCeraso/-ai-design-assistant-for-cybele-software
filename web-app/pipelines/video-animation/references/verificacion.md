# Verificación y reporte

1. **Mirar el MP4, no los keyframes.** Tras armar: `contact_sheet.py` en el centro de cada transición (corte ± 0.3 s), en cada cambio pedido y en cada arranque de escena (el primer cuadro de la escena k+1 debe ser el último de la k; comparación de PSNR entre ambos ≈ 40 dB o más).
2. **Medir sincronías en el MP4.** Checks, agujas, apariciones: `measure_motion.py` sobre la zona del elemento, o área de píxeles por cuadro. Los keyframes no bastan (el exportador puede mover un instante por redondeo de fps).
3. **Duraciones.** `ffprobe`: cada escena = fin−inicio de sus cortes (+ pausas); el video total = último corte − `cuts[0]` + pausas. El AAC añade ~0.06 s por escena: no importa.
4. **Desfases típicos y su causa**
   - Escena 1 con 0 s: `cuts` mal armado (usar N+1 valores, `cuts[0]` = inicio de la 1ª escena).
   - Sonido tapado: usar nivel automático o `fix` más alto.
   - Un sonido de más en un tramo sin acción: revisar `sfx` de esa escena.
   - "Too many video exports started": exportar de a 1–2.
   - `export_video` devuelve un texto cortado en la transición: el último tramo se ve clonado durante la transición; no dejar elementos a medio salir al final de la escena.
5. **Reporte final** (español, breve): archivo y duración, qué cambió por escena, ids de Figma, qué se midió en el MP4 y qué NO se pudo comprobar (reproducción en movimiento, audio), interpretaciones tomadas y la decisión abierta, si la hay.
