---
name: styling
description: Apply selected Tailwind styling with clsx/tailwind-merge cn(), cva variants and theme tokens. Use when composing utility classes, changing visual variants or styling tokens in a project that explicitly selects these libraries; CSS Modules alone does not activate this skill.
kind: convention
domain: react
profile: styling
applicability: React projects selecting Tailwind utility styling
requires: tailwind, cva, clsx, tailwind-merge
provenance: ui, selected-library
---

# Styling

Owns the selected Tailwind class-merging, visual-variant and theme-token practices. Library policy and
selection live in `react:libraries`; component behavior and composition live in `react:ui-components`.
These rules do not apply to a CSS Modules-only project.

## Classes merge in `cn()`, nowhere else

`cn()` is clsx plus tailwind-merge, so a later utility actually beats an earlier one instead of both
landing in the class string and the loser winning by source order.

```ts
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Every component that accepts a `className` passes it through `cn()` last, so a caller can always override.
A component that concatenates class strings by hand, or that drops the caller's `className`, is a bug.

## Variants are `cva`, not stacked ternaries

A component with more than one visual axis (variant, size, tone) declares them once with **cva** and takes
the generated props. Ternaries in the class string are how two axes become an unreadable product of four.

```ts
const badgeVariants = cva("inline-flex items-center rounded-md border px-2 py-0.5", {
  variants: { variant: { default: "…", destructive: "…" } },
  defaultVariants: { variant: "default" },
});
```

## Dark mode and tokens

Colours come from CSS variables the theme defines, not from literal palette utilities scattered through
components. A component that hard-codes a specific shade renders wrong in the other theme, and the failure
shows up only in whichever mode the author was not using.
