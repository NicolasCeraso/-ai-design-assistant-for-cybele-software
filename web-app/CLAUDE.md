# Cybele Project Console

A local web app (the "Web App for the team" from the Cybele AI Design Assistant project) that
tracks the project and **prepares jobs** for Claude to run. Single self-contained `index.html`
+ `brand-icons.js`, served by `server.js` on **port 3491** (`node server.js`). Dark/light Cybele
theme (palette 06/26). The documents the user generates live in `jobs/<id>/` and are what the UI
calls **tasks**. `data/roadmap.json` is a different thing: milestones about building the console
itself. Two concepts, two words, never mix them.

## Running tasks (important)

The UI calls these **tasks**; on disk/endpoints they are still `jobs/<id>` (ids now prefixed `task-`,
legacy ones `job-`). When the user asks to **"run task-XXXX"**, **"corré la task-XXXX"** (or legacy
**job-XXXX**), or to run queued tasks:

1. Read `jobs/<id>/job.json` and any source file in `jobs/<id>/`.
2. **Follow [RUNBOOK.md](RUNBOOK.md)** — it maps each pipeline to its execution recipe and to the
   right section of `data/progress.md` for context.
3. Produce output into the **versioned** folder `jobs/<id>/output/v<N>/` (base = `v1`, revision N =
   `v<N+1>`; never overwrite an earlier `v<N>`), then mark the job done
   (`POST http://localhost:3491/jobs/<id>` with `{status:"done", result, resultPath, previewPath}`
   pointing inside that `v<N>/`), and tell the user what was produced.

**Python.** Use the interpreter that `setup.ps1` built: `web-app/.venv/Scripts/python.exe` (it has every
library in `requirements.txt`; `server.js` picks it first too). Without it, fall back to `py -3.13` and state
in the run which interpreter you used. If a module is missing, say which one and tell the user to run
`setup.ps1`. (A 3.14 launcher default may be broken — PyMuPDF/COM — so a failure there is not a bug in the script.)

The document pipelines (pptx, whitepaper, storyboard, carousel) live in
`web-app/deckgen/` — versioned in this clone (setup: `deckgen/README.md`, Python deps:
`requirements.txt`). If a run needs one and a dependency is missing, say which one and stop. Blog and arch visuals need nothing external:
they are the `cybele-blog-visuals` and `thinfinity-architecture` skills, self-contained in
`skills/`.

**Visual change requests:** a revision may carry `annotationImages` (PNGs under `jobs/<id>/annotations/`
with numbered pins drawn on the rendered page) and `pins` (`{n, page, xPct, yPct, comment}`). When present,
**read both** — view the image(s) and apply each pin's comment at its page/location. See RUNBOOK §2.5.

**Attached files:** a revision may also carry `attachments` — files the user added to the change
request, stored under `jobs/<id>/attachments/rev<N>/`. **Read every one before working**; they are
part of the request, not background material. See RUNBOOK §2.6.

## Publishing to GitHub (on request only)

The user works **locally** (Desktop copy); tasks stay on disk and are **not** pushed automatically.
`jobs/<id>/` (the per-task output folders) is gitignored on purpose — drafts/in-progress/error tasks
never go to the repo. The **project roadmap** (`data/roadmap.json`) IS committed and **shared across the team** —
it's the same list for everyone; only the heavy `jobs/<id>/` outputs stay local until explicitly pushed.

**Only when the user explicitly asks to push** (e.g. "subí a GitHub", "hacé el push"):
1. Sync the app code to the clone (`web-app/`) and commit/push to **the branch this clone is on**
   (`git branch --show-current` — e.g. Nick, FACU, a tester's own; **never a hardcoded branch**). This
   mirrors how the in-app sync (`server.js`, `branch: null`) pulls from each clone's own branch, so the
   flow is identical for every teammate. Keep the repo's portable divergences: `server.js`
   `const BASE = __dirname`, `Start-Cybele-Console.bat` `cd /d "%~dp0"`, `make-icon.py` `__file__`-based BASE.
2. **Also carry over ALL tasks** that appear in Task history (every `jobs/<id>/`, **any status** —
   queued/running/done/error/cancelled/approved): copy each from the Desktop `jobs/<id>/` into the
   clone's `jobs/<id>/`, then `git add -f web-app/jobs/<id>` (force, since `jobs/` is ignored) and
   include them in the same commit/push. Rule of thumb: **if it's in Task history, it gets saved.**
   This is the only way task data reaches GitHub (nothing task-related is pushed during local testing).
3. **Propagate deletions (Option A — explicit only).** Read `data/deleted-tasks.json` (the log the
   Delete button appends to; also `GET /deleted-tasks`). For each logged id still present in the
   clone's `jobs/<id>/`, **show the user the list and get confirmation**, then `git rm -r` those and
   include them in the commit. After a successful push, clear the log (`[]`). NEVER remove a task from
   the repo just because it's absent locally — only ids the user explicitly deleted here are ever
   dropped, so a teammate's tasks in the shared history are never touched.

## Server endpoints (`server.js`)

- `GET/POST /roadmap` — project roadmap (whole-list replace), stored in `data/roadmap.json`. Not the
  user's documents; those are the `/jobs` endpoints below.
- `GET /jobs`, `POST /jobs`, `GET|POST /jobs/<id>` — prepared jobs
- `GET /progress-section?pipeline=<key>` — extracts the pipeline's section from `data/progress.md`
- `GET /run-stream`, `POST /run` — execute a shell command (stream / blocking)

## UI work → load the `impeccable` skill first

Before editing anything that changes **what the user sees** — layout, typography, colour, spacing,
new or altered controls, states (hover/focus/empty/error), motion, responsive behaviour,
accessibility — invoke the `impeccable` skill and follow it, then edit.

This does NOT apply to changes that leave the rendered UI identical: logic, endpoints, data
handling, dead-code removal, comments, refactors. Judge by the rendered result, not by which file
you touch. Adding a checkbox to the export dialog qualifies; deleting an unused MIME entry does not.

**The Cybele design system wins.** `impeccable` carries its own strong opinions on type, colour and
layout. Where they conflict with the conventions below or with what the app already does, follow the
app. Use the skill for what it is good at here: contrast and accessibility checks, visual hierarchy,
state coverage, interaction details.

## Conventions

- Keep the Cybele palette 06/26 and component rules (borderless, shadowless, low-contrast, Inter).
- The user is non-technical about implementation: explain plainly, recommend a default, verify
  changes in the browser before reporting done. The launcher is `Start-Cybele-Console.bat`
  (desktop shortcut "Cybele Console").
- `data/progress.md` is the current content source; the future goal is to pull it from GitHub.
