# Server And Interface Lifecycle Cleanup Source Ledger - 2026-06-01

## Scope

Tier 2 host-only cleanup that closes repo-owned local server/listener/interface
instances before reopening or starting a replacement, while failing closed for
unrecorded live listeners.

## Source Basis

- `SRC-LOCAL-MULTI-WINDOW-CODEX-SCHEDULER-2026-06-01`
- `SRC-LOCAL-SUBAGENT-LIFECYCLE-CLEANUP-2026-06-01`
- `SRC-LOCAL-ESPNOW-BBS-LCD-MENU-GRAPHICS-BROWSER-AGENT-2026-05-31`
- `SRC-LOCAL-ESPNOW-BBS-LCD-BROWSER-QA-HARDENING-2026-05-31`

## Verified Facts

- `scripts/server_lifecycle.py` stores lifecycle metadata in a user-state
  directory, not in the repository.
- Metadata records schema, tool name, endpoint, host, port, optional Unix socket
  path, PID, command marker, cwd, and start time.
- Replacement cleanup closes in-process registered instances first, removes
  stale metadata/PID/socket records when no live owner exists, and only signals
  a recorded same-tool PID when command marker and cwd match.
- Live unrecorded or mismatched listeners fail closed with
  `listener_in_use_unowned`.
- The gateway simulator now supports managed close/context cleanup and
  `keep_existing` behavior for preserving occupied-port failures.
- The scheduler now supports `daemon restart` and
  `daemon start --replace-existing`; default `daemon ensure` remains
  non-destructive.
- The LCD browser mirror remains an inert no-socket request shim and now has
  close/reopen/context lifecycle behavior.

## Reviewer Quorum

- Coordinator / architecture-risk, weight 5: approved.
- Tooling, weight 3: approved with same-tool/unowned-listener conditions.
- QA, weight 3: approved mutation start and required focused tests/audits.
- LCD/browser interface, weight 2: approved inert close/reopen behavior.

Weighted disposition: 13/13 approve, no P1/P2 blockers for the host-only
mutation boundary. Reviewer agents were collected and closed before mutation.

## Outcome

- Added `scripts/server_lifecycle.py`.
- Updated `scripts/agent_scheduler.py`.
- Updated `tools/simulators/esp32_gateway_tcp/esp32_gateway_sim.py`.
- Updated `tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py`.
- Added focused test coverage in `tests/scaffold_audits/test_agent_scheduler.py`,
  `tests/esp32_gateway_tcp/test_protocol.py`, and
  `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`.
- Added task/source/docs records for this cleanup.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.esp32_gateway_tcp.test_protocol tests.lcd_bbs_menu.test_lcd_bbs_menu tests.scaffold_audits.test_agent_scheduler`
  ran 56 tests.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py self-test`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `git diff --check`.
- PASS: process cleanup scan found no lingering scheduler daemon, owned test
  listener, or gateway simulator process from this task.
- PUBLICATION RECHECK: after PF0530O audit/record reconciliation,
  `scripts/verify_scaffold.py` passed in the same publication gate. This source
  record still does not accept or reject the PF0530O firmware lane.

## Authority Limits

This record does not authorize live hardware, COM/serial access, flashing,
monitor, RF/XBee writes, ESP-NOW live runtime, relay GPIO writes,
relay-expander writes, wiring mutation, DMM/current measurement, load, mains,
erase, persistent configuration, credentials, external services, GitHub
publication, release, commit, or push.
