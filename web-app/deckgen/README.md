# deckgen — document pipelines and brand assets

Only what the console's **pptx**, **wp** (whitepaper) and **linkedin-carousel** tasks need to
generate a new document. Nothing generated, nothing one-off. It used to live outside the repo on
one machine; since 2026-10-26 it is versioned here so a clone reproduces the same results.

Set up once, from `web-app/` (details in `../README.md`):

```powershell
.\setup.ps1     # .venv + libraries, Chromium, pptxgenjs, icon PNGs, Inter font
```

The console passes this folder to Claude as `deckgenDir` (`CYBELE_DECKGEN_DIR` overrides it). Every
script resolves its paths from its own location, so none needs to be run from a fixed place.

## What is here

| Path | Used by | Run |
|---|---|---|
| `whitepaper/` | **wp** — DOCX → paginated, branded PDF | `python whitepaper/build_whitepaper.py <in.docx> <abs/out.pdf>` |
| `brand_assets/` | Cybele/Thinfinity logos (SVG for the carousel, PNG for whitepaper and decks) and `thinfinity_icon_white.png` (closing-slide swap) | — |
| `brand_config.json`, `build_pptx.py` (cards take any icon of the library by name) | **pptx**, from-scratch editorial generator | `python quick_deck.py <in.docx> --output Deck.pptx` (also `generate_deck.py`, `text_to_content.py`, `example_content.json`) |
| `enterprise_vdi_oci_esp/` | **pptx**, faithful path (Node + pptxgenjs). The reference deck `build_deck.js` (40 slides), the closing-slide swap, the PowerPoint render/verify loop and the two icon renderers | `node build_deck.js` · `python swap_closing_slide.py` · `python render_for_critique.py` |
| `linkedin_carousel/build_svgs_v2.js` | **linkedin-carousel** reference generator (spec: `../pipelines/LINKEDIN_CAROUSEL_SPEC.md`) | `node build_svgs_v2.js [out-dir]` |

Also in the repo, outside this folder: the closing slide template `../../presentations/assets/cierre.pptx`,
the PPTX engine with architecture diagrams `../../presentations/reference_builder/`, the carousel
checker `../pipelines/verbatim_check.js` and the specs in `../pipelines/`.

## Not versioned (and why)

- **Generated, rebuilt by the setup above:** `icons_png/` and `enterprise_vdi_oci_esp/diagram_icons/`
  (PNG renders of the whole icon library, `../brand-icon-lib.js`, and of the architecture-skill icons), `node_modules/`, `output/`, `__pycache__/`, `_icon_cache/`.
- **Outputs and one-off history** left in the author's original folder: `blog_covers/` (322 MB of
  renders and per-article builds), `success_cases_vertical/`, `pdf_pages/`, `blog_illustrations/`,
  per-customer deck scripts (`build_healthcare_*`, `build_telecom_*`, `build_demo_call_*`, …),
  experiments and QA scratch. The blog rules that matter live in `../../skills/cybele-blog-visuals/`.
- **Retired:** the image-based deck mode (`slide_templates.py`) — it turned text into pixels.
- A second, shorter reference deck (`build_oci_internal_v2.js`, 21 slides) — `build_deck.js` is the complete one.
- Unused brand files (social-network icons, `arch_basic.svg`, the legacy blue "white" Thinfinity PNG).

## Requirements outside pip

- **Python 3.13** and **Node 18+** (install first), **Microsoft Edge** (icon rasterising in `presentations/reference_builder`).
- **Inter** font: installed by `../install-fonts.ps1` (run by `setup.ps1`), not bundled.
- **PPTX → PDF previews** (`../render_pdf.py`, `render_for_critique.py`): Microsoft PowerPoint if installed (reference
  renderer), otherwise **LibreOffice** headless — `setup.ps1` installs it when neither exists. LibreOffice is fine for
  review (checked on the 40-slide deck: fonts, tables, diagrams, closing slide). Without either, decks still build and
  only previews fail.
- **Editable-PPTX download** (`../export_doc.py`): writes the SVG-in-PPTX package itself with python-pptx and Chrome.
  **PowerPoint is not required.**

## Retired

- The python-pptx "brand-a-source" route and its 2-slide cover/closing template (obsolete; removed from the process 2026-10-26). Closing slides come from `cierre.pptx`.
