# Brief por escena (plantilla para subagentes) — y qué NO es aceptable

## Una presentación de diapositivas NO es el entregable
Empujar cada estado completo del storyboard (un clon entero entra, el anterior sale) es una presentación de diapositivas. Nick lo rechazó explícitamente. Eso, solo, **no se entrega como "hecho"**. El storyboard dibuja ESTADOS; el trabajo es animar lo que cambia ENTRE un estado y el siguiente, elemento por elemento, para que la secuencia "complete las ideas" del storyboard. Si no alcanza el tiempo o el presupuesto para hacerlo en todas las escenas, entregá lo logrado como versión parcial, marcala así (no `done` limpio) y decí qué escenas quedaron como empuje simple; nunca presentes un empuje de estados como animación terminada.

## Cómo se animan las transiciones entre estados (la técnica)
1. Para cada par de estados consecutivos (A → B) de una escena, compará elemento por elemento (por nombre y por posición; `use_figma` read-only con x, y, ancho/alto, fills, strokes, opacity, visible):
   - **En A y en B, cambia posición/tamaño/color** → se MUEVE/ESCALA/RECOLOREA ese mismo elemento (TRANSLATION, SCALE, fills/strokes). No se borra y se redibuja.
   - **Solo en B** → ENTRA con movimiento propio según su rol: empuje desde el borde, escala desde su punto de origen, trazo de línea (PATH_TRIM), máscara, rotación/giro (pills), bounce si corresponde. Cada elemento con su tiempo (no todos a la vez).
   - **Solo en A** → SALE con su movimiento (se desplaza fuera, se encoge, se pliega) o es empujado por lo que entra.
   - **Texto** → palabra por palabra con clones (`animacion-figma.md`).
   - Conexiones/flechas/líneas → se trazan (PATH_TRIM) de origen a destino.
2. El estado B del storyboard es el REPOSO final de ese tramo; A es el reposo inicial.
3. Cada escena arranca en el último estado de la anterior y termina en reposo.
4. Hacia el final de cada tramo, lo que importa (la idea del estado) queda un momento en pantalla antes de salir.
5. Fondo distinto entre escenas → transición de color al armar (barrido/círculo/empuje); mismo fondo → continuidad.

## Plantilla de pedido al subagente (una escena o un par por agente; en paralelo)
```
Escena N del storyboard Figma <fileKey>, columna/estados <ids>. Duración exacta <s>.
[Con audio: palabras con tiempos relativos <rs> y silencios. Sin audio: tiempos estimados.]
Reglas: no tocar los originales; sección `Animación – Escena N` en x=-318, y=55000+(N-1)*3000; un frame `EscN – Animación`;
iconos solo clones; texto idéntico y palabra por palabra; parábola cubic-bezier(0.44,0.145,0.01,1) en el movimiento;
técnica de diff estado por estado (references/brief-por-escena.md §Cómo se animan).
Verificá con render bajo (WIDTH 768, fps 10) + contact sheet, ≤3 iteraciones; final 1920/30 fps/high de a 1–2 exports.
Reportá: archivo, duración, qué se animó por elemento, ids Figma, qué no se logró.
```
Cada agente lee `animacion-figma.md` y `reglas-de-nick.md`. El agente principal (o el script) arma el video con `assemble_video.py`. Si no hay subagentes disponibles, hacé las escenas una por una en el mismo orden, sin saltarte la técnica de diff.

## Control de calidad antes de marcar `done`
- Mirá, por escena, un contact sheet de 8–12 cuadros: ¿se ve movimiento de elementos individuales (entradas, trazos, giros) o solo empuje de pantallas completas? Si es lo segundo, la escena no está lista.
- Duración total razonable: ~2.8 palabras/s de locución; el video de referencia fue de 88 s para 10 escenas. Un total > 150 s sin audio es señal de estimación inflada: revisá.
- Reportá con honestidad qué elementos quedaron sin animar.
