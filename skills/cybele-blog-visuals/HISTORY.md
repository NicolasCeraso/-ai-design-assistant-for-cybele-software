# Section Illustrations — record

> **Not rules.** What was retired, what was superseded, and what is still undecided. The rules in
> force live in [`SECTION_RULES.md`](SECTION_RULES.md); nothing here governs a visual. It exists so a
> colour that was deliberately dropped is not quietly re-introduced six months later.

## Retired values

**Retired 2026-09-09: "Dimmed label"** (`rgba(255,255,255,0.80)`). It came from the June amendment,
where it reads *"Label atenuado — white @ 80% opacity"* with the example "Affected Models": a small
group label in dark mode. It arrived with a colour and nothing else — no size, no weight, no light
value, no rule about when to use one — and it contradicted the line above it, which says an
illustration has exactly three text levels. No delivered illustration ever used it; the card titles
already do that job. Yanina's call: dropped rather than defined. If a group label is ever wanted,
add it as a fourth text level with all of its variables, and fix that sentence at the same time.

**Retired (2026-06), never use as free accents:** `#d97706` orange · `#7c3aed` / `#a78bfa` purple ·
`#06b6d4` / `#38bdf8` cyan · `#ec4899` pink · `#c084fc` lavender.

## Superseded values

**Superseded colour values.** The 2026-03 reading of the Blog Posts file specified gradient
backgrounds (`#0b1120 → #0e1726` dark, `#f8f5fc → #f0ecf6` light) and a wide rainbow accent set
(orange, purple, cyan, pink, lavender). Both were **retired by the 2026-06 amendment** and replaced
by the flat surfaces and per-element colour rules in `SECTION_RULES.md`. They are recorded only so an
older illustration can be recognised — never as a source to draw from.

## Open decisions

These were flagged as pending when the reduced palette was defined. Until each is settled, follow
what `SECTION_RULES.md` says and raise the question rather than inventing a value:

- Token names for the applied derivatives still in use: `#94A3B8`, and `#0AA9FF`, which is a raw
  fill with no Figma variable.
- The exact role of `blue-violet/500` `#8878ED` / `700` `#321BC8` and `water-green/500` `#3DCCA1`
  — decorative or structural.
- Whether `blue/900` `#030C1D` or `blue-cybele/900` `#021425` is the canonical dark surface. The
  sample uses `#021425`, so that is what this file says.
- **Typography hexes disagree with the corporate palette.** This file uses `#373737` / `#515151`,
  measured from the Figma source of the amendment. The company's 06/26 palette
  (`BRAND_DESIGN_RULES.md` §2) says `TEXT_PRIMARY #2E2E2E` / `TEXT_BODY #454B57`. Blog visuals follow
  the amendment; someone should decide whether the two should converge.

## Measurements, consolidated (2026-09-08)

Every dimension moved into one `## Measurements` section in `SECTION_RULES.md`: the canvas, the safe
margin, badge and icon sizes, corner radius, connector sizes, and the gaps between text blocks. They
used to sit in five places — a `## Canvas` section, `## Icon badge`, `## Cards rules`,
`## Arrows / connectors` and editorial rule 5 — which is how "content fills ~70%" ended up written
three times in one file, the safe margin only in `SKILL.md`, and the gap between a body-text title
and its body text nowhere at all.

Values kept as they were, with three exceptions worth knowing:

- **The icon inside a badge is now a percentage of the badge diameter, not a fixed size.** That was
  already how the rule read in prose ("~60%"), but the two absolute values disagreed with it: the
  card badge was 61.8% and the hub 49.6%. Each row now carries its own exact ratio — 62% and 50% —
  so a badge at any size between the minimum and maximum scales its icon.
  **The hub icon therefore goes 120px → 121px.** A one-pixel change on a 242px badge, accepted to
  make the ratio a round number; set the row back to 49.6% if that pixel matters.
- **The safe margin became a percentage per side (3%), replacing "minimum 60px from any edge".**
  It is a percent of the canvas *width* on all four sides, so equal percentages read as an equal
  frame; 3% is 58px at 1920×1080, within two pixels of the rule it replaces.
- **"Content fills ~70% of the canvas" is gone**, replaced by the four safe-margin values above.
  Those numbers were measured off the two illustrations delivered on 2026-09-08, not invented, and
  measuring them is what showed the rule was missing: illustration 1 sat 120px from each side,
  illustration 2 sat 100px, and illustration 2 left only 48px at the bottom — under the 60px minimum
  the spec asked for at the time. The 70% had never been checked against anything.
- **A second inset was tried and dropped the same day.** For a few hours the spec carried both a
  hard limit (3% per side) and a separate "content fill" target (7 / 6 / 3.5 / 6%). Yanina's call:
  one value is enough, and two invited the question of which one to build against. The safe margin
  now *is* the layout margin and carries the measured values; the 3% floor is not recorded anywhere
  because nothing ever composed to it.
- **The gap between a Body text title and its Body text is now stated: 10px.** Nothing said it
  before, and two illustrations in the same run rendered it differently. `SECTION_RULES.md` carries
  the conversion the SVG route needs, since only Figma has auto-layout.

## Filed by purpose, not by kind (2026-09-08, later the same day)

The `## Measurements` section above lasted a few hours. Yanina's call, and the better one: a person
looking for the badge goes to the badge, not to a table of every number in the system. The spec is
now four top-level sections that the console shows as bands —

1. **Margins and spacing** — canvas, safe margin, the gaps between blocks
2. **Text** — the three levels, each with its colour, font, weight and size in one row
3. **Elements** — page surface, card, icon background, connector: each carrying its own sizes *and*
   its own colours
4. **Colors** — only what belongs to no element, which today is the accent pair

— so a measurement now sits with the thing it measures. "One rule, one place" is unchanged: every
value still appears exactly once. What changed is the filing order, and the console's grouping
follows the file rather than a mapping of its own.

Two names went with it: the two accent rows stopped being two sections called "Brand violet" and
"Brand green" and became one element, **Accent colors**, with four labelled values. And the badge is
one element again — sizes on one row, and its two colours on another, paired by mode (light fill
with light icon, dark with dark) — after being split across three sections. The word "glyph" went
with it: what sits in the background is an icon, which is what everyone calls it.

## Modes became explicit, and accents became a list (2026-09-08)

**Modes.** They existed only as column names, so the only way to learn that "dark" was a thing was
to notice some elements had a second colour. There is now a `## Modes` table: what variants exist,
what each is for, and the ability to add or drop one. Every column that varies by mode names its
mode (`Light`, or `Light · bg fill` when an element colours two things), which is what lets the
console show a mode's values as one block. Adding a mode copies an existing one into every table
that varies by mode — an empty cell is not a value the editor can offer, and "copy then adjust" is
how a variant actually gets built.

**Accents were modelled wrong twice before landing.** First as one row with a column per
mode-and-hue, which made the console draw violet and green as a tied pair. Then as one row per
accent with a column per mode — better, but it forced every accent to exist in every mode. They are
now **one row per mode, with the accents as a list in one cell**, which is what they actually are:
the set a mode is allowed to reach for. A colour can be allowed in light and absent from dark, and
adding a mode brings the accents of the mode it was copied from.

A convention came out of it: **`(list)` in a column header** means the cell holds a set, and the
console then offers add and remove on a single value there. Without the marker a multi-value cell is
one structure — a gradient pair, a stroke-and-text colour — and pulling one value out would break
it. The cover spec has a dozen such cells, which is why this is a marker and not a guess.

The first attempt, for the record: They were one row with a column per mode-and-hue
(`Light · violet`, `Light · green`), which made the console draw violet and green as a tied pair.
They are not a pair: they are the list of accents a composition may reach for, and using one implies
nothing about the other. The table is now one row per accent with a column per mode, so an accent
can be added or dropped on its own and so can a mode. The tie shown in the console — a bordered
block with a link between values — now means only what it says: values decided together, which is
true of an icon background and the icon on it, and false of a palette.

## Icons: the icon became the measurement (2026-09-09)

The size used to be the background (99-150px) with the icon as a percentage of it (43.43%). That
made "no background" impossible to express well: the box still had a size, so the layout reserved
space for something nobody could see. Yanina's objection, and she was right.

Inverted: **the icon carries the size, and a background is padding around it** — a percent of the
icon, so it scales across the range. The geometry is unchanged, only its expression:

| Before | Now |
|---|---|
| background 99px, icon 43.43% | icon 43px + 65% padding → background 99px |
| background 150px, icon 43.43% | icon 65px + 65% padding → background 150px |
| hub 242px, icon 43.43% | icon 105px + 65% padding → background 242px |

Two consequences worth knowing:

- **Icon styles are rows now**, so a second style is a row in the sizes table and one with the same
  name in the colours table. `Badge as the central hub` became the style `Central hub` and gained its
  own colours, which it used to borrow from the badge rules.
- **Each mode decides whether its style has a background**, by holding a colour or the word `none`.
  That needed a second column marker, `(fill)`: in a marked column a value may be a colour *or*
  `none`, and the console offers "no fill" / "add fill" there. Anywhere else `none` would be a value
  nothing knows how to draw, so it stays refused.

## An icon style is per mode, all of it (2026-09-09)

The sizes started as a property of the style and the colours as a property of the style *in a mode*.
That split does not survive the first mode that drops its background: an icon standing on the page
usually wants a different size than one inside a filled circle, and there was nowhere to say so.

So the two tables became one, with **five values per mode** — icon min, icon max, bg padding, bg,
icon — and nothing left at the level of the style but its name. Yanina's words: the icon styles are
100% dependent on their mode.

The markdown line is long (five columns times however many modes exist) and that was accepted
deliberately: the file is edited through the console, where the values are shown as one block per
mode that wraps to the width available. Adding a mode still copies its whole set of columns, so a
new mode arrives with a size and colours already filled in.

Values were carried across unchanged: every mode of `Icons` starts at 43-65px with 65% padding, and
`Central hub` at 105px with 65% — the same geometry the single per-style row used to describe.

## Colors stopped being a section (2026-09-09)

Section 4 held one thing — the accents — and accents turned out to belong to the mode, not to a
place of their own. They now live in the `## Modes` table, one column beside each mode's
description, so a mode is a single row that says what it is and what it may reach for. The spec is
three numbered sections again: margins and spacing, text, elements.

The console shows them the same way: the accents of a mode are drawn on that mode's row in the Modes
card, with their remove and their +, instead of appearing as separate elements repeating the mode
names under the same band. Adding a mode copies the whole registry row, so a new mode arrives with
the accents of the one it was copied from rather than with an empty cell.

## Five modes, and no accents (2026-09-09)

Yanina drew one placa per mode she wants and handed them over as a PDF. The colours below were read
out of its vectors, not judged by eye, and they replace everything the spec said about colour.

- **The accents are gone, concept included.** They were a list that sat beside the elements; now
  every colour is stated by the element that uses it, in the mode that uses it. Section 4 · Colors
  went with them, and the `## Modes` table is back to a name and a description.
- **"Color 1" was a test mode and was deleted.** The five that stand: `Light mode`,
  `Light mode green accent`, `Blue Mode`, `Dark mode`, `Dark mode green accent`.
- **Three of the five draw no icon background at all** — light, light-green and dark put the icon
  straight on the card. That is what `none` in a bg column is for, and it was drawn that way before
  the console could express it.
- **Light mode's text colours changed** from `#021425` / `#2B4051` to `#373737` / `#515151`, because
  that is what her placa uses. That settles the "typography hexes disagree" question left open above
  for section illustrations: the placas win.
- **Three elements gained values they never had.** Card had only a radius and now has a fill per
  mode. Pill or chip had only a radius and now has a background, a text colour, a size and a weight.
  **Central hub description** is new: 43px SemiBold, a colour per mode, centred under the hub, with
  its distance from the hub as a gap in *Margins and spacing*.

Sizes, radii and padding were not touched — she said so explicitly, and the placas measure the same
75 / 43 / 38px type the spec already had.

Two values were filled in with the best reading of the placas and are worth a second look: the icon
inside the hub (white in all five) and Dark mode's body text (measured pure white, though it reads
as a very light grey on screen).

## Architecture inside a section illustration (2026-09-09)

A section that describes a path or a topology could not be illustrated: the four layout patterns had
no flow among them, and a run said so out loud rather than forcing one — on 2026-09-08 it discarded
*"How does the connection path stay secure without opening ports?"* with the note that none of the
sanctioned patterns is a flow diagram. Meanwhile a complete grammar for exactly that already existed
in the `thinfinity-architecture` skill, as a separate pipeline with its own canvas.

Two things were added, and they are not the same thing:

- **A fifth layout pattern, `Architecture / flow`** — the archetype. It decides how the composition
  is built, and it borrows the arch grammar: the pill as the one atom, nesting, dashed zones, the
  connector distance rules, the icon set.
- **A sixth mode, `Arch`** — where that archetype's values live. Yanina's call, and the right one:
  the pieces carry sizes and colours that correspond to none of the colour modes, and a value needs
  a column to live in.

The pieces are new elements — Diagram pill (one size, category by border and text only), Zone,
Diagram label, Diagram connector, and the gap between containers. Their tables carry **only the Arch
column**, because no other pattern draws them; adding a mode copied from Light leaves them alone,
and adding one copied from Arch extends them.

Lengths are the arch grammar **doubled**: that spec sizes a diagram to its own canvas with small
type, and here the frame is a fixed section canvas. Read off Yanina's two hand-made examples, the
diagram label lands at 25px against the 12px the arch spec uses.

Two rules of the arch skill are deliberately dropped in this pattern: its canvas (a white card sized
to the content) and its **mandatory `REFERENCIA` footer**. The frame is a section illustration, and
the article's own text explains the arrows — her examples were built that way before the spec said so.


## The triggers were low-effort, and the spec was the reason (2026-09-11)

A brief for *Multicloud VDI* came back and Yanina marked it against one Gemini had produced from the
same rules. The gap was not tone. Four things were wrong, and three of them were the spec's fault.

**One idea, five hats.** Every scene in the run was a door or a key — the warehouse gate, the library
counter, the lift, the keyring, the badge, the key rack. Asked why the Hipérbole example was the same
as the Metáfora one, the honest answer is that it *was* the same: one analogy was found and passed
through five devices. Nothing in the spec said the five had to differ, so now it does, and the shared
object is named as the tell.

**The devices were never applied.** The spec gave one question per device and no definition and no
mechanics. Nothing in the Hipérbole row was exaggerated; the Paradoja row had no contradiction in it
— Yanina's note was simply "¿y dónde está la paradoja?". Each device now carries its definition, a
short table of named mechanics offered as inspiration rather than a limit, and a **Check** line that
decides whether a scene is that device at all. Section 3.1 runs the checks over the finished brief.

**The output format caused the brevity.** Scenarios were asked for inline, separated by `·`, so what
came back were noun phrases: *"el llavero con una llave por puerta"*. The Gemini brief carried the
same idea — the one Yanina marked as correct — as an image: an exhausted office worker hauling a
giant ring of mismatched rusted keys, standing in front of one door. A scene is now a described
image of one or two sentences, three per device, each closing with a parenthesis that traces it back
to the article.

**And the problem itself was read wrong.** The article's pain is friction — another credential,
another console, another licence. The brief modelled it as *impediment*, "you cannot get in", which
is why three metaphors were marked wrong for the same reason: the user was never locked out. The
cause was one line up. *Problema* said "the problem is the sum" without naming the parts, and every
trigger anchored to a blur. Naming the parts is now the rule, and it is the most expensive line on
the page.

Two rules were relaxed at the same time, both Yanina's call:

- **Scenes may show what changes, not only what hurts.** The examples she liked best were
  solution-side. The product itself stays out — no interface, no logo, no architecture, no brand.
- **"Everyday" is no longer the test; legible at a glance is.** That rule was fighting the wrong
  enemy: what she rejected was abstraction, not invention. A fighter jet with iron train wheels
  welded to a rail is not an everyday scene and reads instantly.

Composition stayed out, and that has not moved: no halves, no lighting, no palette, no style.


## What the skill stopped carrying (2026-09-11)

A brief-only run — no cover drawn, no section illustrations, `sectionImages: 0` — took eight minutes
to produce one page of text. The output was the best the skill had produced; the time was not the
writing.

Before a word was written, a run opened around 128,000 characters of specification. Of those, about
44,000 governed nothing that run was doing: two thirds of the cover spec was the retired generative
system (archetypes, colour families, gradient recipes), and the whole section-illustration spec was
read whether or not anything was being drawn. Sitting beside them were three journals — `PROGRESS`,
`HANDOFF`, `RECONCILIATION`, another 85,000 characters — that the skill itself described as history
never to take an instruction from. Their only remaining function was to be read and discarded.

Everything retired moved to `archive/`, which no run may open: the three journals, the generative
cover system, and the twenty-one covers of 2026-03 that it produced. A brief-only run now reads the
process and the cover spec, and nothing else.

The console's *Covers* row went with it. It listed 141 values, every one from the generative system
and none of them editable. A cover is a text brief designed by a person: there is nothing to
configure, so an empty row would only look like something had failed to load.

None of this changes a rule or a value. The 169 editable section-illustration values are untouched.


## The brief gained a line for someone who knows nothing (2026-09-14)

Yanina asked for a layer the brief did not have: besides the problem, a short retelling of the whole
article in plain words, readable by someone who knows nothing about technology.

It earns its place twice. It is the line she can hand to anyone, and it is the honesty check on the
two below it — a problem understood only in the article's own vocabulary is a problem not understood.
The brief that read the pain as "you cannot get in", when the article said "you get in three times",
would have failed here first, in plain words, where the mistake is obvious and cheap.

It sits between *Idea* and *Problema*, carries no jargon, no acronym and no product category, and is
an explanation rather than a scene: if it reaches for "it is like a warehouse with three sheds" it
has started competing with *Disparadores*, which come later and need this line to be literal.


## The layouts were formulaic, and the pattern list was why (2026-09-14)

Two illustrations from two unrelated articles came back nearly identical: *"One platform, any cloud"*
and *"One image, every store"* — same title shape, same two-by-two grid of cards, same four items.
Yanina's worry was that the content was being squeezed to fit. It was, and the second image proves it.

**"One image, every store" is a sequence**: build the image, provision with IaC, schedule the
capacity, update everywhere. Four stages in time, drawn as a symmetric grid — the figure that means
*"equal, parallel, no order"*. No numbers, no direction, and in a two-by-two nobody can tell whether
to read across or down. The spec already had *Numbered cards — sequential steps* and it was not used.

Three things in the spec caused it:

- **Three of the five patterns were the same picture.** Hub-and-spoke, Center + features and
  Symmetric 2+2 all describe a centre with four things around it. The menu looked like five choices
  and offered two.
- **Editorial rule three put a thumb on the scale** — *"Symmetric layouts preferred — 2 left + 2
  right"* — stated globally, so whatever the content was, the run was pushed toward the grid.
- **Nothing made the content choose.** The "when to use" column overlapped almost entirely, and every
  pattern's description said four while Phase 1 asked for three to six. Four became a magnet: a
  section with three got padded, one with six got trimmed.

The list is now keyed to the **shape of the information** — sequence, two sides, whole and parts,
peers, path — each pattern owning one shape and stating what the figure claims. The shape is named in
Phase 1, in words, before any composition is imagined. Symmetry dropped to a tie-breaker inside a
chosen pattern. Two illustrations in one article may not share a pattern, and two titles may not
share a grammatical shape.

**And a second defect, unrelated to layout.** In *"One platform, any cloud"*, the card headed **No
inbound ports** carried the description *"Roles mapped to the exact apps a job needs"*. That is a
different subject from its own title — and it is in no part of the article, which never mentions
roles mapped to apps. It reads plausibly because it is true of the product in general. The article's
own sentence is that the host dials out, so adding a cloud opens nothing.

Two rules came out of that one card: a description has to be about its own card's title, and **every
word on an illustration has to be traceable to a passage**. It replaced "symmetric layouts preferred"
in the editorial list, which is a fair trade — one rule that pushed the run toward a lie, swapped for
the rule that catches the quietest kind of error there is: the invented line that reads perfectly.


## The illustration has to add something, and importance has to outrank drawability (2026-09-14)

Two corrections from Yanina, both aimed at the same place.

**Sizes follow the text, not the other way round.** The proposal on the table was to derive card
widths from a column count. She rejected the premise: fix the card and the text gets trimmed to fit
the box, which is what produced the squeezed cards in the first place. The line is now explicit — a
card has no fixed width and no fixed height, and giving it one is a defect. What stays a rule is what
makes a *set* one system: margin, gaps, type, colour, radius, icon sizes. The only number added is a
floor, and it is a floor rather than a size: below it the composition reflows instead of squeezing.

**"It repeats what it last saw" is not a law to design around.** Also hers, also right. The mechanism
is not memory — runs are independent and never see the previous illustration — it is that a rule
weak enough to decide nothing produces the same default every time. Same symptom, different cause,
and the fix is the one already made: the choice comes from the content.

**Illustrations were being chosen for being easy to draw.** The counts table said, in as many words,
"the N most illustrable sections". Importance appeared nowhere in the selection, and what the run
reported was *why it's illustrable*, never *why it matters*. Three things followed from that:
a throwaway enumeration beat the section the article rests on; asking for one, two or ten only took
more of the same ranked list, with no notion of covering the argument; and Phase 1 capped selection
at two to four sections, so a request for ten could not be satisfied at all. Executive summaries were
excluded by position, which is often exactly where the argument is most concentrated — with a single
illustration requested, the one thing that should have been on it.

Selection is now three judgements in order: how much it carries the argument, whether its information
has a drawable shape, and whether the drawing reveals anything. The set is chosen as a set — one
illustration carries the spine, two split it, ten spread it — and when the article does not yield the
number asked for, the run says so and delivers fewer.

**And the rule that gives an illustration its reason to exist.** An illustration that repeats the
article is the same paragraph in another typeface: a numbered list of five drawn as five cards adds
nothing, because the reader had those items in that order a few lines above. What an illustration
contributes is a **relation** — simultaneity, proportion, containment, direction, absence — something
the prose had to say one item at a time. Two tests carry it: one sentence before composing saying
what the image shows that the paragraph does not, and, before delivering, covering every word on the
illustration to see whether anything is still being claimed.

This sits beside the traceability rule without contradicting it. **The facts come from the article;
the arrangement is the reading.** An illustration may not add a fact, and it must add an insight.

It raises the bar knowingly: some articles will not yield the number of illustrations requested, and
saying so is the correct outcome.


## What the reference illustrations taught the spec (2026-09-14)

Fifteen finished section illustrations were measured node by node. Six things the spec did not know:

**The text budget is keyed to columns, not to card count.** Four cards in a two-by-two are as wide as
two cards; what shrinks a card is the column count. Keyed that way the reference sorts itself. The
previous bands, invented rather than measured, flagged a dozen of the designer's own good cards as
too long and rejected a seventeen-character line as too short.

**Cards in one illustration stay within about twice each other.** Across all fifteen the median ratio
between the longest and shortest description is 1.21 and the maximum 2.03. That evenness is what
makes a set read as one thing, and nothing had ever said so.

**Three elements existed in the work and not in the spec** — the stat card's display number, the step
number, and the column label that lets a two-column grid make a comparison without a word of prose.
The step number had been drawn three different ways across two articles, which is exactly the drift a
rule prevents; it is now one form, the bare digit.

**Medium 500 is in the system.** The type rule said only 400 and 600 exist. The stat number is
Medium, and so is the diagram label in *Architecture pieces*.

**The card's own geometry was missing** — padding 28, icon to title 36, and the title-to-description
gap confirmed at exactly the 10 the spec already had. The icon sits beside the title on a wide card
and above it on a narrow one, and that is not taste: an icon above costs its own height, which is why
two rows of cards with the icon on top do not fit inside the safe margin.

**A card may have no fill at all.** Several reference illustrations put the icon, title and
description straight onto the page surface. It is the compact form, and it is what makes two rows of
three fit where filled cards of the same content overflow.

One invented value was wrong and was corrected: the card minimum width had been set at 380px, and the
designer's five-column illustration uses 324px — the floor forbade her own work.


## The brief went down to three lines (2026-09-15)

The rhetorical devices are retired - metaphor, metonymy, hyperbole, comparison, paradox, and the
fifteen scenes they produced. They had been rebuilt once, carefully, against a Gemini brief the
designer preferred, and the second version was much better writing. It still did not help her work,
which is the only test a brief has to pass. Good prose that does not move the job forward is a cost,
not an output.

*Idea*, *Representar* and *Naturaleza* went with them. The brief is now three lines:

- **Sin tecnicismos** - the whole article in plain words, for someone who knows nothing about
  technology. Unchanged, and now the opening line rather than the second.
- **Problema** - what the article says and why it hurts, with its parts named. Unchanged.
- **Palabras clave** - three or four words ranked in the order the article makes them matter. New,
  and it carries the whole weight the devices used to.

Two rules on the keywords exist because they are the obvious ways to get them wrong. **The order is
the argument's, not the writer's** - a list in any other order is not a ranking, it is four words.
And **they are never the SEO keyphrases**, which every article ships in its front matter: those are
written for a search engine, they name the market the article sells into rather than what it is
about, and taking them is the easy wrong answer.

What survives from the retired system is the boundary it was built to protect: the brief says what
the article is, and never proposes an image, a composition, a palette or a treatment. Finding what
to draw is the designer's work. The devices were an attempt to help with that from the outside, and
the attempt is over.


## The keywords have to cover the article, not one corner of it (2026-09-15)

The three-line brief was run on *"Smart Card Redirection for VDI: Tap-and-Go Fingerprint
Authentication for Healthcare on OCI"* and returned **carnet, huella, lector, puesto compartido**.
Four pieces of mechanism. No person, no place, nothing clinical - from an article whose first
paragraph opens on a hospital floor with a nurse roaming between exam rooms, and whose title says
*for Healthcare*.

The first correction added the title as the frame of the whole brief, which was right and stays: the
cover is published beside the title and read with it, so a brief that would fit any article about
badges accompanies nothing.

**The second correction overshot, and that is the more useful half.** The replacement list named the
clinician, the record, the ward and the med cart: now four words about healthcare, and nothing about
the fingerprint, the access or the virtual desktop - which is what the article is for. One bias
swapped for its mirror image.

The rule is neither "add the who" nor "add the mechanism". It is **coverage without redundancy**:
between them the words carry who and where, what is at stake, and the mechanism, and no two of them
say the same thing. Read the list back and ask what each word adds that the ones above it did not.

Two smaller things came out of the same review, both from the designer:

- **As general as the article allows, as specific as it requires.** The article says "a nurse or
  physician", so the word is the one that covers both; narrowing to one is a claim the article did
  not make. And a prop from a single sentence is not what the piece is about - the ward, not the med
  cart.
- **Three or four is the usual size and not a cap.** If the article has five or six things that
  matter and none repeats another, they all go in, ranked. Padding to four and trimming to four are
  the same mistake, and it is the same one already written about card counts in the illustrations.


## An illustration is read alone (2026-09-15)

A hub illustration came back for *"How does one platform consolidate VDI and app virtualization?"*
titled **"Both models come from one platform"**, with three property cards and three arrows pointing
inward at an off-centre logo. The designer found four things wrong with it, all correct, and the
diagnosis underneath them is worth more than the four.

**"Both models" is VDI and VDA.** The article defines the pair in its second paragraph and then uses
the phrase loosely for the rest of the piece, so the run quoted it faithfully - and that is the
point. **Traceable is not the same as self-contained.** The rule written the day before says every
word has to come from a passage, and this one did. But an illustration is met on its own, halfway
down a scroll, without the paragraph that set it up: the article has memory, the image does not. The
new rule is to read it cold with the article covered, and anything leaning on a definition that is
not on the image is wrong however exactly it was quoted.

**The arrows contradicted the title.** The title said the models came **out of** the platform; every
arrow pointed **into** it. An arrowhead is a claim about direction, and one of the two was false. The
deeper error is that there should have been no arrows at all: "one console" does not flow into the
platform, it is what the platform **is**. A connector table now says which patterns take an arrow -
architecture, where something travels - which take a line, and which take nothing.

**And the hub was not in the middle.** With the centre at the far left and every item to its right,
the eye reads the logo first and then travels backwards through the items. That is not a hub, it is
a list with a logo beside it, and the centre of a hub now sits in the middle of its items - which
settles the reading order without a rule about reading order.

**Last, the title pointed at something that was not drawn.** "Both", "these", "the two" are pointers;
a reader follows one and finds nothing. Either the thing is on the illustration or the title does not
name it.


## Three illustrations, and the rules they broke (2026-09-15)

A set for the Parallels comparison article came back: a two-sided card comparison, a hub, and an
architecture diagram. The set-level rules written this week all held - the modes alternated, no two
illustrations shared a pattern, no two titles shared a grammatical shape. The failures were
elsewhere, and three of them are new rules.

**One size per kind, inside one illustration.** The hub's three text boxes were three different
widths. The spec said a card has no fixed size because the content decides it, and that is right and
stays - but it is only half the rule, and the missing half is the designer's: the content decides
**one** size, set by the box that needs the most room, and every other box of that kind takes it.
Three boxes at three sizes read as three different kinds of thing, and the reader goes looking for
what the difference means. Free between illustrations, fixed inside one. The architecture pattern had
been saying this about its pill all along; it is now written once for everything.

**An arrow or nothing - never a headless line.** Yesterday's rule said a hub takes "a line, or
nothing". The designer's correction: a bar with nothing on either end states nothing and decorates
nothing, it is an arrow someone stopped drawing halfway, and the reader spends a moment working out
which it was meant to be. Where nothing moves there is no connector at all; a hub shows belonging by
proximity and arrangement, which is what a hub is for.

**In a comparison, the dimension is named once.** The two-sided placa had "Licensing model" as a card
title in *both* columns, and "White-label / multi-tenancy" in both - so the icons repeated too,
because the icon travels with the title. At a glance it does not read as a comparison: it reads as a
block pasted twice. The dimension belongs above or between the sides; each side carries the answer.

**And the same placa was a table the article already prints.** Two rows of the side-by-side
comparison, verbatim, in bigger type - and with one of its three columns dropped to fit two across.
Both halves are old failures in a new place: an illustration that adds nothing, and content trimmed
to fit a layout. The rule excluding comparison tables had been deleted the day before, along with the
exclusion of executive summaries by position, which deserved to go. It is back, on the right footing:
not because of where the table sits in the article, but because redrawing it adds nothing - and if it
genuinely needs illustrating, it is drawn whole.

One thing was ruled *not* an error, by the designer: a brand mark keeps its own colours. HTML5, AWS,
Azure and the like are recognised by colour, and repainting one costs the recognition that was the
only reason to use it.


## The designer redrew a set, and three new variables came out of it (2026-09-15)

A corrected version of the Parallels set, annotated. Six changes, four of them new variables.

**The column headers had disappeared.** In the run's version the two sides were named by a line of
body text that floated above the cards, and at a glance the comparison had no two halves. Redrawn,
the header became a level of its own: a **Column title** in SemiBold at the card-title size, in the
mode's accent colour, with an ordinary Body text subtitle under it, both sitting on a **Column header
bg** that spans the column. That surface is what makes the grouping visible; without it the headers
float. It reads as an intermediate level between the illustration's Title and a card title, which is
exactly what the comparison needed and what the spec had no name for.

**A Divider line between stacked items**, measured off the correction: 2px, the mode's accent at 20%.
The opacity is the point - at full strength the rule competes with the text it separates. Thickness,
colour and opacity are three separate variables, per the designer's request.

**The icon goes left of the whole text block, not beside the title.** The run put the icon on a row
with the title and started the description back at the card's edge underneath both, which breaks the
text's left edge and leaves the description belonging to nothing. The icon sits in its own column,
vertically centred against title and description together, and the two share one left edge.

**No interpunct as a sentence separator.** `Thinfinity · concurrent single license` is two thoughts
welded with a dot that means nothing. The dot belongs between items of the same kind - `MFA · SSO ·
SAML` - and nowhere else. Where one thing qualifies another they are a title and a subtitle on two
lines.

**The company name is never written in the third person, and rarely at all.** "A strong Cybele
partnership behind it" reads like someone else describing us.

**And the hub with the product logo at its centre is generated on every run.** The designer's note:
it ends up being very repetitive.

The first attempt at a rule banned the mark from the centre, and she rejected it: the archetype is
good, the logo is fine, **the frequency is the problem**. Every article here is about the same
platform, so every article *could* carry that picture - which is precisely why it cannot be the
answer every time. A composition that fits everything distinguishes nothing.

The second attempt added a history check - "if the answer is yes twice running, look again" - and she
rejected that too, precisely: **it is not repetition over time that bothers her, it is over-use.**
Two articles in a row may both deserve the hub, and that is fine. What is wrong is that the pattern
is *available* for every article, because every article is about the same platform.

So the rule tightens the entry conditions instead of counting. Four, all of which must hold: the
centre is named in **this** section as the thing the others meet at; the items are instances of one
kind, not a console plus a policy plus a licence; **taking the centre away stops the illustration
saying anything**; and many-becoming-one is the section's point rather than background. If any one
needs an argument, it is a grid. The third is the test that settles it - three property cards with a
logo in the middle are three property cards.

(Worth recording as a pattern, not just an incident: three attempts at this rule, and the first two
failed in the same way as the keyword rule earlier the same day - swinging to the mirror image of the
problem, then reaching for a mechanism instead of a criterion. Every one of her corrections here was
about **degree**, and what finally worked was making the qualifying conditions narrow enough that the
archetype stops being the easy answer.)

**And the frames are named for the run, not the section.** She deletes the previous set to keep the
page manageable, so what a frame name has to do is tell one run apart from the next: a date-and-time
stamp shared by the whole set, plus a number. The section title is already the illustration's own
Title, and repeating it in the layer name made the list unreadable without helping.


## The style screen was reorganised (2026-09-16)

`3 · Elements` had become a drawer: twenty-five elements in one band, from the page surface to the
character budgets, in the order they happened to be written. The designer's read was right - what is
text, what is an object and what is a distance were mixed together, and finding anything meant
scrolling past everything.

Six bands now, four to eight elements each:

| Band | What is in it |
|---|---|
| 1 · Canvas and spacing | Canvas, safe margin, the gaps between blocks |
| 2 · How much fits | Card counts, the three text budgets, the size floors |
| 3 · Text | The three reading levels, plus stat number, step number, column title, hub description |
| 4 · Surfaces and containers | Page surface, card, divider, pill, connector |
| 5 · Icons | Icon styles, the central hub, and where a card icon sits |
| 6 · Architecture | The arch grammar, untouched |

Nothing moved between files and no value changed: 272 editable values before, 272 after, verified by
comparing the full list the console reports, element by element, against the same list taken before
the move. The element descriptions survived too - they are keyed by the element's own name, not by
the section it sits under, which is why this was safe to do at all.

One judgement call worth recording: **Column header stayed whole in *Text*** rather than having its
title moved to Text and its background to Surfaces. Splitting an element across two bands to satisfy
a category costs more than the category is worth - one rule, one place beats a tidy taxonomy.


## A comparison needs a list, not a stack of pills (2026-09-16)

A two-sided comparison came back with each column's items drawn as a column of pills. The designer
redrew it and the note was exact: **it did not look like a table.** Pills do not work as the resource
in that kind of graphic - a pill is a label for one thing, and three stacked read as three loose
tags, not as one enumeration. She replaced them with a list, gave each item a check mark to say
these are things you get, and carried the column's background down under the list so the items stop
floating on the page surface.

Three things came out of it, all measured from her file rather than invented:

**A List element.** Item text at Body text size, a 35px filled disc with the tick knocked out, 16px
between the check and the text, 26px between items. The item text sits at **full strength** while
the column's description above it stays at the mode's body opacity - the description qualifies the
column, the list is what the column is actually saying, and the brightness difference is what says so.

**A column is two blocks, not one block and some loose items.** Header, a 21px gap, then a body block
carrying the same fill. `Column header bg` became `Column block bg` because both blocks use it. And
the body blocks are the same height across columns even when one holds three items and the other
holds one - the size rule applies here like anywhere else.

**And a rule about what a pill is for.** One pill is a label; several stacked are not a list. Where a
column enumerates what something reaches or includes, that is the List element. In a comparison the
difference is not cosmetic: a column of pills stops the thing reading as a comparison at all.


## The list icon is a vocabulary, not a check (2026-09-16)

Three corrections from a run, and the third is the interesting one.

**A task could not be deleted from where it is shown.** The Prepared tasks section has three views;
the list view and the whole of Task history carried a Delete button and the card view did not. The
wiring was already there - only the button was missing from one renderer.

**The divider's colour and its opacity had drifted into two tables**, so the console showed them at
opposite ends of the element. Same fix as the text levels and the card: one table, the opacity in
the column beside its colour.

**And the check mark was the wrong default.** Every list came back with a check, and the designer's
point is semantic: *a check says everything here is fine*, and half the lists in these articles are
counting costs. The element is now `List icon` rather than `List check` - one style rule covering all
of them - with a vocabulary of six marks from the design system, always in the `circled-filled-bold`
variant: `check` for what you get, `alert` for what is not quite right, `cancel` for what does not
exist, `minus` for what is not allowed, `question` for what is open, and `arr-right` for a neutral
enumeration where no judgement is meant.

Two rules travel with it. **One mark per list** - mixing them turns a list into a salad of symbols
and the reader stops reading the marks at all. But **two columns may carry different marks, and often
should**: `check` on one side against `alert` on the other is what makes a comparison argue, and it
is not mixing, because each list stays consistent with itself.

**The stretched icons were our fault, not the library's.** All six components are 194 by 194, square.
They arrive deformed when the instance is dropped into an auto-layout row that stretches it, so the
rule is now explicit on the Figma route: resize to one number on both axes and leave the layout
sizing FIXED on both - never FILL, never grow.


## The icon library became a dictionary (2026-09-17)

Icons were being chosen from a shortlist of twenty-two names the skill happened to remember, against
a library of 532. That is how a *Kubernetes (OKE)* pill got a `workload` icon and *OCI Load Balancer*
got `network`, while `kubernetes` and `load-bal` sat in the library under exactly those names.

The designer went through the whole set and wrote what each icon depicts. That list is now
`ICON_MEANINGS.md`, and choosing an icon means reading it. The design-system search stays as the
fallback for the rare concept it does not cover; `ICON_INDEX.md`, which listed twenty-four icons and
described the set as holding 131, is retired to `archive/`.

The review that produced it turned up more than descriptions, and two of those findings are worth
keeping:

**Five icons had been renamed in the library without a record**, which would have broken anything
referencing them by name: `notebook` to `laptop`, `radius` to `loginradius`, `rec` to `rec-active`,
`remote` to `remote-app-mark`, plus `recordings` added and `youtube` removed from the group. The
comparison that found them was between the library's own names and a stale copy of them - 531 names
each, 526 identical - and the spreadsheet now carries a *Was* column so the next rename is logged.

**And twenty-three variants across eleven icons carry a transform an instance does not inherit** -
`sx = -1` on the component rather than on the vector inside it, so the artwork is correct on the
canvas and mirrored the moment it is instanced. It affects the directional icons most, where the
direction *is* the meaning: `a-up`, `double-left`, `double-right`, `coll-list`, `exp-list`, `coll-w`,
`exp-w`, `connect`. Three more carry `sx = 0`. This is a library defect, not a spec one, and it is
recorded here because it produced a false report first: the mirrored instances were read as proof
that `double-left` and `double-right` were named backwards, and they are not. Measuring the transform
is what separated the two.
