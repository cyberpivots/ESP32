# ESP-NOW BBS LCD Browser QA Hardening Source Ledger - 2026-05-31

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-BBS-LCD-BROWSER-QA-HARDENING-2026-05-31`
- `SRC-LOCAL-ESPNOW-BBS-LCD-MENU-GRAPHICS-BROWSER-AGENT-2026-05-31`
- `SRC-HITACHI-HD44780U-DDRAM-CGRAM-2026-05-31`
- `SRC-NXP-HD44780-4X20-DDRAM-2026-05-31`
- `SRC-LCDMENU-ROTARY-ENCODER-2026-05-31`

## Purpose

Record the source basis and validation evidence for the Tier 2 host-only LCD
browser mirror QA hardening continuation.

## Verified Facts

- [repo-verified] `bbs_lcd_render.v1` now includes `glyph_bank_name` in
  addition to the eight-slot `glyph_bank` list.
- [repo-verified] `POST /api/lcd/intent` accepts only an `intent` payload field
  and rejects unknown or secret-bearing payload fields.
- [repo-verified] The generated static HTML mirrors cursor row, column, DDRAM
  address, focus, and active glyph-bank name through inert markup/data
  attributes.
- [repo-verified] Focused browser tests cover all four allowed UI intents,
  method closure, malformed JSON, non-object JSON, unknown payload fields,
  secret payload fields, cursor metadata, and glyph-bank metadata.
- [repo-verified] The browser mirror remains a host-only request shim/static
  HTML generator. It opens no socket and adds no active browser network,
  serial, Bluetooth, GPIO, relay, flash, erase, XBee, Wi-Fi, WebSocket, or
  ESP-NOW behavior.

## Assumptions

- Browser mirror behavior remains simulator-only and does not imply firmware
  browser behavior.
- Static HTML metadata is UI corroboration only.
- Rotary intents remain local view-state changes only.
- Future ESP32 HTTP/SoftAP/WebSocket work still requires a separate live,
  network, security, memory, and rollback gate.

## Unknowns

- Physical LCD custom-glyph rendering and glyph-bank swap visibility.
- Encoder direction/select proof after PF0530K.
- Firmware memory budget and network/security policy for any future ESP32
  browser surface.
- Exact LCD backpack electrical behavior, pullup voltage, and rail margin.

## Reviewer Quorum

Read-only Tier 2 reviewers approved the host-only continuation boundary.

- Coordinator/Architecture-risk, weight 5: approved Tier 2 host-only
  continuation and denied Tier 3 expansion.
- QA, weight 3: approved host-only simulator/browser/test continuation.
- Evidence Records, weight 2: approved with a new continuation task/source
  record requirement.

Weighted approval: 10/10. No P1/P2 blockers remained inside the host-only
boundary.

## Mutation Boundary

- `tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py`
- `tools/simulators/lcd_bbs_menu/README.md`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `docs/projects/espnow-bbs/lcd-menu-graphics-browser-agent-plan.md`
- `knowledge-base/source-index.md`
- this source ledger
- `docs/index.md`
- `.agents/TASK_LOG/0117-espnow-bbs-lcd-browser-qa-hardening.md`
- `.agents/handoffs/0086-espnow-bbs-lcd-browser-qa-hardening-to-qa.md`

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
- PASS: changed-file source-ID scan.
- PASS: changed-file Markdown link scan.
- PASS: closed-surface scan reviewed expected closed/no-authority hits.
- PASS: `git diff --check`

## Stop Gates

This source record does not authorize live flash, prepare/flash/complete,
monitor, serial writes, serial-write expansion, XBee/RF, ESP-NOW live runtime,
relay GPIO writes, relay-expander writes, TFT, MicroSD, wiring mutation, load,
mains, erase, firmware ABI changes, bridge ABI changes, coordinator serial ABI
changes, Gate F service-code changes, `mesh_discovery.v1` changes, Win31
transport changes, persistent configuration endpoints, framework changes
outside accepted ADRs, release gating, commit, or push.
