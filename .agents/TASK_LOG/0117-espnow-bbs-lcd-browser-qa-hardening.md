# Task 0117: ESP-NOW BBS LCD Browser QA Hardening

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-31

## Goal

Continue the documented LCD menu graphics/browser plan with a host-only QA
hardening slice for the inert browser mirror, without opening firmware,
network, live bench, serial, RF, relay, wiring, release, commit, or push
surfaces.

## Verified Facts

- Task 0115 is already implemented and validated for `bbs_lcd_render.v1`,
  cursor/DDRAM metadata, dirty metadata, glyph banks, widgets, an inert browser
  mirror, and recallable LCD menu skill/agent records.
- The browser mirror is a Python request shim and static HTML generator; it
  opens no socket and starts no server.
- PF0530K remains flashed/verify-flashed for user testing but is not accepted
  as interactive because prior live evidence captured zero `ENC_RAW`,
  `ENC_EV`, `BBS_MENU_STEP`, and `BBS_MENU_SELECT`.
- Focused LCD tests passed before this mutation at 16 tests.

## Assumptions

- The user's request to continue execution means continue the host-only plan
  unless a separate Tier 3 gate is explicitly opened.
- The user's bench safe-state statement is context only for this slice and does
  not open live flash, monitor, serial/RF, relay, wiring, or release gates.
- Browser mirror changes are local simulator/schema/test changes only.

## Unknowns

- Physical LCD custom-glyph behavior.
- Encoder direction/select proof after PF0530K.
- Target firmware memory budget and network/security policy for any future
  ESP32 browser mirror.
- Exact LCD backpack electrical behavior, pullup voltage, and rail margin.

## Reviewer Quorum

Read-only Tier 2 reviewers approved the host-only continuation boundary before
mutation.

- Coordinator/Architecture-risk, weight 5: approved Tier 2 host-only
  continuation and denied Tier 3 expansion.
- QA, weight 3: approved host-only simulator/browser/test continuation.
- Evidence Records, weight 2: approved with a new continuation task/source
  record requirement.

Weighted approval: 10/10. No P1/P2 blockers remained for the named host-only
mutation boundary.

## Mutation Boundary

- `tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py`
- `tools/simulators/lcd_bbs_menu/README.md`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `docs/projects/espnow-bbs/lcd-menu-graphics-browser-agent-plan.md`
- `knowledge-base/source-index.md`
- `knowledge-base/source-ledger/2026-05-31-espnow-bbs-lcd-browser-qa-hardening.md`
- `docs/index.md`
- this task record
- `.agents/handoffs/0086-espnow-bbs-lcd-browser-qa-hardening-to-qa.md`

## Implementation

- Added `glyph_bank_name` to the `bbs_lcd_render.v1` output dictionary.
- Added strict intent payload validation so `POST /api/lcd/intent` accepts only
  the `intent` field and rejects unknown or secret-bearing payload fields.
- Added inert cursor and glyph-bank mirror metadata to generated static HTML.
- Expanded browser tests for method closure, all allowed intents, malformed
  JSON, non-object JSON, unknown payload fields, secret payload fields, cursor
  metadata, and glyph-bank metadata.

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- Changed-file source-ID scan.
- Changed-file Markdown link scan.
- Closed-surface scan.
- `git diff --check`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py` (18 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'` (18 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py` (32 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_data.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (49 tests)
- PASS: `git diff --check`

## Handoff

Continue with
[../handoffs/0086-espnow-bbs-lcd-browser-qa-hardening-to-qa.md](../handoffs/0086-espnow-bbs-lcd-browser-qa-hardening-to-qa.md).

## Closed Surfaces

Live flash, prepare/flash/complete, monitor, serial writes,
serial-write expansion, XBee/RF, ESP-NOW live runtime, relay GPIO writes,
relay-expander writes, TFT, MicroSD, wiring mutation, load, mains, erase,
firmware ABI changes, bridge ABI changes, coordinator serial ABI changes, Gate
F service-code changes, `mesh_discovery.v1` changes, Win31 transport changes,
persistent configuration endpoints, framework changes outside accepted ADRs,
release gating, commit, and push remain closed.
