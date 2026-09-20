---
name: client-state
description: Client state ownership — a store is a private implementation detail of the feature that owns it, consumed through a facade hook rather than exported from the barrel or imported by a component, with every transition in a named store action, derived values computed from explicit inputs rather than stored or read off a singleton, one deliberate imperative session object for non-React consumers (route guards, request headers, logout) instead of a family of getter/setter wrappers, and server data never mirrored into the store. Use when adding client state, exposing state to components, writing a derivation over stored state, needing state outside React, or reviewing a `getState()`/`setState()` call.
kind: contract
domain: react
profile: client-state
applicability: React features with shared client state
requires: zustand
provenance: framework, selected-library
---

# Client state

Read and follow the [canonical shared definition](../../../.agents/contract/client-state/SKILL.md) in full.
This discovery entry is generated; edit the referenced `.agents/` definition.
