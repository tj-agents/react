# react

Read `README.md` and `SOURCE_LAYOUT.md` before changing repository structure.

Authored generic React and TypeScript capabilities live once under `.agents/<kind>/<name>/SKILL.md`.
`.agents/plugins/sources.json` owns the source map and generated-root declaration. `.codex/skills/`,
`.claude/skills/`, `.agents/INDEX.md`, both marketplace bridges, and `plugins/*` are generated. Authored host
manifests live under `.agents/plugins/manifests/`. Run `pwsh .agents/sync-generated.ps1` after authored changes
and require `pwsh .agents/sync-generated.ps1 -Check` before delivery.

Every definition declares its profile, applicability, prerequisites, and provenance. React and TypeScript core
must remain usable without TanStack libraries, Zustand, Tailwind, axios, zod, dayjs, or a multi-app repository.
Optional profiles activate only when the consuming repository selects their prerequisite. Product-specific rules
and concrete harness commands stay with their product owner.
