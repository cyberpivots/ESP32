# Four Relay KY-040 BBS LCD Menu PF0530W ART Carousel Ledger

Date: 2026-06-02

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-ART-CAROUSEL-2026-06-02`

## Scope

Tier 2 source/build continuation that makes the existing five-panel ART catalog
selectable by rotary movement on the host ART page and in the PF0530W firmware
ART renderer. The work preserves the PF0530W firmware identity and does not
open live flash, monitor, serial-write, RF/XBee, relay, wiring, load, or mains
surfaces.

## Source Coverage

- HD44780 custom-character constraints remain source-backed by
  `SRC-HITACHI-HD44780U-DDRAM-CGRAM-2026-05-31`.
- 20x4 DDRAM row-base planning remains source-backed by
  `SRC-NXP-HD44780-4X20-DDRAM-2026-05-31`.
- Host ART compilation and pixel-preview catalog behavior are recorded by
  `SRC-LOCAL-ESPNOW-BBS-LCD-VISUAL-ART-COMPILER-2026-06-02` and
  `SRC-LOCAL-ESPNOW-BBS-LCD-PIXEL-PREVIEW-CATALOG-2026-06-02`.
- PF0530W firmware-visible ART integration and prior live readiness are
  recorded by
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-VISUAL-ART-2026-06-02`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-LIVE-2026-06-02`, and
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-PIXEL-PREVIEW-LIVE-2026-06-02`.

## Verified Facts

- The user directed this continuation to stop revisiting encoder concerns; the
  encoder is treated as working for this source/build task.
- The host ART page now preserves selected menu item focus while rotary events
  cycle the five catalog panels.
- Host render metadata includes `art_active_name`, `art_active_index`,
  `art_panel_count`, `art_catalog.active`, and normalized `view.art_index`.
- Browser mirror intent handling exposes ART rotation as local inert state
  with `last_intent=art_next` or `last_intent=art_previous`.
- Firmware source now defines five `fr_bbs_art_panels` under the existing
  PF0530W identity and keeps `FR_BBS_GLYPH_BANK_COUNT 7u`.
- Firmware ART-page rotation changes `menu->art_index`, reports `ART NEXT` or
  `ART PREV`, and does not cycle the page's selected menu item.
- Firmware LCD glyph-bank cache validation now includes `art_panel_index` when
  the loaded bank is `FR_BBS_ART_GLYPH_BANK_INDEX`, forcing CGRAM reloads when
  the active ART panel changes.
- `BBS_LCD_RENDER` keeps its existing prefix and now reports `art=%u` for
  source/build telemetry.
- GPIO13/GPIO14/GPIO32 remain input-only, GPIO21/GPIO22 remain display-only,
  and `FR_DIAG_XBEE_BRIDGE_CLOSED 1` remains unchanged.

## Unknowns

- Physical LCD readability, contrast, flicker, and transient CGRAM redraw
  behavior for the carousel remain unverified.
- Live ART-page telemetry for the carousel remains unverified until a separate
  Tier 3 gate flashes and monitors this source.
- Exact LCD module/backpack identity, R/W wiring, pullup voltage, and rail
  margin remain unresolved by this source/build task.

## Authority Limits

This record does not authorize live bench work, flash, erase, monitor, serial
writes, XBee/RF writes, ESP-NOW runtime expansion, relay GPIO writes,
relay-expander writes, SoftAP/browser firmware runtime, persistent config,
MicroSD, TFT, wiring, DMM/current/load/mains work, release, commit, push, PR
creation, deploy, or physical LCD acceptance claims.

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

## Decision

Decision: source/build implementation is accepted for QA review inside the
Task 0148 Tier 2 boundary. Physical ART acceptance and any live flash remain
separate Tier 3 gates.
