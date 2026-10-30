<!-- Autoritativo para el pipeline `video` de la consola. Copia del skill `cybele-video-animation` (~/.claude/skills);
     la carpeta pipelines/video-animation/ trae los scripts y las referencias. Si cambiás uno, sincronizá el otro. -->

# VIDEO_ANIMATION_SPEC — del storyboard en Figma al MP4

Pipeline validado en el video "Thinfinity para Contact Centers" (10 escenas, 1:28, 30 fps, voz en off + SFX + música). Todo el criterio visual y sonoro viene de pedidos reales de Nick: no lo "mejores" por tu cuenta, seguilo (`pipelines/video-animation/references/reglas-de-nick.md`).

## Entradas necesarias
- Figma: `fileKey` del storyboard, y el frame/columna de cada escena (estados clave de arriba hacia abajo + textos "VO n" + "Guion"). Para Thinfinity: archivo `K8rHguGyksdPWdHrSA3VOi` ("Youtube").
- Locución: un WAV con TODA la voz en off (ya final). Si cambia el audio, cambian cortes y tiempos: se retemporiza. **Es OPCIONAL: si no hay audio, NO es un error ni se frena la tarea** (ver "Sin audio" abajo).
- Opcional: música de fondo (MP3) y carpeta de efectos de sonido (WAV).
- Herramientas: Figma MCP (`create_session`, `use_figma`, `get_screenshot`, `export_video`), skills `figma-use`, `figma-use-motion`, `figma-generate-design`; ffmpeg; Python 3.13 con numpy (`py -3.13`); un transcriptor con tiempos por palabra (Whisper).

## Calidad mínima: NO una presentación de diapositivas
Animar NO es empujar cada estado completo del storyboard (un clon entra, el anterior sale): eso es una presentación de diapositivas y Nick lo rechazó. Cada transición entre estados se construye comparando elemento por elemento (se mueve lo que está en ambos estados, entra con movimiento propio lo nuevo, sale con el suyo lo que ya no está, el texto va palabra por palabra, las líneas se trazan) — la técnica y la plantilla de pedido a subagentes están en `pipelines/video-animation/references/brief-por-escena.md`. Un empuje de estados completos no se entrega como "hecho": si no alcanza el presupuesto, entregá una versión parcial, marcala así y decí qué escenas quedaron simples. Delegá una escena (o dos) por subagente en paralelo si hay Agent tool.

## Flujo (en orden)
0. **Preflight (automático, antes de tocar nada).**
   - Fuera de Figma: `py -3.13 scripts/preflight.py [video.json]` (Python 3.13+, numpy, ffmpeg + libx264, y que existan locución, música, SFX y MP4 de escena). Si sale con código 1, instalá lo que falte o avisá.
   - Motion de Figma: es una función de la cuenta/sesión y NO se puede habilitar desde el repo ni desde el skill. Se detecta con un `use_figma` de solo lectura:
     `const n = figma.currentPage.findOne(x => x.type === 'FRAME'); try { void n.manualKeyframeTracks; void figma.motion.figmaAnimationStyles; return {motion:true}; } catch (e) { return {motion:false, error:String(e.message)}; }`
     Si devuelve `motion:false` (o cualquier llamada de motion falla con `"<nombre>" is not a supported API`), PARÁ: no reintentes ni gastes llamadas; decile a Nick que el motion de Figma no está habilitado para su cuenta/sesión y pedile que lo active (o que abra el archivo con una cuenta que lo tenga). Con `motion:true` seguí.
1. **Audio → cortes por escena** (sin audio: saltá al bloque "Sin audio" de abajo y definí `scene_durations`). Transcribí con tiempos por palabra y detectá silencios (`ffmpeg silencedetect`). Cada escena se corta en una pausa. Whisper marca TARDE (~0.3–0.5 s) la primera palabra de cada frase: el inicio real de frase es el FIN del silencio previo. Guardá `cuts` (segundos absolutos) y las palabras con tiempo relativo a su escena. → `pipelines/video-animation/references/audio-y-armado.md` §1
2. **Animar cada escena en Figma** (con la técnica de diff de `pipelines/video-animation/references/brief-por-escena.md`, no con empuje de pantallas) (una sección `Animación – Escena N` y un frame `EscN – Animación` por escena; nunca tocar los frames originales). Texto palabra por palabra con clones, easing de la "parábola", bounce en las entradas que Nick pida, iconos solo clones. → `pipelines/video-animation/references/animacion-figma.md`
3. **Exportar cada escena**: `export_video` (1920 px, 30 fps, high) de a 1–2 por vez, bajar con `curl`, mezclar el audio de la escena con ffmpeg → `escenas/Escena_NN.mp4`. Podés repartir escenas entre subagentes (uno por escena o par de escenas, reanudables); el `export_video` falla con "Too many video exports started" si exportan varios a la vez.
4. **Armar el video**: copiá `pipelines/video-animation/video.example.json` a tu proyecto, completalo (cortes, pausas, transiciones, SFX, música) y corré `py -3.13 scripts/assemble_video.py video.json salida.mp4`. → `pipelines/video-animation/references/audio-y-armado.md` §2–§5
5. **Verificar mirando el MP4** (no los keyframes): `pipelines/video-animation/scripts/contact_sheet.py` alrededor de cada transición y de cada cambio, `pipelines/video-animation/scripts/measure_motion.py` para sincronizar sonidos con movimiento. → `pipelines/video-animation/references/verificacion.md`
6. **Preview y entregable.** Junto al maestro (`video.mp4`) queda `video_low.mp4` (720p, lo escribe `assemble_video.py` solo) y `pipelines/video-animation/scripts/make_preview_html.py <carpeta>` arma `preview.html`: reproductor con calidad **BAJA por defecto** (pedido de Nick) y selector Baja/Alta. La descarga permite elegir formato (MP4 H.264, WebM VP9, MOV) y calidad (baja 720p, media 1080p, alta tamaño original); el entregable de este tipo es solo video.
7. **Entregar**: H.264 (`salida.mp4` ya lo es: High, yuv420p, AAC, faststart) y, si se pide, 4K con `--4k` (ojo: es un escalado, ver abajo). Reportar con honestidad lo que no se pudo verificar (no se ve en movimiento ni se oye el audio).

## Sin audio (pedido de Nick: se sigue igual, sin sonido)
Si no hay WAV de locución, la tarea NO falla: se anima y se entrega un video **sin audio**.
- Duración de cada escena: de los textos VO/Guion del storyboard, `max(3.0 s, 0.5 s + palabras ÷ 2.5 + 0.6 s)`, y al menos ~1 s por estado clave. Documentá en `NOTES.md` que los tiempos son estimados.
- Texto: la 1ª palabra de cada frase arranca a ≈0.3 s del inicio de su estado y las demás en cascada de 0.08 s. Movimiento con la parábola, como siempre.
- Nada de SFX, música ni pausas. En `video.json` omití `voice`, `cuts`, `music`, `sfx` y poné `"scene_durations": [seg por escena]`: `assemble_video.py` arma el video SIN pista de audio (`-an`). Las transiciones se aplican igual. `preflight.py` lo avisa sin fallar.
- No inventes ni generes audio. Reportá "sin audio" y que los tiempos son estimados.
- **Cuando llegue el audio** (Nick lo adjunta en un request de changes): rehacé desde el paso 1 — cortes por escena, retemporizar TODAS las keyframes a las palabras reales, `setTimelineDuration` exacta, re-exportar las escenas con su audio, completar `voice`/`cuts` (y pausas/SFX/música si corresponde) y volver a armar. Es un cambio de tiempos de todo el video, no un parche.

## Scripts (`pipelines/video-animation/scripts/`)
| script | para qué |
|---|---|
| `assemble_video.py video.json [out.mp4] [--4k]` | arma escenas + transiciones + mezcla de audio + codificación. Reproducido bit a bit contra el armado original (mismo audio, misma duración). |
| `measure_motion.py escena.mp4 x0 y0 x1 y1` | intervalos en que se mueve una zona (agujas de un reloj, un check…) |
| `contact_sheet.py video.mp4 out.png t1 t2 …` | tira de fotogramas en los instantes dados, para mirar con Read |
| `insert_pauses.py` | audio de una escena con micro-pausas entre palabras |
| `make_preview_html.py carpeta` | `preview.html` con `<video>`: calidad baja por defecto, selector de calidad |
| `preflight.py [video.json]` | chequeo previo de dependencias y archivos |
| `helper_palabras.js` | partir un texto en un clon por palabra dentro de `use_figma` (ver notas en `pipelines/video-animation/references/animacion-figma.md`) |

## Reglas que no se negocian
- No modificar los frames originales del storyboard; trabajar sobre clones.
- Iconos = clones de lo que ya existe en el storyboard (instancias del Design System). Nunca `createNodeFromSvg` ni vectores nuevos; si falta un icono, avisar y pedir confirmación.
- El texto en pantalla se deja IDÉNTICO al del storyboard (incluso erratas) aunque no coincida con la voz: es decisión de Nick. Se sincroniza el movimiento con el audio real.
- Nada de pausas largas en la voz (suenan antinaturales): ≤0.08 s dentro de una frase; 1.2 s al final de una escena con el último cuadro congelado ya fue aceptado.
- Nunca push ni commit sin pedido explícito.
- 4K: el video sale de escenas exportadas a 1920 px, así que `--4k` ESCALA (lanczos) y no agrega detalle. Para 4K nativo hay que re-exportar cada escena a 3840 px (y recomponer logos/AE a 3840). Decirlo siempre.
- Reporte final breve, en español, con ids de Figma, tiempos medidos y lo que no se pudo comprobar.
