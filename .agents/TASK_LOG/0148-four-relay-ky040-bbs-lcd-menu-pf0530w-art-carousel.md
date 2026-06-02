# Task 0148: Four Relay KY-040 BBS LCD Menu PF0530W ART Carousel

Status: implemented and source/build validated; physical ART acceptance pending

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-ART-CAROUSEL-2026-06-02`

## Goal

Continue the graphical improvement of the rotary-controlled 20x4 LCD menu by
turning the existing host ART catalog into a source/build-validated ART
carousel on the host simulator and PF0530W firmware renderer, without
returning to encoder diagnostics or opening live hardware surfaces.

## Routing Packet

- Verified facts: the user reports the encoder works; PF0530W is the current
  firmware-visible LCD visual-art identity; Task 0146 added five host ART
  catalog panels; Task 0147 live-flashed the Task 0146 artifact under PF0530W;
  and physical ART visual acceptance remains open.
- Assumptions: the requested continuation is source/host/firmware-display
  implementation, not further encoder proof and not a fresh live flash.
- Unknowns: physical LCD readability, contrast, flicker, transient CGRAM redraw
  behavior, and live ART-page telemetry for the carousel remain unverified.
- Selected tier: Tier 2.
- Owner role: LCD Menu Developer with Firmware, QA, LCD UX, and Evidence
  Records lenses.
- Evidence need: read-only reviewer quorum, host simulator tests, firmware
  boundary tests, generator freshness, firmware/source/docs/records audits,
  and no-flash ESP-IDF build proof.
- Mutation boundary: LCD host simulator, LCD tests, firmware display-only ART
  render/cache behavior, firmware and simulator README text, scaffold audit
  markers, source index, source ledger, docs index, task record, and QA
  handoff. No live device access or generated XML/header change was required.
- Validation plan: focused LCD and firmware-boundary tests, LCD generator
  `--check`, firmware audit, source/docs/records/scaffold audits, no-flash
  ESP-IDF v6.0.1 build, `git diff --check`, and Git status.
- Gate authority: source/build only. No Tier 3 flash, monitor, serial write,
  RF/XBee, ESP-NOW runtime, relay, wiring, load, mains, release, commit, push,
  PR, or deploy authority was opened by this task.
- Trust boundary: host/source/build evidence only; no physical LCD or live
  hardware behavior claim.

## Reviewer Quorum

- LCD menu UX reviewer, weight 3: approved source/host improvement and
  recommended using the existing five-panel ART catalog as a carousel. No
  P1/P2 blockers for this source/host boundary.
- Firmware/device reviewer, weight 3: approved host/source/build-only work and
  blocked live continuation without a separate gate. P2 required a fresh
  no-flash build before accepting firmware-visible mutation.
- QA validation reviewer, weight 3: approved source/host work with P2 no-flash
  build, dirty-tree preservation, and no physical ART acceptance claim.
- Coordinator/architecture-risk role, weight 5: accepted the source/build
  mutation boundary after reviewer output, with live surfaces closed.

Weighted disposition: 14/14 approve for the named source/build boundary after
the no-flash build passed. No P1/P2 blockers remain for Task 0148. Reviewer
outputs were captured and reviewer agents were closed before implementation
continued.

## Implementation Summary

- Added `MenuViewState.art_index` and ART-page rotary behavior in the host
  simulator. Rotating on `ART` cycles the five catalog panels while preserving
  selected menu item focus and back-stack behavior.
- Exposed host viewport metadata for the active panel:
  `art_active_name`, `art_active_index`, `art_panel_count`, and
  `art_catalog.active`.
- Updated browser-mirror intent coverage so `rotate_right` from `ART` advances
  to `mesh_radar` and reports `last_intent=art_next`.
- Replaced the firmware fixed ART slot map with five `fr_bbs_art_panels`
  variants matching the host catalog names.
- Added firmware `art_index` and `art_panel_index` tracking so ART-page
  rotation selects the next/previous panel without cycling menu items.
- Updated the LCD glyph-bank loader so the ART bank cache includes panel
  identity and reloads CGRAM rows when the selected ART panel changes.
- Added `art=%u` render telemetry to `BBS_LCD_RENDER` while preserving the
  existing proof-line prefix and closed-surface policy.
- Updated scaffold audit markers and docs from fixed ART tile-map language to
  source/build ART-carousel language.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.lcd_bbs_menu.test_lcd_bbs_menu tests.scaffold_audits.test_firmware_encoder_pullup_boundary`
  (38 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (34 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.scaffold_audits.test_firmware_pcnt_accumulator tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (44 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
  (97 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: no-flash ESP-IDF v6.0.1 build to
  `/tmp/esp32-pf0530w-art-carousel-build`.
- PASS: `git diff --check`.

No-flash build artifact hashes:

- `bootloader.bin`:
  `b424bf752943976e040194985f92bcf3258b5ce80bdc01285eda10cad878ed38`.
- `partition-table.bin`:
  `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820`.
- `four_relay_xbee_wifi.bin`:
  `fb5c15e0cc9ca799cf76e39ef1b4483b7c26249ea2c81ab950ee465d7356c499`.
- `four_relay_xbee_wifi.elf`:
  `418a764cbae153a4d0f8349e2dcb80df117641657d5ec4cf51a535ac0629daa4`.

## Closed Surfaces

No live bench, flash, erase, monitor, serial command writes, XBee/RF,
ESP-NOW runtime expansion, relay GPIO writes, relay-expander writes, SoftAP or
browser firmware runtime, persistent configuration endpoints, MicroSD, TFT,
wiring, DMM/current/load/mains work, release, commit, push, PR, or deploy is
authorized by this task.

## Handoff

Handoff:
[../handoffs/0109-four-relay-ky040-bbs-lcd-menu-pf0530w-art-carousel-to-qa.md](../handoffs/0109-four-relay-ky040-bbs-lcd-menu-pf0530w-art-carousel-to-qa.md)

## Decision Footer

Decision: `pf0530w_art_carousel_source_build_passed_physical_art_pending`.
Next gate: QA review of Task 0148 source/build evidence, then an optional
separate Tier 3 live flash/visual proof only if requested. Owner: LCD Menu
Developer with Firmware, QA, LCD UX, and Evidence Records. Evidence: read-only
reviewer quorum, focused tests, no-flash ESP-IDF build, source/docs/records
updates, and source ledger.
