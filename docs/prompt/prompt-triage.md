# Prompt Triage

## Goal

Route work requests to the smallest reliable agent/profile that can complete the
task while preserving evidence and validation requirements.

## Triage dimensions

- task type: research, architecture, firmware, hardware, QA, GitHub, release,
- tier: Tier 0, Tier 1, Tier 2, or Tier 3,
- risk level: low, medium, high, live/risky,
- evidence need: none, local, web, physical bench,
- mutation scope: read-only, docs, code, hardware,
- required owner role,
- reviewer quorum: none, local lenses, or read-only subagents,
- gate authority: named gate and mutation boundary only.

## Default tier rules

- Tier 0: read-only lookup or trivial formatting with no durable record change.
- Tier 1: narrow docs, tests, or code mutation inside a clear file boundary.
- Tier 2: governance, protocol, firmware contracts, evidence records, `.codex`
  hook/profile changes, or broad code work.
- Tier 3: live bench, flashing, wiring, radio, serial writes, relay/load/mains,
  release gates, or hardware-adjacent mutation.

## Routing rule

If a task touches live hardware, firmware flashing, power wiring, relays, or
radio configuration, route to high-rigor review and require a task-specific
bench plan.

For Tier 1 or higher mutation, state verified facts, assumptions, unknowns,
selected tier, owner role, evidence need, mutation boundary, and validation
plan. For Tier 2 and Tier 3 work, run a reviewer quorum before mutation.
Project-local read-only subagents are default-authorized when available and
safe; if they are not spawned, record the local role lenses used instead.

For Tier 2 and Tier 3 gates, a no-P1/P2 reviewer quorum may approve only the
named gate and mutation boundary. Tier 3 approval also requires explicit
gate authority, same-session evidence, recovery path, validation, and cleanup
or rollback criteria.

## Decision Footer

End non-trivial work with: decision, next gate or slice, owner role, evidence
need, approved mutation boundary, validation command, required durable record,
and authority limits.
