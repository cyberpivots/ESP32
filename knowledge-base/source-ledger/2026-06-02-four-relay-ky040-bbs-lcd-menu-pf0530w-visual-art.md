# Source Ledger: Four Relay KY-040 BBS LCD Menu PF0530W Visual Art

Date: 2026-06-02

## Source IDs

- `SRC-HITACHI-HD44780U-DDRAM-CGRAM-2026-05-31`
- `SRC-NXP-HD44780-4X20-DDRAM-2026-05-31`
- `SRC-LOCAL-ESPNOW-BBS-LCD-VISUAL-ART-COMPILER-2026-06-02`
- `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-PCNT-SOURCE-BUILD-2026-06-02`
- `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-LIVE-2026-06-02`
- `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-USER-ACCEPTANCE-2026-06-02`
- `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-VISUAL-ART-2026-06-02`
- `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-LIVE-2026-06-02`

## Purpose

Record the bounded source/build integration that makes the LCD visual-art plan
firmware-visible as `PF0530W`; COM6 flashing is now recorded separately under
the PF0530W live source ledger, while physical visual acceptance remains a
separate gate.

## Verified Facts

- HD44780 CGRAM remains limited to eight 5x8 custom-character slots per active
  bank. Source ID: `SRC-HITACHI-HD44780U-DDRAM-CGRAM-2026-05-31`.
- The local LCD menu uses a four-row, 20-column display model. Source ID:
  `SRC-NXP-HD44780-4X20-DDRAM-2026-05-31`.
- Task 0141 added a host-only art compiler and explicitly did not authorize
  firmware generation or live flash. Source ID:
  `SRC-LOCAL-ESPNOW-BBS-LCD-VISUAL-ART-COMPILER-2026-06-02`.
- PF0530V is the accepted PCNT encoder lineage baseline with prior COM6
  write/verify/readiness proof and user functional acceptance. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-PCNT-SOURCE-BUILD-2026-06-02`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-LIVE-2026-06-02`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-USER-ACCEPTANCE-2026-06-02`.
- PF0530W adds a firmware-visible `ART` page, seventh `art_panel` glyph bank,
  and a fixed 4x20 tile map using three nonblank custom glyph shapes from the
  host art compiler sample.
- PF0530W preserves GPIO13/GPIO14/GPIO32 input-only encoder handling,
  GPIO21/GPIO22 LCD display-only I2C handling, `FR_DIAG_XBEE_BRIDGE_CLOSED 1`,
  and the no-relay/no-load/no-mains boundary.
- PF0530W COM6 identity, rollback, write-flash, separate verify-flash,
  read-only readiness monitor, transcript scan, and cleanup proof passed under
  Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-LIVE-2026-06-02`.

## Assumptions

- The same low-voltage LCD/KY-040 bench lane was used for the PF0530W live
  gate.
- The art-panel tile map is a deterministic visual proof surface, not a
  general runtime bitmap parser.
- Operator visual acceptance is still required for the physical ART page.

## Unknowns

- Physical LCD readability, contrast, flicker, and transient glyph behavior of
  the PF0530W art panel remain unproven.
- ART page render telemetry remains open because the read-only PF0530W monitor
  stayed on HOME with no physical encoder input.

## Reviewer Disposition

Read-only Tier 3 reviewers blocked immediate flash because the existing visual
art work was host-only and no current artifact proved firmware integration.
They conditionally allowed the source/build path used by this record as the
required next gate before any COM6 write/verify.

## Mutation Boundary

- `firmware/projects/four-relay-xbee-wifi/main/main.c`
- `firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h`
- `tools/simulators/lcd_bbs_menu/bbs_lcd_menu.v1.xml`
- `tools/simulators/lcd_bbs_menu/generate_lcd_menu.py`
- `tools/simulators/lcd_bbs_menu/generated_menu.py`
- `tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `scripts/scaffold_audit_firmware.py`
- `tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py`
- project docs, source index, source ledger, and task log records

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
  (30 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.scaffold_audits.test_firmware_pcnt_accumulator tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (40 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `git diff --check`.
- PASS: ESP-IDF v6.0.1 no-flash build to
  `/tmp/esp32-pf0530w-visual-art-build`.
- PASS: PF0530W COM6 live flash gate under
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-LIVE-2026-06-02`.
- Pending: physical ART page visual proof and ART render telemetry.

## Stop Gates

Stop before any further live flash unless a new Tier 3 gate supplies
same-session authority, identity, recovery/rollback, artifact hashes,
write/verify plan, monitor plan, and cleanup plan. Stop before claiming physical
ART page acceptance until operator visual evidence is collected. Stop before
erase, serial command writes, XBee/RF, ESP-NOW runtime expansion, relay GPIO
writes, relay-expander writes, MicroSD/TFT, wiring mutation, relay/load/mains,
persistent config, external services, release, commit, or push.
