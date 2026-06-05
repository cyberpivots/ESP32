# Source Ledger - 2026-06-05 Agentic Planning Guide

## Scope

Tier 2 governance/config/docs/records update adding a durable start-here
agentic planning guide, raising project-local subagent nesting from
`agents.max_depth = 1` to `agents.max_depth = 2`, and updating the matching
agent-process audit expectation.

This ledger covers only repo-local process documentation, project-local Codex
configuration, and scaffold validation. It does not authorize live hardware,
flashing, monitor, serial/RF/XBee writes, relay/load/mains work, signing,
release, publication, commit, push, PR, deploy, `/etc/codex/requirements.toml`,
or `admin-strict` installation.

## Source IDs

- `SRC-LOCAL-AGENTIC-PLANNING-GUIDE-2026-06-05`
- `SRC-CODEX-SUBAGENTS-2026-06-05`
- `SRC-CODEX-SUBAGENT-CONCEPTS-2026-06-05`
- `SRC-CODEX-CONFIG-REFERENCE-2026-06-05`
- `SRC-LOCAL-DEVELOPMENT-PLAN-CONSOLIDATION-2026-05-27`
- `SRC-LOCAL-DEVELOPMENT-AGENT-PANEL-2026-05-31`
- `SRC-LOCAL-SUBAGENT-LIFECYCLE-CLEANUP-2026-06-01`
- `SRC-LOCAL-ALWAYS-ON-SUBAGENT-PROCESS-ENFORCEMENT-2026-06-02`

## Verified Facts

- `AGENTS.md` is the canonical ESP32 workspace operating contract.
- The required governance docs were re-read before mutation:
  `.agents/GOVERNANCE.md`, `.agents/OWNERSHIP.md`, `.agents/ROLES.md`,
  `docs/index.md`, and `knowledge-base/source-index.md`.
- Current official Codex docs describe `agents.max_depth` as spawned-agent
  nesting depth, document default depth `1`, and warn that raising depth is for
  specific recursive-delegation needs because it increases token, latency,
  local resource, and predictability risk.
- The user explicitly requested increasing the allowed depth of subagent
  threads.
- The implementation keeps `agents.max_threads = 6` and changes only
  `agents.max_depth` to `2`.
- `docs/agentic-planning-guide.md` records source precedence, stale-record
  refresh rules, dirty-tree boundaries, lifecycle cleanup, weighted quorum,
  lane routing, serialized packet shapes, bounded subagent-depth guidance, and
  decision footer requirements.
- The guide points agents to the current plan, status ledger, known gaps,
  source index, task logs, handoffs, and source ledgers rather than creating a
  second roadmap.

## Assumptions

- `max_depth = 2` is the conservative interpretation of the user request: it
  permits one nested subagent layer for bounded recursive read-only evidence
  gathering while preserving the six-thread cap.
- Future Codex sessions may need a new thread, restart, or config reload before
  honoring the changed project config.
- The guide is internal repo documentation, not public-site publication.

## Unknowns

- Future Codex runtime subagent availability and lifecycle visibility remain
  runtime-dependent.
- Whether future tasks need nested subagents is lane-specific and must be
  justified in each routing packet.
- Public-site inclusion of the guide remains unopened.

## Reviewer Quorum

Project-local read-only subagents were attempted and completed before
mutation. The parent captured outputs and closed all reviewer agents after
recording their votes.

| Role | Weight | Vote | Disposition |
| --- | ---: | --- | --- |
| Development panel coordinator | 5 | approve with conditions | No P1/P2 for the bounded mutation after clarification. |
| QA validation reviewer | 3 | approve with conditions | No P1 blocker to mutation; required path-scoped diff and validation. |
| Evidence record auditor | 3 | approve with conditions | No P1/P2 if Task 0178, source ledger, source rows, and audit update are added. |
| Tooling resource reviewer | 3 | approve with conditions | Required config and audit expectation to move together from depth 1 to 2. |

Weighted disposition: 14/14 approved for the named Tier 2 mutation boundary
after clarification. Threshold: 70 percent. No P1/P2 blockers remain for the
pre-mutation gate.

## Validation

Passed on 2026-06-05:

- `git diff --check` exited `0` with the pre-existing CRLF normalization
  warning for
  `apps/cbbs-hardware-tools-windows/windows/CbbsHardwareToolsWindows/CbbsHardwareToolsWindows.cpp`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 178`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.

## Decision

Decision: accept the bounded Tier 2 docs/config/audit/records mutation for the
agentic planning guide and `agents.max_depth = 2`. Keep all Tier 3, system
policy, release, publication, and hardware authority closed.
