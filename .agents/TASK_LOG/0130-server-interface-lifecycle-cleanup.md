# Server And Interface Lifecycle Cleanup

Status: Tier 2 host-only lifecycle cleanup implemented and focused validation passed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-01

## Routing

- Selected tier: Tier 2 because this changes repo-local host tooling,
  simulator listeners, interface lifecycle behavior, tests, and durable
  records.
- Owner role: Tooling with QA, Agent Operations, and LCD/browser interface
  lenses.
- Evidence need: required governance docs, read-only reviewer quorum, focused
  lifecycle/gateway/scheduler/LCD tests, scheduler self-test, scaffold
  agent-process audit, `git diff --check`, and dirty-tree boundary review.
- Mutation boundary: `scripts/server_lifecycle.py`,
  `scripts/agent_scheduler.py`,
  `tools/simulators/esp32_gateway_tcp/esp32_gateway_sim.py`,
  `tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py`, focused tests, docs index,
  source index, source ledger, and this task record.
- Gate authority: host-only cleanup for repo-owned local listeners and inert
  interface objects. No live hardware, COM/serial, flash, monitor, RF/XBee,
  wiring, relay/load/mains, external service, commit, or push authority.

## Verified Facts

- Existing dirty PF0530O firmware/LCD/menu/source files were present before
  this cleanup and are outside this task's behavioral intent.
- `scripts/server_lifecycle.py` did not exist before this task.
- The gateway TCP simulator owned a local TCP listener and required manual
  shutdown/server-close handling.
- The scheduler daemon used a user-state Unix socket and PID file, but did not
  expose `daemon restart` or `daemon start --replace-existing`.
- The LCD browser mirror is an inert Python request shim and opens no socket.

## Assumptions

- "All listeners" means repo-owned local host listeners/interfaces only.
- Recorded same-tool metadata plus command-marker/cwd checks are required
  before process termination.
- Unknown, mismatched, corrupt, or unrecorded live listeners must fail closed
  as unowned.
- Stale metadata, stale PID files, and stale Unix socket files may be cleaned
  when no live listener/process is present.

## Unknowns

- Future host tools may need endpoint types beyond TCP and Unix sockets.
- Future Codex scheduler runtime metadata may change; the helper is currently
  stdlib/Linux-oriented for PID command-line and cwd verification.

## Reviewer Quorum

- Coordinator / architecture-risk, weight 5: approved the named Tier 2
  host-only lifecycle cleanup boundary with no P1/P2 blockers.
- Tooling, weight 3: approved with conditions for user-state metadata,
  same-tool PID checks, default non-destructive `daemon ensure`, and no
  unowned listener termination.
- QA, weight 3: approved mutation start and required focused lifecycle,
  scheduler, gateway, LCD, audit, and dirty-tree validation before acceptance.
- LCD/browser interface, weight 2: approved inert mirror close/reopen/context
  behavior with focused lifecycle tests.

Weighted disposition: 13/13 approve, no P1/P2 blockers for the named mutation
boundary. Reviewer output was collected with `wait_agent`, then all four
reviewer agents were closed with `close_agent` before mutation continued.

## Work Completed

- Added `scripts/server_lifecycle.py` with user-state metadata, stale metadata
  cleanup, in-process registration cleanup, same-tool PID verification, and
  fail-closed unowned listener handling.
- Updated the gateway simulator so `serve()` and `start_background_server()`
  prepare fixed ports before binding by default, support `--keep-existing`,
  and expose `close()` plus context-manager cleanup.
- Updated the scheduler with lifecycle metadata, stale socket/PID cleanup,
  `daemon restart`, and `daemon start --replace-existing`; default
  `daemon ensure` remains non-destructive.
- Updated the LCD browser mirror with `close()`, `reopen()`, `closed`, and
  context-manager support. Requests after close return HTTP-style `410` with
  `{"error": "interface_closed"}`.
- Added focused tests for lifecycle metadata, owned process cleanup, unowned
  listener fail-closed behavior, gateway replacement/rebind behavior,
  scheduler restart/replace/stale cleanup, and LCD mirror close/reopen/context
  behavior.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.esp32_gateway_tcp.test_protocol tests.lcd_bbs_menu.test_lcd_bbs_menu tests.scaffold_audits.test_agent_scheduler`
  ran 56 tests.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py self-test`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `git diff --check`.
- PASS: cleanup scan found no lingering `agent_scheduler.py daemon run`,
  `owned_listener.py`, or `esp32_gateway_sim.py` processes after tests.
- DIRTY-TREE REVIEW: this task intentionally added/touched only the lifecycle
  helper, scheduler/gateway/LCD host code, focused tests, docs/source records,
  source index, and docs index. Existing PF0530O firmware/menu/source files and
  task/source records remain present and were not reverted.
- PUBLICATION RECHECK: after the PF0530O audit/record reconciliation,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py` passed in the
  same publication gate. This cleanup task still does not accept or reject the
  PF0530O firmware lane beyond preserving its dirty-tree boundary.

## Authority Limits

This task does not authorize live hardware, COM/serial access, flashing,
monitor, RF/XBee writes, relay/load/mains, wiring mutation, firmware framework
changes, credentials, external services, destructive git, GitHub publication,
release, commit, or push.

## Decision Footer

Decision: `complete` for the host-only lifecycle cleanup. Next gate: separate
PF0530O firmware/menu audit reconciliation if that lane needs full scaffold
verification. Owner: Tooling with QA. Evidence: reviewer quorum, local
code/tests, source ledger, validation commands, and cleanup scan. Approved
mutation boundary: the host lifecycle helper, gateway/scheduler/LCD host code,
focused tests, docs/source/task records. Authority limits remain host-only.
