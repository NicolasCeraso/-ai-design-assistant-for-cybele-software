# Animar una escena en Figma (motion API) — lo aprendido

## Preparación
- Herramientas Figma son deferred: cargalas con ToolSearch (`create_session,get_metadata,get_screenshot,use_figma,export_video`). Cargá los skills `figma-use`, `figma-use-motion`, `figma-generate-design` y pasá `skillNames` en cada `use_figma`. `create_session` con el `fileKey` antes de cualquier otra herramienta.
- `get_metadata` del frame grande puede devolver cientos de miles de caracteres: no lo uses. Inspeccioná con `use_figma` read-only (hijos por id, depth 2).
- Cada escena = una COLUMNA de frames 3840×2160 (estados clave de arriba abajo), con textos "VO n" y "Guion". Verificá el orden mirando cada frame (`get_screenshot`): los nombres no son confiables, guiate por la posición x y el contenido.
- Sección por escena `Animación – Escena N` en posición FIJA (x=-318, y=55000+(N-1)*3000) para no pisarse entre agentes en paralelo. Un solo frame animado top-level por escena (`EscN – Animación`).
- Estrategia: clonar el frame del primer estado, traer (clonar) lo que sólo aparece en estados posteriores y animar hacia los estados siguientes comparando posiciones/colores/opacidades por nombre. Cada estado del storyboard es un estado de reposo.
- Cada escena debe ARRANCAR en el estado final de la anterior y TERMINAR en su reposo final (sin fundir a negro). Si el storyboard cambia un estado, revisá la escena anterior y la siguiente.

## API (lo que funciona)
- `node.applyManualKeyframeTrack({type:'PROPERTY', name:'TRANSLATION_X'|'TRANSLATION_Y'|'OPACITY'|'SCALE_X'|'SCALE_Y'|'ROTATION'|'WIDTH'|…}, {keyframes:[{timelinePosition:seg, value:{type:'FLOAT',value:n}, easing:{…}}]})`
- TRANSLATION/ROTATION/SCALE son ADITIVAS respecto del reposo (0 / 1 = sin cambio); OPACITY, WIDTH y HEIGHT son absolutas. El primer keyframe se sostiene hacia atrás hasta t=0, el último hacia adelante. No animar el frame top-level, sólo descendientes.
- `SCALE_XY` exige VECTOR: usá `SCALE_X` y `SCALE_Y` por separado.
- Easing válidos: EASE_IN, EASE_OUT, EASE_IN_AND_OUT, LINEAR, EASE_*_BACK, GENTLE, QUICK, BOUNCY, SLOW, HOLD, CUSTOM_CUBIC_BEZIER (`easingFunctionCubicBezier:{x1,y1,x2,y2}`). NO existe `EASE_IN_OUT`.
- Colores: `node.manualKeyframeTracks = {...existing, fills:{...(existing.fills??{}), 0:{keyframes:[{timelinePosition:t, value:{type:'COLOR', value:{r,g,b,a:1}}, easing}]}}}` (idem `strokes`), valores 0–1.
- Trazado de línea: `PATH_TRIM_START` / `PATH_TRIM_END` sobre vectores (una máscara de trazo); su curva real no es lineal: para sincronizar otras cosas con el borde del trazo, calculá con la curva.
- Duración: `const [tl]=frame.timelines; frame.setTimelineDuration(tl.id, seg)` con la duración EXACTA de la escena (fin − inicio de sus cortes; incluye pausas insertadas).
- Rotación "sobre el eje z": ROTATION. Giro 3D (rotateY): SCALE_X 1→0→1 intercambiando el contenido a mitad (dos clones con opacidad HOLD).
- Clones de vectores dentro de grupos quedan en x=0,y=0: copiar x/y del original.
- Dos keyframes de una misma pista en el mismo instante rompen: separalos unos 0.02–0.07 s.
- Un `use_figma` que falla se revierte completo.

## TEXTO: palabra por palabra con clones (el exportador NO escalona TextStagger)
`export_video` renderiza TextStagger como un bloque. Solución obligatoria: una capa clon por palabra.
1. Quitar tracks/animationStyles del texto original. Para cada palabra k: `t.clone()`, mismo lugar, y `setRangeFills(otras palabras, [])` (conserva los fills originales de la palabra visible, p. ej. acentos). Agrupar como `WORDS: <capa>`; el original queda `visible=false` con el copy completo. (`scripts/helper_palabras.js`)
2. Cada palabra dentro de un frame contenedor con `clipsContent=true`, fills=[], del tamaño EXACTO de su línea (alto = lineHeight); el clon va en (0,0) del contenedor (multilínea: un contenedor por palabra con y = y_texto + fila·lineHeight y el clon en y = −fila·lineHeight).
3. Animación (valores medidos del AE de referencia, preset "Slide & Pop In"): OPACITY 0→1 y TRANSLATION_Y +12 % de la altura del cuadro → 0 (260 px en 2160), MISMA curva y duración, arrancan juntas: 0.32 s, `CUSTOM_CUBIC_BEZIER {0.16,1,0.3,1}` en ambos keyframes de ambas pistas. Compuerta HOLD 0 antes de tIn.
4. Tiempos: la 1ª palabra de cada frase arranca en su tiempo de voz (fin del silencio previo); las siguientes en cascada rápida de ≈0.08 s entre palabras, independiente de la voz. Salida: OPACITY→0 en 0.25 s o junto con el elemento que se desplaza (empujado fuera); nunca fundido de bloque lento.
5. El copy queda IDÉNTICO (mismas mayúsculas, incluso erratas). Un typo se corrige sólo si Nick lo pide (`insertCharacters/deleteCharacters` en original y clones).
Los textos y las apariciones de logos usan SU curva (la de arriba), NO la parábola.

## Easing del movimiento: la "parábola"
Todo el movimiento que no es texto ni logo usa `cubic-bezier(0.44, 0.145, 0.01, 1)` (velocidad pico al ~27 %; arranca rápido y desacelera largo). Aplicala a todas las keyframes salvo HOLD/LINEAR. En el armado, las transiciones de empuje usan la misma curva (`easing` del JSON).

## Bounce de entrada
Pedido por Nick para: entrada del browser/desktop (esc. 4), del elemento MFA (esc. 4), de la laptop (esc. 10). Receta: el elemento llega con overshoot de ~4–6 % del recorrido (p. ej. 60–80 px en un recorrido de 1500–1800) y asienta en ≈0.3 s; el estado final no cambia. Sólo donde se pida.

## Preferencias de movimiento
- Empuje / escala / trazo / máscara antes que fades de imágenes superpuestas. Entre escenas del mismo fondo no hay transición drástica (continuidad y empuje).
- Salidas: los elementos se desplazan fuera de cuadro con los siguientes entrando; los textos acompañan a sus elementos.
- Ecualizador/barras de audio: envolvente real de la voz de la escena, cada barra con su banda, ~15 fps, SCALE_Y (no animación artificial).
- Lupa con aumento: clon del contenido escalado 1.6–2× dentro de un contenedor circular con clip que acompaña a la lupa.
- Logos: revelación desde una línea vertical hacia el "+"; las aperturas con After Effects se hacen aparte (ver `audio-y-armado.md` §6).

## Exportar la escena
1. Bajo para iterar: `export_video` con `constraint {type:'WIDTH', value:768}`, `quality:'low'`, `fps:10` → frames con ffmpeg → mirarlos. Hasta 2–3 iteraciones; agrupá todos los arreglos antes de re-renderizar.
2. Final: `fps:30`, `quality:'high'`, `constraint {type:'WIDTH', value:1920}`. Si devuelve `jobId`+`processing`, re-llamar con `{fileKey, jobId}` cada 10–15 s hasta tener `downloadUrl`; bajar con `curl.exe -s -f -L -o silent.mp4 "<url>"`.
3. Sumar el audio recortado: `ffmpeg -y -loglevel error -i silent.mp4 -ss <inicio> -t <dur> -i "<wav>" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest Escena_NN.mp4`. El AAC suma ~0.06 s (no importa: el armado recorta por duración exacta).
4. `get_screenshot` muestra SOLO el reposo; el movimiento se ve exportando y mirando cuadros.
