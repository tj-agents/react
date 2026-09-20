# react-agents

Generic React and TypeScript guidance for Claude Code and Codex, published as `react@react-agents`.

## Ownership

Full authored definitions live under `.agents/<kind>/<name>/SKILL.md`. The repository scope already means
React and TypeScript, so there is no repeated `react/` source folder. `.codex/skills`, `.claude/skills`,
marketplaces, the capability index, and `plugins/react` are generated from those definitions and authored host
manifests. See [SOURCE_LAYOUT.md](SOURCE_LAYOUT.md).

## Applicability

The `core` profile contains only contract naming, React structure, and TypeScript style. TanStack Query, Router,
and Table; Zustand; Tailwind and component primitives; axios; zod; dayjs; testing; the selected full stack; and
multi-app sharing are independent profiles. Installing the plugin makes every capability discoverable; a repository
selects only the profiles matching its actual libraries and shape.

Product-specific frontend rules remain with their product owner. Machine and engineering workflow capabilities
remain in `tomjseery/base-agents`. .NET guidance remains in `tomjseery/dotagents`.

## Authoring and verification

Each definition declares `kind`, `domain`, `profile`, `applicability`, `requires`, and `provenance`. After an
authored change run:

```powershell
pwsh .agents/sync-generated.ps1
pwsh .agents/sync-generated.ps1 -Check
python -B -m unittest discover -s .agents/tests -p "test_*.py"
```

The generator rejects source-map drift, unsafe output roots, duplicate identities, unresolved local skill
references, missing selection metadata, product-owner leakage, and inconsistent host manifests.
