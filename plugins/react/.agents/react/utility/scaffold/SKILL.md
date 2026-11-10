---
name: scaffold
description: Configure a new React project's TypeScript and ESLint checks, or create its application tree once react:structure records an agreed File structure. Use when starting a React project or adding the scaffold's mechanical standards checks.
kind: utility
domain: react
profile: scaffold
applicability: new React projects
requires: react
provenance: house
---

# React project scaffold

Owns the React scaffold's TypeScript, ESLint and CI configuration. Application-tree creation still waits
for the File structure `react:structure` records. Its scripts and templates sit beside this file.

## Create a project

Create the application with its selected React toolchain first. Its package must already declare React
and the React TypeScript types. Application-tree scaffolding remains unimplemented until
`react:structure` has an agreed File structure.

## Build and adapt

From the new project, apply the shipped configuration using the installed skill's script:

```text
python <skill-directory>/scripts/configure.py .
npm install
npm run lint
npm run typecheck
```

Commit `package-lock.json`. The script preserves unrelated package metadata, scripts and dependencies,
and refuses existing TypeScript, ESLint, Node-version or supplied CI files and colliding tooling entries
before writing. Reconcile those project-owned choices before applying the scaffold.

The templates select compatible ESLint, typescript-eslint and TypeScript versions; the current parser
supports TypeScript below 6.1, so TypeScript 7 is not installed. No optional application libraries or
frontend test suite are selected.

## Validation and publication

Enforced by `npm run lint`: interface object definitions, camelCase type fields (including the wire
discriminator `$type`), interface extension instead of intersection aliases, exhaustive union switches,
Rules of Hooks and effect dependency lists. Enforced by `npm run typecheck`: strict TypeScript checking,
including optional-value narrowing and `never` exhaustiveness assertions.

Both commands fail CI through `.github/workflows/react-checks.yml`. Require its `CI complete` context in
the consuming repository's ruleset. Editors using the project's TypeScript server and ESLint extension
show the same diagnostics while editing. Wire correspondence, deliberate-null semantics, feature
ownership and the reason an Effect exists still need source review.
