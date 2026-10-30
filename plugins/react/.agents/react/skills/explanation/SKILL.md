---
name: explanation
description: How TypeScript and TSX are quoted when explaining React code. Use when an explanation shows React or TypeScript source.
kind: standard
domain: react
profile: core
applicability: TypeScript and TSX code
requires: typescript
provenance: language, house
---

# Explaining React code

Owns how TypeScript and TSX are quoted in an explanation.

Quote each file in its own top-level `tsx` or `ts` block, never indented inside a list item, under a
`path:line` line. Copy the code verbatim and replace imports, prop type boilerplate, long className
strings and other lines the point does not need with `...`.

#### Example

````markdown
`src/components/Button.tsx:12`

```tsx
export function Button({ label, onClick }: ButtonProps) {
  ...
  return <button onClick={onClick}>{label}</button>;
}
```
````
