# Server state

## React Query owns all server state

Every server **read** is a `useQuery` and every server **write** is a `useMutation`, wrapped in a per-feature hook
(naming in the `react-structure` skill). **Never call an api module from a `useEffect`, and never hand-roll
`useState` + `useEffect` + a promise to load or send server data.**

React Query already owns caching, request **dedup** (including a strict-mode dev double-mount), retries,
routing errors to the central `QueryCache`/`MutationCache` handler, and `isPending`/`isError` state. A fetching `useEffect` re-implements
all of that by hand and worse: it double-fires under strict mode, drops the result when the component
unmounts before the promise settles, and races on out-of-order responses. Those are the exact bugs the
library exists to remove.

**This holds even for a one-shot, fire-on-mount action** — accepting an invitation from an emailed link, for
instance. That is a `useQuery`, which fires on mount and dedupes by key, not
`useEffect(() => { api.accept(id).then(navigate) }, [])`. The success side effects run at the tail of the
`queryFn`, not in a follow-up effect reacting to the result.

> **Anti-pattern:** `useEffect(() => { api.getX().then(setX) }, [])`, or an on-mount `mutate()` guarded by a
> `useRef` to dodge the strict-mode re-fire. Both are a hand-rolled reimplementation of `useQuery`.

**Litmus:** *reading or writing server data? → a `useQuery`/`useMutation` hook. Reaching for `useEffect` or
`useState` to load or send it? → that's the violation.*

## A `queryFn` may never resolve to `undefined`

React Query v5 throws `Query data cannot be undefined` the instant a `queryFn` resolves to `undefined` —
a runtime throw the moment that branch is hit, not a lint warning. This is the one place the
`typescript-style` skill's "absent values default to `undefined`" default is wrong: an api-module call
that is awaited directly inside, or handed unchanged as, a `queryFn` — and whose result can genuinely come
back empty (a 404 the client treats as "not found yet", a 204, a `null` JSON body) — must resolve to
`T | null`, never `T | undefined`.

```ts
// WRONG — the undefined branch crashes the query the moment a caller has none yet
getMine: async (): Promise<Thing | undefined> => {
  const { data, status } = await api.get<Thing>(BASE);
  return status === 204 ? undefined : data;
},

// CORRECT
getMine: async (): Promise<Thing | null> => {
  const { data, status } = await api.get<Thing>(BASE);
  return status === 204 ? null : data;
},
```

A hook built on top of that call may still normalize back to `undefined` for its own **public** return
type (`query.data ?? undefined`) — that conversion runs after the promise has already resolved, so it
never reaches the `queryFn` contract. The rule binds only the raw value a `queryFn` awaits or returns
unwrapped.

**Litmus:** *awaited directly inside, or handed unchanged as, a `queryFn`? → `T | null`, never
`T | undefined`. Everywhere else — DTOs, request bodies, ordinary optional fields — the `typescript-style`
default of `undefined` still applies.*

## Query keys — arrays, generic to specific, one factory per feature

Keys are arrays ordered most-generic to most-specific with the resource name first —
`["shipments", "order", orderId]` — so invalidation works by prefix. Centralize a feature's
keys in one exported factory object, so a key and its invalidations cannot drift apart across files.

## Mutation variables versus form state

- **The live controlled-input buffer is local `useState` in the component.** It is *not* an `XRequest`, and
  it **never holds server data copied out of the query cache** — copying breaks background refetch.
- On submit, the component maps its buffer to the `XRequest` and passes that as the mutation's **variables**.
- **The mutation hook binds everything constant for its lifetime** — route ids, success invalidations — and
  takes only the per-submit variables. Don't thread a fixed id through the mutation call if the hook already
  closed over it.

The parse that turns a buffer into a request is the `write-boundary` skill's subject.

**Litmus:** *changes per submit → a mutation variable. Fixed for the hook's life → bound inside the hook.*
