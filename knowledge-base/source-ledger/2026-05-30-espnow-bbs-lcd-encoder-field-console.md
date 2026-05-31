# ESP-NOW BBS LCD/Encoder Field Console Source Ledger - 2026-05-30

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-BBS-LCD-ENCODER-FIELD-CONSOLE-2026-05-30`
- `SRC-HITACHI-HD44780U-CGRAM-2026-05-30`
- `SRC-RFC8949-CBOR-2026-05-30`
- `SRC-RFC1055-SLIP-2026-05-30`
- `SRC-RFC1662-PPP-HDLC-2026-05-30`
- `SRC-CHESHIRE-BAKER-COBS-2026-05-30`

## Purpose

Record the source basis for a host-only LCD/encoder BBS field-console design
packet and renderer.

## Verified Facts

- [repo-verified] The field console slice is host-only docs, source-index,
  source-ledger, task/handoff, renderer, and tests.
- [repo-verified] The accepted BBS path, Gate F/G/M host-only boundaries,
  PF0530F/PF0530G lineage, and XBee closed-surface boundaries are preserved.
- [source-verified] HD44780 CGRAM planning is limited to eight 5x8 custom
  character types.
- [source-verified] RFC 8949, RFC 1055, RFC 1662, and Cheshire/Baker COBS are
  references for future payload/framing comparison only.
- [repo-verified] The renderer rejects secret-bearing fields, outputs exactly
  four 20-character lines, and emits an eight-slot glyph bank.

## Assumptions

- First firmware use, if later authorized, will be static/simulated or
  simulator-fed and will not transmit radio, XBee, serial, or relay commands.
- `bbs_lcd_state.v1` is a local renderer snapshot schema, not a bridge or
  firmware ABI.

## Unknowns

- No physical LCD visual evidence, rail-margin evidence, encoder direction
  proof, boot-held behavior, XBee mapping proof, or ESP-NOW live runtime proof
  is captured by this task.

## Reviewer Quorum

Local read-only role-lens quorum ran before mutation. No subagents were spawned
because the available subagent tool requires explicit delegation and the
provided implementation plan selected local lenses.

- Coordinator/Architecture-risk, weight 5: approved host-only mutation.
- Communications, weight 3: approved while bridge/radio/XBee surfaces stay
  closed and framing records remain planning references.
- Hardware/Firmware, weight 3: approved while there is no flash, monitor,
  wiring, firmware runtime, or framework expansion.
- QA, weight 3: approved with renderer tests, protocol tests, scaffold audits,
  source/link checks, closed-surface scan, and `git diff --check`.

Weighted approval: 14/14. No P1/P2 blockers remain for the named boundary.

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

## Stop Gates

This source record does not authorize live flash, monitor, serial writes,
serial-write expansion, XBee/RF, ESP-NOW live runtime, relay GPIO writes,
relay-expander writes, TFT, MicroSD, wiring mutation, load, mains, erase,
firmware ABI changes, bridge ABI changes, coordinator serial ABI changes,
Win31 transport changes, framework selection, commit, or push.
