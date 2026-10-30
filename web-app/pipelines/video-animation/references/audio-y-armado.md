# Audio y armado del video

## 1. Cortes por escena
- Transcripción con tiempos por palabra (Whisper) + `ffmpeg -af silencedetect=noise=-35dB:d=0.3`. Cortá cada escena en una pausa. Whisper marca tarde (~0.3–0.5 s) la 1ª palabra de cada frase: el inicio real = fin del silencio previo; las `rs` (relativas a la escena) sirven para el resto.
- `cuts` del JSON = [inicio escena 1, fin escena 1 = inicio escena 2, …, fin escena N] en segundos absolutos del WAV (N+1 valores). Si el WAV trae locución antes de la escena 1 (p. ej. un título que se resuelve aparte), `cuts[0]` la deja afuera.
- Si el audio cambia, cambian todos los tiempos: retemporizar por palabras equivalentes, no desplazar.
- Chasquidos sueltos de la locución: `voice_mute: [[a,b]]` (segundos absolutos) los silencia.

## 2. Pausas
`pauses: [{"at": seg_abs, "seconds": s, "hold_scene": n?}]` inserta silencio en la voz en `at`. Con `hold_scene` el último cuadro de esa escena se congela durante la pausa (así quedó 1.2 s tras la escena 4: aceptado). Pausas DENTRO de una frase: ≤0.08 s (Nick rechazó 0.18 s, y 0.08 s aún le pareció notable; terminó en 0.03 s). Si una escena lleva pausas internas, su MP4 se exporta ya con la voz con pausas (`insert_pauses.py`) y su duración incluye esos segundos.

## 3. Transiciones (`transitions`, clave k = entre escena k y k+1)
`[tipo, segundos]`. Tipos: `fade`, `diag` (panel diagonal), `circle` (círculo desde el borde derecho), `sweep` (barrido curvo), `ccenter` (círculo que se cierra hacia el centro), `slide` (empuje lateral), `slidev` (empuje vertical), `band` (sólido de color que se expande del centro hacia los costados, sin fade). `slide`, `slidev`, `ccenter`, `band` usan la parábola; los demás, ease in-out cúbico.
Criterio de Nick: mismo fondo entre escenas → casi sin transición (`fade` 0.1–0.2 o continuidad de elementos); cambio de fondo → barridos. Las transiciones se centran en el corte: la escena anterior se extiende medio tiempo y la siguiente arranca medio tiempo antes (último/primer cuadro clonado), por eso cada escena debe arrancar y terminar en reposo.
Referencia de transiciones (video de After Effects `video vdi.aepx`): panel diagonal, círculo desde el borde, barrido curvo, barras, fundido.

## 4. Efectos de sonido
- `sfx: {"<escena>": [{"f":"Pop 2.wav","at":2.85,"db":-22,"fix":true}]}`; `at` es el instante del PICO del efecto en segundos de la escena. Sin `fix`, el nivel es automático: voz local (RMS ±0.3 s) + 4 dB, entre −16 y −8 dB (los efectos fijos bajos quedaban tapados por la voz).
- Tramo del efecto sincronizado a un movimiento (con loop si el efecto es más corto): `{"f":"Counting Results 02.wav","seg":true,"start":0.43,"dur":1.87,"off":0,"db":-17,"fix":true}` corta seco (fundido 60 ms) cuando el movimiento termina. Medí los intervalos de movimiento con `measure_motion.py`.
- `transition_sfx: {"3":["Whoosh 06.wav",-11]}` pone un whoosh en el corte k→k+1.
- Gustos de Nick: pocos efectos, whooshes preferidos; un efecto largo para una animación corta no sirve (elegí uno cuya duración coincida: `whoosh.wav` 1.1 s para un trazo de 0.95 s); los giros de elementos iguales llevan el mismo sonido; cada sonido acompaña UNA acción visible (aparición, salida), no cada micro-detalle; checks: Digital Button 03 (no Bright Popup/Confirmation).
- Un sonido pertenece a lo que se ve: al mover una animación, mové su sonido (si una aparición se elimina de una escena, quitá su sonido y ponelo donde ahora aparece).

## 5. Música
`music: {"file": "...mp3"}`: loop con crossfade de 2 s, ~20 dB bajo la voz, ducking (−16 dB con voz / −7 dB en pausas), fundido de entrada 2 s y de salida 3 s. Campos: `crossfade`, `idle_db`, `voice_db`, `fade_in`, `fade_out`.

## 6. After Effects (sólo aperturas/logos con alfa)
La apertura con logos se hizo en AE (`AfterFX.exe -m -r script.jsx` en instancia aparte; NUNCA matar procesos de AfterFX: la sesión de Nick está abierta; los scripts abortan si la instancia tiene un proyecto abierto). `aerender.exe` con template "Sin pérdida" ("Sin pérdida con alfa" para alfa). El `.aepx` es XML legible. Los logos con alfa (1920×1080, 60 fps) se componen sobre la base de la escena con ffmpeg (`overlay`, último cuadro congelado). Para 4K nativo habría que re-renderizar esto a 3840.

## 7. Salidas
- `python assemble_video.py video.json out.mp4` → H.264 High, yuv420p, AAC 192k, faststart, 30 fps (CRF 17 por defecto).
- `--4k` → 3840×2160 (lanczos) con el mismo audio. NO es 4K nativo (ver SKILL.md).
- Copia "H264" explícita: `ffmpeg -i out.mp4 -c copy -movflags +faststart out_H264.mp4` (ya es H.264; verificá con `ffprobe`). El bitrate es bajo (~0.5 Mbps) porque las escenas son planos de color; subir `crf` más bajo o recodificar si lo piden (p. ej. YouTube).
- El grafo y el audio intermedio quedan en `_graph.txt` y `_master_audio.wav` junto al JSON.
