# Sizing for Advanced mode (users → components)

Use this **only** when the task's case data says `advanced: true` ("Modo Advanced" in the prompt). In
the standard mode nothing here applies: a field left empty is not relevant and is not drawn.

In Advanced mode a sizing field left empty is **not dropped, it is calculated** (Nick, 2026-10-26).
The console already applied this model when the task was created and wrote the result into the
prompt ("Dimensionamiento estimado") and into `job.options.arch.plan`. Use those numbers. This file
exists so that a run started from somewhere else (a deck, an intervention answer) reaches the same
figures, and so the reasoning is on record.

**Source.** The model of Mariano's *Thinfinity Architect v2* (`thinfinity-architect.html`, read on
2026-10-26): bandwidth per user profile, throughput per OCPU, Layer-7 balancer limit and the two
platform presets. Knowledge only, no code. **It is an estimate, not a product spec:** the app itself
says to confirm against current Thinfinity documentation, and the Communication Gateway figure is a
linear extrapolation outside the range the app measured (2–8 OCPU; the preset uses 16). Say so in the
task result whenever the diagram carries numbers computed here.

## 1. Bandwidth

`bandwidth (Gbps) = concurrent users × Mbps per user ÷ 1000`, then `× 1.2` (20 % margin). A
`Ancho de banda pico` typed by the user replaces the first step; the margin still applies.

| Perfil de uso | Mbps / user | with H.264 |
|---|---|---|
| Inactivo | 0.0003 | 0.0003 |
| Word | 0.15 | 0.3 |
| Excel | 0.2 | 0.5 |
| PowerPoint | 4.5 | 1.8 |
| Navegación web | 6.5 | 1.0 |
| Galería de imágenes | 3.6 | 0.8 |
| Video (media pantalla) | 9.5 | 2.8 |
| Video (pantalla completa) | 8.5 | 3.1 |

No profile given → **Video (media pantalla)**: the most demanding of the set, so an unstated profile
never under-sizes. No users and no bandwidth → no calculation: use the preset quantities of §3.

## 2. Throughput of a machine

`operative Gbps = min(OCPU × 1, 40) × 0.97 × 0.8` (1 Gbps per OCPU, 40 Gbps ceiling per VM, 97 %
network efficiency, 80 % operating factor). A 4-OCPU Gateway carries 3.104 Gbps; a 16-OCPU
Communication Gateway carries 12.416 Gbps. The Layer-7 load balancer tops out at **8 Gbps**.

## 3. Platforms and what gets calculated

| | **Nueva (HA extendida)** — default | **Legacy (HA básica)** |
|---|---|---|
| Gateways | 2 · Linux · 4 OCPU / 16 GB | 2 or more · Windows · 4 OCPU / 16 GB |
| Communication Gateways | `max(2, ceil(bandwidth ÷ 12.416))` · Linux · 16 OCPU / 32 GB | none |
| Brokers | 2 · Windows · 8 OCPU / 64 GB | 2 · Windows · 8 OCPU / 32 GB |
| Monitoring | 2 VictoriaMetrics · 8 OCPU / 32 GB | same |
| Extras | Layer-4 NLB; Heatwave HA profile DB; Victoria Logs | no L4 NLB; VM MySQL for analytics |
| Session traffic goes through | the Communication Gateways | the Gateways |

- **Nueva:** the Gateways stay at 2 whatever the load; Communication Gateways grow with bandwidth.
- **Legacy:** Gateways = `max(2, ceil(min(bandwidth, 8) ÷ 3.104))`. Above 8 Gbps Legacy is out of range.
- **Alta disponibilidad = No:** every minimum drops from 2 to 1 (Gateway, Communication Gateway,
  Broker). That is this console's rule, not Mariano's (his presets are always HA); say so if asked.
- A quantity the user typed always wins over the calculated one.

Worked figures (default profile, no H.264): 250 users → 2.85 Gbps → Nueva 2 / 2 / 2; 1,000 users →
11.4 Gbps → Nueva 2 / 2 / 2, **Legacy out of range**; 3,000 users → 34.2 Gbps → Nueva 2 Gateways, 3
Communication Gateways, 2 Brokers; 700 users on Legacy → 7.98 Gbps → 3 Gateways.

## 4. Conflicts (alert, never block)

The console shows these in the window; the run repeats them in the task result. **The values the user
typed are the ones drawn.** Do not silently "fix" them.

| Conflict | Message |
|---|---|
| Legacy and `Communication Gateways` > 0 | Legacy has no Communication Gateways. |
| HA = Sí and Gateways, Brokers or Communication Gateways < 2 | HA needs at least 2. |
| HA = No and any of them > 1 | HA is No but more than one was entered. |
| Brokers > 6 | The maximum is 6 Brokers. |
| Legacy and bandwidth (with margin) > 8 Gbps | Over the L7 balancer limit: use Nueva. |
| Legacy and bandwidth > typed Gateways × 3.104 Gbps | The Gateways cannot carry it: add some or use Nueva. |
| Nueva and typed Communication Gateways < needed | Not enough for that bandwidth (give the number needed). |

## 5. How it reaches the drawing

- Pills stay **160 × 43** and carry no OCPU/RAM text. Draw each component once per instance up to 3;
  from 4 up, draw two with the `⋮` ellipsis idiom of SKILL.md §5.1 and a `×N` in the label.
- The numbers (platform, quantities, OCPU/RAM per component, bandwidth with margin) go in a compact
  table **under** the diagram in the HTML preview, plus one line saying they are an estimate.
- Draw the Communication Gateway as its own Thinfinity pill (icon `gateway`, label `Communication
  Gateway`) in the DMZ next to the Gateways; Legacy has none.
