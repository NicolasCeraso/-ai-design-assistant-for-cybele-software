# Section Illustration Rules — the specification

> **This is the single source of truth for in-article section illustrations.** Everything about how
> one looks — layout, light/dark alternation, colour, typography, cards, connectors, icons — is
> here, and only here. `SKILL.md` carries the process (when to run, how many, what to name the
> files) and points at this file; it deliberately repeats none of these values.
>
> Covers are a different deliverable with its own spec: `BLOG_COVER_RULES.md`.
>
> **Editing this file:** a value belongs in a table, or inside a code fence if it is a worked
> example. The console's style editor turns any number in ordinary prose into an editable
> value, so a number written mid-sentence shows up as a rule nobody can act on. Reasons, measurements
> and history go in `HISTORY.md`.
>
> Assembled 2026-09-04 from the two places these rules used to live: `SKILL.md` Phase 3 and the
> *SVG Blog Illustration Pipeline* section of the project journal, now `archive/PROGRESS.md`. No
> value was changed in the move.

---

## Modes

Every illustration is built in **one** mode. A mode is not a runtime theme switch: it is chosen per
illustration, and a set alternates between them. Everything an element looks like is decided per
mode — its colours and, for icons, its sizes too.

| Mode | What it is |
|---|---|
| Light mode | Pale blue surface, white cards, blue accent. Where a set starts, unless the article says otherwise. |
| Light mode green accent | The light surface in neutral grey, with green as the accent. |
| Blue Mode | A saturated pale-blue surface, for an article that wants more colour than the light modes. |
| Dark mode | The deep navy surface with dark cards and light text. |
| Dark mode green accent | The navy surface with light cards, and green as the accent. |
| Arch | The architecture grammar at section scale. Only the Architecture / flow pattern uses it. |

Every value that varies by mode names its mode in the column: `Light mode`, or `Light mode · bg` when
the element has more than one thing to set. **Adding a mode here gives every such element a slot for
it**, copied from an existing mode so nothing starts empty, and then edited element by element.

---

## 1 · Canvas and spacing

Where the content sits and how far apart its blocks are. Nothing here belongs to one element: these
are the distances the whole composition is laid out to.

Distances, and the frame they sit in. Every other measurement lives with the element it belongs to,
in *Surfaces and containers* below. A distance the generator chose on its own is a defect: that is how one run
rendered the same rule as two different spacings.

Lengths are in px at the canvas size below. **Ratios are in %**, so one rule holds at any size.

### Canvas

| Element | Width | Height |
|---|---|---|
| Canvas | 1920px | 1080px |

### Safe margin

| Element | Top | Right | Bottom | Left |
|---|---|---|---|---|
| Safe margin | 10% | 6.25% | 10% | 6.25% |

**This is where the content begins, and nothing crosses it** — not text, not a card, not a connector,
not a halo, not a background. One margin, not a limit plus a target: the composition is laid out to
these four values.

It is a **percent of the canvas width on all four sides** — not of the side each one sits on. That way
the same number reads as the same distance top, bottom and sides, and the frame survives a change of
canvas size. Sides are given top / right / bottom / left, so the top can breathe more than the bottom
without touching the others.

### Gaps between blocks

Think of each pair as one vertical auto-layout frame, because on the Figma route that is literally
what it is. Each number is the gap between the two blocks:

| Element | Gap |
|---|---|
| Body text title → Body text | 10px |
| Hub → its description | 24px |

The whole table is binding, including rows added to it later.

**How to apply a gap, per route:**

- **Figma** — the two texts sit in one vertical auto-layout frame and the gap is its `itemSpacing`.
  Nothing to compute.
- **SVG** — there is no auto-layout, so the generator converts the gap into baseline positions once,
  using the line-box model this spec assumes (a line occupies 1.25 × its font size, and its baseline
  sits 1.0 × font size below the top of that box):

  ```
  first body baseline = last title baseline + 0.25 × title size + gap + 1.0 × body size
  ```

  Compute it from the tables every run and round to whole px. Never carry the result over as a
  constant: it stops being true the moment a size or the gap changes, and the only numbers that are
  rules are the ones in the tables.

---

## 2 · How much fits

How many pieces an illustration may hold and how much text each may carry. These are the values that
stop content bending to a layout — the size of a box follows its text, so what has to be bounded is
the text.

### How many cards, and how much text

**The limit is the text, not the box.** The card is free to be whatever size its content needs, so
the thing that has to be bounded is the content — and bounding the text is what keeps a set looking
like one system without ever trimming a concept to fit a rectangle.

| Element | Fewest | Most |
|---|---|---|
| Cards in one illustration | 2 cards | 6 cards |

**The budget follows how many cards sit across a row, not how many the illustration holds.** Four
cards in a two-by-two have the same width as two cards — what shrinks a card is the column count, so
that is what the bands are keyed to. A single full-width row reads like the widest band.

| Element | Cards across a row | Card title | Card description |
|---|---|---|---|
| Text budget · wide card | 1, 2 or 3 | 34 chars | 90 chars |
| Text budget · medium card | 4 | 28 chars | 70 chars |
| Text budget · narrow card | 5 or 6 | 16 chars | 35 chars |

A description also has a floor — it is one or two short phrases saying what the thing does and why it
matters, so a three-word description is as wrong as an overlong one. And the cards of one
illustration have to be **roughly the same length**: one card carrying three times the text of its
neighbour reads as a mistake before it reads as emphasis.

| Element | Shortest description | Longest vs shortest, same illustration |
|---|---|---|
| Card | 16 chars | 200% |

**What to do when a concept does not fit its budget — never trim the meaning.** In this order:

1. Use fewer cards. Fewer cards is a larger budget, and most overflows are really a set that was
   split too finely.
2. Change the pattern. A concept that needs a paragraph is usually not a peer in a grid.
3. Split the section into two illustrations.

Cutting the sentence until it hits the count is the failure this rule exists to prevent: it produces
a card that reads like a label and explains nothing, which is how a description ends up being about
something other than its own title.

**More than the maximum is two illustrations, not a smaller card.** And fewer than the minimum is not
an illustration at all — one card is a sentence with a border around it.

### Card size floors

The one exception is a **floor**, and it is a floor rather than a size: below it the composition is
reflowed — fewer columns, or the section split — instead of squeezed.

| Element | Min width | Min air between cards | Padding | Icon → card title |
|---|---|---|---|---|
| Card | 300px | 32px | 28px | 36px |

## 3 · Text

**The three text levels, in order.** An illustration has exactly **one Title** and **no subtitle**.
Below it comes the body text, and the body text has its own title — that title belongs to the body
text, not to the illustration. Anything not on this list is not a text level; a label that belongs to
an element, like the central hub's description, lives with that element in *Surfaces and containers*.

1. **Title** — the title of the illustration. One per illustration, never two, max 6 words.
   - **It says what *this* section claims**, in the article's own terms. Not the section heading
     copied, and not a slogan about the product.
   - **No two titles in a set share a grammatical shape.** Two illustrations that open "One platform,
     any cloud" and "One image, every store" are one title written twice: same rhythm, same claim,
     same comma. When the second one falls into the shape of the first, the second was not written —
     it was cast in the same mould, and that is usually the sign that the layout was too.
   - **It may not point at something the illustration does not show.** "Both", "these", "the two",
     "either side" are pointers; the reader follows them and finds nothing. *"Both models come from
     one platform"* over three property cards sends her looking for two models that are not drawn —
     and the phrase came straight out of the article, where it had been defined twenty paragraphs
     earlier. Either the thing is on the illustration, or the title does not name it.
2. **Body text title** — the title of a body-text block. Several per illustration, one per block.
   It is **not** a subtitle of the illustration.
3. **Body text** — the running text. The second reading level: what it does and why it matters.

Each level carries all of its own variables — a colour per mode, then font, weight and size:

| Element | Light mode · colour | Light mode · opacity | Arch · colour | Arch · opacity | Light mode green accent · colour | Light mode green accent · opacity | Blue Mode · colour | Blue Mode · opacity | Dark mode · colour | Dark mode · opacity | Dark mode green accent · colour | Dark mode green accent · opacity | Font | Weight | Size |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Title | `#373737` | 100% | `#373737` | 100% | `#373737` | 100% | `#021425` | 100% | `#FFFFFF` | 100% | `#FFFFFF` | 100% | Inter | Regular 400 | 75px |
| Body text title | `#373737` | 100% | `#373737` | 100% | `#373737` | 100% | `#021425` | 100% | `#FFFFFF` | 100% | `#021425` | 100% | Inter | Regular 400 | 43px |
| Body text | `#515151` | 100% | `#515151` | 100% | `#515151` | 100% | `#2B4051` | 100% | `#FFFFFF` | 80% | `#2B4051` | 100% | Inter | Regular 400 | 38px |

**Each colour carries its own opacity, in the column beside it.** They are two variables, not one:
the colour says which ink, the opacity says how much of it. Kept apart, a mode can be softened
without inventing a new hex that only looks right against one background — and the two stay
adjustable from the console without either one hiding inside the other.

- The opacity **multiplies** the colour in the column to its left; it never replaces it.
- **Figma** — set it on the text node's **fill**, not on the layer, so a group or an effect applied
  later does not compound it.
- **SVG** — `fill-opacity` on the `<text>`, for the same reason: `opacity` on the element would fade
  anything nested inside it too.

**These numbers are the rule, not a suggestion.** Before delivering, list the distinct size/weight
pairs in the file and check each one against the table — a pair that is not here is a defect, not a
variation.

- **The only weights that exist are the ones the tables declare** — today Regular, Medium and
  SemiBold, with Medium appearing only where a table says so: the stat card's display number, and
  the diagram label in *Architecture pieces*. Everywhere else it is Regular or SemiBold. Never
  invent a numeric weight because a label reads a certain way; the number belonging to each weight
  is in the table beside it.
- Never italic, never lighter than Regular.
- Title max **6 words**.
- Body text: 1–2 short sentences (what it does + why it matters).

---

### Stat number

A card whose subject **is** a number — a percentage, a multiplier, a count — with a line under it
saying what the number counts. The number is the content, not a decoration on a normal card, so it
gets its own size and its own weight.

| Element | Font | Weight | Size | Light mode · colour | Arch · colour | Light mode green accent · colour | Blue Mode · colour | Dark mode · colour | Dark mode green accent · colour |
|---|---|---|---|---|---|---|---|---|---|
| Stat number | Inter | Medium 500 | 74px | `#373737` | `#373737` | `#373737` | `#021425` | `#FFFFFF` | `#FFFFFF` |

- The line beneath it is ordinary **Body text**, and it carries the same budget as a card
  description.
- **The number is not a title.** An illustration still has exactly one Title, above the cards.
- A stat card holds one number. Two numbers in one card is two cards.
- **It is round, and like every card its size follows the row** — there is no fixed diameter. It
  takes the card fill and opacity from *Card*, which is where the translucent surface the reference
  uses for these comes from.
- The number is **centred**, and so is the line under it. It is the one card that is not
  left-aligned, because a number read off-centre in a circle looks like a mistake.

### Step number

The number on a card in the **Ordered steps** pattern — the thing that makes the order visible,
which is the whole reason that pattern exists.

| Element | Font | Weight | Size | Size when it is the only graphic element | Light mode · colour | Arch · colour | Light mode green accent · colour | Blue Mode · colour | Dark mode · colour | Dark mode green accent · colour |
|---|---|---|---|---|---|---|---|---|---|---|
| Step number | Inter | Medium 500 | 36px | 67px | `#0B84F4` | `#0A74D6` | `#3DCCA1` | `#007DC1` | `#0B84F4` | `#3DCCA1` |

- **A step card carries a number or an icon, never both.** They do the same job — saying where you
  are in the sequence — so together they compete and the eye has to choose. Pick one per
  illustration and use it on every card.
- **When the number is the only graphic element on the card**, it takes the larger size. With nothing
  else to carry the composition the number stops being an annotation and becomes the design, and at
  the small size it reads as a footnote to its own card.
- **Icons instead of numbers only works in a single row read left to right.** The moment the steps
  wrap to a second row the direction stops being obvious, and then the numbers are not optional.
- **One form, and it is the bare digit** — `1`, not `01` and not `1.`. The reference illustrations
  used three different treatments for the same thing across two articles, which is exactly the kind
  of drift a rule prevents.
- **The number sits in a column of a fixed width, so every card title shares one left edge.** A `1`
  is narrower than a `4`; let the number size itself and each title starts a few pixels from where
  the one above it started, which reads as sloppiness rather than as a decision.

| Element | Column width |
|---|---|
| Step number | 56px |
- Only the Ordered steps pattern has them. A number on a grid card claims an order that is not there.

### Column header

What names a whole column in a **Two sides** comparison, and the reason the reader can tell the two
apart before reading a word. It is a **title, a subtitle, and the surface they sit on** — and it
reads as an intermediate level between the illustration's Title and a card title.

| Element | Font | Weight | Size | Light mode · colour | Arch · colour | Light mode green accent · colour | Blue Mode · colour | Dark mode · colour | Dark mode green accent · colour |
|---|---|---|---|---|---|---|---|---|---|
| Column title | Inter | SemiBold 600 | 43px | `#0A74D6` | `#0A74D6` | `#238568` | `#007DC1` | `#0B84F4` | `#3DCCA1` |

| Element | Light mode · fill | Arch · fill | Light mode green accent · fill | Blue Mode · fill | Dark mode · fill | Dark mode green accent · fill |
|---|---|---|---|---|---|---|
| Column block bg | `#FFFFFF` | `#FFFFFF` | `#FFFFFF` | `#EFF9FF` | `#112232` | `#EFF9FF` |

| Element | Gap |
|---|---|
| Header block to body block | 21px |

- The **subtitle under it is ordinary Body text**, one line, directly below the title and inside the
  same surface. It qualifies the column; it is not a second title.
- The header **spans the column**, and its surface is what makes the grouping visible. Without it the
  two headers float and the comparison loses its two halves — which is what happened the first time
  this was drawn.
- **A column is two blocks on the same fill, not one block and some loose items**: the header, a gap,
  and a body holding whatever the column contains. The body block carries the fill too, so nothing
  inside it floats on the page surface. The two blocks of every column are the same width, and the
  body blocks are the same height across columns even when one holds fewer items — the size rule in
  *Surfaces and containers* applies here like anywhere else.
- **Either every column has one or none does.** A single labelled column is a card title in the
  wrong place.
- In a grid of peers there is nothing for it to name.

### List

What a column uses to enumerate: what something reaches, includes, covers, or costs. Each item is a
**check mark and a line of text**, stacked. It is the element a comparison needs, and it is what
replaced a stack of pills, which read as scattered tags rather than as one list.

| Element | Font | Weight | Size | Light mode · colour | Arch · colour | Light mode green accent · colour | Blue Mode · colour | Dark mode · colour | Dark mode green accent · colour |
|---|---|---|---|---|---|---|---|---|---|
| List item | Inter | Regular 400 | 38px | `#373737` | `#373737` | `#373737` | `#021425` | `#FFFFFF` | `#021425` |

| Element | Size | Light mode · colour | Arch · colour | Light mode green accent · colour | Blue Mode · colour | Dark mode · colour | Dark mode green accent · colour |
|---|---|---|---|---|---|---|---|
| List icon | 35px | `#0B84F4` | `#0A74D6` | `#3DCCA1` | `#007DC1` | `#0B84F4` | `#3DCCA1` |

| Element | Check to text | Between items |
|---|---|---|
| List | 16px | 26px |

**The icon is always a filled disc with its mark knocked out of it** — the `circled-filled-bold`
variant of the Cybele Design System component, never an outline and never a bullet. Which mark it is
carries meaning, and a check is not the neutral choice: a check says *this is fine*, and half the
lists in these articles are counting costs.

| Mark | What it says |
|---|---|
| `check` | This is right, this is included, you get this |
| `alert` | Look at this — something here is not quite right |
| `cancel` | This does not exist, or it is badly wrong |
| `minus` | This is not allowed |
| `question` | This is an open question |
| `arr-right` | Neutral. Use it when the list is simply an enumeration and no judgement is meant |

- **One mark per list.** Mixing them inside a single list turns it into a salad of symbols, and the
  reader stops reading the marks at all. Mix only where the difference itself is the point, and even
  then think twice.
- **Two columns may carry different marks, and often should.** `check` on one side and `alert` on the
  other is what makes a comparison argue — and it is not mixing, because each list stays consistent
  with itself.
- **The disc is square and stays square.** The components are 194 by 194; an instance is resized to
  one number on both axes and never allowed to fill or grow inside an auto-layout row. A list icon
  that arrived stretched is this rule broken, not a bad icon.
- The tick, or whatever mark it is, is the whole reason the list beats a run of pills: a pill is a
  label for one thing, and three pills stacked look like three loose tags.
- **A list item is one line.** If it needs two it is a card with a description, not a list item.
- The item text sits at full strength, brighter than the description above it: the description
  qualifies the column, the list is what the column is actually saying.

### Central hub description

The short label under the central hub — "Golden Image" in the reference. It belongs to the hub, not
to the reading hierarchy, which is why it is here and not among the three text levels.

| Element | Font | Weight | Size | Light mode | Arch | Light mode green accent | Blue Mode | Dark mode | Dark mode green accent |
|---|---|---|---|---|---|---|---|---|---|
| Central hub description | Inter | SemiBold 600 | 43px | `#373737` | `#373737` | `#373737` | `#021425` | `#FFFFFF` | `#FFFFFF` |

- **Centred under the hub**, always. The distance between them is the `Central hub → description`
  `Hub → its description` gap in *Canvas and spacing*.
- One line. If it needs two, the label is doing the job of a body text title and should be one.

## 4 · Surfaces and containers

The solid parts: what the content sits on, what it sits in, and what joins it. Each carries its own
colours per mode.

### Page surface

| Element | Light mode | Arch | Light mode green accent | Blue Mode | Dark mode | Dark mode green accent |
|---|---|---|---|---|---|---|
| Page surface | `#EFF7FE` | `#F0F7FE` | `#F2F2F2` | `#99DBFF` | `#021425` | `#021425` |

- **Alternation across a set is mandatory.** Never the same mode twice in a row.
- **Surfaces are flat.** No background gradients anywhere in a section illustration.

### Card

| Element | Radius | Light mode · fill | Light mode · opacity | Arch · fill | Arch · opacity | Light mode green accent · fill | Light mode green accent · opacity | Blue Mode · fill | Blue Mode · opacity | Dark mode · fill | Dark mode · opacity | Dark mode green accent · fill | Dark mode green accent · opacity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Card | rx="4" | `#FFFFFF` | 100% | `#FFFFFF` | 100% | `#FFFFFF` | 100% | `#EFF9FF` | 100% | `#112232` | 100% | `#EFF9FF` | 100% |
| Highlighted card | rx="4" | `#FFFFFF` | 100% | `#FFFFFF` | 100% | `#FFFFFF` | 100% | `#EFF9FF` | 100% | `#112232` | 100% | `#EFF9FF` | 100% |

- **Flat solid fill**, no internal gradients.
- A card takes its colour from this table, not from decoration.
- **A card may be plain: no fill at all, and no padding**, with the icon, title and description
  sitting directly on the page surface. Several of the reference illustrations are built that way,
  and it is not a lesser version — it is the compact form. A plain card is what makes two rows of
  three fit inside the safe margin, where filled cards of the same content do not. Use it when the
  illustration needs the height; use a filled card when the grouping has to be unmistakable.
- **Each fill carries its own opacity, in the column beside it** — the same pair as the text levels
  in *2 · Text*. It multiplies the fill; it never replaces it. On the Figma route it goes on the
  frame's **fill**, not on the layer, so the text and icons inside keep their own; on the SVG route
  it is `fill-opacity` on the `<rect>`, never `opacity`, which would fade the contents with it.

**A card has no fixed width and no fixed height, and giving it one would be a defect.** The card
follows the text, never the other way round: it is as tall as its own content needs and as wide as
the composition allows, so a concept that takes two sentences to explain gets two sentences. The same
goes for how many columns a set of cards uses — that follows the item count, which follows the
article. The numbers that are rules in this spec are the ones that keep a *set* looking like one
system: the margin, the gaps between blocks, the type, the colours, the radius, the icon sizes.

**Within one illustration, every box of the same kind is the same size.** This is the other half of
the rule above and it is not in tension with it: the content decides the size, and then **one**
size is decided — set by the box that needs the most room, whether that is the most important text
or simply the hardest to fit — and every other box of that kind takes it. Three text boxes at three
sizes read as three different kinds of thing; the reader goes looking for what the difference means
and there is nothing there. The size is free between illustrations and fixed inside one.

This is the same rule the architecture pattern already states for its pill, written once for
everything: cards, text boxes, pills, zones, stat circles.

### Divider line

The rule between stacked items inside a column. It is what keeps a column reading as a list of
separate things rather than one run of text.

| Element | Width |
|---|---|
| Divider line | 2px |

| Element | Light mode · colour | Light mode · opacity | Arch · colour | Arch · opacity | Light mode green accent · colour | Light mode green accent · opacity | Blue Mode · colour | Blue Mode · opacity | Dark mode · colour | Dark mode · opacity | Dark mode green accent · colour | Dark mode green accent · opacity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Divider line | `#0A74D6` | 20% | `#0A74D6` | 20% | `#238568` | 20% | `#007DC1` | 20% | `#FFFFFF` | 20% | `#FFFFFF` | 20% |

- It separates items **within** a column. It never boxes a card and never runs between columns --
  the gap already does that.
- The opacity is what keeps it a rule and not a border: at full strength it competes with the text
  it is separating.

### Pill or chip

| Element | Radius | Font | Weight | Size | Light mode · bg | Light mode · text | Arch · bg | Arch · text | Light mode green accent · bg | Light mode green accent · text | Blue Mode · bg | Blue Mode · text | Dark mode · bg | Dark mode · text | Dark mode green accent · bg | Dark mode green accent · text |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Pill or chip | rx="4" | Inter | Regular 400 | 38px | `#C7EBFF` | `#0B84F4` | `#C7EBFF` | `#0B84F4` | `#C0EFE1` | `#238568` | `#C7EBFF` | `#007DC1` | `#0B84F4` | `#FFFFFF` | `#99DBFF` | `#021425` |

- A pill is a label, not a button: no border, no shadow, no icon inside.
- **One pill is a label. Several stacked are not a list.** Where a column enumerates what something
  reaches or includes, that is the **List** element — check mark and text, on the column's own
  block. A column of pills reads as scattered tags and, in a comparison, stops the thing reading as
  a comparison at all.

### Connector

| Element | Stroke | Arrowhead width | Arrowhead depth |
|---|---|---|---|
| Connector | 36px | 67px | 34px |

- The arrowhead is a separate `<polygon>` triangle, filled — **wider than deep**, which is what those
  two numbers say.
- Direction: **straight lines from closest lateral edge → hub**.
- No decorative lines — every connector must carry meaning.

**An arrowhead is a claim about direction, and it has to be true.** Something moves, and it moves
that way: a session reaching a gateway, a step following the one before it.

**Where nothing moves, there is no connector at all — not a headless line.** A bar running from a
card to the centre with nothing on either end states nothing and decorates nothing; it is an arrow
someone stopped drawing halfway, and the reader spends a moment deciding which it was meant to be.
Either the connector says which way something goes, or it is not there. Belonging is shown by
proximity and arrangement, which is what a hub is for.

| Pattern | Connector |
|—-|—-|
| Architecture / flow | Arrow. Something travels, and which way is the point |
| Ordered steps | Arrow, or nothing — the numbers already carry the order |
| Hub | **Nothing.** A property does not flow into the thing it is a property of |
| Grid, Two sides | Nothing. Peers are not connected to each other |

*"One console and one image strategy" with an arrow into the platform* says the console arrives from
somewhere and enters it. It does not: it is what the platform **is**. And when the title said those
things came **out of** the platform while every arrow pointed **into** it, one of the two was lying
— which a reader notices long before she works out which.

## 5 · Icons

Which icon, at what size, in what colour — and where it sits on the card it belongs to.

### Icons

**The icon is the measurement.** A background is optional: when a mode asks for one it is padding
around the icon, so a mode with no background reserves no space for one — there is no invisible box
for the layout to work around.

**An icon style is decided per mode, all of it** — its size as much as its colours. A mode that drops
the background usually wants a different icon size than one that keeps it.

| Icon style | Light mode · icon min | Light mode · icon max | Light mode · bg padding | Light mode · bg (fill) | Light mode · icon | Arch · icon min | Arch · icon max | Arch · bg padding | Arch · bg (fill) | Arch · icon | Light mode green accent · icon min | Light mode green accent · icon max | Light mode green accent · bg padding | Light mode green accent · bg (fill) | Light mode green accent · icon | Blue Mode · icon min | Blue Mode · icon max | Blue Mode · bg padding | Blue Mode · bg (fill) | Blue Mode · icon | Dark mode · icon min | Dark mode · icon max | Dark mode · bg padding | Dark mode · bg (fill) | Dark mode · icon | Dark mode green accent · icon min | Dark mode green accent · icon max | Dark mode green accent · bg padding | Dark mode green accent · bg (fill) | Dark mode green accent · icon |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Icons | 79px | 79px | 65% | none | `#0B84F4` | 46px | 46px | 0% | none | `#373737` | 79px | 79px | 65% | none | `#3DCCA1` | 53px | 65px | 65% | `#99DBFF` | `#007DC1` | 79px | 79px | 65% | none | `#0B84F4` | 53px | 65px | 65% | `#99DBFF` | `#021425` |
| Central hub | 105px | 105px | 65% | `#0B84F4` | `#FFFFFF` | 105px | 105px | 65% | `#0B84F4` | `#FFFFFF` | 105px | 105px | 65% | `#3DCCA1` | `#FFFFFF` | 105px | 105px | 65% | `#007DC1` | `#FFFFFF` | 105px | 105px | 65% | `#0B84F4` | `#FFFFFF` | 105px | 105px | 65% | `#3DCCA1` | `#FFFFFF` |

- **icon min / max** measures the icon itself, in that mode. The layout picks within the range —
  tighter cards take the minimum — and every icon of that style in one illustration uses the same size.
- **bg padding** is a percent of the chosen icon size, added on every side, so a background scales
  with the icon it sits behind. A mode whose background is `none` ignores it.
- **bg** holds a colour, or `none` for a mode that draws no background at all: the icon then stands
  on the card or the surface.
- The five values of a mode are one decision, taken together.
- The icon is **centred on both axes**, always.
- A new icon style is a new row. A new mode adds its five columns to every row.
- **`(fill)` in a column header** means the value may be a colour or `none`. Elsewhere a colour
  column is a colour, and `none` would be a value nothing knows how to draw.

### Card icon placement

**Where the icon sits is decided by the card, not by taste.**

| Element | Where it sits | When | Size |
|---|---|---|---|
| Card icon · inline | Left of the whole text block | The default. The card is wide enough to carry the icon beside the text | 65px |
| Card icon · stacked | Above the text block | The card is narrow — four or more columns across | 65px |
| Card icon · hero | Above the text block | The illustration has two or three cards and the icon carries the composition | 99px |

**Inline means left of the title *and* the description, not just the title.** The icon sits in its
own column, vertically centred against the whole text block; the title and the description share one
left edge to the right of it. The wrong version — icon beside the title, description starting back
at the card's edge underneath both — breaks that edge and leaves the description belonging to
nothing in particular.

```
wrong                          right
[icon] Title                   [icon]  Title
Description runs back here             Description lines up under the title
```

An icon above the title costs roughly the icon's height plus the gap in card height, which is why it
is the narrow-card form: two rows of cards with the icon on top do not fit inside the safe margin.

## 6 · Architecture

Only the Architecture / flow pattern draws these, and only in the `Arch` mode.

### Architecture pieces

Only the **Architecture / flow** pattern draws these, and only in the `Arch` mode — which is why
their tables carry that one column. They are the `thinfinity-architecture` grammar at section scale:
that spec sizes a diagram to its own canvas, with type small enough for a dense topology, and a
section illustration is a fixed canvas at the size in *Canvas and spacing* — so every length here
is **that grammar doubled**.

| Element | Width | Height | Radius | Border | Arch · fill |
|---|---|---|---|---|---|
| Diagram pill | 320px | 86px | rx="14" | 3px | `#FFFFFF` |

**One pill size. Do not vary it** — that rule is the whole reason the grammar reads as a system. A
pill whose label needs two lines keeps its size; the label breaks instead.

Category is communicated **only** by the border and the text on it, never by a tinted fill:

| Element | Arch · border | Arch · text |
|---|---|---|
| Pill · Thinfinity | `#0A74D6` | `#0A74D6` |
| Pill · User | `#373737` | `#373737` |
| Pill · Secondary | `#BDBDBD` | `#373737` |

| Element | Font | Weight | Size | Icon | Arch · colour |
|---|---|---|---|---|---|
| Diagram label | Inter | Medium 500 | 25px | 46px | `#373737` |

| Element | Radius | Border | Dash | Arch · border | Arch · label |
|---|---|---|---|---|---|
| Zone | rx="22" | 3px | 12 8 | `#BDBDBD` | `#373737` |

- A **zone** is a dashed container grouping pills that share a context — a network, a DMZ, a tier.
  Transparent: it never carries a fill of its own.
- Its label sits at the **top-left inside** the zone, icon then text, and the pills start below it.

| Element | Stroke | Arrowhead width | Arrowhead depth | Arch · colour |
|---|---|---|---|---|
| Diagram connector | 4px | 36px | 28px | `#0A74D6` |

- The arrowhead is a **chevron**, drawn as a stroked path — not the filled triangle the blog
  connector uses. Two different elements on purpose: one is a thick editorial arrow, the other has to
  stay legible beside a diagram label.
- Straight runs only, from the closest lateral edge. Never a long arrow across empty canvas.

| Element | Gap |
|---|---|
| Between containers | 86px |

**Completeness beats composition, and this is where the two specs disagree on purpose.** The
editorial rules below prefer symmetry and a full canvas; an architecture answers to the article
instead. If it names four host locations, four are drawn, however lopsided that leaves the frame. A
diagram that balances by dropping a node is not a tidier diagram, it is a false one.

**When the topology does not fit**, in this order — and never by dropping a node:

1. Stack a zone's pills into a column instead of a row. Four hosts read fine stacked; that is what
   the reference examples do.
2. Split the section into two illustrations, each a complete part of the path, and say so in the
   run notes.
3. Report that it does not fit, and why. A run that says "this needs two illustrations" is useful;
   one that quietly drew three of the four hosts is a defect nobody will notice until it is published.

**What this pattern does NOT take from `thinfinity-architecture`:** its canvas (a white card on a
pale page, sized to the content), its own title treatment, and the **mandatory `REFERENCIA` footer**.
Here the frame is a section illustration — canvas, safe margin, title and page surface come from this
spec — and the article's own text explains what the arrows mean, so the legend is dropped.

## What an illustration has to add

**An illustration that repeats the article is not an illustration, it is the same paragraph in a
different typeface.** If a section carries a numbered list and the illustration draws that list as
cards, nothing was added: the reader already had those items, in that order, a few lines above.

Two rules that sound contradictory and are not:

- **The facts come from the article.** Nothing invented — see *Section editorial rules*.
- **The arrangement is the reading.** That is what the illustration contributes.

An illustration adds a **relation**, not a fact: something the prose had to say one item at a time,
which the drawing says at once. What a drawing can carry and a paragraph cannot:

| | What it does that prose cannot |
|---|---|
| Simultaneity | Prose says "and also, and also"; a drawing says "all at once" |
| Proportion | Prose gives every item its own paragraph, so they look equal. A drawing can show that one is the point and the rest are detail |
| Containment | That these belong inside that — prose can only assert it |
| Direction and cause | Prose says "because"; a drawing shows which way it runs |
| Absence | Prose rarely says "and here there is nothing". A drawing can show the hole |

**Before composing, write one sentence: what does this image show that the paragraph does not?** If
the sentence is "it shows the four items", there is no illustration in that section — and it goes to
the discarded list even if it is important and even if it is easy to draw.

**A table the article already prints is the clearest case of this.** Redrawing two of its rows in
bigger type adds nothing: the reader has just read them, in a layout built for exactly this
comparison. If a table genuinely needs an illustration, it is because something about the *shape* of
the comparison is worth showing — and then it is drawn **whole**. Dropping one of its three columns
to fit two side by side is the content bending to the layout, which is the failure this whole section
exists to prevent.

**Before delivering, cover every word on the illustration and look at what is left.** If removing the
labels leaves no claim — no hierarchy, no inside, no direction, no asymmetry — it was a list in a
nicer typeface. The arrangement has to mean something on its own.

This raises the bar on purpose, and it has a consequence worth stating out loud: **some articles will
not yield the number of illustrations that was asked for.** A section can carry the argument, have a
drawable shape, and still not deserve an image because the image would only repeat it. Say so and
deliver fewer. Never pad the set.

## Layout patterns (the content chooses one)

**A pattern is not a styling choice. Each one makes a claim about how the items relate**, and a
pattern that does not match the content makes the illustration state something false. Four steps of a
process drawn as a symmetric grid say *"these are interchangeable and there is no order"* — which is
not a looser version of the truth, it is the opposite of it.

So the order of work is: read the section, **name the shape of its information**, then take the
pattern that shape owns.

| The information is… | Pattern | What the figure claims |
|---|---|---|
| A sequence — steps in time, or stages that only work in order | Ordered steps | These happen in this order, and the order is part of the meaning |
| Two options weighed against each other | Two sides | These are alternatives; read across to compare them |
| One thing and its parts, or a centre everything else depends on | Hub | Everything here belongs to, or reaches, that centre |
| Peers — items of equal rank that answer the same question | Grid | These are of equal weight and in no particular order |
| A path, a topology or a perimeter — who talks to whom, and which way | Architecture / flow | This is the real shape of the system. Drawn in the `Arch` mode, with the pieces in *Architecture pieces* |

**In Two sides, the dimension is named once and the sides carry only what differs.** If the same
card title appears in both columns, the comparison has been written twice and half the image is an
echo — and because the icon comes with the title, the icon repeats too. At a glance that does not
read as a comparison at all: it reads as a mistake, as though the same block had been pasted twice.
The dimension belongs above or between the two sides; what sits on each side is the answer, and any
icon there says something about **that** answer.

**The Hub is the rare pattern, and the product mark can be its centre.** The archetype is good and
it is meant to be used. What it cannot be is *available*: every article here is about the same
platform, so a hub with the mark in the middle fits every one of them, and a composition that fits
everything distinguishes nothing.

The fix is not to count how recently it was used — two articles in a row may both deserve it. It is
that the conditions are strict, and most sections simply do not meet them. **All four have to hold.**

1. **The centre is named in this section**, as the thing the others meet at — not merely present
   somewhere in the article.
2. **The items are instances of one kind.** Three clouds, two delivery models, four client types. A
   console, a security model and a licence are three different kinds of thing: that is a list.
3. **Take the centre away and the illustration stops saying anything.** This is the test that settles
   it. If the items still hold up on their own, they were peers and the centre was decoration —
   three property cards with a logo in the middle are three property cards.
4. **Many-becoming-one is the section's point**, stated there, not background the article mentions
   elsewhere.

**If any one of them needs an argument to hold, it is a grid.** Grids and ordered steps carry most
sections; the hub is what is left when a section is genuinely about convergence.

**The centre of a Hub sits in the middle of its items.** It is what the word means, and it settles
the reading order by itself. A centre pushed to one side with every item on the other is not a hub:
it is a list with a logo beside it, and the eye reads the logo first and then travels backwards
through the items — which is the one direction no composition should ask for.

**Name the shape out loud before choosing.** The run notes say which it is — "this section is a
sequence of four stages", "these are four peer properties of the platform". A shape that cannot be
named is a section that is probably not illustrable, and saying so is a better outcome than a grid.

**A shape may not borrow another shape's pattern.** In particular: **if the order matters, the order
has to be visible** — numbered, or running in one direction. A sequence laid out in a two-by-two
grid has no reading order at all; nobody can tell whether it goes across or down.

**Symmetry is a tie-breaker inside a chosen pattern, never a reason to choose one.** Once the
pattern is settled, balance the composition however it reads best. It is not a criterion for picking
the pattern, and it never outranks the shape of the content.

**Two illustrations in the same article may not use the same pattern.** If they converge, one of the
two was not chosen — it was inherited. Go back to the shape of the second section and name it again.

**Four is not a target.** Every pattern above works at the size the section actually has. A section
with three ideas gets three; one with six gets six, or gets split. Padding to four invents content
and trimming to four drops it, and both have happened.

**The content is not trimmed to fit the pattern** — the pattern is chosen to fit the content. When
it does not fit, in this order, and never by dropping or merging an item:

1. Change the pattern to one the content actually has the shape of.
2. Split the section into two illustrations, each complete, and say so in the run notes.
3. Report that it does not fit, and why. A run that says "this section needs two illustrations" is
   useful; one that quietly drew four of the six is a defect nobody notices until it is published.

## Icons (section illustrations)

**A brand mark keeps its own colours.** HTML5, AWS, Azure, Oracle and the like are recognised by
their colour, and repainting one costs the reader the half-second of recognition that was the only
reason to use it. Everything else takes the icon colour its mode declares.

### Which icon

**Open `ICON_MEANINGS.md` and choose from it. Never choose from memory.** It lists every icon in
the library with what it actually depicts, written by the designer from the components themselves.
It is the first stop and it answers almost everything; the design-system search is the fallback for
the rare concept it does not cover.

**The label names the icon.** Look for the words already written on the pill or the card, the literal
noun first: a pill that says *Kubernetes (OKE)* looks up `kubernetes`, one that says *OCI Load
Balancer* looks up `load-bal`. Only when nothing matches is it a question of judgement, and then the
search is for the **function** the thing performs, never for a brand.

The failure this rule exists for: a run drew *Kubernetes (OKE)* with a `workload` icon and *OCI Load
Balancer* with a `network` icon, while `kubernetes` and `load-bal` were both in the library under
those very names. Nothing was wrong with the naming — the run chose from a short list it remembered
instead of reading the one in front of it.

- **The names differ between the two sources.** The repo's SVG set calls it `load-balancer.svg`; the
  Figma library calls it `load-bal`. `ICON_MEANINGS.md` carries the **Figma** names.
- If you do fall back to `search_design_system`: it takes **one query per call**, and a batch of
  several is silently clamped to the first.
- **An icon whose name has nothing to do with the words on its pill is a defect**, not a stylistic
  choice. If nothing in the file fits, say which concept had no icon in the run notes.

**Where the icon comes from depends on the output route.** At what size and in what colour is decided
here for both; only the source differs:

| Route | Source |
|---|---|
| Built in Figma | An **instance of the matching Cybele Design System component** in that Figma file — variant `light`. It stays linked to the library, so a design-system change reaches the illustration. Never a hand-drawn icon, and never the repo's icon paths pasted in as loose vectors. |
| SVG file | The Cybfont set in this repo, embedded as native `<path>` data — the order below. |

Everything from here down is the SVG route.

**The Cybfont set is in this repo.** Look for it in this order and use the first that exists:

1. `../thinfinity-architecture/icons/` — 131 Cybfont SVGs, the same set, bundled beside this skill
2. an `icons/` folder inside this skill
3. `$CYBELE_ICONS_DIR/`, when that variable is set and the path exists
4. Cybfont via the Figma API

**Drawing icons from primitives is the last resort, not a shortcut.** Only if all four fail: say so,
then either ask for the SVGs or build simple geometric icons — and state in `NOTES.md` which. An
illustration whose icons were invented while the set was sitting in the repo is a defect.

- Extract `viewBox` + inner `<path>`/`<g>` content
- Recolor by replacing `fill` attribute values via regex
- Embed inside `<g transform="translate(x,y)"><svg viewBox="..." width="..." height="...">`
- Must represent FUNCTION, not brand
- Pick by what it depicts, from `ICON_MEANINGS.md`

**The whole library, with what each icon depicts, is `ICON_MEANINGS.md`.** Choose from there. The
handful of names that past articles happened to reuse are not a menu, and picking from a remembered
shortlist instead of reading the file is how a Kubernetes pill ends up with a workload icon.

## Section editorial rules

1. **Light/dark alternation** is mandatory across the set
2. **Every card should have a subtitle/description** — not just a title, and **the description has
   to be about that card's own title.** Both halves come from the same passage of the article: the
   title names what the passage is about, the description says what it does or why it matters *there*.
   A description that is true of the article but not of its own title is the tell that content was
   shuffled to fill a slot — a card headed "No inbound ports" once carried "Roles mapped to the exact
   apps a job needs", which is a different subject and, as it turned out, in no part of the article.
3. **Every word on the illustration is in the article.** Titles, card titles, descriptions, labels.
   Not paraphrased from the topic, not filled in from what the product generally does, not invented
   to round out a card — traceable to a passage. This is the one rule whose breach is invisible in
   the design review and obvious to a reader who knows the subject.
4. **And every word has to work with the article covered.** Traceable is not the same as
   self-contained: the illustration is met on its own, halfway down a scroll, without the paragraph
   that set it up. A phrase the article had defined pages earlier arrives on the image undefined.
   Before delivering, hide the article and read the illustration cold — anything that needs the
   text beside it to make sense is wrong, however exactly it was quoted.
5. **Never the interpunct as a sentence separator.** `Thinfinity · concurrent single license` is two
   thoughts welded together with a dot that means nothing. The dot belongs between items of the same
   kind — `MFA · SSO · SAML`, `OCI · AWS · Azure` — and nowhere else. Where one thing qualifies
   another, they are a title and a subtitle on two lines, not one line with a dot in the middle.
6. **Never write the company's name in the third person, and avoid writing it at all.** "A strong
   Cybele partnership behind it" reads like someone else describing us. It is "a strong partnership
   behind it". The product name is used where a pill or a label genuinely names the product; the
   company name almost never earns its place on an illustration.
7. **No cards near the image title** — leave breathing room
8. **One illustration per illustrable section. No variants** — variants are a cover thing.
9. Native SVG on the SVG route, editable in Figma (the authoring rules are in `SKILL.md`); real
   frames on the Figma route.
10. The margin the composition is laid out to is in **1 · Canvas and spacing**.

### Before delivering

Run this over the finished set. Every line is a failure that has actually shipped:

- Each illustration has its **one sentence** saying what it shows that the paragraph does not, and
  that sentence is not "it shows the items".
- **Cover the words: something is still being claimed.** No illustration is a list reset in a nicer
  typeface.
- The shape of each section's information is **named**, and the pattern is the one that shape owns.
- **Where order matters, order is visible.** No sequence in a grid.
- No two illustrations in the set use the same pattern, and no two titles share a grammatical shape.
- Every card's description is about that card's own title.
- Every word on every illustration is traceable to a passage of the article.
- **Read cold, with the article covered, every illustration still makes sense on its own** — no
  phrase leaning on a definition that is not on the image, and no title pointing at something that
  is not drawn.
- Every arrowhead is a claim about direction that is true, and **nothing that does not move has a
  connector at all** — no headless lines.
- **Every box of the same kind is the same size within the illustration**, set by the one that needed
  the most room.
- Anything a column enumerates is a **List**, not a stack of pills, and it sits on the column's body
  block rather than floating on the page surface.
- Every list uses **one mark**, chosen for what it says rather than defaulting to a check, and every
  list icon is square.
- **Every icon was searched for by the words on its own pill**, and its name is recognisably about
  them. Any concept the search could not match is named in the run notes.
- In a Two sides comparison, no card title appears in both columns, and **each column has a header**
  — title, subtitle, and the surface under them.
- No interpunct is doing the work of a full stop, and the company name appears nowhere in the third
  person.
- If an illustration is a hub, all four of its conditions hold — in particular, **removing the
  centre would break it**. If the items survive alone, it should have been a grid.
- The item count came from the section, not from the pattern — nothing was padded or dropped to
  reach four — and it is within the card minimum and maximum.
- Every card title and description is inside its text budget, and no sentence was cut to get there.
- The distinct size/weight pairs in the file all appear in the type table in **3 · Text**.

---

## Where these rules came from (Figma reference)

> **Reference only.** What follows is the record of the Figma sources these rules were derived from.
> Where it restates a value, the tables above are the rule — this is a record, and editing it would
> rewrite history rather than change a design.

### Purpose

Generate branded illustrations for Cybele blog articles as **editable SVGs** that can be opened, adjusted, and finalized in Figma. Each article section gets a single image (dark or light mode, alternated for variety).

### Input / Output

| Input | Output |
|-------|--------|
| Article text (English, technical) | 1920x1080 SVG per section |
| Section titles to illustrate (selected by the user) | Native SVG: `<text>`, `<rect>`, `<circle>`, `<path>` — fully editable in Figma |
| Figma style reference (Blog Posts file) | Cybfont icons embedded as real vector paths |
| Figma iconography reference (Cybele Design System) | Dark and light variants mixed across illustrations |

### Figma sources

| Source | What it gave us |
|---|---|
| `figma.com/design/1rA3ZWuHPxh1BW2YXfF1LR/Blog-Posts---2026` | The original style: layouts, typography, sizing (2026-03) |
| Figma file **"Exercise"** `8RBfhSYgaCuo4uM82JqAHL` — palette `264:287`, light sample `264:358`, dark sample `264:323` | The reduced palette and the semantic states now in force (2026-06) |
| `figma.com/design/x0HMD1pXkcYdFM7NSaBvb4/Cybele-Design-System` → `8120:7263` | The Cybfont icon library |

**Layout patterns identified** (the shapes seen in the 2026-03 reference; the live list, and which
content each one is for, is *Layout patterns* above):
- A centre with three or four branches radiating from it, with arrows
- Numbered cards in a zigzag, each with icon, title and description
- A centre logo with four features around it, on curved connectors

**Sizing rules:**
- Canvas: 1920x1080px
- Content should fill ~70% of the composition
- Not all illustrations need the same mode — alternate dark/light across the set
- Max 6 words per title
- Descriptions: 1–2 short sentences focused on what + why

### Cybfont Iconography (from Figma Design System)

**Source:** `figma.com/design/x0HMD1pXkcYdFM7NSaBvb4/Cybele-Design-System` → node `8120:7263`

The Cybfont is a custom icon library organized by category (Apps, Communication, Devices, Commerce, Hackers, Controls, Numbers, Objects, Concepts, Logos, etc.). Each icon has variants: `light`, `bold`, `filled-bold`.

**Critical process for using Cybfont icons in SVGs:**

1. Identify the icon by conceptual match (e.g., "shield-ok" for backup/protection, "import-export" for VM migration)
2. Get the icon's frame node ID from the Design System metadata
3. Get the specific variant symbol ID (e.g., `light` for outlines, `filled-bold` for solid)
4. Call `get_design_context(nodeId, fileKey, excludeScreenshot=true)` → returns an asset URL
5. **Key discovery:** The asset URL (`figma.com/api/mcp/asset/UUID`) returns **SVG content**, not PNG
6. Fetch the SVG text, extract the `viewBox` and inner `<path>` / `<g>` elements
7. Embed the native SVG paths into the illustration, wrapped in a `<g transform="translate(x,y)"><svg width="..." height="..." viewBox="...">` container
8. Colorize by replacing `fill` and `stroke` attributes with the target color

> Every icon in the library, with what it depicts, is in
> [`ICON_MEANINGS.md`](ICON_MEANINGS.md) — the designer's own list, read off the components.
> Pick by what the illustration has to communicate, from there.

### How the illustrations are built

Build on `./reference_generator.py`, which is bundled here: read the icon SVGs from the icon set
(`BRAND_DESIGN_RULES.md` §8 says how to find it), recolour them by replacing their `fill` values,
compose the illustration programmatically, and write the SVGs to the output directory the caller
gives. Two older generators (`export-native-svgs.mjs`, `build_blog_svgs.py`) live outside this repo
and are **not** required — if you are told to use one and cannot open it, say so and carry on.

**What does NOT work for Figma-compatible SVGs:**
- **Editable paragraphs.** No SVG can carry one: Figma splits every hard line break into its own
  text layer, `<tspan>`s included (verified 2026-09-08). Group a paragraph in one `<text>` with
  `<tspan>` children anyway — see `SKILL.md` → *Text: SVG cannot carry a wrapping paragraph* — and
  tell the user that editing text as paragraphs means building the illustration in Figma instead.
- `<foreignObject>` (Figma ignores it — `dom-to-image` output is useless)
- `<image href="data:image/png;base64,...">` (Figma drops these on import)
- External URL references in any form
- Only native SVG primitives are accepted: `<rect>`, `<circle>`, `<text>`, `<path>`, `<line>`, `<polygon>`, `<linearGradient>`, `<g>`, `<svg>` (nested)

---

## Record

Colours that were retired, values that were superseded, and the decisions still open are kept out of
this file so it holds only what is in force: see [`HISTORY.md`](HISTORY.md). Consult it before
re-introducing a colour — several were tried and dropped on purpose.
