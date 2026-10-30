# Job Runbook — Cybele Project Console

How Claude (Claude Code) executes a job that was prepared in the dashboard.
Trigger: the user says **"run task-XXXX"**, **"corré la task-XXXX"** (or legacy **"job-XXXX"**), or **"run the queued tasks"**. (UI term = "task"; on disk they live in `jobs/<id>/`.)

## 1. Locate the job

Each job lives in `jobs/<id>/`:

- `jobs/<id>/job.json` — `{ id, pipeline, prompt, sourceFile, status, createdAt }`
- `jobs/<id>/<sourceFile>` — the uploaded source document (if any)
- `jobs/<id>/output/v<N>/` — **versioned** output, one folder per run. The base run is `v1`,
  revision 1 is `v2`, revision 2 is `v3`, … (version = revision number + 1). **Never overwrite a
  previous `v<N>` folder** — each version is kept so the team can compare and roll back.

List queued work: read `jobs/*/job.json` (or `GET http://localhost:3491/jobs`) and pick those with `status: "queued"`.

## 2. Load context

For the job's `pipeline`, read the matching section of `data/progress.md` (same mapping the
server uses). It carries the brand rules, file locations and prior decisions for that pipeline:

| pipeline | progress.md section | execution |
|---|---|---|
| `pptx`   | PPTX Generation Pipeline | See §3.1 |
| `wp`     | PDF Whitepaper Pipeline  | See §3.2 |
| `blog`   | SVG Blog Illustration Pipeline (a pointer — the rules live in the skill) | See §3.3 |
| `arch`   | Thinfinity Architecture Diagram Skill | See §3.4 |
| `storyboard` | Video Storyboard Pipeline | See §3.4b |
| `linkedin-carousel` | LinkedIn Carousel (Placas) | See §3.4c |
| `video` | Animated Video Pipeline (pointer — the rules live in the spec) | See §3.4d |
| `webapp` | Project Vision | Implement the change in this project |
| `shared` | Next Steps | Ad-hoc; follow the prompt |

Always honor the canonical Cybele palette **06/26** and the component rules (borderless,
shadowless, low-contrast, Inter) described in `data/progress.md`.

## 2.5 Visual annotations on a revision (Annotate mode)

A revision created from the preview's **Annotate** mode carries extra fields — **if a revision has
`annotationImages` and/or `pins`, read BOTH before acting**:

- `rev.pins` — array of `{ n, page, xPct, yPct, comment }`: the change number, the **1-based page** it
  refers to, the location as a percentage of that page (x from left, y from top), and the requested change.
- `rev.annotationImages` — array of PNG paths under `jobs/<id>/annotations/` (e.g. `rev2_p1.png`),
  one per annotated page, with the **numbered pins drawn on the rendered page**. **Open/view these images** —
  they show exactly where each numbered comment points.

Apply each pin's `comment` at the page/location it marks. The revision `prompt` also lists the pins as
text (number · page · location · comment); the image is the visual ground truth, the pins are the exact data.

## 2.6 Files attached to a change request

A change request can carry files the user added (a new logo, a corrected brief, a reference
screenshot). When a revision has **`attachments`**, treat them as part of the request:

- `rev.attachments` — array of paths under `jobs/<id>/attachments/rev<N>/` (one folder per revision,
  so the same filename sent twice never overwrites what an earlier version was built from).
- **Open/read every one of them before doing the work.** The run prompt lists them too. What each
  file is *for* is in the revision `prompt` — an attachment does **not** replace the task's
  `sourceFile` unless the user says so there.
- They are inputs, never output: `attachments/` is excluded from the deliverable scan, so an
  attached SVG or PNG is never exported as if the run had produced it.

## 3. Execute per pipeline

> **Pipeline sources are in this repo.** Everything the document pipelines need — scripts, brand
> logos, icons, the closing-slide template — is versioned under `web-app/deckgen/` (and
> `presentations/`). Setup is in `deckgen/README.md`. If a Python module or tool is missing, **say
> which one and stop**; never guess a path, insert a username, or substitute another document. Set
> `CYBELE_DECKGEN_DIR` only to point at a different copy of `deckgen/`.

Working base for the document pipelines: `web-app/deckgen/` (the console passes its absolute path as
`deckgenDir`; run the commands below from there).

**Python.** Use the interpreter that `setup.ps1` built: `web-app/.venv/Scripts/python.exe` (it has every
library in `requirements.txt`; `server.js` picks it first too). Without it, fall back to `py -3.13` and state
in the run which interpreter you used. If a module is missing, say which one and tell the user to run
`setup.ps1`. (A 3.14 launcher default may be broken — PyMuPDF/COM — so a failure there is not a bug in the script.)

> **Output folder:** everywhere below, `jobs/<id>/output/` means the **versioned** folder for this
> run — `jobs/<id>/output/v<N>/` (base = `v1`, revision N = `v<N+1>`). The dashboard's run prompt
> tells you the exact `v<N>`. Never overwrite an earlier version.

### 3.1 pptx — PPTX deck
- Text source (DOCX/MD/TXT) → from-scratch editorial generator (`build_pptx.py` pattern).
- Rendered source (PDF/PPTX) → the faithful pptxgenjs path (`deckgen/enterprise_vdi_oci_esp/`; `build_deck.js` is the reference). There is no 2-slide cover/closing template any more: build the cover in the deck and use `presentations/assets/cierre.pptx` for the closing.
- Honor the job `prompt` (audience, language, emphasis). Put the `.pptx` in `jobs/<id>/output/`.
- **Architecture diagrams inside a deck** (the source shows or describes a topology — an image, a
  diagram page, or prose about gateways, brokers, zones, clouds): draw each one with the
  **`thinfinity-architecture` skill's rules, from the repo copy `skills/thinfinity-architecture/`**
  (SKILL.md + `reference/`; `~/.claude/skills/` is only a mirror). That means pill system, icon colour
  follows the pill (§6), environment zones (§2.2b), blue reference arrow (§11), the pre-render
  checks (§12), and ports/firewall only if asked (`reference/ports_and_firewall.md`).
  - **How to draw it in PowerPoint:** the rules live with the rest of the deck rules, in
    `data/progress.md` › PPTX Generation Pipeline › **"Architecture diagrams in a deck"** (the
    section this run already loads, §2). Reuse the engine in
    `presentations/reference_builder/build_script.py` rather than writing a new one.
  - Take the case data (cloud, users, HA, identity…) **from the source material**. What the source
    doesn't say is not relevant: draw the standard, simple case. If a missing fact would change the
    diagram in a way that matters, ask through §3.5 with `"form": "arch"`, so the window shows the
    architecture case-data fields.
  - Redraw an architecture image from the source in the Cybele style; do not paste it as is.

### 3.2 wp — Whitepaper PDF
- The builder reads **DOCX only**, but the task accepts any source (`.docx .pdf .pptx .md .txt .png .jpg .jpeg .svg`).
  **Never fail because the source is not a DOCX — convert it first:**
  `py -3.13 source_to_docx.py "jobs/<id>/<sourceFile>" "jobs/<id>/output/source.docx"` (in `web-app/`;
  a `.docx` is just copied). It keeps the text verbatim in the source language, infers headings from
  the PDF's font sizes / the slide titles, and keeps the pictures.
- **Read the converted DOCX before building** (titles, order, pictures in the right place) and fix what
  the heuristics got wrong. The cover title comes from its first `Title`/`Heading 1` paragraph.
- **Image-only sources (`.png .jpg .jpeg .svg`)** have no text to extract: the script prints a NOTE.
  View the picture, write what it says into the DOCX (same language, never translate), then build.
- `cd web-app/deckgen && py -3.13 whitepaper/build_whitepaper.py "<the DOCX>" "<abs path>/jobs/<id>/output/<name>.pdf"` (give the output as an absolute path: the script runs from `deckgen/`)

### 3.3 blog — Blog Images
- Invoke the **`cybele-blog-visuals`** skill with the article (the `sourceFile` or the prompt).
- **Honor what the user picked in the launcher** — `job.json` → `options`
  (`coverBrief`, `sectionImages`; the prompt repeats them as a "Deliverables for this article" line).
  `sectionImages: null` means auto — one illustration per illustrable section. They override the
  skill's own defaults.
- **The cover is not drawn.** `coverBrief: true` means one `COVER_BRIEF.md` in the run folder — the
  idea, the problem, the rhetorical triggers and what is worth representing. A person designs the
  cover from it. Never produce a cover image, whatever an older document says; legacy tasks carrying
  `coverVariants: N` mean the brief, not N covers. The console shows the brief on the task once the
  run is done, so do not paste it into the response as well.
- **Honor the output routes too** — `job.json` → `options.outputs` (`figma` + `figmaUrl`, `svg`,
  `preview`; the prompt repeats them as an "Output route" line). Only the checked routes are
  produced: an unchecked one writes no file at all. The launcher's default for blog visuals is
  **Figma + Preview** (no SVG): Figma is where the visuals are reviewed, the preview is the quick look
  from the console. On Figma + Preview, render the PNGs from the frames with `exportAsync` into the version folder. See
  OUTPUT ROUTES and Phase 4 in the skill.
- On the Figma route the icons are **instances of the Cybele Design System components** in that
  file, and body copy is **one text node per paragraph** (fixed width, auto height). Importing SVGs
  instead gives loose vectors and one text layer per line — that is the bug this route fixes.
- **Deliver only what was asked for.** When a preview is requested, it (and so `preview.pdf`) holds
  one page per requested visual and nothing else: no title/core-concept sheet, no "Notes for this
  run" page, no placeholder for a phase that was skipped. Run notes go in `NOTES.md` as a file.
- Save whatever files the routes produced into `jobs/<id>/output/v<N>/`. A Figma-only run has no
  image files to save: report the frame node ids instead.
- **Always write `visuals.json`** in that folder — the visuals in order, each with the **article
  section title** and a **`placement`**: `where` (`after` / `before` / `top`) plus one sentence
  **copied verbatim from the article**, so whoever lays out the post can find the spot with Ctrl+F.
  The Preview shows exactly that under each visual. Without the file the console can only guess a
  title from the filename and has no placement to show.
- **With a preview, every `visuals.json` entry carries `file`** — the PNG of *that* visual (one entry and
  one file per variant, e.g. `"file": "s1-dark.png"`). An entry that has a Figma link but no `file` shows in
  the console as an empty box with only "Open in Figma": the PNGs exist but nothing points to them.
- **A revision (v2, v3…) of a Blog Images task always writes the preview of what it built** — the PNGs,
  `preview.pdf` and `visuals.json` with `file` on every entry — whatever the base task's
  `options.outputs.preview` says. Tasks created before Figma + Preview became the default carry
  `preview: false`, and revisions inherit it; Nick asked that Blog Images requests always give a preview.
  A revision that builds nothing (ambiguous request, frames not found) says so in `NOTES.md` and writes no preview.

### 3.4 arch — Architecture diagram
- Invoke the **`thinfinity-architecture`** skill with the topology described in the `prompt`.
- **Case data** (`job.options.arch`, also printed at the end of the prompt as "Datos del caso"):
  optional fields from the New task window — Nube o entorno, Usuarios concurrentes, Alta
  disponibilidad, Tipo de escritorios, Identidad, Accesos de terceros, Sitios o regiones, Mostrar
  puertos, Incluir reglas de firewall, Otros datos. **A field that is absent is not relevant to this
  diagram: do not guess it and do not draw it.** No case data at all = the standard, simple case
  (Nick, 2026-09-28). Filled fields shape the drawing: cloud → that cloud's names, plus the environment zone of SKILL.md §2.2b (cloud = violet, On-premises = green, Híbrido = both, Hosteado por Cybele = blue); users →
  how many Gateways/hosts; HA → duplicate Gateway and Broker; identity → which IdP and how it links;
  third-party access → the ZTNA vendor path; sites → single or multi-site.
- **Advanced** (`job.options.arch.advanced: true`; the prompt says "Modo Advanced"): the New task
  window had the Advanced section open, with extra fields — Perfil de uso, Códec H.264, Plataforma,
  Ancho de banda pico, Gateways, Communication Gateways, Brokers. Here, unlike the standard fields, **an
  empty sizing field is calculated, not dropped**: read
  `skills/thinfinity-architecture/reference/sizing.md` and use `job.options.arch.plan` (the console
  already applied the model; the prompt repeats it as "Dimensionamiento estimado"). Values the user
  typed win. `job.options.arch.alerts` holds the conflicts the window showed: draw what was typed,
  repeat each alert in the task result, and say the figures are an estimate. The standard fields keep
  their rule (empty = not relevant). Without `advanced`, none of this applies.
- **Ports / firewall** only when those fields say `Sí`: follow
  `skills/thinfinity-architecture/reference/ports_and_firewall.md` (arrow direction rule, port per
  component, how rules are derived per zone). Never add ports or rules unasked.
- **Missing data you need** → ask through §3.5. For an arch task the intervention window shows the
  same case-data form, pre-filled; the answer comes back in `pending.decision.fields` and also
  replaces `job.options.arch`. Fields still empty after that stay out: continue with the standard
  case for them.
- **Before saving, parse the SVG as XML** (escape `&` as `&amp;` in labels — a bare `&` makes the console's SVG link fail with a browser error). Save the SVG + HTML preview into `jobs/<id>/output/`.

### 3.4b storyboard — Video storyboard
- Read **`web-app/pipelines/STORYBOARD_SPEC.md`** (authoritative) plus the voiceover
  script (the `sourceFile` or the `prompt`). Keep the VO **verbatim** — only graphic decisions.
- Produce **blocks of 3840×2160 native Figma-safe SVG** scenes (`NNa/NNb/NNc`; one dominant element per
  scene, background chosen by the story beat, red only for problems, no glow/gradients) as one **HTML
  preview** with each block = its scenes + `VO n` + a `Guion` box (`VOICEOVER:` verbatim + `En pantalla:`
  in Spanish). Render & verify against the spec's checklist (§12), then open it for review.
- Save the HTML + SVGs into `jobs/<id>/output/`. On approval, push to the **"Youtube"** Figma file
  (`K8rHguGyksdPWdHrSA3VOi`) via the project's Figma workflow. (Skill `cybele-video-storyboard` is not
  yet packaged — follow the spec directly.)

### 3.4c linkedin-carousel — LinkedIn carousel (placas)
- Read **`web-app/pipelines/LINKEDIN_CAROUSEL_SPEC.md`** (authoritative) plus the post
  text (the `sourceFile` or `prompt`) — a script with `PLACA 1…N` copy, or raw article text.
- **STRICT VERBATIM (spec §1b/§3.7).** No word added, removed or altered. No invented headlines,
  eyebrow tags, diagram labels, axis dates or CTA phrasing; never render **or mine** the `CAPTION`.
  Free: line breaks, accent word, which fragment takes which type step, composition. If the cover
  block has no hard number, do **not** write one — raise it in `NOTES.md` instead (§3.6 rule 2).
  Enforce mechanically before delivering:
  `node web-app/pipelines/verbatim_check.js <script.txt> <output/v N dir>` —
  exit 1 = violations, do not deliver. It separates INVENTADA (delete/redesign) from ALTERADA
  (restore the script's exact form) and flags a figure printed twice on one placa.
- Compose an **original** layout (one governing metaphor tied to the thesis — don't clone a reference).
  Produce **4–7 native Figma-safe 1200×1500 SVG placas** (median 6) on the `hook → middle → CTA`
  skeleton — pick one of the four middle types (linear / enumeration / contrast / dimension
  comparison), one theme (claro / navy / oscuro) and one cover archetype. Node-based generator
  (built-ins only), **emitting colour from the spec's token table, never hardcoded hex**; brand
  assets/icons as native `<path>` with `var()`→hex cleanup.
- Emit a single `preview.html` (horizontal carousel strip, each placa labeled `PLACA n · role · theme`).
  Render & self-verify with **Edge headless** against the spec's §11 checklist — which is numeric
  (fill ≈50%, ≤6 type sizes, cover ≤26 words, ≥2 hard rhythm swings) plus accessibility (no red/green
  carrying meaning; colour never the only cue) plus Figma-safe. Save into `jobs/<id>/output/v<N>/`.
  On approval, SVGs are the deliverable (Figma-importable; optional push to a `fileKey/nodeId`).
  (Skill `cybele-linkedin-carousel` not yet packaged — follow the spec directly.)
- **Variants (after delivery).** "Variantes de la placa N" or "el mismo carrusel en tema claro" →
  spec §10. Copy is **frozen**; variants go in `output/v<N>/variants/` inside the *current* version,
  never a new one. Move one axis at a time, 3 by default, and emit `variants.html` comparing them.
  If a request would change a word, it's a revision → new `v<N+1>`, not a variant.

### 3.4d video — Animated video (storyboard → MP4)
- Read **`web-app/pipelines/VIDEO_ANIMATION_SPEC.md`** (authoritative; scripts and detailed references in
  `web-app/pipelines/video-animation/`, a copy of the skill `cybele-video-animation`) plus the task's
  inputs: the Figma storyboard link the user pasted in the launcher (`job.options.video` = `figmaUrl`,
  `fileKey`, `nodeId`; also repeated as a line at the end of the prompt — if absent, the prompt or the
  source file names it, else ask through §3.5), and the audio — all **optional** — that the user attached in the launcher: `job.options.video.audio` =
  `{ voice, music, sfx[], sfxDir }` (paths relative to `jobs/<id>/`, saved under `audio/voice|music|sfx/`; a
  voice-over attached as the task's source file counts as `voice` too). Use exactly what was given: voice →
  `video.json` `voice`/`cuts`; music → `music.file`; SFX → `sfx_dir`, placed by their names where the action
  fits (whoosh on pushes, pop on appearances…). Do **not** add music or effects that were not provided and do
  not invent audio. Keep every on-screen word as the storyboard has it.
- **No audio is NOT a failure and NOT a reason to stop.** Animate without sound (spec "Sin audio": scene
  durations estimated from the VO text, no SFX/music, `scene_durations` in `video.json`, a video with no
  audio track) and say so in the result. When the user later attaches the audio in a changes request, redo
  the timing from the real audio (spec step 1): it is a retiming of the whole video, not a patch.
- **Step 0 — preflight, always first and automatic:** `python pipelines/video-animation/scripts/preflight.py
  [video.json]` (Python 3.13+, numpy, ffmpeg with libx264, input files) and the Figma motion probe in the
  spec (a read-only `use_figma`). Figma motion is a feature of the account/session: it cannot be turned on
  from this repo. If the probe says it is not enabled, **stop and ask through §3.5** — do not retry or burn
  calls; tell the user motion is not enabled for their Figma. numpy is in `requirements.txt` (run
  `pip install -r requirements.txt` if the venv lacks it).
- **Quality bar — not a slideshow.** Pushing whole storyboard states in and out is a slideshow and is NOT an
  acceptable deliverable. Animate element by element between states (move what persists, give each new
  element its own entrance, word-by-word text, traced lines) using the technique and the per-scene brief in
  `pipelines/video-animation/references/brief-por-escena.md`; delegate one scene (or two) per subagent in
  parallel when the Agent tool exists. If budget runs out, deliver a partial version, say which scenes stayed
  simple and do **not** present it as finished (§3.5).
- Run: audio → cuts per scene → animate each scene in Figma → export one MP4 per scene (1–2 exports at
  a time) → fill `video.json` (copy `video-animation/video.example.json`) → `python
  video-animation/scripts/assemble_video.py video.json output/v<N>/video.mp4` (also writes
  `video_low.mp4`, 720p). 4K only if asked (`--4k`, an upscale, never call it native).
- Save into `jobs/<id>/output/v<N>/`: `video.mp4` (master), `video_low.mp4`, per-scene MP4s under
  `scenes/`, `video.json`, `contact_sheet.png`, and `preview.html` made with
  `python pipelines/video-animation/scripts/make_preview_html.py output/v<N>` — a `<video>` that opens in
  **low quality by default** (switchable). Set `resultPath` to `video.mp4`: the console then opens that
  `preview.html` player for the Preview button and the thumbnail. `previewPath` can still be a PDF/PNG of
  the contact sheet (the task card needs an image for its thumbnail), but the user never sees it as the
  preview: **the animation must be playable in the browser, not shown as a PDF.**
- **Output is video only.** The Download dialog for this type offers MP4 (H.264), WebM (VP9) and MOV, with
  quality Low (720p) / Medium (1080p) / High (the master's size). The console transcodes `video.mp4` with
  ffmpeg on request (`/export-video`; ffmpeg via `CYBELE_FFMPEG`, PATH or WinGet). No SVG/PNG/PDF/PPTX.
- **By scenes:** the dialog can also export the per-scene clips instead of the complete video, choosing which
  scenes (one file each; a zip when several). It reads `output/v<N>/scenes/*.mp4` in scene order, so the run
  must leave every scene's MP4 there (a `*_base.mp4` intermediate is ignored).
- Verify on the MP4 (contact sheets, measured timings) and report what could not be verified (playback, audio).

## 3.6 Report progress (every pipeline)

The console shows a progress bar on every running task. It can only be as real as what you tell it, so at
each **milestone** POST the state of the run to the job (the same endpoint as the final status):

```
POST http://localhost:3491/jobs/<id>   { "progress": { "steps": ["Preflight", "Audio", "Scene 1", …], "done": 3, "label": "Animating scene 3 of 9" } }
```

- **Declare the stages once, up front** with `steps` (≤ 60 short names, in order; the console keeps them until you
  send a new list). The task card then shows "Step 4 of 9 · <label>", one segment per stage (done / current /
  pending) and a checklist of the stages — that is what lets the user see parts of the process being completed.
  `total` defaults to the number of `steps`. Later updates only need `done` (stages finished) and `label`.

- `done` = how many stages are finished (the current one is `steps[done]`); `total` only if you send no `steps`. Set it as soon as you know it
  (it may grow as you learn more; that is fine). **If you cannot know the total, send `total: 0`:** the bar is
  then indeterminate and shows only the label and elapsed time. Never fake a percentage.
- Send an update when something finishes or a new phase starts, not on a timer. A few to a few dozen per run.
- `label` says what you are doing *now*, in the user's language, short (≤ 140 characters).
- Do **not** clear it: the console removes the progress and the elapsed time when the run ends (status leaves
  `running`). For a revision, report progress the same way (the run in flight owns it).
- Typical milestones: **pptx / wp** — read source → structure → build → render → verify (5). **blog** — brief →
  one step per image → verify. **arch** — case data → topology → draw → verify. **storyboard** — read script →
  one step per scene → preview. **linkedin-carousel** — read post → skeleton → one step per placa → verbatim check.
  **video** — preflight → audio/cuts → one step per scene animated and exported → assemble → verify.
  Count the real items (images, scenes, placas) as soon as you know them.

## 3.5 If you're blocked or unsure (human-in-the-loop)

When running a task **autonomously** (triggered by the dashboard's "Run with Claude"), do **not**
silently guess on a consequential decision, and do **not** just die on an error that stops progress.
Instead, pause and ask the user through the dashboard:

1. `POST http://localhost:3491/jobs/<id>/ask` with `{ "question": "<clear question / what's blocking>", "options": ["allow","continue","cancel"] }`. This flips the task to **needs-input** and pops an intervention window in the web app. When the question is about an **architecture diagram** in any task type (a deck, a whitepaper…), add `"form": "arch"`: the window then also shows the architecture case-data fields (arch tasks always show them).
2. **Wait** for the answer: poll `GET http://localhost:3491/jobs/<id>` every ~3-5s until `pending.decision` is set (a single bash loop with `curl` + `sleep` is fine — one tool call that returns when resolved).
3. Act on `pending.decision.choice` (and read `pending.decision.note` for any guidance; for an
   **arch** task also `pending.decision.fields`, the case-data form as the user left it):
   - **allow** → do the specific action you asked about, then continue.
   - **continue** → proceed / skip the blocker and keep going (best effort).
   - **cancel** → stop now; the server already set the task to `cancelled`. Do not produce output.

Use this for: destructive or irreversible actions, ambiguous creative choices you'd normally confirm,
missing inputs (e.g. the source file is needed but absent), or an error you can't resolve on your own.

## 4. Close the job

When finished, mark it done so the dashboard shows it:

```
POST http://localhost:3491/jobs/<id>   body: { "status": "done", "result": "<one-line summary>", "resultPath": "jobs/<id>/output/v<N>/...", "previewPath": "jobs/<id>/output/v<N>/..." }
```

`resultPath` / `previewPath` must point inside this run's version folder (`v<N>`). For a **revision**,
update that revision's entry inside the `revisions` array (its own `status`/`result`/`resultPath`/`previewPath`)
rather than the base fields.

(or edit `jobs/<id>/job.json` directly: set `status: "done"` and add `result` / `resultPath`.)

Then tell the user what was produced and where.

## 5. Icon library from Figma ("actualizá los iconos desde Figma")

Not a job — a request the user makes in chat. Source: Figma `x0HMD1pXkcYdFM7NSaBvb4` (Cybele
Design System), frame "Cyb Font" `8120:7263` (also in `data/icon-source.json`). One SVG per icon,
**light variant**, or — only when an icon has no light — the first of bold, filled-light,
filled-bold, extra-bold (Nick's rule, 2026-09-28). Icons land in `data/icons-figma/`;
`build-icon-lib.js` merges them with the older Cybfont set into `brand-icon-lib.js`.

Nick has **no Figma token** on purpose ("plan B"): Claude does the sync through its own Figma
connection (`use_figma`, load the `figma-use` skill first). `use_figma` returns at most ~20 KB, so
never re-download the whole set — compare fingerprints and move only what changed:

1. **Category fingerprints from Figma** — one read-only `use_figma` call with the SELECT block
   below, returning `Object.entries(groups).map(([g, pairs]) => g + '=' + fnv(pairs.slice().sort().join(','))).join('\n')`
   where `groups[g]` holds `name + ':' + fnv(await node.exportAsync({format:'SVG_STRING'}))`.
2. **Local fingerprints** — `node figma-icons-claude.js digest`; compare line by line. Equal
   everywhere → nothing changed in Figma: run `node figma-icons-claude.js checked` (stamps the
   "last updated" date the library shows), then step 5.
3. **For each category that differs** — `use_figma` returning that category's `name:fp` pairs,
   then `node figma-icons-claude.js diff "<category>" "<pairs>"` → `added / changed / removed`.
4. **Export only those** with `exportAsync({format:'SVG_STRING'})`, ~4 per call (20 KB cap), and
   write them: save `{ icons: [{name, group, variant, svg}], remove: [names] }` to a scratch JSON,
   `node figma-icons-claude.js write <file>` (stores the new fingerprints in `_manifest.json`).
5. `node build-icon-lib.js`, check the new icons visually, and give each **new** icon a category:
   the library groups icons by the console's own categories in `data/icon-categories.json` (Nick's
   11, 2026-09-28; the Figma file is never reorganised). A new icon lands by its Figma category
   (`figmaGroups`), which is only a guess for Figma's mixed groups (objetos, conceptos, flechas,
   cuadrados, lineas, circulares): if it belongs elsewhere, add its name to that category's
   `icons`. The build prints `uncategorized` for icons whose Figma category maps nowhere.
   Also give each new icon **search keywords** in `data/icon-keywords.json` — Spanish first, main
   meaning as the first word, then English synonyms not already in the name — so the search can
   suggest it by meaning; the build lists icons without any under `noKeywords`. Then tell Nick to press **Update** (or
   reload) in Brand assets — without a token that button only rebuilds from this folder.

SELECT block (same rules as `sync-figma-icons.js`; keep them in step):

```js
const root = await figma.getNodeByIdAsync('8120:7263');
let p = root; while (p && p.type !== 'PAGE') p = p.parent;
await figma.setCurrentPageAsync(p);
const ORDER = ['light','bold','filled-light','filled-bold','extra-bold'];
const variantOf = n => { const m = /^Property 1=(.+)$/.exec(n.trim()); return m ? m[1].trim() : null; };
const safe = n => n.trim().replace(/[\/:*?"<>|\s]+/g, '-');
const fnv = s => { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return (h >>> 0).toString(36); };
const icons = [], seen = new Set();   // [name, category, variant, node]; first name wins
const walk = (node, group) => {
  const kids = 'children' in node ? node.children : [];
  const vs = kids.filter(k => (k.type === 'COMPONENT' || k.type === 'INSTANCE') && variantOf(k.name));
  let pick = null;
  if (vs.length) pick = ORDER.map(v => vs.find(k => variantOf(k.name) === v)).find(Boolean) || vs[0];
  else if (node.type === 'COMPONENT' && !variantOf(node.name)) pick = node;
  if (pick) { const n = safe(node.name); if (!seen.has(n)) { seen.add(n); icons.push([n, group, pick === node ? null : variantOf(pick.name), pick]); } return; }
  kids.forEach(k => walk(k, group));
};
root.children.forEach(g => { if (g.name !== 'Frame 26') walk(g, g.name); });
```

**Console-drawn icons** live in `data/icons-custom/` (e.g. `attach`, the paperclip, 2026-09-28): drawn in
the brand's light style (194 canvas, 9.2 stroke, round caps) where Figma has no equivalent; tooltip
"dibujado para la consola, fuera de Figma". A Figma icon with the same name replaces it on the next build.
Draw them with `stroke="currentColor"` / `fill="currentColor"`, never `black` or a hex: a fixed colour
ignores the theme (`attach` was black and vanished in dark mode until 2026-10-26).
Give each one a category (`icons` in `icon-categories.json`) and keywords.

Icons whose Figma name says **"no se usa"** (retired, e.g. "absolute-touch ⚠️ no se usa") are
synced like any other, so fingerprints keep matching, but `build-icon-lib.js` leaves them out of the
library (Nick, 2026-09-28). The build lists them under `retired`.

Fingerprints are stored per icon (`fp` in `_manifest.json`) because the REST export used by the
token path rounds some coordinates differently from `exportAsync`: after a token sync, icons have
no `fp` and all show as changed. "Failed to fetch" on the Update button means the console server
(port 3491) is not running — not a sync problem.
