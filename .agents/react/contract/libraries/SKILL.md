---
name: libraries
description: Own React dependency policy and scoped library choices. Use when adding, replacing or selecting a dependency, choosing a state or validation library, or reviewing overlapping libraries. Optional defaults apply only when explicitly adopted; concern skills own detailed use.
kind: contract
domain: react
profile: core
applicability: React projects; concrete defaults only for explicitly adopted choices
requires: react
provenance: house
---

# Libraries

Owns dependency policy and concrete library choices, with selected usage delegated to concern owners.

## Agreed

**One library per job.** If an existing library already owns a job, replace it or keep it; adding a
second answer creates overlapping concepts and maintenance. Review actual requirements before adding
a dependency for a single utility function.

```text
Project: React with CSS Modules, native Tauri commands and an adopted Vitest suite.
Result: retain CSS Modules and native IPC; Tailwind and axios are not implied by React.
New requirement: validate user input; explicitly select Zod and load react:validation.
```

## Scoped defaults

These are Tommy's defaults when the corresponding choice is adopted, not installation requirements
for every React application. A project may select only the rows its architecture needs. Installing
this plugin or loading this core policy does not select the complete library stack.

| Job | Selected default | Usage owner |
|---|---|---|
| Server state | TanStack Query | `react:state-server` |
| Shared mutable client state | Zustand | `react:state-client` |
| Untrusted input validation | Zod | `react:validation` |
| Typed routing | TanStack Router | `react:routing` |
| Utility styling | Tailwind, clsx/tailwind-merge `cn`, cva | `react:styling` |
| Component primitives | Owned Radix/shadcn primitives | `react:ui-components` |
| Dates | dayjs behind one formatting module | `react:date-formatting` |
| HTTP | axios, one client per backend service | `react:http-layer` |
| Adopted frontend tests | Vitest | `react:testing-frontend` |
| Tables | TanStack Table | `react:data-tables` |

For an adopted Zustand choice, shared client state belongs in its store; a reducer still suits a local
state machine read only by its owning component. Context supplies dependencies such as a client or theme.
For the adopted full stack, Redux, MobX, moment, CSS-in-JS runtimes, duplicate HTTP/date clients and a
handwritten event emitter are not additional defaults. If an incumbent cannot meet a requirement,
explain that concrete gap before changing the choice. These exclusions do not impose Tailwind or axios
on a project with a different explicit architecture.

The concern owners define validation, state, styling and other usage details. Keep policy and the
choice table here instead of introducing a second library-selection skill.
