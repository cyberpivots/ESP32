# Task 0146: ESP-NOW BBS LCD Pixel Preview Catalog

Status: implemented and host/source-build validated; one unrelated scaffold verify issue recorded

Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Implement the approved host-first graphical improvement plan for the rotary
encoder LCD menu system by adding deterministic pixel preview metadata, a
small ART catalog, and first-viewport label polish without opening live
hardware or firmware runtime surfaces.

## Routing Packet

- Verified facts: PF0530W is the current firmware-visible LCD ART image,
  PF0530V is the accepted PCNT encoder baseline, `bbs_lcd_render.v2` remains
  the host render output, and PF0530W physical ART-page visual acceptance is
  still pending. Source IDs:
  `SRC-LOCAL-ESPNOW-BBS-LCD-VISUAL-ART-COMPILER-2026-06-02`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-VISUAL-ART-2026-06-02`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-LIVE-2026-06-02`.
- Assumptions: the implementation should stay host-first; PF0530X remains
  unopened until a separate source/build gate updates records, tests, audits,
  and no-flash build evidence together.
- Unknowns: physical LCD readability, contrast, flicker, transient CGRAM redraw
  behavior, exact LCD backpack behavior, and ART navigation telemetry.
- Selected tier: Tier 2.
- Owner role: LCD Menu Developer with Firmware, Tooling, QA, Evidence Records,
  and Agent-Ops lenses.
- Evidence need: read-only reviewer quorum, current source/docs/tests,
  generated artifact parity, focused LCD tests, source/docs/records audits,
  and closed-surface scan.
- Mutation boundary: `tools/simulators/lcd_bbs_menu/`, `tests/lcd_bbs_menu/`,
  generated LCD menu artifacts from XML, LCD project docs, source index/source
  ledger, this task record, docs index, and QA handoff.
- Gate authority: no Tier 3 authority; no flash, erase, monitor, serial write,
  RF/XBee, ESP-NOW runtime, relay, wiring, load, mains, release, commit, push,
  PR, or deploy.
- Validation plan: generator check, focused LCD tests, LCD unittest discovery,
  firmware boundary tests, source/docs/records/scaffold audits, and
  `git diff --check`.
- Trust boundary: host and source/build evidence only; no physical LCD or live
  device claim.

## Reviewer Quorum

- Coordinator/architecture-risk local packet, weight 5: approved host-first
  implementation with live surfaces closed.
- LCD menu UX reviewer, weight 3: approved with P1 claim boundary and P2
  acceptance checks for ART focus parity, label clipping, catalog metadata, and
  inert browser behavior.
- QA validation reviewer, weight 3: approved with dirty-tree attribution and
  validation requirements.
- Firmware/device reviewer, weight 3: approved PF0530W source/build boundary;
  blocked PF0530X until a separate source/build gate.
- Source research reviewer, weight 2: approved existing source coverage with
  physical-display claims kept unresolved.

Weighted disposition: 16/16 approve for host-only/source-boundary mutation.
No P1/P2 blockers remain for this scoped implementation. Read-only reviewers
were waited on and closed after output capture.

## Implementation Summary

- Added `bbs_lcd_pixel_preview.v1` metadata: each compiled LCD art panel now
  exposes 32 deterministic 100-column `.`/`#` rows derived from `cell_slots`
  and 5x8 glyph row bytes.
- Added a host-only ART catalog with five candidate panels:
  `bbs_badge`, `mesh_radar`, `packet_flow`, `signal_skyline`, and `link_heat`.
- Kept every catalog panel inside a single eight-slot HD44780 custom glyph
  bank and preserved fail-closed overflow behavior.
- Aligned host ART cursor/focus metadata with firmware by reporting
  `art_panel` focus at row 0, column 0, DDRAM `0x00`.
- Shortened HOME first-viewport labels and regenerated the generated host and
  firmware LCD menu artifacts from XML.
- Kept the browser mirror static and inert while exposing ART pixel preview
  metadata through data attributes and JSON.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (33 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'`
  (33 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.scaffold_audits.test_firmware_pcnt_accumulator tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (43 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
  (97 tests).
- PASS: no-flash ESP-IDF build to
  `/tmp/esp32-pf0530w-lcd-pixel-preview-build`.
- PASS: `git diff --check`.
- PASS after publication-gate skill inventory refresh:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- PASS after publication-gate skill inventory refresh:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.

No-flash build artifact hashes:

- `four_relay_xbee_wifi.bin`:
  `5b4afdccc6b363a6cc08e19a5b8c9d85b3aac2b0e5224be78699f34a7e837b0f`.
- `four_relay_xbee_wifi.elf`:
  `8d38d58b5ed766e954846a0fc0623d23c5174101e55cd169b4c31427063d0614`.
- `bootloader.bin`:
  `4fa4cd077b7639c2ab63c0c892a6e444bf93892c8e92a383ba54683355d55fe5`.
- `partition-table.bin`:
  `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820`.

## Closed Surfaces

No live bench, flash, erase, monitor, serial command writes, XBee/RF,
ESP-NOW runtime expansion, relay GPIO writes, relay-expander writes,
SoftAP/browser firmware runtime, persistent configuration endpoints, MicroSD,
TFT, wiring, DMM/current/load/mains work, release, commit, push, PR, or deploy
is authorized by this task.

## Handoff

Handoff: [../handoffs/0107-espnow-bbs-lcd-pixel-preview-catalog-to-qa.md](../handoffs/0107-espnow-bbs-lcd-pixel-preview-catalog-to-qa.md)

## Decision

Decision: implementation accepted within the approved Tier 2 host-only LCD
visual tooling/source-build boundary. Next gate: QA review; physical ART
acceptance remains a separate Tier 3 gate.
