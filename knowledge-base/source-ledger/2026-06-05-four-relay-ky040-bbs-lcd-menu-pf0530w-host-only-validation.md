# Four Relay KY-040 BBS LCD Menu PF0530W Host-Only Validation Ledger

Date: 2026-06-05

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-HOST-ONLY-VALIDATION-2026-06-05`

## Scope

Tier 2 host-only validation packet for the PF0530W LCD visual-art lane. This
ledger records reviewer quorum output, focused host validation, and durable
status updates after Task 0148 added a source/build ART carousel. It does not
open live hardware or claim physical LCD acceptance.

## Source Coverage

- PF0530W firmware-visible ART integration is recorded by
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-VISUAL-ART-2026-06-02`.
- PF0530W COM6 write/verify/readiness proof is recorded by
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-LIVE-2026-06-02`.
- PF0530W pixel-preview/catalog live artifact proof is recorded by
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-PIXEL-PREVIEW-LIVE-2026-06-02`
  and the host catalog record
  `SRC-LOCAL-ESPNOW-BBS-LCD-PIXEL-PREVIEW-CATALOG-2026-06-02`.
- PF0530W ART-carousel source/build behavior is recorded by
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-ART-CAROUSEL-2026-06-02`.
- HD44780 custom-character and 20x4 row-planning constraints remain covered by
  `SRC-HITACHI-HD44780U-DDRAM-CGRAM-2026-05-31` and
  `SRC-NXP-HD44780-4X20-DDRAM-2026-05-31`.

## Verified Facts

- The agentic planning guide lists PF0530W visual/host validation as the third
  approved next sequence item.
- `.codex/config.toml` and the guide record `max_threads = 6` and
  `max_depth = 2`; deeper delegation is bounded to small evidence-only helper
  tasks.
- Read-only reviewers approved the host-only packet with 11/11 weighted
  approval and no P1/P2 blockers for the named records boundary.
- The host LCD test suite passes with 34 tests.
- The generated menu freshness check passes.
- The focused firmware/LCD boundary suite passes with 44 tests.
- Host ART metadata inspection shows the ART page cycles five panels:
  `bbs_badge`, `mesh_radar`, `packet_flow`, `signal_skyline`, and `link_heat`.
  The host model wraps back to `bbs_badge`, keeps `cursor.focus=art_panel`,
  keeps selected item `0`, keeps glyph bank `art_panel`, and exposes
  `bbs_lcd_pixel_preview.v1` metadata for each active panel.
- The render payload source ID still reports the earlier PF0530W visual-art
  source/build record; Task 0148 and this ledger are the provenance for
  carousel and host-only validation acceptance.

## Unknowns

- Physical LCD readability of the `ART` page remains unverified.
- Live ART-carousel telemetry remains unverified until a separate Tier 3 gate
  flashes and monitors a carousel source image.
- Current COM6/device state was not inspected.
- Exact LCD module/backpack behavior, pullup voltage, contrast, flicker,
  transient CGRAM redraw behavior, and rail margin remain unresolved by this
  host-only record.

## Authority Limits

This record does not authorize live bench work, flash, erase, monitor, serial
writes, RF/XBee writes, ESP-NOW runtime expansion, relay GPIO writes,
relay-expander writes, SoftAP/browser firmware runtime, persistent config,
MicroSD, TFT, wiring, DMM/current/load/mains work, release, publication,
commit, push, PR creation, deploy, `/etc/codex/requirements.toml`, or
`admin-strict` mutation.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (34 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`.
- PASS: host ART metadata import check for five-panel cycle/wrap, `art_panel`
  focus, selected item stability, `art_panel` glyph bank, and
  `bbs_lcd_pixel_preview.v1` metadata.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.scaffold_audits.test_firmware_pcnt_accumulator tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (44 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 181`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `git diff --check`.

## Decision

Decision: PF0530W host-only validation is accepted for simulator, catalog, and
ART-carousel records. Physical ART visual acceptance and live ART-page
telemetry remain open behind a separate Tier 3 gate.
