# React structure

## A feature is a slice

Everything one domain exchanges and owns lives together under `features/<feature>/` — `types`, `api`,
`hooks`, `components`, `pages`, `schemas`. One domain, one module, state and behaviour co-located with
explicit owners.

The rule is about **cohesion, not file count.** More files are fine; the defect is the same state or
derivation copied across disjoint owners.

## Hooks orchestrate; components render

All logic — fetch, mutate, derive, orchestrate — lives in hooks. A component consumes a hook and renders.
Two named tiers:

- **Raw hook** — wraps one `useQuery`/`useMutation` and returns the library's result verbatim, `.data`,
  `.isPending` and `.mutate` included. The suffix is mandatory: `useOrderQuery`,
  `useAcceptOrderMutation`. A bare name on a raw hook is the violation.
- **Facade hook** — composes raw hooks and returns a remapped **domain** object (`useOrder` →
  `{ order, isLoading }`, `useApply` → `{ apply, canApply }`). It takes the plain domain name *because* it
  is no longer a raw query — it is the app-facing API, and it is where orchestration lives: invalidations,
  submit sequencing, listeners, navigate-versus-dialog branching. For a form, this is the mutation only —
  see `write-boundary` for why the form's own field state and validation live in `useForm`, not here.

Non-data hooks (`useDebounce`, `useIsMobile`) are neither and take no suffix. Hooks live in
`features/<feature>/hooks/`, one concern per file.

**Litmus:** *does the hook hand back the raw `useQuery`/`useMutation` object — `.data`, `.isPending`,
`.mutate`? → `…Query`/`…Mutation`. Does it hand back a domain shape? → plain `useX`.*

```ts
// CORRECT — orchestration in a facade hook; the component's useForm calls it with the validated request
function useInviteMember() {
  const mutation = useInviteMemberMutation();
  const submit = (request: InviteRequest, onDone: () => void) =>
    mutation.mutate(request, { onSuccess: onDone });
  return { submit, isPending: mutation.isPending };
}
```

**The anti-patterns:**

- **Mutation wiring inside a component** — instantiating a mutation and holding a submit handler with an
  inline `.mutate({…}, { onSuccess, onError })`, or building a whole request object in a submit handler.
  Move it to a facade hook; the component keeps the `useForm` call and the JSX.
- **Side-effect orchestration in a component** — wiring a `window` listener, then a refetch, then
  branching, then opening a window. That is a hook.
- **A hand-rolled `safeParse` call in a component or a facade hook** instead of `useForm` +
  `zodResolver` — see `write-boundary`. Hoist derivation that isn't form validation into the hook and
  render the result.

## An Effect is for syncing with something outside React

Only that: a socket subscription, a DOM listener. Mount-only ones go through a shared mount-effect hook.
An Effect is **not** how you respond to an event or compute derived data — that is the *you might not need
an Effect* trap, and it forces `useRef` guards to stop re-fire loops.

Route by trigger:

| Trigger | Where it goes |
|---|---|
| An event (click, open, submit) | an event handler |
| Derived from existing state | computed in render |
| Server data, read or write | a query or mutation hook (see `server-state`) |

## Dispatch on a closed key with one table

When behaviour varies by a closed key — a wire discriminator, a role, a mode — resolve it through **one**
table keyed on that value, with a `never` exhaustiveness arm so a new member breaks the build. Never
sprinkle the same switch or ternary on that key across components and hooks.

```ts
// CORRECT — one table, exhaustive; a new $type is a compile error
const render: Record<Price["$type"], (p: Price) => ReactNode> = {
  fixed: (p) => …, tiered: (p) => …, usage: (p) => …,
};
```

**The anti-patterns:**

- **A switch or ternary on the key inlined across components** — it gets copy-pasted and drifts.
- **A partial, hand-maintained permission or capability matrix.** A client catalog modelling four of the
  server's thirteen permissions silently desyncs the day the server's matrix changes. Model the full set,
  aligned to the server's constant names, and treat the server as the source — the client gate is cosmetic
  and the server enforces.
- **Returning a label the caller must re-switch.** Resolve to the value, not an enum every consumer
  reinterprets.
