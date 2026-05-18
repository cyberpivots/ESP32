# Pre-Engineered Prompts

## Research prompt

Use when filling a knowledge gap:

```text
Investigate the named hardware, protocol, or toolchain item. Use only directly
verifiable sources. Separate verified facts, unknowns, and inferred risks. Add
source-index entries before updating any factual profile.
```

## Firmware prompt

Use after ADR-0001 is accepted:

```text
Implement only the requested firmware behavior. Preserve framework and board
contracts. Cite any hardware constraints used. Add focused tests or a documented
manual validation path.
```

## Review prompt

```text
Review for unsupported claims, framework drift, missing source references,
missing safety notes, missing tests, and handoff gaps.
```

