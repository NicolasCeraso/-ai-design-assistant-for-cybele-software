# Reconciliation — Unified decisions for both HANDOFFs

> ⚠️ **Journal, not a specification.** This file records how the system was built and why.
> The design rules live in `BLOG_COVER_RULES.md` (covers) and `BRAND_DESIGN_RULES.md` (brand
> tokens); the counts of covers and section illustrations live in `SKILL.md` → INVOCATION
> MODES. Where this file disagrees with those, they win. Never use it as a stand-in for a
> rule file you could not open.

> **Purpose:** Two parallel Claude Code sessions produced independent HANDOFF documents for the same project (Cybele blog cover visual system). This document records the final decisions — confirmed by Nick Ceraso on 2026-04-17 — that both HANDOFFs must reflect.

**Source documents:**
- **H1:** `cybele_deckgen/blog_covers/HANDOFF.md` (this session — visual analysis + Python generator)
- **H2:** `Downloads/files/HANDOFF.md` (other session — visual analysis + SVG templates proposal)
- **H2 reference artifact:** `Downloads/files/cover_variants.html`

---

## 1 · Where both sessions agreed (confirmed, no change)

| Topic | Shared conclusion |
|---|---|
| Editorial rule | Variants = same idea, different composition. NOT six different angles on the article. |
| Red for pain only | Red/dramatic palette reserved for "problem" covers. Never default to red for "big". |
| Icon vocabulary | Small consistent set (shield, cloud, factory, monitor, server, robot arm, Thinfinity mark, phone, chat, email, social, video, check, X, warning, receipt). Use canonical glyphs, don't reinvent. |
| Third-party logos | Oracle / AWS / Azure / etc. rendered as a generic cloud glyph + text label. No pixel-accurate reproductions. |
| Illustration style | Flat vector. No outlines. Soft internal gradients. Radial white halo behind the focal element. |
| Titles on cover | Short (3–6 words) in a chip (rounded-rect with fill). Most covers have NO headline — title lives in CMS. |
| Font stack | Inter with system fallback. |
| Figma compatibility | No `<foreignObject>`, no `<image>` tags, no external URLs, no base64. Self-contained SVGs only. |

---

## 2 · Decisions on contradictions

### 2.1 Canvas size → **1920 × 1080 px (16:9)**

| Source | Canvas | Ratio |
|---|---|---|
| H1 (my session) | 1840 × 1084 px | 5:3 (odd) |
| H2 (other session) | 1600 × 900 px | 16:9 |
| **Final decision** | **1920 × 1080 px** | **16:9** |

**Rationale:** H1's 5:3 came from the embedded bbox in `sample portadas.pdf`, not from the intended design. H2's 16:9 matches standard web/social/blog hero dimensions. Nick confirmed 1920×1080 as the correct export size.

**Impact:**
- All archetype templates use `viewBox="0 0 1920 1080"`
- All existing SVGs (both H1's 6 generated covers and H2's `cover_variants.html`) must be migrated to 1920×1080

---

### 2.2 Number of compositions → **6 archetypes (H2's model)**

Adopt H2's 6-archetype system. H1's 5 patterns map 1:1 onto the first five; the sixth (Editorial/poster) is a distinct archetype H1 had collapsed into a color family.

| Unified name | Description |
|---|---|
| **A1 Hub-and-spokes** | Central focal object with satellite icons orbiting, connected by dotted curves |
| **A2 Duality** | Two complementary halves of the same concept, joined by a beam or arc |
| **A3 Hero + halo** | One monumental subject floating in radiant space, minimal supporting elements |
| **A4 Stack / ecosystem** | Three (or four) equal cards in a row — platform/integration stories |
| **A5 UI mockup** | Realistic product panel floating on dark background. Two flavors: *agent console* vs *admin / Cloud Manager dashboard* |
| **A6 Editorial / poster** | Saturated, cinematic composition. Two flavors: *dark editorial* (red radial — problem covers only) and *poster editorial* (violet-blue radial — aspirational product hero) |

**Rationale:** A6 has distinct anatomy (radial background, sparkles, cinematic framing) independent of color. Separating it yields a cleaner system.

---

### 2.3 Color system → **Named tokens only**

Adopt H2's named-token palette as the sole color layer. Drop H1's A–F "family" editorial grouping — the gradient recipes below already provide the editorial shortcut.

**Tokens (from H2 §3.1):**

| Token | Hex | Role |
|---|---|---|
| `blue-deep` | `#0f1e6e` | Primary brand, darkest blue |
| `blue-royal` | `#2b3eaa` | Primary brand, mid blue |
| `cyan` | `#4dd4c8` | Accent, bright cool |
| `teal` | `#3ac6a6` | Success / positive state |
| `violet` | `#6a4cc8` | Accent, violet-blue |
| `violet-light` | `#a98cdb` | Accent, softer violet |
| `magenta` | `#b06fd9` | Accent for "social" category |
| `warning` | `#f2c14e` | Semantic — warning |
| `danger` | `#d64040` | Semantic — error / alarm |
| `danger-deep` | `#6b0f0f` | Editorial "problem" covers |
| `ink` | `#0a1533` | Text on light, dark surfaces |
| `paper` | `#f3f5fb` | Light surface / background |
| `white` | `#ffffff` | Highlights, halos, icon badges |

**Gradient recipes (from H2 §3.2):**

| Recipe | Stops | Use |
|---|---|---|
| `cyan-to-blue` | `cyan` → `blue-royal` | Default positive cover background |
| `violet-to-blue` | `violet` → `blue-deep` | Product-hero covers |
| `teal-to-navy` | `teal` → `blue-deep` | Compliance / reliability covers |
| `red-dramatic` | radial `#b52323` → `danger-deep` → `#3a0606` | Editorial "problem" covers only |
| `halo` | radial `white` 0.5 → transparent | Always behind focal element |
| `monitor-body` | `blue-deep` → `ink` | Device frames |

---

### 2.4 Technical approach → **Python generator only**

Adopt H1's Python generator as the sole production method. Drop H2's SVG-template proposal.

**Rationale (approved by Nick):** Nick's workflow is always *batch-generate → review in HTML → approve one → export native SVG for Figma*. For this workflow the generator wins on every resource axis:

| Criterion | Winner |
|---|---|
| Storage (single script vs 6 templates × 6 archetypes) | Generator |
| Producing 6 variants for one article | Generator (one command) |
| Maintenance (change shield style once → affects all covers) | Generator |
| Consistency (impossible to drift out of system — tokens enforced in code) | Generator |
| Review HTML (auto-produced alongside SVGs) | Generator |
| Export native SVG for Figma | Tie (both produce identical Figma-compatible SVG) |

Fine-grained visual tweaks happen **in Figma after approval**, not before — so templates' main advantage (editability pre-approval) doesn't apply to this workflow.

**What this means practically:**
- `archetypes/*/template.svg` and `scripts/new-cover.js` from H2's proposed repo structure are **dropped**
- H1's `build_telecom_cx_covers.py` is the working prototype; it will be refactored into a reusable package

---

### 2.5 Reference covers → **21 from PDF is baseline**

Nick confirmed that `sample portadas.pdf` is the canonical reference set. H2's mention of 29 was likely a miscount or included smaller bbox variants. Moving forward: 21 reference covers in `examples/reference/`.

---

## 3 · Final repo structure

Reflects the decisions above: generator-only, 6 archetypes, named tokens, 16:9 canvas.

```
cybele-cover-system/                    # repo root (exact name TBD by Nick)
├── README.md                           # Quickstart
├── STYLE_GUIDE.md                      # The visual bible — tokens, archetypes, icons
├── HANDOFF_H1.md                       # Archived for context
├── HANDOFF_H2.md                       # Archived for context
├── RECONCILIATION.md                   # This document (final decisions)
│
├── tokens/                             # Ground-truth design tokens
│   ├── colors.json                     # Named tokens (§2.3)
│   ├── gradients.json                  # Gradient recipes (§2.3)
│   └── typography.json                 # Font stack, sizes, weights
│
├── docs/
│   └── archetypes/                     # One markdown per archetype
│       ├── a1-hub-and-spokes.md        # Anatomy, when to use, pitfalls
│       ├── a2-duality.md
│       ├── a3-hero-halo.md
│       ├── a4-stack-ecosystem.md
│       ├── a5-ui-mockup.md              # agent-console + admin-dashboard flavors
│       └── a6-editorial-poster.md       # dark + poster flavors
│
├── cybele_covers/                      # Python package (H1's generator, refactored)
│   ├── __init__.py
│   ├── pyproject.toml
│   ├── tokens.py                       # Loads tokens/*.json
│   ├── svg_helpers.py                  # wrap, gradients, halos, pill, badge, rings
│   ├── icons.py                        # ICON dict + glyph helpers
│   ├── heroes/                         # Reusable hero primitives
│   │   ├── shield.py
│   │   ├── cloud.py
│   │   ├── monitor.py
│   │   ├── agent.py                    # with headset
│   │   ├── factory.py
│   │   ├── server.py
│   │   ├── thinfinity_ring.py
│   │   └── ...
│   ├── archetypes/                     # One per A1–A6
│   │   ├── a1_hub_and_spokes.py
│   │   ├── a2_duality.py
│   │   ├── a3_hero_halo.py
│   │   ├── a4_stack_ecosystem.py
│   │   ├── a5_ui_mockup.py
│   │   └── a6_editorial_poster.py
│   ├── builder.py                      # Cover class: archetype × tokens × hero × satellites → SVG
│   └── render.py                       # Playwright SVG → PNG (for HTML preview)
│
├── examples/
│   ├── reference/                      # 21 reference PNGs from sample portadas.pdf
│   └── telecom-contact-center-vdi/
│       ├── article.md                  # Source copy
│       ├── generate.py                 # Script that produced the 6 covers
│       ├── covers/                     # 6 approved SVGs at 1920×1080
│       └── preview.html                # Auto-generated HTML comparator
│
└── scripts/
    ├── validate_tokens.py              # Lint: colors in SVGs are from tokens/
    ├── validate_svg.py                 # Lint: ID prefixing, Figma-safe, no forbidden elements
    └── generate.py                     # CLI entry: python scripts/generate.py --article <path> --variants 6
```

---

## 4 · Alignment actions (per HANDOFF)

### H1 (my HANDOFF) — updates applied in the same commit as this reconciliation:

- §1 canvas → **1920×1080 (16:9)**
- Composition names **A1–A6** (not P1–P5). Add A6 Editorial/poster.
- §5.1 repo structure → unified layout from §3 above
- Drop all "family A–F" references in favor of token names
- Add reference to `RECONCILIATION.md` at top
- `BLOG_COVER_RULES.md` regenerated to match

### H2 (other session's HANDOFF) — suggested edits (to be applied by that session):

- §6.1 canvas → **1920×1080** (currently 1600×900)
- §8 repo structure → drop `archetypes/*/template.svg`, add `cybele_covers/` Python package instead
- §9 implementation roadmap → Phase 2 "archetype templates" becomes "archetype Python builders"
- Reference `RECONCILIATION.md` at top

---

## 5 · Still open (Nick to confirm before repo session starts)

1. **Repo name** — proposals: `cybele-cover-system`, `cybele-blog-covers`, `cybele_covers`
2. **Repo visibility** — private or public?
3. **Thinfinity mark** — use `brand_assets/thinfinity_logo.svg` (already available) or the stylized simplified version from the generator?
4. **CI** — set up GitHub Actions for the lint scripts from day 1, or defer?

---

## 6 · What the next repo session can start on safely

- Scaffold the repo structure from §3
- Transcribe tokens into `tokens/colors.json` and `tokens/gradients.json` from §2.3
- Copy 21 reference PNGs into `examples/reference/`
- Port H1's `build_telecom_cx_covers.py` into `cybele_covers/` package, splitting helpers by module
- Write `docs/archetypes/*.md` — one page per archetype (anatomy, when to use, pitfalls)
- Regenerate the 6 telecom-CX covers at 1920×1080 as the canonical example

All of this can happen before Nick answers §5 questions.

---

*End of reconciliation — decisions confirmed by Nick on 2026-04-17.*
