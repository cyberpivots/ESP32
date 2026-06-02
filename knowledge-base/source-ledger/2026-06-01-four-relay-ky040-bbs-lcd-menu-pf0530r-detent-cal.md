# Four Relay KY-040 BBS LCD Menu PF0530R Detent Calibration Source Ledger

Source ID: `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530R-DETENT-CAL-2026-06-01`

Date: 2026-06-01

## Scope

PF0530R started as a non-live source/build calibration candidate after the user
reported PF0530Q works but is not stable. A later same-session Tier 3 gate
flashed and separately verify-flashed PF0530R on COM6; that live evidence is
recorded separately under
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530R-LIVE-2026-06-01`.

## Verified Facts

- PF0530R changes firmware identity and generated menu metadata to `PF0530R`.
- Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530R-DETENT-CAL-2026-06-01`.
- GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` remain input-only with pullups.
- LCD GPIO21/GPIO22 remains display-only, and `FR_DIAG_XBEE_BRIDGE_CLOSED 1`
  remains set.
- PF0530R keeps two A/B stable samples, 30 ms switch debounce, 75 ms switch
  guard, and 650 ms long press.
- PF0530R sets:
  - `FR_ENCODER_AB_DEBOUNCE_MS 8`
  - `FR_ENCODER_AB_QUIET_MS 15`
  - `FR_ENCODER_DETENT_AB 3U`
  - `FR_ENCODER_TRANSITIONS_PER_STEP 2`
  - `FR_ENCODER_STEP_LOCKOUT_MS 90`
- PF0530R emits a rotation step through `fr_menu_emit_rotation_step()` only
  when accepted quadrature returns to detent A/B `3`.
- PF0530R adds detent telemetry counters and `ENC_FILTER reason=detent_partial`.
- PF0530R appends `cal=detent-v4`, `ab_ms=8`, `quiet_ms=15`,
  `step_lockout_ms=90`, and `detent=3` to readiness logs.
- The XML schema remains `bbs_lcd_menu.v1`; the render schema remains
  `bbs_lcd_render.v2`.

## Assumptions

- The reported PF0530Q instability is likely caused by bounce-driven extra
  movement, partial detents, or inconsistent detent boundaries, not by a dead
  GPIO path.
- KY-040 pullup idle/resting state is A/B `3`, making it the practical detent
  return point for this calibration candidate.

## Unknowns

- PF0530R physical direction, one-detent behavior, fast rotation behavior,
  button select behavior, and LCD response.
- Whether the new detent gating solves the reported instability.

## Validation

- PASS: focused LCD/encoder unittest suite:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.lcd_bbs_menu.test_lcd_bbs_menu`
- PASS: comprehensive bench-process unittest:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_comprehensive_bench_process`
- PASS: generated menu freshness check:
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: firmware scaffold audit:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: ESP-IDF v6.0.1 no-flash build:
  `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-pf0530r-detent-cal-build build`
- PASS: scaffold verification:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: diff hygiene:
  `git diff --check`
- Build result:
  - App size: `0x2d8b0`
  - Free app partition space: `0xd2750` (`82%`)
  - Bootloader size: `0x6610`
  - Free bootloader space before partition table: `0x9f0` (`9%`)

## Artifact Hashes

- Bootloader:
  `<redacted-sha256>`
- Partition table:
  `<redacted-sha256>`
- App:
  `<redacted-sha256>`

## Files

- `firmware/projects/four-relay-xbee-wifi/main/main.c`
- `firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h`
- `tools/simulators/lcd_bbs_menu/bbs_lcd_menu.v1.xml`
- `tools/simulators/lcd_bbs_menu/generate_lcd_menu.py`
- `tools/simulators/lcd_bbs_menu/generated_menu.py`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py`
- `tests/scaffold_audits/test_comprehensive_bench_process.py`
- `scripts/scaffold_audit_firmware.py`
- `firmware/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/four-relay-xbee-wifi/rotary-encoder-menu-plan.md`
- `docs/projects/espnow-bbs/lcd-encoder-field-console-plan.md`
- `docs/prompt/comprehensive-bench-development-process.md`
- `research/triage-status.md`
- `research/development-status-ledger.md`
- `research/known-gaps.md`
- `docs/index.md`
- `knowledge-base/source-index.md`
- `.agents/TASK_LOG/0133-four-relay-ky040-bbs-lcd-menu-pf0530r-detent-calibration.md`
- `.agents/handoffs/0097-four-relay-ky040-bbs-lcd-menu-pf0530r-to-hardware-qa.md`

## Closed Surfaces

This source/build record by itself does not prove or authorize COM6 access,
flash, verify-flash, monitor, serial command writes, XBee/RF writes or tests,
ESP-NOW live runtime, relay GPIO writes, relay-expander writes, MicroSD/TFT
action, wiring mutation, DMM/current measurement, relay/load/mains work,
erase, persistent config, external services, GitHub publication, release,
commit, or push. The later PF0530R COM6 write/verify/readiness gate is recorded
only by the separate PF0530R live source ledger.
