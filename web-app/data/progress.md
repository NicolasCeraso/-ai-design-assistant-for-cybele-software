# Cybele AI Design Assistant — Progress Report

**Last updated:** 2026-06-10
**Project:** AI-assisted branded document and design generation for Cybele Software

---

## Project Vision

Build an AI-powered system that enables the Cybele design team to:

1. **Brand documents** — Take unbranded content and produce branded PDFs/PPTX
2. **Generate illustrations** — Create article illustrations following brand guidelines, export to Figma as SVG
3. **Generate blog covers** — Produce on-brand hero images for blog articles following a reverse-engineered visual system
4. **Generate architecture diagrams** — Produce Thinfinity product architecture diagrams as native Figma-compatible SVG in the official Cybele "pill" visual system
5. **Co-design in Figma** — Push and iterate designs directly in Figma via MCP integration
6. **Web App for the team** — A shared interface so all team members can leverage these capabilities

---

## Infrastructure Setup

### MCP Servers

| Server | Type | Capability | Status |
|--------|------|------------|--------|
| `claude.ai Figma` | Cloud | Read designs, screenshots, metadata | Authenticated |
| `figma-remote-mcp` | Local | Read + **write** designs (`generate_figma_design`) | Authenticated |

### Figma-to-Design Workflow

Established pipeline for pushing HTML/CSS designs into Figma:

1. Generate HTML/CSS in `~/dashboard/`
2. Serve locally with `http-server`
3. Add Figma capture script
4. Call `generate_figma_design` with `outputMode: existingFile`
5. Poll `captureId` until completed
6. Iterate via `get_design_context` for reading back from Figma

### Python Environment

- Python 3.14.3 with key packages:
  - `python-pptx 1.0.2` — PPTX generation
  - `PyMuPDF 1.27.1` — PDF reading and image extraction
  - `Pillow 12.1.1` — Image processing
  - `Playwright` — Chromium headless for HTML→PDF conversion and Figma captures
  - `weasyprint 68.1` — HTML→PDF (installed but requires GTK/Pango native libs on Windows)
  - `lxml` — SVG validation during cover generation

---

## Brand System

### Sources Analyzed

| Source | File Key | Content |
|--------|----------|---------|
| Cybele Brandbook | `y7mHflD4ukCFDo6YsPzIf4` | Full brand manual (screenshot) |
| Cybele Design System | `x0HMD1pXkcYdFM7NSaBvb4` | Colors, Typography, Icons, Grid, Logos, Components |
| 9 Whitepaper designs | Various | Document branding patterns |
| PPT Template PDF | Local | 44+ slide type templates |
| 21 Blog covers | `sample portadas.pdf` | Hero image visual system (reverse-engineered 2026-04-17) |

### Brand Tokens Extracted

> **Note — primary blue reconciled (2026-06-11):** the **official primary is `#0A74D6`** (Cybele Brandbook in Figma, file `y7mHflD4ukCFDo6YsPzIf4`). The 06/26 deck work adopted `#0F7FE0` as primary, but per the Brandbook that value is **superseded — use `#0A74D6`**. The other 06/26 tokens (NAVY `#0A1A2F`, CANVAS `#EEF4FB`, MINT `#3DCCA1`, etc.) still stand. ✅ Deck code reconciled 2026-06-11: `build_pptx.py` already used `#0A74D6` (via `brand_config.json`); the `enterprise_vdi_oci_esp` scripts (`build_deck.js`, `render_icons.py`, `render_diagram_icons.py`, `render_for_critique.py`) were updated `#0F7FE0` → `#0A74D6`.

**Colors (previous canonical, until 06/26):**
- Primary Blue: `#0A74D6`
- Navy (covers): `#0B1A3B`
- Dark Text: `#373737`
- Body Text: `#515151`
- Light BG: `#F0F4F8`
- Accent Green: `#3DCCA1`
- Oracle Red: `#C74634`
- Full palette scales: Blue Cybele, Thinfinity, Blue Violet, Purple, Pink, Red Cybele, Orange Cybele, Yellow, Green, Water Green (50-900 each)

**Typography:**
- Primary: **Inter** (Regular 400, Medium 500, SemiBold 600, Bold 700)
- Secondary: Titillium Web (brandbook), Arial (fallback)
- Icon font: Cybfont (custom, not yet installed locally)
- Brandbook text styles (extracted from Figma node `926:1192` etc.):
  - **Main title**: Inter SemiBold 600, 40px/53px, `#0A74D6`
  - **Section**: Inter Medium 500, 26px/38px, `#373737`
  - **Subtitle**: Inter Regular 400, 22px/35px, `#373737` (blue arrow prefix)
  - **Paragraph**: Inter Regular 400, 17px/27px, `#515151`
- Responsive: CSS clamp values for Desktop and Mobile typescales

**Breakpoints:**
- Mobile: < 768px
- Tablet: 768px – 1360px
- Widescreen: > 1360px

### Whitepaper document pattern

- **Cover:** navy gradient background, badge/tag, white title, logos bottom-left.
- **Interior:** white bg, blue H2 titles, gray body, circled icons for feature lists.
- **Back cover:** CTA card, contact info, copyright footer with Cybele logo.

Detailed patterns for **Presentations (PPTX)** and **Blog covers** live in their respective pipeline sections below.

---

## Logo & Icon Assets

### Logos (`brand_assets/`)

**Usage rule:** the **default is the branded (blue) variant**. The **white** variant is used **only when the background's contrast does not allow legibility of the blue** (e.g., dark navy backgrounds, saturated gradients, blue-dominant photography).

| File | Variant | Size | Use |
|------|---------|------|-----|
| `cybele_logo.png` | Cybele blue on transparent | 700x260 | **Default** |
| `thinfinity_logo.png` | Thinfinity blue on transparent | 900x240 | **Default** |
| `thinfinity_logo_white_real.png` | True white on transparent | 900x240 | Only on dark / saturated backgrounds |
| `cybele_logo_white.png` | _Legacy — actually blue_ | 700x260 | DEPRECATED. Use `cybele_logo.png` (default) |
| `thinfinity_logo_white.png` | _Legacy — actually blue_ `RGB(0,125,193)` | 900x240 | DEPRECATED. Use `thinfinity_logo_white_real.png` for genuine white |
| SVG versions | `.svg` for all above | Vector | |

External: `Oracle_logo (2) 1.png` (5484x709, red)

### Icons (`icons_png/`, 200x200 RGBA each)

`audit-log`, `broker`, `cloud`, `dollar-sign`, `enterprise-ztna`, `gateway`, `gpu-fast`, `lock-check`, `no-vpn`, `pc`, `remote-work`, `scale`, `search`, `shield`, `stats`, `user`, `vdi`

Each has a `_white.png` variant for use on dark/colored backgrounds.

SVG originals available in `icons/`.

### Console brand library (web app, 2026-09-28)

What the console's **Brand assets** view shows. It is separate from the `cybele_deckgen` assets above.

- **Files:** all five brand files are **SVG** (`web-app/data/brand-assets/`), exported from the Figma
  Design System (`x0HMD1pXkcYdFM7NSaBvb4`, page "Logos"):
  - `oracle-logo.svg`: the ring-over-wordmark from the icon set;
  - `thinfinity-icon.svg`: the white isotype, `thinfinity-logo-square` Versión=Negativa;
  - `thinfinity-logo-white.svg`: logo "Original", Versión=Negativa.

  Nick's rule: keep SVG as the source and rasterise only when a use needs it.
- **Icon library:** 574 icons (`brand-icon-lib.js`).
  - **Sources:**
    - 535 from the Design System frame "Cyb Font" (`8120:7263`), light variant, or the closest
      variant when an icon has no light one;
    - 38 legacy Cybfont icons that aren't in Figma under that name;
    - 1 icon drawn for the console in the light style, `attach` (the paperclip, `data/icons-custom/`).
  - **Leaves out** any icon whose Figma name says "no se usa".
  - **Grouping:** the console's own **11 categories** (`data/icon-categories.json`); the Figma file is
    never reorganised.
  - **Search:** by meaning, in Spanish and English (`data/icon-keywords.json`).
  - **Updates:** there is no Figma token (Nick's "plan B"). Claude syncs through its own Figma
    connection by comparing fingerprints (RUNBOOK §5).
- **Console UI icons** use the brand set:
  - the task status glyphs: `clock`, `check`, `alert-s`, `question`, `cancel`; the spinner stays drawn;
  - Run (`play`) and Stop (`cancel`);
  - attachments (`attach`).

### Sourcing assets across environments (Desktop/CLI · web sandbox)

> **Applies to every pipeline below.** The asset *files* above (logos, `icons_png/`, and the 131-icon arch set) are **local-filesystem resources** — they exist only on the machine where this project lives. The build code is identical across surfaces; **only the source path changes**. This note exists so that, operating from this `.md` alone, Claude knows how to obtain and embed them regardless of where it is running.

**Where the files come from, per surface:**

- **Local — Claude Code (CLI) or Claude Desktop** (both run on the user's machine with full local-filesystem + local-tool access). Files are on disk; point the build straight at them — no upload, highest fidelity. This is the default path and the one the session logs below assume:
  - `BRAND_DIR  = cybele_deckgen/brand_assets`
  - `ICONS_PNG  = cybele_deckgen/icons_png`
  - `ARCH_ICONS = skills/thinfinity-architecture/icons` in the console repo — the source of truth since 2026-09-28; `~/.claude/skills/thinfinity-architecture/` is a mirror of it (for diagram pills)
- **Web sandbox — claude.ai (web/app chat).** Runs in a cloud container with **no access to the local disk**: only chat-**uploaded** files land in `/mnt/user-data/uploads`, and only **remote** connectors are reachable (a *local* MCP such as `figma-remote-mcp` is **not**; a hosted Figma connector is). Two options:
  1. **Upload** `brand_assets/` + `icons_png/` + the pill SVGs, then point the build at the upload dir.
  2. **Fetch from Figma** via the hosted connector + `get_design_context(nodeId, fileKey, excludeScreenshot=true)` → native SVG (see "Cybfont iconography"). File keys: Design System `x0HMD1pXkcYdFM7NSaBvb4` · brandbook `y7mHflD4ukCFDo6YsPzIf4` · arch atoms `8RBfhSYgaCuo4uM82JqAHL` · 131-icon lib `W3Pnm739iwmVdo3hSaBNQe`.

  If neither is available, **fall back** to generated substitutes and say so — never block the build on missing brand files.

**Embedding rules (all environments):**

- **Resolve with fallback** so the build never breaks: use the real asset if present, else the generated substitute (`assets/ic_*` chips, `assets/dg_*` pills). One code path, two sources.
- **Logos:** place by a fixed height and derive width from the real aspect ratio (`cybele 700:260`, `thinfinity 900:240`, `oracle 5484:709`) — never distort. Default blue; white only on dark/saturated backgrounds. *Known gap:* there is **no genuine white Cybele** (the `_white` file is actually blue) → on navy, use a text wordmark or a light chip until a true-white asset exists.
- **Icons:** pptxgenjs embeds **PNG** most reliably → rasterize brand SVGs with `sharp` at high density. For diagram **pills**, the icon takes the **pill's colour**: `#0A74D6` in Thinfinity pills, `#373737` in every other pill, Active Directory and TLS included; green / violet are only for environment zones (architecture skill §2.2b and §6, Nick 2026-09-28 — this replaces the old "icon keeps its native brand color" rule).

> Expanded step-by-step (drop-in `logoImg()`, `chip()`, `pill()` with the fallback resolver, plus the icon-name → brand-asset mapping) lives in the **branding-assets runbook** kept alongside this report.

---

## PPTX Generation Pipeline

> **Two paradigms of this pipeline coexist by design**, chosen by **source-document format**:
>
> - **Source is a text format** (DOCX / TXT / MD / Google Docs / etc.) → use the **from-scratch generator** (`python-pptx`, one builder function per slide).
> - **Source is a rendered artifact** (PDF / PPTX / image) → use the **faithful pipeline** (Node / pptxgenjs, `enterprise_vdi_oci_esp/`, see below). The older python-pptx "brand-a-source" route with a 2-slide cover/closing template was retired (2026-10-26) and its template no longer exists.
>
> Slide count is dynamic, dictated by source content. Closing-slide language always matches the source — the closing is `cierre.pptx`, transplanted byte-for-byte in structure with its text translated.

### Architecture diagrams in a deck (all three paths, 2026-09-28)

Every Thinfinity architecture diagram in a deck is drawn as **native, editable PowerPoint shapes that look like the Architecture diagram task's output**. It is the same system, not a deck variant.

**Where the rules come from.** Nick reviewed deck task `task-1790624980817` ("test 09/28/2026", 54 slides, 30 diagrams) and accepted v3 after two rounds:
- *"esperaba que los gráficos de arquitectura quedaran más parecidos a los que se generan desde la task de arch diagrams"*
- *"las puntas de flecha … están algo raras, pero en líneas generales, los gráficos funcionan mejor"*

Everything in the `thinfinity-architecture` skill (repo copy `skills/thinfinity-architecture/`) still applies; below is what the slide adds. The accepted builder is the reference implementation. Reuse its `ARCHITECTURE ENGINE v2` section (≈ lines 330–720) instead of writing a new engine: `presentations/reference_builder/build_script.py` (+ `_cybele_icons.py`).

- **Units and size.**
  - Lay the diagram out in the skill's units:

    | Element | Size |
    |---|---|
    | Pill | 160×43 |
    | Zone label band / side pad / bottom pad | 48 / 20 / 24 |
    | Gap between containers | 43 |
    | Vertical stride between stacked pills | 54 |

  - Scale the whole scene **once, uniformly**, to fit its card: 90–100 % of skill size, and about 80 % at the lowest for dense component maps.
  - Centre it. Never stretch a diagram to the slide width.
- **Pills.**
  - White fill, 1.5 px stroke, label **Inter 12 regular** (not bold), icon 23 px at (10, 10).
  - The icon takes the pill's colour: `#0A74D6` in Thinfinity pills, `#373737` everywhere else (AD, TLS and security included). Green and violet are only for environment zones.
  - Rejected: 172×50 pills with bold labels.
- **Zones.**
  - Dashed gray network zones, labelled with the zone's icon + **title case** in Inter Medium 13 `#373737` ("Remote Access", "DMZ", "Identity"). Rejected: uppercase labels without an icon.
  - Environment zones (dashed intense stroke on a soft fill) appear only where the source names the hosting: customer `#3DCCA1`/`#F5FCFA`, cloud `#8878ED`/`#F9F8FE`, hosted by Cybele `#0A74D6`/`#EFF7FE`. Network zones sit inside them; users stay outside.
- **Topology.**
  - Arrows point **toward the Gateway**: users → Gateway, Broker → Gateway, resources → Broker.
  - Protocols go in **wire pills on the line** ("TLS 1.3 / Port 443", "Outbound-only TLS / No Inbound Port"), never floating text with leader lines. Ports and firewall tables only when asked (`skills/thinfinity-architecture/reference/ports_and_firewall.md`).
  - Resources → Broker converge on **one bus**, with one chevron per broker.
  - The IdP goes in its own **Identity** zone, linked by a dashed authentication line.
  - Z-order: zones → connectors → pills.
- **Arrowheads.**
  - Never use PowerPoint's built-in arrow line end: it has a wide mitred head and the shaft runs through it, so it reads like a spear.
  - Draw the skill's open chevron (`M2 2 L11.5 9 L2 16`) as **its own open freeform**: 9.5 px deep, 14 px tall, 2 px stroke in `#0AA9FF`, round caps and joins, scaled with the diagram.
  - The tip stops **4 px before** the target, and the line stops 1 px short of the tip.
  - The last straight run is ≥ 14 px.
  - Connectors are straight, 2 px, in `#0AA9FF` (1.5 px when dashed), with square caps at the corners.
- **Card and reference.**
  - Each diagram sits on a **white card** (radius 14 px), whatever the slide's background mode. Diagram slides are white anyway.
  - The **reference goes inside the card**, above its bottom edge, **in the deck's language**. It holds:
    - the blue arrow with the same chevron;
    - the gray dashed zone;
    - the dashed secondary flow, if the slide has one;
    - one swatch per environment colour the slide uses.
- **Text.**
  - Measure every label with the real Inter metrics (e.g. PIL + `Inter-Regular.ttf` / `Inter-Medium.ttf`). Report any pill label wider than 160 − 39 − 6 px, or any zone label wider than its zone.
  - Shorten the wording to fit ("Backup Site · Sec. LM", "DMZ · Port 443"); never shrink the type or widen a pill. List the edits in NOTES.md.
  - All copy is live text. The only images are the brand icons, as PNG rendered from the skill's SVGs in the pill's colour.
  - Inter / Inter Medium only, no shadows. Pills and zones keep their strokes: they are the skill's atoms, not content cards.

### From-Scratch Editorial Generator — `build_pptx.py`

**Deck:** *VDI & VDA para Universidades* — Cybele commercial proposal, editorial style **(palette 06/26)**, 13.33×7.5" widescreen. Slide count is dynamic per source document. Output for this test case: `VDI_VDA_Universidades_v3.pptx` (10.6 MB, 27 slides for this specific source).

**Paradigm shift vs the older pipeline:** the deck is authored entirely in code (no source PPTX is branded). Every shape, card, and text run is placed by a per-slide builder function. Dimensions stay at **native 13.33×7.5"** (not downscaled to 10×5.625") so the transplanted closing slide drops in without scaling.

**Design tokens** (`build_pptx.py`, "DESIGN TOKENS" block) — the **06/26 palette** (supersedes the older `#0B1A3B` navy). **Primary blue note:** 06/26 used `#0F7FE0`, but the primary was **reverted to the Brandbook `#0A74D6` on 2026-06-11** (see the note under §"Brand Tokens Extracted"); the table below still shows the values hardcoded in the deck code, which need updating to `#0A74D6`:

| Token | Hex | Role |
|---|---|---|
| `NAVY` | `#0A1A2F` | Dark-mode background |
| `CANVAS` | `#EEF4FB` | Light-mode background (very light blue) |
| `BRAND_BLUE` | `#0A74D6` | Primary — Brandbook-official (2026-06-11; was `#0F7FE0` in 06/26, superseded). Deck code still hardcodes `#0F7FE0` — update separately. |
| `BLUE_LIGHT` | `#5BAFFF` | Accent on navy |
| `MINT` | `#3DCCA1` | Bullet dots, positive accent |
| `ORACLE_RED` | `#C74634` | Negative accent, "VPN tradicional" tag |
| `TEXT_PRIMARY` | `#2E2E2E` | Body text on canvas/white |
| `TEXT_SECONDARY` | `#6B7280` | Descriptions, subtitles |
| `TEXT_ON_NAVY_MUTED` | `#A8B0BC` | Muted text on navy |
| `FOOTER_TEXT` / `DARK_FOOTER_TEXT` | `#CCCCCC` / `#4A6A90` | Low-contrast footer (intentional) |
| `DARK_CARD` | `#122542` | Card fill on dark slides (borderless) |

**Typography:** Inter **Light / Regular / Medium / SemiBold** only. `set_run()` maps `bold=True` + `font="Inter"` to **Inter SemiBold** (no faux-bold, no Thin/ExtraLight).

**Card system (borderless, shadowless, constant-radius):**
- `add_card_white` (light mode), `add_card_dark` (`DARK_CARD` fill, navy slides), `add_card_brand` (solid brand-blue, used for "the solution" on comparison slides).
- **No borders** — cards are distinguished purely by fill contrast (white on canvas, `DARK_CARD` on navy).
- **No shadows** anywhere in `ppt/slides/` (audit = 0 `outerShdw`/`innerShdw`/`reflection`/`softEdge`).
- **Constant absolute corner radius:** `CARD_RADIUS_EMU = 22860` (= 0.025"). `add_rect`'s `radius_emu` parameter recomputes `radius_frac` per shape so the *visual* radius is identical regardless of container size.

**Dark-mode mix (~22%, dispersed):** roughly 1-in-5 slides are dark (navy bg + `DARK_CARD` containers + white/muted text), spread throughout the deck rather than clustered. Concrete distribution depends on the source content.

**Dynamic footer numbering:** `_count_slide_builders()` counts the `build_slide_*` functions in the module and overwrites `TOTAL_SLIDES` at `build()` time. `add_footer(slide)` infers the 1-based index from `prs.slides` and the total from `TOTAL_SLIDES` (pass `dark=True` on navy slides). Cover and closing carry no standard footer (each has its own bottom design). Add or remove a `build_slide_*` and the whole deck re-numbers automatically.

**Closing-slide transplant** (`replace_slide27.py`) — preserves a hand-made closing slide pixel-identically without inheriting the deck's theme:
1. Inserts the source `cierre.pptx` slide **byte-for-byte**.
2. Copies its **entire layout → master → theme chain** (e.g. `slideLayout1 → slideLayout12`, `slideMaster1 → slideMaster2`, `theme1/theme2 → theme2/theme3`), rewriting all internal `_rels` references.
3. Registers the new parts in `[Content_Types].xml`, `presentation.xml.rels`, and `presentation.xml`.
4. Copies the closing's media with a `cierre_` prefix to avoid collisions.
5. Runs **`force_white_hyperlinks()`** — rewrites `<a:hlink>`/`<a:folHlink>` in the transplanted themes to `FFFFFF` (otherwise PowerPoint paints every `<a:hlinkClick>` run in Office-blue `#0563C1`, overriding the hardcoded white).
6. **Language rule:** preserves visual structure byte-for-byte but **translates text content to match the source-document language**.

**Build commands:**
```bash
cd pptx_work
python3 build_pptx.py                 # → output/<deck>_v3.pptx
python3 replace_slide27.py            # transplant cierre → output/<deck>_v3_with_cierre.pptx
# Verify:
cd output && rm -f *.pdf slide-*.jpg
soffice --headless --convert-to pdf <deck>_v3_with_cierre.pptx
pdftoppm -jpeg -r 80 <deck>_v3_with_cierre.pdf slide
```

**Quality gate:** shadow audit = 0 across `ppt/slides/` (themes carry ~20 latent effect refs that don't affect the render); slide size = `12191969 × 6858000` EMU (13.33×7.5"); footer spot-check confirms first and last slides are footer-less and the rest read `NN / TOTAL`.

**Key decisions (rationale):**
- **Theme transplant > link-stripping** for hand-made closing slides — preserves pixel-identical output where stripping `<a:hlinkClick>` runs from a rebuilt slide could not.
- **Constant absolute corner radius** via per-shape `radius_frac` keeps every container visually consistent regardless of size (avoids the "bigger box ⇒ rounder corner" artifact).
- **Contrast-only cards** (no borders, no shadows) carry the editorial look; mode is signaled by `DARK_CARD` vs white fill, not by strokes.

**Assets** (in `assets/`): `lockup_thinfinity_oracle.png`, `cybele_isologo.png` (white, cover), `bg_navy_cover.jpg`, `bg_navy_closing.jpg`, and `cybele_icons/` (63 PNGs = 21 Figma icons × 3 variants, consumed by `add_icon(name, variant=...)`).

### Faithful Brand-a-Source Reproduction (Node / pptxgenjs) — `enterprise_vdi_oci_esp/` (2026-06-10)

A **second PPTX path**, in **Node.js + `pptxgenjs`** (not python-pptx). Use it when the source is a rendered artifact (PDF) that must be reproduced **faithfully** — verbatim copy, same structure — **and** its architecture diagrams must become **native editable shapes**. (The from-scratch generator authors copy editorially; the python-pptx brand-a-source path swaps a cover/closing template; this path transcribes the source 1:1 and draws the diagrams natively.) Deliverable: *Enterprise VDI on OCI · Discovery Demo (ESP)* — 39-page source PDF → **40-slide** Google-Slides `.pptx`. Working dir `cybele_deckgen/enterprise_vdi_oci_esp/`; build: `node build_deck.js` → `python swap_closing_slide.py` → `python render_for_critique.py`.

- **Verbatim copy** — every title/bullet/table transcribed from the source; source language preserved (English cover tagline stays English, Spanish body stays Spanish) per the preserve-source-language rule. No editorial rewriting.
- **Inter rendering fix (root cause of "washed-out" text):** only the *variable* Inter font was installed locally, which PowerPoint/LibreOffice render hairline-thin. Fix = install Inter **static** weights (Regular/Medium/SemiBold/Bold) to user fonts (`%LOCALAPPDATA%\Microsoft\Windows\Fonts` + HKCU `Fonts` registry). Google Slides resolves Inter weights natively regardless, so it only affected local renders/desktop PowerPoint.
- **Render/verify loop** — `render_for_critique.py` uses **PowerPoint COM** (real PowerPoint, not LibreOffice) → PDF → PyMuPDF JPGs + `slides_preview.html`. ⚠ The machine's default Python at `C:\Python314` is **broken** (missing stdlib `encodings`); use **Python 3.13** (`%LOCALAPPDATA%\Programs\Python\Python313\python.exe`) for every script here.
- **Native architecture diagrams (12)** — *(historical: the rules for any deck are now "Architecture diagrams in a deck" above)* — scale-driven JS engine applying the **construction rules** of the `thinfinity-architecture` skill (see that section): uniform **160×43 px-ratio pills** (one pill width per diagram → each diagram is a clean zoom of the same system), gap = one pill-height, **edge-centered orthogonal connectors** with ≥14 px straight run before each chevron, dashed zones, layer order. Icons rendered from the skill's 131-icon SVG set to PNG via `render_diagram_icons.py` (blue / dark / white). `centerDiagram()` post-shifts each diagram to **center it on x/y** within the slide body (clamped to clear the title and never overlap the footer); specs-panel slides center only the topology in the upper region.
- **Cover** — emulates a co-branded reference cover: solid navy, outlined eyebrow badge, bold hero title, muted subtitle, bottom divider, **Thinfinity + Oracle Cloud** lockup bottom-left + **Cybele** bottom-right. Logo **aspect ratios preserved** (no distortion) via a `LOGO_AR` table; co-brand logos equal height, Cybele larger — the reference's size proportions are respected.
- **Closing** — `cierre.pptx` swapped at the XML level (`swap_closing_slide.py`); the **animated GIF is retained** for this deck (motion wanted), superseding the earlier static-PNG substitution. Deck ≈ 11 MB with the GIF.
- **Background-mode system** — content slides split ≈ **⅓ light `#EEF4FB` · ⅓ white `#FFFFFF` · ⅓ dark navy**, dispersed (per-slide `SLIDE_MODE` map + mode-aware theme object `TH` driving every builder). Hard rules override the split: diagram slides are **always white**; **no dark slide immediately before/after a section separator** (except the closing); cover / section dividers / Q&A / closing are dark by design and excluded from the count.
- **Color rules** — **no vibrant `#0F7FE0` in containers**; accent containers use a **low-contrast** fill (soft `#DCE8F8` on light, muted `#1C3E63` on dark); `#0A74D6` only for the table header row; vibrant brand blue reserved for **details** (title text, bullet dots, diagram-pill strokes). **Containers are borderless** (flat fill); low container-vs-background contrast throughout.
- **Footer** — alludes to the document title + the **Thinfinity + OCI** binomial (else "Cybele Software"); on **content slides only** (removed from cover / dividers / Q&A / closing); thin rule + page number; ≥10 px safety margin so no content invades it.

> Diagram **pills (colored stroke)** and **dashed zones** keep their borders — they are the skill's atoms, not "content containers" — as does the cover's outlined badge.

---

## PDF Whitepaper Pipeline (stable)

Converts a DOCX with long-form content into a branded multi-page PDF. Stable since 2026-03-27 and reusable across documents.

**Single-command invocation:**
```bash
cd web-app/deckgen
python whitepaper/build_whitepaper.py <input.docx> [output.pdf]
```

**Pipeline (4 stages in `cybele_deckgen/whitepaper/`):**
1. `generate_wp_pages.py` — DOCX → paginated HTML pages (795×1125 px each, matching the reference Figma whitepaper).
2. `redesign_wp.py` — applies Figma-reference CSS + content transforms: labeled items (blue title + description), bullet lists with separators, callout boxes (`#EEF4FD` bg + blue border), pro/con check items (green `#3DCCA1` / red `#E04040`).
3. `generate_cover_closing.py` — generates cover (navy gradient + badge + white title + Thinfinity/Cybele logos) and closing (CTA box with blue gradient + contact info + navy footer). Cover title auto-extracted from the DOCX (`Title` / `Heading1` style → first non-empty paragraph → filename fallback). Language coherence: closing translated to match the source.
4. `generate_pdf.py` — renders the HTML pages to PDF via Playwright + PyMuPDF and merges.

**Page count is dynamic** — driven by the source DOCX's pagination, not by a pipeline constant. Typography uses the brandbook text styles extracted from Figma (Inter SemiBold 600 titles `#0A74D6`, Inter Regular body `#515151`, scaled 0.55× to the 795 px page width).

**Figma upload (optional):** the same HTML pages can be uploaded to a Figma frame via `figmaselector=#capture-target`, which constrains the capture region to the exact 795×1125 frame.

---

## SVG Blog Illustration Pipeline

> **The rules moved (2026-09).** How a blog visual looks is no longer described here. Both blog
> deliverables are produced by the Claude skill **`cybele-blog-visuals`**, and each has exactly one
> specification, inside that skill's folder:
>
> | Deliverable | Specification |
> |---|---|
> | In-article section illustrations | `SECTION_RULES.md` |
> | Cover / hero image | `BLOG_COVER_RULES.md` |
> | Brand tokens both share | `BRAND_DESIGN_RULES.md` |
>
> This section used to be a third copy of those rules and had already drifted from them — that is why
> it is a pointer now. **Do not re-add design values here.** To change how a visual looks, edit the
> spec; there is one place per rule.

### What the pipeline produces

Native, Figma-editable SVGs at 1920×1080 for a Cybele blog article, in one pass: the cover plus one
illustration per illustrable section. Icons come from the Cybfont set as real vector paths (no
rasters, no `<foreignObject>` — Figma drops both).

### How many of each — per task

The console launcher asks, and stores the answer in `jobs/<id>/job.json` → `options`:

| Field | Meaning |
|---|---|
| `coverVariants` | How many covers. **1 by default. `0` means no cover at all** — the skill skips that phase entirely |
| `sectionImages` | How many in-article illustrations. Empty/`null` = auto, one per illustrable section. `0` = none |

The counts also appear in the task prompt as a "Deliverables for this article" line. They override
the skill's own historical defaults (which were 6 covers + one per section).

### What the run delivers

`jobs/<id>/output/v<N>/` with `covers/` and/or `sections/` holding the SVGs (plus PNG renders), and a
`preview.html` / `preview.pdf` carrying **one page per requested visual and nothing else** — no title
sheet, no "notes for this run" page. Run notes go in `NOTES.md` as a file.

---

## Video Storyboard Pipeline

> **Pointer (2026-09-28).** The rules for video storyboards live in one file:
> **`web-app/pipelines/STORYBOARD_SPEC.md`** (authoritative, v1.0 2026-07-15). This section only exists
> so the console can hand a storyboard run its context, like the other task types. **Do not re-add
> design values here:** to change how a storyboard looks, edit the spec.

- **What it produces:** from a fixed voiceover script (kept verbatim; only graphic decisions are free),
  an ordered set of 1920×1080 native, Figma-safe SVG keyframes, one idea per scene. Each scene gets its
  `VOICEOVER:` line and a `Motion:` note, and all scenes go in one stacked HTML preview.
- **House style:** dark navy, minimal, depth and glow, colour with a job, mechanism shown rather than
  labelled (spec §4 onwards).
- **Figma:** after approval, the SVGs go to the "Youtube" file `K8rHguGyksdPWdHrSA3VOi`.
- **Run recipe:** RUNBOOK §3.4b. There is no packaged `cybele-video-storyboard` skill yet: follow the spec.

## LinkedIn Carousel (Placas)

> **Pointer (2026-09-28).** The rules for LinkedIn carousels live in one file:
> **`web-app/pipelines/LINKEDIN_CAROUSEL_SPEC.md`** (authoritative, rewritten 2026-07-29 from
> measurements of the 10 reference carousels). This section only exists so the console can hand a
> carousel run its context. **Do not re-add design values here:** edit the spec.

- **What it produces:** from the text of a LinkedIn post, 4–7 native, Figma-safe 1200×1500 SVG placas
  (median 6) on the `hook → middle → CTA` skeleton, plus a `preview.html`. Variants come after delivery
  (spec §10).
- **Strict verbatim:** no word is added, removed or altered, and the `CAPTION` is never rendered.
  `web-app/pipelines/verbatim_check.js` enforces it; exit 1 means do not deliver.
- **References:** the Figma "Exercise" file `8RBfhSYgaCuo4uM82JqAHL`, section `281:2156` (10 reference carousels).
- **Run recipe:** RUNBOOK §3.4c. There is no packaged `cybele-linkedin-carousel` skill yet: follow the spec.

## Thinfinity Architecture Diagram Skill

### Purpose

Generate **Thinfinity (Cybele Software) product architecture diagrams** as native, Figma-compatible
SVG, built from a small, strict visual vocabulary reverse-engineered from Cybele's official Figma.
Distinct from the Blog pipelines: this is not editorial illustration — it is **technical diagramming
from fixed atoms on a grid**. Output is a standalone SVG + an HTML preview, optionally pushed to Figma.

**Source of truth (2026-09-28):** the console repo's `skills/thinfinity-architecture/`. The copy at
`~/.claude/skills/thinfinity-architecture/` mirrors it: after changing the repo copy, copy it over
(they had drifted apart; the drifted copy is backed up in `~/.claude/skills-backup/`).
The skill is **packaged and live** at `~/.claude/skills/thinfinity-architecture/` and auto-invokes
whenever the user asks to create/draw/diagram a Thinfinity or Cybele architecture (deployment topology,
reference architecture, gateway/broker/IDP layout, VDI/DaaS topology, multi-region/multi-tenant setup,
or to redraw an existing architecture image in the Cybele style).

### Input / Output

| Input | Output |
|-------|--------|
| Natural-language description of an architecture (explicit OR conceptual — see modes below) | Standalone SVG (icons inlined) |
| (Optional) an existing architecture image to redraw in the Cybele style | HTML preview (`test_NN.html`) for browser inspection |
| (Optional) target Figma `fileKey` + `nodeId` | After approval: native Figma-safe push via `generate_figma_design` |

### Visual System (the "pill" vocabulary)

Reverse-engineered from Figma files `8RBfhSYgaCuo4uM82JqAHL` (canonical atoms — 5 reference frames
Nick curated) and `W3Pnm739iwmVdo3hSaBNQe` (131-icon library). Authoritative spec: `SKILL.md`
(inside the skill) + `STYLE_SPEC.md` (in the working dir).

- **The pill (one atom for everything):** uniform **160×43 px**, 1.5 px solid border, radius 7, white
  fill always, icon 23×23 at (10,10), Inter 12 px label. **No size variants.** Category is communicated
  **only by stroke + text color**:
  - **Thinfinity** = Cybele blue `#0A74D6` (Gateway, Broker, IDP, Agent, Comm Gateway)
  - **User** = dark `#373737` (browsers, end users)
  - **Secondary** = gray `#BDBDBD` stroke + `#373737` text (resources, firewall, TLS tunnel, DB)
  - The icon takes the pill's colour: `#0A74D6` in Thinfinity pills, `#373737` everywhere else (2026-09-28; it used to keep its native colour, which made AD and TLS green).
- **Zones = dashed containers** (`stroke-dasharray="6 4"`) labeling a network/site/tier: Remote Access,
  DMZ, Corporate/Internal Network, Cloud, On-Prem, IDP Integration, region bands. **Hard rule: no dashed
  inside dashed** — subnets/pools/domains become pill rows with a text label, not sub-boxes. *Only
  exception (2026-09-28):* an environment zone may hold network zones, one level deep (see next).
- **Environment zones (2026-09-28, SKILL §2.2b):** colour marks **where things are hosted**, and only
  that. Each is a dashed intense stroke on a soft fill:
  - customer / on-prem: `#3DCCA1` on `#F5FCFA`;
  - cloud: `#8878ED` on `#F9F8FE`;
  - hosted by Cybele: `#0A74D6` on `#EFF7FE`.

  Values come from the Figma "Architecture sample: Hybrid" (`W3Pnm739iwmVdo3hSaBNQe` `428:4159`).
  Dashed is Nick's rule: dashed lines are for environments and networks. Network zones stay gray
  inside them, and users stay outside. The zone icon is `cloud-inf` for sites that live in a cloud;
  the building (`premises`) is for on-prem only. These hues are never used for icons or pills. **Strict
  (Nick, 2026-09-28):** official Figma diagrams that paint tenant/network sub-zones or a shared-DB
  bus green are redrawn gray / connector blue, and "Managed by Cybele" is one blue environment.
- **Details settled on 2026-09-28** (SKILL §11–12, from a reviewed test task):
  - The reference footer's arrow is connector blue, not gray.
  - Every chevron stops 4 px before its target.
  - Port labels, only when asked, sit **on** the line inside a pill with a 1 px `#BDBDBD` stroke. A
    segment too short to show the line on both sides is lengthened; the label never moves off it.
  - Firewall IN/OUT chips are neutral: IN filled `#373737`, OUT outlined.
  - Ports and firewall rules follow `reference/ports_and_firewall.md`: the port matrix read from the
    Architect Studio's `PORT-MATRIX.md` (knowledge only, no code), to be validated with dev before any
    customer use.
- **Case data (console, 2026-09-28):** an Architecture diagram task can carry an optional "Datos del
  caso" form: cloud, users, HA, desktops, identity, third-party access, sites, ports, firewall, notes.
  An empty field is not relevant; an empty form means the standard, simple diagram. The same form
  comes back in the intervention window when a run asks (RUNBOOK §3.4/§3.5).
- **Connector = open chevron stroke** in azure `#0AA9FF` (NOT the Cybele `#0A74D6`, NOT a filled
  triangle), width 2, orthogonal routing, buses for converge/distribute. **Dashed connector** = a
  secondary/support flow (IDP auth, management, backup).
- **Layer order (hard rule):** zones → connectors → pills, or arrowheads get hidden.
- **Default is monochrome**; per-flow color-coding is an opt-in exception (e.g. color per region in
  multi-region diagrams).
- **131 brand icons** in `icons/` (+ `_arrow.svg`), native viewBox 23×23, fixed `preserveAspectRatio`
  (`xMidYMid meet`) so they don't deform. *(2026-09-28: `cloud-inf` added from the Figma Design System,
  and the 15 icons that carried green / violet / orange recoloured to `#373737`.)*

### Product knowledge layer (capability → topology)

A second layer was specified so the skill can produce a diagram from a **conceptual description of
Thinfinity capabilities**, not only from an explicit list of boxes and arrows. Captured in
`thinfinity_arch_skill_handoff_v2.md` (Downloads). It adds:

- **Component catalog** (role → pill): Gateway, Primary/Secondary Broker, IDP, Agent, Comm Gateway,
  endpoints, backend resources, TLS tunnels, external IDPs.
- **Zone catalog** and **product invariants** (the non-negotiable rules the skill applies even when
  unspoken): reverse connection / no inbound ports (arrows point to the Gateway); Gateway lives in the
  DMZ/Cloud; Broker lives in the corporate network with the resources; clientless browser access; HA =
  Primary + Secondary Broker; TLS 1.3/443 transport; multi-region = per-region Comm Gateway + Sec Broker;
  multi-domain = per-domain Primary Broker; IDP auth drawn dashed; managed/DaaS = "Managed by Cybele
  Software" hub-and-spoke.
- **Capability → topology map**: translates "clientless access", "no open ports", "VDI/DaaS", "SSO/MFA",
  "multi-region", "hybrid", etc. into the concrete components to instantiate.
- **Two prompt modes** converging on the same render pipeline:
  1. **Explicit** — user enumerates zones/nodes/flows (validated, in production).
  2. **Conceptual** — user describes capabilities; the skill derives the topology via the invariants.

> Status: the 🟢 rules are confirmed by the 7 validated diagrams; the 🟡 product inferences await
> Nick's validation before being codified into the skill (e.g. is the Agent always required on every
> resource; is the Comm Gateway exclusive to multi-region; is MFA a separate pill or assumed in the IDP).

### 7 validated diagrams (calibration set)

Built at increasing complexity in `C:/Users/NickCeraso/thinfinity_arch_skill/` and bundled as the
skill's `examples/` + `reference/` renders. Each became a reusable topology "recipe":

| # | File | Pattern |
|---|------|---------|
| 01 | `test_01_basic.html` | Remote User → Gateway ← Broker + Web App (Network zone) |
| 02 | `test_02_hybrid.html` | Hybrid: Users (bus) → Cloud(Gateway) ← On-Prem(Broker + Windows Server) |
| 03 | `test_03_full.html` | Full reference: Remote + Local users → Gateway (DMZ) → Broker (Corp) → vertical bus → all resource types + Cloud VDI |
| 04 | `test_04_multiregion.html` | Multi-region, **color-coded dual-flow** (blue control plane + per-region session planes; Comm Gateway + Sec Broker per region) — the opt-in color exception |
| 05 | `test_05_idp_domains.html` | Multi-domain + `Thinfinity IDP` (auth drawn as dashed connector to each domain's Primary Broker) |
| 06 | `test_06_vdipools_backup.html` | IDP Integration → Gateway → Primary Broker(s) → Internal Network with VDI pools (subnets) + Backup |
| 07 | `test_07_managed_hub.html` | "Managed by Cybele Software" hub-and-spoke; central Gateway, mirrored cloud spokes (Broker + resources) |

### Render & self-check

Headless Edge screenshot → read the PNG → verify against the spec (uniform pills? no hidden/overlapping
arrowheads? ≥14 px straight run before each arrowhead? gaps ~43 px? mirrored groups clean?) → iterate.

```powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu `
  --hide-scrollbars --window-size=<W>,<H> --screenshot="<out>.png" "file:///<path>.html"
```

### Files

| File | Purpose |
|------|---------|
| `skills/thinfinity-architecture/` (console repo) | **Source of truth since 2026-09-28**; the `~/.claude/skills/` rows below are its mirror |
| `skills/thinfinity-architecture/reference/ports_and_firewall.md` | Ports per component, arrow-direction rule, firewall rules per zone (optional layer, 2026-09-28) |
| `presentations/reference_builder/build_script.py` | Reference implementation for diagrams inside a deck (see PPTX › "Architecture diagrams in a deck") |
| `~/.claude/skills/thinfinity-architecture/SKILL.md` | Authoritative spec + build workflow (the live skill) |
| `~/.claude/skills/thinfinity-architecture/icons/` | 131 brand SVG icons + `_arrow.svg` |
| `~/.claude/skills/thinfinity-architecture/examples/` | The 7 validated HTML sources |
| `~/.claude/skills/thinfinity-architecture/reference/` | 7 validated PNG renders + atoms spec |
| `thinfinity_arch_skill/STYLE_SPEC.md` | Canonical visual style spec (atoms, colors, tokens) |
| `thinfinity_arch_skill/test_0[1-7]_*.html` + `*_render.png` | The 7 calibration diagrams + renders |
| `thinfinity_arch_skill/icons_gallery.html` | Gallery of the 131 icons |
| `~/Downloads/thinfinity_arch_skill_handoff.md` | Handoff v1 — visual system + provenance |
| `~/Downloads/thinfinity_arch_skill_handoff_v2.md` | Handoff v2 — product knowledge layer (capability → topology), drafted 2026-05-27 |

---

## Pipeline Comparison

| Dimension | PPTX (Presentations) | PDF (Whitepapers) | SVG (Blog Illustrations) | SVG (Blog Covers) | SVG (Arch Diagrams) |
|-----------|---------------------|-------------------|--------------------------|-------------------|---------------------|
| **Input** | PDF/text with slide content | DOCX with long-form content | Article text + section titles | Article text (full) | Architecture description (explicit or conceptual) or image to redraw |
| **Output** | `.pptx` (Google Slides compatible) | Branded PDF (multi-page) | 1920×1080 SVG per section | 6 × 1920×1080 SVG variants + HTML preview | Standalone SVG + HTML preview |
| **Language** | Python (`python-pptx`) | Python (Playwright + PyMuPDF) | Python (local SVG icons) or Node.js (Figma API) | Python (programmatic SVG + Playwright render) | SVG authored directly (HTML wrapper + Edge render) |
| **Brand source** | `brand_config.json` + PNG assets | Figma reference + hardcoded styles | Figma Blog Posts + Design System | 21 reference covers (`sample portadas.pdf`) + named tokens | `SKILL.md` + `STYLE_SPEC.md` (canonical Figma atoms) |
| **Icons** | PNG from `icons_png/` | SVG inline (pro/con, contact) | Cybfont vector paths from Figma API | Hero primitive library + icon dict (100×100 viewbox) | 131 brand SVG icons inlined (23×23) |
| **Figma integration** | None (standalone file) | Optional upload via `generate_figma_design` | SVG import to Figma for editing | SVG import to Figma; optional auto-push | Optional push via `generate_figma_design` (fileKey+nodeId) |
| **Editable in** | PowerPoint / Google Slides | Not editable (final PDF) | Figma (all elements are native SVG) | Figma (all elements are native SVG) | Figma (all elements are native SVG) |
| **Scope** | Content deck | Document body | Per-section in-article image | Hero image at top of post | Product architecture / topology diagram |
| **Key challenge solved** | Shadow removal, typography enforcement | Pagination, cover title extraction | Cybfont as native SVG paths; arrow style | Archetype system, parallel-session reconciliation, batch variant generation | Strict pill atom system; layer order; capability→topology knowledge layer |

---

## Project Timeline

Chronological log of milestones. Operational detail for each lives in the corresponding pipeline section above.

| Date | Milestone |
|---|---|
| 2026-03-20 | Brand rules + project docs initialized (`BRAND_DESIGN_RULES.md`, `PROGRESS.md`). |
| 2026-03-25 | PPTX brand-a-source pipeline: nuclear shadow removal (4-layer cleanup through theme XML), typography enforcement, `<a:noAutofit/>` fix for Google Slides title sizing. |
| 2026-03-26 | Whitepaper PDF pipeline built: DOCX → paginated HTML → branded PDF (Playwright + PyMuPDF). Pipeline moved to `cybele_deckgen/whitepaper/`. Figma upload of WP pages via `figmaselector=#capture-target`. Brandbook typography extracted from Figma. `thinfinity_logo_white_real.png` created (the original `_white.png` is actually blue). |
| 2026-03-27 | Whitepaper pipeline hardened: dynamic cover-title extraction from DOCX, design corrections from Figma reference, reusability tested across documents. CISO PPTX (brand-a-source) shipped with hyperlink-color override fix (strip `<a:hlinkClick>`). First SVG blog illustration pipeline (Citrix migration article, 3 sections, Cybfont icons via Figma MCP asset URLs returning native SVG). Second illustration set (Secure RD article) establishes light/dark alternation, solid-fill cards, straight arrows. |
| 2026-04-17 | Blog cover visual system reverse-engineered from 21 production covers (`sample portadas.pdf`). Parallel-session reconciliation produced final canon: 1920×1080 canvas, 6 archetypes A1–A6, named color tokens, generator-only (no templates). Telecom CX article = first proof-of-concept (6 variants). |
| 2026-05-22 | Thinfinity Architecture Diagram Skill authored: pill visual system from Figma atoms + 131-icon library, 7 calibration diagrams of increasing complexity, packaged at `~/.claude/skills/thinfinity-architecture/`. Handoff v1. |
| 2026-05-27 | Arch skill product-knowledge layer (capability → topology): component catalog, product invariants, capability-to-topology map, two prompt modes (explicit + conceptual). Handoff v2 with 🟢 confirmed rules vs 🟡 product inferences awaiting validation. |
| 2026-06-02 | PPTX from-scratch paradigm: VDI/VDA Universidades editorial deck (`build_pptx.py`, ~2,340 lines, palette 06/26 adopted as new canonical Cybele palette, supersedes `#0A74D6`/`#0B1A3B`). Closing-slide byte-for-byte transplant + theme-chain transplant + `force_white_hyperlinks()`. Language-coherence rule: transplant preserves visual structure, translates text content to source language. |
| 2026-06-08 | Architecture skill expanded with §3.3 edge centering, §3.4 convergence/bifurcation, §11 in-SVG reference footer (mandatory), §12 pre-render distance check (mandatory). New artifacts: OT vendor access diagram, manufacturing VDI 6-layer, VDI pools HA. Recipes R8–R11 added to capability catalog. |
| 2026-09-28 | **Console + architecture review session (Nick).** **Console:** see Logo & Icon Assets › Console brand library for the icon, file and UI changes. **Architecture skill:** see Thinfinity Architecture Diagram Skill › Visual System (icon colour, environment zones, arrow and label details, case-data form). **Decks:** architecture diagrams follow the new PPTX › "Architecture diagrams in a deck", from Nick's review of task-1790624980817. **Housekeeping:** one copy of the architecture skill (repo = source, `~/.claude` = mirror). |
| 2026-06-10 | **Faithful brand-a-source reproduction path** (Node/pptxgenjs, `enterprise_vdi_oci_esp/`): *Enterprise VDI on OCI · Discovery Demo (ESP)* rebuilt from a 39-pg source PDF → 40-slide Google-Slides deck with **verbatim copy** + **12 native editable architecture diagrams** drawn from the thinfinity-architecture **construction rules** (pill px-ratios, gap = pill-height, edge-centered connectors) and auto-**centered on x/y**. Inter **static-font** install fixes the hairline "washed-out" render (variable-font issue); render loop = PowerPoint COM → PDF → PyMuPDF (use Python 3.13 — system 3.14 is broken). **⅓/⅓/⅓ background-mode** split (light/white/dark) with diagram-always-white + no-dark-beside-separator rules; **borderless, low-contrast** containers (no vibrant `#0F7FE0` fills; `#0A74D6` only for table headers); co-brand cover emulated with **logo proportions preserved**; **animated-GIF closing retained**; footer alludes to doc title + "Thinfinity + OCI" with a ≥10 px safe margin. |

---

## Next Steps

### Immediate
- [ ] Whitepaper pipeline: add TOC page and improve pagination (avoid cutting content blocks, reduce whitespace on sparse pages).
- [ ] Forward `RECONCILIATION.md` to the parallel session's HANDOFF owner so the reconciled decisions land there.
- [ ] **Arch skill:** validate the 🟡 product inferences in handoff v2 (Agent always required? Comm Gateway multi-region-only? MFA separate pill vs assumed in IDP?). Once validated, codify them into the skill's `reference/thinfinity_reference_architecture.md` and hook it into `SKILL.md` §9. Then generate 2-3 diagrams from *conceptual* prompts to validate the capability→topology expansion.

- [ ] **From the 2026-09-28 session (need Nick or dev):**
  - [ ] Validate `reference/ports_and_firewall.md` with development before a diagram with ports or
        firewall rules goes to a customer.
  - [ ] Review the 38 legacy icons "fuera de Figma". Several have Figma twins under other names
        (2FA/2fa, database/db, windows/win, load-balancer/load-bal).
  - [ ] Fix two things in Figma: the duplicate `audio-file`, and add `attach` (`web-app/data/icons-custom/attach.svg`)
        to the Design System if it should be official.
  - [ ] Push branch `Nick`, so teammates get today's changes. (Since `d559e6d` the start-up sync no longer
        overwrites local work: files with unpushed or uncommitted changes are kept and shown in Settings.)

### Short-term
- [ ] Generalize `build_pptx.py` (from-scratch generator) beyond the *Universidades* deck into a reusable, content-driven template.
- [ ] **Generalize `brand_config.json` (currently PPTX-only)** so any pipeline can load the same brand tokens from one source of truth. Expose the 06/26 canonical palette as default.
- [ ] Build a content-extraction pipeline (Google Docs / DOCX → structured content → branded output).
- [ ] Test PPTX output in Google Slides and iterate.
- [ ] Document all four pipelines (PPTX + PDF + SVG illustrations + SVG covers) for team reference.
- [ ] Create a reusable Cybfont icon-fetcher module (shared across SVG illustration tasks).

### Medium-term — Web App
- [ ] Build a web app for team-wide access (stack TBD).
- [ ] Add support for co-branded documents (Cybele + Oracle, Cybele + partner).

### Long-term
- [ ] Figma plugin / integration for direct design generation.
- [ ] Multi-language support (EN / ES).
- [ ] Template library expansion (one-pagers, datasheets, case studies).
- [ ] Team onboarding documentation.
- [ ] Cybfont icon index (name → concept mapping) for faster illustration generation.
- [ ] Blog cover system: dark-mode variants if blog redesign calls for them.

> **Done in this iteration:** the blog cover system is packaged as the `cybele-blog-visuals` skill (englobes covers + section illustrations in one invocation, installed at `~/.claude/skills/cybele-blog-visuals/`).
>
> **GitHub repo public-release tasks** (move scripts to `blog_illustrations/`, init repo, separate cover system repo, README, `.gitignore`) are on-demand future work — not active priority.

---

## File Structure

```
cybele_deckgen/
├── brand_assets/              # Logos (see §"Logo & Icon Assets" for usage rule)
│   ├── cybele_logo.png                  # Default (Cybele blue)
│   ├── thinfinity_logo.png              # Default (Thinfinity blue)
│   ├── thinfinity_logo_white_real.png   # True white — only on dark/saturated backgrounds
│   ├── cybele_logo_white.png            # DEPRECATED (actually blue)
│   └── thinfinity_logo_white.png        # DEPRECATED (actually blue)
├── icons/                     # SVG icon source files
├── icons_png/                 # 200x200 PNG icons (dark + white variants)
├── brand_config.json          # Brand tokens (palette 06/26 to be exposed here — see Short-term task)
├── PROGRESS.md                # This file
├── BRAND_DESIGN_RULES.md      # Complete brand & design specification
│
├── whitepaper/                # PDF whitepaper pipeline (stable)
│   ├── build_whitepaper.py          # Orchestrator: DOCX → branded PDF
│   ├── generate_wp_pages.py         # 1. DOCX → paginated HTML
│   ├── redesign_wp.py               # 2. Figma-style CSS + content transforms
│   ├── generate_cover_closing.py    # 3. Cover + closing HTML
│   └── generate_pdf.py              # 4. HTML → merged PDF
│
├── blog_covers/               # Blog cover system (unified under cybele-blog-visuals skill)
│   ├── BLOG_COVER_RULES.md          # Authoritative visual system spec
│   ├── HANDOFF.md                   # Generative brief (from article → cover)
│   ├── RECONCILIATION.md            # Reconciled decisions
│   ├── build_telecom_cx_covers.py   # Reference implementation
│   ├── reference/cover_0[1-21].png  # 21 production reference covers
│   └── output/                      # Generated SVGs/PNGs + preview.html per article
│
└── (legacy / superseded — kept on disk but no longer the active code path)
    ├── build_final_pptx.py    # Earlier brand-a-source PPTX generator
    ├── build_branded_deck.py  # HTML-based deck builder
    ├── slide_templates.py / text_to_content.py / generate_deck.py / quick_deck.py
```

### From-scratch PPTX working dir (`pptx_work/`)

```
pptx_work/                                   # ★ Working dir — from-scratch editorial generator
├── build_pptx.py                  # From-scratch editorial builder (palette 06/26, ~2,340 lines, slide count dynamic per source)
├── replace_slide27.py             # Closing-slide + theme-chain transplant; force_white_hyperlinks()
├── cierre.pptx                    # Original closing slide (inserted as-is — never edited)
├── assets/
│   ├── lockup_thinfinity_oracle.png
│   ├── cybele_isologo.png
│   ├── bg_navy_cover.jpg
│   ├── bg_navy_closing.jpg
│   └── cybele_icons/              # 63 PNGs (21 Figma icons × 3 variants)
└── output/
    ├── VDI_VDA_Universidades_v3.pptx              # 27 slides, 10.6 MB
    └── VDI_VDA_Universidades_v3_with_cierre.pptx  # Final deliverable (closing transplanted)
```

### Faithful reproduction working dir (`enterprise_vdi_oci_esp/`)

```
cybele_deckgen/enterprise_vdi_oci_esp/        # ★ Node/pptxgenjs faithful brand-a-source path
├── build_deck.js              # Whole deck: brand system, mode-aware theme (TH), diagram engine, 40 builders
├── swap_closing_slide.py      # XML-swap cierre.pptx as the last slide (animated GIF retained)
├── render_diagram_icons.py    # Render needed thinfinity-skill icons → PNG (blue/dark/white) in diagram_icons/
├── render_for_critique.py     # PowerPoint COM → PDF → PyMuPDF JPGs + slides_preview.html
├── diagram_icons/             # 24 icons × 3 colorways (from the skill's 131-icon set)
└── output/Enterprise_VDI_OCI_Discovery_Demo_ESP.pptx   # 40 slides, ~11 MB (final, GIF closing)
```
> Build chain: `node build_deck.js` → `python swap_closing_slide.py` → `python render_for_critique.py` (Python 3.13).

### Thinfinity Architecture Diagram Skill (outside `cybele_deckgen/`)

```
~/.claude/skills/thinfinity-architecture/   # ★ The live, packaged skill
├── SKILL.md                   # Authoritative spec + build workflow
├── icons/                     # 131 brand SVG icons + _arrow.svg
├── examples/                  # The 7 validated HTML sources
└── reference/                 # 7 PNG renders + atoms spec

~/thinfinity_arch_skill/                     # ★ Working dir (R&D + calibration set)
├── STYLE_SPEC.md              # Canonical visual style spec
├── icons/                     # 131 SVG + _arrow.svg
├── spec_preview.html          # Visual preview of the atoms
├── icons_gallery.html         # Gallery of the 131 icons
├── test_0[1-7]_*.html         # 7 calibration diagrams
└── test_0[1-7]_render.png     # Their renders

~/Downloads/
├── thinfinity_arch_skill_handoff.md     # Handoff v1 — visual system + provenance
└── thinfinity_arch_skill_handoff_v2.md  # Handoff v2 — capability → topology knowledge layer
```
