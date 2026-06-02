# Source Ledger: ESP-NOW BBS LCD Visual Art Compiler

Date: 2026-06-02

## Source IDs

- `SRC-HITACHI-HD44780U-DDRAM-CGRAM-2026-05-31`
- `SRC-NXP-HD44780-4X20-DDRAM-2026-05-31`
- `SRC-LUMA-LCD-HD44780-2026-05-31`
- `SRC-LOCAL-ESPNOW-BBS-LCD-ENCODER-FIELD-CONSOLE-2026-05-30`
- `SRC-LOCAL-ESPNOW-BBS-LCD-MENU-GRAPHICS-BROWSER-AGENT-2026-05-31`
- `SRC-LOCAL-ESPNOW-BBS-LCD-BROWSER-QA-HARDENING-2026-05-31`

## Purpose

Record the Tier 2 host-only implementation of `bbs_lcd_art.v1`, a visual art
metadata compiler for the 20x4 ESP-NOW BBS LCD simulator lane.

## Verified Facts

- HD44780 CGRAM planning remains limited to eight 5x8 custom-character types.
  Source ID: `SRC-HITACHI-HD44780U-DDRAM-CGRAM-2026-05-31`.
- The host LCD model uses four rows, 20 columns, and 20x4 DDRAM row bases
  `0x00`, `0x40`, `0x14`, and `0x54`. Source ID:
  `SRC-NXP-HD44780-4X20-DDRAM-2026-05-31`.
- Luma.LCD remains a design reference for reusing and redrawing HD44780 custom
  characters, not a dependency. Source ID: `SRC-LUMA-LCD-HD44780-2026-05-31`.
- The local host renderer keeps `bbs_lcd_state.v1` as input and
  `bbs_lcd_render.v2` as render output. Source IDs:
  `SRC-LOCAL-ESPNOW-BBS-LCD-ENCODER-FIELD-CONSOLE-2026-05-30`,
  `SRC-LOCAL-ESPNOW-BBS-LCD-MENU-GRAPHICS-BROWSER-AGENT-2026-05-31`.
- This task adds `bbs_lcd_art.v1` metadata for deterministic 100x32 ASCII PBM
  `P1` fixtures and direct 4x20 tile maps, exact nonblank tile dedupe, stable
  custom-glyph slot assignment, ASCII-safe preview lines, and fail-closed
  overflow above eight unique nonblank glyphs.

## Assumptions

- `bbs_lcd_art.v1` is a host-only planning and test surface.
- Compiled art metadata can guide a future firmware/live design, but does not
  change any firmware ABI or serial/bridge ABI.
- Blank 5x8 tiles consume no CGRAM slot; repeated nonblank tiles reuse the
  same slot.

## Unknowns

- Physical readability of new art panels on the real LCD is unproven.
- Flicker or transient wrong-glyph behavior during any future real CGRAM
  redraw is unproven.
- Exact LCD module/backpack timing and electrical behavior are outside this
  host-only record.

## Reviewer Quorum

- Coordinator/process/architecture-risk reviewer, weight 5: approved
  host-only mutation with no P1/P2 blockers.
- LCD menu UX reviewer, weight 3: approved with conditions to keep `lines`
  ASCII-safe and expose slot data as metadata.
- QA validation reviewer, weight 3: approved with required bitmap mapping,
  dedupe, and overflow tests.
- Evidence record auditor, weight 2: approved record mutation with source
  boundary requirements.

Weighted disposition: 13/13 approve. No P1/P2 blockers remained before
mutation.

## Mutation Boundary

- `tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py`
- `tools/simulators/lcd_bbs_menu/README.md`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `docs/projects/espnow-bbs/lcd-menu-graphics-browser-agent-plan.md`
- `knowledge-base/source-index.md`
- `knowledge-base/source-ledger/2026-06-02-espnow-bbs-lcd-visual-art-compiler.md`
- `.agents/TASK_LOG/0141-espnow-bbs-lcd-visual-art-compiler.md`
- `docs/index.md`

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- Closed-surface scan.
- `git diff --check`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
  (29 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'`
  (29 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
  (32 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
  (85 tests).
- PASS: closed-surface scan found expected stop-gate wording, negative-test
  strings, and preexisting source-index references only.
- PASS: `git diff --check`.

## Stop Gates

Stop before live bench, prepare/flash/complete, monitor, serial writes,
serial-write expansion, XBee/RF, ESP-NOW live runtime, relay GPIO writes,
relay-expander writes, TFT, MicroSD, wiring mutation, load, mains, erase,
firmware header generation, firmware ABI changes, coordinator serial ABI
changes, bridge ABI changes, Win31 transport changes, persistent configuration
endpoints, framework changes outside accepted ADRs, release gating, commit, or
push.
