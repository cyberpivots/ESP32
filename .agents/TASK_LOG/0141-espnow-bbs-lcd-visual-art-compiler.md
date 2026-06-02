# Task 0141: ESP-NOW BBS LCD Visual Art Compiler

Status: implemented and validated; host-only boundary accepted

Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Implement the approved 4x20 LCD visual improvement plan as a host-only
`bbs_lcd_art.v1` compiler for deterministic image-like LCD panels while
preserving the existing `bbs_lcd_state.v1` and `bbs_lcd_render.v2` boundaries.

## Routing Packet

- Verified facts: current LCD host renderer is fixed at four 20-character
  ASCII-safe lines, emits `bbs_lcd_render.v2`, and caps custom glyph banks at
  eight 5x8 HD44780 glyphs. Source IDs:
  `SRC-LOCAL-ESPNOW-BBS-LCD-MENU-GRAPHICS-BROWSER-AGENT-2026-05-31`,
  `SRC-HITACHI-HD44780U-DDRAM-CGRAM-2026-05-31`.
- Assumptions: this task is host-only and framework-neutral; no physical LCD
  readability or flicker claim is made for new art.
- Unknowns: physical readability, real CGRAM redraw behavior, and exact LCD
  backpack behavior for new art panels.
- Selected tier: Tier 2.
- Owner role: LCD menu UX/tooling with QA and Evidence Records lenses.
- Evidence need: read-only reviewer quorum, source-backed constraints,
  focused compiler tests, docs/source audits, closed-surface scan, and durable
  records.
- Mutation boundary: LCD simulator code/README, LCD tests, LCD project plan,
  source index/ledger, this task record, and docs index.
- Validation plan: focused LCD tests, LCD unittest discovery, source/docs/
  agent audits, scaffold verify, scaffold audit unittest suite, closed-surface
  scan, and `git diff --check`.

## Reviewer Quorum

- Coordinator/process/architecture-risk reviewer, weight 5: approved with no
  P1/P2 blockers.
- LCD menu UX reviewer, weight 3: approved with conditions to keep LCD `lines`
  ASCII-safe and expose custom slot data as metadata.
- QA validation reviewer, weight 3: approved with required bitmap mapping,
  dedupe, invalid-input, and overflow tests.
- Evidence record auditor, weight 2: approved with source/task record
  requirements.

Weighted disposition: 13/13 approve. No P1/P2 blockers remained before
mutation. Lifecycle state listing was not available in the tool surface;
spawned reviewers were waited on and closed after output capture.

## Implementation Summary

- Added `bbs_lcd_art.v1` host-only metadata for compiled LCD art panels.
- Added PBM `P1` parsing for exact 100x32 one-bit fixtures and direct 4x20
  tile-map compilation.
- Mapped each 5x8 tile to HD44780 row bytes with leftmost pixel in bit 4.
- Reused exact duplicate nonblank tiles, treated blank tiles as no-slot cells,
  and failed closed when more than eight unique nonblank tiles are required.
- Preserved ASCII-safe `bbs_lcd_render.v2` `lines`; custom glyph references
  live in `preview_lines`, `cell_slots`, and compiled glyph-bank metadata.
- Added focused tests for dedupe, PBM mapping, invalid inputs, and overflow.

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

## Closed Surfaces

No live bench, prepare/flash/complete, monitor, serial writes, XBee/RF,
ESP-NOW live runtime, relay GPIO writes, relay-expander writes, TFT, MicroSD,
wiring mutation, load, mains, erase, firmware header generation, firmware ABI
changes, coordinator serial ABI changes, bridge ABI changes, Win31 transport
changes, persistent configuration endpoints, framework selection, release,
commit, or push is authorized by this task.

## Decision Footer

Decision: ready_for_mutation. Next gate: optional future Tier 3 physical LCD
visual proof only if real-device readability is requested. Owner: LCD menu
UX/tooling with QA and Evidence Records. Evidence: reviewer quorum passed and
host validation passed. Approved mutation boundary: host-only LCD simulator/
tests/docs/records. Authority limits: no live hardware or firmware/runtime
mutation.
