# Documents (Whitepapers — PDF)

Converts a DOCX of long‑form content into a branded multi‑page PDF. Stable since 2026‑03‑27, reusable across documents. Brand basics → [`_shared/BRAND.md`](../_shared/BRAND.md).

## Task rules

- **Cover:** navy gradient bg, category badge/pill (`#558BEE`), white title (Inter SemiBold), white subtitle, **Thinfinity + Cybele** logos at bottom. Cover title auto‑extracted from the DOCX (`Title`/`Heading1` → first non‑empty paragraph → filename fallback).
- **Interior:** white bg; H2 titles in brand blue; body Inter Regular; circled icons for feature lists; large blue numbers for "Key Takeaways"; tables with blue headers; blue accent ribbon (6 px) at bottom; page number top‑right.
- **Content transforms:** labeled items (blue title + description); bullet lists with separators; callout boxes (`#EEF4FD` bg + blue border) for "Key Takeaway/Summary/Implication"; pro/con check items — green `#3DCCA1` check / red `#E04040` cross (circle‑light SVG, outline only).
- **Back cover:** CTA card (blue gradient + white Thinfinity logo, "Start today"/"Book a call"), contact (address/phone/email with line‑art icons), navy footer with copyright + Cybele logo.
- **Typography:** brandbook text styles (Inter SemiBold titles, Inter Regular body) scaled 0.55× to the 795 px page width.
- **Pagination is dynamic** — driven by the source DOCX, not a constant.
- **Language:** preserve the source language verbatim; closing/CTA copy follows the source.

## Pipeline — `cybele_deckgen/whitepaper/`

Single command:
```bash
python whitepaper/build_whitepaper.py <input.docx> [output.pdf]
```

Four stages:
1. `generate_wp_pages.py` — DOCX → paginated HTML pages (795×1125 px, matching the Figma reference frame).
2. `redesign_wp.py` — Figma‑reference CSS + the content transforms above.
3. `generate_cover_closing.py` — cover + closing/back‑cover HTML (dynamic cover title via `WP_COVER_TITLE`).
4. `generate_pdf.py` — render to PDF (Playwright/Chromium) + merge (PyMuPDF).

**Figma upload (optional):** the same HTML pages upload to a Figma frame via `figmaselector=#capture-target` (constrains capture to the 795×1125 frame).

## Deliverables
- "AWS Virtual Desktops vs Thinfinity VDI on OCI" — 38–45 pp.
- "Delivering Your Software as SaaS Using Thinfinity" (from "Moving your business to SaaS").

## Next
- Add a TOC page; reduce whitespace on sparse pages; avoid cutting content blocks across pages.

## Whitepaper reference designs (Figma)
Transforming Digital Workspaces `3nDzupbog4IeureY5DZxyT` · AWS vs Thinfinity `3a6xHucGqzJ031REc3pMRO` · Deployment Options `RHnnX0bN67RvsvpeLxpltE` · Zero Trust + PAM `nrEht2faLJKl4aOUsFr7ah` · POS Remote Access `m2QQD3VhsBzHzN4LKVD7Sq` · ROI Comparison `lTv8KdbEAkS2pJFJmp6QeU` · GPU `neZepbihR0yvjmQ8xp9Mwf`.
