# LinkedIn Carousel (Placas) — Document Type / Pipeline Spec

**Added:** 2026-07-27 · **Rewritten:** 2026-07-29 · **Owner:** Nick Ceraso · **Status:** live
**Pipeline id:** `linkedin-carousel` · **Family:** SVG / Figma (sits next to *Blog visuals*)

> **What this doctype does.** Given the **text of a LinkedIn post**, generate a set of **native,
> Figma-safe SVG placas** (portrait 1200×1500, 4:5) applying Cybele/Thinfinity's LinkedIn carousel
> system, plus an HTML preview. After delivery it also generates **variants** — of a single placa or
> of the whole set — without touching the copy. Same task lifecycle as the other pipelines
> (`queued → ▶ Run → review / ✎ revise → ✓ approve`).

This spec is self-contained: operating from this file alone, Claude can analyse a post, choose the
structure and theme, build the SVGs, self-verify against numeric targets, and produce variants.

---

## 0. How this version was produced (read this before doubting a number)

The 2026-07-27 draft was written from visual impression. On **2026-07-29** the whole reference
library was **measured programmatically**: all 10 carousels / **56 placas**, geometry parsed from the
Figma metadata dump, colour sampled pixel-by-pixel from renders, CVD simulated with the
Viénot–Brettel–Mollon transform.

Four claims in the old draft turned out to be **wrong** and are corrected below:

| Old claim | Measured reality |
|---|---|
| "Cover headline ~56–64 px" | **103.7 px** (DBIR cover, exact CSS) and 114 px (regulatory 2) |
| "Alternate light/navy modes" | Reference carousels use **3–4 modes**, not 2; this rule is what makes output monotonous |
| "Every carousel follows the same 7-beat arc" | Holds in **3 of 10**. The real invariant is `hook → middle → CTA` with 4 middle types |
| "The last placa always carries the Cybele Blogs CTA" | **6 of 10**. Others close on a comment prompt, a resource list, or an honest concession |

Two tokens were **confirmed** by measurement: `NAVY #0A1F3A` (measured #041C3C–#04244C across all 10)
and `CANVAS #EEF4FB` (measured #ECF4FC).

> **Methodological warning for anyone re-running this.** In the Figma metadata, placas are listed in
> **creation order, not left-to-right order** — 6 of the 10 carousels are scrambled, and FSLogix is
> fully reversed. **Always sort placa frames by `x`** before assigning cover/interior/close roles.

---

## 1. Input / Output

| Input | Output |
|-------|--------|
| **Post text**: (a) a *script* with explicit `PLACA 1…N` copy (verbatim), or (b) raw article text to be segmented | **N native SVG placas** at 1200×1500, `<slug>_placa<NN>.svg` |
| (Optional) theme, placa count, structure override | A single **`preview.html`** — horizontal strip, each placa labeled `PLACA n · role · theme` |
| (Optional) variant request (see §10) | `variants/` folder + `variants.html` comparison |
| (Optional) Figma `fileKey` + `nodeId` | After approval: SVGs importable to Figma |

**Language rule (non-negotiable, project-wide):** placa copy is **never translated**. Source language
is preserved verbatim. Only design commentary is localized.

A typical input script looks like this (real example, DBIR 2026):

```
LinkedIn Posts
POST 1 · Verizon's DBIR 2026 - Edge device exploitation
Agregar link en comentarios: https://blog.cybelesoft.com/dbir-2026-edge-device-exploitation/

CAPTION
<the LinkedIn caption, with hashtags — NOT placa copy, do not render it>

PLACA 1 <copy>
PLACA 2 <copy>
...
LOGO CYBELE BLOGS
```

The `CAPTION` block is the post body on LinkedIn, **not** placa content — never render it onto a
placa, and **never mine it for headlines either** (see §3.7). `Agregar link en comentarios` names the
article the CTA placa points to.

---

## 1b. The verbatim contract (decided 2026-07-29 — read before writing any text)

**No word may be added, removed, or altered.** Every word that appears on a placa must appear in the
script's `PLACA` blocks. This is a hard constraint, mechanically audited in §11.

This was an explicit decision by Nick, taken with full knowledge that the reference library does
**not** work this way. Measured against the DBIR script, the reference designer preserved ~70% of the
words but also reordered sentences, rewrote a lead into an imperative, and **added three things that
exist nowhere in the script**: the cover headline *"Device Exploitation Hits 22% of Breaches"*, the
chart axis dates *"Nov. 2024 / Nov. 2025"*, and the closing question *"Are you still trying to patch
your way out?"*.

**Those additions are not available to this pipeline.** Nick keeps authorship of the copy; the
pipeline gets typography and composition. See §3.7 for exactly what latitude remains, and §3.6 rule 2
for how the pipeline surfaces a stronger cover *without* writing it.

---

## 2. Source references (provenance)

- **Reference library:** Figma **"Exercise"** file `8RBfhSYgaCuo4uM82JqAHL`, section **`281:2156`**
  ("Linkedin Blog Posts") — 10 finished carousels. Per-carousel node ids: regulatory post 1
  `270:9859` · regulatory post 2 `270:10155` · FortiOS `270:10404` · Section 1 / NOC `301:2598` ·
  DBIR 2026 `270:11587` · Citizens/Frost `287:823` · z/Scope `287:984` · desktop prices `287:1090` ·
  parallels `301:1789` · FSLogix `301:2232`.
- **Reference implementation:** `web-app/deckgen/linkedin_carousel/build_svgs_v2.js`
  (`node build_svgs_v2.js [output-dir]`).
- **Superseded draft:** an earlier 2026-07-27 draft of this spec existed outside the repo.
  **This file is authoritative.**

---

## 3. Editorial structure

### 3.1 The invariant

Every one of the 10 references follows exactly this and nothing more:

```
HOOK  →  MIDDLE (2–5 placas)  →  CTA
```

Length: 4–7 placas, **median 6** (measured distribution: 4,4,5,5,6,6,6,6,7,7). The arc, not a fixed
count, drives length.

### 3.2 The four middle types

All the variety lives in the middle. Pick **one** and commit:

| Middle type | Shape | Used by | Colour consequence (§5) |
|---|---|---|---|
| **Linear argument** (5/10) | trigger → problem → mechanism → proof | DBIR, Frost, prices, z/Scope, FortiOS | no coding — house blue |
| **Enumeration** (1/10) | N near-identical category placas | regulatory 1 (4 audit artifacts) | one colour per category |
| **Contrast** (2/10) | Before/After, or Option A/Option B | regulatory 2, FSLogix | two colours |
| **Dimension comparison** (2/10) | one table/grid of N dimensions, then the mechanism | NOC, parallels | no coding, or one accent |

**The middle type determines the colour mechanism.** These are not two separate decisions — pick the
structure, and §5 tells you the palette that follows from it.

### 3.3 The invariant reframe

Any sector event → *the durable fix is architectural = Thinfinity Workspace*. Value props to lean on:
**browser tab · no agent · no inbound ports (reverse-connect) · session recording = audit evidence ·
white-label**. The hook never opens on the product.

### 3.4 CTA types (the close is not always the blog)

| CTA type | Count | Example |
|---|---|---|
| Blog CTA — "Read the breakdown at Cybele Blogs" + `CYBELE \| Blogs` lockup | 6/10 | DBIR, prices, z/Scope |
| Comment prompt — "Drop a comment!" / "Comment to see a demo" | 2/10 | FortiOS, NOC |
| Resource list | 1/10 | FSLogix — "Remediation commands. Model-choice triggers. Honest limits." |
| **Honest concession** | 1/10 | parallels — "When is Parallels still the better fit?" |

Default to the blog CTA when the script ends with `LOGO CYBELE BLOGS` or names an article link. Use a
comment prompt when the script itself asks a question. The concession close is reserved for
competitor-comparison posts and is a deliberate credibility move — keep it available.

### 3.5 Word budget (measured, hard limits)

| Role | Median | Range | Rule |
|---|---|---|---|
| **Cover** | 18 | 12–26 | **Never exceed 26 words.** No reference does. |
| **Interior** | 50 | 16–122 | Above ~90 the placa needs a table/grid, not paragraphs |
| **Close** | 23 | 16–41 | |

If the script's copy for a placa exceeds the range, **split the placa** — do not shrink the type.

### 3.6 Editorial rules (mandatory)

1. **Generate, don't clone.** Compose an original layout. Pick **one governing visual metaphor** tied
   to the post's thesis and carry it across placas. Never reproduce a reference post's composition —
   the library calibrates the *system*, not the layout to copy.
2. **The cover leads with the number — if the script gives one.** When the cover block contains a hard
   statistic, that fragment takes the `display` step and the narrative sentence demotes to the subhead.
   **When it does not, the pipeline may not invent one** (§1b).

   **This note is conditional — do not emit it on every run.** Raise it in `NOTES.md` *only* when the
   cover block has no figure **but the post has one elsewhere** (another `PLACA` block, or the
   caption). If the post contains no hard figure at all, say nothing: there is no better cover
   available and the note would be pure noise.

   > *"PLACA 1 has no hard number. The strongest reference covers lead with one (DBIR: 'Device
   > Exploitation Hits 22% of Breaches'). The post's number — 22% — appears in PLACA 2 and in the
   > caption. Consider revising the script's PLACA 1 if you want the cover to carry it."*

   It is a **suggestion, not a failure**: it blocks nothing, and it is unrelated to the
   `verbatim_check.js` gate (§11), which only fails on actual contract violations. Authorship stays
   with Nick; the pipeline just points at the option.
3. **One focal per placa.** One idea, one dominant visual.
4. **Copy verbatim — see the contract in §1b and the latitude in §3.7.** No word added, removed or
   altered.
5. **No diagram on the cover.** Diagrams are interior material (see §7.2).

### 3.7 What the pipeline may and may not do to the copy

**Free — these are typographic decisions, not editorial ones:**
- Line breaks, and which word takes the accent colour.
- Which fragment of the block becomes the headline, the body, the caption — i.e. assigning type steps
  and spatial position. The script gives a paragraph; something has to be the title.
- Splitting a compound sentence into bullets **at its own existing punctuation or conjunction**, with
  no words added. Punctuation may be adjusted at the split point only (a comma becoming a colon or a
  full stop). *Log every split in `NOTES.md`.*
- Emphasis: bold, size, colour.

**Forbidden:**
- Adding any word — including headlines, kickers, eyebrow labels, chart axis labels, units, dates,
  closing questions, or CTA phrasing not present in the script.
- Removing or paraphrasing any word, including turning a phrase into an imperative
  (*"It's removing the inbound listener"* → *"Remove the inbound listener"* is a **rewrite**, not a
  line break).
- **Reordering the script's sentences within a placa.** Reading order follows the script.
- Mining the `CAPTION` block for any on-placa text.
- Inventing diagram labels. If a diagram needs a label the script does not supply, the diagram is
  wrong for this copy — change the diagram, not the copy. *(A generated attempt added `OUTSIDE`,
  `INBOUND LISTENER`, `YOUR NETWORK`, `THE TRIGGER` — none are in the script. All four are now
  violations.)*
- Repeating the same figure twice on one placa. *(The same attempt printed `3%`, `22%` and `7x` twice
  each on placa 2.)*

**Structural text that is exempt** (it is chrome, not copy, and is fixed by the brand): the
`CYBELE | Blogs` lockup wordmark, and the article URL when the script supplies it.

**When the copy will not fit the composition, the composition yields.** Never shrink type below the
ladder (§6.1) and never trim a sentence to make it fit — split the placa (§3.5) or change the layout.

---

## 4. Themes

Three themes. Nine of the ten references live in the first two; the third is a rare register shift
for posts about something being removed, deprecated or forcibly migrated.

| Theme | Background | Primary | Accents | Use |
|---|---|---|---|---|
| **claro** | `#ECF4FC` + `#FCFCFC` | navy `#0A1F3A` (as text) | `#3484CC` · `#5CACF4` | comparisons, cost, calm explanation |
| **navy** | `#FCFCFC` outer, navy field | `#0A1F3A`–`#04244C` (15–37% of canvas) | `#2494FC` · `#0C74D4` · `#5CACF4` | authority, security, covers, CTA |
| **oscuro** | near-black `#040C1C` | `#040C1C` | maroon `#3C0C0C` | loss / removal / forced migration (1 of 10 — do not overuse) |

A carousel picks **one theme** and varies *modes within it* (§7.4). Theme is not a per-placa choice.

### 4.1 Token map (this is what makes theme variants mechanical)

**The generator must emit colours from this token table, never hardcoded hex.** A full-theme variant
(§10) is then a table swap, not a re-draw.

| Token | claro | navy | oscuro |
|---|---|---|---|
| `BG` | `#EEF4FB` | `#0A1F3A` | `#040C1C` |
| `BG_ALT` | `#FFFFFF` | `#14335C` | `#0C0C24` |
| `SURFACE` | `#FFFFFF` | `#10294D` | `#1A0E0E` |
| `INK` | `#0F2233` | `#FFFFFF` | `#F2F2F2` |
| `INK_MUTED` | `#5B7089` | `#9FB0C6` | `#9A8F8F` |
| `PRIMARY` | `#0A74D6` | `#5CACF4` | `#C0C6CF` |
| `ACCENT_A` | `#E8452A` | `#E8452A` | `#3C0C0C` |
| `ACCENT_B` | `#1A7FE0` | `#7FC0FF` | `#8A9AA8` |
| `HAIRLINE` | `#D4E4F4` | `#2B4A6F` | `#2A1A1A` |

---

## 5. Colour semantics and colour-vision accessibility

**Accessibility is a requirement of this doctype, not a nice-to-have.** Every palette decision below
was tested by simulating protanopia, deuteranopia and tritanopia and measuring CIE ΔE and chroma
retention.

### 5.1 The finding that drives everything

The brand's `red = Before / green = After` pair **remains distinguishable** under CVD (worst ΔE 30) —
but **green stops being green**. Measured chroma retention for deuteranopes:

| Green | Chroma | Deuteranope sees | Retention |
|---|---|---|---|
| `MINT #3DCCA1` | 49 | `#ADADA4` | **10%** |
| `SAVINGS #1AA778` | 49 | `#8C8C7B` | 20% |
| measured `#14BC8C` | 52 | `#9D9D8F` | 15% |

Red survives (chroma 80 → 64). So ~6% of men see **"dark olive vs light grey"** where the design
intends **"danger vs good"**. The distinction survives; the meaning does not.

### 5.2 Rules

1. **The Before/After pair is red vs blue, not red vs green.**

   | Pair | Worst ΔE | Both keep their colour? |
   |---|---|---|
   | `#E8452A` / `#1AA778` — old | 30 | **no** (56% / 20%) |
   | **`#E8452A` / `#1A7FE0` — use this** | **105** | **yes** (56% / 57%) |

   3.5× the separation, and blue is the brand colour — this is more on-brand, not less.

2. **If a green is genuinely needed** (savings, money), use **teal `#0B6E7F`** (61% retention) or
   **cyan `#00A3C4`** (72%). Never `#3DCCA1` or `#1AA778` as a load-bearing signal.

3. **Colour never carries meaning alone.** Every semantic colour is paired with a redundant cue: an
   icon, a label, a number, or position. This is the only rule that fully solves the problem.

4. **Enumeration of 4+ categories cannot be solved by hue.** Best achievable is ΔE 23 (ambiguous) with
   navy/amber/blue/purple; even Okabe-Ito — the reference CVD-safe palette — only reaches 17. So for
   enumeration the **number and label carry identity and colour is decoration**. The reference already
   does this (`01 Multi-Factor Authentication`); it is now a rule, not an accident.

5. **Avoid blue-vs-green as an A/B pair.** It collapses in tritanopia (ΔE 7). Low priority —
   tritanopia is ~0.008% of the population — but amber/blue is free and better.

6. Accent semantics after these rules: 🔴 red `#E8452A` = danger / Before / VPN / breach · 🔵 blue
   `#1A7FE0` = the durable fix / After / Thinfinity · 🟠 amber `#E8912A` = the second option in an A/B ·
   🟣 purple = category coding only · teal `#0B6E7F` = savings.

### 5.3 The 3% accent rule

Measured across all 10 carousels: the chromatic accent never exceeds **3.2%** of a placa's area
(green 1.9–3.2% · red 0.4–2.4% · purple 1.3% · maroon 0.9%). Blue is the exception because it is
structural, not accent (up to 16%).

> **An accent covering more than ~3% of the placa has stopped being an accent.** This is the
> measurable form of the project's golden rule: *less is more*.

---

## 6. Typography

### 6.1 The scale — six steps, no others

Measured single-line type across 56 placas clusters at 26–32 / 40–44 / 56–64 / 68–76 / 104–114. The
ladder is therefore:

| Step | px | Weight | Use |
|---|---|---|---|
| `display` | **104** | 600–700 | cover headline **only** |
| `title` | **72** | 700 | interior placa headline |
| `subtitle` | **60** | 600 | secondary headline, big numbers in body |
| `body` | **40** | 400–500 | paragraphs |
| `small` | **32** | 500 | dense tables, captions |
| `label` | **26** | 600 | eyebrow pills, axis labels, footers |

**Hard limits: at most 6 distinct sizes in a carousel, at most 4 in a placa, and no size outside the
ladder.** *(A generated attempt used **15** sizes from 20 to 66 with 2 px increments — that is a
continuum, not a scale, and it is why nothing read as hierarchy.)*

- **Inter** only (Regular 400 / Medium 500 / SemiBold 600 / Bold 700–800). No faux-bold, no Light.
- Cover headline: line-height ≈ **1.18×** size, tracking ≈ **−0.01em** (measured: 103.7 px / 122 / −1.037).
- Titles ≤ ~7 words per line; break lines deliberately.
- Exactly **one word** in the headline takes the accent colour.

### 6.2 The cover is typographic, not decorative

Reference cover anatomy (DBIR, exact values): eyebrow pill `rgba(255,255,255,.25)`, radius 50,
padding 30/20, text 32 px · headline **103.7 px** at x=96, y=349, width 840 · subhead **55 px** Regular
at 90% opacity · logo lockup **565×88** at x=96, y=1356, sitting on a `#EFF7FE` panel radius 30.

Left margin **96 px** on covers; **100–130 px** top margin on interiors (measured cluster). Margins in
the current generator are already correct — **do not change them.**

---

## 7. Composition

### 7.1 Fill and text share (measured targets)

"Fill" = share of the canvas covered by content boxes, background excluded, on a 20 px grid.

| Role | Fill | Text share | Icons |
|---|---|---|---|
| Cover | **61%** | 50% | 1 |
| Interior | **46%** | **65%** — interiors are the most typographic, not the most illustrated | 3 |
| Close | **54%** | 43% | 2 |

Overall target ≈ **50% fill**. *(A generated attempt averaged 32% — visibly empty.)*

### 7.2 Cover archetypes — three bands, pick one and land in it

| Archetype | Fill | Text share | Description |
|---|---|---|---|
| **magra** | 29–40% | 56–89% | type floating in air, almost nothing else |
| **media** | 62–64% | 30–62% | type plus one supporting shape |
| **panel** | 87–88% | **20–37%** | a large decorative gradient panel fills the canvas |

Panel covers are **always** low-text — when the panel dominates, the text share drops. **Do not land
between bands.** *(A generated cover measured 29% fill / 32% text: as empty as a *magra* but with as
little type as a *panel* — the worst of both, and the reason it read as weak.)*

### 7.3 The close is the most constructed placa

It averages **three times** the graphic elements of an interior. It is a built object, not a text
slide: article-thumbnail card + `CYBELE | Blogs` lockup + decorative panels.

Reference close anatomy (DBIR): headline block at x=112, y=140, width 976 — a small question line
(~28 px) above a large CTA headline · thumbnail card **1088×401** containing the real article cover
image **525×296**, a ~12 px kicker, a ~40 px title · lockup **462×106** (Cybele logo 267 wide, divider,
"Blogs").

> **Thumbnail decision (2026-07-29):** `<image>` stays forbidden (§8). The CTA card renders a
> **placeholder rect** at the correct size and radius, which Nick fills in Figma. Never embed a raster.

### 7.4 Rhythm — the relationship between consecutive placas

Adjacent placas differ in text share by a mean of **25 points** across the reference (46 transitions).
Per carousel the mean ranges 8–55; the most characterful sets are the most contrasty (DBIR 55,
parallels 39, Frost 33) and the flattest are the least memorable (regulatory 2 = 8).

**Honest limit:** this is a tendency, not a law — 26% of reference transitions are also low-contrast,
so "every placa must contrast with its neighbour" would be false.

Rules:
- **At least two hard swings** (|Δ| ≥ 40 in text share) per carousel.
- Use **3–4 modes** within the theme across the set, not 2. *(The old "alternate light/navy" rule
  produces exactly 2 and is the direct cause of flat output.)*
- The cover normally breaks with a field of its own rather than being one more interior.
- **Exception — enumeration:** category placas are *deliberately identical* (measured |Δ| of 1–4).
  That is correct. The contrast rule applies to narrative middles, not enumerated ones.

### 7.5 Grid

**There is no rigid grid — the grid is flexible** (Nick, 2026-07-29). What is fixed: the canvas, the
edge margins (§6.2), and the metrics in §7.1. Everything inside is composed per placa.

### 7.6 Component vocabulary

**Golden rule: less is more.** The kit is a menu, not a checklist — use whatever the content actually
needs and nothing else. Available: pill/tag labels · numbered circles (`01–04`) · check bullets and
warning triangles · compliance badges (NERC CIP / DORA / NIS2 / HIPAA / GDPR) · Before/After node
diagrams (laptop / gateway / broker / HMI / PLC / SCADA) · the Audit-Question→Artifact `?—✓`
connector · donut and bar charts · line charts with real axes · week-timeline and cost-line bars ·
article-thumbnail card.

**Data deserves a real chart.** The DBIR reference draws an actual curve with axes and labelled
endpoints (3% Nov 2024 → 22% Nov 2025); a generated attempt reduced the same data to two flat bars.
If the copy contains a trend, draw the trend.

**Use brand icons, never hand-drawn primitives.** Reference placas instance named icons: `hacker`,
`user`, `remote`, `insecure-transfer`, `not-locked`, `target`, `no-listener`, `no-vpn`, `lock-check`,
`rev-tunnel`, `alert`. Icon framing is consistent: a **116 px** frame containing a **68 px** icon
(inset 24).

> **Known gap:** only about half of those exist locally. `brand-icon-lib.js` (131 icons, in the web
> app) has `hacker`, `user`, `remote`, `remote-app-mode`, `lock-check`, `shield-ok`, `gateway`,
> `broker`, `firewall`, `perimeter-based`, `vpn-tunnels`, `VPN-alert`, `rec`… but not `not-locked`,
> `target`, `insecure-transfer`, `no-listener`, `rev-tunnel`, `alert`. Use the nearest brand
> equivalent; build a geometric substitute only as a last resort, and say so in `NOTES.md`.

---

## 8. SVG authoring (Figma compatibility)

Unchanged and still correct — these rules are what make the placas import as editable vectors.

- **Canvas:** `viewBox="0 0 1200 1500"`, 60–96 px edge padding.
- **Allowed:** `<rect> <circle> <ellipse> <path> <line> <polygon> <polyline> <g> <svg>
  <linearGradient> <radialGradient> <defs> <text> <tspan>`.
- **Forbidden:** `<foreignObject>`, `<image>`, external `<use>`, base64 data URIs, external URL refs,
  `<style>` / CSS classes.
- All copy in native `<text>`; escape `&`→`&amp;`, `<`→`&lt;`. Typographic `'` for apostrophes.
- **Prefix every gradient/id per placa** (`p1-bg`, `p6-thumb`, …) — shared ids silently break fills.
- `gradientUnits="userSpaceOnUse"` with explicit coords.
- **Logos/icons as `<path>`**, not `<image>`. When loading a brand SVG: strip the outer `<svg>`,
  **replace `var(--fill-…, #hex)` with the plain `#hex`**, drop internal `id=`/`style=`, then wrap in
  `<g transform="translate(x y) scale(s)">` with `s = targetWidth / viewBoxWidth`.
- Place logos by fixed height, derive width from the true ratio (`thinfinity 200.985:50.966`,
  `thinfinity_white 165.615:41.997`, `cybele 231:88`). **Never distort.**

---

## 9. Build recipe

**Language:** Node.js, built-ins only (no `npm install`).

1. **Analyse the script** → identify hook / middle / CTA, choose the **middle type** (§3.2), the
   **theme** (§4), the **governing metaphor**, and the **cover archetype** (§7.2). State all four in
   `NOTES.md` before drawing.
2. **Load brand assets** with a fallback resolver — real asset if present, else a generated
   substitute; never block the build. Apply the `var()`→hex + id-strip cleanup.
3. **Emit from the token table (§4.1), never hardcoded hex.** This is what makes §10 cheap.
4. **Compose each placa** (bg → metaphor/graphics → text → lockup), ids prefixed.
5. **Write** `<slug>_placa<NN>.svg`.
6. **Emit** `preview.html` — horizontal strip, each placa labeled `PLACA n · role · theme`.
7. **Self-verify (§11), iterate, then report.**

**Environment:** system Python `C:\Python314` is broken — this pipeline is Node-based. If Python is
ever needed use `py -3.13`. Render/verify with Edge headless:

```powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless=new --disable-gpu `
  --hide-scrollbars --window-size=<W>,<H> --default-background-color=00000000 `
  --screenshot="<out>.png" "file:///<preview>.html"
```

---

## 10. Variants (post-delivery)

Once a version is delivered and reviewed, Nick can ask for **variants**. A variant explores an
alternative *design* for copy that is already settled.

### 10.1 The line between a variant and a revision

| | Copy | Output location |
|---|---|---|
| **Variant** | **frozen — never changes** | `output/v<N>/variants/` inside the *current* version |
| **Revision** | may change | a **new** `output/v<N+1>/` |

If a request would change a word, it is a revision, not a variant. Say so and bump the version.

### 10.2 Variant axes

Move **one axis at a time** unless asked otherwise — that is what makes variants comparable.

| Axis | Scope | What changes | What must not |
|---|---|---|---|
| `theme` | whole set | swap the §4.1 token table | layout, copy, metaphor |
| `cover` | placa 1 | switch archetype band (§7.2) | copy, theme |
| `metaphor` | whole set | the governing visual | copy, theme, structure |
| `rhythm` | whole set | redistribute fill / text share (§7.4) | copy, theme, metaphor |
| `accent` | whole set | swap the semantic pair (§5.2) | everything else |
| `layout` | one placa | rearrange the same copy | copy, theme, type scale |
| `cta` | last placa | switch CTA type (§3.4) | the article being pointed to |

### 10.3 The two scopes Nick asks for

**Single-placa variants** — *"dame variantes de la placa 3"*
Produce **3** by default, labelled `a`/`b`/`c`, moving the `layout` axis:
```
output/v<N>/variants/placa03-layout-a.svg
output/v<N>/variants/placa03-layout-b.svg
output/v<N>/variants/placa03-layout-c.svg
```
Each must hold the same copy, the same theme, the same type ladder, and land within the §7.1 fill
band for its role. They should differ in **composition**, not decoration: change what is the focal,
where the metaphor sits, whether the data becomes a chart or a table.

**Full-theme variants** — *"mostrame el carrusel en tema claro"*
Re-render **all** placas with a different token table:
```
output/v<N>/variants/theme-claro/<slug>_placa01.svg …
```
Because §9.3 forces token-based emission, this is a table swap. Two things still need judgement and
must be re-checked, not assumed:
- **Contrast** — re-run the §11 checks; a colour legible on navy may fail on `#EEF4FB`.
- **Cover archetype** — a *panel* cover built for navy usually needs a different gradient in `claro`.

### 10.4 Preview and reporting

Every variant run emits **`variants.html`**: the original in the first row, each variant in its own
row beneath, same order, labelled with the axis and value. Report which axis moved, and give a
one-line reason per variant — the point is to make a choice easy, not to produce options.

### 10.5 Defaults

- No count given → **3** variants.
- No axis given → `layout` for a single placa, `theme` for a whole set.
- Never generate variants of a variant. Always branch from the delivered version.

---

## 11. Verify — mandatory before reporting done

Render headless, read the PNGs, and check. The numeric ones are measurable; do not eyeball them.

**Numeric**
- [ ] Fill ≈ 50% overall — cover ~61%, interiors ~46%, close ~54% (§7.1)
- [ ] Cover lands **inside one archetype band**, not between (§7.2)
- [ ] Cover ≤ 26 words; interiors 16–122; close 16–41 (§3.5)
- [ ] ≤ 6 distinct type sizes in the set, ≤ 4 per placa, all on the ladder (§6.1)
- [ ] Cover headline at `display` 104 px, and it contains the post's hard number (§3.6)
- [ ] ≥ 2 adjacent transitions with |Δ text share| ≥ 40 (§7.4) — unless the middle is enumeration
- [ ] 3–4 modes used within the theme, not 2 (§7.4)
- [ ] No chromatic accent exceeds 3% of any placa (§5.3)

**Accessibility**
- [ ] No red/green pair carries meaning; Before/After is red/blue (§5.2)
- [ ] Every semantic colour has a redundant cue — icon, label, number or position (§5.2 rule 3)
- [ ] Enumerated categories are numbered, not colour-only (§5.2 rule 4)

**Figma-safe**
- [ ] No `<foreignObject>` / `<image>` / base64 / external URLs
- [ ] All text native `<text>`; `&` escaped
- [ ] Logos/icons native `<path>`; no `var(--…)` left in fills
- [ ] Ids prefixed per placa; gradients in `<defs>`
- [ ] `viewBox 0 0 1200 1500` on every file
- [ ] Logos undistorted (width derived from the true ratio)

**Editorial**
- [ ] **Verbatim audit passes with zero unmatched words** — run it, do not eyeball it:
      `node web-app/pipelines/verbatim_check.js <script.txt> <output-dir>`
      It extracts every `<text>`/`<tspan>` from the placas and reports any word absent from the
      script's `PLACA` blocks, plus any figure printed twice on one placa. **Exit code 1 = do not
      deliver.** See §1b / §3.7.
- [ ] Source language preserved (never translated)
- [ ] The `CAPTION` block was not rendered onto any placa, nor mined for headlines
- [ ] Middle type, theme, metaphor and cover archetype are stated in `NOTES.md`
- [ ] Every bullet split is logged in `NOTES.md` (§3.7)
- [ ] If the cover has no figure **and the post has one elsewhere**, `NOTES.md` raises it — otherwise
      it stays silent (§3.6 rule 2). This is a suggestion; it never blocks delivery.

---

## 12. Assets

- **Local (Claude Code / Desktop):**
  - `BRAND_DIR = web-app/deckgen/brand_assets` — `thinfinity_logo.svg`, `thinfinity_logo_white.svg`,
    `cybele_logo.svg`, `cybele_logo_white.svg`. Prefer the **`.svg` white variants** on navy — the
    `_white.png` rasters are legacy and actually blue.
  - **`brand-icon-lib.js`** in the web app (131 icons, one JSON
    map, `currentColor`) — the richest source. See §7.6 for the coverage gap.
  - **Icon fill note:** brand icons use `fill="#0A74D6"`; some are outline-style with a secondary
    `<path>` inheriting `fill="none"` → **force the fill** when embedding or the shape renders empty.
- **Web sandbox (claude.ai):** no local disk — upload the assets, or fetch from Figma via
  `get_design_context(nodeId, fileKey, excludeScreenshot=true)`. File keys: Design System
  `x0HMD1pXkcYdFM7NSaBvb4` · brandbook `y7mHflD4ukCFDo6YsPzIf4` · LinkedIn/atoms
  `8RBfhSYgaCuo4uM82JqAHL`.

---

## 13. Key decisions (rationale)

- **Portrait 1200×1500, 4–7 placas** — native LinkedIn document format; the arc drives length.
- **Governing metaphor per post > reusing a reference layout** — the explicit guard against
  clone-by-retrieval.
- **`hook → middle → CTA` replaces the 7-beat arc** — the 7-beat version described 3 of 10 carousels
  and forced the other 7 into a shape they do not have.
- **Six-step type ladder** — the reference works in few large steps; a continuum of 15 sizes reads as
  no hierarchy at all.
- **Red/blue instead of red/green** — 3.5× the CVD separation, both colours keep their identity, and
  blue is the brand colour. Accessibility and brand agree here.
- **Colour is never the only cue** — the only rule that survives all three CVD types, and the only way
  to enumerate 4+ categories at all.
- **Token-based emission** — the precondition that makes full-theme variants a table swap.
- **Borderless / low-contrast / Inter** — inherited brand rule, keeps placas consistent with every
  other Cybele surface.
- **Node + Edge-headless verify** — no npm, no Python, and a screenshot check catches distortion,
  wrong mode and hidden metaphor before hand-off.
- **Strict verbatim over the designer's re-casting (Nick, 2026-07-29).** The reference library rewrites
  and adds copy; this pipeline may not. Nick keeps authorship of the words, the pipeline gets
  typography and composition. The cost is accepted and explicit: when the script's cover block has no
  hard number, the cover cannot lead with one — the pipeline flags it instead of fixing it.
- **The contract is machine-checked, not trusted.** `verbatim_check.js` is what turns §1b from an
  intention into a gate. Auditing the first generated carousel against its own script found **17
  invented words, 3 altered forms and 4 duplicated figures** — including caption-mined phrasing that
  no reviewer had noticed.

---

## 14. Changelog

- **2026-07-29 (b)** — Copy policy decided: **strict verbatim** (option A). Added §1b (the contract)
  and §3.7 (allowed vs forbidden), rewrote §3.6 rules 2 and 4, tightened the CAPTION rule from
  "don't render" to "don't render or mine", and added the mechanical audit `verbatim_check.js` to
  §11. Recorded that the reference designer does *not* work this way, and what that costs.
- **2026-07-29** — Rewritten from measurement of all 56 reference placas. Corrected the type scale,
  the editorial arc, the mode-rhythm rule and the CTA claim. Added: themes with measured palettes,
  the CVD section, fill/text-share targets, cover archetypes, word budgets, the 3% accent rule, the
  token table, and the variant system (§10). Recorded the x-ordering gotcha.
- **2026-07-27** — First draft, written from visual impression.
