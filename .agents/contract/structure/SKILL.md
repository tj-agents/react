---
name: structure
description: How React code is organized — feature slices with explicit owners, hooks for reusable stateful orchestration and external integration, components that handle immediate UI events and render, Effects reserved for synchronization outside React, derived values computed during render, and closed-key behavior dispatched through one exhaustive table. Use when adding a feature folder, deciding whether logic belongs in a component or hook, reaching for useEffect, or writing a second branch on the same discriminator.
kind: contract
domain: react
profile: core
applicability: React applications
requires: react, typescript
provenance: framework, house
---

# React structure

## A feature is a slice

Everything one domain exchanges and owns lives together under `features/<feature>/` — `types`, `api`,
`hooks`, `components`, `pages`, `schemas`. One domain, one module, state and behaviour co-located with
explicit owners.

The rule is about **cohesion, not file count.** More files are fine; the defect is the same state or
derivation copied across disjoint owners.

## Hooks orchestrate; components render

A hook owns reusable stateful orchestration or integration with something outside the component. A component
owns immediate UI input state, handles the user's event, consumes hooks, and renders their result. Hooks live
in `features/<feature>/hooks/`, one concern per file.

Library-specific adapters belong to the optional contract that selects that library. Core React structure does
not prescribe a query library, state store, HTTP client, form validator, router, or styling system. When a
repository selects one of those profiles, its adapter hook may sit behind a plain feature-facing hook so the
component still consumes domain values and actions rather than a third-party API.

**The anti-patterns:**

- **Reusable orchestration copied into components** — if multiple screens coordinate the same state and external
  effect, give that concern one hook.
- **Derived values stored as state** — compute them from current props and state during render.
- **A hook created only to hide one expression** — ordinary event handling and render-time calculation remain in
  the component when they are local and readable.

## An Effect is for syncing with something outside React

Only that: a socket subscription, a DOM listener. Mount-only ones go through a shared mount-effect hook.
An Effect is **not** how you respond to an event or compute derived data — that is the *you might not need
an Effect* trap, and it forces `useRef` guards to stop re-fire loops.

Route by trigger:

| Trigger | Where it goes |
|---|---|
| An event (click, open, submit) | an event handler |
| Derived from existing state | computed in render |
| Server data, read or write | the repository's selected data adapter (see the `react:server-state` skill when applicable) |

## Dispatch on a closed key with one table

When behaviour varies by a closed key — a wire discriminator, a role, a mode — resolve it through **one**
table keyed on that value, with a `never` exhaustiveness arm so a new member breaks the build. Never
sprinkle the same switch or ternary on that key across components and hooks.

```ts
// CORRECT — one table, exhaustive; a new $type is a compile error
const render: Record<Price["$type"], (p: Price) => ReactNode> = {
  fixed: (p) => …, tiered: (p) => …, usage: (p) => …,
};
```

**The anti-patterns:**

- **A switch or ternary on the key inlined across components** — it gets copy-pasted and drifts.
- **A partial, hand-maintained permission or capability matrix.** A client catalog modelling four of the
  server's thirteen permissions silently desyncs the day the server's matrix changes. Model the full set,
  aligned to the server's constant names, and treat the server as the source — the client gate is cosmetic
  and the server enforces.
- **Returning a label the caller must re-switch.** Resolve to the value, not an enum every consumer
  reinterprets.
