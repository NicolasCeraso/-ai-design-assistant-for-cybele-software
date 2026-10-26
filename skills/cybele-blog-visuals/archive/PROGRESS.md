# Cybele AI Design Assistant — Progress Report

> ⚠️ **Journal, not a specification.** This file records how the system was built and why.
> The design rules live in `BLOG_COVER_RULES.md` (covers), `SECTION_RULES.md` (section
> illustrations) and `BRAND_DESIGN_RULES.md` (brand tokens); the counts of covers and section illustrations live in `SKILL.md` → INVOCATION
> MODES. Where this file disagrees with those, they win. Never use it as a stand-in for a
> rule file you could not open.
>
> The section-illustration rules that used to sit in this file are now `SECTION_RULES.md`.

**Last updated:** 2026-04-17
**Project:** AI-assisted branded document and design generation for Cybele Software

---

## Project Vision

Build an AI-powered system that enables the Cybele design team to:

1. **Brand documents** — Take unbranded content and produce branded PDFs/PPTX
2. **Generate illustrations** — Create article illustrations following brand guidelines, export to Figma as SVG
3. **Generate blog covers** — Produce on-brand hero images for blog articles following a reverse-engineered visual system
4. **Co-design in Figma** — Push and iterate designs directly in Figma via MCP integration
5. **Web App for the team** — A shared interface so all team members can leverage these capabilities

---

## Infrastructure Setup (Completed)

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

## Brand System Analysis (Completed)

### Sources Analyzed

| Source | File Key | Content |
|--------|----------|---------|
| Cybele Brandbook | `y7mHflD4ukCFDo6YsPzIf4` | Full brand manual (screenshot) |
| Cybele Design System | `x0HMD1pXkcYdFM7NSaBvb4` | Colors, Typography, Icons, Grid, Logos, Components |
| 9 Whitepaper designs | Various | Document branding patterns |
| PPT Template PDF | Local | 44+ slide type templates |
| 21 Blog covers | `sample portadas.pdf` | Hero image visual system (reverse-engineered 2026-04-17) |

### Brand Tokens Extracted

**Colors:**
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

### Document Patterns Identified

**Whitepapers:**
- Cover: navy gradient bg, badge/tag, white title, logos bottom-left
- Interior: white bg, blue H2 titles, gray body, circled icons for feature lists
- Back cover: CTA card, contact info, copyright footer with Cybele logo

**Presentations (Google Slides):**
- Cover: blue wave bg, Thinfinity + Oracle logos, white title
- Content slides: Oracle logo top-left, Cybele logo top-right
- 15+ slide types: summary, section divider, grid (4/6/8 items), features, stats, use cases, case study, comparison, timeline, closing
- Closing: "Thanks for watching!", animated GIF wave, contact info, social icons

**Blog covers (reverse-engineered 2026-04-17):**
- Canvas: 1920×1080 px (16:9)
- 6 compositional archetypes (Hub-and-spokes, Duality, Hero+halo, Stack/ecosystem, UI mockup, Editorial/poster)
- Palette: named tokens with gradient recipes (cyan-to-blue, violet-to-blue, teal-to-navy, red-dramatic)
- Flat illustration style with soft internal gradients, radial halos, no photorealism
- Titles NOT baked into cover — title lives in CMS. Only small in-illustration labels (pills, acronyms)

---

## Logo & Icon Assets Available

### Logos (`brand_assets/`)

| File | Variant | Size |
|------|---------|------|
| `cybele_logo.png` | Dark on transparent | 700x260 |
| `cybele_logo_white.png` | White on transparent | 700x260 |
| `thinfinity_logo.png` | Dark on transparent | 900x240 |
| `thinfinity_logo_white.png` | White on transparent | 900x240 |
| SVG versions | `.svg` for all above | Vector |

External: `Oracle_logo (2) 1.png` (5484x709, red)

### Icons (`icons_png/`, 200x200 RGBA each)

`audit-log`, `broker`, `cloud`, `dollar-sign`, `enterprise-ztna`, `gateway`, `gpu-fast`, `lock-check`, `no-vpn`, `pc`, `remote-work`, `scale`, `search`, `shield`, `stats`, `user`, `vdi`

Each has a `_white.png` variant for use on dark/colored backgrounds.

SVG originals available in `icons/`.

---

## PPTX Generation Pipeline (In Progress)

### Standard Template

**Base file:** `Copy of VDI_VDA_Universidades_Editable.pptx` (2 slides: cover + closing)
- Cover: blue wave bg, Thinfinity + Oracle logos, white title + subtitle
- Closing: "Thanks for watching!", contact info, social icons, animated GIF

**Approach:**
1. Open the 2-slide template (cover + closing)
2. Insert N content slides between them using `python-pptx`
3. Reorder XML `sldIdLst` so closing moves to the end
4. Update cover title + subtitle from source document; remove tagline
5. Fix closing slide: strip hyperlinks from contact text (cause blue color override), force white on phone numbers and URL
6. Apply branding to all content slides + nuclear shadow cleanup + typography enforcement

**Cover/closing rules:**
- Always use the standard 2-slide template — never preserve the source file's cover/closing
- Cover title and subtitle are updated per document; tagline ("Thinfinity Workspace | ...") is blanked
- Closing slide language must match the presentation content language (e.g., English content → English closing, Spanish content → translate closing to Spanish)
- Contact text (`cybelesoft.com`, phone numbers) must be white — hyperlinks (`<a:hlinkClick>`) must be stripped from XML because they override the font color with the theme's link color (blue)
- "Thanks for watching!" stays blue (`#0A74D6`); copyright stays gray (`#999999`)

### Test Cases

| Document | Slides | Script |
|----------|--------|--------|
| "VDI & VDA Para Instituciones Educativas" (v1) | 27 slides, 442 shapes | `build_final_pptx.py` |
| "CISO Risk Lens: Thinfinity vs Citrix" (v2) | 32 slides, 360 shapes | `build_ciso_pptx.py` |

### Current Script: `build_ciso_pptx.py`

**Input:** Source PPTX with content (34 slides, 13.33"×7.5")
**Output:** Branded `.pptx` (32 slides, 10"×5.625", Google Slides compatible)

**Features implemented:**
- Google Slides dimensions (10" x 5.625")
- Inter SemiBold 18pt for header titles (white on blue bar), Inter Regular for body text
- Cybele + Thinfinity logo PNGs on every content slide footer
- Icon PNGs from Design System (`icons_png/`) inside content cards
- Flat design: no gradients
- **Nuclear shadow removal** — cleans shapes, slide layouts, slide masters, AND theme XML
- No italic text; no Thin/Light/ExtraLight font variants (global enforcement pass)
- Multiple slide layouts: `two_card_slide`, `content_with_items`, `icon_content_slide`, `add_section_divider`
- Section dividers: navy bg, large number + blue accent line + white title + Thinfinity logo
- Numbered items: single-digit in blue circle (0.35"), prevents digit wrapping
- **Hyperlink color fix**: strips `<a:hlinkClick>` from closing slide contact runs to prevent theme blue override
- Cover title auto-updated from source; tagline removed
- Closing page contact text forced white + `endParaRPr` color cleaned

### Key Functions

| Function | Purpose |
|----------|---------|
| `add_header_bar()` | Blue header bar with white title, optional blue subtitle below |
| `add_section_divider()` | Full navy slide with number, accent line, white title |
| `add_textbox()` | Generic text box with explicit run font control + noAutofit |
| `add_multiline_textbox()` | Multi-paragraph text with optional per-line styling |
| `add_box()` | Rounded rectangle, flat fill, no shadow |
| `add_icon()` | Insert PNG icon at given size |
| `add_footer_logos()` | Cybele bottom-left, Thinfinity bottom-right |
| `two_card_slide()` | Two-column comparison with icons + titles + body |
| `content_with_items()` | N items in grid (auto cols), numbered circles + title + body |
| `icon_content_slide()` | Large icon left + title + body text |
| `_nuke_effects_from_xml()` | Nuclear XML cleanup: effects from shapes, groups, layouts, masters, theme |
| `remove_shadow()` | Wrapper — calls `_nuke_effects_from_xml()` on shape element |

### Known Issues

- Cybfont icon font not yet available locally (using PNG icons as substitute)
- Orphaned slide data in ZIP when template has >2 slides (use 2-slide template to avoid)
- Need to validate rendering in Google Slides for all slide types

---

## SVG Blog Illustration Pipeline (In Progress)

> **Moved.** The rules that used to live here — visual style, layout patterns, sizing, typography,
> the Cybfont icon process and the SVG export steps — are now the specification
> [`SECTION_RULES.md`](SECTION_RULES.md), the single place they live. Nothing was changed in the
> move; this section kept only the historical record below.

### Files

Historical record of the first runs. These lived on the original author's machine and are **not**
inputs to this skill — do not go looking for them.

| File | Purpose |
|------|---------|
| `citrix-migration-illustrations.html` | HTML preview (browser) — Citrix article |
| `export-native-svgs.mjs` | Node.js: fetches Cybfont SVG paths, builds SVGs |
| `build_blog_svgs.py` | Python: reads local icons, builds SVGs programmatically |
| `citrix-why-replace.svg` | Citrix article — Slide A, light |
| `citrix-migration-tooling.svg` | Citrix article — Slide B, dark |
| `citrix-why-thinfinity.svg` | Citrix article — Slide C, dark |
| `secure-rd-strategic-drivers.svg` | Secure RD article — Slide A, light (18 KB) |
| `secure-rd-use-cases.svg` | Secure RD article — Slide B, dark (13 KB) |
| `secure-rd-endpoint-control.svg` | Secure RD article — Slide C, light (6 KB) |

---

## Blog Cover Generation System (New — 2026-04-17)

### Purpose

Generate branded **hero images for blog articles** (the cover image displayed at the top of each blog post). Distinct from the Blog Illustration Pipeline — which produces images *inside* articles for specific sections. Covers express the **core concept of the article** as a single visual piece.

### Input / Output

| Input | Output |
|-------|--------|
| Article text (full copy or summary) | 6 cover variants, 1920×1080 SVG each |
| Core concept (one-sentence distillation) | HTML preview with all 6 stacked vertically for comparison |
| (Optional) Target Figma fileKey + nodeId | After approval: one native Figma-safe SVG |

### Workflow (canonical, every invocation)

1. Read the article; distill the core concept into one sentence
2. Pick 6 kits `{archetype, gradient_recipe, hero, satellites}` varying all four
3. Generate 6 SVGs at 1920×1080
4. Build a single HTML preview with all 6 stacked vertically, each labeled
5. Show preview in browser; wait for user to pick one (or request tweaks)
6. Export the chosen SVG as native Figma-safe output

**Rule:** the 6 variants are **6 ways to draw the same core concept**, NOT 6 different angles on the article.

### Visual System (reverse-engineered from 21 reference covers)

**Source analyzed:** `sample portadas.pdf` — contact sheet of 21 production Cybele blog covers (extracted via PyMuPDF, bbox analysis, color quantization, edge sampling).

**Canvas:** `viewBox="0 0 1920 1080"` (16:9). Minimum 60 px padding from any edge.

#### Design tokens (colors)

| Token | Hex | Role |
|---|---|---|
| `blue-deep` | `#0f1e6e` | Primary brand, darkest blue |
| `blue-royal` | `#2b3eaa` | Primary brand, mid blue |
| `cyan` | `#4dd4c8` | Accent, bright cool |
| `teal` | `#3ac6a6` | Success / positive state |
| `violet` | `#6a4cc8` | Accent, violet-blue |
| `violet-light` | `#a98cdb` | Accent, softer violet |
| `magenta` | `#b06fd9` | Accent for "social" category |
| `warning` | `#f2c14e` | Semantic warning |
| `danger` | `#d64040` | Semantic error / alarm |
| `danger-deep` | `#6b0f0f` | Editorial "problem" covers |
| `ink` | `#0a1533` | Text on light, dark surfaces |
| `paper` | `#f3f5fb` | Light surface / background |
| `white` | `#ffffff` | Highlights, halos, icon badges |

#### Gradient recipes

| Recipe | Stops | Use |
|---|---|---|
| `cyan-to-blue` | `cyan` → `blue-royal` | Default positive cover background |
| `violet-to-blue` | `violet` → `blue-deep` | Product-hero covers |
| `teal-to-navy` | `teal` → `blue-deep` | Compliance / reliability covers |
| `red-dramatic` | radial `#b52323` → `danger-deep` → `#3a0606` | Editorial "problem" covers ONLY |
| `monitor-body` | `blue-deep` → `ink` | Device frames |
| `halo` | radial `white` 0.5 → transparent | Always behind focal element |

#### Six compositional archetypes (A1–A6)

| Code | Archetype | When to use | Anatomy |
|---|---|---|---|
| **A1** | Hub-and-spokes | Concepts that integrate multiple components | Diagonal gradient bg + horizon curve + radial halo + central hero + 4–6 satellite circles + dotted connectors |
| **A2** | Duality | Two partner sides of the same concept | Unified background, two focal groups left/right, dotted session arc, small labels under each half, top chip naming the relationship |
| **A3** | Hero + halo | General-purpose hero, product portraiture | Violet-to-blue or cyan-to-blue gradient + big halo + cloud drift + single large hero + optional horizon silhouettes |
| **A4** | Stack / ecosystem | Platform / integration / "X + Y + Z" stories | Light soft background + big diffuse cloud + 3 circular cards in a row + dashed connectors + top chip |
| **A5** | UI mockup (2 flavors) | Product-direct stories — "what it looks like in practice" | Dark navy background + faint grid + big halo + main card with mock top bar, nav, content panels + 1–2 floating notification cards |
| **A6** | Editorial / poster (2 flavors) | Saturated, cinematic, emotionally-charged | Radial background + sparkles + light rays + hero bust or dramatic prop + kicker text |

**A5 flavors:** agent console (product in use) vs admin / Cloud Manager dashboard (platform management) — pick deliberately, they serve different narratives.

**A6 flavors:**
- **Dark editorial** (red radial, alarm icons, torn-paper props, coins): for "problem" covers ONLY
- **Poster editorial** (violet-blue radial, agent bust, channel icons arcing as halo, cloud above): for aspirational / product-hero covers

#### Hero primitive library

Thirteen reusable hero objects identified: **shield, cloud, padlock, monitor/desktop, laptop, server rack, factory silhouette, robotic arm, graduation cap, gears, coins, agent with headset, Thinfinity ring**. Compound heroes (two fused primitives) are common — e.g., cloud + padlock = secure cloud; shield + credit card = PCI-safe session.

#### Satellite vocabulary

Circle badges (60–100 px, color-coded by semantic: green=approved, red=denied, orange=warning, blue=neutral, violet=data/policy), connection lines (4–6 px white), glow halos, concentric rings, label pills (navy bg, Inter SemiBold 14–18 px), logo chips (white circular container).

#### Editorial rules (confirmed through iteration)

1. **Variants = same idea, different composition.** Never six different angles.
2. **Don't default to red for "big".** `red-dramatic` / A6 dark = financial or operational pain. For aspirational covers use A6 poster.
3. **Use canonical glyphs.** Don't reinvent per cover.
4. **Titles in chips, not floating text.**
5. **One focal per cover** — halo tells the viewer where to look.
6. **Products over logos.** Third parties (Oracle / AWS / Azure / Citrix) as generic cloud glyph + text label.
7. **A5 flavors are distinct** — agent console and admin dashboard serve different narratives.

#### Topic → visual kit matrix (quick lookup)

| Article topic | Gradient | Archetype | Hero |
|---|---|---|---|
| Security / Zero Trust / ZTNA | teal-to-navy / cyan-to-blue | A3 | Shield with keyhole or check |
| Cloud migration | cyan-to-blue / violet-to-blue | A4 / A3 | Cloud with logo or padlock |
| OT / IT / Manufacturing | teal-to-navy | A3 / A2 | Shield bridging factory + building |
| VDI / Virtual desktop | cyan-to-blue / monitor-body | A3 / A5 | Monitor + laptop |
| Contact center / BPO | violet-to-blue | A1 / A6 poster | Agent bust with headset |
| Cost / ROI / savings | teal-to-navy + teal accent | A2 | Coins + bar chart |
| Pain point / lock-in | red-dramatic (rare) | A6 dark | Receipt, chain |
| Automation / robotics | teal-to-navy | A3 | Robotic arm + conveyor |
| Monitoring / analytics | cyan-to-blue | A5 admin | Browser with chart |
| Transformation / modernization | violet-to-blue | A2 / A3 | Old → new flow |
| Aspirational product hero | violet-to-blue radial | A6 poster | Agent bust + channel halo |

### SVG authoring rules (Figma compatibility)

Same strict rules as Blog Illustrations — native SVG primitives only:

**Allowed:** `<rect>`, `<circle>`, `<ellipse>`, `<path>`, `<line>`, `<polygon>`, `<polyline>`, `<g>`, `<svg>`, `<linearGradient>`, `<radialGradient>`, `<defs>`, `<filter>`, `<text>`, `<tspan>`

**Forbidden:** `<foreignObject>`, `<image>`, external `<use>`, base64 data URIs, external URL references

**Key rules:**
- Escape `&` → `&amp;`, `<` → `&lt;` in `<text>` content (otherwise silent parse failure)
- Prefix SVG IDs per cover (`c1-bg`, `c2-halo`) — shared IDs across SVGs in one HTML break fills silently
- Use `gradientUnits="userSpaceOnUse"` with explicit coords for predictable scaling
- No CSS classes, no `<style>` blocks — inline attributes only

### Generator Pipeline

**Approach chosen (after reconciliation with parallel session):** Python generator only. Builds SVG programmatically from parameters. Reasons: single source of truth, one command produces 6 variants + HTML preview, helpers propagate brand changes automatically, no template drift.

**Dropped alternative:** SVG templates with placeholder slots — redundant given the batch→review→export workflow.

**Build pattern:**

```python
# 1. Build SVG as string (parameterized by archetype × tokens × hero × satellites)
svg = build_cover(kit)

# 2. Write to file
path = output_dir / f"cover_{slug}.svg"
path.write_text(svg, encoding="utf-8")

# 3. Render PNG for HTML preview via Playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.goto(f"file:///{path.as_posix()}")
    page.screenshot(path=str(path.with_suffix('.png')),
                    clip={'x': 0, 'y': 0, 'width': 1920, 'height': 1080})

# 4. Emit preview.html with all 6 covers stacked vertically, labeled
```

### Proof-of-concept: Telecom Contact Center VDI article

**Article:** "Telecom Contact Centers at Scale: A CIO's Strategy for VDI-Powered Customer Experience"
**Core concept:** *VDI on OCI powering telecom contact center agents at scale*

**6 variants generated** — all express the same concept with different visual approaches:

| # | Metaphor | Archetype | Gradient | Hero |
|---|---|---|---|---|
| 01 | Thinfinity hub + agents orbiting | A1 | cyan-to-blue | Thinfinity ring + agent badges |
| 02 | Cloud delivering desktops to agents | A3 | monitor-body | Cloud with monitor inside |
| 03 | Unified agent with channels | A3 | paper → violet-light | Agent bust + channel badges |
| 04 | Contact center at scale (mgmt view) | A5 admin | violet-to-blue | Cloud Manager dashboard |
| 05 | Physical → Virtual | A2 | teal-to-navy | Cubicles ↔ VDI cloud |
| 06 | 1K / 5K / 10K agents | A4 | cyan-to-blue | Three sized circles tied to OCI |

**Output validated:** all 6 SVGs parse cleanly via lxml, render correctly at 1920×1080 via Playwright, ready for Figma import.

### Reconciliation with parallel session

A second Claude Code session analyzed the same reference material independently. Both sessions converged on editorial principles, visual vocabulary, and Figma safety rules. Four contradictions were identified and resolved (see `blog_covers/RECONCILIATION.md`):

| # | Contradiction | Resolution |
|---|---|---|
| 1 | Canvas size: 1840×1084 (my session) vs 1600×900 (other) | **1920×1080** — standard 16:9 hero dimensions |
| 2 | 5 patterns (P1–P5) vs 6 archetypes | **6 archetypes (A1–A6)** — Editorial/poster has distinct anatomy |
| 3 | Color families A–F vs named tokens | **Named tokens only** as ground truth |
| 4 | Python generator vs SVG templates | **Generator only** — matches batch→review→export workflow |

### Files

| File | Purpose |
|------|---------|
| `cybele_deckgen/blog_covers/BLOG_COVER_RULES.md` | Full visual system spec (tokens, archetypes, icons, rules, topic-to-kit matrix) |
| `cybele_deckgen/blog_covers/HANDOFF.md` | Generative brief — how to produce a new cover given a new article (for future sessions or Skill) |
| `cybele_deckgen/blog_covers/RECONCILIATION.md` | Final reconciled decisions across parallel sessions |
| `cybele_deckgen/blog_covers/build_telecom_cx_covers.py` | Working prototype generator (reference implementation) |
| `cybele_deckgen/blog_covers/reference/cover_01.png … cover_21.png` | 21 production covers extracted from `sample portadas.pdf` |
| `cybele_deckgen/blog_covers/output/telecom_cx_0[1-6]_*.svg` | 6 generated SVG covers (telecom CX proof of concept) |
| `cybele_deckgen/blog_covers/output/telecom_cx_0[1-6]_*.png` | 6 rendered PNGs for HTML preview |
| `cybele_deckgen/blog_covers/output/preview.html` | Vertical comparator of the 6 variants |

---

## Pipeline Comparison

| Dimension | PPTX (Presentations) | PDF (Whitepapers) | SVG (Blog Illustrations) | SVG (Blog Covers) |
|-----------|---------------------|-------------------|--------------------------|-------------------|
| **Input** | PDF/text with slide content | DOCX with long-form content | Article text + section titles | Article text (full) |
| **Output** | `.pptx` (Google Slides compatible) | Branded PDF (multi-page) | 1920×1080 SVG per section | 6 × 1920×1080 SVG variants + HTML preview |
| **Language** | Python (`python-pptx`) | Python (Playwright + PyMuPDF) | Python (local SVG icons) or Node.js (Figma API) | Python (programmatic SVG + Playwright render) |
| **Brand source** | `brand_config.json` + PNG assets | Figma reference + hardcoded styles | Figma Blog Posts + Design System | 21 reference covers (`sample portadas.pdf`) + named tokens |
| **Icons** | PNG from `icons_png/` | SVG inline (pro/con, contact) | Cybfont vector paths from Figma API | Hero primitive library + icon dict (100×100 viewbox) |
| **Figma integration** | None (standalone file) | Optional upload via `generate_figma_design` | SVG import to Figma for editing | SVG import to Figma; optional auto-push |
| **Editable in** | PowerPoint / Google Slides | Not editable (final PDF) | Figma (all elements are native SVG) | Figma (all elements are native SVG) |
| **Scope** | Content deck | Document body | Per-section in-article image | Hero image at top of post |
| **Key challenge solved** | Shadow removal, typography enforcement | Pagination, cover title extraction | Cybfont as native SVG paths; arrow style | Archetype system, parallel-session reconciliation, batch variant generation |

---

## Prior Work in This Project

### HTML-to-Figma Illustrations (March 2025)

Files in `~/dashboard/`:
- `blog-final-illustrations.html` — Blog article illustrations
- `zero-trust-manufacturing-*.html` — Zero Trust manufacturing series
- `vdi-manufacturing-illustrations.html` — VDI manufacturing visuals
- `vdi-f-architecture.html` — VDI architecture diagrams
- SVG exports: `zt-illust-1.svg`, `zt-illust-2.svg`, `zt-illust-3.svg`
- PNG renders via Puppeteer: `zt-v2-*.png`, `zt-v3-*.png`
- Scripts: `capture-to-figma.mjs`, `export-svgs.mjs`, `render-and-push.mjs`

### Desktop App (March 2025)

`~/Desktop/Claude Code App/`:
- `email-preview.html` — Branded email template
- `server.js` — Local Puppeteer server for captures

---

## Session Log

### 2026-03-20 — Brand Rules Documentation

- Created `BRAND_DESIGN_RULES.md` with complete brand specification
- Created `PROGRESS.md` with full project state documentation
- Documented all brand tokens, typography rules, visual rules, asset locations
- Catalogued Figma Design System and Brandbook references

### 2026-03-25 (Session 1) — Shadow Removal & Typography Enforcement

- **Solved persistent shadow problem**: discovered that `theme1.xml` contained 3 `outerShdw` entries in `effectStyleLst` that were inherited by all shapes regardless of per-shape cleanup. Implemented nuclear 4-layer cleanup: shapes → layouts → masters → theme XML.
- Replaced `remove_shadow()` with `_nuke_effects_from_xml()` — also removes `effectRef` (theme references) and handles `grpSpPr` (group shapes).
- Theme cleanup: parses theme blob via `etree.fromstring(theme_part.blob)`, strips all effect elements, rebuilds valid minimal `effectStyleLst` (3 empty entries), writes back via `theme_part._blob`.
- Added global typography enforcement pass: caps blue (`#0A74D6`) text at max 18pt, strips Thin/Light/ExtraLight/Italic font variants, replaces with Regular or SemiBold.
- Verified output: zero `outerShdw`/`innerShdw` across all slides, layouts, masters, and theme. Zero text-on-text overlaps.
- Updated `BRAND_DESIGN_RULES.md` and `PROGRESS.md` with session findings.

### 2026-03-25 (Session 2) — Title sizing, noAutofit, v1 backup

- **Title size issue in Google Slides**: discovered that `<a:spAutoFit/>` in title textboxes caused Google Slides to display 22pt instead of the 18pt set in XML. Fix: replaced `spAutoFit` with `<a:noAutofit/>` and tightened textbox height from `Pt(size+10)` to `Pt(size+4)`.
- Corrected "RESUMEN EJECUTIVO" to "Resumen Ejecutivo" (title case, matching rest of document).
- Verified via raw XML that all title runs have `sz="1800"` (18pt) and `<a:noAutofit/>`.
- Confirmed zero text-on-text overlaps across all 27 slides (only intentional icon-on-box overlaps).
- Generated `VDI_VDA_Universidades_Final_v1.pptx` as backup of this version's output before structural redesign.

### 2026-03-26 — Whitepaper PDF Pipeline + Figma Upload

**PDF Whitepaper Generation (new pipeline):**
- Built `build_whitepaper_pdf.py` — converts DOCX content to branded PDF via HTML→Playwright/Chromium
- Test document: "AWS Virtual Desktops vs Thinfinity VDI on Oracle Cloud" (844 lines, 10 chapters)
- Generates 38-page branded PDF with cover, TOC, 10 chapters, contact page, footer
- Cover: navy bg 85% + white logo strip 15%, badge, Thinfinity+Cybele logos
- Interior: brandbook text styles applied, blue accent bar at bottom, callout boxes, styled tables
- Last page: contact section with CTA box, navy footer with copyright
- Output: `AWS_vs_Thinfinity_VDI_Whitepaper.pdf` (0.79 MB)

**Figma Whitepaper Upload (new capability):**
- Built `generate_wp_pages.py` — parses DOCX and generates 34 individual HTML pages (795x1125px each, matching Figma frame size from reference whitepaper)
- Each HTML page includes: `#capture-target` wrapper for precise Figma capture, Inter font, blue bar, page numbers, brandbook styles
- Successfully uploaded all 34 pages to Figma file `8RBfhSYgaCuo4uM82JqAHL` using `figmaselector=#capture-target` for correct dimensions
- Solved viewport-vs-frame size issue: capture script takes full viewport by default; fixed by wrapping content in `#capture-target` div and using `figmaselector` parameter
- PDF export from HTML pages: 34-page PDF via Playwright, merged with PyMuPDF

**Brandbook Typography Extraction:**
- Extracted exact text styles from Figma Brandbook (file `y7mHflD4ukCFDo6YsPzIf4`):
  - Main title: Inter SemiBold 600, 40px/53px, `#0A74D6` (node `926:1192`)
  - Section: Inter Medium 500, 26px/38px, `#373737` (node `926:1193`)
  - Subtitle: Inter Regular 400, 22px/35px, `#373737` (node `926:1195`)
  - Paragraph: Inter Regular 400, 17px/27px, `#515151` (node `926:1196`)
- Applied scaled versions to whitepaper HTML (0.55x factor for 795px page width)

**New files created:**
- `~/dashboard/wp-page-03.html` through `wp-page-36.html` — 34 whitepaper interior pages
- `~/Downloads/generate_wp_pages.py` — DOCX→paginated HTML generator
- `~/Downloads/build_whitepaper_pdf.py` — HTML→branded PDF generator
- `~/Downloads/AWS_vs_Thinfinity_VDI_Whitepaper.pdf` — Full branded PDF

### 2026-03-26 (Session 2) — Whitepaper Redesign & Styling

**Figma reference analysis:**
- Analyzed Figma whitepaper `73xvjMj0ha14tVMQBq8I1U` (Thinfinity Deployment Options) as design reference
- Extracted exact measurements: content at `left:60px, top:69px`, width 675px, page number at `right:60px, top:35px`, ribbon 9px at bottom
- Identified design patterns: labeled items with blue title + description, bullet lists with separators, callout boxes (#EEF4FD bg + blue border), pro/con check items

**Redesign pipeline (`redesign_wp.py`):**
- Replaces CSS entirely with Figma-reference typography and spacing
- Transforms labeled paragraphs (`<strong>Label:</strong> desc`) into styled `.labeled-item` with blue title + description + blue bullet
- Transforms short paragraph groups into `.bullet-item` with blue dot + separator lines
- Detects "Key Takeaway"/"Summary"/"Implication" patterns → `.callout-box` (light blue bg, blue border, rounded)
- Styles ✅/❌ items as green/red `.check-item`
- Body text: 12px Inter, line-height 1.6, color #515151
- Blue bar: `position:absolute; bottom:0; left:0; right:0; height:6px; z-index:10`
- Result: 581 elements transformed (179 labeled, 364 bullets, 14 callouts, 24 pro/con)

**Cover + closing pages (completed):**
- Cover: dark navy gradient, "Whitepaper" badge, white title, Thinfinity + Cybele logos (base64 embedded)
- Closing: SVG contact icons (location, phone, email), CTA box with blue gradient + white Thinfinity logo, pill-shaped buttons, navy footer with copyright + Cybele logo
- Created `thinfinity_logo_white_real.png` — actual white version (original `_white.png` was misleadingly blue)

**Pro/con icons:**
- Replaced ✅/❌ emoji with inline SVG circle-light icons (no fill, outline only)
- Green `#3DCCA1` circle + checkmark for pros
- Red `#E04040` circle + cross for cons

**Pagination recalibrated for 12px text:**
- `CHARS_PER_LINE = 75`, `SAFE_HEIGHT = 840`, `PAD_BOT = 55`
- Heights: H1=66, H2=50, H3=34, TABLE_ROW=28, LI=26
- Result: 43 content pages + cover + closing = 45 total

**Whitepaper pipeline moved to repo (`cybele_deckgen/whitepaper/`):**
- All 4 scripts accept paths via environment variables (`WP_DOCX_PATH`, `WP_OUTPUT_DIR`, `WP_DASHBOARD`, `WP_OUTPUT_PDF`) with fallback defaults
- `build_whitepaper.py` orchestrates the full pipeline: takes any DOCX, outputs branded PDF via temp dir
- Tested end-to-end: `python whitepaper/build_whitepaper.py input.docx output.pdf`

**Current working pipeline (stable):**
```bash
# Option A — Single command from repo:
cd C:/Users/NickCeraso/cybele_deckgen
python whitepaper/build_whitepaper.py <input.docx> [output.pdf]

# Option B — Step by step:
python whitepaper/generate_wp_pages.py    # 1. DOCX → HTML pages (795x1125px)
python whitepaper/redesign_wp.py          # 2. Apply Figma-style redesign
python whitepaper/generate_cover_closing.py  # 3. Cover + closing pages
python whitepaper/generate_pdf.py         # 4. Render PDF via Playwright+PyMuPDF
```
Output: 45-page branded PDF (4.57 MB)

**New/updated files:**
- `cybele_deckgen/whitepaper/build_whitepaper.py` — Orchestrator (single DOCX → branded PDF)
- `cybele_deckgen/whitepaper/generate_wp_pages.py` — DOCX → paginated HTML pages
- `cybele_deckgen/whitepaper/redesign_wp.py` — CSS + content transformation
- `cybele_deckgen/whitepaper/generate_cover_closing.py` — Cover + closing HTML pages
- `cybele_deckgen/whitepaper/generate_pdf.py` — HTML pages → merged PDF
- `cybele_deckgen/brand_assets/thinfinity_logo_white_real.png` — Actual white logo variant

### 2026-03-27 — Pipeline Hardening & Reusability Test

**Dynamic cover title extraction:**
- `build_whitepaper.py` now extracts the document title from the DOCX automatically
- Looks for first paragraph styled `Title` or `Heading1`, falls back to first non-empty paragraph, then filename
- Passes title via `WP_COVER_TITLE` env var to `generate_cover_closing.py`
- Cover page title is no longer hardcoded — updates automatically per document

**Design corrections from Figma reference:**
- Cover badge ("Whitepaper" pill): fixed to `#558BEE` (Blue/300 from Figma design system, node `1:677`)
- CTA box on closing page: gradient `#1E88E5 → #42A5F5 → #2196F3` with white Thinfinity logo
- Created `thinfinity_logo_white_real.png` — pixel-level white conversion (original `_white.png` was incorrectly blue `RGB(0,125,193)`)
- Pro/con icons: circle-light SVG (outline only, no fill) — green `#3DCCA1` check, red `#E04040` cross
- Contact icons on closing page: SVG line-art (location pin, phone, email) in `#0A74D6`

**Reusability test — second document:**
- Input: "Copy of Whitepaper - Moving your business to Saas.docx"
- Pipeline auto-extracted title: "Delivering Your Software as SaaS Using Thinfinity"
- Output: `Moving_your_business_to_SaaS.pdf` (10 pages, 0.59 MB)
- Confirmed: cover title updates, styling consistent, pipeline runs cleanly on any DOCX

### 2026-03-27 (Session 2) — PPTX Pipeline: New Document + Template Standardization

**New test case:** "CISO Risk Lens: Thinfinity vs Citrix" (34-slide source, 13.33"×7.5")

**Pipeline evolution:**
1. **Standard cover/closing template established** — all presentations now use the 2-slide `Copy of VDI_VDA_Universidades_Editable.pptx` as base. Source file cover/closing are never preserved. Cover title + subtitle are updated per document; tagline is removed.
2. **Adapted to 10"×5.625"** — source was 13.33"×7.5" (standard widescreen); output converted to Google Slides dimensions.
3. **New slide layouts**: `two_card_slide` (side-by-side comparison with icons), `content_with_items` (auto-grid numbered cards), `icon_content_slide` (large icon + text), `add_section_divider` (navy bg with number + title).
4. **Numbered circle fix** — original `02` in 0.3" circle caused digit wrapping (one number above, one below). Fixed: enlarged to 0.35", switched to single digit (`1` instead of `01`), size 12pt.
5. **Hyperlink color override discovery** — contact text on closing slide (`cybelesoft.com`, phone numbers) appeared blue despite `srgbClr val="FFFFFF"` in XML. Root cause: `<a:hlinkClick>` with `<ahyp:hlinkClr val="tx"/>` caused the theme's hyperlink color to override the run's fill color. Fix: strip all `<a:hlinkClick>` elements from contact run properties XML + force white on `endParaRPr`.
6. **Closing slide language rule** — if presentation content is in English, closing stays English; if content is in another language, closing must be translated to match.

**Key discoveries:**
- `python-pptx` `run.font.color.rgb = WHITE` does NOT override hyperlink colors — must remove `<a:hlinkClick>` at XML level
- Removing slides from `sldIdLst` without deleting the underlying parts causes orphaned ZIP entries and duplicate name warnings — always start from a clean 2-slide template
- `endParaRPr` (end-of-paragraph run properties) can retain old colors (`C6E1FA`) even after fixing all visible runs

**Files:**
- `~/Downloads/build_ciso_pptx.py` — Build script for CISO Risk Lens presentation
- `~/Downloads/CISO_Risk_Lens_Thinfinity_vs_Citrix_2026-03-27.pptx` — Output (32 slides, 360 shapes, 12 MB)

### 2026-03-27 (Session 3) — SVG Blog Illustration Pipeline

**Article:** "Replacing Citrix in Manufacturing: A No-Disruption Migration Guide for CIOs (2026)"

**3 sections illustrated:**
1. "Why Replace Citrix Now" — Light mode, hub-and-spoke layout (3 converging pressures)
2. "Production-Safe Migration Tooling" — Dark mode, 4 numbered gradient cards (RackWare, FSLogix, Datadog, Veeam)
3. "Why Thinfinity for Manufacturing" — Dark mode, center logo + 4 features with curved connectors

**Style reference:** Figma `1rA3ZWuHPxh1BW2YXfF1LR` node `8188:256` (Blog Posts — 2026)
**Iconography reference:** Figma `x0HMD1pXkcYdFM7NSaBvb4` node `8120:7263` (Cybele Design System — Cybfont)

**Key discoveries and process decisions:**

1. **Figma MCP asset URLs return SVG, not PNG** — calling `get_design_context` on individual icon symbol nodes returns a `figma.com/api/mcp/asset/UUID` URL. Despite looking like a raster endpoint, it serves native SVG with real `<path>` data. This is the breakthrough that enabled true Cybfont icon embedding.

2. **Figma SVG import only accepts native SVG primitives** — `<foreignObject>` (from dom-to-image), `<image>` with base64 data URIs, and external URL references are all silently dropped by Figma on import. Only `<rect>`, `<circle>`, `<text>`, `<path>`, `<line>`, `<polygon>`, `<linearGradient>`, `<g>`, nested `<svg>` work.

3. **Icon colorization** — Cybfont SVG paths come with `fill="black"`. To recolor: replace all `fill="(not none)"` with target color, same for `stroke`. Apply via regex before embedding.

4. **Typography sizes from reference** — analyzed existing blog illustrations in Figma: titles ~52px, subtitles ~26-28px, body ~18-20px. Content should fill ~70% of the 1920x1080 canvas.

5. **Dark/light mixing** — user preference is not 2 versions of each image, but rather alternating modes across the set for visual variety (e.g., A=light, B=dark, C=dark).

6. **Icon selection by concept** — icons should represent what the tool/concept *does*, not the brand logo. E.g., `import-export` for RackWare (moves VMs), `shield-ok` for Veeam (backup protection), `monitor-use` for Datadog (observability).

7. **Text synthesis** — titles max 6 words, descriptions 1-2 sentences focused on "what it does + why it matters for the migration."

**Files created:**
- `~/dashboard/citrix-migration-illustrations.html` — HTML preview with all 3 slides
- `~/dashboard/export-native-svgs.mjs` — Node.js script: fetches Cybfont SVG paths from Figma, builds native SVGs
- `~/Downloads/citrix-why-replace.svg` (24 KB) — Slide A, light
- `~/Downloads/citrix-migration-tooling.svg` (13 KB) — Slide B, dark
- `~/Downloads/citrix-why-thinfinity.svg` (20 KB) — Slide C, dark

### 2026-03-27 (Session 4) — SVG Blog Illustrations: New Article + Style Refinement

**Article:** "Secure Remote Desktop in 2025: 5 Strategic Priorities for Zero Trust and Hybrid VDI Success"

**3 sections illustrated (chosen for visual structure, not all sections are illustrable):**
1. "Strategic Drivers" — Light mode, hub-and-spoke (4 trends converging on Thinfinity hub)
2. "Enterprise Use Cases" — Dark mode, 4 solid-fill gradient cards (workforce, compliance, GPU, devs)
3. "Endpoint Control" — Light mode, center hub + 5 feature cards (2 left, 2 right, 1 bottom)

**Sections discarded and why:**
- Executive Summary: too generic, no visual structure
- DaaS vs VDI: argumentative text, not composable
- Comparison table: already visual as a table
- Action Points / Final Word / FAQ: short text, no strong visual concept

**New Python pipeline (`build_blog_svgs.py`):**
- Reads local SVG icons from `cybele_deckgen/icons/` (no Figma API calls needed)
- Extracts `viewBox` + inner `<path>` content, recolors via regex
- Builds 1920×1080 SVGs programmatically with layout functions
- Accepts DOCX input (extracts headings via `python-docx`)
- Auto-opens generated SVGs in browser tabs; new tabs on each iteration for visual comparison

**Design rules established:**
1. **Light/dark alternation** — always mix modes across the set (e.g., Light → Dark → Light for 3 images)
2. **Cards with solid fill** — not stroke/border. White text inside. Colors from accent palette (#7c3aed, #06b6d4, #d97706, #059669, #ec4899)
3. **Hub can be circle or rounded rect** — circles work well for center concepts
4. **Arrows: straight lines from closest lateral** — thick (36px stroke), with separate triangular arrowhead (34×67px, fill, wider than deep)
5. **Symmetric layouts preferred** — 2 left + 2 right (+ 1 bottom for 5 items)
6. **Every card should have a subtitle/description** — not just a title; reinforces the concept
7. **Ampersands must be escaped** — `&amp;` in SVG/XML text content
8. **No cards near the image title** — leave breathing room between title area and content

**Arrow style iterations (resolved):**
- Thin dashed lines → too subtle
- Filled polygon arrows → correct weight but straight only
- Curved bezier → didn't match Figma reference style
- L-shaped with cubic bezier corners → correct Figma pattern (`V → C → H`) but complex routing caused direction issues
- **Final: straight arrows from closest lateral** — simple, clean, reliable. Arrow exits perpendicular from card edge closest to hub, points directly at hub edge

**Figma reference analysis:**
- Examined 8+ illustrations from `1rA3ZWuHPxh1BW2YXfF1LR` (Blog Posts — 2026)
- Confirmed: cards use solid fill (not stroke), arrows are 36px stroke-width
- Arrow pattern from reference SVG: `M → V → C(cubic bezier) → H` with separate triangle arrowhead path
- For now, simplified to straight arrows — curved L-shape connectors to be revisited when layout requires them

**Files:**
- `~/Downloads/build_blog_svgs.py` — Python build script
- `~/Downloads/secure-rd-strategic-drivers.svg` (18 KB) — Slide A, light
- `~/Downloads/secure-rd-use-cases.svg` (13 KB) — Slide B, dark
- `~/Downloads/secure-rd-endpoint-control.svg` (6 KB) — Slide C, light

### 2026-04-17 (Session 1) — Blog Cover Visual System Analysis + First Generator

**Goal:** reverse-engineer the visual system of Cybele's existing blog covers to enable automated generation of new on-brand covers.

**Input analyzed:** `sample portadas.pdf` — contact sheet of 21 production blog covers (1840×1084 px each, embedded in PDF).

**Analysis method:**
- Extracted each cover individually via PyMuPDF `get_text("dict")` → bbox filtering
- Programmatic color quantization per cover (top 6 dominant colors + percentages via PIL `quantize`)
- Edge-sampling to detect gradient direction (top-lighter / bottom-lighter / diagonal)
- Visual catalog of hero objects, satellite elements, composition patterns, style fingerprint
- Cross-referenced against existing Cybele brand tokens (`BRAND_DESIGN_RULES.md`)

**Patterns identified (later refined during reconciliation):**
- 6 color families for gradients, reduced to named tokens and gradient recipes
- 5 composition patterns (later expanded to 6 archetypes after reconciliation)
- 11 hero primitives (shield, cloud, padlock, monitor, laptop, server, factory, robot arm, graduation cap, gears, coins)
- Satellite vocabulary: colored circular badge nodes, connection lines, halos, rings, pills, logo chips
- Style fingerprint: flat + gradients, halos, rounded corners, no textures, no 3D
- Most covers carry NO title text — title lives in CMS

**Test case — "Telecom Contact Centers at Scale" article:**
- First attempt (discarded): 6 covers each addressing a different section (the $47M problem, omnichannel, provisioning, energy savings, PCI-DSS, roadmap)
- **User feedback:** variants should be *six ways to draw the same core concept*, not six different angles
- Second attempt (accepted): 6 covers all expressing "VDI on OCI powering telecom contact center agents at scale" with different archetypes
- All 6 validated via lxml parse + Playwright render

**Deliverables:**
- `blog_covers/BLOG_COVER_RULES.md` — full visual system spec (13 sections, topic → kit matrix, anti-patterns)
- `blog_covers/reference/cover_01.png … cover_21.png` — 21 reference covers
- `blog_covers/build_telecom_cx_covers.py` — working prototype generator with helpers (`wrap`, `linear_grad`, `radial_grad`, `rings`, `pill`, `circle_badge`, `thinfinity_ring`, `agent_with_headset`, `ICON` dict)
- `blog_covers/output/` — 6 SVGs + 6 PNGs + preview.html

**Key SVG gotchas solved:**
- Unescaped `&` in `<text>` causes silent SVG parse failure → always `&amp;`
- Python 3.14 on Windows: `print()` with emojis fails (`cp1252` codec) → use `[ok]` / `[err]` markers
- IDs shared across SVGs in one HTML silently break fills → prefix per cover (`c1-`, `c2-`)

### 2026-04-17 (Session 2) — Parallel Session Reconciliation

**Context:** a second Claude Code session had been working on the same problem independently (blog cover visual system). Both sessions produced HANDOFF documents. User requested reconciliation so the two documents would not contradict and would complement each other.

**Input:**
- `Downloads/files/HANDOFF.md` — other session's handoff
- `Downloads/files/cover_variants.html` — other session's reference artifact with 6 SVG variants

**Method:**
- Side-by-side comparison of both HANDOFFs
- Verification of contested claims (e.g., checked `viewBox` in other session's SVGs, confirmed 1600×900 vs my 1840×1084)
- Explicit resolution per contradiction with user confirmation

**4 contradictions identified and resolved (user-confirmed):**

| # | Contradiction | Winner | Decision |
|---|---|---|---|
| 1 | Canvas size: 1840×1084 vs 1600×900 | Neither | **1920×1080** (true standard) |
| 2 | 5 patterns vs 6 archetypes | Other session | **6 archetypes A1–A6** — Editorial/poster separated |
| 3 | Color families A–F vs named tokens | Other session | **Named tokens only** |
| 4 | Python generator vs SVG templates | My session | **Generator only** — matches batch→review→export workflow |

**Deliverables:**
- `blog_covers/RECONCILIATION.md` — final decisions document, referenced by both HANDOFFs
- `blog_covers/HANDOFF.md` — rewritten as **generative brief** (not session log) — focuses on rules that enable generating new covers from a new article, usable by another session or as input to a future Claude Skill
- Updated `blog_covers/BLOG_COVER_RULES.md` — canvas now 1920×1080, archetype names A1–A6, topic matrix updated to gradient recipes
- Regenerated 6 telecom CX covers at 1920×1080

**Key insight on HANDOFF structure:** the first HANDOFF was a session log (what was done); the user explicitly wanted a **generative spec** (what rules enable future sessions to produce new covers). Rewritten accordingly so it can be dropped into a new session or packaged as a `SKILL.md`.

**Technical decision rationale (generator vs templates):** both approaches serve different users, but for the established workflow (*batch-generate 6 → review in HTML → approve → export SVG*), the generator wins on storage, maintenance, consistency, and propagation of brand changes. Templates would add overhead without payoff since fine visual tweaks happen in Figma post-approval, not pre-approval.

---

## Next Steps

### Immediate
- [ ] Add table of contents page to whitepaper pipeline
- [ ] Improve pagination to avoid cutting content blocks and reduce whitespace on sparse pages
- [ ] Move SVG illustration scripts to `cybele_deckgen/blog_illustrations/`
- [ ] Apply the reconciled decisions to the parallel session's HANDOFF (user to forward `RECONCILIATION.md` to that session)

### Short-term
- [ ] Build content extraction pipeline (Google Docs/DOCX → structured content → branded output)
- [ ] Test PPTX output in Google Slides and iterate
- [ ] Document all four pipelines (PPTX + PDF + SVG illustrations + SVG covers) for team reference
- [ ] Create reusable Cybfont icon fetcher module (shared across SVG illustration tasks)
- [ ] Package the blog cover system as a Claude Skill (`.claude/skills/cybele-blog-covers/SKILL.md`) derived from `HANDOFF.md`

### Medium-term — GitHub Repo
- [x] Move whitepaper scripts to `cybele_deckgen/whitepaper/`
- [x] Create blog cover system folder (`cybele_deckgen/blog_covers/`) with rules, handoff, reconciliation, prototype generator
- [ ] Move SVG illustration scripts to `cybele_deckgen/blog_illustrations/`
- [ ] Initialize GitHub repo with project structure
- [ ] Create separate repo for the blog cover system (`cybele-cover-system`) — structure proposed in `RECONCILIATION.md` §3
- [ ] Create README with setup instructions (Python deps, Node deps, MCP config, Figma auth)
- [ ] Add `.gitignore` for generated outputs, node_modules, __pycache__

### Medium-term — Web App
- [ ] Build Web App for team-wide access (stack TBD)
- [ ] Create brand guideline config that can be loaded by any generation script
- [ ] Add support for co-branded documents (Cybele + Oracle, Cybele + partner)

### Long-term
- [ ] Figma plugin or integration for direct design generation
- [ ] Multi-language support (EN/ES)
- [ ] Template library expansion (one-pagers, datasheets, case studies)
- [ ] Team onboarding documentation
- [ ] Build Cybfont icon index (name → concept mapping) for faster illustration generation
- [ ] Expand blog cover system: handle dark-mode variants if blog redesign calls for them

---

## File Structure

```
cybele_deckgen/
├── brand_assets/              # Logo PNGs and SVGs
│   ├── cybele_logo.png
│   ├── cybele_logo_white.png
│   ├── thinfinity_logo.png
│   ├── thinfinity_logo_white.png
│   └── thinfinity_logo_white_real.png  # Actual white variant
├── icons/                     # SVG icon source files
├── icons_png/                 # 200x200 PNG icons (dark + white variants)
├── brand_config.json          # Brand tokens (colors, fonts, icons list)
├── PROGRESS.md                # This file
├── BRAND_DESIGN_RULES.md      # Complete brand & design specification
│
├── whitepaper/                # ★ Whitepaper PDF pipeline
│   ├── build_whitepaper.py          # Orchestrator: DOCX → branded PDF
│   ├── generate_wp_pages.py         # Step 1: DOCX → paginated HTML pages
│   ├── redesign_wp.py               # Step 2: Figma-style CSS + content transforms
│   ├── generate_cover_closing.py    # Step 3: Cover + closing HTML pages
│   └── generate_pdf.py              # Step 4: HTML pages → merged PDF
│
├── blog_illustrations/        # ★ SVG blog illustration pipeline (in-article images, to be moved from ~/dashboard/)
│   ├── export-native-svgs.mjs       # Fetches Cybfont SVG paths + builds native SVG files
│   └── citrix-migration-illustrations.html  # HTML preview for browser iteration
│
├── blog_covers/               # ★ Blog cover generation system (added 2026-04-17)
│   ├── BLOG_COVER_RULES.md          # Full visual system spec (13 sections, topic → kit matrix)
│   ├── HANDOFF.md                   # Generative brief: how to produce new covers from an article
│   ├── RECONCILIATION.md            # Final decisions across parallel sessions
│   ├── build_telecom_cx_covers.py   # Working prototype generator (reference implementation)
│   ├── reference/                   # 21 production covers extracted from sample portadas.pdf
│   │   └── cover_01.png … cover_21.png
│   └── output/                      # Generated SVGs + PNGs + preview.html
│       ├── telecom_cx_0[1-6]_*.svg
│       ├── telecom_cx_0[1-6]_*.png
│       └── preview.html
│
├── build_final_pptx.py        # PPTX generator (in Downloads, to be moved)
├── build_branded_deck.py      # Earlier HTML-based deck builder
├── slide_templates.py         # Slide type definitions
├── text_to_content.py         # Content parser
├── generate_deck.py           # Deck orchestrator
└── quick_deck.py              # Quick generation script
```
