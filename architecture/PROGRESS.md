# Architecture Diagrams

Thinfinity/Cybele architecture diagrams as native, Figma‑safe **SVG** in the official **"pill" visual system**. Packaged as the **[`thinfinity-architecture`](../skills/thinfinity-architecture)** skill (the skill's `SKILL.md` is authoritative). Brand basics → [`_shared/BRAND.md`](../_shared/BRAND.md). Provenance/notes: [`thinfinity_arch_skill_handoff.md`](thinfinity_arch_skill_handoff.md).

> This is **technical diagramming from fixed atoms on a grid**, not editorial illustration. Consistency is the point — follow the construction rules exactly.

## Construction rules (the vocabulary)

- **Pill (one atom for everything):** uniform **160×43**, 1.5 px solid border, radius 7, **white fill always**, icon 23×23 at (10,10), text start x=39, Inter 12 px. **No size variants.** Category = **stroke + text color only**: Thinfinity `#0A74D6` · User `#373737` · Secondary stroke `#BDBDBD`/text `#373737`. The icon takes the pill's colour: `#0A74D6` in Thinfinity pills, `#373737` everywhere else (2026-09-28; it used to keep its native colour, which made AD and TLS green).
- **Zones = dashed containers** (`stroke-dasharray="6 4"`, radius 10–12, transparent) marking a network/site/tier; label = icon + 13 px text top‑left (or a corner badge). **Hard rule: no dashed‑inside‑dashed** — subnets/pools become pill rows with a text label. Only exception (2026‑09‑28): an **environment zone** may hold network zones.
- **Environment zones (2026‑09‑28, SKILL §2.2b):** colour marks where things are hosted — customer/on‑prem `#3DCCA1` on `#F5FCFA`, cloud `#8878ED` on `#F9F8FE`, hosted by Cybele `#0A74D6` on `#EFF7FE`; dashed intense stroke, soft fill; network zones stay gray inside. Cloud sites use the `cloud-inf` icon, never the building. Also settled that day: blue reference arrow, 4 px air at every chevron, port labels (only when asked) on the line in a stroked pill, neutral IN/OUT chips — see SKILL §11–12 and `reference/ports_and_firewall.md`.
- **Connector = open chevron stroke** in **azure `#0AA9FF`** (NOT `#0A74D6`, NOT a filled triangle), width 2, orthogonal routing, buses for converge/distribute. Dashed connector = secondary/support flow (IDP auth, mgmt, backup).
- **≥14 px straight run before any arrowhead**; arrowheads into one element ≥14 px apart. **Edge centering** — single‑arrow edges enter/exit at the edge center; multi‑arrow edges offset symmetrically.
- **Layer order (hard):** zones → connectors → pills (else arrowheads get hidden).
- **Gaps ≈ 43 px** (one pill‑height); widen only dense crossing zones. Default is **monochrome**; per‑flow color‑coding is opt‑in only.
- **Mandatory:** in‑SVG **reference footer** (legend travels with the SVG) + a **pre‑render distance check** (two passes) before declaring done.

## Product knowledge (capability → topology)

Invariants the skill applies even when unspoken: reverse connection / no inbound ports (arrows point to the Gateway); Gateway in DMZ/Cloud; Broker in the corporate net with resources; clientless browser access; HA = Primary + Secondary Broker; TLS 1.3/443; multi‑region = per‑region Comm Gateway + Sec Broker; multi‑domain = per‑domain Primary Broker; IDP auth drawn dashed; managed/DaaS = "Managed by Cybele Software" hub‑and‑spoke. Recipes **R1–R11** in `reference/thinfinity_reference_architecture.md`.

**Official Figma catalog (source of truth).** `reference/official_figma_catalog.md` indexes ~60 real Cybele architecture diagrams from the official Figma file (`fileKey W3Pnm739iwmVdo3hSaBNQe`) with their node IDs, plus new component/zone vocabulary, extended visual conventions, and the named‑topology catalog **R12–R33**: Single Machine (R12), Gateway/Broker split + separation (R13/R14), ownership models On‑Prem/Hybrid/Fully‑Hosted/BYOD (R15), single‑tenant farm (R16), Single Datacenter HA (R17), Load‑Balancing variants (R18–R21), Failover/DR (R22), Multiple Networks (R23), Multi‑Domain/Multi‑Tenant (R24–R25), Single‑DB (R26/R27), RBAC (R28), Behind Palo Alto (R29), IT/OT (R30), OT & Offline (R31), WAG (R32), and **Zero Inbound Ports / ZTNA on OCI (R33)**. For any named or ambiguous topology, find the closest entry there and open its nodeId in Figma to calibrate before drawing. Key finding: **no official or customer diagram uses per‑protocol color‑coding** — clients are monochrome blue; color‑coding stays opt‑in only.

## Build & self‑check

Emit one SVG (`<defs>` markers → zones → connectors → pills → reference footer) wrapped in the HTML preview scaffold; render headless (Edge) → read the PNG → verify (uniform pills? no hidden/overlapping arrowheads? ≥14 px runs? footer doesn't overlap pills? centered single‑arrow edges?) → iterate. Optional push to Figma via `generate_figma_design` (needs fileKey+nodeId).

```powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu `
  --hide-scrollbars --window-size=<W>,<H> --screenshot="<out>.png" "file:///<path>.html"
```

## Native diagrams inside PPTX
For presentation decks, diagrams are drawn **natively** so they look like this task's output. Since 2026‑09‑28 the full rules live in [`web-app/data/progress.md`](../web-app/data/progress.md) › PPTX Generation Pipeline › "Architecture diagrams in a deck", with the reference builder in [`presentations/reference_builder/`](../presentations/reference_builder/). The 2026‑06 description (scale‑driven engine, one pill width per diagram, gap = pill‑height, edge‑centered connectors) still holds. Icons are rendered from the skill's 131‑icon set (132 SVG incl. `_arrow.svg`) to PNG.

## Calibration set
8 validated diagrams (basic → hybrid → full reference → multi‑region color‑coded → IDP/domains → VDI pools+backup → managed hub → **zero‑inbound / ZTNA on OCI**) in `skills/thinfinity-architecture/examples/` + `reference/` (`ex01…ex08_*.png`). `ex08_zero_inbound_ztna.png` / `test_08_zero_inbound_ztna.html` is the canonical R33 reference.
