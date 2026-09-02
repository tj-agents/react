---
name: write-boundary
description: The client write boundary — every user-editable form is react-hook-form's useForm validated by a zod schema through @hookform/resolvers/zod, never a hand-rolled useState per field plus a manual safeParse call, so handleSubmit only calls its handler with data the schema already narrowed (removing the `!` bang and `?? fallback` that are the missing validation) with formState.errors/isValid giving per-field messages and a real submit gate for free; the schema lives in the feature's `schemas/` folder and is tied to the request with `z.infer` so drift is a compile error, register wires native inputs while Controller wires a custom controlled component, the reshape (trim, empty-to-undefined, conditional drops) lives in the schema itself via `.transform()` rather than a post-submit mapping step, the facade hook shrinks to just the mutation call (no separate XBuffer/XDraft type once useForm owns the fields), and client validation is a UX affordance rather than a trust boundary. Use when building or reviewing a form, wiring a field to a schema, seeing a non-null assertion on form data, reporting a validation message, or finding a component that calls .safeParse itself.
---

# write-boundary

The standard is `../../standards/react/FORMS.md`, shipped in this plugin. Read it and follow it; this skill only routes to it.
