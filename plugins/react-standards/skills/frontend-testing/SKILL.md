---
name: frontend-testing
description: What a Vitest suite should and should not cover — pure logic, api modules, store transitions, browser-boundary wrappers and orchestrating hooks earn tests, while testing the library itself or re-proving through the DOM what a browser end-to-end suite already covers does not; plus the shape that keeps it honest — colocated thing.test.ts files, a node environment by default with a DOM opted into only where something truly touches it, vi.hoisted for anything a vi.mock factory closes over, mocking one boundary out rather than six modules to reach one assertion, test names stating the behaviour rather than the method, mocks cleared between tests, and coverage read as a signal never a target. Use when adding or reviewing a frontend test, deciding whether something belongs in Vitest or the end-to-end suite, mocking a module, or looking at an untested unit.
---

# frontend-testing

The standard is `../../standards/react/TESTING.md`, shipped in this plugin. Read it and follow it; this skill only routes to it.
