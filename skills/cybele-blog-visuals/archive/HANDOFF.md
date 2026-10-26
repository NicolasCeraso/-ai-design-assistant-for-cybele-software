# HANDOFF — Cybele Blog Cover Generation System

> ⚠️ **Journal, not a specification.** This file records how the system was built and why.
> The design rules live in `BLOG_COVER_RULES.md` (covers) and `BRAND_DESIGN_RULES.md` (brand
> tokens); the counts of covers and section illustrations live in `SKILL.md` → INVOCATION
> MODES. Where this file disagrees with those, they win. Never use it as a stand-in for a
> rule file you could not open.

> **What this document is:** the complete ruleset needed to generate on-brand Cybele blog covers from any article. Hand it to a new Claude session (or package it as a Skill) and that session should be able to take an article and return the requested cover variants following this system — without re-doing analysis.

> **Reconciled with a parallel session's output. Final decisions live in `RECONCILIATION.md` (read both).**

> **How many covers is NOT decided here.** This document was written when 6 variants were the only
> mode, so "6" appears throughout. The count always comes from the request (`SKILL.md` → INVOCATION
> MODES; the console sends `coverVariants`, often 1, and **0 means no cover at all**). Read every "6
> variants" below as "the requested number of variants": this is the how, not the how many.

---

## 1 · Mission

Given a **blog article** (text, markdown, or URL), produce the **requested number of cover variants** (6 when nothing is said) that:

- All express the **same core concept** (not one angle per variant)
- Use **different archetypes / gradient recipes / hero primitives** from the Cybele visual system
- Render at **1920 × 1080 px (16:9)** as native SVG
- Show up in a **single HTML preview** stacked vertically for comparison
- Deliver the approved variant as **Figma-safe SVG** on request

---

## 2 · Canonical workflow

Every invocation follows this sequence:

1. **Read the article.** Distill its core concept into one sentence.
2. **Pick one kit per variant.** Each kit = `{archetype, gradient_recipe, hero, satellites}`. Vary all four across the 6 variants.
3. **Generate 6 SVGs** at 1920 × 1080.
4. **Build a single HTML preview** — all 6 covers stacked vertically, each labeled with its kit metadata (archetype / gradient / hero).
5. **Show preview in browser.** Wait for user to pick one (or request tweaks).
6. **Export the chosen SVG** as Figma-safe native SVG.

Do NOT:
- Generate 6 covers, each attacking a different section of the article
- Put the article title as text on the cover (title lives in CMS)
- Skip the HTML preview step
- Use photographic or 3D renders

---

## 3 · Design tokens

### 3.1 Colors

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

### 3.2 Gradient recipes

| Recipe | Stops | Use |
|---|---|---|
| `cyan-to-blue` | `cyan` → `blue-royal` | Default positive cover background |
| `violet-to-blue` | `violet` → `blue-deep` | Product-hero covers |
| `teal-to-navy` | `teal` → `blue-deep` | Compliance / reliability covers |
| `red-dramatic` | radial `#b52323` → `danger-deep` → `#3a0606` | Editorial "problem" covers ONLY |
| `monitor-body` | `blue-deep` → `ink` | Device frames |
| `halo` | radial `white` 0.5 → transparent | Always behind focal element |

Background gradient direction: diagonal (top-left → bottom-right) for linear, radial for A6 covers.

### 3.3 Typography

- Font stack: `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif`
- Weights in use: 500 (body), 600 (emphasis), 700 (titles), 800 (big numerals)
- Letter-spacing: kickers/labels use `1.5–3 px` uppercase
- Titles inside chips — rounded-rect with fill, **3–6 words maximum**
- Covers with NO text at all are common and correct

---

## 4 · Archetypes (A1–A6)

Every cover belongs to exactly one archetype.

### A1 · Hub-and-spokes
**When:** concepts that integrate multiple components (platform, orchestration, unified access)
**Anatomy:** diagonal gradient bg + horizon curve + radial halo behind focal + central hero + 4–6 satellite circles (white fill, icon inside) + dotted curved connectors

### A2 · Duality
**When:** two partner sides of the same concept (agent ↔ cloud, input ↔ output, physical ↔ virtual)
**Anatomy:** unified background (not a split), two focal groups left and right, dotted session arc connecting them, small labels under each half, top chip naming the relationship
**Pitfall:** don't make it adversarial (red vs green). For before/after with pain framing, use A6 dark.

### A3 · Hero + halo
**When:** general-purpose hero image, product portraiture, "subject speaks for itself"
**Anatomy:** violet-to-blue or cyan-to-blue gradient + big halo + cloud drift behind focal + single large hero (monitor, shield, cloud, factory, etc.) + optional subtle silhouettes at horizon

### A4 · Stack / ecosystem
**When:** platform / integration / "X + Y + Z" stories
**Anatomy:** light soft background (paper → soft violet) + big diffuse cloud behind + 3 circular cards in a row (logos or category icons inside) + dashed connectors between cards + top chip naming the stack

### A5 · UI mockup — **two distinct flavors**
**When:** product-direct stories — "what it looks like in practice"
**Anatomy:** dark navy background + faint grid + big halo + main card (rounded, light gradient) with mock OS-style top bar, nav, content panels + 1–2 floating notification cards in corners

- **Agent console flavor:** voice + chat + customer 360 view (the product in use)
- **Admin / Cloud Manager flavor:** metrics on pools, regions, auto-scale (platform management)

Pick flavor deliberately — they serve different narratives.

### A6 · Editorial / poster — **two distinct flavors**
**When:** saturated, cinematic, emotionally-charged composition

- **Dark editorial** (red radial bg, alarm icons, torn-paper props, coins): for "problem" covers ONLY
- **Poster editorial** (violet-blue radial, agent bust with headset, channel icons arcing as halo, cloud above): for aspirational / product-hero covers

**Anatomy (poster flavor):** radial violet-to-navy + sparkles + radial light rays at low opacity + cloud above + halo behind figure + hero bust (head + shoulders + headset, flat vector) + constellation of channel icons arced above head + small kicker at top
**Pitfall:** don't default to dark/red for every "big idea" cover — it communicates *pain*, not *power*.

---

## 5 · Hero primitive library

Heroes are the central visual object. Pick one per cover.

| Primitive | Semantics | Notes |
|---|---|---|
| **Shield** | Security, Zero Trust, compliance | White/light body, dark navy top band, subtle inner gradient |
| **Cloud** | Cloud platform, SaaS, migration | Soft gradient fill (white → lavender/blue); can contain keyhole/gear/logo inside |
| **Padlock** | Access control, identity | Blue arc + white body + purple/blue keyhole |
| **Monitor / Desktop** | VDI, UI, dashboard | Dark frame, gradient screen, window UI mockup |
| **Laptop** | Endpoint, user device | Monitor with base |
| **Server rack** | Infrastructure, on-prem | 3–4 stacked rectangles with small circles/bars |
| **Factory silhouette** | OT, industrial, manufacturing | Dark purple/navy flat silhouette, chimney optional |
| **Robotic arm** | Automation, production | Segmented arm in warm accent (yellow/mustard) |
| **Graduation cap** | Education, campus | Dark flat silhouette with tassel |
| **Gears** | Process, automation | Outline or solid flat, often background |
| **Coins / dollar** | Cost, savings, ROI | Gold `#E6C74C`, stacked or scattered |
| **Agent with headset** | Contact center, CX | Flat bust: head + shoulders + headset + mic boom |
| **Thinfinity ring** | Product mark | Stylized circular logo (see `brand_assets/thinfinity_logo.svg` for canonical) |

Compound heroes (two primitives fused) are common: cloud + padlock, shield + credit card, monitor + GPU chip, etc.

---

## 6 · Satellite vocabulary

Elements that orbit / support the hero:

| Element | Purpose | Spec |
|---|---|---|
| **Circle badges** | Actors, states, services | 60–100 px circle, colored fill, white icon inside at 60% scale |
| **Connection lines** | Relationships | White (60–90% opacity), 4–6 px stroke, curved or straight, optional dashed |
| **Glow halo** | Separate hero from bg | Soft radial, white/accent at 40–70% opacity, large and diffuse |
| **Concentric rings** | Radar, emphasis | 3–5 thin white circles around central point, opacity fading outward |
| **Label pills** | Annotations | Rounded-rect (fully capsule), `ink` bg, `white` text, Inter SemiBold 14–18 px |
| **Logo chips** | Brand references | White circular/pill container, logo at 60% of chip |
| **Sparkles** | A6 poster only | Small white asterisks/dots scattered in bg |

### Badge color semantics

| Color | Token | Meaning |
|---|---|---|
| Green | `teal` | Approved, success, positive |
| Red | `danger` | Denied, blocked, problem |
| Orange/Yellow | `warning` | Caution, pending |
| Blue | `blue-royal` | Neutral actor (user, device) |
| Violet | `violet` | Data, configuration, policy |

### Icon glyph vocabulary (semantic set)

Canonical glyphs — reuse, don't reinvent:

Shield · Cloud · Factory · Office building · Server rack · Monitor+UI · Robot arm · Thinfinity spiral · Phone handset · Speech bubble · Envelope · Three-nodes (social) · Camera block · Two-figure group (CRM) · Green check circle · Red X circle · Red triangle + "!" (warning) · Dotted curve (connection) · Stopwatch (speed) · Receipt (cost)

---

## 7 · SVG authoring rules (Figma compatibility)

### Canvas
- `viewBox="0 0 1920 1080"` in every SVG
- User-space integer units (no `%`, no `em`)
- Minimum padding 60 px from any edge

### Allowed elements
```
<rect>, <circle>, <ellipse>, <path>, <line>, <polygon>, <polyline>,
<g>, <svg>, <linearGradient>, <radialGradient>, <defs>, <filter>,
<text>, <tspan>
```

### Forbidden elements (Figma drops/ignores these)
```
<foreignObject>           ← Figma ignores
<image> / external <use>  ← Figma drops on import
base64 data URIs          ← never
external URL references   ← never
```

### Text
- Always native `<text>` (never HTML)
- Always escape `&` → `&amp;`, `<` → `&lt;` in text content (silent parse failure otherwise)
- Font family on root svg or each `<text>`

### IDs and defs
- Every gradient/filter lives inside the SVG's own `<defs>` block
- Prefix IDs per cover: `c1-bg`, `c2-halo`, etc. — collisions silently break fills when multiple SVGs coexist in HTML
- Use `gradientUnits="userSpaceOnUse"` with explicit coords for backgrounds → direction stays predictable when scaled

### Other
- No external stylesheets, no `<style>` blocks
- No CSS classes — inline attributes only
- Avoid matrix transforms; prefer `translate() rotate() scale()`
- Group related shapes under a single `<g transform="...">` so they stay movable in Figma

---

## 8 · Editorial rules (learned through iteration)

1. **Variants = same idea, different composition.** Six covers of one article = six ways to draw the same core message. Never six different angles/sections.
2. **Don't default to red for "big".** `red-dramatic` / A6 dark = financial or operational pain. For aspirational hero covers, use A6 poster flavor (violet-blue radial).
3. **Use canonical glyphs.** If the concept has a glyph in §6, use it. Inventing "voice v2" icons per cover breaks family resemblance.
4. **Titles in chips, not floating text.** Rounded-rect backgrounds give presence at web-cover sizes.
5. **One focal per cover.** Halo tells the viewer where to look. Two focals at equal weight = a diptych, which is A2 Duality's job.
6. **Products over logos.** OCI / AWS / Azure referenced as generic cloud glyph + text label. Never pixel-accurate reproductions.
7. **Distinguish A5 flavors.** Agent console (product in use) and Admin dashboard (management) serve different narratives — don't conflate.

---

## 9 · Decision matrix — article topic → visual kit

Quick lookup for choosing archetype + gradient per topic:

| Article topic | Gradient | Archetype | Hero | Satellites |
|---|---|---|---|---|
| Security / Zero Trust / ZTNA | `teal-to-navy` or `cyan-to-blue` | A3 | Shield (keyhole or check) | Circuit lines, check/X |
| Cloud migration | `cyan-to-blue` or `violet-to-blue` | A4 or A3 | Cloud with logo/padlock | Provider logo chips |
| OT / IT / Manufacturing | `teal-to-navy` | A3 or A2 | Shield bridging factory + building | Factory silhouette, gears |
| VDI / Virtual desktop | `cyan-to-blue` or `monitor-body` | A3 or A5 | Monitor + laptop | App tiles, cloud, UIs |
| Contact center / BPO | `violet-to-blue` | A1 or A6 poster | Agent bust with headset | Channel badges, cloud |
| Education / campus | `violet-to-blue` or pastel | A3 or A4 | Graduation cap + cloud | ID cards, books |
| Cost / ROI / savings | `teal-to-navy` + teal accent | A2 | Coins + bar chart | Dollar pills, progress bars |
| Pain point / lock-in | `red-dramatic` (rare) | A6 dark | Receipt, chain | Coins, red accents |
| Automation / robotics | `teal-to-navy` | A3 | Robotic arm + conveyor | Gears, warning badges |
| Monitoring / analytics | `cyan-to-blue` | A5 admin | Browser/monitor with chart | Icon badges, KPI numbers |
| GPU / performance | `cyan-to-blue` or `monitor-body` | A3 | GPU chip + monitor | Graph widgets, gauges |
| Transformation / modernization | `violet-to-blue` | A2 or A3 | Citrix → Thinfinity flow | Check nodes, factory |
| Aspirational product hero | `violet-to-blue` radial | A6 poster | Agent bust + channel halo | Sparkles, cloud above |

---

## 10 · Producing several variants — how to vary

When the article is chosen, build 6 distinct kits. Good variance strategy:

- **Use at least 4 different archetypes** across the 6
- **Use at least 3 different gradient recipes**
- **Each variant has a different hero** (or compound hero)
- **Keep all 6 expressing the same core concept** — verify the brief before diverging

Example — article "Telecom Contact Centers at Scale":

| # | Metaphor | Archetype | Gradient | Hero |
|---|---|---|---|---|
| 1 | Thinfinity hub + agents orbiting | A1 | cyan-to-blue | Thinfinity ring + agent badges |
| 2 | Cloud delivering desktops to agents | A3 | monitor-body | Cloud with monitor inside |
| 3 | Unified agent with channels | A3 | paper → violet-light | Agent bust + channel badges |
| 4 | Contact center at scale (mgmt view) | A5 admin | violet-to-blue | Cloud Manager dashboard |
| 5 | Physical → Virtual | A2 | teal-to-navy | Cubicles ↔ VDI cloud |
| 6 | Any scale (1K/5K/10K) | A4 | cyan-to-blue | Three sized circles tied to OCI |

---

## 11 · Environment / dependencies

To produce covers you need:

- **Python 3.12+** (tested on 3.14)
- **Playwright** (Chromium) for SVG → PNG render inside the HTML preview
- **PyMuPDF** only for analyzing PDF references (not runtime)
- **Pillow** for optional color analysis
- **lxml** for SVG validation during development

No external fonts bundled — rely on system Inter + fallback.

### Build pipeline pattern

```python
# 1. Build SVG as string (parameterized)
svg_string = build_cover(kit)

# 2. Write to file with .svg extension
path = output_dir / f"cover_{slug}.svg"
path.write_text(svg_string, encoding="utf-8")

# 3. Render PNG via Playwright for HTML preview
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.goto(f"file:///{path.as_posix()}")
    page.screenshot(path=str(path.with_suffix('.png')),
                    clip={'x': 0, 'y': 0, 'width': 1920, 'height': 1080})

# 4. Emit preview.html with all N covers stacked
```

---

## 12 · Figma export

The SVGs produced by this system are already Figma-safe (native primitives only, no foreignObject, no base64). To hand one off to Figma:

- Save the approved SVG
- Open Figma, drag the file into a frame, or use `figma-remote-mcp` MCP with `generate_figma_design` (see `../PROGRESS.md` for the push pattern)

No post-processing needed.

---

## 13 · Reference library

The system was reverse-engineered from 21 production blog covers extracted from `sample portadas.pdf` (Cybele's past blog history). PNG copies live in `reference/cover_01.png … cover_21.png`.

**Use the reference library when:**
- Unsure which archetype a topic should map to — scan the library for similar topics
- Deciding on satellite density or glyph choice
- Validating that a new cover "feels like Cybele"

---

## 14 · Gotchas that save time

- **Always escape `&` in `<text>`** — silent SVG failure otherwise
- **Playwright on Windows Python 3.14** — `print()` with emojis fails (`cp1252`). Use `[ok]` / `[err]` markers
- **Playwright viewport must match canvas** — 1920×1080 + `clip` param to avoid scrollbar rendering
- **Icon path library is 100×100 viewbox** — always wrap in `<g transform="translate(x,y) scale(s)">` when placing
- **Thinfinity ring canonical source** — `brand_assets/thinfinity_logo.svg`. The stylized generator helper is a simplification for speed
- **IDs in `<defs>`** — prefix per SVG (`c1-`, `c2-`). Shared IDs across multiple SVGs in one HTML break fills silently
- **Don't introduce italic or Thin fonts** anywhere (Cybele brand rule, enforced at generator level)

---

## 15 · Files that ground this system

Read these before generating anything:

| Path | Purpose |
|---|---|
| `./HANDOFF.md` | This document |
| `./RECONCILIATION.md` | Final decisions across two sessions |
| `./BLOG_COVER_RULES.md` | The cover specification (archetypes A1–A6, examples, anti-patterns) |
| `./reference_generator.py` | Reference generator — use for helpers (not as a copy-paste template). The older `build_telecom_cx_covers.py` lives outside this repo and is not required |
| `./reference/cover_01.png … cover_21.png` | 21 production covers for visual calibration |
| `./BRAND_DESIGN_RULES.md` | Cybele corporate brand rules (colors, fonts, logos) |
| `thinfinity_logo.svg` in the brand asset set (see BRAND_DESIGN_RULES.md §8) | Canonical Thinfinity mark |

---

## 16 · When you receive a new article

1. Read it fully.
2. Identify the **one-sentence core concept**.
3. Consult §9 (topic → kit matrix) for defaults.
4. Pick 6 kits with variance per §10.
5. Generate 6 SVGs at 1920 × 1080 following §7 rules.
6. Build the HTML preview per §2, step 4.
7. Open preview in browser, show to user.
8. Wait for approval. Export chosen SVG for Figma.

If the article doesn't fit any matrix row cleanly → build the kit from first principles using §3–§6 and prefer A3 (safest default) when in doubt.

---

## 17 · Open decisions (ask the user when relevant)

- **Thinfinity mark fidelity** — use canonical SVG at `brand_assets/thinfinity_logo.svg` or stylized simplified version? Default to canonical when generating production assets.
- **Dark-mode variants** — none of the 21 references are explicit dark-mode. If a site redesign calls for them, this system needs a new archetype flavor.
- **Third-party brand fidelity** — Oracle / AWS / Azure / Citrix references stay generic (cloud glyph + text) unless user explicitly requests licensed logos.

---

*This document is self-sufficient for cover generation. To build a shareable repo or a Claude Skill from it, see §5 of `RECONCILIATION.md` for proposed structure.*
