# Multi-Window Codex Scheduler Source Ledger - 2026-06-01

## Scope

Tier 2 host-only tooling, hook, docs, test, and record update that adds an
advisory scheduler for coordinating up to five local Codex CLI windows in the
ESP32 workspace.

## Source Basis

- `SRC-CODEX-HOOKS-2026-05-27`
- `SRC-CODEX-CONFIG-REFERENCE-2026-05-27`
- `SRC-LOCAL-MULTI-AGENTIC-DEFAULT-PROCESS-2026-05-27`
- `SRC-LOCAL-MULTI-AGENTIC-CONTINUATION-DECISION-2026-05-27`
- `SRC-LOCAL-ADMIN-STRICT-CODEX-ENFORCEMENT-2026-05-28`
- `SRC-LOCAL-MULTI-AGENTIC-CONTINUOUS-ENFORCEMENT-2026-05-29`

## Verified Facts

- `scripts/agent_scheduler.py` implements a Python-stdlib JSON-over-Unix-socket
  scheduler daemon backed by SQLite.
- The scheduler stores live state in the user state directory under
  `codex/esp32-scheduler/<repo-id>/`, not in the Windows-mounted repository.
- The state schema is `multi_window_coordination.v1` and includes windows,
  claims, append-only events, and task-log/handoff record reservations.
- `window open` enforces the five-active-window limit with deterministic reject
  or queue behavior.
- `claim acquire` rejects overlapping active write/write claims, allows
  read/review overlap with stale-evidence warnings, records dirty-baseline
  overlap acknowledgement state, and keeps closed Tier 3 surfaces outside the
  advisory scheduler authority.
- `.codex/hooks/pre_tool_use_agent_process.py` calls `pretool-check` with a
  short timeout and emits model-visible context only.
- Scheduler unavailable and `permission_mode=bypassPermissions` paths remain
  advisory and do not emit deny/block decisions.

## Reviewer Quorum

- Governance/Agent Operations, weight 5: approved the host-only advisory
  scheduler boundary with source/task/docs record conditions.
- Tooling, weight 3: approved with conditions for timeout fallback, SQLite
  state outside the repo, stale lease coverage, and no hard permission gate.
- Security/Safety, weight 3: approved with closed-surface conditions and no
  credentials, external services, live hardware, `/etc/codex`, commit, push, or
  release authority.
- QA, weight 3: rejected acceptance until scheduler/doctor/fallback,
  dirty-baseline, and reservation-concurrency coverage existed. This task adds
  those tests as part of the mutation boundary.

## Outcome

- Added `scripts/agent_scheduler.py`.
- Added scheduler-focused scaffold tests in
  `tests/scaffold_audits/test_agent_scheduler.py`.
- Updated the project-local `PreToolUse` hook to append scheduler advisory
  context while preserving existing triage warnings.
- Added `docs/prompt/multi-window-codex-scheduler.md`, source-index and
  prompt-registry entries, docs-index links, and task log
  `.agents/TASK_LOG/0125-multi-agent-cli-window-scheduler.md`.

## Authority Limits

This task does not authorize `/etc/codex` mutation, admin-strict install, hard
`codex --yolo` blocking, Tier 3 live hardware, flashing, monitor, serial writes,
RF/XBee writes, relay/load/mains, credentials, external services, destructive
git, GitHub publication, release, commit, or push.
