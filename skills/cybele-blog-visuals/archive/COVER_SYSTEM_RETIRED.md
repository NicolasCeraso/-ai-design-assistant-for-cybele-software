# Retired — the generative cover system (2026-03 → 2026-09)

> **Nothing here governs anything.** This file is not loaded by the skill and not read by the
> console's style editor. It described a system that **generated** covers as SVG: six colour
> families, archetypes A1–A6, a hero and satellite vocabulary, gradient recipes. It was derived from
> the covers in `covers-2026-03/`, which no longer resemble what Cybele publishes.
>
> It is kept so an old cover can be recognised, and so the palette work is recoverable. The live
> rules are `../BLOG_COVER_RULES.md`.

## Record — the retired generative system (2026-03 → 2026-09)

> **Reference only.** What follows described a system that **generated** covers as SVG: six colour
> families, archetypes A1–A6, a hero and satellite vocabulary, gradient recipes. It was derived from
> the 21 covers in `reference/`, which no longer resemble what Cybele publishes. Nothing here governs
> a cover any more, and no value in it is editable. It is kept so an old cover can be recognised, and
> so the palette work is not lost if any of it is wanted back.

### 1. Canvas & Format

| Attribute | Value |
|---|---|
| Aspect ratio | **16:9** (1.778) |
| Canvas size | **1920 × 1080 px** |
| SVG viewBox | `0 0 1920 1080` |
| Orientation | Landscape only |
| Safe area | Keep hero element within central 80% of canvas |
| Minimum padding | 60 px from any edge |

---

### 2. Six Color Families (Background Gradients)

> **Reduced palette (2026-06, revised 2026-09) — read this before picking a colour.** The blog visual
> system was cut back to the brand blues and violets: the free rainbow accents are gone, and so is the
> semantic-state system that briefly replaced them (removed by decision on 2026-09-04 — blog visuals
> no longer colour anything by "state"). For covers that means: build from the **brand blues and
> violets**, keep `red-dramatic` **only** for "problem" covers, and treat the families below as the
> composition vocabulary rather than a licence to introduce new hues. The full re-derivation of the
> families and gradient recipes is **pending a cover sample in the reduced palette** — until that
> exists, prefer the blue/violet families and say in `NOTES.md` when you had to reach for anything
> else.

Each cover uses a single color family as background gradient. Choose one that matches the **emotional tone** of the article.

### Family A — Blue (marine, trust, clarity)
Most common. Default for product/cloud/security neutral articles.

| Stop | Hex | Role |
|---|---|---|
| Light top | `#8BEDFF` → `#94EEFF` | Sky/cyan |
| Mid | `#2D8FDF` → `#4262C2` | Product blue |
| Deep bottom | `#001B81` → `#073F69` | Navy base |

**Example covers:** 01, 02, 04, 07, 17

### Family B — Navy (depth, security, serious)
For security, compliance, IT-heavy articles.

| Stop | Hex | Role |
|---|---|---|
| Mid | `#112C64` → `#1F3082` | Navy mid |
| Deep | `#060F24` → `#031A56` | Near-black navy |
| Accent | `#5A62F4` → `#57A0EB` | Bright blue highlight |

**Example covers:** 03, 08, 14, 18

### Family C — Purple / Violet (innovation, transformation)
For transformation, modernization, SaaS, migration articles.

| Stop | Hex | Role |
|---|---|---|
| Light | `#C36CE1` → `#CB88E6` | Light purple |
| Mid | `#9138B6` → `#A54FC7` | Magenta/violet |
| Deep | `#33188C` → `#400966` | Deep purple |
| Pink accent | `#841573` → `#8D1570` | Magenta end |

**Example covers:** 06, 11, 15, 19, 21

### Family D — Teal / Cyan (automation, industrial, ops)
For OT/IT, manufacturing, automation, pipeline articles.

| Stop | Hex | Role |
|---|---|---|
| Light | `#47D7C0` → `#01D3B8` | Bright teal |
| Mid | `#0085A0` → `#118982` | Teal mid |
| Deep | `#0F222B` → `#075F5E` | Dark teal/navy |

**Example covers:** 09, 10, 20

### Family E — Red (problem, warning, pain-point)
**Rare.** Use only for articles explicitly about a pain point, failure mode, or negative comparison (e.g., vendor lock-in, downtime cost).

| Stop | Hex | Role |
|---|---|---|
| Mid | `#C91A01` → `#B81F08` | Bright red |
| Deep | `#7E0F01` → `#750F00` | Burgundy |

**Example cover:** 05

### Family F — Soft Pastel (intro, overview, neutral)
For introductory, educational, or "gentle" articles (how-to, primer).

| Stop | Hex | Role |
|---|---|---|
| Light | `#C2D2F9` → `#DCE4F9` | Lavender-blue |
| Mid | `#92ADEC` → `#AABCEF` | Periwinkle |
| Shift | `#BEF1FF` → `#C4CBF8` | Cyan-to-purple fade |

**Example covers:** 12, 13

### Cover color tokens

| Token | Hex | Role |
|---|---|---|
| `blue-deep` | `#0f1e6e` | Primary brand, darkest blue |
| `blue-royal` | `#2b3eaa` | Primary brand, mid blue |
| `cyan` | `#4dd4c8` | Accent, bright cool |
| `teal` | `#3ac6a6` | Success / positive |
| `violet` | `#6a4cc8` | Accent, violet-blue |
| `violet-light` | `#a98cdb` | Accent, softer violet |
| `magenta` | `#b06fd9` | "Social" accent |
| `warning` | `#f2c14e` | Warning |
| `danger` | `#d64040` | Error / alarm |
| `danger-deep` | `#6b0f0f` | Editorial "problem" covers only |
| `ink` | `#0a1533` | Text on light, dark surfaces |
| `paper` | `#f3f5fb` | Light surface / background |
| `white` | `#ffffff` | Highlights, halos, icon badges |

> The families above describe the look; these tokens are the names the generator uses for the
> same palette. Change a colour in both places or they disagree.

---

### 3. Gradient Mechanics

- **Direction:** Mostly **diagonal** (top-left → bottom-right) or **vertical** (top → bottom). Horizontal gradients are rare.
- **Distribution:** Smooth 2–3 stops, no hard bands.
- **Lightness trend:** Usually **top lighter, bottom darker** (ground anchor). In cover_04/05/14/21 inverted (light-top) for atmospheric feel.
- **Never:** Harsh banding, radial gradients as background, noise/grain textures.

Example SVG pattern (Family A):
```svg
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"  stop-color="#2D8FDF"/>
    <stop offset="100%" stop-color="#001B81"/>
  </linearGradient>
</defs>
<rect width="1840" height="1084" fill="url(#bg)"/>
```

### Gradient recipes

| Recipe | Stops | Use |
|---|---|---|
| `cyan-to-blue` | `cyan` → `blue-royal` | Default positive |
| `violet-to-blue` | `violet` → `blue-deep` | Product-hero |
| `teal-to-navy` | `teal` → `blue-deep` | Compliance / reliability |
| `red-dramatic` | radial `#b52323` → `danger-deep` → `#3a0606` | A6 dark only |
| `monitor-body` | `blue-deep` → `ink` | Device frames |
| `halo` | radial `white` 0.5 → transparent | Always behind focal element |

---

### 4. Composition Archetypes (A1–A6)

Pick ONE per cover. Every reference cover falls into one of these six archetypes.

### A1 — Hub-and-spokes
Central focal object with satellite icons orbiting, connected by dotted curves.

- Use for: integrative concepts, platforms with multiple components
- Anatomy: diagonal gradient background + horizon curve + radial halo centered behind the focal + central hero + 4–6 satellite circles (white fill, icon inside) + dotted connectors
- **Example covers:** 15, 16

### A2 — Duality
Two complementary halves of the same concept, connected by a beam or arc.

- Use for: concepts with two partner sides (agent ↔ cloud, input ↔ output, physical ↔ virtual)
- Anatomy: unified background (not a hard split), two focal groups left and right, dotted session arc connecting them, small labels under each half, top chip naming the relationship
- **Pitfall:** don't make it adversarial (red vs green). For before/after with pain framing, use A6 dark flavor instead.
- **Example covers:** 01 (Virtual Desktop vs Virtual App), 09, 14, 18

### A3 — Hero + halo
One monumental subject floating in radiant space. Minimal supporting elements.

- Use for: general-purpose hero image, product portraiture, subject speaks for itself
- Anatomy: violet-to-blue or cyan-to-blue gradient + big halo + cloud drift behind focal + single large hero + optional subtle silhouettes at horizon
- **Example covers:** 02, 03, 07, 10, 11

### A4 — Stack / ecosystem
Three (or four) equal cards in a row, each representing a component of a composable system.

- Use for: platform / integration / "X + Y + Z" stories
- Anatomy: light soft background (paper to soft violet) + big diffuse cloud behind + 3 circular cards with logos or category icons + dashed connectors between cards + top chip naming the stack
- **Example covers:** 13 (Azure / Thinfinity+Oracle / AWS)

### A5 — UI mockup
A realistic-looking product panel floating on a dark background, with small notification cards around it.

- Use for: product-direct stories, "what it looks like in practice"
- Anatomy: dark navy background + faint grid + big halo + main card (rounded, light gradient) with mock OS-style top bar, nav, content panels + 1–2 floating notification cards in corners
- **Two flavors — pick deliberately:**
  - **Agent console flavor** — voice + chat + customer 360 view (product in use)
  - **Admin / Cloud Manager flavor** — metrics on pools, regions, auto-scale (platform mgmt)
- **Example covers:** 08 (Cloud Manager), 20 (Graph+Browser)

### A6 — Editorial / poster
A saturated, cinematic, emotionally-charged composition. Single figure or prop as hero. Dramatic lighting.

- **Two flavors — use deliberately:**
  - **Dark editorial** (deep red radial, alarm icons, torn-paper props, coins): for "problem" covers ONLY
  - **Poster editorial** (violet-blue radial, agent figure as hero, channel icons arcing as halo, cloud above): for aspirational / product-hero covers
- **Anatomy (poster flavor):** radial violet-to-navy background + sparkles + radial light rays at low opacity + cloud above + halo behind figure + hero bust (head + shoulders + headset, flat vector) + constellation of channel icons arced above head + small kicker text at top
- **Pitfall:** don't default to dark/red flavor for every "big idea" cover — it communicates *pain*, not *power*
- **Example covers:** 05 (dark — Citrix receipt), 19 (poster — cloud with apps)

---

### 5. Hero Object Vocabulary

When selecting a hero, use one of these semantic primitives. **Keep shapes flat with subtle gradient fills — not realistic 3D.**

| Symbol | Meaning | Color treatment |
|---|---|---|
| **Shield** | Security, Zero Trust, protection, compliance | White/light body, dark navy top band; subtle inner gradient |
| **Cloud** | Cloud platform, SaaS, cloud migration | Soft gradient fill (white → lavender or white → blue); keyhole/gear inside for compound meaning |
| **Padlock** | Access control, identity | Blue arc + white body + purple keyhole |
| **Monitor / Desktop** | Virtual desktop, UI, dashboard | Dark frame, gradient screen content, window UI mockup |
| **Laptop** | Endpoint, user device | Same as monitor but with base |
| **Server rack** | Infrastructure, on-premise | 3–4 stacked rectangles with small circles/bars |
| **Factory silhouette** | OT, industrial, manufacturing | Dark purple/navy flat silhouette, optional chimney |
| **Robotic arm** | Automation, production | Segmented arm in warm accent (yellow/mustard) |
| **Graduation cap** | Education, students, campus VDI | Dark flat silhouette with small tassel |
| **Gears** | Process, automation | Outline or solid flat, often in background |
| **Coins / dollar** | Cost, savings, ROI | Gold `#E6C74C`, stacked or scattered |
| **Agent with headset** | Contact centre, BPO, support | Flat bust silhouette, headset in accent colour |
| **Thinfinity ring** | Thinfinity itself as the subject | The three-blade mark, flat, on a halo |

### Compound heroes
Heroes often combine 2 primitives, e.g.:
- Cloud + padlock = secure cloud
- Shield + keyhole = Zero Trust
- Shield + ID card = identity protection
- Monitor + GPU chip = GPU virtual desktop

---

### 6. Satellite Element Vocabulary

Elements that orbit the hero. Used to convey context without text.

### Circular badge nodes
Small circles (60–100 px), colored fill, white icon inside. Used to mark actors, states, services.

| Color | Hex | Meaning |
|---|---|---|
| Green | `#3DCCA1` or `#22C55E` | Approved, allowed, success |
| Red | `#E04040` | Denied, blocked, problem |
| Orange | `#E67E22` or `#d97706` | Warning, limited, attention |
| Blue | `#0A74D6` or `#3B82F6` | Neutral actor (user, device) |
| Purple | `#7c3aed` or `#a78bfa` | Data, configuration, policy |

**Pattern:** `<circle fill="{color}"/>` + centered `<g>` with white icon at 60% of circle.

### Connection lines
Curved or straight paths connecting hero ↔ satellites.

- **Color:** White (`#FFFFFF`) at 60–90% opacity, or subtle accent tint
- **Stroke width:** 4–6 px (thin, not bold)
- **Dashed:** Occasionally, for "pending" / "potential" states
- **Arrows:** Optional, only when direction matters. Small solid triangle heads.

### Glow halos
Soft radial blur behind hero to separate it from background.

- White or brand accent at 40–70% opacity
- Large, diffuse — use SVG filter `<feGaussianBlur stdDeviation="40"/>` or layered radial gradient

### Concentric rings (radar)
Thin white circles around a central point, fading outward.

- 3–5 rings, 1–2 px stroke
- Opacity decreasing from center (e.g., 0.5, 0.3, 0.2, 0.1, 0.05)
- Used in covers 07, 16, 18

### Label pills
Small rounded rectangles with short text — used for annotations, never for titles.

- Background: `#0B1A3B` (navy) or `#1E293B` (slate)
- Text: white, Inter SemiBold, 14–18 px
- Padding: 10–14 px horizontal, 6–8 px vertical
- Corner radius: 20 px (fully rounded / capsule)

### Brand logo chips
White circular or pill container with the brand logo inside.

- Background: `#FFFFFF` with subtle shadow
- Padding: generous (logo occupies 60% of chip)
- Used for Thinfinity, Oracle Cloud, AWS, Azure, Citrix

---

### 7. Typography on Covers

**Most covers carry NO headline text.** The cover is purely visual; the article title lives in the CMS above/beside the image.

When text IS part of the illustration, rules:

| Element | Font | Weight | Size (at 1840 px) | Color |
|---|---|---|---|---|
| In-pill label ("OT", "RBI access") | Inter | SemiBold 600 | 24–32 px | White on `#0B1A3B` |
| Card headline inside illustration ("Citrix Receipt") | Inter | Bold 700 | 44–56 px | `#1E293B` on white card |
| Card body text | Inter | Regular 400 | 26–32 px | `#515151` |
| Node captions ("Campus VDI") | Inter | Regular 400 | 22–28 px | White on dark / dark on light |
| Acronym in shield ("IDMZ") | Inter | Bold 700 | 48–64 px | `#0A74D6` |

**Never:**
- Italics
- All-caps body text (titles in all-caps OK if short)
- Drop shadows on text
- Outlined (stroked-only) text

---

### 8. Style Fingerprint (the "Cybele look")

Rules that make a cover **feel Cybele** vs. generic tech illustration:

| Rule | Do | Don't |
|---|---|---|
| Fills | Flat colors with 1 gentle gradient per shape | Photorealistic rendering, plastic-3D |
| Outlines | Occasional thin white strokes for separation | Heavy black outlines, stroked-only shapes |
| Shadows | Subtle ground shadow under hero only | Hard drop shadows on every element |
| Glow | Soft diffuse halo behind hero | Hard-edged glow, neon rings |
| Corners | Rounded everywhere (pills, cards, tiles) | Sharp 90° corners on content |
| Icon style | Solid-fill flat icons inside colored circles | Line-art icons floating on bg |
| Perspective | Frontal view, slight depth via layering | True isometric, orthographic schematics |
| Motion cues | None or very subtle (trailing dots) | Motion blur, comic speed lines |
| Textures | None (smooth) | Grain, paper, halftone, gradient mesh |
| Logo handling | Inside white chip/circle | Floating raw on gradient |

---

### 9. SVG Construction Rules

### Allowed elements
```
<rect>, <circle>, <ellipse>, <path>, <line>, <polygon>, <polyline>,
<g>, <svg>, <linearGradient>, <radialGradient>, <defs>, <filter>,
<text>, <tspan>
```

### Forbidden
```
<foreignObject>          ← Figma drops it
<image> / <use href>     ← Embed paths instead
base64 data: URIs        ← Never
External URL references  ← Never
```

### Gradient naming convention
Use descriptive IDs: `bg-blue`, `hero-shield`, `halo-glow` — not `grad1`, `grad2`.

### Layering order (back to front)
1. Background gradient rect
2. Background decorative shapes (rings, blurred blobs)
3. Connection lines
4. Halo glow behind hero
5. Satellite elements (behind-hero ones)
6. Hero object
7. Satellite elements (in-front-of-hero ones)
8. Labels and pills (always top)

### Minimum padding
Keep elements at least **60 px** from any edge.

---

### 10. Semantic Mapping — Article Topic → Visual Kit

Use this matrix to pick the right combination fast. Gradient recipes defined in `RECONCILIATION.md` §2.3.

| Article topic | Gradient recipe | Archetype | Hero | Satellites |
|---|---|---|---|---|
| Security / Zero Trust / ZTNA | teal-to-navy or cyan-to-blue | A3 Hero + halo | Shield (with keyhole or checkmark) | Circuit lines, checkmark/X nodes |
| Cloud migration | cyan-to-blue or violet-to-blue | A4 Stack or A3 | Cloud (with logo or padlock inside) | Provider logo chips |
| OT / IT / Manufacturing | teal-to-navy or cyan-to-blue | A3 or A2 | Shield bridging factory + building | Factory silhouette, gears |
| VDI / Virtual desktop | cyan-to-blue or monitor-body | A3 or A5 | Monitor + laptop combo | App tiles, cloud, window UIs |
| Education / campus | violet-to-blue or paper-pastel | A3 or A4 | Graduation cap + cloud | ID cards, book icons |
| Cost / ROI / savings | teal-to-navy with teal accent | A2 Duality | Coins + bar chart | Dollar pills, progress bars |
| Pain point / Vendor lock-in | red-dramatic (rare) | A6 dark flavor | Receipt, chain, broken chain | Coins, red accents |
| Automation / robotics | teal-to-navy | A3 | Robotic arm + conveyor | Gears, warning/lock badges |
| Monitoring / analytics | cyan-to-blue or teal-to-navy | A5 admin-dashboard flavor | Browser/monitor with chart | Icon badges, KPI numbers |
| GPU / performance | cyan-to-blue or monitor-body | A3 | GPU chip + monitor | Graph widgets, gauges |
| Transformation / modernization | violet-to-blue | A2 or A3 | Citrix → Thinfinity flow | Checkmark nodes, factory |
| Aspirational product hero | violet-to-blue radial | A6 poster flavor | Agent bust with headset + channel halo | Sparkles, cloud above |

---

### 11. Anti-Patterns (do not ship a cover that…)

- Has the headline text baked into the image (title belongs in CMS)
- Uses photography or real-world photos
- Uses mascots or anthropomorphic characters
- Uses gradient mesh or complex 3D renders
- Puts a logo outside a white chip on a colored gradient
- Has more than one hero object at the same visual weight
- Uses > 2 color families in the same cover
- Leaves the canvas with empty quadrants (composition must feel balanced)
- Uses emoji as icons
- Uses bright red Family E for any article that isn't explicitly about a problem

---

### 12. Reference Library

21 sample covers in `reference/cover_01.png` … `cover_21.png`. Each filename corresponds to the examples cited throughout this spec.

---

### 13. Next Steps (implementation)

- [ ] Build `build_blog_cover.py` — Python SVG generator parameterized by (topic_kit, family, composition, hero, satellites)
- [ ] Create library of reusable hero SVG components: shield, cloud, padlock, monitor, laptop, factory, graduation_cap, robotic_arm, server, coin_stack
- [ ] Create library of satellite primitives: circle_badge, connection_line, halo, concentric_rings, label_pill, logo_chip
- [ ] Export pipeline: SVG → PNG 1840×1084 via Playwright/Chromium (matching whitepaper pipeline)
- [ ] Optional: Figma push via `generate_figma_design` for co-design

---

### 14. Variance across variants

When a request asks for several covers:

- At least **4 different archetypes** across the 6
- At least **3 different gradient recipes**
- Each variant has a **different hero** (or compound hero)
- All 6 express the **same core concept** — verify before diverging

(For one cover none of this applies: pick the archetype that fits the article best.)

---

### 15. Cover editorial rules (non-negotiable)

1. **Variants = same idea, different composition.** Never six different angles on the article.
2. **Don't default to red for "big".** `red-dramatic` / A6 dark = pain. For aspirational covers use A6 poster.
3. **Use canonical icons** — don't reinvent per cover.
4. **Titles in chips**, not floating text. Most covers have NO title (the article title lives in CMS).
5. **One focal per cover.** Two focals at equal weight = a diptych (A2 Duality's job).
6. **Products over logos.** Third-party logos (OCI / AWS / Azure / Citrix) as generic cloud icon + text label. No pixel-accurate reproductions.
7. **A5 flavors are distinct.** Agent console vs admin dashboard serve different narratives.
