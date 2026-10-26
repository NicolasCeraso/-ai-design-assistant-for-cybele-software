---
name: thinfinity-architecture
description: >
  Generates Thinfinity (Cybele Software) architecture diagrams as native, Figma-compatible SVG in the
  official Cybele "pill" visual system. Use this skill whenever the user asks to create, draw, generate,
  diagram, or "make a graphic of" a Thinfinity / Cybele architecture — e.g. a deployment topology,
  reference architecture, network diagram, gateway/broker/IDP layout, VDI/DaaS topology, multi-region or
  multi-tenant setup — or asks to convert/redraw an existing architecture image into the Cybele style.
  Output is a standalone SVG + an HTML preview (optionally pushed to Figma). Default style is monochrome;
  per-flow color-coding is an opt-in exception only when the user explicitly asks for it.
---

# Thinfinity Architecture Diagram Generator

You turn a description (or an existing architecture image) into a **Thinfinity architecture diagram** built
from a small, strict visual vocabulary: uniform **pills**, dashed **zones**, and chevron **connectors**.
The system was reverse-engineered from Cybele's official Figma and validated across 8 diagrams of
increasing complexity. Follow the rules below exactly — consistency is the whole point.

You are NOT illustrating freehand. You are assembling a diagram from fixed atoms on a grid.

---

## MANDATORY FIRST STEP — load context

All assets are bundled alongside this `SKILL.md`:

- `icons/` — **131 brand SVG icons** + `_arrow.svg` (the canonical connector). Native viewBox 23×23, brand
  colors baked in via `var(--fill-0, …)` fallback. Use these by inlining (see §6).
- `reference/atoms_spec.png` — the atom catalog (pills, zones, connector, palette).
- `reference/ex01…ex08_*.png` — 8 validated diagrams. **Browse these for calibration before drawing.**
  `ex08_zero_inbound_ztna.png` is the canonical **Zero Inbound Ports / ZTNA on OCI** reference (recipe R33).
- `reference/thinfinity_reference_architecture.md` — **product knowledge (capa 3): component catalog,
  zone catalog, product invariants (I1–I18), capability→topology mapping, and recipes R1–R11**. Load
  when the prompt is **conceptual** (talks about capabilities, not concrete components) — this doc
  derives the topology before you draw.
- `reference/official_figma_catalog.md` — **the canonical source-of-truth: an index of ~60 real Cybele
  architecture diagrams** in the official Figma file (`fileKey W3Pnm739iwmVdo3hSaBNQe`) with their node
  IDs, the **named-topology catalog R12–R32**, new component/zone vocabulary, and extended visual
  conventions (§3 there). **Load this whenever the prompt names a topology** (Single Machine, Failover,
  Multi-Tenant, Behind Palo Alto, IT/OT, WAG, On-Prem/Hybrid/Fully-Hosted/BYOD, OCI VDI, RBAC, ZTNA,
  detailed IDP integration…) **or is ambiguous** — find the closest official diagram, then
  `get_screenshot` its nodeId to calibrate before drawing.
- `examples/*.html` — the exact source of those 8 diagrams. **Copy/adapt their structure; don't reinvent.**
  `examples/test_08_zero_inbound_ztna.html` is the worked source of R33 (zero-inbound / ZTNA on OCI).

The richest single calibration pair is `examples/test_03_full.html` (linear, uniform) and
`examples/test_07_managed_hub.html` (radial); `examples/test_08_zero_inbound_ztna.html` is the model for a
clean ZTNA "no inbound listener" topology. Read at least one before generating. For conceptual
prompts (OT vendor access, manufacturing VDI, "multi-region with PAM", etc.) also read
`reference/thinfinity_reference_architecture.md` §5 (capability→topology) and §6 (recipes).

---

## 1. The atom — the **pill** (one shape for everything)

Every concrete component is a pill. There is **one size**. Do not vary it.

| Property            | Value |
|---------------------|-------|
| Width × Height      | **160 × 43** |
| Border              | **1.5 px solid** (color = category, below) |
| Corner radius       | **7** |
| Background          | **#FFFFFF** (always — never tint solid pills) |
| Icon                | **23 × 23** at local `(10, 10)` |
| Text start x        | **39** (icon 23 + gap 6) |
| Text                | Inter, **12 px**. 1 line → baseline `y=27`. 2 lines → baselines `y=22` and `y=35`. |
| Text color          | = category |

Two-line labels break at a natural word boundary (e.g. `Thinfinity` / `Gateway`, `Virtual Desktops` /
`& Virtual Apps`). Keep each line ≲ 16 chars so it fits inside 160 px.

### 1.1 Pill categories — communicated ONLY by stroke + text color

| Category   | Stroke + text          | Used for |
|------------|------------------------|----------|
| **Thinfinity** | `#0A74D6` (Cybele blue) | Thinfinity components: Gateway, Primary/Secondary Broker, Agent, IDP, Comm Gateway |
| **User**       | `#373737` (dark)        | Human actors / endpoints: User, Remote User, End User, Web Browser / Client / PWA |
| **Secondary**  | stroke `#BDBDBD`, text `#373737` | Peripheral infra: Firewall, Tunnel (TLS), Database/Backup, Terminal/Linux/App/VDI servers, target resources |

> **Superseded 2026-09-28 (Nick):** the icon **takes the pill's colour**: `#0A74D6` in Thinfinity pills,
> `#373737` in every other pill (§6). It no longer keeps its native colour, which is how Active Directory
> and TLS came out green. Box stroke + label text still carry the category colour.

---

## 2. Zones — dashed containers

A **zone** groups pills that share a context (a network, a DMZ, a site, an access tier).

| Property | Value |
|---|---|
| Border | **1.5 px dashed**, `stroke-dasharray="6 4"` |
| Radius | 10–12 |
| Fill | none (transparent) by default |
| Label | icon (22 px) + text (13 px, weight 500) at top-left inset `(zone_x+18, zone_y+15)` for icon, text at `(zone_x+47, zone_y+31)` |

### 2.1 Internal spacing (uniform across all zones)
- Pills sit at **`zone_y + 48`** (clears the top-left label) and **`zone_x + 20`** (left pad).
- A single-pill zone uses the SAME layout: label at top, pill at `zone_y+48`. (Do not center the pill over
  the label — they overlap. This was a real bug.)
- Multi-pill rows: stride 203 horizontally (`160 + 43`), 56–58 vertically.

### 2.2 Canonical zone types (border color stays gray `#BDBDBD` by default; the icon names the type)
| Zone | Icon | Notes |
|---|---|---|
| Remote Access / IDP Integration | `remote-access` / `id` | endpoint tier |
| DMZ / Cloud or DMZ | `connect` | gateway tier |
| Network / Internal Network / Corporate Domain | `premises` or `network` | resource tier |
| Cloud | `cloud` | cloud-hosted site (may use a corner badge instead of a label — see §2.4) |
| Site / region in a cloud (e.g. OCI sites) | `cloud-inf` | cloud infrastructure (Nick, 2026-09-28). The building `premises` means on-prem / customer infrastructure only — never on a site that lives in a cloud. |

### 2.2b Environment zones — where things are hosted (Nick, 2026-09-28)
Colour marks **where** something is hosted, and only that. Values read from the official Figma
"Architecture sample: Hybrid" (`W3Pnm739iwmVdo3hSaBNQe`, node `428:4159`); the dashed line is Nick's
rule: dashed lines are for environments and networks.

| Environment | Stroke (dashed, 1.5 px, intense) | Fill (soft) | Label text | When |
|---|---|---|---|---|
| Customer infrastructure / on-premises | `#3DCCA1` | `#F5FCFA` | `#373737` | on-prem, the customer's own sites (icon `premises`) |
| Cloud | `#8878ED` | `#F9F8FE` | `#373737` | a cloud (OCI, Azure, AWS, GCP, IONOS) the customer runs (icon `cloud`) |
| Hosted by Cybele | `#0A74D6` | `#EFF7FE` | `#0A74D6` | Cybele runs it ("Managed by Cybele", fully hosted / SaaS) |

- Use them only when the hosting location is part of the story: case data `Nube o entorno` (a cloud →
  violet, `On-premises` → green, `Híbrido` → green + violet side by side, `Hosteado por Cybele` →
  blue). With no hosting info, draw no environment zone.
- **Functional / network zones** (Edge, DMZ, Control Plane, Identity, Sites, subnets) stay as in
  §2.2: gray `#BDBDBD` dashed, no fill, and sit **inside** the environment that hosts them.
- Everything outside any environment (the Internet, end users) stays outside, uncoloured.
- Never colour pills or icons with these hues: they belong to the environment containers only.
- **Strict green (Nick, 2026-09-28):** some official Figma diagrams also paint green:
  - tenant or network sub-zones (R23 Multiple Networks, R25b per-customer tenants, R28 RBAC);
  - a collector bus to a shared database (R26).

  **Do not reproduce that.** Green means only "customer infrastructure / on-prem" (the environment
  zone above). Draw those sub-zones as gray network zones and that bus in connector blue `#0AA9FF`.
  The same goes for violet and blue: they mean cloud and hosted by Cybele, and nothing else.
- **"Managed by Cybele"** is drawn as the blue hosted-by-Cybele environment. Figma sometimes nests a
  violet cloud box inside a blue "Managed by Cybele" box; one blue environment is enough (Nick,
  2026-09-28).

### 2.3 NO NESTED DASHED CONTAINERS  ⛔ (hard rule)
The one exception is §2.2b: an **environment zone may contain network zones**, one level deep
(environment → network), and nothing deeper. Apart from that, a dashed zone with elements inside
must **not** contain a smaller dashed box. The big dashed zone IS the marker. So:
- Resource pools / subnets / "Network N" become **plain pill rows with a text label**, not sub-boxes.
- "Corporate Domain + Network 1" collapses into ONE zone labelled `Corporate Domain · Network 1`.
- An outer "Managed by Cybele Software" wrapper becomes a **title pill header**, not a box, so the inner
  zones can stay dashed.

### 2.4 Zone badge (alternative to a top-left label)
For cloud sites you may drop the label and place a **corner badge** (a 22 px icon in the outer-bottom
corner), matching the source diagrams. If you do, give the zone ~30 px of bottom margin so the badge does
**not** overlap the pills inside it. (Overlapping badge = bug; was reported.)

### 2.5 Dashed ZONE-PILL variants (only when a zone is represented as a single labelling pill, not a container)
Same pill box but `border-dashed` + a tinted fill. Use these as standalone zone labels, never nested in a
dashed container.
| Zone | Stroke | Fill | Text | Icon |
|---|---|---|---|---|
| Cloud | `#8878ED` | `#F9F8FE` | `#373737` | `cloud` |
| On-Prem / customer | `#3DCCA1` | `#F5FCFA` | `#373737` | `premises` |
| Hosted by Cybele | `#0A74D6` | `#EFF7FE` | `#0A74D6` | `cloud` |

(Corrected 2026-09-28 to the Figma Hybrid sample and §2.2b: cloud is violet and on-prem is green —
the old table had them swapped — and there is no separate "Hybrid" colour: hybrid = both shown.)
| DMZ | `#BDBDBD` | white | `#373737` | `connect` |
| Network | `#BDBDBD` | white | `#373737` | `network` |

---

## 3. Connectors

Default connector = the canonical `_arrow.svg` style: a thin line + an **open chevron** arrowhead drawn as a
**stroke** (NOT a filled triangle).

- Stroke color: **`#0AA9FF`** (azure — NOT the Cybele `#0A74D6`).
- Stroke width: **2**.
- Arrowhead marker (reuse verbatim):
  ```svg
  <marker id="tip" viewBox="0 0 14 18" refX="11.5" refY="9" markerWidth="14" markerHeight="18"
          orient="auto-start-reverse" markerUnits="userSpaceOnUse">
    <path d="M2 2 L11.5 9 L2 16" fill="none" stroke="#0AA9FF" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
  ```
- Routing: orthogonal (H/V segments). Buses converge/distribute (e.g. 3 users → one bus → gateway).
- **Dashed connector** (`stroke-dasharray="5 4"`, width 1.5, usually no arrowhead) = a *secondary/support*
  flow distinct from the main data flow: IDP→broker auth, management, backup, etc.

### 3.1 Arrow geometry rules (hard)
- **≥ 14 px straight run before any arrowhead** — no bend/curve sitting right at the tip. (14 px = the
  arrowhead width.)
- **Arrowheads entering the same element must be ≥ 14 px apart** (≈ the arrowhead height). If an element
  takes several arrows, distribute them across its edges (left-upper / left-lower / right / top / bottom).
- Don't squish crossing flows: where many flows converge/distribute (a gateway fanning to N targets, plus
  flows crossing through), **widen that gap** above the standard 43 px so each flow gets its own lane.
  Legibility beats compactness in dense crossing zones.

### 3.2 Flow direction
Default: arrows point **toward the gateway** (Thinfinity's reverse-connection / "no inbound port" model):
endpoints → gateway, brokers → gateway, resources → broker. Match the source image when it clearly shows a
different intent.

### 3.3 Edge centering (hard)
**Every arrow enters/exits a pill at the CENTER of its edge** — left/right edge mid `y = pill_y + 21.5`,
top/bottom edge mid `x = pill_x + 80`. This is the default and is not negotiable for single-arrow edges.

When an edge takes **≥2 arrows**, offset them **symmetrically around the center**, with **≥14 px between
adjacent arrows** (14 px = chevron width — below that, the chevrons visually touch). E.g. 3 arrows on a
bottom edge centered at `x_c`: positions `x_c-20, x_c, x_c+20` (20 px spacing).

A common subtle bug: a source pill exits at a center-offset (justified by multi-arrow on its edge), then
the straight horizontal line lands on the target pill **off-center**. Fix by adding a small bend (4–8 px
jog) **before the chevron** so the target entry is at its edge center. The final straight after the bend
must still be ≥14 px (§3.1). **The "centered" requirement applies to BOTH endpoints, independently.**

### 3.4 Convergence and bifurcation (explicit patterns)
When the user describes N sources funnelling into 1 destination, or 1 source fanning out to N
destinations, draw the topology — don't draw N parallel arrows.

**Convergence** (N sources → 1 destination, ONE arrowhead):
- Each source emits a line to a shared bus point (no arrowhead on the inputs).
- A single arrow with chevron exits the bus toward the destination's edge center.

**Bifurcation** (1 source → N destinations, N arrowheads):
- A single line exits the source's edge center to a shared bifurcation point (no arrowhead on the trunk).
- From the bifurcation point, N branches — each with chevron — enter their destination's edge center.

For asymmetric bifurcation (one destination blocked by the other, e.g. AD → 2 stacked VDIs), keep one
branch as a straight continuation of the trunk; route the other branch **around the blocker via outside
the zone** (right of zone right-edge, or left of zone left-edge), then back in to the destination's
center.

---

## 4. Layer order (hard rule — fixes hidden arrowheads)
Draw in this z-order, always:
1. **Zones** (dashed rects + labels) — background.
2. **Connectors** — middle (so chevrons sit on top of zone fills).
3. **Pills** — top (so connector ends tuck cleanly under pill edges).

If you draw a zone after a connector, the zone fill hides the arrowhead. This was a real bug.

---

## 5. Spacing / layout grammar
- **Gap between adjacent containers ≈ 43 px** (one pill-height). Keep it tight; long empty arrows are wrong.
- Reduce distance between element groups — arrows should be short and purposeful, never long across empty
  canvas.
- Outer canvas: a white rounded card (radius 14) on a light `#f5f5f5` page; ~40 px padding. Diagram title as
  an uppercase caption or a `#EFF7FE` rounded "pill" header for an overarching label (e.g. "Managed by
  Cybele Software").
- **Mirroring**: when a broker/hub faces the centre from the right side of its group, mirror the group
  (resources outer, broker inner). Both mirrored and normal groups must read identically — a mirrored group
  is a clean reflection, with its convergence arrow still pointing INTO the broker.
- Recurring macro-patterns (see examples): user bus → firewall/tunnel pill → gateway → broker → resources;
  per-region bands; per-domain zones; hub-and-spoke with a vertical trunk to bottom rows; resources→broker
  via a bus below the row (give it ~30 px so the up-arrows breathe).

### 5.1 Extended conventions from the official Figma (see `reference/official_figma_catalog.md` §3)
The official diagrams use a few extra idioms — pull the full detail from the catalog, but the high-value ones:
- **Scale-out ellipsis `⋮` / `•••`**: two identical rows + an ellipsis = "repeat N" (pools, VMs, brokers).
  Use it instead of drawing every instance.
- **Explicit wire pills**: `TLS 1.3 Traffic Port 443` (ingress) and `TLS 1.3 Traffic No Inbound Port`
  (the reverse Gateway↔Broker hop). Synonyms for the reverse direction: `Only Outbound Connections`,
  `Firewall No Inbound Port(s)`, `TLS 1.3 Outbound Traffic`. These reinforce I1 with a label, not just an
  arrow. In austere client diagrams the return path is a **blue loop bus** above+below the gateway/broker
  cluster, with `WAF`/`Firewall` drawn as labelled **dashed vertical lines** (not boxes).
- **Ownership/deployment encoding** (On-Prem/Hybrid/Fully-Hosted/BYOD): label = `Managed by Cybele` vs
  `Managed by Customer`; the location is an environment zone (§2.2b): green + building (customer /
  on-prem), violet + cloud (cloud), blue (hosted by Cybele).
- **`Thinfinity Agent` is its own pill** (icon `thinfinity`), placed next to each resource it registers —
  distinct from the Gateway. Software-stack order inside a host: Agent → Gateway/Broker →
  Virtualization Process → Desktop/Remote Apps.
- **Client diagrams are monochrome blue** — never auto-apply protocol color-coding (stays opt-in, §8).

---

## 6. Icons
131 SVGs in `icons/`. Inline them (don't `<image href>` an external file if you need to tint, and never use
`<image>` of an icon whose color must change — external SVGs can't be recolored from the parent). For a
normal pill, `<image href="icons/NAME.svg" x="10" y="10" width="23" height="23"/>` is fine only when the
file already has the pill's colour (the files are `#373737`; Thinfinity pills need `#0A74D6`, so inline
those). To **tint** an icon (e.g. a region-colored globe), inline it as a `<symbol>` with
`fill="currentColor"` and set `color` on the `<use>`.

Common mappings: `gateway` (Gateway), `broker` (Primary/Secondary Broker), `thinfinity` (Agent/IDP flower),
`html5` (Web Browser/Client/PWA), `user`/`user-group` (users), `remote`/`remote-access` (remote users),
`premises` (on-prem/building), `firewall`, `vpn-tunnels` (TLS tunnel), `connect` (DMZ), `network`,
`cloud`/`cloud-azure`/`hybrid`, `server`/`app-server`/`broker-monitor` (servers), `vm`/`vdi`/`daas`
(virtual desktops/apps), `terminal`/`ssh-connection`/`vnc` (terminal/protocols), `web-app`/`app-web`
(web apps), `windows`/`linux`/`hyper-v` (platforms), `database`/`databases` (DB/backup),
`active-directory`/`entra-id`/`auth0`/`saml`/`forgerock`/`google`/`duo` (IDPs), `printer`, `monitor-VM`,
`desktop`, `id`.

**Icon colour follows the pill, never the icon file** (Nick, 2026-09-28): Thinfinity pills (Gateway,
Broker, Agent, Thinfinity IdP…) → icon `#0A74D6`; **every other pill → icon `#373737`**, including
identity (Active Directory, Entra ID…), security (shield, firewall) and wire pills (`TLS 1.3 …`).
No green, violet or orange icons: those hues are for environment zones only (§2.2b). The files in
`icons/` were recoloured to `#373737` to match; if an icon still carries another colour, recolour it
when inlining.

---

## 7. Color palette (tokens)
`colors/main #0A74D6` · `Thinfinity/500 #007DC1` · `typography/title #373737` ·
`typography/paragraph #515151` · `Grey/300 #BDBDBD` · `White #FFFFFF` · **connector `#0AA9FF`** ·
`blue/100 #CDDDFA` · `water-green/600 #2FB18A` · `water-green/100 #E2F7F1` · `blue-violet/500 #8878ED` ·
`blue-violet/100 #EDEBFC` · `green/600 #649B1F` · `orange-cybele/500 #FAA928` · header fill `#EFF7FE`.
Environment zones (§2.2b): customer `#3DCCA1` / `#F5FCFA` · cloud `#8878ED` / `#F9F8FE` · hosted by
Cybele `#0A74D6` / `#EFF7FE` (stroke / fill).

---

## 8. Color-coding — EXCEPTION, opt-in only
**Default is monochrome**: all connectors `#0AA9FF`, zones gray. Only color-code flows when the user
explicitly asks (e.g. "color por región", multi-region/multi-tenant where flows must be told apart). Then:
- Each flow gets a color end-to-end; the zone border + label + its globe/icon take that flow's color.
- Suggested flow palette: green `#43A047`, orange `#FAA928`, red `#E5352B`, plus central/shared `#0AA9FF`.
- Provide one marker per color (clone the `tip` marker with the new stroke).
- A "dual flow" original (e.g. blue control plane + colored session planes) needs BOTH sets of arrows;
  remember some elements emit **more than one arrow** (a browser: blue→gateway + colored→comm-gateway).
- Confirm exact hexes with the user if brand-exact values matter; otherwise use the suggested palette and say so.

---

## 9. Build procedure
1. Parse the request (or source image) into: endpoints, gateway(s), broker(s), IDP, resources, zones, and
   the flows between them. Decide default monochrome vs. explicit color-coding.
   **For conceptual prompts** (capabilities, not components): consult
   `reference/thinfinity_reference_architecture.md` — §5 maps capabilities to components, §3 lists
   the invariants I1–I18 that apply automatically (even if the user doesn't mention them), and §6
   has the recipes R1–R11 to pick the closest topology starting point.
2. Lay out on a grid: assign each pill an `(x, y)`; keep ~43 px gaps; align rows; plan buses; widen dense
   crossing gaps.
3. Emit ONE SVG: `<defs>` markers (including `tip-ref` for §11) → zones → connectors → pills → **reference
   footer §11** (the layer order from §4, with the footer as an additional bottom layer inside the SVG).
   Use `viewBox`, `font-family="Inter, system-ui, sans-serif"`.
4. Wrap in the HTML preview scaffold (copy an `examples/*.html`).
5. **Run the §12 pre-render distance check** against the SVG — every arrow / pill / zone-label / footer.
   Fix any violation and update the SVG.
6. **Render & self-check** with headless Edge, then READ the PNG and confirm visually (uniform pills? no
   hidden/overlapping arrowheads? ≥14 px straight runs? footer doesn't pisar pills? centered entries on
   single-arrow edges?). Iterate until clean.
   ```powershell
   & "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu `
     --hide-scrollbars --window-size=<W>,<H> --screenshot="<out>.png" "file:///<path>.html"
   ```
7. Open the HTML for the user (`Start-Process <path>.html`) and report the file paths.

### Output
- Standalone **SVG** (icons inlined) + the **HTML preview**. Write them to the output directory the
  caller gives (for a task from the Cybele Project Console that is `jobs/<id>/output/v<N>/`); with no
  path given, use a folder under the current working directory. Always report the actual path.
- **Inside a PPTX deck:** native editable PowerPoint shapes. The deck-specific rules live with the
  other deck rules, in the console's `web-app/data/progress.md` › PPTX Generation Pipeline ›
  "Architecture diagrams in a deck". The reference implementation is
  `presentations/reference_builder/build_script.py`.
- **Push to Figma** only if the user gives a `fileKey`+`nodeId`. **Icons must land as design-system
  component instances, not loose vectors** (the design team operates and swaps them in Figma). So do NOT push the
  SVG/HTML through `generate_figma_design` (it flattens every icon to a vector). Instead build the
  diagram natively with `use_figma` (load `figma-use` first, `create_session` before it): pills,
  zones and connectors as frames/auto-layout per this skill's geometry, and each icon via
  `search_design_system` -> `componentKey` -> `importComponentSetByKeyAsync` (variant `light`) or
  `importComponentByKeyAsync` -> `createInstance()`, fixed square size, recoloured per §6 by mapping
  `fills` and `strokes` of the instance's descendants. The SVG remains the standalone deliverable.
  If the user explicitly wants the quick vector push, use `generate_figma_design` and say that the
  icons will arrive as vectors.
- **Labels follow the prompt's language** (English default — matches the source diagrams).

---

## 10. Pitfalls (all were real mistakes — do not repeat)
1. Don't infer colors. If a value isn't in the palette (§7) or given, ask before inventing.
2. Pills are **always 160×43**. No size variants.
3. Thinfinity pills are **white with blue stroke**, never blue-filled.
4. The connector is **`#0AA9FF`** with an **open chevron stroke**, not `#0A74D6` and not a filled triangle.
5. When inlining icon SVGs, ensure `preserveAspectRatio` is not `none` (it deforms them).
6. **Layer order zones → connectors → pills**, or arrowheads get hidden.
7. **No dashed-in-dashed**, except environment → network (§2.2b). Flatten any other nesting.
7b. **Icons:** `#0A74D6` in Thinfinity pills, `#373737` everywhere else — no green/violet icons (§6).
8. Single-pill zone: label at top, pill at `zone_y+48` (don't overlap them).
9. Keep gaps tight (~43 px); widen only dense crossing zones.
10. Corner badges must not overlap inner pills — leave bottom margin.
11. ≥14 px straight before any arrowhead; arrowheads into one element ≥14 px apart.
12. Color-coding is opt-in only; default monochrome.
13. **Centered entries / exits on single-arrow edges (§3.3).** A propagated offset from the source's
    multi-arrow edge that lands the line off-center on a single-arrow target is a violation — add a
    4–8 px bend at the end to recover the target's center.
14. **Don't bend an arrow to dodge a zone label.** If a centered arrow lands on top of the zone-label
    text or icon, **move the label** to a corner badge (§2.4). The arrow stays centered.
15. **Every diagram needs the §11 reference footer inside the SVG.** Don't ship a Cybele diagram with
    only an HTML legend below the SVG — the SVG is what gets exported.
16. **Run the §12 pre-render distance check before declaring done.** Two passes minimum: fix any
    violation, re-render, re-check. The 4.5-px-off-center bug is the canonical example of what slips
    through a single pass.

---

## 11. Reference footer (in-SVG legend — mandatory)

Every diagram MUST include a **reference footer inside the SVG** (NOT as a separate HTML `<div class="legend">`
below the SVG — the SVG is the deliverable, and when exported to Figma/PNG/etc. the reference must travel
with it). The footer explains **what arrows mean, what dashed lines mean, and what each color means**.

### 11.1 Position and structure
- `<g transform="translate(60, footer_y)">` where `footer_y ≈ zones_bottom + 60` (well clear of any zone).
- Heading **`REFERENCIA`** at the top: 11 px, weight 500, `#888`, uppercase, letter-spacing `0.05em`.
- Content arranged in **columns**: typically 3 (line styles | color group 1 | color group 2) for diagrams
  with 4 color flows; expand to 4+ columns if more flows. Each column has 2 rows; each row = a 44 px line
  sample + 14 px gap + 11 px label in `#515151`.

### 11.2 Always-present line-style entries (column 1)
| Sample | Label |
|---|---|
| solid arrow with chevron, **connector blue `#0AA9FF`** (the same colour as the diagram's arrows), width 2 (uses `tip-ref` marker) | `Conexión / flujo de datos — la punta indica dirección` |
| dashed line `#BDBDBD`, width 1.5, `stroke-dasharray="6 4"`, no chevron | `Perímetro de red / zona lógica — contenedor de elementos` |

### 11.3 Color-flow entries (one per distinct color used)
For each colored flow in the diagram, add an entry with a 44 px solid line in the flow's color (no chevron
needed in the sample) + a label naming the protocol/purpose. Example for an OCI VDI diagram with 4 flows:

| Sample | Label |
|---|---|
| `#0AA9FF` azure | `User session · HTTPS 443` |
| `#06B6D4` teal | `FSLogix profiles · SMB 445` |
| `#FF7043` orange | `Config DB · MySQL 3306` |
| `#F59E0B` gold | `Directory · LDAP / Kerberos / DNS / SMB / RPC` |

### 11.4 The `tip-ref` marker
Define alongside the per-flow markers in `<defs>`:
```svg
<marker id="tip-ref" viewBox="0 0 14 18" refX="11.5" refY="9" markerWidth="14" markerHeight="18"
        orient="auto-start-reverse" markerUnits="userSpaceOnUse">
  <path d="M2 2 L11.5 9 L2 16" fill="none" stroke="#0AA9FF" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round"/>
</marker>
```

(Nick, 2026-09-28: the reference arrow is blue like the real connectors, not gray.)

### 11.5 Worked SVG template
```svg
<g transform="translate(60, 620)">
  <text x="0" y="-4" font-size="11" font-weight="500" fill="#888" letter-spacing="0.05em">REFERENCIA</text>

  <!-- Col 1: line styles -->
  <line x1="0" y1="14" x2="44" y2="14" stroke="#0AA9FF" stroke-width="2" marker-end="url(#tip-ref)"/>
  <text x="58" y="18" font-size="11" fill="#515151">Conexión / flujo de datos — la punta indica dirección</text>
  <line x1="0" y1="36" x2="44" y2="36" stroke="#BDBDBD" stroke-width="1.5" stroke-dasharray="6 4"/>
  <text x="58" y="40" font-size="11" fill="#515151">Perímetro de red / zona lógica — contenedor de elementos</text>

  <!-- Col 2: flow colors group 1 -->
  <line x1="560" y1="14" x2="604" y2="14" stroke="#0AA9FF" stroke-width="2"/>
  <text x="618" y="18" font-size="11" fill="#515151">User session · HTTPS 443</text>
  <line x1="560" y1="36" x2="604" y2="36" stroke="#06B6D4" stroke-width="2"/>
  <text x="618" y="40" font-size="11" fill="#515151">FSLogix profiles · SMB 445</text>

  <!-- Col 3: flow colors group 2 -->
  <line x1="900" y1="14" x2="944" y2="14" stroke="#FF7043" stroke-width="2"/>
  <text x="958" y="18" font-size="11" fill="#515151">Config DB · MySQL 3306</text>
  <line x1="900" y1="36" x2="944" y2="36" stroke="#F59E0B" stroke-width="2"/>
  <text x="958" y="40" font-size="11" fill="#515151">Directory · LDAP / Kerberos / DNS / SMB / RPC</text>
</g>
```

> If a separate HTML `<div class="legend">` is also useful for local preview redundancy, fine — but the
> SVG-internal footer is the source of truth. Don't omit it just because the HTML below already shows the
> colors.

---

## 12. Pre-render distance check (mandatory before declaring done)

Before reporting a diagram complete, run this checklist against every arrow / pill / zone-label. If ANY
item fails, fix and re-render. **Do not skip the second pass** — the canonical 4.5-px-off-center bug
(an offset propagated through a horizontal line to an unintended-offset entry on the target) is exactly
the kind of subtle violation that only the second pass catches.

| # | Check | How to verify |
|---|---|---|
| 1 | Pills overlap pills? | Stride 56 px vertical / 203 px horizontal — no two pills share any (x, y) extent. |
| 2 | Arrows cross pill bodies? | For each path, check intersection with every pill's bounding box. Crossings only allowed at the entry/exit edge points. |
| 3 | Arrows cross zone-label text? | Path doesn't enter `(label_x_start … label_x_end) × (label_y - 12 … label_y)`. If it does, **move the label to a corner badge** (§2.4) — don't bend the arrow. |
| 4 | Arrows cross zone-label icons? | Path doesn't enter the 22×22 icon box at `(zone_x+18, zone_y+15)` (or the relocated badge position). |
| 5 | Centered entries / exits on single-arrow edges? | Single arrow on a pill edge → enters/exits at the EDGE CENTER. If a propagated offset lands you off-center on the target, add a small bend before the chevron to recover the center. |
| 6 | Symmetric offsets on multi-arrow edges, ≥14 px apart? | When an edge takes ≥2 arrows, positions are symmetric around center with ≥14 px between adjacent positions. |
| 7 | ≥14 px straight before each chevron? | From the path's LAST bend to the chevron tip is ≥ 14 px. No "kink at the tip". |
| 8 | Reference footer overlaps any element? | The footer `<g>` sits at `y > zones_bottom + 30`, inside the card; its own arrow/dashed samples are at the bottom of the canvas where nothing else lives. |
| 9 | All chevrons OUTSIDE pill bodies, with air? | Chevron tips stop **4 px before** the pill / zone / label edge (shorten the path's last segment by 4 px): a small light gap, never touching or overlapping (Nick, 2026-09-28). Chevron arms extend OUTWARD. |
| 10 | Any label covering a connector or a chevron? | A port label sits **on** its line and must leave the line visible on both sides. If the straight segment is shorter than the label + 2×8 px (+ ~13 px for a chevron), **lengthen the segment** by moving pills/zones; never move the label off the line (Nick, 2026-09-28). Real bug: `MySQL :3306` on a 95 px segment hid the whole Broker → Config DB arrow. |

After the check passes, re-render with headless Edge, READ the PNG, and visually confirm. Only then
report the diagram as done.

---

## 13. Provenance
Reverse-engineered from Cybele Figma files `8RBfhSYgaCuo4uM82JqAHL` (canonical atoms) and
`W3Pnm739iwmVdo3hSaBNQe` (132-icon library **and the ~60-diagram "Architecture Diagrams" board** —
indexed in `reference/official_figma_catalog.md`, the source of truth for named topologies R12–R32).
Backstory and open notes were kept in handoff documents (`thinfinity_arch_skill_handoff.md` v1/v2 —
v2 adds §12: fine-grained routing rules, colour-coding palette, reference footer convention — and
`STYLE_SPEC.md`) that live **outside this repo**, on the original author's machine. They are **not**
inputs: everything needed to draw is bundled here (`SKILL.md`, `reference/`, `icons/`, `examples/`).
If you are told to consult one and cannot open it, say so and carry on with the bundled files.
