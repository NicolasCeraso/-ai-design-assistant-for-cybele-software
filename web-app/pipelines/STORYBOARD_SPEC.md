# Cybele / Thinfinity — Video Storyboard Generation Spec

**Version:** 2.1 · **Date:** 2026-10-30 (2.0: 2026-10-09)
**Owner:** Cybele design team (Nick Ceraso)
**Purpose of this file:** the *authoritative, reproducible* spec for generating video storyboards in the
Cybele/Thinfinity house style. A future Claude session should be able to read **only this file** and
produce an on-brand storyboard from a voiceover script.

> **v2.1 (2026-10-30)** folds in Nick's `criterio-storyboard-contact-centers.md`: the Figma board structure, the
> scene-per-key-state rule, the narrative colour logic, the typography as built in the finished storyboard, and the
> asset policy (library instances first). The new material is §16; §4.5, §5 and §7 were corrected where it differs.
>
> **v2.0 replaces v1.0 (2026-07-15).** v1 described a dark-navy "techy" look (glow, dot-grid, glass
> cards, 1920×1080, `NN · SECTION` kickers). The team's real storyboards in the "Youtube" Figma file
> do not look like that. v2 is reverse-engineered from the most mature one — the **"Contact Centers"**
> page (`4472:2633`, 28 scenes in 10 blocks) — and corrected against **"Contractor VDI"** (`3958:6167`)
> and the 3840 scenes of **"Oracle"** (`1067:1518`). Where v1 and the Figma file disagree, the Figma
> file wins.

---

## 0. TL;DR

From a **fixed voiceover script** (the backbone — never altered), produce **blocks of 3840×2160
keyframes** (1–4 scenes per block, one per key state of the animation, stacked in a column), each block paired with its `VO n` lines and a
`Guion` box (`VOICEOVER:` verbatim + `En pantalla:` in Spanish describing the motion). The look:
**flat, minimal, one dominant element per scene, a headline on top with a thin rule under it, one
accent word in red (problem) or none, flat icons, the background colour tells you where you are in the
story.** No glow, no gradients, no dot-grid, no glass.

---

## 1. Purpose & scope

Turn a **video script (voiceover, ~one sentence = one beat)** into a **storyboard** — the ordered
keyframes that visualize each beat — in the house style so every video is visually consistent.

This is **narrative keyframing** (the sequence tells the product story), *not* editorial illustration
(blog) nor technical diagramming (arch). It must *demonstrate* the idea with one clear picture per
scene, not decorate the sentence.

**Hard rule — the script is the backbone.** The voiceover text is fixed and verbatim. We only make
**graphic** decisions: composition, motif, colour, motion. On-canvas headlines may sharpen the beat but
never contradict or replace the VO.

---

## 2. Inputs / outputs

| Input | Output |
|-------|--------|
| Voiceover script (English, verbatim), ~1 sentence per beat | Blocks of 3840×2160 native SVG scenes named `NNa`, `NNb`, `NNc` |
| (optional) emphasis / which beats to stress | One HTML preview: each block = its scenes stacked + `VO n` + `Guion` box |
| The "Youtube" Figma file, page "Contact Centers", as the style reference | (on approval) blocks pushed into the "Youtube" Figma file |

---

## 3. Provenance (where the style comes from)

- **Canonical reference:** Figma file `K8rHguGyksdPWdHrSA3VOi`, page **"Contact Centers"** (`4472:2633`),
  frame `Thinfinity para Contact Centers` (`4473:2682`). Reference scenes: `4473:2685` (problem, light
  bg, red stat), `4473:2727` (enumeration pills), `4473:2890` (repetition as argument), `4474:2769`
  (the "what if" beat, dark bg), `4475:2767` (solution, light bg, two sides), `4478:2767` (three
  capability cards).
- **Older styles, kept only as history:** page "Oracle" (`1067:1518`) holds the first storyboards
  (1920×1080 cascades, dark navy shields/tunnels) and the later 3840 ones; "Contractor VDI" (`3958:6167`)
  is a working canvas with frames reused from other projects. **Do not copy their look.**
- The earlier v1 "techy pass" (glow, glass, dot-grid, vignette) was never adopted by the team and is
  retired.

---

## 4. The design system

### 4.1 Canvas & layout
- **3840×2160** (16:9). Build in the 3840 coordinate system; it is 1:1 with the Figma frames.
- Left text margin **653 px** (the headline x). Content block roughly between 650 and 3170 px wide.
- **Headline** at the top-left, y 276. A **thin divider rule** sits under it: x 668, y 574, 2504 px
  wide, 4 px tall, colour `rule`.
- **One idea per scene.** One dominant element; everything else subordinate. Plenty of empty space.
- Two framings do most of the work: **left picture + right statement** (e.g. grid of agents left,
  "1/3" right) and **A → B** (device left, cloud right, dashed line between).
- Centered layouts (headline centered, picture centered) are for the **"what if" and payoff** beats.

### 4.2 Colour tokens (sampled from the real frames)
```
bgProblem   #E2E9F3   light grey-blue — problem / status-quo scenes
bgSolution  #EFF7FE   lighter blue-white — Thinfinity solution scenes
bgBlue      #003DBC   solid brand blue — payoff / "how it works" scenes
bgNavy      #04266B   deep navy — scenes that show the real product UI full-bleed
bgDark      #021425   near-black navy — the single "what if…?" pivot beat
ink         #003156   headline + body text on light backgrounds
inkSoft     #174366   big statistic numerals and their label
rule        #B8CBDC   thin divider under the headline
pill        #FFFFFF   white pill / card fill on light backgrounds
person      #D5E1EE   inactive/neutral person disc and placeholders
blue        #0A74D6   Thinfinity blue — devices, icons, selected card outline
red         #DF3A1B   PROBLEM / LOSS — the one accent on problem scenes (Nick's criterion, 2026-10-30)
redAlt      #F1280A   the second red the finished frames also use; same job, same scenes
mint        #2ADDBE   SECURE / PROTECTED / CONFIRMED (strokes and small fills)
mintSoft    #3DCCA1   mint when it has to sit on a white card
white       #FFFFFF   text and thin strokes on blue/dark backgrounds
screenBlue  #003DBC   the "desktop" inside a laptop or browser mock
winLight    #D9E2F5   secondary window inside a desktop mock
```

### 4.3 Colour-with-a-job (the most important rule)
Each colour has **one job**, so a frame reads before you read it.

| Role | Colour | Means | Examples |
|---|---|---|---|
| Problem / loss | **red** `#DF3A1B` | something lost, costly, at risk | the 3 agents who leave, "Every exit:", a "gone" word |
| Neutral / not the point | **person** `#D5E1EE` | the rest, inactive, background mass | the 6 agents who stay |
| Thinfinity / device | **blue** `#0A74D6` | the product, a device, a selected item | laptop, selected card outline, supervisor |
| Secure / confirmed | **mint** `#2ADDBE` | protection, data kept safe, "on" | lock on the cloud, shield, "Zero trust" lock |
| Text | **ink** `#003156` | everything you read | headline, labels |

Discipline: **red only on problem scenes, mint only on security ideas.** If a scene has neither, it is
blue + neutrals, and that is correct. No violet, no warm/amber — they are not part of this system.

### 4.4 Background follows the story
The background colour is a narrative signal. Pick it by where the beat sits:

| Beat | Background |
|---|---|
| The problem, the cost, the status quo | `bgProblem` + one red accent |
| The pivot ("What if…?") | `bgDark` + mint outline motif + white centered line |
| How Thinfinity works / the mechanism | `bgSolution` (light) or `bgBlue` (solid) |
| Showing the real product UI | `bgNavy` with the screenshot-style browser mock |
| Payoff / closing line | `bgBlue` + white centered headline |

Within one block, backgrounds stay the same unless the beat itself flips (problem → pivot).

### 4.5 Typography
- **Inter** only. Weights: Medium 500 and Regular 400 for headlines, SemiBold 600 for supporting phrases and
  closing, Bold 700 for big statistic numerals.
- Scale on the 3840 canvas (measured from the frames, ±10%):
  - **Headline on light backgrounds:** 115 px, Inter Medium, `ink`, with the prefix in `red` ("The problem:"),
    and a thin rule under it (§4.1). Example: "**Every exit:** recover · wipe · hope".
  - **Scene title on `bgBlue`/`bgDark`:** 120 px, Inter Regular, white, centered, 150 % line-height, no accent.
  - **Hero statistic:** 593 px Inter Bold, −8 % tracking, `inkSoft` (e.g. "1/3", "0"), with its label at 150 px SemiBold
    and a source line at 96 px Regular. One accent word in the label may be `red`.
  - **Supporting phrase:** 150 px Inter SemiBold, −2 % tracking, 95 % line-height, one keyword in `red`.
  - **Pill / card label and chips:** 80–110 px, Medium.
  - **Caption on an arrow or link:** 72 px, Regular.
  - **Closing plate:** 196 px Inter SemiBold (the same as the Contractor VDI title card).
- The narration lives in the **`VOICEOVER:`** text beside the block, not baked into the frame. The
  on-canvas text is a short headline and labels only (3–6 words).

### 4.6 Shapes & icons
- **Flat and borderless**, in line with the brand rules: no shadows, no gradients, no glow, no blur (the one exception, the cloned title-card artwork of the closing, is in §16.3).
- **Person:** a round disc (`person`, or `red` when "affected") with a thin lighter outline figure inside.
- **Laptop:** `blue` body, `screenBlue` screen with two stacked windows (`white` and `winLight`) inside; a
  small white circular badge in the corner for status (refresh, check, lock).
- **Cloud:** thin `ink` or `mint` outline cloud; the content sits inside it (desktop, database, lock).
- **Pills:** white, fully rounded, label in `ink`, used **only to enumerate** (a short list of real items).
- **Cards:** white, rx="48", icon + 2-line label centered; the *selected* one gets a `blue` outline.
- **Dashed link** between two sides = connection or data flow; label above it in `inkSoft`.
- **Repetition is an argument:** a grid of the same object (12 identical laptops with a refresh badge)
  says "this multiplies". Do this instead of writing "many".
- Use the **brand icons** (`icons/` library, `currentColor`) before drawing anything by hand.

### 4.7 Component vocabulary
Reusable builders (JS helper library that emits SVG strings, so tokens never drift):

`canvas(bg) · headline(accentPart, rest) · rule · stat(value, label, source) · person(state) ·
personGrid(n, affected[]) · laptop(badge) · laptopGrid(rows, cols, badge) · browser(content) ·
cloud(content, stroke) · lock · db · pill(text) · card(icon, label, selected) · dashedLink(label) ·
badgeCircle(kind)`

**ID prefixing (hard rule):** every `<defs>` id (gradients, clip-paths) must be **prefixed per scene**
(`s01a_clip`, …): ids are document-global across stacked inline SVGs; unprefixed ids cause silent fill
breakage.

---

## 5. Editorial rules
- **One headline per scene**, 3–6 words, sharpens the beat, never contradicts the VO.
- **One dominant element.** If a scene has more than 3 competing elements, cut until one leads.
- **Object continuity inside a block.** The same object survives from `a` to `b` to `c` and **changes
  state**: the 9-agent grid (3 red) → the same grid with a laptop on each → the 3 leave and new ones
  appear with a currency icon. Reuse the exact same geometry and position, so the eye follows it.
- **Repetition as argument** (see §4.6). **Highlight as argument:** 3 of 9 painted red = "a third".
- **Show the mechanism, don't label it.** A device and a cloud with a dashed "Display only" link says
  more than a paragraph. Pills are for genuinely enumerable lists (browser / CRM / softphone).
- **Complex → simple in one frame.** Where the beat allows, density resolves to one clean element.
- **Name the object in the scene.** A picture of "agents" should be agents; "laptop" a laptop. No
  abstract tokens (circles, blobs) standing in for a concrete noun.

---

## 6. Motion / `En pantalla:` rules
Storyboards are for **video**, so every block carries the **`En pantalla:`** description — the director's
note on what moves. It is written in **Spanish**, in plain production language, like the team writes it
in Figma:

> "Estadística con 9 agentes de los cuales 3 aparecen pintados. Se le va agregando una laptop a cada
> uno de ellos."
> "Se caen/van los 3 pintados y aparecen unos nuevos con un ícono de pesos. Se agranda la laptop (con
> escritorio) con ícono de update y se multiplica en muchas."

- Describe **what enters, what changes state, what leaves**, in order, tied to the VO phrase that triggers it.
- Name transitions explicitly when the background flips ("el panel se da vuelta y del otro lado es rojo").
- Motion serves the one dominant element; don't animate everything at once.
- Source-language rule: `VOICEOVER:` stays **verbatim in the script's language**; `En pantalla:` is Spanish.

---

## 7. Scene grammar & block decomposition
1. Read the whole script; find its **natural sections** (problem → pivot → mechanism → controls → payoff).
2. **Group into blocks of 1–4 VO sentences** that share one idea. Each block gets a number (`01`, `02`…).
3. Inside a block, **1–4 scenes** (`a`, `b`, `c`, `d`): the continuity chain from §5. **One frame per key state of
   the animation** the script's Visual column describes, so the motion designer sees the start and the end of
   every transition (see §16.2). Each scene is a state of the same picture, not a new picture.
4. Assign each block its **background** (§4.4) and its **motif + colour roles** (§4.3) before drawing.
5. Name each scene `NNx · Short description` (e.g. `01a · Nine agents, one third gone`).
6. Every block ends with the **`Guion`** box: `VOICEOVER:` (verbatim) + `En pantalla:`.
7. The last block is a **payoff / end card** on `bgBlue`; if the script has a CTA, show logos + URL.

---

## 8. SVG Figma-safe rules (hard)
- **Allowed:** `<rect> <circle> <ellipse> <path> <line> <polygon> <polyline> <text> <tspan> <g>
  <linearGradient> <radialGradient> <defs>`. (Gradients are allowed but the house style does not use them.)
- **Forbidden** (Figma drops them silently on import): `<foreignObject> <image>` (incl. base64 data URIs),
  external `<use>`, external URL refs, `<pattern>`, and CSS `<style>`/classes for SVG geometry.
- **Text is live text** — headlines, labels, numerals, never outlined or rasterized.
- Escape `&`→`&amp;`, `<`→`&lt;`, `>`→`&gt;` inside `<text>`. Prefix all ids per scene (§4.7).
- Real product screenshots (browser UI) are **images the designer drops in later**: leave a labelled
  placeholder frame and say so in `En pantalla:`; don't fake a screenshot in vectors.

---

## 9. Authoring workflow
1. **Read this spec** + the target voiceover (verbatim).
2. **Decompose** into blocks and scenes (§7). State, per block, the thesis and the background before drawing.
3. **Build** the HTML preview: JS helper library (§4.7) + one builder per scene, inline
   `<svg viewBox="0 0 3840 2160">`. Layout of the page mirrors Figma: each **block = a row**:
   scenes stacked in a column on the left, then a thin divider, then `VO 1…n` and the `Guion` box.
4. **Render & verify** (§10) — read the PNG against this spec and the §12 checklist. Iterate.
5. **Open** it in the user's browser for review (`start "" "<abs path>"`).
6. On approval, **push to Figma** "Youtube" (`K8rHguGyksdPWdHrSA3VOi`) via `generate_figma_design`
   following the project's Figma workflow (capture script, `outputMode: existingFile`, poll `captureId`).
7. If run inside the Cybele Console, save outputs to `jobs/<id>/output/v<N>/` (pipeline key `storyboard`).

---

## 10. Render / verify recipe
Edge headless, full-page screenshot. **Use an ABSOLUTE path for `--screenshot`** (relative fails with
"Access denied"):
```bash
OUT="C:/abs/path/preview.png"
"/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
  --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1600,<tall-enough> \
  --screenshot="$OUT" "file:///C:/abs/path/storyboard.html"
```
- The tall PNG downscales when read — **crop it into chunks** with Pillow (`py -3.13`) and read each.
- Grep for invalid/typo hex after writing. The JS-helper path avoids this — prefer it.
- **Colour check:** sample the rendered background and accent pixels and compare with §4.2.

---

## 11. HTML preview conventions
- Page: light grey `#F4F6F9`, Inter via `@import`, one **row per block**.
- Each row: column of `<svg viewBox="0 0 3840 2160">` scenes (scaled to ~480 px wide), a thin vertical
  divider, then `VO 1…n` and a `Guion` box (`VOICEOVER:` bold + text, `En pantalla:` bold + text).
- Caption each scene with its `NNx` name.
- No `<use>`/components: each scene repeats its primitives inline (Figma-safe, self-contained).

---

## 12. Quality checklist (before showing the user)
- [ ] Canvas is 3840×2160; headline at the 653 margin with the thin rule under it.
- [ ] One dominant element per scene; max 3 competing elements.
- [ ] Background chosen by the story beat (§4.4); red only on problem scenes; mint only for security.
- [ ] **No** glow, gradient, dot-grid, glass, shadow (v1 look is retired).
- [ ] Objects named in the VO are drawn as that object (agent = person, laptop = laptop, cloud = cloud).
- [ ] Continuity: the same object keeps its geometry across `a/b/c` and only changes state.
- [ ] Brand icons used wherever one exists; pills only for real lists.
- [ ] `VOICEOVER:` verbatim; `En pantalla:` present, in Spanish, and tied to VO phrases.
- [ ] Figma-safe (no forbidden nodes; ids prefixed per scene; hex valid; text is live).
- [ ] Rendered and visually verified; colours sampled against §4.2.

## 13. File naming / versioning
- `storyboard_v<N>_<slug>.html` in the working dir (or `jobs/<id>/output/v<N>/`). Never overwrite a prior
  version — keep v1, v2, … for side-by-side comparison. `<slug>` names the script (e.g. `contact_centers`).
- Scenes inside a block: `NNa`, `NNb`, `NNc`.

## 14. Status & next steps
🟡 **In progress.** v2.0 rewritten from the real Figma storyboards on 2026-10-09; v2.1 (2026-10-30) adds Nick's
Contact Centers criteria (§16). Not yet validated by a console run. Next steps: run one task from a real VO script with this spec, compare it against the
Contact Centers page side by side, then fix whichever token or rule is off. Still **not** packaged as a
Claude skill.

---

## 15. Appendix — worked examples (beat → visual maps)

### A. "Contact centers" (reference page `4472:2633`)
| Block | Beat | Scenes (background · picture) |
|---|---|---|
| 01 | A third of agents are gone within a year. Each sits in front of a business laptop, mostly for a browser, a CRM and a softphone. | **01a** problem bg · 9 agents, 3 red, "1/3 of agents are gone within a year" · **01b** same 9 agents, a laptop on each; right: "Mostly for…" + 3 white pills |
| 02 | Every new hire means a PC to buy, image and ship. Every exit means recovering, wiping, hoping. The auditor asks what was on it. | **02a** the 3 red leave, new ones appear with a currency badge · **02b** one laptop with desktop and update badge · **02c** problem bg · 12 identical laptops with refresh badge, headline "Every exit: recover · wipe · hope" · **02d** the auditor question |
| 03 | The laptop dissolves; the desktop lives in the cloud; meet Thinfinity Workspace. | **03a** laptop dissolves · **03b** `bgDark` · desktop inside a mint-outline cloud, "What if the desktop never left the cloud?" · **03c** payoff |
| 05 | BYOD, data stays in the cloud region, copy/download/print under control. | **05b** solution bg · laptop → dashed "Display only" → cloud with database + mint lock; labels under each side |
| 09 | Supervisors monitor live sessions, record any session, watermark the screen. | **09a** solution bg · supervisor disc + three white cards, first one selected (blue outline) with a mint magnifier |

---

## 16. Contact Centers criteria (Nick, 2026-10-30)

Source: `criterio-storyboard-contact-centers.md`, written for the **"Thinfinity para Contact Centers"** storyboard
(script "Thinfinity para Contact Centers: Guión de video", the YouTube table, 1:20–1:45). Destination: Figma
`Youtube` (`K8rHguGyksdPWdHrSA3VOi`), page **Contact Centers**, frame `Thinfinity para Contact Centers`. Style
reference: the **Contractor VDI** page of the same file. Scope: the main video only; the four LinkedIn / Cybele
Blogs clips are cuts of it and get no board of their own.

### 16.1 Figma board structure (what is pushed to the file)
- A black container frame (`#000000`) with the video title at the top left (Inter Regular 834 px) and a subtitle with
  format and duration.
- **One column per script row** (10 columns), 7300 px apart on X. Each column stacks its **3840×2160 scene frames**
  with a 100 px gap; the columns are aligned at the bottom, as in Contractor VDI.
- To the right of each column: a **white vertical divider** 8 px wide that follows the column's height, and the
  **voiceover fragments** (Inter Regular 160 px, white, 2000 px wide) aligned with the scene in which they sound.
- Below each column, one script block with two parts: **VOICEOVER:** the literal narration, and **En pantalla:** the
  document's literal visual description. Inter 160 px, labels in Bold.
- Layer names `NNx – description` (e.g. `05b – Data stays in the cloud region`): the number is the script row, the
  letter is the animation step.

### 16.2 Scenes per row
Each row is split into as many frames as the Visual column describes **key states of the animation**, so the start
and the end of every transition are drawn. The Contact Centers board, as built:

| Row | Frames | Criterion |
|---|---|---|
| 1 | 2 | Statistic → laptops are added |
| 2 | 4 | Replacement with $ → enlarged laptop → multiplication → the auditor's question |
| 3 | 3 | Laptop dissolves → desktop in the cloud → logos |
| 4 | 2 | Devices → gateway; then the SSO/MFA balloon |
| 5 | 3 | BYOD in the browser → data stays in the cloud → copy / download / print controls |
| 6 | 2 | Outbound connection → zero inbound ports |
| 7 | 3 | Zoom out to Cloud Manager → shift curve → seasonal peaks |
| 8 | 2 | Headset + waveform → encrypted tunnel |
| 9 | 3 | A magnifier over each of the 3 features (one per frame) |
| 10 | 2 | Closing sentence → final plate |

### 16.3 Narrative colour logic (extends §4.3–§4.4)
Backgrounds seen in the finished board: dark `#021425` (solution intro, security, closing), Thinfinity blue
`#003DBC` (connectivity, voice), light A `#E2E9F3` (problem, operations), light B `#EFF7FE` (BYOD, supervision).
Text navy `#003156` / `#174366`. Red for a problem is `#DF3A1B` (the main one) or `#F1280A` (the second red the finished frames use); the token `red` in §4.2 is `#DF3A1B`. The earlier spec had `#F12808`, a mis-sampled `#F1280A`: replaced.
Accent blue `#0A74D6`; accent green `#2ADDBE` (security, OK, gateway).
- **Problem** (rows 1–2): light backgrounds, red for the pain (agents leaving, costs, the auditor).
- **Turn / solution** (row 3): dark background and green for the paradigm change.
- **Benefits** alternate blue, light and dark for rhythm; **never two equal backgrounds in a row**.
- **Closing** (row 10): the dark background with the clouds and red gradient of the existing title card; the final plate
  uses the same structure as Contractor VDI's. This is the one place a gradient is allowed, because it is the
  title card's own artwork and is cloned, not redrawn.

### 16.4 Assets and icons: reuse first, draw last
- **Reuse instances of the Cybele library** already used in Contractor VDI, so they stay linked: `user`, `notebook`,
  `cpu`, `pc-user-location`, `gateway`, `id-integration`, `2fa`, `lock-check`, `copy`, `file`, `doc`, `ilus-toggle`,
  `control-panel`, `ilus-monitor`, `full-desk`, `rec`, `ilus-search`, `forbidden`, `Icon / Arrow / Refresh`.
  (In Figma an icon is always a component instance, never a loose vector: Nick's global rule.)
- **Clone existing graphic pieces** instead of redrawing: laptop `laptop3`, the `browser` window, the red and navy
  laptops with a lock; the **Thinfinity + Oracle Cloud** lockup and the title card's logo group; the `soundwave`
  waveform, the final plate's background ellipse and the title card's gradient clouds.
- **Draw as vectors only what has no library equivalent**: cloud, headset, database, outline monitor, shift curve,
  monthly bars, arrows and dotted connectors. If the library gains one of them, replace the vector with the instance.
- **Connectors are dotted lines**: white on blue, green on dark. It is the same language as the Gateway/Broker flow of
  the earlier storyboard.
- **Recolour icons by background:** navy on light, white on blue/dark, green for security or OK states.

### 16.5 On-screen content
- **On-screen text in English**, like the voiceover and the earlier storyboard; the director's notes stay in Spanish.
- Very little text: short phrases derived from the voiceover ("All they need is a browser", "Outbound only", "No VPN",
  "No plugins"), never the whole narration.
- One simple visual metaphor per technical idea:
  - **Agent turnover:** a grid of 9 avatars with 3 in red, which then appear as dotted places plus new agents with a $ badge.
  - **Hardware cost:** a laptop with desktop and an update badge, then multiplied into a grid.
  - **The desktop never leaves the cloud:** the laptop dissolves into particles and the window rises into a cloud.
  - **Access from any device:** 3 devices converge on a single gateway.
  - **Data in the region:** a laptop with "Display only" connected to a cloud with a database and a lock.
  - **Outbound connection:** the arrow points from the desktops toward the gateway, never the other way round.
  - **Zero inbound ports:** a red inbound arrow blocked by a prohibited icon.
  - **Scaling by shift:** a plateau-shaped curve, green at the start and red at shutdown.
  - **Seasonal peaks:** bars per month with November and December highlighted.
  - **Voice without plugins:** a tunnel with a waveform between the headset and the desktop, a lock on top.
  - **Supervision:** a supervisor with 3 cards; a magnifier visits one card per frame.
- **Final plate:** lockup, "Start with a proof on OCI" and the URL **cybelesoft.com**. The script gives no URL, so the
  one from the earlier storyboard was used.

### 16.6 Open items to validate
- The final plate's URL (`cybelesoft.com` was assumed).
- The "thin client" icon (`cpu` was used) and the "watermark" icon (`doc` was used): replace them if the library has a specific one.
- Headset and calendar were drawn as vectors: replace them with instances if they are added to the library.
- The LinkedIn clips have no storyboard of their own.

---

*Related project docs:* `progress.md` → "Video Storyboard Pipeline"; the "Youtube" Figma file
(`K8rHguGyksdPWdHrSA3VOi`); the Cybele brand system (`BRAND_DESIGN_RULES.md`, palette 06/26, Inter,
borderless/shadowless/low-contrast).
