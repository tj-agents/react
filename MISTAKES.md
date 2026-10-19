# Mistakes

## M001 — React aliases retired before completing the Concertable caller scan

Observed: 2026-10-19. State: in-progress.
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
