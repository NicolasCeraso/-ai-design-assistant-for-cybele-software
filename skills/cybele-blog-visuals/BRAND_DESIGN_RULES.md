# Cybele AI Design Assistant — Brand & Design Rules

> **What this file is.** The skill's self-contained copy of the Cybele brand system: colour,
> typography, logos. It must stay self-contained because the skill has to work when copied out of
> the repo, so it cannot read `_shared/BRAND.md` by path.
>
> `_shared/BRAND.md` is the team-facing original. **If the two ever disagree, that one is right and
> this one is stale** — fix it here and say so. A brand change lands in both, in the same commit.

> **Purpose:** This document contains all approved design decisions, brand rules, and technical specifications for generating branded documents (PPTX, PDF) and Figma designs for Cybele Software. Pass this file to any new Claude Code instance so it can continue working without re-discovering these rules.

---

## 1. Brand Identity

**Company:** Cybele Software, Inc.
**Products:** Thinfinity Workspace, z/Scope
**Website:** cybelesoft.com
**Contact:** sales@cybelesoft.com | +1 (302) 892-9625 | Toll Free: +1 (866) 462-9768
**Copyright:** ©2026 Cybele Software Inc. All rights reserved. Thinfinity® and z/Scope® are registered trademarks of Cybele Software Inc.

---

## 2. Color Palette

### Canonical palette 06/26 — use this for all new work

Copied from the team's brand system (`_shared/BRAND.md` §1), which names it *"canonical … current —
use this for new work"*.

| Token | Hex | Role |
|---|---|---|
| `NAVY` | `#0A1A2F` | Dark-mode background, dividers, cover |
| `CANVAS` | `#EEF4FB` | Light-mode background (very light blue) |
| `WHITE` | `#FFFFFF` | White-mode background, base cards |
| `BRAND_BLUE` | `#0F7FE0` | **Details only** — title text, bullets, accents, pill strokes. **Not** for container fills. |
| `BLUE_LIGHT` | `#5BAFFF` | Accent on navy (titles/labels) |
| `AZURE` | `#0AA9FF` | Diagram connectors (chevrons) |
| `MINT` | `#3DCCA1` | Positive accent, bullet dots, milestone labels |
| `ORACLE_RED` | `#C74634` | Oracle co-branding, negative accent |
| `TEXT_PRIMARY` | `#2E2E2E` | Body on light |
| `TEXT_BODY` | `#454B57` | Secondary body on light |
| `TEXT_ON_NAVY` / `…_MUTED` | `#E8EEF7` / `#A8B4C4` | Body / muted on navy |
| `DARK_CARD` | `#122542` | Base card on navy |

**Container accent fills** (low contrast — never the vibrant `#0F7FE0`): soft `#DCE8F8` on
light/white · muted `#1C3E63` on dark. `#0A74D6` (deeper Cybele blue) is reserved for **table header
rows**.

### Superseded palette (until 06/26) — legacy artifacts only

`Primary Blue #0A74D6` · `Navy #0B1A3B` · `Dark Text #373737` · `Gray Text #515151` ·
`Light BG #F0F4F8` · `Green #3DCCA1`. Kept so an older visual can be matched when one is revised.
**Never pick these for new work.** Until 2026-09-04 this file listed them as the primary palette,
which is why visuals generated before that date carry `#0A74D6` titles and a `#0B1A3B` navy.

### Applied derivatives — blog visuals (2026-06 reduced palette)

Added by the reduced-palette amendment. These are the values the blog specs draw with; each one is
named by an element rule in `SECTION_RULES.md`. (The semantic-state system that introduced the green
and the info blue was removed on 2026-09-04; the colours stay available, but nothing is coloured by
"state" any more.)

| Token | Hex | Usage |
|-------|-----|-------|
| Surface dark | `#021425` | Dark-mode page surface for blog visuals (`blue-cybele/900`) |
| Surface light | `#EEF4FD` | Light-mode page surface (`blue/50`) |
| Deep green | `#0FAD7E` | Green for text and pills (deeper than `#3DCCA1`, holds contrast on white) |
| Soft green panel | `#C6F6E8` | Soft green fill |
| Bright blue | `#0AA9FF` | Bright blue accent (still a raw fill, no Figma variable yet) |
| Soft blue panel | `#C7EBFF` | Soft blue fill |
| Deep red | `#7B1818` | Deep red on the dark surface (panel: the same at 45%) |
| Light red | `#FCA5A5` | Light red for secondary text on the dark surface |
| Slate | `#94A3B8` | Secondary text on the dark surface |
| Brand violet | `#8878ED` / `#321BC8` | `blue-violet/500` and `/700` — measured use, never a fill-by-default |

### Additional accents (unchanged)

| Token | Hex | Usage |
|-------|-----|-------|
| Red Accent | `#E04040` | Negative/problem indicators (VPN issues, etc.) |
| Light Blue BG | `#E8F4FD` | Feature boxes, use case cards |
| Card Blue BG | `#E8F1FB` | Alternative card background |

---

## 3. Typography

### Font Family: Inter

| Weight | Name in PPTX | Usage |
|--------|-------------|-------|
| **SemiBold (600)** | `Inter SemiBold` | Slide titles, section headers, box titles, bold labels |
| **Regular (400)** | `Inter` | Body text, bullet lists, descriptions, subtitles |

### Approved Rules

- **Titles:** Inter SemiBold, `bold=True`, colour `BRAND_BLUE` (`#0F7FE0`)
- **Subtitles:** Inter Regular, `bold=False`, colour `TEXT_BODY` (`#454B57`)
- **Body text:** Inter Regular, `bold=False`, colour `TEXT_PRIMARY` (`#2E2E2E`)
- **Bold labels inside body:** Inter SemiBold, `bold=True`
- **Text on dark/colored backgrounds:** Inter SemiBold or Regular, color White
- **NEVER use italic** — no text should ever be set to italic
- **NEVER use Thin weight** — always use Regular (400) minimum
- Google Slides compatible (Inter is natively available in Google Slides)

### Size Guide (PPTX)

| Element | Size (pt) |
|---------|-----------|
| Slide title | 22 |
| Subtitle | 14 |
| Box title / label | 9–11 |
| Body text | 8–10 |
| Footer / small text | 7–8 |
| Section divider title | 22 |
| Numbers in numbered boxes | 16 |

---

## 4. Visual Design Rules

### APPROVED — Do These:

- **Flat solid fills** on all shapes — no exceptions
- **No borders** on colored boxes (`shape.line.fill.background()`)
- **Rounded rectangles** for content boxes (corner radius ~5%)
- **Thin blue accent line** (3pt) under slide titles
- **Icons ONLY inside container shapes** — never floating loose on the slide
- **Logos maintain aspect ratio** — never stretch or distort
- **White backgrounds** on content slides
- **Navy backgrounds** (`NAVY` `#0A1A2F`) only on cover, section dividers, and closing slides

### FORBIDDEN — Never Do These:

- **No shadows** on any element — strip all `effectLst`, `effectDag`, `outerShdw`, `innerShdw` XML
- **No gradients** — only solid color fills
- **No italic text** — anywhere
- **No Thin weight font** — minimum is Regular (400)
- **No shading/glow effects** on any shape
- **No deformation of logos** — always preserve aspect ratio

### Shadow Removal (Technical)

Every shape must have shadows explicitly removed via XML:

```python
def remove_shadow(shape):
    shape.shadow.inherit = False
    el = shape._element
    ns = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
    for tag in ['effectLst', 'effectDag', 'outerShdw', 'innerShdw']:
        for e in list(el.iter(ns + tag)):
            e.getparent().remove(e)
    spPr = el.find(ns + 'spPr') or el.find('.//' + ns + 'spPr')
    if spPr is not None:
        for e in list(spPr.findall(ns + 'effectLst')):
            spPr.remove(e)
        etree.SubElement(spPr, ns + 'effectLst')  # empty = no effects
```

Apply `remove_shadow()` on: `add_shape()`, `add_textbox()`, `add_box()`, and any other shape creation.

---

## 5. Slide Layout — Presentations

> **Palette note.** This section describes the PPTX pipeline, which this skill does not run. Its hex
> values are the **superseded** palette (§2), kept as the record of how existing decks were built.
> New work — including every blog visual — uses the canonical 06/26 tokens in §2.

### Dimensions

- **Google Slides standard:** 10" x 5.625" (9144000 x 5143500 EMU)
- **Aspect ratio:** 16:9

### Logo Placement on Content Slides

| Logo | Position | Size |
|------|----------|------|
| Oracle | Top-left (left=0.2", top=0.12") | ~0.55" wide, auto height |
| Cybele | Top-right (right edge - 0.75", top=0.15") | ~0.55" wide, auto height |
| Thinfinity | Bottom-right (right edge - 0.85", bottom - 0.35") | ~0.7" wide, auto height |

### Content Slide Structure

```
┌─────────────────────────────────────────────────┐
│ [Oracle logo]                    [Cybele logo]   │
│                                                   │
│ Title (Inter SemiBold 22pt, Blue)                │
│ ─────────────────────────────── (blue line 3pt)  │
│                                                   │
│ ┌─────────────────┐  ┌─────────────────┐        │
│ │ [icon] Box Title │  │ [icon] Box Title │        │
│ │                  │  │                  │        │
│ │ Body text...     │  │ Body text...     │        │
│ └─────────────────┘  └─────────────────┘        │
│                                                   │
│                              [Thinfinity logo]   │
└─────────────────────────────────────────────────┘
```

### Cover Slide (from source file, do NOT generate)

- Use the branded cover from `Copy of VDI_VDA_Universidades_Editable.pptx` (slide 1)
- Blue wave background, Thinfinity + Oracle logos, white title
- Do NOT modify — keep intact from source

### Closing Slide (from source file, do NOT generate)

- Use the branded closing from the same source file (slide 2)
- Contains animated GIF wave element (image/gif, 1200x1200, 750 frames)
- "Thanks for watching!", contact info, social media icons, Cybele logo
- Do NOT modify — keep intact from source

### Section Divider Slide

- Full navy rectangle background (`#0B1A3B`)
- White title text, centered
- No logos needed on dark divider slides

---

## 6. Slide Types — Presentation Templates

### Numbered Boxes Row
Horizontal row of 4-5 boxes with number + text. Used for listing challenges, steps.

### Two-Column Icon Boxes
Two side-by-side light-colored boxes, each with icon + bold title + bullet list. Used for comparisons, use cases.

### Grid Boxes (2x2, 2x3)
Grid of boxes with titles and descriptions. Used for multiple items, features, use cases.

### Comparison Slide
Left vs Right columns, optionally with colored accent bars. Used for Citrix vs Thinfinity, Traditional vs Cloud.

### Highlight Boxes
Green-accent boxes at bottom of slides for key metrics (savings, percentages).

---

## 7. Document Branding — Whitepapers

### Cover Pattern
- Navy/dark blue gradient background
- Badge/pill tag at top (category: "Whitepaper")
- Large white title (Inter SemiBold)
- White subtitle
- Thinfinity + Cybele logos at bottom

### Interior Pages
- White background
- Page number top-right
- Section titles (H2): Inter SemiBold, Primary Blue
- Body: Inter Regular, Dark Text
- Circled icons for feature lists (blue, green, orange borders)
- Large blue numbers for "Key Takeaways"
- Tables with blue headers

### Back Cover
- CTA card: dark blue background, Thinfinity logo, "Start today" / "Book a call" buttons
- Contact: address, phone, email with icons
- Footer: navy background, copyright, Cybele logo right

---

## 8. Asset Locations

**How to find these assets** — try in order, and use the first that exists:

1. an `assets/` folder inside this skill;
2. `$CYBELE_DECKGEN_DIR/brand_assets/` (and `/icons/`), when that environment variable is set and the path exists;
3. `web-app/data/brand-assets/` when running inside the project repo;
4. otherwise, **say which asset you need and ask the user for it.** Never guess a path, and never
   insert a username into one.

Exact filenames vary between those locations (`cybele_logo.svg` vs `cybele-logo.svg`); match by name,
not by exact spelling. The inventories below say what the set contains.

### Logos

```
brand_assets/
├── cybele_logo.png          (700x260, dark, RGBA)
├── cybele_logo_white.png    (700x260, white, RGBA)
├── cybele_logo.svg
├── cybele_logo_white.svg
├── thinfinity_logo.png      (900x240, dark, RGBA)
├── thinfinity_logo_white.png (900x240, white, RGBA)
├── thinfinity_logo.svg
├── thinfinity_logo_white.svg
└── arch_basic.svg
```

**Oracle logo:** `oracle-logo.png` in the same asset set (5484x709, red, RGBA)

### Icons (200x200 RGBA each)

```
icons_png/
├── audit-log.png / audit-log_white.png
├── broker.png / broker_white.png
├── cloud.png / cloud_white.png
├── dollar-sign.png / dollar-sign_white.png
├── enterprise-ztna.png / enterprise-ztna_white.png
├── gateway.png / gateway_white.png
├── gpu-fast.png / gpu-fast_white.png
├── lock-check.png / lock-check_white.png
├── no-vpn.png / no-vpn_white.png
├── pc.png / pc_white.png
├── remote-work.png / remote-work_white.png
├── scale.png / scale_white.png
├── search.png / search_white.png
├── shield.png / shield_white.png
├── stats.png / stats_white.png
├── user.png / user_white.png
└── vdi.png / vdi_white.png
```

SVG originals: the `icons/` folder of the same asset set

### Icon Usage Guide

| Icon | Use For |
|------|---------|
| `vdi` | VDI, desktops, virtual environments |
| `cloud` | Cloud, OCI, infrastructure |
| `shield` | Security, compliance |
| `lock-check` | Zero Trust, access control, identity |
| `dollar-sign` | Cost, finance, savings |
| `scale` | Scalability, growth |
| `user` | Users, students, teachers, stakeholders |
| `remote-work` | Remote access, browser access, clientless |
| `gpu-fast` | GPU, performance, CAD |
| `stats` | Metrics, data, analytics |
| `enterprise-ztna` | ZTNA, Zero Trust Network Access |
| `no-vpn` | VPN problems, no-VPN solutions |
| `pc` | Desktop, workstation, physical labs |
| `broker` | Orchestration, policies, management |
| `gateway` | Network, gateway |
| `audit-log` | Compliance, audit, logging |
| `search` | Analysis, investigation |

---

## 9. PPTX Technical Approach

### Building a Presentation

1. **Start from a source PPTX** that has the branded cover + closing slides
2. **Insert blank content slides** between them using `prs.slides.add_slide(blank_layout)`
3. **Reorder XML** so closing slide moves to the end:
   ```python
   sldIdLst = prs._element.sldIdLst
   slide_ids = list(sldIdLst)
   closing = slide_ids[1]
   sldIdLst.remove(closing)
   sldIdLst.append(closing)
   ```
4. **Build content** on each slide using helper functions
5. **Never touch** the cover or closing slides

### Text Must Use Explicit Runs

Do NOT use `p.text = "..."` followed by `p.font.name = "Inter"` — this does not reliably set fonts.

Always use:
```python
run = p.add_run()
run.text = "..."
run.font.name = "Inter SemiBold"  # or "Inter"
run.font.size = Pt(22)
run.font.bold = True  # or False
run.font.color.rgb = RGBColor(0x0A, 0x74, 0xD6)
run.font.italic = False  # ALWAYS False
```

### Source Files for Cover/Closing

- **Source PPTX** (historical reference, not required by this skill): `Copy of VDI_VDA_Universidades_Editable.pptx`
  - Slide 1: Cover (8 shapes, includes logos and wave image)
  - Slide 2: Closing (15 shapes, includes animated GIF, social icons, Cybele logo)
  - Dimensions: 10" x 5.625" (Google Slides standard)

### Python Dependencies

```
python-pptx >= 1.0.2
PyMuPDF >= 1.27.1
Pillow >= 12.1.1
```

### Main Script

Historical: `build_final_pptx.py`, from the PPTX pipeline. It lives outside this repo and is
not an input to the blog-visuals skill — if you cannot find it, carry on without it.

---

## 10. Figma Integration

### MCP Servers

- **`claude.ai Figma`** — Cloud, read-only (screenshots, metadata, design context)
- **`figma-remote-mcp`** — Local, read + write (`generate_figma_design`)
- Both authenticated for user Nick Ceraso (nceraso@cybelesoft.com)

### Design System File

- **File:** Cybele Design System
- **Key:** `x0HMD1pXkcYdFM7NSaBvb4`
- **Sections:**
  - Colors: `node-id=2689-326`
  - Typography: `node-id=2689-316`
  - Icons (Cybfont): `node-id=2689-4636` and `node-id=8120-7263`
  - Logos: `node-id=2689-932`
  - Grid: `node-id=2440-316`
  - Breakpoints: `node-id=2701-24352`
  - Main Components: `node-id=2689-19404`
  - Resources: `node-id=2689-5910`

### Brandbook File

- **File:** Cybele Brandbook
- **Key:** `y7mHflD4ukCFDo6YsPzIf4`
- **Section used:** `node-id=926-939`

### HTML-to-Figma Workflow

1. Generate HTML/CSS in a local working folder
2. Serve with `npx http-server -p 8080 -c-1`
3. Add capture script: `<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>`
4. Call `generate_figma_design` with `outputMode: existingFile`, provide `fileKey` and `nodeId`
5. Open page with capture hash
6. Poll `captureId` every 5s until `completed`
7. Open Figma to see result

---

## 11. Whitepaper Reference Designs in Figma

| Document | File Key | Node ID |
|----------|----------|---------|
| Transforming Digital Workspaces | `3nDzupbog4IeureY5DZxyT` | `0:1` |
| AWS vs Thinfinity VDI on OCI | `3a6xHucGqzJ031REc3pMRO` | `11:489` |
| Deployment Options | `RHnnX0bN67RvsvpeLxpltE` | `0:1` |
| Zero Trust + PAM | `nrEht2faLJKl4aOUsFr7ah` | `0:1` |
| POS Remote Access | `m2QQD3VhsBzHzN4LKVD7Sq` | `0:1` |
| ROI Comparison | `lTv8KdbEAkS2pJFJmp6QeU` | `0:1` |
| Master Services Agreement | `K99ecYxLAbrZBR8B16V6fB` | `1:355` |
| GPU Whitepaper | `neZepbihR0yvjmQ8xp9Mwf` | `4:1434` |
| Deployment Options (alt) | `73xvjMj0ha14tVMQBq8I1U` | `0:1` |

---

## 12. Known Issues & Pending Items

- **Cybfont** icon font not installed locally — using PNG icons as workaround
- PPTX text sizing and spacing needs fine-tuning per slide
- Need to validate full PPTX rendering in Google Slides
- `build_final_pptx.py` still lives outside the repo
- Oracle logo should be moved to `brand_assets/` for consistency
- Whitepaper template (`build_whitepaper.py`) not yet created
- Web App for team not yet started
