---
name: data-tables
description: TanStack Table behind one shared DataTable component — features supply columns and rows and never touch useReactTable, flexRender or a row model themselves, row models past the core one are opt-in because each costs work on every render, client-side sorting and pagination are dropped wherever the server already does it (otherwise the table sorts one page and calls it sorted), column definitions live at module scope or memoized so the table does not lose its state to a new column identity each render, cells render rather than fetch or decide, and a list of non-comparable rows is not a table at all. Use when adding a table, adding sorting/filtering/pagination to one, writing a ColumnDef or cell renderer, or reviewing a component that builds its own table instance.
kind: contract
domain: react
profile: data-tables
applicability: React features rendering interactive data tables
requires: tanstack-table
provenance: framework, selected-library
---

# Tables

Owns how interactive data tables are built on TanStack Table behind one shared `DataTable` component.

TanStack Table, behind one `DataTable` component. A feature supplies **columns and rows**; it never touches
`useReactTable`, `flexRender`, or a row model.

## One table component owns the rendering

The shared component takes `columns` and `data`, builds the table instance, and renders the markup —
including the empty state, which is where hand-rolled tables reliably differ from each other.

```tsx
export function DataTable<TData, TValue>({ columns, data }: DataTableProps<TData, TValue>) {
  const table = useReactTable({ data, columns, getCoreRowModel: getCoreRowModel() });
  …
}
```

A second table built directly on `useReactTable` in a feature is the violation. Extend the shared component
— a new prop, a new opt-in row model — so every table gains the capability at once.

## Row models are opt-in, and cost what they add

`getCoreRowModel` is the floor. Sorting, filtering, grouping and pagination each need their own row model
and each does real work on every render; add one when the table needs it, not by default.

**Where the server already paginates, filters or sorts, do not also do it client-side.** The table renders
the page it was handed and the query owns which page that is — otherwise the table sorts 20 of 4,000 rows
and calls the result sorted.

## Columns are declared outside the render

A `ColumnDef[]` rebuilt on every render gives the table a new column identity each time, resetting the
state the row models hold. Declare columns at module scope, or memoize them when they close over something
that genuinely varies.

Keep the column definition declarative: a `header` string and a `cell` that renders. Fetching, navigation
decisions and business rules belong in the feature, not in a cell renderer.

## The table is presentation, not state

Server data reaches the table as the query's `data`. Selection, expansion and column visibility are table
state and live in the table instance. Nothing about a table belongs in a global store, and nothing about a
table should be written back to the server without an explicit mutation.

## When not to use a table at all

Two columns of key/value, or a list of cards with no shared axis, is not a table. A table earns its
overhead when rows are genuinely comparable across columns — otherwise it costs a dependency, a row model
and a header for markup a list would have done better.
