---
name: libraries
description: When a TypeScript/React app takes a new dependency — one library per job, replacing rather than adding a second answer to a question an existing library already solves. Use when adding a dependency or reviewing a PR that introduces a library overlapping one already in the stack. See react:libraries-selected for Tommy's concrete, selected React library stack.
kind: contract
domain: react
profile: core
applicability: React projects
requires: react
provenance: house
---

# Libraries

Owns when to take a dependency and the one-library-per-job rule; `react:libraries-selected` records which
concrete libraries are chosen for a repository that has adopted Tommy's full stack.

## Agreed

**One library per job.** Adding a second library for a job an existing one already does is the violation,
even when the new one is better in isolation — two answers to one question is what makes a codebase
unlearnable. Replace, or don't add.

Which concrete library to reach for is a stack decision, recorded in `react:libraries-selected`, not part of
this core rule.
