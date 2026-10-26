# Blog Visuals (Covers + Section Illustrations)

Both blog deliverables — the cover image and the in-article section illustrations — are produced in
one pass by the Claude skill **`cybele-blog-visuals`** (`skills/cybele-blog-visuals/`).

## Where the rules live

One rule, one file. To change how a visual looks, edit the spec that owns it:

| Subject | File |
|---|---|
| Covers: archetypes A1–A6, colour families and tokens, gradients, heroes, satellites, typography, variance, editorial rules | `skills/cybele-blog-visuals/BLOG_COVER_RULES.md` |
| Section illustrations: layout patterns, light/dark alternation, accents, typography, cards, connectors, icons | `skills/cybele-blog-visuals/SECTION_RULES.md` |
| Brand tokens both share | `skills/cybele-blog-visuals/BRAND_DESIGN_RULES.md` |
| The process: what to read, the phases, how many visuals, what to deliver | `skills/cybele-blog-visuals/SKILL.md` |

The skill's `HANDOFF.md`, `RECONCILIATION.md` and `PROGRESS.md` are journals — history, not rules.

This file used to be a fourth, summarised copy of the rules above. It drifted, as copies do, so it is
a map now. **Do not re-add design values here.**

## How many visuals per article

Chosen per task in the console launcher, stored in `jobs/<id>/job.json` → `options`:
`coverVariants` (1 by default, `0` = no cover at all) and `sectionImages` (empty = auto, one per
illustrable section; `0` = none).

## Pending

`Blog-Visuals-Style-Update-2026-06.md`, in this folder, is an amendment that reduces the colour
palette for both deliverables. It is **not applied**: the document declares itself partial ("faltan
variables por construir"), and applying it changes every future image. Decide, then apply it to the
two specs above — not here.
