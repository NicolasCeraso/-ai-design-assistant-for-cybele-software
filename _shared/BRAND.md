# Cybele — Shared Brand System

> Brand rules common to **every** task (presentations, documents, blog, architecture). Each task doc adds only its task‑specific rules and references this file.

**Company:** Cybele Software, Inc. · **Products:** Thinfinity Workspace, z/Scope · cybelesoft.com
**Contact:** sales@cybelesoft.com · +1 (302) 892‑9625 · Toll‑free +1 (866) 462‑9768
**Copyright:** ©2026 Cybele Software Inc. All rights reserved. Thinfinity® and z/Scope® are registered trademarks of Cybele Software Inc.

---

## 1. Color palette

### Canonical palette **06/26** (current — use this for new work)

| Token | Hex | Role |
|---|---|---|
| `NAVY` | `#0A1A2F` | Dark‑mode background, dividers, cover |
| `CANVAS` | `#EEF4FB` | Light‑mode background (very light blue) |
| `WHITE` | `#FFFFFF` | White‑mode background, base cards |
| `BRAND_BLUE` | `#0F7FE0` | **Details only** — title text, bullets, accents, pill strokes. **Not** for container fills. |
| `BLUE_LIGHT` | `#5BAFFF` | Accent on navy (titles/labels) |
| `AZURE` | `#0AA9FF` | Diagram connectors (chevrons) |
| `MINT` | `#3DCCA1` | Positive accent, bullet dots, "Hito" labels |
| `ORACLE_RED` | `#C74634` | Oracle co‑branding, negative accent |
| `TEXT_PRIMARY` | `#2E2E2E` | Body on light |
| `TEXT_BODY` | `#454B57` | Secondary body on light |
| `TEXT_ON_NAVY` / `…_MUTED` | `#E8EEF7` / `#A8B4C4` | Body / muted on navy |
| `DARK_CARD` | `#122542` | Base card on navy |

**Container accent fills (low contrast — never the vibrant `#0F7FE0`):** soft `#DCE8F8` on light/white · muted `#1C3E63` on dark. `#0A74D6` (deeper Cybele blue) is reserved for **table header rows**.

### Previous canonical (until 06/26) — legacy reference only
`Primary Blue #0A74D6` · `Navy #0B1A3B` · `Dark Text #373737` · `Body #515151` · `Light BG #F0F4F8` · `Green #3DCCA1`. Kept for legacy artifacts; new work uses the 06/26 tokens above. Full brand scales (Blue Cybele, Thinfinity, Violet, Purple, Pink, Red, Orange, Yellow, Green, Water‑Green, 50–900) live in the Figma Design System.

---

## 2. Typography — **Inter**

- **Inter SemiBold** → titles, headers, labels. **Inter** (Regular) / **Inter Medium** → body.
- **Never** italic. **Never** Thin/ExtraLight (Regular 400 minimum).
- Brandbook text styles (Figma): Main title SemiBold 40/53 · Section Medium 26/38 · Subtitle Regular 22/35 · Paragraph Regular 17/27.
- ⚠ **Local rendering caveat:** only the *variable* Inter font installed locally renders hairline‑thin in PowerPoint/LibreOffice ("washed‑out" text). Install Inter **static** weights (Regular/Medium/SemiBold/Bold) to the user font dir. Google Slides resolves Inter weights natively regardless.

---

## 3. Logos & assets

Location: `cybele_deckgen/brand_assets/`.

**Usage rule:** default is the **branded (blue)** variant. Use the **white** variant only when background contrast requires it (dark navy / saturated / blue photography).

| File | Variant | Native size (AR) | Use |
|---|---|---|---|
| `cybele_logo.png` | Cybele blue | 700×260 (2.69:1) | **Default** |
| `cybele_logo_white.png` | White text + colored flag | 700×260 | On dark backgrounds |
| `thinfinity_logo.png` | Thinfinity blue | 900×240 (3.75:1) | **Default** |
| `thinfinity_logo_white_real.png` | True white | 900×240 | On dark/saturated backgrounds |
| `cybele_logo_white.png` *(old)* / `thinfinity_logo_white.png` *(old)* | — | — | **DEPRECATED** (were actually blue) |
| Oracle Cloud lockup | `Downloads/oracle cloud.png` (stacked ORACLE/CLOUD, red, 3.29:1) | — | Co‑brand with Oracle |
| Oracle wordmark | `Downloads/Oracle_logo (2) 1.png` (red) | 5484×709 | — |

**Logo proportions (hard rule):** never distort — always preserve native aspect ratio. When co‑branding **Thinfinity + Oracle Cloud + Cybele** on one surface, keep the reference proportions: the Thinfinity + Oracle lockup at **equal height**, Cybele **larger**.

Icons: `cybele_deckgen/icons_png/` (200×200, dark + `_white`), SVG sources in `cybele_deckgen/icons/`. Cybfont (custom icon font) is **not** installed locally → use PNG/SVG icons as substitute.

---

## 4. Global visual rules

- **Flat solid fills** — no gradients.
- **No shadows** — strip `effectLst`/`outerShdw`/`innerShdw` everywhere (incl. theme XML for PPTX).
- **Borderless containers** — content cards/boxes have flat fill, **no stroke**; differentiate by fill, not borders. (Diagram pills/zones are the exception — their stroke is the skill's vocabulary.)
- **Low contrast** between containers and their background.
- **No italics; no Thin weight.**
- **Logos** keep aspect ratio.

---

## 5. Brand sources (Figma)

| Source | File key |
|---|---|
| Cybele Brandbook | `y7mHflD4ukCFDo6YsPzIf4` |
| Cybele Design System (colors/type/icons/logos/grid) | `x0HMD1pXkcYdFM7NSaBvb4` |
| Canonical diagram atoms / 131‑icon library | `8RBfhSYgaCuo4uM82JqAHL` · `W3Pnm739iwmVdo3hSaBNQe` |

**MCP:** `claude.ai Figma` (read) · `figma-remote-mcp` (read + write, `generate_figma_design`). Both authenticated for nceraso@cybelesoft.com.
