# Source Ledger: ESP-NOW BBS LCD Pixel Preview Catalog

Date: 2026-06-02

Source ID: `SRC-LOCAL-ESPNOW-BBS-LCD-PIXEL-PREVIEW-CATALOG-2026-06-02`

## Summary

This Tier 2 host-only continuation adds pixel-level preview metadata and a
small candidate ART catalog for the 20x4 HD44780 LCD menu simulator. It keeps
the normal LCD render lines ASCII-safe and does not claim physical LCD
readability.

## Source Coverage

- HD44780 custom-character constraints remain source-backed by
  `SRC-HITACHI-HD44780U-DDRAM-CGRAM-2026-05-31`.
- 20x4 DDRAM row-base planning remains source-backed by
  `SRC-NXP-HD44780-4X20-DDRAM-2026-05-31`.
- Prior host art compiler behavior is recorded by
  `SRC-LOCAL-ESPNOW-BBS-LCD-VISUAL-ART-COMPILER-2026-06-02`.
- PF0530W firmware-visible ART integration and live readiness are recorded by
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-VISUAL-ART-2026-06-02`
  and `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-LIVE-2026-06-02`.

## Verified Facts

- `bbs_lcd_pixel_preview.v1` is derived from `bbs_lcd_art.v1` compiled art and
  emits 32 rows by 100 columns of deterministic `.`/`#` preview data.
- The ART catalog contains five host candidate panels: `bbs_badge`,
  `mesh_radar`, `packet_flow`, `signal_skyline`, and `link_heat`.
- Each catalog panel compiles through the existing 4x20 tile-map compiler and
  remains capped at eight nonblank custom glyph slots.
- The host ART cursor focus now reports `art_panel`, matching the PF0530W
  firmware special-case renderer for ART pages.
- HOME first-viewport labels were shortened in `bbs_lcd_menu.v1.xml` and the
  generated host/firmware LCD menu artifacts were refreshed from that XML.

## Unknowns

- Physical LCD readability, contrast, flicker, and transient CGRAM redraw
  behavior for the new catalog panels remain unverified.
- PF0530W ART-page visual acceptance and ART render telemetry remain pending.
- Exact LCD module/backpack identity, R/W wiring, pullup voltage, and rail
  margin remain unresolved.

## Authority Limits

This record does not authorize live bench work, flash, erase, monitor, serial
writes, XBee/RF writes, ESP-NOW runtime expansion, relay GPIO writes,
relay-expander writes, SoftAP/browser firmware runtime, persistent config,
MicroSD, TFT, wiring, load, mains, release, commit, push, PR creation, or
physical LCD acceptance claims.

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

## Decision

Decision: host/source-build validation passed inside the approved LCD
simulator/tests/docs/records boundary. Publication-gate skill inventory drift
was refreshed and scaffold verification passed. Next gate: QA review of host
evidence, then optional separate Tier 3 physical ART visual proof only if
requested.
