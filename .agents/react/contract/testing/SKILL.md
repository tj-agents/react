---
name: testing
description: Frontend test authorization — tests are added only when explicitly requested or repo-owned guidance adopts a tier; this hub does not authorize or shape any suite by itself. See react:testing-frontend once a suite is adopted. Use when proposing, adding, changing, or reviewing frontend tests or test infrastructure.
kind: contract
domain: react
profile: core
applicability: React projects
requires: react
provenance: house
---

# Testing

Owns whether a test may be authored at all; `react:testing-frontend` shapes an adopted suite once this gate
is passed.

## Agreed

Do not add a test, install a test dependency, create a test setup, widen CI, or introduce a new test tier
merely because production code changed or an untested unit exists. Tests may be authored only when the user
explicitly requests them for the current work, or repo-owned guidance or a plan says that the relevant tier
is adopted and requires them. A `test` script, test dependency, or a few existing files is not by itself an
adoption decision.

When tests are not authorized, run the relevant existing suite if it is part of verification, and fix an
existing test only when the production change legitimately invalidates it. Do not expand coverage. A test
standard is never implicit permission to turn a production refactor into a test-infrastructure project.

Once a tier is adopted, `react:testing-frontend` defines how it is shaped.
