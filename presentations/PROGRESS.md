# Presentations (PPTX)

Editable `.pptx` decks for Google Slides. Brand basics (palette 06/26, Inter, logos, flat/no‑shadow) → [`_shared/BRAND.md`](../_shared/BRAND.md). Skills: **thinfinity‑architecture** (diagram layer), **impeccable** (design polish).

## Task rules

- **Dimensions:** native **13.333 × 7.5"** (from‑scratch / faithful paths) or 10 × 5.625" (legacy brand‑a‑source). 16:9.
- **Typography:** Inter SemiBold titles, Inter/Inter Medium body. Install Inter **static** weights locally or body renders thin (see BRAND §2). Explicit runs only (`run.font.*`), never `p.text=` then set font.
- **Containers:** borderless, flat fill; **low contrast** vs background; **no vibrant `#0F7FE0` fills** — accent fill = `#DCE8F8` (light) / `#1C3E63` (dark). `#0A74D6` only for **table header rows**. Vibrant blue only for details (title text, bullets, pill strokes).
- **Background modes:** split content slides ≈ **⅓ light `#EEF4FB` · ⅓ white `#FFFFFF` · ⅓ dark navy**, dispersed. Hard rules override the split: diagram slides are **always white**; **no dark slide adjacent to a section separator** (except the closing); cover / dividers / Q&A / closing are dark by design and excluded from the count.
- **Cover:** solid navy; outlined eyebrow badge; bold hero title; muted subtitle; bottom divider (red tint); co‑brand **Thinfinity + Oracle Cloud** lockup bottom‑left + **Cybele** bottom‑right. Logo aspect ratios preserved; lockup equal height, Cybele larger (BRAND §3).
- **Closing:** always the canonical `assets/cierre.pptx` slide, **XML‑swapped** as the last slide (never reconstructed in code). Keep the **animated GIF** when motion is wanted (≈11 MB) — or substitute a static PNG for a light deck.
- **Footer:** content slides only (not on cover/dividers/Q&A/closing). Alludes to the **document title + "Thinfinity + OCI"** binomial (else "Cybele Software") + page number; ≥10 px safe margin — content never invades it.
- **Diagrams:** native editable shapes that look like the Architecture diagram task's output. The full rules (updated 2026-09-28 from Nick's review of a deck task) are in [`web-app/data/progress.md`](../web-app/data/progress.md) › PPTX Generation Pipeline › "Architecture diagrams in a deck"; the reference builder is [`reference_builder/`](reference_builder/).
- **Language:** preserve the source document's language verbatim; don't translate or rewrite copy (closing text follows the source language).

## Pipelines (3 paradigms, chosen by source)

| Source | Path | Tool | Where |
|---|---|---|---|
| **Text** (DOCX/MD/Docs) | From‑scratch **editorial** generator (authors copy) | python‑pptx | `cybele_deckgen/pptx_work/build_pptx.py` |
| **Rendered artifact**, faithful 1:1 + native diagrams | **Verbatim** transcription + native diagrams | Node `pptxgenjs` | `cybele_deckgen/enterprise_vdi_oci_esp/` |

Common: closing via `cierre.pptx` XML swap; nuclear shadow removal; Inter‑only typography; slide count is dynamic per source.

### Faithful path build chain (`enterprise_vdi_oci_esp/`)
`node build_deck.js` → `python swap_closing_slide.py` → `python render_for_critique.py` (Python 3.13). Render/verify = **PowerPoint COM → PDF → PyMuPDF JPGs** + `slides_preview.html`. Diagram icons via `render_diagram_icons.py`.

## Deliverables

- *VDI & VDA para Universidades* — from‑scratch editorial, 27 slides.
- *CISO Risk Lens: Thinfinity vs Citrix* — brand‑a‑source.
- *Enterprise VDI on OCI · Discovery Demo (ESP)* — faithful 1:1, 40 slides, native diagrams (`enterprise_vdi_oci_esp/output/`).
