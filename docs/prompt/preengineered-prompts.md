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

## Yolo-compatible managed-hook prompt

```text
Apply ESP32 yolo-compatible managed-hook governance. Before Tier 1+ mutation,
emit verified facts, assumptions, unknowns, selected tier, owner role, evidence
need, mutation boundary, validation plan, reviewer quorum, and weighted-veto
disposition. For every reviewer vote, record role, weight, evidence reviewed,
vote, blockers, conditions, and confidence. Do not proceed when required roles
are missing, weighted approval is below 70 percent, a P1/P2 blocker remains,
or Tier 3 live-gate authority fields are missing. When permission_mode is
bypassPermissions, hooks must not deny or block the user's intended
`codex --yolo` full-access launch.
```

## Agent instruction enforcement prompt

```text
Use agent instruction files as the enforcement surface. Treat AGENTS.md as
canonical and require every .codex/agents/*.toml developer-instruction profile
to inherit operator sovereignty: do not create, install, or rely on
/etc/codex/requirements.toml to restrict codex --yolo, danger-full-access,
approval_policy=never, or command prefix behavior unless the user explicitly
requests admin-strict by name. If permission_mode=bypassPermissions is visible,
do not deny or block; governance is advisory.
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
