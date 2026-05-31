# Handoff 0085: ESP-NOW BBS LCD Menu Graphics, Browser Mirror, And Agent To QA

Date: 2026-05-31

Task:
[../TASK_LOG/0115-espnow-bbs-lcd-menu-graphics-browser-agent.md](../TASK_LOG/0115-espnow-bbs-lcd-menu-graphics-browser-agent.md)

## Current State

- Added `bbs_lcd_render.v1` output metadata while keeping `bbs_lcd_state.v1`
  as the input schema.
- Added software cursor/DDRAM metadata, dirty-row/cell metadata, named glyph
  banks, widget helpers, and browser-mirror host tests.
- Added an inert browser mirror request shim and static HTML generator; no
  socket or server is opened.
- Added a repo-local `lcd-menu-operations` skill and read-only
  `lcd-menu-ux-reviewer` agent profile.
- Added source-index rows, a new source ledger, docs cross-links, and this
  handoff.

## QA Focus

1. Confirm every render still has exactly four lines of exactly 20 ASCII-safe
   cells.
2. Confirm all named glyph banks are capped at eight slots and row bytes stay
   in `0x00..0x1F`.
3. Confirm browser mirror behavior is host-only and rejects unknown intents,
   unknown routes, active network/browser APIs, and secret-bearing snapshots.
4. Confirm `bbs_lcd_render.v1` is an output schema only and does not imply
   bridge, firmware, coordinator serial, radio, or Win31 transport changes.
5. Confirm the new skill/agent remain advisory and preserve operator
   sovereignty plus closed live surfaces.

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

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- PASS: `.codex/config.toml` and `.codex/agents/*.toml` parse check.
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
