# Canonical source migration

Use `react:structure` for React code organization. The previous
`react:react-structure` name forwards to it through 2027-03-31; new routes and
references should use the short name.

The former `standards/react` documents and `.agents/skills` routers were folded into complete definitions under
`.agents/contract`. Public skill names did not change. Consumers should select profiles from
`plugins/react/selection.json`; installing the plugin makes capabilities discoverable but does not make every
optional library or repository-shape rule applicable.
