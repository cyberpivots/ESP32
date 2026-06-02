# Four Relay KY-040 BBS LCD Menu PF0530P Debounce Calibration Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530P-DEBOUNCE-CAL-2026-06-01`

## Verified Facts

- PF0530P is a non-live source/build continuation after the PF0530O real-menu
  calibration live gate captured LCD readiness/render/heartbeat proof and zero
  encoder/button input events.
- Later same-day PF0530P COM6 write/verify/read-only readiness evidence is
  recorded separately under
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530P-LIVE-2026-06-01`; this
  source ledger remains the source/build proof boundary.
- PF0530P changes the active firmware ID to `PF0530P` and updates the generated
  `bbs_lcd_menu.v1` firmware/header and host model metadata from XML.
- PF0530P keeps GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` input-only with
  pullups, keeps LCD GPIO21/GPIO22 display-only, and keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`.
- PF0530P keeps `FR_ENCODER_TRANSITIONS_PER_STEP 1`,
  `FR_ENCODER_AB_STABLE_SAMPLES 2`, `FR_ENCODER_SW_DEBOUNCE_MS 30`,
  `FR_ENCODER_SW_GUARD_MS 75`, and `FR_ENCODER_LONG_PRESS_MS 650`.
- PF0530P adds `FR_ENCODER_AB_DEBOUNCE_MS 5` and
  `FR_ENCODER_STEP_LOCKOUT_MS 40`.
- PF0530P accepts a stable A/B candidate only after the source-visible stable
  sample count and minimum candidate hold time both pass.
- PF0530P suppresses extra accepted menu steps inside the 40 ms step-lockout
  window while keeping the stable A/B state current.
- PF0530P adds source-visible counters/logging for A/B debounce holds, accepted
  stable A/B transitions, step lockouts, invalid transitions, suppressed
  transitions, and queue drops.
- PF0530P extends existing log prefixes without adding double-click behavior or
  changing `bbs_lcd_menu.v1` or `bbs_lcd_render.v2` schemas.

## Assumptions

- PF0530P is a calibration candidate for future KY-040 LCD-menu user testing,
  not proof that PF0530O failed because of debounce behavior.
- ESP-IDF PCNT and Espressif `knob`/`button` component work remain deferred
  unless later live evidence proves raw A/B events exist but software decoding
  is the failure.
- The separate PF0530P live gate rechecked identity, rollback, artifact hashes,
  write/verify, read-only monitor, attended input, and cleanup evidence before
  the PF0530P flash. Future COM6 live actions still require a fresh Tier 3
  gate.

## Unknowns

- Whether physical actuation occurred during the PF0530O attended monitor.
- Exact physical encoder bounce behavior, accepted direction, per-detent
  behavior, quick-rotation behavior, short-button behavior, and long-button
  behavior under PF0530P remain unproven.
- PF0530P flash, verify-flash, and read-only readiness evidence exists only in
  the separate live record; physical encoder/button acceptance remains
  unproven.

## Validation

- PASS: focused Python unit tests:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (`Ran 30 tests in 0.181s`)
- PASS: touched comprehensive bench-process test:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_comprehensive_bench_process`
  (`Ran 3 tests in 0.011s`)
- PASS: generated menu freshness check:
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: firmware scaffold audit:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: scaffold verification:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: ESP-IDF v6.0.1 no-flash build:
  `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-pf0530p-debounce-cal-build build`
- PASS: `git diff --check`.

## Build Artifacts

- Bootloader path:
  `/tmp/esp32-pf0530p-debounce-cal-build/bootloader/bootloader.bin`
- Bootloader SHA-256:
  `<redacted-sha256>`
- Partition table path:
  `/tmp/esp32-pf0530p-debounce-cal-build/partition_table/partition-table.bin`
- Partition table SHA-256:
  `<redacted-sha256>`
- App path:
  `/tmp/esp32-pf0530p-debounce-cal-build/four_relay_xbee_wifi.bin`
- App SHA-256:
  `<redacted-sha256>`
- App size:
  `0x2d690`; free in the 1 MiB app partition: `0xd2970` (`82%`)
- Bootloader size:
  `0x6610`; free before partition table: `0x9f0` (`9%`)

## Files

- `firmware/projects/four-relay-xbee-wifi/main/main.c`
- `firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h`
- `firmware/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/four-relay-xbee-wifi/rotary-encoder-menu-plan.md`
- `docs/projects/espnow-bbs/lcd-encoder-field-console-plan.md`
- `docs/prompt/comprehensive-bench-development-process.md`
- `research/triage-status.md`
- `research/known-gaps.md`
- `research/development-status-ledger.md`
- `tools/simulators/lcd_bbs_menu/bbs_lcd_menu.v1.xml`
- `tools/simulators/lcd_bbs_menu/generate_lcd_menu.py`
- `tools/simulators/lcd_bbs_menu/generated_menu.py`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py`
- `tests/scaffold_audits/test_comprehensive_bench_process.py`
- `scripts/scaffold_audit_firmware.py`
- `knowledge-base/source-index.md`
- `docs/index.md`
- `.agents/TASK_LOG/0131-four-relay-ky040-bbs-lcd-menu-pf0530p-debounce-calibration.md`

## Authority Limits

This source record does not prove or authorize COM6 access, flash,
verify-flash, monitor, serial writes, XBee/RF writes, ESP-NOW live runtime,
relay GPIO writes, relay-expander writes, MicroSD/TFT action, wiring mutation,
DMM/current measurement, relay/load/mains work, erase, firmware
HTTP/SoftAP/WebSocket runtime, persistent config, external services, GitHub
publication, release, commit, or push. The later PF0530P live record proves
only its separately authorized COM6 write/verify/read-only monitor gate.
