# Reglas de Nick para videos animados (las fue corrigiendo escena por escena)

Nick (Cybelesoft) es diseñador, habla español, sin background de programación. Reportar breve y honesto, en español.

## Texto
- Aparece palabra por palabra (ver `animacion-figma.md`), curva (0.16, 1, 0.3, 1), 0.32 s, con máscara por línea. 1ª palabra de cada frase en su tiempo de voz; las siguientes en cascada ≈0.08 s.
- Copy idéntico al storyboard (aunque difiera de la voz). Alinear rótulos con su ícono (un rótulo corrido porque los clones por palabra colapsaron el layout se corrige restaurando el marco del rótulo).
- Un texto de la voz que el storyboard no muestra no se agrega; un texto que sobra (p. ej. "headset just works") se quita cuando Nick lo pide.

## Movimiento
- Todo lo que no es texto/logo usa la parábola `cubic-bezier(0.44, 0.145, 0.01, 1)`.
- Empuje/escala/trazo/máscara antes que fades de imágenes superpuestas.
- Bounce SOLO donde lo pide (ver lista en `animacion-figma.md`).
- Reposos: un estado que explica algo debe quedarse en pantalla un momento (p. ej. usuarios 1 s antes de retirarse) antes de que cambie el fondo/apaguen pantallas; si todo se va "muy rápido", el problema suele ser una salida muy temprana.
- Las salidas de una línea/trazo van despacio (0.8 s, borde que va cambiando el color de lo que pasa).
- Dos cambios sincronizados con el borde de un trazo se calculan con la curva real del trazo.

## Sonido
- Pocos efectos, whooshes preferidos, nivel relativo a la voz, mismo sonido para acciones iguales, sin sonidos para detalles que Nick no marca, sin pausas largas en la voz.
- Música ~20 dB bajo la voz con ducking.
- Si una animación cambia de lugar o se elimina, su sonido se mueve o se elimina con ella.

## Proceso
- No ampliar cambios: lo que se pide en una escena no se aplica a otras (ya pasó con la curva nueva en textos/logos y hubo que revertir).
- Interpretar con cuidado pedidos ambiguos y declarar la interpretación en el reporte ("interpreté 'el desktop' como la ventana del browser").
- Nada de push/commit sin pedido. No tocar archivos Figma de marca. Iconos = instancias del Design System.
- No decir que algo "se ve bien" sin haber mirado fotogramas del MP4; decir siempre qué no se pudo comprobar (reproducción, audio).
