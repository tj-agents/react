# react-agents

Generic React and TypeScript engineering contracts for Claude Code and Codex.

The react-agents marketplace publishes one plugin, react. Canonical skills live under .agents/skills and
standards live under standards/react. The generator produces both harness mirrors and the self-contained
plugins/react payload.

Concertable-specific frontend rules belong in Concertable/agents. Machine operations belong in
tomjseery/base-agents. .NET contracts belong in tomjseery/dotagents.

## Authoring

The open skill-kind taxonomy is defined in
[`base-agents/SKILL_KINDS.md`](https://github.com/tomjseery/base-agents/blob/main/SKILL_KINDS.md).
Every skill here declares `kind: contract` and routes to exactly one standards document. After a change run:

    pwsh .agents/sync-generated.ps1
    pwsh .agents/sync-generated.ps1 -Check

The generator rejects missing kinds, missing documents, orphan documents, manifest drift, and any plugin
payload that would reference files outside its own subtree.

## Installation

The central Concertable provisioner installs react@react-agents for both harnesses:

    pwsh path\to\agents\scripts\provision-agents.ps1

A running session retains the payload loaded at startup; restart it after an update.
