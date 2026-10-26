# Shared Skills

The Claude Code **Agent Skills** used across tasks. They are **vendored in this repo** under [`/skills`](../skills) so the team can install them, and they also live (live copy) in `~/.claude/skills/`.

## Catalog

| Skill | Folder | What it does | Used by |
|---|---|---|---|
| **impeccable** | [`skills/impeccable`](../skills/impeccable) | Frontend/UI design: review, redesign, polish, layout, hierarchy, a11y, motion, tokens. | All tasks (general design quality), esp. **blog**, **presentations** |
| **cybele-blog-visuals** | [`skills/cybele-blog-visuals`](../skills/cybele-blog-visuals) | Complete visual set for a Cybele blog article in one pass: cover (6 variants) + one illustration per section. Brand‑compliant native SVG (Figma‑editable). | **blog** |
| **thinfinity-architecture** | [`skills/thinfinity-architecture`](../skills/thinfinity-architecture) | Thinfinity/Cybele architecture diagrams in the official "pill" system (native Figma‑safe SVG; monochrome default). | **architecture**, and the diagram layer of **presentations** |

## Installing (per machine)

Copy a skill folder into your personal skills dir, then it's auto‑available:

```powershell
Copy-Item -Recurse -Force ".\skills\<name>" "$env:USERPROFILE\.claude\skills\<name>"
```

Invoke with `/<name>` (or Claude auto‑invokes from the description).

## Availability by surface

| Surface | Skills? |
|---|---|
| CLI (terminal) | ✅ |
| Desktop app (local/SSH session) | ✅ |
| VS Code / JetBrains extensions | ✅ |
| Web (claude.ai/code) | ❌ |
| Desktop **Remote/cloud** session | ❌ (no access to local `~/.claude/skills/`) |

> Personal (`~/.claude/skills/`) and project (`.claude/skills/`) skills share the same config across CLI + desktop + IDE. A skill packaged as a **plugin** must be enabled in the desktop plugin manager.
