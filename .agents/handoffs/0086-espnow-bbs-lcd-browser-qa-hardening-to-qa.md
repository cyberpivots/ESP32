# Handoff 0086: ESP-NOW BBS LCD Browser QA Hardening To QA

Date: 2026-05-31

Task:
[../TASK_LOG/0117-espnow-bbs-lcd-browser-qa-hardening.md](../TASK_LOG/0117-espnow-bbs-lcd-browser-qa-hardening.md)

## Current State

- Added `glyph_bank_name` to `bbs_lcd_render.v1`.
- Tightened `POST /api/lcd/intent` so the payload accepts only an `intent`
  field and rejects unknown or secret-bearing fields.
- Added inert cursor and active glyph-bank mirror metadata to generated static
  HTML.
- Expanded focused LCD browser tests to cover all four v1 intents, method
  closure, bad JSON, non-object JSON, unknown payload fields, secret payload
  fields, cursor metadata, and glyph-bank metadata.

## QA Focus

1. Confirm every render still has exactly four 20-character ASCII-safe lines.
2. Confirm `glyph_bank_name` matches the selected eight-slot glyph bank and is
   emitted in API output plus static HTML metadata.
3. Confirm `POST /api/lcd/intent` rejects payload fields other than `intent`,
   including secret-bearing keys.
4. Confirm generated static HTML remains inert and includes no active browser
   network, serial, Bluetooth, GPIO, relay, XBee, flash, erase, Wi-Fi,
   WebSocket, or ESP-NOW behavior.
5. Confirm this host-only continuation does not imply firmware browser,
   SoftAP, WebSocket, live browser proof, serial-write, RF, relay, flash,
   monitor, or wiring authority.

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

## Validation Recorded

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

Do not use this slice to authorize live flash, prepare/flash/complete, monitor,
serial writes, serial-write expansion, XBee/RF, ESP-NOW live runtime, relay
GPIO writes, relay-expander writes, TFT, MicroSD, wiring mutation, load, mains,
erase, firmware ABI changes, bridge ABI changes, coordinator serial ABI
changes, Gate F service-code changes, `mesh_discovery.v1` changes, Win31
transport changes, persistent configuration endpoints, framework changes
outside accepted ADRs, release gating, commit, or push.
