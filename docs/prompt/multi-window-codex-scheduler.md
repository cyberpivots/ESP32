# Multi-Window Codex Scheduler

## Source Basis

This prompt policy references `SRC-CODEX-HOOKS-2026-05-27`,
`SRC-CODEX-CONFIG-REFERENCE-2026-05-27`,
`SRC-LOCAL-MULTI-AGENTIC-DEFAULT-PROCESS-2026-05-27`,
`SRC-LOCAL-ADMIN-STRICT-CODEX-ENFORCEMENT-2026-05-28`,
`SRC-LOCAL-MULTI-AGENTIC-CONTINUOUS-ENFORCEMENT-2026-05-29`, and
`SRC-LOCAL-MULTI-WINDOW-CODEX-SCHEDULER-2026-06-01`.

## Verified Facts

- `scripts/agent_scheduler.py` is a host-only, Python-stdlib scheduler for
  coordinating local Codex CLI windows in this workspace.
- Runtime scheduler state is stored outside the repo under the user state
  directory, normally
  `~/.local/state/codex/esp32-scheduler/<repo-id>/`.
- The scheduler state schema is `multi_window_coordination.v1` and records
  windows, claims, record reservations, and append-only events.
- The daemon uses JSON over a Unix domain socket and stores state in SQLite.
- Project-local `PreToolUse` integration is advisory only. If the scheduler is
  unavailable, the hook emits `scheduler-unavailable` context and does not deny
  or block.
- When `permission_mode=bypassPermissions` is visible, scheduler context is
  advisory only and must not override operator sovereignty.

## Scheduler Commands

- `daemon ensure|start|stop|status`
- `window open|heartbeat|close`
- `claim acquire|renew|release|finalize`
- `record reserve|finalize`
- `preflight`
- `pretool-check`
- `doctor`
- `self-test`

## Conflict Model

- At most five windows may be active at once. A sixth window is rejected by
  default or placed in a deterministic queue when requested.
- Active `write` claims conflict with overlapping active `write` claims.
- `read` and `review` claims may overlap active writes, but the scheduler emits
  stale-evidence warnings.
- Claims touching paths that were dirty when the daemon captured its startup
  baseline emit dirty-baseline overlap warnings and record whether the overlap
  was explicitly acknowledged.
- Expired claim leases and stale window heartbeats are reaped through explicit
  `stale-reap` events.

## Closed Surfaces

The scheduler does not authorize Tier 3 work, credentials, external services,
release gates, destructive git, serial/RF/flash/relay/load/mains work, live
hardware, `/etc/codex` mutation, hard `codex --yolo` blocking, commit, push, or
release. Those surfaces remain closed unless a separate prompt opens an
explicit gate with the required same-session evidence and reviewer quorum.

## Validation

Expected host-only validation:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_agent_scheduler`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py self-test`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py doctor --repo /mnt/h/ESP32`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`
