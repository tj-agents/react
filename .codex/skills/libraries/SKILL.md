---
name: libraries
description: Which library to reach for in a TypeScript/React app and when — React Query for server state, Zustand over useReducer or Context for shared client state (and the narrow case where a reducer is still right), zod at every untrusted boundary including form submit and route search params and env, TanStack Router with typed routes, Tailwind with a cn helper and cva variants over CSS-in-JS, dayjs behind one formatting module, Vitest, and the list of libraries deliberately not used (Redux, MobX, moment, styled-components, a second HTTP client). Use when adding a dependency, choosing between a reducer and a store, picking how to validate or parse something, reaching for a date or class-name utility, or reviewing a PR that introduces a library that overlaps one already in the stack.
kind: contract
domain: react
profile: core
applicability: Repositories choosing Tommy's complete React library stack
requires: selected-library-stack
provenance: selected-stack, house
---

# Stack defaults

Read and follow the [canonical definition](../../../.agents/react/contract/libraries/SKILL.md) in full.
This discovery entry is generated; edit the referenced `.agents/` definition.
