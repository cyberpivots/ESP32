# Agent Operating Contract

This workspace supports multi-agent development for ESP32-based devices,
custom firmware, communication interfaces, and verified hardware integrations.

## Non-negotiable rules

- Do not make unverified hardware, protocol, toolchain, or wiring claims.
- Keep verified facts, assumptions, and unknowns in separate sections.
- Do not select Arduino, ESP-IDF, PlatformIO, or any other framework until an
  accepted ADR changes the framework-neutral status.
- Do not add source code that depends on a specific framework during the
  scaffold phase.
- Do not copy vendor PDFs or bulky source artifacts into the repository.
  Store source links and concise verified summaries instead.
- Hardware bring-up work must identify power, voltage, boot-pin, and isolation
  risks before recommending bench actions.

## Multi-Agent Process For Every Prompt

Every prompt starts with coordinator triage. The coordinator must select a tier,
owner role, evidence need, mutation boundary, and validation plan before
non-trivial mutation. Trivial read-only prompts can stay lightweight, but they
still use the same classification.

- Tier 0: trivial or read-only lookup. Use coordinator triage plus a local role
  lens. Subagents are not required.
- Tier 1: normal docs, tests, or bounded code. Use coordinator triage plus the
  relevant owner and QA lens. Subagents are optional when they reduce risk.
- Tier 2: governance, protocol, firmware, evidence, hook/config, or broad code
  work. Run a read-only reviewer quorum before mutation, either through
  project-local subagents when explicitly authorized and safe or through local
  role perspectives when subagents are unavailable.
- Tier 3: live bench, flashing, wiring, radio configuration, serial writes,
  relay/load/mains work, release gates, or other risky hardware-adjacent work.
  Require same-session evidence, explicit gate authority, recovery path, and
  reviewer quorum before mutation.

Before Tier 1 or higher mutation, state:

- verified facts,
- assumptions,
- unknowns,
- selected tier,
- owner role,
- mutation boundary,
- validation plan.

For Tier 2 and Tier 3 work, preserve dirty-tree boundaries, keep write scopes
disjoint for worker agents, and do not spawn mutating workers unless their
write scope is explicit. If subagents are unavailable or unsafe, run the same
role lenses locally and record that no subagents were spawned.

## Required reading before edits

1. `.agents/GOVERNANCE.md`
2. `.agents/OWNERSHIP.md`
3. `.agents/ROLES.md`
4. `docs/index.md`
5. `knowledge-base/source-index.md`

## Evidence rule

Any factual change under `hardware-profiles/`, `comm-protocols/`, `firmware/`,
or `docs/architecture/` must cite a source listed in
`knowledge-base/source-index.md`, or mark the item as an unresolved gap.

## Handoff rule

Each non-trivial task must leave a task record in `.agents/TASK_LOG/` and, when
another role needs to continue the work, a handoff in `.agents/handoffs/`.
