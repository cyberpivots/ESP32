# Task 0110: ESP-NOW BBS LCD/Encoder Field Console

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-30

## Goal

Implement the first host-only LCD/encoder BBS field-console slice: source-backed
design packet, source-index/source-ledger records, host renderer, tests, and
handoff.

## Verified Facts

- The accepted BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- PF0530G passed serial LCD init diagnostics at `0x27`; physical LCD visual
  confirmation remains unproven.
- PF0530F menu acceptance remains blocked after `LCD_INIT_FAILED`.
- Gate F/G/M host-only boundaries, 512-byte bridge lines, 250-byte ESP-NOW
  v1-compatible packet budgeting, and non-executing `control_intent` are
  preserved.

## Assumptions

- `bbs_lcd_state.v1` is a host renderer snapshot schema only.
- Rotary input produces local UI intents only.
- Missing data renders as `?` and closed surfaces render as `CLOSED`.

## Unknowns

- Physical LCD visual state, rail margin, LCD backpack pullup voltage, encoder
  direction, boot-held behavior, and future XBee/ESP-NOW mapping are unknown.
- No live proof is captured by this task.

## Reviewer Quorum

Local read-only role-lens quorum was used before mutation. No subagents were
spawned because explicit delegation was not provided and the available subagent
tool contract requires explicit delegation.

- Coordinator/Architecture-risk, weight 5: approved bounded host-only mutation.
- Communications, weight 3: approved if bridge/radio/XBee lanes stay closed.
- Hardware/Firmware, weight 3: approved if no flash, wiring, monitor, or
  runtime expansion occurs.
- QA, weight 3: approved with focused renderer tests and existing scaffold
  validation.

Weighted approval: 14/14. No P1/P2 blockers.

## Mutation Boundary

- `docs/projects/espnow-bbs/lcd-encoder-field-console-plan.md`
- `tools/simulators/lcd_bbs_menu/`
- `tests/lcd_bbs_menu/`
- `docs/index.md`
- `docs/projects/espnow-bbs/README.md`
- `docs/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/four-relay-xbee-wifi/rotary-encoder-menu-plan.md`
- `tests/README.md`
- `knowledge-base/source-index.md`
- `knowledge-base/source-ledger/2026-05-30-espnow-bbs-lcd-encoder-field-console.md`
- this task record
- `.agents/handoffs/0080-espnow-bbs-lcd-encoder-field-console-to-qa.md`

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- Changed-file source-ID scan.
- Changed-file Markdown link check.
- Closed-surface scan.
- `git diff --check`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py` (10 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page HOME`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py` (32 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (49 tests)
- PASS: changed-file source-ID scan over 7 Markdown files.
- PASS: changed-file Markdown link scan over 10 Markdown files.
- PASS: closed-surface scan reviewed expected closed/no-authority hits.
- PASS: `git diff --check`

## Handoff

Continue with
[../handoffs/0080-espnow-bbs-lcd-encoder-field-console-to-qa.md](../handoffs/0080-espnow-bbs-lcd-encoder-field-console-to-qa.md).

## Closed Surfaces

Live flash, prepare/flash/complete, monitor, serial writes, serial-write
expansion, XBee/RF, ESP-NOW live runtime, relay GPIO writes, relay-expander
writes, TFT, MicroSD, wiring mutation, load, mains, erase, firmware ABI
changes, bridge ABI changes, coordinator serial ABI changes, Gate F service-code
changes, `mesh_discovery.v1` changes, Win31 transport changes, framework
selection, release gating, commit, and push remain closed.
