# Product

## Register

product

## Users

One user per running instance. The sidebar hardcodes that user: `Nick Ceraso`, `Design Team · Admin` (`index.html`). Nick is a designer at Cybele Software with no programming background. He writes his task prompts in Spanish (see the real prompts in `jobs/task-*/job.json`), while the UI ships in English with an optional Spanish layer: a single `I18N.es` lookup table in `index.html`, language stored in `localStorage['np-lang']`, default `en`, switched in Settings.

Context of use: a local desktop browser at `http://localhost:3491`, started by double-clicking `Start-Cybele-Console.bat`. Not hosted, not multi-tenant, no login, no accounts. `server.js` binds to `127.0.0.1` so the console is reachable only from this machine. That is deliberate and load-bearing: there is no authentication anywhere, `POST /run` executes an arbitrary shell command, and a task run spawns the Claude CLI with `--dangerously-skip-permissions`. Anything that would expose the server beyond loopback needs auth first.

The job to be done: turn a brief (an article, a DOCX, a voiceover script, a topology description, or just a paragraph of intent) into a branded Cybele deliverable, without writing code, and keep track of every version of it.

Two things used to be called "tasks" and were renamed apart on 2026-07-28. **Tasks** are the
documents the user generates; they live in `jobs/<id>/` and appear under Task history. The
**roadmap** (`data/roadmap.json`, `/roadmap`) is a separate list of milestones about building the
console itself, and its board is no longer reachable. Never conflate them.

The team dimension is narrow and deliberate. `data/roadmap.json` is committed and shared across the team through git. `jobs/` is gitignored, so per-task output stays on the machine that produced it until someone explicitly pushes it (`CLAUDE.md`, "Publishing to GitHub"). `data/progress.md` and the brand (`data/brand.json`, `data/brand-assets/`) are mirrored from the repo into the local cache by `POST /sync`, so everyone starts from the same content.

## Product Purpose

The console prepares and tracks work; Claude Code executes it. Nothing in this app renders a deck or an SVG itself.

What it actually does, verified in `server.js` and `index.html`:

- **Prepare a task.** Pick a document type, optionally attach a source file, write a prompt. The server injects the matching section of `data/progress.md` as context (`GET /progress-section`) and writes `jobs/<id>/job.json`. Built-in types: `pptx`, `wp` (whitepaper PDF), `blog`, `arch`, `storyboard`, `linkedin-carousel`, `webapp`. The user can add more at runtime; they persist to `data/custom-pipelines.json` and are shared with the team.
- **Run it.** `POST /jobs/<id>/run` spawns the Claude Code CLI headlessly (`claude -p <prompt> --dangerously-skip-permissions`), logging to `jobs/<id>/run.log`. The prompt it builds points Claude at `CLAUDE.md` and `RUNBOOK.md`.
- **Get unblocked.** A run that hits a consequential decision calls `POST /jobs/<id>/ask`, which flips the task to `needs-input` and raises the intervention modal. The user answers `allow` / `continue` / `cancel` with an optional note.
- **Review.** Preview shows the rendered PDF in an iframe. Annotate mode turns the preview into a pinboard: click the page, type a comment, and the pins (`{n, page, xPct, yPct, comment}`) plus rendered PNGs go out as one change request.
- **Revise, versioned.** Every change request appends to `revisions[]` and produces a new folder, base `v1`, revision N becomes `v(N+1)`. Earlier versions are never overwritten.
- **Export.** The download modal offers format (original / PPTX / PDF / PNG / JPEG / SVG), transparent background, 1x/2x/3x or a 200 KB auto-fit, single-canvas or per-page, all pages or a selection. `GET /formats` first reports which formats the deliverable can honestly produce; vector formats are only offered when real vector SVGs exist in the folder, so a raster never gets shipped disguised as an editable file.
- **Approve, reopen, stop, re-run, delete.** Deletions append to `data/deleted-tasks.json` and only propagate to the repo when the user confirms them during a push.
- **Brand assets.** Cybele colors (editable, persisted to `data/brand.json`), logos and files, and the 131-icon Cybfont library in `brand-icon-lib.js`.

Four nav destinations, and four is the number Nick wants: Overview, Task history, Brand assets,
Settings. `VIEWS` also keeps `jobs`, which is not linked because `setView()` lands on it right
after a task is created. Three further views (`pipelines`, `tasks`, `milestones`) were defined and
reachable by nothing; the router entries were removed on 2026-07-28. The roadmap-board code behind
`tasks` and `milestones` is still in the file and still runs into hidden containers, because
removing it also removes the `/roadmap` endpoint and `data/roadmap.json`, which the team shares.
Renaming it apart from the document tasks removed the ambiguity that made deletion look urgent.

Success looks like: a queued task becomes an approved, downloadable file, with its revision history intact and nothing silently overwritten.

## Brand Personality

**Techy, modern, simple.** Nick's own three words (2026-07-28), and the governing rule under them
is **less is more**. Treat that as the tie-breaker: when a change could go either way, the version
with fewer elements, fewer lines and fewer decisions wins.

What each word buys you here:

- **Techy** is earned by density and precision, not by decoration. Monospace where a value is
  literally a path or a command, exact counts instead of "several", a log you can actually read.
  Never a fake terminal, scanlines, neon or a circuit motif.
- **Modern** means current craft, quietly applied: real states, honest motion, tokens for both
  themes. It does not mean the visual fashion of the moment. No glass, no gradient text, no
  oversized hero numbers.
- **Simple** is about how much the screen asks of you, not about how sparse it looks. A dense view
  that answers a question at a glance is simple. A roomy one that hides the answer behind a click
  is not.

The console is Cybele's own tooling and looks like Cybele: navy surfaces, `#0A74D6` as the only
real accent, Inter throughout, no display type anywhere.

Tone is plain and operational: "Pick a document type to start a task", "Drag a card between
columns to update status", "Send all changes". Not a line of persuasion anywhere. Spanish strings
are informal Rioplatense ("Elegí un tipo de documento", "Describí qué cambiar…"), matching how the
one user speaks.

No reference product yet. Nick has not named an app whose feel he wants; if one comes up, add it
here, because a concrete reference beats three adjectives.

## Anti-references

- **A hosted SaaS dashboard.** No sign-in, no billing, no onboarding tour, no marketing surface. There is no `/` landing page: `index.html` is the app.
- **A framework rebuild.** `package.json` has zero dependencies and one script, `node server.js`. `server.js` uses only Node built-ins. The UI is one self-contained `index.html` (about 3,480 lines) plus two generated icon files. No build step, no bundler, no component library. Anything that would introduce one is out of scope.
- **Heavy chrome.** `CLAUDE.md` states the component rules as "borderless, shadowless, low-contrast, Inter". Radii are deliberately split: buttons and pills are `999px`, badges and cards `5px`.
- **Decorative motion.** Transitions are 0.12s to 0.3s and all convey state (hover, saving, running, open). The only looping animations are the running-status pulse and the spinner.
- **Overriding the Cybele system with generic good taste.** `CLAUDE.md` is explicit: when the `impeccable` skill's opinions conflict with what this app already does, the app wins. Use the skill for contrast, hierarchy, state coverage and interaction detail.

Resolved 2026-07-28: "borderless, shadowless" applies to the console chrome, not only to generated
deliverables. The containers that still carried an outline (`.job-card`, `.task-card`, `.file-card`,
`.ctx-panel`, `.modal`) were the bug and have been stripped; separation comes from surface tone, and
the modal relies on its dimmed, blurred backdrop instead of a shadow. Borders remain only where they
are an affordance rather than chrome: text inputs and selects, outline buttons, the floating filter
menu (nothing dims behind it), the dashed add-a-document-type card, and toasts. `border-top`
dividers such as `.sidebar-user` and `.job-versions` are separators, not outlines, and stay.

## Design Principles

1. **Less is more, and it is the tie-breaker.** Nick's stated golden rule. Before adding an element,
   a border, a panel or a step, try the version without it. Ship the smaller one unless the larger
   one answers a question the smaller one cannot. This is what settled the borderless containers.
2. **The console prepares, Claude executes.** Every screen should end in either a queued task or a reviewed file. If a control does not move work toward one of those, it does not belong.
3. **Never lose a version.** Versioned output folders, an append-only `revisions[]`, a logged and confirm-gated delete. Destructive-feeling actions must stay reversible or explicitly gated.
4. **Speak the user's words, not the disk's.** The UI says "task" and "document type"; the filesystem still says `jobs/` and `pipeline`. The interface is written for someone who does not read the code, and stays that way.
5. **One file, no build.** Staying dependency-free is a product decision, not an accident: it is what lets any teammate clone the repo and run `node server.js`. Prefer a plain-CSS, plain-JS solution over a better one that needs tooling.
6. **Local by default, shared on purpose.** The shared task list travels through git; heavy per-task output does not, until someone says so. Do not add anything that pushes work automatically.

## Accessibility & Inclusion

**The target, set by Nick 2026-07-28.** Deliberately narrow, so that a review reports what matters
here and stays quiet about the rest:

1. **Text contrast at WCAG AA (4.5:1), in both themes.** Met and verified. Any new colour must be
   measured against its real background before it ships.
2. **Usable with colour vision deficiency.** Met and verified. No state, status or category may be
   distinguishable by hue alone; it needs a glyph, a label, or both.
3. **Keyboard operation and screen readers are explicitly out of scope.** One user, one local
   machine, mouse-driven. Nick does not navigate with Tab. Do not report focus rings or focus traps
   as defects; if that ever changes, this line changes first.

**Verified 2026-07-28.** Contrast was measured by walking every rendered text node in both themes
against its real computed background, not by eyeballing tokens, which is what caught six failures
the token-level pass missed. All are fixed; zero remain. Most came from one pattern worth
remembering: a colour tuned for the dark theme was never redefined for light, fell through, and
landed on a near-white surface. `--brand-light` at 2.39:1 and `--mint` at 2.03:1 were both this.

Colour blindness was simulated for protanopia, deuteranopia and tritanopia. The palette does
collapse under all three (running against done, queued against error, and several project colours
against each other), but nothing depends on hue: each of the six statuses carries a distinct glyph
(clock, spinner, check, triangle, question mark, cross) and every project carries an icon and a
label. Rendered under each simulation, all six statuses stay tellable apart. **The glyphs are the
accessibility feature. Do not replace a status glyph with a plain coloured dot.**

Already in place:

- `prefers-reduced-motion: reduce` neutralizes every animation and transition (`0.001ms`), and `reduceMotion` is read in JS.
- `color-scheme: dark` / `light` is set per theme so native controls and scrollbars stay legible; the status filter is a custom `role="listbox"` dropdown built specifically because native option lists rendered light-on-light in dark mode.
- Modals use `role="dialog" aria-modal="true"` with `aria-labelledby`; Escape closes every modal and the mobile sidebar; several modals autofocus their first field.
- Icon-only buttons carry `aria-label` or `title` (theme toggle, hamburger, close, view toggles, page nav).
- Responsive is structural: sidebar collapses behind a hamburger at 720px, stat grid drops to 2 columns at 1200px and 1 at 720px, kanban stacks at 960px.

Known gaps, all real but all **out of scope** under the target above. Listed so nobody rediscovers
them and treats them as bugs:

- No `:focus-visible` styles anywhere. Text inputs signal focus by changing `border-color`; buttons,
  nav items and cards show nothing, so keyboard navigation is close to invisible.
- Modals have no focus trap and no focus restore, despite `aria-modal="true"`.
- The roadmap kanban has no keyboard equivalent for its drag and drop. It is also unreachable now,
  see the note on `VIEWS` in `index.html`.

Dark is the default theme (`data-theme="dark"` on `<html>`, and the inline boot script falls back to `dark` when `localStorage['np-theme']` is unset). Both themes are fully tokenized, so any new color must be added as a variable in both `:root` and `[data-theme="light"]`.
