# Handoff 0129 - PF0530W Host-Only Validation To QA/LCD/Hardware

Continuation record for Task 0181
`four-relay-ky040-bbs-lcd-menu-pf0530w-host-only-validation`.

## Continue with

- Treat Task 0181 as host-only validation of PF0530W simulator/catalog/
  ART-carousel behavior, not physical LCD acceptance.
- Use
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-HOST-ONLY-VALIDATION-2026-06-05`
  for the accepted host-only validation packet.
- Preserve Task 0148 provenance with
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-ART-CAROUSEL-2026-06-02`;
  the render payload source ID still points to the earlier PF0530W visual-art
  source/build record.
- If physical acceptance is needed, open a separate Tier 3 gate for physical
  encoder navigation to `ART`, operator visual acceptance, optional read-only
  ART-page monitor telemetry, same-session evidence, recovery path, and
  cleanup.

## Stop Gates

- No physical ART-page visual acceptance is proven by Task 0181.
- No live-flashed Task 0148 carousel behavior, current COM6 state, flash,
  erase, monitor, serial writes, RF/XBee, ESP-NOW runtime, relay GPIO writes,
  relay-expander writes, MicroSD, TFT, wiring mutation, DMM/current/load/mains,
  release, publication, commit, push, PR, deploy,
  `/etc/codex/requirements.toml`, or `admin-strict` mutation is authorized.

## Validation to preserve

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.lcd_bbs_menu.test_lcd_bbs_menu
PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.scaffold_audits.test_firmware_pcnt_accumulator tests.lcd_bbs_menu.test_lcd_bbs_menu
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 181
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py
git diff --check
```
