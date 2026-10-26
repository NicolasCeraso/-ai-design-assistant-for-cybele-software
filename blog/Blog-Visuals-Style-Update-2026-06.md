# Cybele Blog Visuals — Style Update v2 · Paleta Reducida (Light / Dark)

> **Tipo de documento:** Enmienda (delta) a `PROGRESS.md` y a las reglas de visuales de blog.
> **Fecha:** 2026-06-03
> **Estado:** Parcial — la paleta y los dos samples son la base confirmada; faltan variables por construir (ver §9).
> **Prioridad:** Este documento PISA las reglas de color de las pipelines de blog (ilustraciones de sección + covers). Todo lo demás de `PROGRESS.md` (canvas, reglas SVG Figma-safe, sistema de íconos, tipografía Inter, layout patterns) sigue vigente sin cambios.

> ## ⚠️ REVOCADO EN PARTE — 2026-09-04
>
> **Los estados semánticos (§5) ya no rigen.** Yanina decidió que las placas de blog no coloreen
> nada "por estado": el color de cada elemento (título, cuerpo, superficie, badge) lo define su
> propia regla en `SECTION_RULES.md`, y no hay una paleta de acentos aparte.
>
> Sigue vigente todo el resto de esta enmienda: superficies planas (light `#EEF4FD` / dark
> `#021425`), la tipografía, los radios, las cards planas y el **retiro de los acentos arcoíris**
> (naranja, púrpura, cian, rosa, lavanda), que era el objetivo original del recorte.
>
> Los colores que §5 había introducido (`#0FAD7E`, `#C6F6E8`, `#0AA9FF`, `#C7EBFF`, `#7B1818`,
> `#FCA5A5`) siguen listados en `BRAND_DESIGN_RULES.md` como colores disponibles — lo que se fue es
> la regla de cuándo usarlos.

> ## ✅ APLICADO — 2026-09-04
>
> Ya no hay que aplicarlo a mano: esta enmienda está **incorporada a las especificaciones**, que son
> lo que se lee al generar. Este archivo queda como el registro de dónde salió la paleta y por qué.
>
> | Qué se aplicó | Dónde vive ahora |
> |---|---|
> | Superficies planas (light `#EEF4FD` / dark `#021425`), tipografía, radios | `skills/cybele-blog-visuals/SECTION_RULES.md` → *Surfaces* |
> | El retiro de los acentos arcoíris | idem → *Accent colours* (los cuatro estados se quitaron el 2026-09-04, ver arriba) |
> | Cards planas, color por estado, radios 7/14/20 | idem → *Cards rules* |
> | ~~Conector con gradiente solo hacia danger~~ | se fue con los estados |
> | Subordinación de la paleta de covers | `BLOG_COVER_RULES.md` §2 (nota al inicio) |
> | Derivados aplicados como tokens de marca | `BRAND_DESIGN_RULES.md` §2 |
> | Los pendientes de §9 | `SECTION_RULES.md` → *Open questions* |
>
> **Lo único que quedó sin aplicar es lo que el propio documento deja abierto** (§9): la re-derivación
> completa de los gradientes de cover, que espera un cover sample en la paleta reducida.
>
> Si cambiás algo acá, no se propaga solo. Editá la especificación.

---

## 0. Qué cambia y por qué

Se **reduce la paleta cromática** de las imágenes de blog. El sistema anterior usaba un set ancho de acentos tipo arcoíris por ilustración (naranja, púrpura, cian, rosa, lavanda, verde…), definido en la pipeline de ilustraciones y en `BLOG_COVER_RULES.md`. El nuevo sistema lo recorta a una paleta **acotada y semántica**: azules/violetas de marca + **un** verde (positivo) + **un** azul brillante (info/neutral) + rojo **solo** para estados de problema, sobre dos superficies (light y dark).

Resultado buscado: mayor consistencia, menos ruido visual, y dos modos (light/dark) bien definidos que se alternan a lo largo de un set, igual que antes — pero con vocabulario de color cerrado.

---

## 1. Fuente

Archivo Figma **"Exercise"** — `fileKey 8RBfhSYgaCuo4uM82JqAHL`

| Nodo | id | Rol |
|---|---|---|
| Paleta cromática | `264:287` | Paleta reducida (6 swatches) |
| Sample light | `264:358` | Modo light aplicado (cheat-sheet / numbered cards) |
| Sample dark | `264:323` | Modo dark aplicado (timeline / flujo horizontal) |

Los samples son ejemplos de **ilustración de sección (DIAGRAM MODE)**, no covers. El recorte de paleta aplica a todos los visuales de blog; el tratamiento de covers se re-deriva de esta paleta (ver §6 y §9).

---

## 2. Paleta reducida — tokens confirmados

### 2.1 Tokens de color (variables Figma)

| Token | Hex | Notas |
|---|---|---|
| `blue/50` | `#EEF4FD` | Superficie light / badges de ícono |
| `blue/900` | `#030C1D` | Azul más oscuro (token) |
| `blue-cybele/900` | `#021425` | **Superficie dark** (usada en el sample) |
| `blue-violet/500` | `#8878ED` | Violeta de marca (uso medido) |
| `blue-violet/700` | `#321BC8` | Violeta profundo de marca |
| `water-green/500` | `#3DCCA1` | Verde decorativo / relleno (token) |

### 2.2 Color "raw" sin variable (a tokenizar)

| Color | Hex | Uso observado |
|---|---|---|
| Azul brillante (info) | `#0AA9FF` | Pill + texto de estado "info / fuera de alcance" (sample light) |

### 2.3 Tipografía (variables)

| Token | Hex |
|---|---|
| `color/typography/title` | `#373737` |
| `color/typography/paragraph` | `#515151` |

### 2.4 Escala tipográfica (variables, Inter SemiBold)

| Token | Definición |
|---|---|
| `title-xl` | Inter SemiBold 75 / line-height 100 |
| `title` | Inter SemiBold 62.28 / line-height 100 |

> Tipografía sin cambios respecto al sistema: **Inter** (Regular 400 / SemiBold 600), nunca itálica, mínimo Regular.

### 2.5 Radios (variables)

| Token | px | Uso |
|---|---|---|
| `border-radius-m` | 7 | Pills / chips |
| `border-radius-l` | 14 | Tarjetas |
| `border-radius-xl` | 20 | Tarjeta destacada (danger card en dark) |

---

## 3. Sistema LIGHT mode (colores aplicados)

Derivado del Sample light (`264:358`).

| Elemento | Color | Token / origen |
|---|---|---|
| Fondo de página | `#EEF4FD` | `blue/50` |
| Tarjeta (cuerpo) | `#FFFFFF` | white |
| Badge circular de ícono | `#EEF4FD` | `blue/50` |
| Glifo de ícono | oscuro, line/outline (`#373737`) | Cybfont light variant |
| Label de categoría | `#515151` | `color/typography/paragraph` |
| Título de tarjeta | `#373737` | `color/typography/title` (Inter SemiBold) |

**Estado positivo (verde):**
- Pill + texto de acento: `#0FAD7E`
- Panel inferior (relleno suave): `#C6F6E8`

**Estado info / neutral-azul:**
- Pill + texto de acento: `#0AA9FF`
- Panel inferior (relleno suave): `#C7EBFF`

> Nota sobre el verde: `water-green/500 #3DCCA1` queda como token **decorativo/relleno**. Para **texto y pills** el sample usa un verde más profundo `#0FAD7E` (mejor contraste sobre blanco). Mantener esa distinción: `#3DCCA1` = decoración; `#0FAD7E` = acento legible.

---

## 4. Sistema DARK mode (colores aplicados)

Derivado del Sample dark (`264:323`).

| Elemento | Color | Token / origen |
|---|---|---|
| Fondo de página | `#021425` | `blue-cybele/900` |
| Disco/nodo neutral | `rgba(255,255,255,0.10)` | white @ 10% sobre navy |
| Texto primario | `#FFFFFF` | white |
| Texto secundario | `#94A3B8` | slate (sub-labels: "FortiOS", "2 GB RAM") |
| Label atenuado | white @ 80% opacity | ej. "Affected Models" |

**Estado de problema / danger (solo para "problema"):**
- Disco circular: `#7B1818`
- Panel de tarjeta: `rgba(123,24,24,0.45)` (= `#7B1818` @ 45% sobre el navy)
- Texto secundario danger: `#FCA5A5`
- Glifo (cancel/✕): blanco, dentro del disco rojo
- Radio de la danger card: `border-radius-xl` (20)

**Conectores (flechas):**
- Peso visual fuerte, color oscuro/slate sobre el navy.
- La flecha **contigua al estado danger** usa gradiente lineal oscuro → rojo (única instancia de gradiente del sample).

---

## 5. Estados semánticos (el corazón del recorte)

La paleta de acentos se reduce a **cuatro estados**, no a una rampa de colores por gusto:

| Estado | Light (acento / panel) | Dark (disco / texto) | Cuándo |
|---|---|---|---|
| Positivo / recomendado | `#0FAD7E` / `#C6F6E8` | verde de marca / — | "recommended", beneficio, éxito |
| Info / neutral-azul | `#0AA9FF` / `#C7EBFF` | azul de marca / — | "out of scope", nota, neutral |
| Neutral (sin estado) | grises tipográficos | `rgba(255,255,255,0.10)` / `#94A3B8` | nodos base, info estructural |
| Problema / danger | (reservar rojo de marca) | `#7B1818` + `rgba(123,24,24,0.45)` / `#FCA5A5` | EOL, riesgo, "removed", alarma |

**Regla:** un visual usa los azules/violetas de marca como base + **a lo sumo** los acentos semánticos necesarios. No introducir hues fuera de esta tabla.

---

## 6. Mapeo old → new (deprecaciones)

Lo que **sale** del sistema anterior de visuales de blog:

| Antes (deprecado) | Ahora |
|---|---|
| Set de acentos arcoíris: `#d97706` (orange), `#7c3aed`/`#a78bfa` (purple), `#06b6d4`/`#38bdf8` (cyan), `#ec4899` (pink), `#c084fc` (lavender) | **Eliminado.** Solo estados semánticos de §5 |
| Tarjetas de colores variados (1 color por card) por variedad | Tarjetas blancas (light) / superficie translúcida (dark); el color lo da el **estado**, no la decoración |
| Fondo dark gradiente `#0b1120 → #0e1726` | Superficie dark plana `#021425` (`blue-cybele/900`) |
| Fondo light gradiente lavanda `#f8f5fc → #f0ecf6` | Superficie light `#EEF4FD` (`blue/50`), tinte azul, plana |
| Gradientes internos suaves en cards | **Fills planos** (consistente con regla de marca "flat solid fills"). Gradiente solo donde el sample lo muestra: flecha→danger en dark |

Lo que **se mantiene** (no tocar):
- Violeta de marca (`blue-violet/500`/`700`) — sigue disponible, uso **medido**, no como color de relleno arcoíris.
- Canvas `1920×1080`, contenido ~70%.
- Reglas SVG Figma-safe (§8).
- Sistema de íconos Cybfont (line/outline), dentro de contenedores circulares.
- Inter SemiBold/Regular, sin itálica.
- Layout patterns: hub-and-spoke, center+features, numbered/symmetric cards, timeline.
- Alternancia light/dark a lo largo de un set.

---

## 7. Secciones de los docs existentes que se ajustan

Aplicar estos cambios sobre los documentos del proyecto:

**En `PROGRESS.md` → "SVG Blog Illustration Pipeline" → tabla "Visual Style Rules (from Figma reference)":**
- Reemplazar fila **Background** dark por `#021425` plano; light por `#EEF4FD` plano (quitar gradientes).
- Reemplazar fila **Accent colors** por la tabla de **estados semánticos** de §5 (eliminar orange/purple/cyan/pink/lavender como acentos libres).
- Body/secundario dark: `#94A3B8`; títulos light `#373737`, párrafo `#515151` (sin cambios, ya alineados a tokens).

**En `PROGRESS.md` → "Design rules established" (sesión 2026-03-27 S4):**
- Regla 2 "Cards with solid fill … Colors from accent palette (#7c3aed, #06b6d4, …)" → actualizar a: cards blancas (light) / translúcidas (dark); color por **estado semántico** (§5), no por paleta de acentos.

**En `PROGRESS.md` → "Blog Cover Generation System" → "Design tokens (colors)" y "Gradient recipes":**
- Subordinar la paleta de covers a esta paleta reducida. Los `gradient recipes` se **re-derivan** solo de azules/violetas de marca + verde/azul de estado; `red-dramatic` se mantiene **solo** para covers de "problema". Marcar el resto como pendiente hasta tener un cover sample (§9).

**En `BRAND_DESIGN_RULES.md` (fallback, no override):**
- No contradice nada: "flat solid fills", "no gradients", Inter sin itálica y badges de ícono siguen siendo coherentes con este update. El `#3DCCA1` (Green) ya figura; agregar como derivados aplicados `#0FAD7E` (verde texto/pill), `#0AA9FF` (info), `#021425` (superficie dark), `#7B1818`/`#FCA5A5` (danger dark).

---

## 8. Reglas SVG (Figma-safe) — sin cambios

Se mantienen idénticas. Recordatorio:

**Permitido:** `<rect>`, `<circle>`, `<ellipse>`, `<path>`, `<line>`, `<polygon>`, `<polyline>`, `<g>`, `<svg>` anidado, `<linearGradient>`, `<radialGradient>`, `<defs>`, `<text>`, `<tspan>`.

**Prohibido:** `<foreignObject>`, `<image>`, base64 data URIs, `<use>` externo, referencias a URL externas.

**Recordatorios clave:** escapar `&`→`&amp;`; IDs prefijados por imagen; `gradientUnits="userSpaceOnUse"`; atributos inline (sin `<style>`/clases); íconos Cybfont embebidos como `<path>` nativos y recoloreados por regex al color de estado.

---

## 9. Pendientes / por confirmar

El usuario aclaró que esto es **parcial** ("no es la totalidad de las variables, lo estamos construyendo"). Quedan abiertos:

- [ ] **Tokenizar `#0AA9FF`** (azul brillante info) — hoy es fill raw, sin variable.
- [ ] Definir nombres de token para los **derivados aplicados**: verde texto `#0FAD7E`, panel verde `#C6F6E8`, panel azul `#C7EBFF`, danger `#7B1818`/`#FCA5A5`, slate `#94A3B8`.
- [ ] Confirmar el **rojo de marca para light mode** (los samples solo muestran danger en dark).
- [ ] Conseguir un **cover sample** con la paleta reducida para re-derivar `gradient recipes` y archetypes de cover.
- [ ] Decidir el rol exacto de `blue-violet/500/700` y `water-green/500` dentro de los estados (decorativo vs. estructural).
- [ ] Confirmar si `blue/900 #030C1D` o `blue-cybele/900 #021425` es la superficie dark canónica (el sample usa `#021425`).

---

## Resumen de un vistazo

```
Superficie    light #EEF4FD   ·   dark #021425
Texto         título #373737  ·   párrafo #515151  ·   dark sec. #94A3B8
Marca         blue-violet/500 #8878ED · /700 #321BC8 · blue/50 #EEF4FD
Estados       positivo #0FAD7E (/panel #C6F6E8)
              info     #0AA9FF (/panel #C7EBFF)
              neutral  rgba(255,255,255,.10) (dark)
              danger   #7B1818 (/panel rgba(123,24,24,.45) · texto #FCA5A5)
Radios        m 7 · l 14 · xl 20      Tipografía Inter SemiBold/Regular
Canvas        1920×1080, contenido ~70%, SVG Figma-safe (sin cambios)
```
