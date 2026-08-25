---
name: frontend-testing
description: What a Vitest suite should and should not cover — pure logic, api modules, store transitions, browser-boundary wrappers and orchestrating hooks earn tests, while testing the library itself or re-proving through the DOM what a browser end-to-end suite already covers does not; plus the shape that keeps it honest — colocated thing.test.ts files, a node environment by default with a DOM opted into only where something truly touches it, vi.hoisted for anything a vi.mock factory closes over, mocking one boundary out rather than six modules to reach one assertion, test names stating the behaviour rather than the method, mocks cleared between tests, and coverage read as a signal never a target. Use when adding or reviewing a frontend test, deciding whether something belongs in Vitest or the end-to-end suite, mocking a module, or looking at an untested unit.
domain: react
---

# Testing

Vitest. The question this file answers is **what to test at which level** — a frontend suite that tries to
prove everything through rendered components is slow, brittle, and still misses the logic that actually
breaks.

## What earns a unit test

The layers where a bug is silent and cheap to catch:

- **Pure logic** — resolution, permission and eligibility functions, mappers, derivations. These are the
  highest-value tests in the repo and need no framework at all.
- **API modules** — that each call hits the right method and URL and shapes its body correctly, with the
  HTTP client mocked at its module boundary.
- **Store logic** — that an action moves the store through the transition it claims to.
- **Storage, consent and other browser-boundary wrappers** — the branches nobody exercises by hand.
- **A hook whose orchestration is the point**, with its library boundaries mocked.

## What does not

**Do not test the library.** A test asserting that `useQuery` caches, that the router redirects, or that a
primitive renders its children is testing someone else's code and fails on their next release.

**Do not prove a screen through the DOM when a browser suite already covers it.** Rendered
component-and-navigation behaviour is what an end-to-end suite is for; duplicating it in Vitest buys a
second, flakier copy. Reach for a rendering test when a *component itself* holds branching worth pinning —
and if the repo has no rendering setup, that is a deliberate line, not an omission to quietly cross.

## Shape

Tests are colocated: `thing.test.ts` beside `thing.ts`. There is no parallel `__tests__` tree — a test that
sits next to its subject gets moved and deleted along with it.

The default environment is `node`. Opt a project into a DOM environment only where something under test
genuinely touches the DOM; the node default is what keeps the suite fast.

```ts
const mocks = vi.hoisted(() => ({ request: vi.fn() }));
vi.mock("@/lib/apiClient", () => ({ apiClient: { request: mocks.request } }));

describe("actionLinkApi", () => {
  beforeEach(() => vi.clearAllMocks());

  it("executes the advertised method without duplicating the API prefix", async () => {
    …
  });
});
```

**`vi.hoisted` for anything a `vi.mock` factory closes over** — the factory is hoisted above the file's
imports, so a plain `const` above it is still undefined when it runs.

**Mock at the module boundary you own**, one level out: the HTTP client, the query client, the router. A
test that mocks six modules to reach one assertion is telling you the unit has too many collaborators —
fix the unit.

**A test name states the behaviour, not the method.** "executes the advertised method without duplicating
the API prefix" survives a rename and tells the next reader what broke; "test getById" does neither.

`beforeEach(() => vi.clearAllMocks())` in every suite that mocks; undo global stubs in `afterEach`. A test
that passes only when run after its neighbour is worse than no test.

## Coverage is a signal, never a target

Chase the branches that would ship a real defect. A number the suite must hit produces tests written to
raise the number, which is exactly the test nobody trusts when it fails.
