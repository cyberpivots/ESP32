# Agentic Planning Guide

Source index: [../knowledge-base/source-index.md](../knowledge-base/source-index.md)

This guide is the start-here operating map for future agents. It does not
replace [../AGENTS.md](../AGENTS.md), the consolidated development plan, the
status ledger, ADRs, task logs, handoffs, or source ledgers. It tells agents
where current truth lives, how to route work, and how to serialize decisions so
the next agent can continue without widening authority.

## Source Precedence

1. `AGENTS.md` is the canonical workspace operating contract.
2. Accepted ADRs under `.agents/DECISIONS/` govern accepted technical
   decisions.
3. `knowledge-base/source-index.md`, source ledgers, task logs, handoffs, and
   bench records govern accepted local evidence.
4. `research/development-status-ledger.md` is the detailed status spine.
5. `research/development-plan.md` is the singular next-action plan, not a
   replacement for evidence.
6. Current official OpenAI Codex docs govern Codex product behavior such as
   subagent configuration; local docs govern how this workspace applies it.

When these records conflict, use the latest accepted ADR/source-index/task/
source-ledger record for the lane and mark older summary wording stale instead
of copying it forward.

## Continuous Start Sequence

Every non-trivial prompt starts here:

1. Read `AGENTS.md`, `.agents/GOVERNANCE.md`, `.agents/OWNERSHIP.md`,
   `.agents/ROLES.md`, `docs/index.md`, and
   `knowledge-base/source-index.md`.
2. Check `git status --short --branch --untracked-files=all` and preserve
   dirty-tree boundaries.
3. Classify the prompt by tier, owner, evidence need, mutation boundary,
   reviewer quorum, gate authority, validation plan, and trust boundary.
4. Attempt project-local read-only subagents when the selected tier requires
   them and the tools are available and safe.
5. Capture reviewer votes, then close reviewer agents with `close_agent` after
   output is preserved. If lifecycle state is not visible, record that fact.
6. Mutate only after the named boundary has no P1/P2 blockers for the
   pre-mutation gate.
7. Leave a task record and, when another role must continue, a handoff.

## Dirty-Tree Boundaries

- Treat existing dirty files as user-owned unless the current task explicitly
  names them.
- Before editing an already-dirty file, read it and keep the change scoped to
  the current task.
- Record the intended path boundary in the task log before mutation.
- Validate with a path-scoped diff when shared files such as `docs/index.md` or
  `knowledge-base/source-index.md` already contain unrelated changes.
- Never use destructive git cleanup unless the user explicitly requests it.

## Subagent Limits

Project config currently allows:

```toml
[agents]
max_threads = 6
max_depth = 2
```

`max_depth = 2` is a bounded recursive-delegation allowance for cases where a
read-only reviewer needs one nested evidence-gathering helper. It is not a
default fan-out instruction. Keep `max_threads = 6`, ask nested agents for
small evidence-only tasks, and avoid repeated broad delegation. Official Codex
docs warn that deeper nesting can increase token use, latency, local resource
use, and predictability risk.

The main thread owns decisions, authority, dirty-tree boundaries, durable
records, and final validation. Read-only subagents gather noisy evidence.
Mutating workers run only after an approved gate names a disjoint write scope.

## Reviewer Quorum

Use weighted veto for Tier 2 and Tier 3 gates:

| Role class | Weight |
| --- | ---: |
| Coordinator or architecture-risk | 5 |
| High-reasoning specialist | 3 |
| Medium specialist | 2 |
| Low-risk helper | 1 |

A gate passes only when required roles are present, approval weight is at
least 70 percent, and no P1/P2 blockers remain for the named mutation
boundary. Tier 3 also requires same-session evidence, explicit live-gate
authority, recovery path, reviewer quorum, and closed-surface review. Weights
cannot waive Tier 3 prerequisites.

## Lane Router

| Lane | Start with | Owner roles | Current default gate |
| --- | --- | --- | --- |
| Governance and agent process | `AGENTS.md`, this guide, `docs/agent-coordination.md` | Agent Operations + QA + Tooling | Tier 2 docs/config/records |
| ESP-NOW BBS | `research/development-status-ledger.md`, ESP-NOW project docs | Communications + QA | Tier 2 host/design unless live gate is named |
| DOS-C and Win31 | Status ledger, task/handoff records, copied evidence records | UI/Protocol + QA | Tier 2 copied evidence or host-only work |
| Custom wireless protocol | ADR-0006/0007/0008 and protocol docs | Communications + Firmware + QA | Tier 2 host/design |
| Mesh M3 | Mesh discovery docs and `mesh_discovery.v1` records | Communications + Architecture + QA | Tier 2 design review |
| LCD and PF0530V-W | LCD menu tasks, source ledgers, LCD skill docs | LCD/UI + Firmware + QA | Tier 2 host/visual records unless live authority is named |
| Four-relay XBee Wi-Fi | Four-relay docs, XBee study docs, known gaps | Hardware + Firmware + Communications + QA | Tier 2 docs/tooling |
| XBee radio | XBee radio study, read-only live-radio records | Communications + Hardware + QA | Tier A read-only identity evidence |
| Remote LCD XBee solar client | Private submodule stream docs | Hardware + Power/Safety + QA | Tier 2 hardware identity intake |
| CBBS React Native and RNW | CBBS React Native project docs and RNW records | React Native + DevEx + QA + Security | Tier 2 host-only unless native runtime gate is named |
| Hardware Tools | Hardware Tools app docs and bridge records | Tooling + RNW + QA + Security | Tier 2 host-only |
| Rapid prototyping | Hardware rapid prototyping docs | Hardware + Fabrication/CAD + Safety + QA | Tier 2 docs/CAD source only |
| Public docs and Pages | `docs/index.md`, Pages docs, release records | Release + QA | Tier 2 validation before publication |
| Scripts, tests, simulators | `tests/README.md`, scaffold audit scripts | Tooling + QA | Tier 1 or Tier 2 by blast radius |

Approved next sequencing for this guide:

1. Host protocol/custody review.
2. Mesh M3 design review.
3. PF0530W visual/host validation.
4. XBee Tier A identity evidence.
5. Remote solar-client hardware intake.
6. Separately gated Tier 3 packets only after same-session evidence and
   explicit authority.

## Serialized Packets

Use JSON-compatible packets in task logs, source ledgers, handoffs, or review
summaries when a compact durable shape is useful.

### `routing_packet.v1`

```json
{
  "schema": "routing_packet.v1",
  "tier": "Tier 2",
  "ownerRole": "Agent Operations + QA",
  "verifiedFacts": [],
  "assumptions": [],
  "unknowns": [],
  "evidence": [],
  "sourceIds": [],
  "dirtyTreeBaseline": {
    "statusCommand": "git status --short --branch --untracked-files=all",
    "preExistingDirtyPaths": [],
    "taskOwnedPaths": []
  },
  "mutationBoundary": [],
  "quorum": {
    "requiredRoles": [],
    "subagentAttempt": "attempted",
    "lifecycleCleanup": "closed_after_capture"
  },
  "gateAuthority": [],
  "validation": [],
  "durableRecords": [],
  "trustBoundary": []
}
```

### `reviewer_vote.v1`

```json
{
  "schema": "reviewer_vote.v1",
  "role": "qa-validation-reviewer",
  "weight": 3,
  "evidenceReviewed": [],
  "p1Findings": [],
  "p2Findings": [],
  "vote": "approve_with_conditions",
  "conditions": [],
  "confidence": "high",
  "authorityLimits": []
}
```

### `decision_packet.v1`

Use the packet shape accepted by
[../scripts/agent_process_decision.py](../scripts/agent_process_decision.py).
Required fields include `gate`, `tier`, `approvalThreshold`,
`requiredRoles`, `tier3Prerequisites`, `votes`, `evidenceGaps`, and
`workRemaining`. A decision can be `continue`, `ready_for_mutation`,
`ask_user`, `blocked`, or `handoff`.

The gate passes only when required roles are present, weighted approval is at
least 70 percent, no P1/P2 blockers remain, and Tier 3 prerequisites are true
when Tier 3 is selected.

### `handoff_packet.v1`

```json
{
  "schema": "handoff_packet.v1",
  "sourceRole": "Agent Operations",
  "targetRole": "QA",
  "touchedFiles": [],
  "sourcesUsed": [],
  "decisions": [],
  "validation": [],
  "unresolvedGaps": [],
  "nextGate": "Tier 2 host-only validation",
  "authorityLimits": []
}
```

## Decision Footer

End non-trivial work with:

- Decision: `continue`, `ask_user`, `blocked`, `ready_for_mutation`, or
  `handoff`.
- Next gate or slice.
- Owner role.
- Evidence need.
- Approved mutation boundary.
- Validation command.
- Required durable record.
- Authority limits.

Do not use a decision footer to expand authority beyond the named gate.
