# Mistakes

## M001 — React aliases retired before completing the Concertable caller scan

Observed: 2026-10-19. State: resolved.
React PR20 removed seven forwarding aliases after repository-local checks, before the full explicitly
inventoried Concertable caller migration. Concertable's route generator still emits retired generic
React identifiers and platform-frontend AGENTS still names all seven removed aliases. Source generation
and producer tests did not establish caller convergence.
Correction owner: the authorized personal-projects rollout, in Concertable standards' isolated
Feature/PersonalAdoption slice and the platform-frontend adoption; no runtime alias remapper or
compatibility restoration. Existing launch/coordinator repair ownership remains separate.
Prevention: validate actual active route tables and instruction references against current shipped
producer inventories before retiring names. Extend the existing shared reference checker and invoke
it in the caller's CI; do not create a duplicate alias registry.
Acceptance: caller source/generated host tables and native instructions use current names, focused
route tests and current-corpus reference checks pass, permitted deliveries land, and real host loading
and installed convergence are proven or retained at their explicit external/owner gates.

Resolution evidence: Template PR27 delivered the shared current-reference check; Concertable
standards PR139 and frontend PR17 delivered the actual callers and generated host payloads.
The197-skill canonical corpus,24 native Linux routing tests,799 Windows hooks and both Codex
delivery tests passed. Fresh normal Windows session01a15605-4acb-7232-878e-7e98f5e0c341 supplied
react:style and efcore:persistence, and explicitly reported retired react:client-state absent.
Native personal policy loaded. Claude403 and native Linux DNS/runtime acceptance remain at their
explicit external gates in the canonical personal goal; this records the corrected caller cutover
and does not claim those independent host gates resolved or take over the launcher repair.
