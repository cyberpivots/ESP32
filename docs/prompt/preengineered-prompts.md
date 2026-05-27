# Pre-Engineered Prompts

## Default multi-agentic process

Use at the start of every ESP32 workspace task:

```text
Apply the ESP32 default-multi-agentic-process. Classify the prompt as Tier 0,
Tier 1, Tier 2, or Tier 3. State verified facts, assumptions, unknowns, owner
role, mutation boundary, and validation plan before non-trivial mutation. Use
project-local subagents only when explicitly authorized and safe; otherwise run
the same role lenses locally and record that no subagents were spawned.
```

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
