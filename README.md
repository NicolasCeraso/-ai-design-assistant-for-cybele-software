# AI Design Assistant for Cybele Software

Brand & design guidelines for the Claude‑based design assistant. Each **task** has its own folder with a `PROGRESS.md` (rules + pipeline + state). Brand basics and the Agent **skills** are shared.

## Tasks

| Task | Docs | Output |
|---|---|---|
| 🖥️ **Presentations** | [`presentations/PROGRESS.md`](presentations/PROGRESS.md) | `.pptx` for Google Slides |
| 📄 **Documents** (whitepapers) | [`documents/PROGRESS.md`](documents/PROGRESS.md) | Branded multi‑page PDF |
| ✍️ **Blog** (covers + illustrations) | [`blog/PROGRESS.md`](blog/PROGRESS.md) | Native Figma‑safe SVG |
| 🧩 **Architecture** (diagrams) | [`architecture/PROGRESS.md`](architecture/PROGRESS.md) | Native Figma‑safe SVG |

## Shared

- **[`_shared/BRAND.md`](_shared/BRAND.md)** — palette (06/26), typography, logos/assets, global visual rules.
- **[`_shared/SKILLS.md`](_shared/SKILLS.md)** — the Agent skills and how to install them.
- **[`_shared/OVERVIEW.md`](_shared/OVERVIEW.md)** — vision, environment, master timeline, next steps.
- **[`skills/`](skills)** — vendored skills: `impeccable`, `cybele-blog-visuals`, `thinfinity-architecture`.

## Layout

```
.
├── README.md
├── index.html                 # landing page
├── _shared/                   # BRAND · SKILLS · OVERVIEW (+ _archive/)
├── skills/                    # vendored Agent skills (install into ~/.claude/skills/)
├── presentations/             # PROGRESS.md (+ assets/cierre.pptx)
├── documents/                 # PROGRESS.md
├── blog/                      # PROGRESS.md (+ Blog-Visuals-Style-Update)
└── architecture/              # PROGRESS.md (+ handoff)
```

## Conventions

- Read the task's `PROGRESS.md` first; it links back to `_shared/BRAND.md` and the skill(s) it uses.
- Don't duplicate brand rules into task docs — extend `_shared/BRAND.md` and reference it.
- To use a skill, copy its folder from `skills/` into `~/.claude/skills/` (see `_shared/SKILLS.md`).
