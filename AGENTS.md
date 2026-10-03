# react

This repository uses the plugin layout `kit:check` documents and enforces
(https://github.com/tj-agents/kit). Authored skills live once under `.agents/<plugin>/<kind>/<name>/SKILL.md`,
with each skill's scripts and templates beside it; related skills share a family folder, family first
(`state/client/` publishes `state-client`). `.agents/sync_generated.py`, `.agents/sync-generated.ps1`,
`.gitattributes`, `.gitignore`, `CLAUDE.md` and `.github/workflows/ci.yml` are vendored from kit and pinned by
`.agents/plugins/kit.json`: change them in kit, then run `kit:update`.

`.codex/skills/`, `.claude/skills/`, `.agents/INDEX.md`, both marketplace files and `plugins/*` are generated. Run
`pwsh .agents/sync-generated.ps1` after authored changes and require `pwsh .agents/sync-generated.ps1 -Check`
before delivery.

`knowledge` is Tommy's progress record: change it only under `learning`'s Progress rules. A `contract` skill
gains a rule only through `learning`'s convention procedure, after Tommy decides it.

Every definition declares its profile, applicability, prerequisites, and provenance. React and TypeScript core
must remain usable without TanStack libraries, Zustand, Tailwind, axios, zod, dayjs, or a multi-app repository.
Optional profiles activate only when the consuming repository selects their prerequisite. Product-specific rules
and concrete harness commands stay with their product owner.
