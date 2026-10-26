# Cybele / Thinfinity — Video Storyboard Generation Spec

**Version:** 1.0 · **Date:** 2026-07-15
**Owner:** Cybele design team (Nick Ceraso)
**Purpose of this file:** the *authoritative, reproducible* spec for generating video storyboards in the
Cybele/Thinfinity house style. A future Claude session (or the `cybele-video-storyboard` skill) should be
able to read **only this file** and produce an on-brand storyboard from a voiceover script.

> Modeled on the project's `progress.md` ("Video Storyboard Pipeline" section) and the session handoff
> `storyboard_handoff_contractor_desktop.md`. This spec **supersedes** the short progress.md section by
> adding the **editorial pass** and the **techy pass** developed across storyboard versions v1→v4.

---

## 0. TL;DR

From a **fixed voiceover script** (the backbone — never altered), produce an ordered set of
**1920×1080 keyframes** as **native, Figma-safe SVG**, one idea per scene, each paired with its
`VOICEOVER:` line and a `Motion:` note. Delivered as a single **HTML preview** with the scenes stacked
vertically. On approval, the SVGs are pushed into the team's **"Youtube"** Figma file. The look:
**dark-navy, minimal, depth + glow, glass cards, colour-with-a-job, mechanism shown not labelled.**

---

## 1. Purpose & scope

Turn a **video script (voiceover, ~one sentence = one beat)** into a **storyboard** — the ordered
keyframes that visualize each beat — reproducing the house style so every video is visually consistent.

This is **narrative keyframing** (the sequence tells the product story), *not* editorial illustration
(blog) nor technical diagramming (arch). It is a **software-product** register: modern, techy, and it must
*demonstrate* "making something complex feel simple", not just say it.

**Hard rule — the script is the backbone.** The voiceover text is fixed and verbatim. We only make
**graphic** decisions: composition, motif, colour, depth, motion, on-canvas headlines (headlines may
paraphrase/sharpen the beat, but never contradict or replace the VO).

---

## 2. Inputs / outputs

| Input | Output |
|-------|--------|
| Voiceover script (English, verbatim), ~1 sentence per beat | One 1920×1080 SVG per scene (native, editable in Figma) |
| (optional) emphasis / which beats to stress | Single HTML preview — scenes stacked vertically, each with its `VOICEOVER` + `Motion` line |
| The "Youtube" Figma file as the style reference | (on approval) scenes pushed into the "Youtube" Figma file |

---

## 3. Provenance (where the style comes from)

- **House style (base):** reverse-engineered from the team's **"Youtube"** Figma file —
  `fileKey K8rHguGyksdPWdHrSA3VOi`, page **"Oracle"** (`1067:1518`). ~10 finished storyboards, each a
  **horizontal cascade of 1920×1080 frames**, every scene paired with a `VOICEOVER:` text node. Reference
  scenes: `1614:3290` (tunnel), `1614:3222` (tunnel struck + active shield), `1067:4508` (compliance pills).
- **Editorial pass (v2):** bolder on-canvas headlines, filled device/desktop mockups, glass cards,
  consolidated beats, duotone brand-blue payoff.
- **Techy pass (v3/v4):** depth (gradient + dot-grid + vignette), glow on the focal element, glassmorphism,
  **colour-with-a-job**, mechanism-shown-not-labelled, numbered wayfinding, per-scene motion notes.

The techy pass (v3/v4) is the **current standard**. Everything below reflects it.

---

## 4. The design system

### 4.1 Canvas & layout
- **1920×1080** (16:9). Title-safe margin ≈ 120 px.
- **One idea per scene.** A single focal element; everything else is subordinate. Generous negative space.
- Headline anchored **top-left** (or centered for overview/payoff scenes); hero diagram fills the rest.
- Prefer **comparison** (problem left / Thinfinity right) and **state-change** (off→on, before→after) framings.

### 4.2 Colour tokens
```
navy      #0B1A2F   scene base (top of the bg gradient)
navy2     #0E2338   bg gradient bottom
brand     #1E80C6   payoff scenes (solid fill)
blue      #2E9CFF   PRODUCT / ACTIVE
blueDim   #6FB4FF   eyebrow / kicker text
mint      #2BD9A0   SECURITY / EVIDENCE / CONFIRMED
violet    #7B7BF5   NETWORK / IDENTITY / PROTOCOL
warm      #F5B454   CLIMAX ACCENT — one per storyboard, reserved
white     #FFFFFF   text, thin strokes, bands
muted     #8AA6C4   secondary body text / sublabels
chipText  #DDEBF8   chip / pill label text
card      #0F2942   card fill (used at ~0.66 opacity for glass)
chip      #0F2136   chip / pill fill
uiBar     #26456A   UI-mock title bar
uiLine    #1C3550   UI-mock content lines
stroke    #33557A   neutral card stroke
strokeDim #26456A   dim / secondary stroke
dim       #2E4A6B   "off"/inactive state fill
```

### 4.3 Colour-with-a-job (the most important rule)
Each colour has **one job**. This is what lets a frame read *without* reading the labels. Assign the role
first, then map the beat's concepts onto the roles:

| Role | Colour | Means | Examples |
|---|---|---|---|
| Product / active | **blue** `#2E9CFF` | the Thinfinity product, an active/on element | Gateway, Broker, Cloud Manager, active desktop, flows |
| Security / evidence | **mint** `#2BD9A0` | secure, positive, confirmed, audit, compliance | shields, checks, "private fleet", "data at rest", audit evidence, framework badges |
| Network / identity / protocol | **violet** `#7B7BF5` | the network layer, IdP/identity, raw protocols | ZTNA, IdP auth (dashed), RDP/SSH/VNC |
| Climax accent | **warm** `#F5B454` | exactly **one** highlight per storyboard | FedRAMP badge, a single hero payoff detail |
| Neutral / off | **dim** `#2E4A6B` / muted | inactive, "not designed to", dissolved | greyed capabilities, logoff desktop, closed ports |

Discipline: don't let blue "do everything". If a scene has no security/network/climax concept, most of it
is blue + neutrals, and that's correct.

### 4.4 Typography
- **Inter** only. Weights: 400 / 500 / 600 / 700 / 800.
- Scale (px on the 1920-wide canvas):
  - **Kicker / eyebrow:** 24, weight 700, letter-spacing ~3, colour `blueDim`, uppercase — e.g. `02 · GATEWAY`.
  - **Headline:** 46–56 (payoff up to 78), weight 800. One **accent word** may take a role colour
    (e.g. "**Zero** inbound ports."). Keep the rest white.
  - **Sublabel / node title:** 26–34, weight 600–700.
  - **Body / caption inside canvas:** 18–24, weight 400–600, colour `muted`.
- The **narration lives in the `VOICEOVER:` caption**, not baked into the frame — unless the on-screen
  headline *is* the point of the scene.

### 4.5 Depth & material (the "techy" layer)
Applied to every navy scene (skip on solid-brand payoff scenes):
- **Background gradient:** vertical `navy → navy2`.
- **Dot-grid:** faint dots (`#5C8FC4` at ~0.09 opacity) on a ~58 px grid → reads like a "system/console".
- **Vignette:** subtle radial darkening at the edges.
- **Glow:** a soft radial halo behind the **focal element**, in that scene's role colour
  (blue / mint / violet / warm). This is the main eye-director.
- **Glass cards:** `card` fill at ~0.66 opacity + 1.6 px role-colour stroke + a 2.4 px white top-highlight
  strip at ~0.12 opacity.

### 4.6 Motif library (reuse — do NOT invent new metaphors)
The base "Youtube" vocabulary plus the techy-pass additions:
- **Shield** — hero for protection/audit. Active = role-colour fill (~0.16) + stroke + check.
- **Tunnel / pipe** — horizontal cylinder with **violet dashed** bidirectional arrows = network traffic / VPN.
- **Diagonal strike** — a bright line across an element = negate / "not designed to" / replace.
- **Compliance pill / chip** — rounded `chip` fill + role-colour stroke + a **check circle** + label.
- **Module cards** — glass card + glyph + title + subtitle (Gateway / Broker / Cloud Manager, etc.).
- **Device/desktop mock** — screen with title bar (`uiBar`) + content lines (`uiLine`); `on` state = blue title bar.
- **Browser mock** — window chrome + traffic-light dots (`#E0637B`/`#E5B94B`/`#2BD9A0`) + URL bar (+ inner desktop).
- **Ports** — a stack of small squares; closed = dim with an ×. (mechanism for "zero inbound").
- **Packets** — small dots riding a dashed connector = live traffic.
- **Seal / tamper-evident** — a mint shield with a check = sealed evidence.
- **Framework badges** — uniform fixed-width chips (SOC 2, PCI DSS, HIPAA, GDPR, ISO 27001, NIS2, FedRAMP…).
- **Thinfinity wordmark lockup** — ring + inner dot + "Thinfinity", used on brand-blue payoff scenes.
- Thin clean strokes, rounded caps, dashed for any flow.

### 4.7 Component vocabulary (the reusable SVG builders)
The recommended authoring path is a small JS helper library that emits SVG strings (guarantees token
consistency and avoids hand-typed hex typos). Canonical builders (see v3/v4 files for the implementation):

`text · kicker · head · headA/headEnd(accent word) · defs(n) · dots · glow(n,cx,cy,r,role) ·
checkC · chip · glass · card · arrow · flow(packets) · strike · zone · screen(on) · person ·
shield · recDot · webApp · fwBadge(framework) · dimCard(struck) · bigCloud · module glyphs
(gwGlyph/brGlyph/cmGlyph) · scene(n,bg,inner)`

**ID prefixing (hard rule):** every `<defs>` id (gradients, patterns) must be **prefixed per scene**
(`g1bg`, `g2glow`, …) because ids are document-global across the stacked inline SVGs; unprefixed ids cause
silent fill breakage.

---

## 5. Editorial rules
- **One editorial headline per scene** (eyebrow/kicker + bold headline). It sharpens the beat; it never
  replaces or contradicts the VO.
- **Numbered wayfinding kicker:** `NN · SECTION` (e.g. `03 · SESSION RECORDING`) for rhythm and orientation.
- **One focal per frame.** If a scene has >4 competing elements, subordinate or cut until one hero remains.
- **Show the mechanism, don't label it.** Prefer a visual (ports going dark, a packet leaving, a desktop
  dissolving) over a text chip. Reserve chips for genuinely enumerable items (MFA/SAML/OAuth, CAD/3D/ML,
  framework names).
- **Complex → simple, within a frame.** Where the beat allows, let density *resolve* to one clean line
  (many connections → one; many ports → one outbound). This is a graphic treatment of the existing beat —
  **not** an added scene or narrative change.
- **Graphic continuity.** A recurring entity (Gateway, Broker, Cloud Manager, the evidence shield) keeps the
  **same shape + colour** every time it reappears, so the video reads as one system.

---

## 6. Motion / shot-list rules
Storyboards are for **video**, so each keyframe carries a **`Motion:` note** (it's a shot-list, not just
frames). Graphic motion vocabulary (decisions, not script changes):
- **Flowing dashes + packets** along connectors = live traffic.
- **State toggles** (off→on, dim→active), **strike drawn on** to negate, **materialize/dissolve** (particles).
- **Enter/exit** per element (fade/scale-in, stagger), plus an implied **duration** per beat.
- Keep motion in service of the one focal; don't animate everything at once.

---

## 7. Scene grammar & beat→scene decomposition
1. Read the whole script; find its **natural halves / sections** (often a "walkthrough" half and an
   "explainer" half). The user may ask for only one half.
2. **~one sentence = one beat = one scene**, but **consolidate closely-related sentences** into one richer
   scene when they describe the same idea (e.g. the whole Gateway sentence → one scene).
3. Assign each beat a **motif** from §4.6 and a **role colour** from §4.3 before drawing.
4. Keep the source language **verbatim** in the `VOICEOVER:` caption (preserve-source-language rule).
5. Mark **payoff beats** (turns like "does both", "one gateway") as brand-blue duotone scenes.

---

## 8. SVG Figma-safe rules (hard)
- **Allowed:** `<rect> <circle> <ellipse> <path> <line> <polygon> <polyline> <text> <tspan> <g>
  <linearGradient> <radialGradient> <defs>`.
- **Forbidden** (Figma drops them silently on import): `<foreignObject> <image>` (incl. base64 data URIs),
  external `<use>`, external URL refs, `<pattern>` (bake the dot-grid as real `<circle>`s instead), and CSS
  `<style>`/classes for SVG geometry.
- Escape `&`→`&amp;`, `<`→`&lt;`, `>`→`&gt;` inside `<text>`. Prefix all ids per scene (§4.7).
- Use `gradientUnits="userSpaceOnUse"` (or `objectBoundingBox` consistently) — don't mix.

---

## 9. Authoring workflow
1. **Read this spec** + the target voiceover.
2. **Decompose** the script into beats/scenes (§7).
3. **Build** the HTML preview: a JS helper library (§4.7) + one builder per scene, emitting inline
   `<svg viewBox="0 0 1920 1080">`. Page wrapper is dark; each scene is a card with the SVG then a caption bar
   (number + `VOICEOVER` + `Motion`).
4. **Render & verify** (§10) — read the PNG against this spec (roles correct? one focal? glow on focal?
   Figma-safe? captions present?). Iterate.
5. **Open** it in the user's browser for review (`start "" "<abs path>"`; opens a new tab).
6. On approval, **push to Figma** "Youtube" (`K8rHguGyksdPWdHrSA3VOi`) via `generate_figma_design` following
   the project's Figma workflow (capture script, `outputMode: existingFile`, poll `captureId`).
7. If run inside the Cybele Console, save outputs to `jobs/<id>/output/v<N>/` (pipeline key `storyboard`).

---

## 10. Render / verify recipe
Edge headless, full-page screenshot. **Use an ABSOLUTE path for `--screenshot`** (relative fails with
"Access denied"):
```bash
OUT="C:/abs/path/preview.png"
"/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
  --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1120,<tall-enough> \
  --screenshot="$OUT" "file:///C:/abs/path/storyboard.html"
```
- Height ≈ 180 (header) + ~680 px per scene. The tall PNG downscales when read — **crop it into chunks**
  with Pillow (`py -3.13`) and read each chunk to inspect detail:
  ```python
  from PIL import Image
  im=Image.open('preview.png'); w,h=im.size
  for i in range(N): im.crop((0,i*(h//N),w,(i+1)*(h//N))).save(f'chunk_{i}.png')
  ```
- **Lesson (hand-authored SVG):** grep for invalid/typo hex after writing (`#12booms` etc.). The JS-helper
  path avoids this — prefer it.

---

## 11. HTML preview conventions
- Page: dark bg (`#050C17`), Inter via `@import`, `.grid` max-width ~1080 px centered.
- Each scene: `<div class="scene">` = `<svg class="frame" viewBox="0 0 1920 1080">` + `<div class="cap">`.
- Caption bar: number chip + `VOICEOVER` label + the verbatim line, then a `Motion:` line (blue "▸ Motion ·").
- All scenes share the 1920×1080 coordinate system → 1:1 portable to Figma frames.
- No `<use>`/components: each scene repeats its primitives inline (Figma-safe, self-contained).

---

## 12. Quality checklist (before showing the user)
- [ ] One focal per scene; glow sits on that focal, in the correct role colour.
- [ ] Colour-with-a-job respected (blue=product, mint=security, violet=network, warm=one climax only).
- [ ] Mechanism shown where possible; chips only for enumerable lists.
- [ ] Editorial headline + numbered kicker present; headline agrees with the VO.
- [ ] Recurring entities keep the same shape+colour across scenes.
- [ ] `VOICEOVER` verbatim; `Motion` note present.
- [ ] Figma-safe (no forbidden nodes; ids prefixed per scene; hex all valid).
- [ ] Rendered & visually verified against this spec.

## 13. File naming / versioning
- `storyboard_v<N>_<slug>.html` in the working dir (or `jobs/<id>/output/v<N>/`). Never overwrite a prior
  version — keep v1, v2, … for side-by-side comparison. `<slug>` names the script (e.g. `contractor_desktop`,
  `ztna_audit`).

## 14. Status & next steps
🟡 **In progress.** The style spec and console instance exist; the flow is **not yet packaged as a Claude
skill**. Next step: package `cybele-video-storyboard` (mirroring `cybele-blog-visuals` /
`thinfinity-architecture`) — codify this spec + the §4.7 helper library, add a small set of calibration
storyboards from real VO scripts, and wire it as the `storyboard` pipeline's execution.

---

## 15. Appendix — worked examples (beat → visual maps)

### A. "How a contractor gets a desktop" (second half — v2/v3)
| # | Beat | Visual (role colour) |
|---|------|----------------------|
| 1 | What makes that possible is three modules | 3 glass module cards, flow + packets (blue) |
| 2 | Gateway is outbound-only reverse proxy, zero inbound, never public | Gateway (blue, glow); **ports off** + one **outbound packet**; struck public internet; **private fleet** (mint zone) — *mechanism, not chips* |
| 3 | Broker routes to the right pool, RBAC | Broker (blue, glow) → routing bus → 3 pools; **RBAC** chip (mint) |
| 4 | Cloud Manager provisions/scales/retires; golden images, roaming profiles, autoscaling | Provision→Scale→Retire cycle + **automatic** loop arc; 3 mint chips |
| 5 | Every desktop model, from one gateway | **Brand-blue payoff** + Thinfinity lockup; duotone headline; **warm** underline (climax) |
| 6 | Ephemeral, created at logon / destroyed at logoff, minimal data at rest | logon desktop (blue glow) → **dissolves to particles**; "data at rest" (mint) |
| 7 | GPU shapes for CAD/3D/ML | GPU desktop (blue glow) + CAD/3D/ML chips |
| 8 | Persistent/pooled/published + raw RDP/SSH/VNC | model cards (blue) + protocol cards (**violet**) |

### B. "ZTNA vs Thinfinity — recording & audit evidence" (v4)
| # | Beat | Visual (role colour) |
|---|------|----------------------|
| 1 | Network-layer ZTNA controls web-app access, not full desktop / not recording | **ZTNA (violet)** → web app; two capabilities **dim + struck** ("not designed to") |
| 2 | Thinfinity does both | **Brand-blue payoff**; both capabilities lit + mint checks |
| 3 | Every session recorded (keystrokes/screen/clipboard/file transfers), tamper-evident | session + **REC**; 4 capture chips → **mint sealed shield** |
| 4 | Evidence supports the controls auditors test: SOC 2, PCI DSS, HIPAA, GDPR, ISO 27001, NIS2 | mint evidence shield → **6 framework badges** (mint) |
| 5 | + FedRAMP on Oracle Cloud Government | evidence → Oracle Cloud Government (blue) → **FedRAMP badge in warm** (the single climax) |

---

*Related project docs:* `progress.md` → "Video Storyboard Pipeline"; the "Youtube" Figma file
(`K8rHguGyksdPWdHrSA3VOi`); the Cybele brand system (`BRAND_DESIGN_RULES.md`, palette 06/26, Inter,
borderless/shadowless/low-contrast).
