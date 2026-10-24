---
name: ui-components
description: Component API and composition for explicitly selected Radix/shadcn primitives, owned generic UI, icons, operation toasts and optional animation. Use when building a component primitive, changing its API or composing feature UI. Tailwind class merging and visual variants belong to react:styling.
kind: contract
domain: react
profile: ui
applicability: React applications using the selected primitive component stack
requires: radix-or-shadcn
provenance: ui, selected-library
---

# UI components

Owns component API/composition and the selected owned primitive layer, including icons, operation toasts
and optional animation. `react:styling` owns the selected Tailwind implementation. Component selection
does not require that styling choice; a CSS Modules project does not inherit Tailwind/cva rules.

```tsx
// A feature composes the selected generic primitive; domain behavior stays with the feature.
<Button onClick={save} disabled={pending}>Save</Button>
```

## Copy-in primitives are owned code

Primitives generated into `components/ui/` (the shadcn model over Radix) are **your files**. Edit them in
place when the design needs it; they are not vendored dependencies to leave untouched and wrap.

Two rules keep that from turning into drift:

- **A primitive is generic.** No feature vocabulary, no domain type, no data fetching. The moment a
  primitive imports from a feature, it stopped being a primitive.
- **A feature never re-implements one.** If the button needs a new tone, the button gains a variant.

Do not add a second component library alongside the primitives already in the tree, and do not add a
CSS-in-JS runtime — the point of utilities plus owned primitives is that there is one place to look.

## One icon set, one toast library

Pick a single icon package and import from it directly; mixing sets is visible on screen. Toasts come from
one library, mounted once at the root.

**Fire the toast from the hook that owns the operation, not from the component that rendered the button.**
The mutation knows whether it succeeded; the component should not have to. That also keeps the message from
appearing twice when two components trigger the same mutation.

## Animation is opt-in and local

An animation library earns its place at genuine entrance/exit and layout transitions. Reach for a CSS
transition first — most hover, focus and open/close states need nothing more.

Never animate on every render, and never make an animation load-bearing for whether content is reachable:
if the library fails to load, the page must still show its content.
