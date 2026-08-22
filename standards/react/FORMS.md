# The write boundary

Every user-editable form is `react-hook-form`'s `useForm`, validated by a **zod** schema through
`@hookform/resolvers/zod`, mapped to the `XRequest` by the resolver — never a hand-rolled `useState` per
field plus a manual `schema.safeParse` call. A form with free-typed fields and no schema is the
violation; a form that reimplements what `useForm` already does is the other one.

```ts
const {
  register,
  handleSubmit,
  formState: { errors, isValid },
} = useForm<UpdateOrderRequest>({
  resolver: zodResolver(updateOrderRequestSchema),
  defaultValues: { reference: "" },
  mode: "onBlur", // or "onChange" for validation as the user types, not just after a blur/submit
});

const onValid = (request: UpdateOrderRequest) => updateOrder(request);

<form onSubmit={handleSubmit(onValid)}>
  <input {...register("reference")} aria-invalid={errors.reference != null} />
  {errors.reference && <p>{errors.reference.message}</p>}
  <button type="submit" disabled={isPending || !isValid}>Save</button>
</form>
```

The resolver does two jobs a hand-rolled `if` cannot do together:

- **It narrows the type at the boundary.** `handleSubmit(onValid)` only ever calls `onValid` with data
  proven present and correctly typed by the schema, so nothing downstream needs a `!` bang or a
  `?? fallback`. **The non-null assertion *is* the missing validation** — a schema removes it honestly
  instead of asserting past it.
- **It feeds inline field errors for free.** `formState.errors` carries per-field messages the component
  renders next to each input, and `formState.isValid` gates the submit button — React state reflects
  *actual* validity, the UX a server 400 can only deliver after a round trip.

The schema lives in `features/<feature>/schemas/`. Keep it aligned to the request with
`type XRequest = z.infer<typeof xRequestSchema>`, which makes drift a compile error, while the naming and
camelCase wire rules still hold.

## `register` for native inputs, `Controller` for anything controlled

A plain `<input>`/`<textarea>`/`<select>` takes `{...register("field")}` — `react-hook-form` manages its
value uncontrolled, which is also why it doesn't re-render the whole form on every keystroke. A custom
component that owns its own value/onChange contract (a design-system `Select`, a rich text editor, a
date picker) can't take `register` directly — wrap it in `Controller` instead:

```tsx
<Controller
  control={control}
  name="outcome"
  render={({ field }) => (
    <Select
      options={outcomes}
      value={outcomes.find((o) => o.value === field.value)}
      onChange={(o) => field.onChange(o.value)}
      getLabel={(o) => o.label}
      getValue={(o) => o.value}
    />
  )}
/>
```

## Reshape *in the schema*, never after the parse

Inputs are flat because that is how a form renders; the request is sometimes nested because that is how
the API models it, or needs normalization (an empty string is absent, not `""`; a checkbox gates a
sibling field). Because the resolver validates the raw form values directly, **the reshape belongs in
the schema itself** — `.trim()`, `.transform()`, a `.refine()` for cross-field rules — not in a
post-submit mapping step:

```ts
export const resolveReportRequestSchema = z.object({
  outcome: z.enum(["noActionTaken", "contentRemoved", "referredToLegal"]),
  notes: z.string().trim().transform((v) => v || undefined).optional(),
});
```

**Mapping after `handleSubmit` resolves is the mistake**, and it is a quiet one: it puts a second shape
between the validated data and the wire, so the thing the schema proved correct is not the thing sent.
Every conditional drop and every empty-string-to-`undefined` normalization belongs in the schema, because
those decide what counts as valid — they must happen as part of validation, not after it.

**Client validation is a UX affordance, not a trust boundary.** The server re-validates every field
regardless. Never drop a server check because the client has one.

## The facade hook owns the mutation, not the form

With `react-hook-form` owning field state and validation, a feature's facade hook (`useResolveReport`,
`useInviteMember`) shrinks to what only it can do: call the mutation with an already-validated request,
and handle the success/error side effects (toast, invalidation, closing a dialog). It takes the typed
`XRequest` `handleSubmit` already produced — never a raw, unvalidated draft:

```ts
export function useInviteMember() {
  const { mutate, isPending } = useInviteMutation();
  const submit = (request: InviteRequest, onDone: () => void) =>
    mutate(request, { onSuccess: () => { toast.success("Invited"); onDone(); } });
  return { submit, isPending };
}
```

There is no longer a separate `XBuffer`/`XDraft` type to name — `react-hook-form` *is* the pre-validation
form state. A feature that still exports one is holding onto the pattern this section replaced.

**The anti-patterns:**

- **A `useState` per field plus a manual `schema.safeParse` call** — the pattern `react-hook-form`
  replaces. If a component is calling `.safeParse` itself rather than through a `resolver`, it's
  reimplementing the library.
- **A hand-maintained `XBuffer`/`XDraft` type mirroring the form's fields** — once `useForm` owns the
  fields, there's nothing left for that type to name.
- **Raw values mapped to a request with a `!` bang or a `?? fallback`** after `handleSubmit` resolves.
  The bang is the missing schema coverage.
- **A form with free-typed fields and no schema** — no `schemas/` folder for a feature with editable
  inputs is the tell.
- **Client validation reported by a toast** instead of inline from `formState.errors`.

**Litmus:** *a field the user can type into, with nothing validating it before the mutation call? → add
the schema and wire it through `useForm` + `zodResolver`. Reaching for `useState` and a manual
`safeParse` instead of `useForm`? → that's the violation this section names.*
