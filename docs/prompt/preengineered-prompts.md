# Pre-Engineered Prompts

## Default multi-agentic process

Use at the start of every ESP32 workspace task:

```text
Apply the ESP32 default-multi-agentic-process. Classify the prompt as Tier 0,
Tier 1, Tier 2, or Tier 3. Emit a routing packet with verified facts,
assumptions, unknowns, owner role, evidence need, mutation boundary, reviewer
quorum, gate authority, validation plan, and trust boundary before
non-trivial mutation. Project-local read-only subagents are default-authorized
for safe Tier 2 and Tier 3 quorum; mutating workers require explicit disjoint
write scopes. End with a decision footer: continue, ask_user, blocked,
ready_for_mutation, or handoff; next gate; owner; evidence; approved mutation
boundary; validation; durable records; and authority limits.
```

## Research prompt

Use when filling a knowledge gap:

```text
Investigate the named hardware, protocol, or toolchain item. Use only directly
verifiable sources. Separate verified facts, unknowns, and inferred risks. Add
source-index entries before updating any factual profile.
```

## Firmware prompt

Use after the scoped project has an accepted framework and board ADR:

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
