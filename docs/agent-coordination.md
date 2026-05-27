# Agent Coordination

## Required sequence

1. Read `AGENTS.md`.
2. Identify the owner role in `.agents/OWNERSHIP.md`.
3. Select the tier from the workspace multi-agent process.
4. State verified facts, assumptions, unknowns, owner role, mutation boundary,
   evidence need, and validation plan before non-trivial mutation.
5. Open or update a task record in `.agents/TASK_LOG/`.
6. Check source coverage before editing factual docs.
7. Leave validation evidence and handoff notes.

## Tiers

- Tier 0: trivial or read-only. Coordinator triage plus local role lens.
- Tier 1: normal docs, tests, or bounded code. Coordinator plus owner and QA
  lens; subagents optional.
- Tier 2: governance, protocol, firmware, evidence, hook/config, or broad code.
  Read-only reviewer quorum before mutation.
- Tier 3: live bench, flashing, wiring, radio, serial writes, relay/load/mains,
  or release gates. Same-session evidence and explicit gate authority required.

## Reviewer quorum

Tier 2 and Tier 3 work needs at least coordinator, relevant owner, and QA
perspectives before mutation. Project-local read-only subagents are
default-authorized when available and safe. Use local role lenses only when
subagents are unavailable or unsafe, and record that no subagents were spawned.

A no-P1/P2 reviewer quorum may accept only the named gate and mutation
boundary. Tier 3 acceptance also requires same-session evidence, explicit
live-gate authority, recovery path, and closed-surface review.

## Continuation decision

End non-trivial work with a decision footer: `continue`, `ask_user`,
`blocked`, `ready_for_mutation`, or `handoff`; the next gate or slice; owner
role; evidence need; approved mutation boundary; validation command; required
durable record; and authority limits.

## Project-local profiles

- Read-only reviewers: `governance-cartographer`, `evidence-record-auditor`,
  `live-bench-gate-reviewer`, `win31-dashboard-vision-gate`,
  `ui-code-protocol-analyst`, `source-skill-curator`,
  `prompt-token-triage`, and `qa-validation-reviewer`.
- Workers: `governance-doc-worker`, `kb-record-worker`, and
  `bounded-implementation-worker`.
- Workers require an explicit disjoint write scope from the parent and must
  preserve dirty work, avoid framework selection, avoid live hardware actions,
  list changed paths, and skip commit/push unless explicitly requested.

## Enforcement

No feature or factual document should be considered accepted unless it has:

- a task record,
- a source-index reference where factual claims are made,
- explicit unknowns,
- validation results,
- an owner for the next action,
- selected tier and mutation boundary for non-trivial work.
- continuation decision and authority limits.

Project-local Codex hooks under `.codex/hooks.json` add model-visible reminders
for triage, subagent boundaries, and mutating tool calls. They are advisory
runtime aids until the active Codex runtime reviews and trusts them.
