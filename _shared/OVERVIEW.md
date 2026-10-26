# Project Overview & Timeline

AI‑assisted branded document/design generation for Cybele Software. Cross‑cutting context lives here; task‑specific rules and pipelines live in each task folder.

## Tasks

| Task | Folder | Output | Skill(s) |
|---|---|---|---|
| Presentations | [`presentations/`](../presentations/PROGRESS.md) | `.pptx` (Google Slides) | thinfinity‑architecture (diagrams), impeccable |
| Documents (whitepapers) | [`documents/`](../documents/PROGRESS.md) | Branded multi‑page PDF | — |
| Blog | [`blog/`](../blog/PROGRESS.md) | Native SVG covers + section illustrations | cybele‑blog‑visuals, impeccable |
| Architecture | [`architecture/`](../architecture/PROGRESS.md) | Native Figma‑safe SVG diagrams | thinfinity‑architecture |

Shared: [`BRAND.md`](BRAND.md) · [`SKILLS.md`](SKILLS.md).

## Environment / infrastructure

- **MCP:** `claude.ai Figma` (read) · `figma-remote-mcp` (read+write `generate_figma_design`).
- **Python:** use **3.13** (`%LOCALAPPDATA%\Programs\Python\Python313\python.exe`). ⚠ The default `C:\Python314` is broken (missing stdlib `encodings`). Key libs: `python‑pptx`, `PyMuPDF (fitz)`, `Pillow`, `Playwright`, `pywin32` (PowerPoint COM).
- **Node:** `pptxgenjs` (faithful presentation path).
- **Fonts:** install Inter **static** weights locally (variable‑only renders thin) — see `BRAND.md §2`.
- **Pipelines and brand assets:** `web-app/deckgen/` (in this repo; setup in its README). Live skills: `~/.claude/skills/` is only a mirror of `skills/`.

## Timeline (master log)

| Date | Milestone |
|---|---|
| 2026‑03‑20 | Brand rules + project docs initialized. |
| 2026‑03‑25 | PPTX brand‑a‑source: nuclear shadow removal (through theme XML), typography enforcement, `noAutofit` title‑size fix. |
| 2026‑03‑26/27 | Whitepaper PDF pipeline (DOCX→HTML→PDF); dynamic cover‑title; Figma WP upload; brandbook type extracted; CISO PPTX shipped; first blog SVG illustrations. |
| 2026‑04‑17 | Blog cover visual system reverse‑engineered (21 covers): 6 archetypes, named tokens, generator‑only. |
| 2026‑05‑22 | Thinfinity Architecture Diagram **skill** authored (pill system, 131 icons, 7 calibration diagrams). Handoff v1. |
| 2026‑05‑27 | Arch skill product‑knowledge layer (capability→topology, invariants, recipes). Handoff v2. |
| 2026‑06‑02 | PPTX **from‑scratch editorial** paradigm (`build_pptx.py`, palette 06/26 adopted as canonical). Closing byte‑for‑byte + theme‑chain transplant. |
| 2026‑06‑08 | Arch skill: edge centering, convergence/bifurcation, in‑SVG reference footer, pre‑render distance check. New diagrams + recipes R8–R11. Blog + covers unified under `cybele-blog-visuals`. |
| 2026‑06‑10 | **Faithful brand‑a‑source PPTX path** (Node/pptxgenjs) — *Enterprise VDI on OCI · Discovery Demo (ESP)*: verbatim 39‑pg PDF→40 slides, 12 native diagrams from the arch‑skill construction rules + x/y centering, Inter static‑font fix, ⅓/⅓/⅓ background modes, borderless low‑contrast containers, co‑brand cover (logo proportions preserved), animated‑GIF closing. |
| 2026‑06‑10 | **Repo restructured** into per‑task folders (this layout) with shared brand + vendored skills. |

## Next steps

- Generalize the from‑scratch PPTX generator and `brand_config.json` (one source of truth for the 06/26 palette).
- Whitepaper: TOC page + pagination improvements.
- Validate the arch‑skill 🟡 product inferences; generate diagrams from conceptual prompts.
- Team web app for shared access.

> Full master progress log: [`_archive/Progress-06-10-2026.md`](_archive/Progress-06-10-2026.md).
