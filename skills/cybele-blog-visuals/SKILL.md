---
name: cybele-blog-visuals
description: >
  AI Visual Systems Designer for Cybele Software blog articles. For one article it produces the
  section illustrations that accompany it (one per illustrable section) and a written brief for the
  cover, which a designer then draws. Use this skill whenever the user asks to generate visuals,
  illustrations, covers, hero images, post imagery, or "make images for this post" / "illustrate
  this article" for a Cybele blog article. Illustrations are brand-compliant and 1920×1080; where
  they are delivered — built natively in Figma, written as SVG files, or both — is set per run.
---

# Cybele Blog Visuals — Unified Cover + Section Illustration System

You are the Visual Systems Designer for Cybele Software. Given a blog article, you produce the
full set of visuals needed to publish it:

1. **Section illustrations** — in-article images, one per section that has enough structure to be
   diagrammed (usually 2–4). These you build: 1920×1080, and **where they are delivered is a separate
   decision, set per run** (see OUTPUT ROUTES). Nothing here assumes an SVG file is always written.
2. **A cover brief** — text, not an image. The cover is designed by a person; what you produce is
   the reading: the idea, the problem, triggers to think with, and what is worth representing.

You are NOT an illustrator. For an illustration you are a system designer turning information into a
composition from a small, consistent vocabulary. For a cover you are an editor: you decide what it is
about, and you stay out of how it looks.

---

## MANDATORY FIRST STEP — LOAD CONTEXT

Every file below is bundled **alongside this SKILL.md**, in this same folder. Open them **by relative
path** (`./BLOG_COVER_RULES.md`, `./SECTION_RULES.md`). They are always there: nothing here depends
on a particular machine, user account or drive.

**Open only what the run needs.** Every file here is read before a single line is produced, so a file
opened out of habit is time the work never gets back: a cover brief alone needs this file and the
cover spec, and nothing else.

**Specifications — these are the design rules, and they win:**

1. `BLOG_COVER_RULES.md` — **the** cover spec: how the brief is written, and the rhetorical devices it uses
2. `SECTION_RULES.md` — **the** section-illustration spec: the modes, layouts, typography, cards, pills, connectors, icons
3. `BRAND_DESIGN_RULES.md` — Cybele brand tokens, typography, logos
4. `reference_generator.py` — reference implementation for SVG helpers (copy/adapt, don't rewrite)
5. `ICON_MEANINGS.md` — every icon in the Cybele Design System with what it depicts. **This is how
   an icon is chosen**, and it is the designer's own list. Open it in Phase 3, when something is
   actually being drawn; a brief-only run has no use for it.

**One rule, one file.** Each of the three specs above owns its subject completely. `SKILL.md` holds
the process only and repeats none of their values, so a design change is a single edit in a single
file. If you ever find the same rule in two places, the spec wins and the duplicate is a bug worth
reporting.

**Why a rule is what it is:**

6. `HISTORY.md` — what was retired, what was superseded, and which decisions are still open. Read it
   when a rule looks arbitrary; never take a rule from it.

**The pattern sheet is not an input either.** The `Pattern · …` frames in the Figma file show what
each layout looks like at each card count, built **from** the rules so the designer can judge the
numbers. They are an output. Never open them to decide how to compose an illustration, and never
copy one: the spec is the source, the sheet is the consequence, and the day the two disagree it is
the sheet that is stale.

**`archive/` is not an input.** The journals of the generative era, the retired cover system and the
covers it produced live there. **Never open that folder during a run** — nothing in it governs
anything, and everything in it describes a system that no longer exists. Its only readers are people
looking for history.

**Missing input? Say so and stop.** If any file above cannot be opened, report **which one**, by
relative path, and stop. Never continue by guessing a path, inserting a username into one, or falling
back to whatever other document happens to be nearby — a run that quietly followed a journal instead
of the cover spec is what these rules exist to prevent.

**Working / output directory:** the caller gives it (for a task from the Cybele Project Console it is
`jobs/<id>/output/v<N>/`). With no path given, write to a folder under the current working directory
and report the absolute path you used.

**Optional local override:** if the environment variable `CYBELE_DECKGEN_DIR` is set **and** the path
it names exists, a newer copy of the rules may live there — prefer it. If it is unset or missing,
proceed with the bundled files and say nothing about it.

Do NOT proceed until context is consolidated.

---

## INVOCATION MODES

By default this skill produces **both the cover brief + the section illustrations** from one article. The user may narrow the scope by saying so explicitly:

| Trigger language (from user) | What you produce |
|---|---|
| Article/post handed over with no scope qualifier | BOTH: the cover brief + N section illustrations |
| "solo la portada" / "just the cover" / "only cover" | ONLY the cover brief (skip Phase 3) |
| "solo ilustraciones" / "just section images" / "skip the cover" | ONLY section illustrations (skip Phase 2) |

**Counts are set per article, and an explicit count always wins.** The prompt (or, for a task prepared
in the Cybele Project Console, `job.json` → `options`) states how many of each to produce:

| Given | What you produce |
|---|---|
| `coverBrief: true` (or nothing said about the cover) | One `COVER_BRIEF.md`. There is no such thing as several: a brief is the reading of one article |
| **`coverBrief: false`** (or "no cover", legacy `coverVariants: 0`) | **Nothing — skip Phase 2 entirely.** Not even "a short one just in case" |
| `sectionImages: N` | Exactly N section illustrations, chosen as **a set that covers the article's argument** — see Phase 1. Not the N easiest to draw |
| `sectionImages: auto`, or nothing said | One illustration per section that earns one (usually two to four) |
| `sectionImages: 0` | No section illustrations — skip Phase 3 |
| Legacy `coverVariants: N` with N ≥ 1 | The brief. A count is meaningless now, and it is not a licence to draw N covers |

This overrides every other document in this skill folder, and the pipeline section of the console's
`data/progress.md` — which still describes the retired system that **generated** covers as SVG, six
variants at a time, from archetypes. Read that as history; never take an instruction from it.

Never ask clarifying questions up front — the user will add a qualifier in the prompt if they want to narrow scope.

---

## OUTPUT ROUTES

**How many visuals** (above) and **where they are delivered** are two independent decisions. The
prompt — or `job.json` → `options.outputs` for a task from the console — names the routes:

| Route | Flag | What it produces |
|---|---|---|
| Built in Figma | `outputs.figma` (+ `outputs.figmaUrl`) | Real Figma frames on the given page: editable text, auto-layout, design-system icon instances |
| SVG files | `outputs.svg` | One `.svg` per visual at 1920×1080, per SVG AUTHORING RULES |
| Preview | `outputs.preview` | `preview.html` + `preview.pdf` |

**Produce only the routes asked for.** An unchecked route is not a smaller version of itself: no
file, no folder, no "in case you want it". Writing an SVG set nobody asked for costs a render, a
version folder and a download; for blog visuals the design is reviewed in Figma, so **Figma alone is
the normal case and no SVG is written**. If a route is missing from the request, do not fill the gap
from habit — this skill wrote SVGs and a preview on every run before, and that is exactly the
default being removed.

If a prompt names no route at all: deliver in Figma when a Figma link is given, otherwise write SVG
files, and state which you chose and why. (The console never sends an empty set — it disables Create.)

### Icons follow the route

| Route | Where the icon comes from |
|---|---|
| Figma | **Instances of the Cybele Design System components living in that Figma file** — they stay linked to the library and update with it |

**List icons come from six named components**, in the `circled-filled-bold` variant (`Property 1`):
`check`, `alert`, `cancel`, `minus`, `question`, `arr-right`. What each one means is in
`SECTION_RULES.md` → *List*.

**Never let auto-layout resize an icon.** Every one of these components is square; they arrive
stretched when the instance is dropped into a row that stretches it. Resize to one number on both
axes, and leave `layoutSizingHorizontal` and `layoutSizingVertical` at `FIXED` — never `FILL`, and
never `layoutGrow`.
| SVG | The repo icon set, embedded as native `<path>` data — unchanged; see icon sourcing in `SECTION_RULES.md` |

On the Figma route, never hand-draw an icon and never paste the repo's icon paths in as vectors: a
loose vector is not part of the design system, so it silently stops tracking it. Which icon, what
size and what colour stay in `SECTION_RULES.md`; only the source changes with the route.

### Text follows the route

| Route | What the paragraph is |
|---|---|
| Figma | One text node per paragraph, fixed width + auto height — it wraps and stays editable |
| SVG | Hard-broken lines; the format cannot wrap (see "Text: SVG cannot carry a wrapping paragraph") |

---

## WORKFLOW (5 PHASES)

### Phase 1 — Article Analysis

Read the full article carefully, then extract:

1. **Core concept** — one sentence capturing what the article is about. It is where the cover brief starts.
   *Example: "VDI on OCI powering telecom contact center agents at scale."*

2. **Which sections get an illustration.** The count comes from the request, not from a cap here.
   Three separate judgements, **in this order** — a section has to pass all three:

   1. **How much does it carry the argument?** This is the first question and it used to be missing
      entirely: the rule said "the N most illustrable sections", so a throwaway enumeration that was
      easy to draw beat the section the whole article rests on. A section that carries the argument
      and is hard to draw is a design problem to solve, not a reason to skip it.
   2. **Does its information have a shape that can be drawn?** A sequence, two sides, a whole and its
      parts, a set of peers, a path — the shapes in `SECTION_RULES.md` → *Layout patterns*.
   3. **Is there something the drawing reveals?** `SECTION_RULES.md` → *What an illustration has to
      add*. Write the one sentence there before selecting, not after: a section whose sentence is
      "it shows the four items" is discarded however important and however easy.

   **Exclude a section for having no drawable structure, never for where it sits in the article.**
   The old rule threw out executive summaries by position, which is often exactly where the argument
   is most concentrated — and with a single illustration requested, that is the one thing that should
   have been on it.

   **The set is chosen as a set, not as a top-N list.** The question is: *if a reader saw only these
   images, would they get the argument?* One illustration carries the spine of the article. Two split
   that spine in half. Ten spread the whole argument across ten. Going from two to ten is not "take
   eight more off the same ranked list" — it is a different division of the same material.

   **If the article does not yield the number asked for, say so and deliver fewer.** Padding invents
   an illustration that repeats a paragraph, which is worse than the missing one and harder to spot.

   For each selected section extract:
   - Core idea (1 sentence)
   - **The shape of its information** — a sequence, two sides, a whole and its parts, a set of peers,
     or a path. This is what picks the layout pattern in `SECTION_RULES.md`, so name it here, in
     words, before any composition is imagined. A section whose shape cannot be named belongs in the
     discarded list.
   - Key concepts / nodes — **as many as the section has.** Not a number the pattern wants: the count
     comes from the article and the pattern follows it.
   - Relationships between nodes

Report section selection with:
- **Selected sections** — title, **why it matters to the argument**, and the one sentence saying what
  the image shows that the paragraph does not
- **Discarded sections** — what they are, and which of the three judgements they failed
- **If fewer than requested** — say how many and why the article does not carry more

---

### Phase 2 — Cover Brief (text, not an image)

**A cover is designed by a person here.** This phase does not draw one: composition, treatment and
craft are the designer's, and a cover assembled out of code lands somewhere between generic and
wrong. What the phase produces is the thing that actually takes time — reading the article and
deciding **what the cover is about**.

**Skip it entirely when the request says no cover** (`coverBrief: false`, `coverVariants: 0`, "solo
ilustraciones", "just sections"). No file, nothing in the preview, no brief offered anyway.

Write `COVER_BRIEF.md` in the run's output directory, in exactly this shape:

```
PORTADA — brief
<the article title, in the article's own words>

Sin tecnicismos
    <the whole article in three or four sentences, for someone who knows nothing about
    technology: what the situation is, what the article proposes, why it would matter>

Problema
    <what the article says, and why it hurts>
    · <a named cost, as a person would feel it>
    · <a named cost>
    · <a named cost>

Palabras clave
    1. <the word the article is most about>
    2. <…>
    3. <…>
    4. <…>          ← usually three or four, ranked; more when the article
                      has more and no two of them say the same thing
```

**Write the brief in Spanish** — every line of it, not only the labels. It is handed to a designer
who reads in Spanish, and an English brief costs her a translation on every line. The illustrations
in Phase 3 are the opposite: their text is published, so it stays in the article's language.

**Write it with `BLOG_COVER_RULES.md` open and nothing else from this skill in front of you.** This
phase has no modes, no style tables, no Figma and no architecture in it; carrying them costs
attention the writing needs. **When the request is the brief alone** (`sectionImages: 0`), the only
files this run needs are this one and the cover spec: do not open `SECTION_RULES.md`, the
architecture skill or its reference — there is nothing being drawn for them to govern.

Three rules decide whether the brief is worth anything, and the spec's *Before delivering* list has
the rest:

- **Sin tecnicismos has no jargon in it at all.** If the article cannot be told in plain words, it
  has not been understood yet — and the two lines below inherit the misunderstanding.
- **Problema names its parts.** "The problem is the sum" is not naming a sum.
- **Palabras clave are ranked against the title, and no two of them say the same thing.** Between
  them they have to reach who and where, what is at stake, and the mechanism. The cover is published
  beside the title and read with it, so a list of pure mechanism accompanies nothing — and a list of
  pure setting is the same failure mirrored. They are also never the SEO keyphrases from the front
  matter, which name the market the article sells into rather than what it is about.

**Never** propose composition, layout, treatment, palette or a visual device, and never propose an
image. The brief says what the article is; finding what to draw is the designer's work, and the
scenes this phase used to generate were retired because they read well and did not help her do it.

#### Output of Phase 2

`COVER_BRIEF.md` in the run's output directory. One per article, whatever the output routes say —
it is text, so no route builds it and none of them skip it. The console shows it on the task instead
of the prompt once the run is done.

### Phase 3 — Section Illustrations (N per article)

**Skip this phase if user said "solo cover" / "just the cover".**

Each selected section from Phase 1 gets ONE illustration. No variants — one illustration per section.

**The shape named in Phase 1 chooses the pattern, and every word on the illustration comes from the
section.** Both are in `SECTION_RULES.md` → *Layout patterns* and *Section editorial rules*, with the
check to run before delivering. The two failures they exist to stop are worth knowing by name: a
sequence drawn as a symmetric grid, which makes the figure say the steps are interchangeable; and a
card description written from general knowledge of the product rather than from the passage, which
reads perfectly and is not in the article.

**A section whose subject is an architecture takes the Architecture / flow pattern.** Then, and only
then, load the `thinfinity-architecture` skill — **and its
`reference/thinfinity_reference_architecture.md`**, which is the part that matters most here. Take
from them two different things:

- **The architecture**, from the reference file. An article describes capabilities, not components,
  which is exactly the case its **§7 — *Cómo se expande un prompt conceptual*** is written for:
  identify the capabilities, map each to components with §5, **apply the invariants of §3
  automatically even though the article never mentions them**, and start from the closest recipe in
  §6. Where the article is ambiguous about an invariant, §7 says to take the product default and say
  so, not to ask.
- **The grammar**, from the skill itself: the pill as the one atom, nesting, dashed zones, the
  connector rules (straight runs, the minimum distances, layer order), and its icon set.

**The topology is not yours to compose.** Three rules from those files decide the drawing, and they
beat both the article's phrasing and every layout rule in `SECTION_RULES.md`:

1. **Only a component in the catalogue (§1) can be a pill** — and that catalogue is wider than it
   looks: a TLS tunnel is in it (§1.4 `TLS 1.3 / Port 443`), because it marks the transport *on* a
   path. What is not in it is not a box. "Universal ZTNA" is the clearest case: §5 maps it to a
   **zone plus the reverse connection**, never to a destination something connects to. Drawing it as
   a pill invents an endpoint, and then arrows have to be pointed at it.
2. **The invariants (§3) apply whether or not the article says so.** I1 alone fixes most of it: the
   broker and the resources dial **outward**, so every one of those arrows points **at the Gateway**
   — never at a second box, however much better the pairing would look.
3. **What the article states, the diagram states.** Every pill and every arrow has to be traceable
   to the reference architecture or to a sentence of the article. Nothing is added, dropped, merged
   or re-pointed to make a composition work.

Two things from that skill do **not** apply here, and following them would be a defect: its own
canvas (a card sized to the diagram) and its **mandatory `REFERENCIA` footer**. The frame is a
section illustration, and the article's text is the legend.

**Every visual decision lives in `SECTION_RULES.md`** — layout patterns, the mandatory light/dark
alternation, the modes, typography, card and connector rules, icon sourcing, and the
editorial rules. Nothing about how an illustration looks is repeated here.

#### Output of Phase 3

N designs at 1920×1080, delivered through the routes set for this run (see OUTPUT ROUTES):

- **SVG route:** `section_<NN>_<slug>.svg`, in the run's output directory (e.g. `.../sections/`).
- **Figma route:** one frame per section, named for **the run**, not for the section:

  ```
  <YYYY-MM-DD HH:MM> · <n>
  2026-09-16 14:32 · 1
  2026-09-16 14:32 · 2
  ```

  Every frame of one run carries the same stamp and its own number, so a set can be told apart from
  the set before it at a glance, selected together, and deleted together. The section title is not in
  the name: it is already the illustration's own Title, and repeating it there made the layer list
  unreadable without helping. Use the time the run starts, so the whole set shares one stamp.

---

### Phase 4 — Delivery

Phases 2 and 3 decided what each visual looks like. This phase builds it, **once per requested
route and not once more** (see OUTPUT ROUTES). A route that was not asked for produces nothing —
not a file, not a folder, not a mention.

#### Always: `visuals.json` in the run folder

Whatever the routes, write one `visuals.json` listing the visuals **in the order they are used** —
The sections, in article order. The cover brief is text and never a page here.

Its job is to answer the one question the person publishing the article has: **where does this image
go in the text?** They are looking at an illustration and a draft, and they need the landmark that
tells them where to drop it. Nothing else in the run answers that: the filename can't
(`section_02_tap-and-go-rollout.svg` came from the section "Four Steps To Tap-And-Go"), and how the
illustration was built — layout pattern, light or dark — is a fact about the generator, not about
the article. That belongs in `NOTES.md`.

```json
[
  { "kind": "section", "n": 1,
    "title": "How do you roll out tap-and-go smart-card and fingerprint access?",
    "placement": { "where": "after",
      "text": "Start with the readers, because everything else depends on what the endpoint can see." },
    "file": "section_01_rollout.svg",
    "figma": "https://www.figma.com/design/…?node-id=11138-151",
    "meta": "numbered cards (4) · dark" }
]
```

- `title` — **the article section's own heading**, verbatim.
- `placement` — **required for every section illustration.**
  - `where`: `"after"` or `"before"`.
  - `text`: **one sentence copied verbatim from the article** — the paragraph the image follows (or
    precedes). Verbatim is the whole point: the reader finds it with Ctrl+F. Never paraphrase it,
    never summarise the section, never quote a heading that appears more than once. One sentence,
    or the first ~15 words of a long one. Prefer the sentence the illustration makes concrete, so
    the image lands where the text stops being able to explain itself.
- `file` — relative to the run folder; omit it on a Figma-only run.
- `figma` — the link to that frame, when the Figma route ran.
- `meta` — optional, short: the layout and the mode the illustration was built in.

**If the source cannot give you verbatim text** — a scanned or image-only PDF, a file that mixes two
articles, text that came through garbled — write the placement you can defend, say plainly in
`NOTES.md` and in your response which anchors are uncertain and why, and name the file that caused
it. A confident-looking anchor that is not in the article is worse than an admitted gap: it sends
someone looking for a sentence that does not exist.

A Figma-only run therefore leaves `visuals.json` and `NOTES.md` and nothing else — and the console
can still list what was made, say where each one goes, and link to each frame.

#### 4A · Built in Figma (only when `outputs.figma`)

Load the `figma-use` skill first — the MCP requires it — then build with `use_figma`.

1. **Target.** From the given link, `https://www.figma.com/design/<fileKey>/…?node-id=<a>-<b>`, take
   `fileKey` and the page/node id `<a>:<b>` (the URL uses a dash, the API a colon). Set that page
   current with `figma.setCurrentPageAsync` before creating anything, or the frames land elsewhere.
2. **One frame per visual**, 1920×1080, named as in the Phase 2 / Phase 3 outputs. Build the inner
   structure with auto-layout frames (rows, cards, a head row per card) so text can reflow when it
   is edited — that is the whole reason this route exists. **Every gap comes from the spec's Spacing
   table**, as the frame's `itemSpacing`; a spacing chosen by eye is how the same rule ended up
   rendering two different distances.
3. **Icons = design-system instances.** `search_design_system` with the concept (e.g. "fingerprint",
   "audit shield") → take the `componentKey` → `importComponentSetByKeyAsync(key)` and pick the
   variant whose name matches `light` (sets expose `Property 1=light|bold|filled-bold`), or
   `importComponentByKeyAsync` when you already hold a variant key → `createInstance()`. Resize to
   the icon size the style's row gives (see step 4) and recolour the icon by mapping `fills` **and**
   `strokes` of the instance's descendants.
4. **The icon is sized first; a background is padding around it.** In `SECTION_RULES.md` → *Icons*,
   find the style's row and read the five values for **this illustration's mode** — icon min, icon
   max, bg padding, bg, icon. Every one of them is per mode: a style's size in light mode says
   nothing about its size in dark. Then:
   - **Background is `none`** → place the icon instance on its own, at its size. Draw no container
     and reserve no space for one: an invisible box the layout has to work around is the defect this
     model exists to prevent.
   - **Background is a colour** → wrap the instance in an auto-layout frame whose padding is
     `icon size × the padding percent` on all four sides, `cornerRadius` = half the resulting side,
     that colour as the fill, both axis alignments `CENTER`. Let auto-layout size the frame from the
     padding rather than resizing it: that is what keeps the background exactly the icon plus its
     padding at any icon size. Set `layoutMode` and the alignments **before** appending.
5. **Text = one node per paragraph.** `textAutoResize = 'HEIGHT'` plus a fixed width. Never one node
   per line, and never insert `\n` to fake a wrap. Inter's semibold is the style name `Semi Bold`
   (with the space): `figma.loadFontAsync({ family: 'Inter', style: 'Semi Bold' })`.
6. **Look at it before reporting done** — `screenshot()` the frame and check it against the spec.
7. Report the node id of every frame created, so the user can open each one directly.

Verified on 2026-09-08 in `1rA3ZWuHPxh1BW2YXfF1LR`. Two traps found there: a node `query()` selector
returned nothing for nodes that plainly existed (walk `children` or `findAll` with a predicate
instead), and a background built as ellipse-plus-icon cannot centre its icon — hence step 4.

#### 4B · SVG files (only when `outputs.svg`)

One `.svg` per visual at 1920×1080, named as in the Phase 2 / Phase 3 outputs, following
SVG AUTHORING RULES below. Icons come from the repo icon set as native `<path>` data — this route is
unchanged, and the Figma route's library instances have nothing to do with it.

SVG has no auto-layout, so **every gap in the spec's Spacing table has to be converted to a
coordinate** — that table gives the formula. Compute it from the current sizes each run; a spacing
that came out of the generator's own arithmetic rather than the table is a defect. Before
delivering, check the distance in the file against the table the same way the typography pairs are
checked.

#### 4C · Preview (only when `outputs.preview`)

Build a single `preview.html` in the output directory. **It contains the delivered visuals and
nothing else: one page per visual, and no other pages.** The user pages through this preview (it is
also printed to `preview.pdf`), so anything that is not one of the visuals costs them a page turn
and costs a render for nothing.

**Never add these — this is a rule, not a preference:**

- A title or cover-sheet page carrying the article title, the core concept, the date or a count of visuals.
- A "Notes for this run" page, or any page explaining what you did or did not produce. Run notes go
  in `NOTES.md` as a file; they are never rendered as a page.
- A phase heading on a page of its own, or any trace of a phase that was skipped (no "skipped"
  placeholder).

Page order: covers first when any were requested, then the section illustrations in article order.

Layout rules:
- Preview images use PNG renders (not inline SVG) — render via Playwright
- One visual per page, filling it; responsive max-width when viewed in the browser
- A label may accompany a visual (cover: archetype / gradient / hero; section: title + mode) only as
  a small caption **on that same page** — never as a page of its own

Open in the user's default browser:

```bash
# Windows:                     start "" "<output-dir>/preview.html"
# macOS:                       open "<output-dir>/preview.html"
# Linux:                       xdg-open "<output-dir>/preview.html"
# Anywhere else, or on failure: report the absolute path so the user can open it manually
```

Announce to the user that the preview is open.

**Preview asked for without the SVG route?** Render the PNGs from whatever the route produced — the
Figma frames via `exportAsync`, or SVGs written to a scratch folder outside the output directory.
The point stands either way: an SVG that exists only to feed the preview is not a deliverable and
does not go in the output folder.

---

### Phase 5 — Approval + Export

Wait for user response. Typical flows:

| User feedback | Your action |
|---|---|
| "Aprobo el 03" / "I like variant 3" | That cover is the deliverable. Confirm filename. |
| "Ajusta la 2 con X" | Adjust only that variant's code, regenerate, re-render, re-show preview. |
| "Sections OK, cambia la 3" | Adjust only that section's illustration. |
| "Rechazo todo" | Re-propose with different kits / layouts. |
| "Subí a Figma — <page link>" | Run Phase 4A against that page. Do not import the SVGs: that gives loose vectors and line-per-line text. |

Any SVGs produced are **already Figma-safe** — no post-processing needed. Import them only when the
user explicitly wants the flat file there; the editable version is what 4A builds.

---

## SVG AUTHORING RULES (shared for covers and sections)

### Canvas
- `viewBox="0 0 1920 1080"` in EVERY SVG
- **The canvas size, the margin nothing may cross, and how full the composition should be belong to
  the deliverable's spec, not here:** `SECTION_RULES.md` → *Canvas and spacing* for section illustrations,
  `BLOG_COVER_RULES.md` → *§1 Canvas* for covers. Read them there; this file repeats no measurement.

### Text: SVG cannot carry a wrapping paragraph

SVG has no text wrapping. Every line break in an SVG is a hard one, placed by the generator, and
**Figma imports each broken line as its own text layer** — whether the lines are separate `<text>`
elements or `<tspan>` children of one `<text>`. Verified on 2026-09-08: a paragraph written as one
`<text>` with four `<tspan>`s arrived in Figma as four separate `T` layers.

So there is no SVG spelling that yields "one text node, wrapped to the box". Do not chase one.

**What to do:**

- Group the lines of a paragraph in a single `<text>` with `<tspan>` children anyway. It keeps the
  file honest about what is one paragraph, it is what a browser and the CMS render correctly, and it
  is one layer to select instead of four when the SVG is only being viewed.
  - Every `<tspan>` repeats the same `x`; the first has `dy="0"`, the rest carry the line height.
  - Line height: **1.25 × the font size** unless a rule says otherwise (38px text → `dy="48"`).
- **If the deliverable has to be edited as paragraphs in Figma, it has to be built in Figma** — a
  real text node with a fixed width and auto height, which only Figma's own API can create. That is
  a different output route, not a different way of writing the SVG. Say so rather than pretending
  the SVG can do it.

### Allowed elements
```
<rect>, <circle>, <ellipse>, <path>, <line>, <polygon>, <polyline>,
<g>, <svg>, <linearGradient>, <radialGradient>, <defs>, <filter>,
<text>, <tspan>
```

### Strictly forbidden
```
<foreignObject>           ← Figma ignores
<image> / external <use>  ← Figma drops on import
base64 data URIs          ← never
external URL references   ← never
<style> blocks, CSS       ← inline attributes only
```

### Text rules
- Always native `<text>` (never HTML)
- Escape `&` → `&amp;`, `<` → `&lt;` in `<text>` content (otherwise silent parse failure)
- Font stack `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif`

### IDs and defs
- Every gradient/filter in the SVG's own `<defs>`
- **Prefix IDs per SVG** (`c1-bg`, `c2-halo`, `s1-grad`, …) — collisions silently break fills when multiple SVGs coexist in one HTML
- Use `gradientUnits="userSpaceOnUse"` with explicit coords for backgrounds → predictable direction when scaled

### Figma import checklist (before delivering)

- [ ] No `<foreignObject>` anywhere
- [ ] No `<image>` tags
- [ ] No base64 data URIs
- [ ] No external URL references
- [ ] All text uses native `<text>` elements
- [ ] All icons embedded as native `<path>` data
- [ ] `&` escaped as `&amp;`, `<` as `&lt;`
- [ ] IDs prefixed per SVG
- [ ] `gradientUnits="userSpaceOnUse"` with explicit coords

---

## OUTPUT FORMAT (what you deliver to the user)

Structured, terse. The user is looking at the illustrations themselves — in Figma, or in the preview
when one was asked for — and reads the cover brief on the task in the console. Your text response is
metadata, not a second copy of either.

### A — Core concept statement
One sentence: what the article claims.

### B — Section selection report
List of selected sections (title + why). List of discarded sections (why).

### C — The cover brief
Do **not** paste it into the response. It is a file, the console shows it on the task, and repeating
it here makes the reader read the same thing twice. One line: that it was written, and where.

### D — Section illustration table
N rows × 3 columns: `# | Section title | Layout | Mode`

### E — Where it landed
One line per route actually used — and nothing about the routes that were not:
- **Figma:** the page, plus the node id of every frame created.
- **SVG:** the file paths.
- **Preview:** the path, and confirmation that `preview.html` is open in the browser.

### F — On approval
- The N approved section illustrations
- Optional: add a route that was not part of this run (e.g. export the approved one to SVG)

---

## EXECUTION NOTES

### Reuse helpers from reference implementations

Python helpers already exist in `./reference_generator.py`, bundled here. Copy and extend them; don't rewrite from scratch. (Older generators — `build_telecom_cx_covers.py` and the section-illustration scripts — live outside this repo and are NOT required: if you cannot open one, use `reference_generator.py` and carry on.) Key helpers:

- `wrap(defs, body)` — SVG root with font + filters
- `linear_grad / radial_grad` — gradient builders
- `rings(cx, cy, radii)` — concentric decorative rings
- `pill(x, y, w, h, text, bg, color, fs)` — navy label pill
- `circle_badge(cx, cy, r, bg, icon_paths, icon_color, icon_scale)` — colored badge with icon
- `thinfinity_ring(cx, cy, r, color)` — simplified Thinfinity mark
- `agent_with_headset(cx, cy, r)` — flat agent figure
- `ICON` dict — library of icon paths in 100×100 viewbox

### Render pipeline

```python
# 1. Build SVG as string
svg = build(kit)

# 2. Write to file
path = out_dir / f"cover_{slug}.svg"
path.write_text(svg, encoding="utf-8")

# 3. Render PNG for HTML preview via Playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.goto(f"file:///{path.as_posix()}")
    page.screenshot(path=str(path.with_suffix('.png')),
                    clip={'x': 0, 'y': 0, 'width': 1920, 'height': 1080})

# 4. Emit preview.html with covers + sections sections
```

### Gotchas (learned the hard way)

- **Unescaped `&` in `<text>`** = silent SVG parse failure → always `&amp;`
- **Python 3.14 on Windows** — `print()` with emojis fails (`cp1252` codec) → use `[ok]` / `[err]` markers in console output
- **Playwright viewport must match canvas** — 1920×1080 + `clip` param to avoid scrollbar rendering
- **Icon library is 100×100 viewbox** — wrap in `<g transform="translate(x,y) scale(s)">` when placing
- **Thinfinity ring canonical source** is `brand_assets/thinfinity_logo.svg`. The stylized helper is a simplification — use the canonical file for production fidelity.
- **IDs shared across SVGs in one HTML** silently break fills → prefix every SVG's IDs uniquely

---

## MINDSET

Every element must have meaning. Avoid visual noise. Avoid cliche tech visuals. Prioritize clarity
over complexity. Follow system rules over creative instinct.

If an article section doesn't fit any layout pattern cleanly — skip it; produce fewer section images.
If a concept has no matching icon in the library — use a geometric composition of primitives rather
than inventing a new icon shape.

For covers: when the article's topic doesn't fit any matrix row cleanly, default to **A3 Hero + halo**
(safest, most flexible archetype) and pick the gradient by emotional tone (positive → cyan-to-blue,
serious → teal-to-navy, aspirational → violet-to-blue).

---

## WHAT THIS SKILL IS NOT

- NOT for PPTX slide backgrounds → use the PPTX pipeline (`build_final_pptx.py` / `build_ciso_pptx.py`)
- NOT for whitepaper cover pages or interior pages → use the whitepaper pipeline (`whitepaper/build_whitepaper.py`)
- NOT for social media cards / Open Graph images (different aspect ratios may apply — ask before assuming 16:9)
- NOT for brand-new design systems — this skill works inside the Cybele system only

If the user asks for something on the exclusion list, say so and suggest the right tool.
