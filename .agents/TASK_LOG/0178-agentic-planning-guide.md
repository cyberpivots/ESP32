# Task 0178: Agentic Planning Guide

Status: completed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-05

Source IDs:
`SRC-LOCAL-AGENTIC-PLANNING-GUIDE-2026-06-05`,
`SRC-CODEX-SUBAGENTS-2026-06-05`,
`SRC-CODEX-SUBAGENT-CONCEPTS-2026-06-05`,
`SRC-CODEX-CONFIG-REFERENCE-2026-06-05`,
`SRC-LOCAL-DEVELOPMENT-PLAN-CONSOLIDATION-2026-05-27`,
`SRC-LOCAL-DEVELOPMENT-AGENT-PANEL-2026-05-31`,
`SRC-LOCAL-SUBAGENT-LIFECYCLE-CLEANUP-2026-06-01`,
`SRC-LOCAL-ALWAYS-ON-SUBAGENT-PROCESS-ENFORCEMENT-2026-06-02`

## Routing

- Verified facts: the user requested a durable implementation of the prior
  plan, then explicitly requested increasing the allowed depth of subagent
  threads. `.codex/config.toml` had `agents.max_threads = 6` and
  `agents.max_depth = 1`. `scripts/scaffold_audit_agent_process.py` required
  `agents.max_depth == 1`. Current official Codex docs describe
  `agents.max_depth`, default it to `1`, and warn that raising depth increases
  token, latency, local resource, and predictability risk.
- Assumptions: `max_depth = 2` is the conservative requested increase because
  it permits one nested subagent layer for bounded recursive read-only
  evidence gathering while keeping `max_threads = 6`. The guide is internal
  repo documentation, not a public-site artifact.
- Unknowns: future Codex sessions may need a reload/new thread to honor the
  changed project config. Future subagent availability and lifecycle visibility
  remain runtime-dependent. Public-site inclusion remains unopened.
- Selected tier: Tier 2 governance/config/docs/records.
- Owner role: Agent Operations with QA, Tooling, and Evidence Records.
- Evidence need: required governance docs, `.codex/config.toml`, current
  official Codex docs, scaffold audit scripts, docs index, prompt docs, prompt
  registry, development plan, triage status, known gaps, source index, and
  read-only reviewer quorum output.
- Mutation boundary: `.codex/config.toml`,
  `scripts/scaffold_audit_agent_process.py`,
  `docs/agentic-planning-guide.md`, `docs/index.md`,
  `docs/agent-coordination.md`, `docs/prompt/prompt-triage.md`,
  `docs/prompt/preengineered-prompts.md`,
  `knowledge-base/prompt-registry.md`,
  `research/development-plan.md`, `research/triage-status.md`,
  `research/known-gaps.md`, `knowledge-base/source-index.md`,
  `knowledge-base/source-ledger/2026-06-05-agentic-planning-guide.md`,
  and this task record.
- Reviewer quorum: read-only project-local subagents were spawned, waited, and
  closed after output capture. Lifecycle state was not listable before
  spawning, so no prior completed-agent inventory was visible. After
  clarification, development-panel coordinator, QA validation, evidence-record
  auditor, and tooling-resource reviewer approved the named Tier 2 boundary
  with conditions. Weighted result: 14/14 approval, threshold 70 percent, no
  P1/P2 blockers for the pre-mutation gate.
- Gate authority: docs/config/audit/records only. No live bench, flash,
  monitor, serial/RF/XBee write, firmware runtime, wiring, relay/load/mains,
  signing, release, publication, commit, push, PR, deploy,
  `/etc/codex/requirements.toml`, or `admin-strict` authority is opened.
- Validation plan: run `git status --short --branch --untracked-files=all`,
  `git diff --check`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 178`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`, and a
  path-scoped diff/name-status check for this boundary.
- Trust boundary: local repo records and current official Codex docs. Hooks and
  managed profiles remain advisory under `bypassPermissions`; parent-side
  lifecycle cleanup remains required.

## Implementation

- Added [../../docs/agentic-planning-guide.md](../../docs/agentic-planning-guide.md)
  as the start-here guide for future agents.
- Changed [../../.codex/config.toml](../../.codex/config.toml) to keep
  `agents.max_threads = 6` and set `agents.max_depth = 2`.
- Updated [../../scripts/scaffold_audit_agent_process.py](../../scripts/scaffold_audit_agent_process.py)
  to require `agents.max_depth == 2`.
- Linked the guide from docs index, agent coordination, prompt triage,
  pre-engineered prompts, and prompt registry.
- Added source precedence notes to the development plan, triage status, and
  known gaps.
- Added current Codex source rows and the local source ledger/source-index row
  for this guide.

## Validation

Passed on 2026-06-05:

- `git status --short --branch --untracked-files=all` captured the broad
  pre-existing dirty tree and this task's new paths.
- `git diff --check` exited `0` with the pre-existing CRLF normalization
  warning for
  `apps/cbbs-hardware-tools-windows/windows/CbbsHardwareToolsWindows/CbbsHardwareToolsWindows.cpp`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 178`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- Path-scoped diff/name-status was checked for the approved boundary.

## Authority Limits

Still closed: live bench, prepare/flash/complete, erase, monitor, serial
writes, RF/XBee writes, XBee profile writes, HostCommandBridge live dispatch,
native adapter execution, shell execution, firmware runtime migration, BLE,
Web Bluetooth, Web Serial, live mesh, PCAP, router/admin mutation, Windows
Wi-Fi mutation, relay/load/mains, wiring-under-power, signing, Store/App
Installer distribution, EAS, App Center, release, publication, commit, push,
PR, deploy, `/etc/codex/requirements.toml`, and `admin-strict` installation.

## Handoff

No handoff is required if validation passes. Future public-site inclusion,
deeper subagent fan-out beyond `max_depth = 2`, managed policy installation,
release/publication, or live hardware work requires a separate gate.

## Decision

Decision: accept the bounded Tier 2 agentic planning guide and project-local
subagent-depth config update. `agents.max_depth = 2` is accepted only as a
bounded recursive read-only evidence delegation allowance with
`agents.max_threads = 6`; all Tier 3, system-policy, release, publication, and
hardware surfaces remain closed.
