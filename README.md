# react

Generic React and TypeScript guidance for Claude Code and Codex, published as `react@react-agents`.

Use `react:structure` for React code organization. The previously published `react:react-structure` remains
as a forwarding compatibility skill through 2027-03-31. The canonical repository is
[`tj-agents/react`](https://github.com/tj-agents/react); the marketplace ID remains `react-agents`.

## Skills

- Contracts, empty until a decision is recorded: `react:build`, `react:domain-design`, `react:errors`,
  `react:libraries`, `react:structure`, `react:style`, `react:testing`.
- Knowledge: `react:direction`, `react:knowledge`, `react:learning`.
- Utilities: `react:scaffold`.
- Other contracts: `react:data-tables`, `react:date-formatting`, `react:http-layer`,
  `react:naming-contracts`, `react:routing`, `react:state-client`, `react:state-server`,
  `react:tiered-shared-code`, `react:ui-components`, `react:write-boundary`.
- Compatibility aliases (removed after 2027-03-31): `react:react-structure`, `react:client-state`,
  `react:server-state`, `react:contract-naming`, `react:typescript-style`, `react:frontend-testing`,
  `react:stack-defaults`.

## Applicability

The `core` profile contains only React structure, TypeScript style, contract naming, and the other required
stack contracts. TanStack Query, Router, and Table; Zustand; Tailwind and component primitives; axios; zod;
dayjs; testing; the selected full stack; and multi-app sharing are independent profiles. Installing the
plugin makes every capability discoverable; a repository selects only the profiles matching its actual
libraries and shape.

Product-specific frontend rules remain with their product owner. Machine and engineering workflow capabilities
remain in `tj-agents/core`. .NET guidance remains in `tj-agents/dotnet`.

## Authoring and verification

```powershell
pwsh .agents/sync-generated.ps1
pwsh .agents/sync-generated.ps1 -Check
```

The layout, the vendored generator and CI come from [kit](https://github.com/tj-agents/kit).
