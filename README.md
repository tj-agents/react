# react-agents

The generic TypeScript and React engineering standards — every React/TS repo Tommy owns, naming no
product. The .NET half lives in `tomjseery/dotagents`; the stack-agnostic method — branching, plans,
reviews, merging, and the hooks that enforce them — lives in `tomjseery/process-agents`; anything
Concertable-specific lives in `Concertable/agent-standards`.

**How this is authored and delivered — read
[`dotagents/ARCHITECTURE.md`](https://github.com/tomjseery/dotagents/blob/main/ARCHITECTURE.md) before
changing the shape of any of it.** It is the one home for the five tiers and why the repos stay separate,
the authoring → generate → install chain (a plugin *copies* its payload; it can never reference one), the
per-machine setup for both harnesses, and what a new project needs. This README does not restate it.

## The standards map

**The doc is the payload and the skill is a router.** A standard is a plain markdown file under
`standards/react/`, and its skill is eight lines naming that file — so a repo can `@`-import the doc to
make it always-on, or route to it by skill everywhere else.

**Look a topic up in [`standards/react/INDEX.md`](standards/react/INDEX.md) before writing a rule down**,
so it lands in the one file that owns it. The index is generated from the tree, so it cannot drift from it.

A doc name never repeats its folder (`react/HTTP.md`, not `react/REACT_HTTP.md`) while skill names stay
globally unique (`http-layer`), because the deployed skill namespace is flat and spans every stack.

```
standards/react/                   -> ~/.agents/standards/react/
                                      The standards themselves. Source of truth — edit here.

.agents/skills/                    -> ~/.agents/skills/
                                      One router per doc: front matter plus that doc's path.

.agents/sync-generated.ps1         Regenerates .claude/skills/, plugins/react-standards/ and
                                   INDEX.md. Refuses to write when a router and the tree
                                   disagree. CI runs it with -Check.

plugins/react-standards/           Generated. The installable plugin — its own full copy of the
                                   tree, because a plugin cannot reference outside its root.
```

Run after any change to an authored file:

```
pwsh .agents/sync-generated.ps1          # write
pwsh .agents/sync-generated.ps1 -Check   # verify only; what CI runs
```

## Install

Per machine, not per repo. From a clone of `Concertable/agent-standards`, provision this plugin together
with its Concertable counterpart and the process/.NET plugins for both harnesses:

```
powershell -ExecutionPolicy Bypass -File scripts/provision-agent-standards.ps1
```

```
powershell -ExecutionPolicy Bypass -File scripts/provision-agent-standards.ps1 -VerifyOnly
```

This repo is private, so provisioning needs git credentials that can read it. On Tommy's own
machine the trees are additionally junctioned into `~/.agents/` by `dotagents`'
`.agents/deploy-skills.ps1`, which takes this repo as one of its source roots.

## Named gaps — create the node, write the standard

These slots are deliberately empty rather than silently missing. Adding one is a new doc in the tree plus
its router; nothing else moves.

`component-design` (props typing, composition over configuration, when to split) · `loading-and-errors`
(skeleton vs spinner, suspense and error boundaries, where pending renders) · `accessibility` ·
`formatting` (money and numbers behind one module) · `realtime` (connection lifecycle, subscription in
an Effect, payload naming) · `performance` (memo policy, keys, code splitting) · `type-safety` (no `any`,
`unknown` at boundaries, no non-null assertion, `satisfies`) · `cross-platform` (shared versus platform
code, navigation versus router, secure storage).
