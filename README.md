# react-agents

The generic TypeScript and React engineering standards — every React/TS repo Tommy owns, naming no
product. The .NET half lives in `tomjseery/dotagents`; anything Concertable-specific lives in
`Concertable/agent-standards`.

**How this is authored and delivered — read
[`dotagents/ARCHITECTURE.md`](https://github.com/tomjseery/dotagents/blob/main/ARCHITECTURE.md) before
changing the shape of any of it.** It is the one home for the four tiers and why the repos stay separate,
the authoring → generate → install chain (a plugin *copies* its payload; it can never reference one), the
per-machine setup for both harnesses, and what a new project needs. This README does not restate it.

## The standards map

**The skill is the payload.** A standard is authored in exactly one file,
`.agents/skills/<name>/SKILL.md` — front matter declaring `domain: react`, then the standard itself.
There is no separate doc: `@`-import expands only inside `CLAUDE.md`/`AGENTS.md`, never inside a
`SKILL.md`, so a skill naming a doc could only ever be a pointer that cost an extra Read for content the
invocation always needed.

**Look a topic up in [`SKILLS.md`](SKILLS.md) before writing a rule down**, so it lands in the one skill
that owns it. The catalogue is generated from the skill tree, so it cannot drift from it.

**A generic standard and its Concertable counterpart share a skill name on purpose** — `http-layer` here
and `http-layer` in `agent-standards` — and the plugin namespace tells them apart:
`react-standards:http-layer` against `react:http-layer`. Install whichever pair a repo needs and invoke
the one you mean.

```
.agents/skills/                    Source of truth — edit here. One skill per standard: front
                                   matter declaring its domain, then the standard itself.

SKILLS.md                          Generated catalogue: skill -> what it covers -> owning plugin.

.agents/sync-generated.ps1         Regenerates .claude/skills/, plugins/react-standards/ and
                                   SKILLS.md. Refuses to write when the skills and the plugin
                                   payloads disagree. CI runs it with -Check.

plugins/react-standards/           Generated. The installable plugin — its own full copy of every
                                   skill, because a plugin cannot reference outside its root.
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

This repo is private, so provisioning needs git credentials that can read it. Nothing here is junctioned
onto a machine: this repo holds only standards, and the plugin is what delivers them.

## Named gaps — create the node, write the standard

These slots are deliberately empty rather than silently missing. Adding one is a new skill; nothing else
moves.

`component-design` (props typing, composition over configuration, when to split) · `loading-and-errors`
(skeleton vs spinner, suspense and error boundaries, where pending renders) · `accessibility` ·
`formatting` (money and numbers behind one module) · `realtime` (connection lifecycle, subscription in
an Effect, payload naming) · `performance` (memo policy, keys, code splitting) · `type-safety` (no `any`,
`unknown` at boundaries, no non-null assertion, `satisfies`) · `cross-platform` (shared versus platform
code, navigation versus router, secure storage).
