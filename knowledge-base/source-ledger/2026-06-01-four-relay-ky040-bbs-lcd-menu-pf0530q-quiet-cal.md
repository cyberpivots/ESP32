# Four Relay KY-040 BBS LCD Menu PF0530Q Quiet Calibration Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530Q-QUIET-CAL-2026-06-01`

## Verified Facts

- PF0530Q is a non-live source/build continuation after the user clarified
  that they did not rotate the encoder during the PF0530P read-only monitor;
  the PF0530P zero-input transcript is therefore not diagnostic of debounce
  behavior.
- Later same-day PF0530Q COM6 write/verify/read-only readiness evidence is
  recorded separately under
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530Q-LIVE-2026-06-01`; this
  source ledger remains the source/build proof boundary.
- Prior PF0530L/PF0530N interaction evidence under
  `SRC-LOCAL-TIER3-COM6-ATTENDED-INTERACTION-PROOF-2026-05-31` proved that the
  GPIO interrupt/software quadrature path can capture raw and decoded KY-040
  input events when physical actuation occurs.
- PF0530Q changes the active firmware ID to `PF0530Q` and updates the generated
  `bbs_lcd_menu.v1` firmware/header and host model metadata from XML.
- PF0530Q keeps GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` input-only with
  pullups, keeps LCD GPIO21/GPIO22 display-only, and keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`.
- PF0530Q keeps `FR_ENCODER_TRANSITIONS_PER_STEP 1`,
  `FR_ENCODER_AB_STABLE_SAMPLES 2`, `FR_ENCODER_AB_DEBOUNCE_MS 5`,
  `FR_ENCODER_SW_DEBOUNCE_MS 30`, `FR_ENCODER_SW_GUARD_MS 75`, and
  `FR_ENCODER_LONG_PRESS_MS 650`.
- PF0530Q adds `FR_ENCODER_AB_QUIET_MS 10`, raises
  `FR_ENCODER_STEP_LOCKOUT_MS` to `60`, and accepts stable A/B changes through
  a combined two-bit pair filter instead of independent per-channel stable
  acceptance.
- PF0530Q requires the candidate A/B pair to satisfy stable sample count, a
  5 ms candidate hold, and a 10 ms raw-edge quiet window before the stable pair
  is accepted.
- PF0530Q adds source-visible telemetry for raw A/B edge gaps, raw burst count,
  A/B quiet holds, accepted stable A/B pair transitions, debounce holds,
  step-lockouts, invalid transitions, suppressed transitions, and queue drops.
- PF0530Q extends existing log prefixes with `cal=quiet-v3`, `quiet_ms=10`,
  `ENC_FILTER reason=ab_quiet`, and heartbeat raw-burst/gap counters without
  adding double-click behavior or changing `bbs_lcd_menu.v1` or
  `bbs_lcd_render.v2` schemas.

## Assumptions

- PF0530Q is an inferred calibration candidate from prior raw/bounce
  transcripts, not accepted physical encoder/button behavior.
- ESP-IDF PCNT and Espressif `knob`/`button` component work remain deferred
  unless later live evidence proves raw A/B events exist but software decoding
  is the failure.
- The same-session user live-gate authority supplied after this source/build
  work was later paired with COM6 identity, rollback, artifact, write, verify,
  monitor, and cleanup evidence in the separate PF0530Q live ledger.

## Unknowns

- Exact KY-040 bounce timing under the current hardware remains unaccepted until
  a live transcript captures physical actuation under PF0530Q.
- Physical direction, one-detent behavior, quick-rotation behavior, short
  button behavior, long-button behavior, and LCD response under PF0530Q remain
  unaccepted.

## Validation

- PASS: focused Python unit tests:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (`Ran 30 tests in 0.138s`)
- PASS: generated menu freshness check:
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: firmware scaffold audit:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: ESP-IDF v6.0.1 no-flash build:
  `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-pf0530q-quiet-cal-build build`

## Build Artifacts

- Bootloader path:
  `/tmp/esp32-pf0530q-quiet-cal-build/bootloader/bootloader.bin`
- Bootloader SHA-256:
  `<redacted-sha256>`
- Partition table path:
  `/tmp/esp32-pf0530q-quiet-cal-build/partition_table/partition-table.bin`
- Partition table SHA-256:
  `<redacted-sha256>`
- App path:
  `/tmp/esp32-pf0530q-quiet-cal-build/four_relay_xbee_wifi.bin`
- App SHA-256:
  `<redacted-sha256>`
- App size:
  `0x2d7c0`; free in the 1 MiB app partition: `0xd2840` (`82%`)
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
- `.agents/TASK_LOG/0132-four-relay-ky040-bbs-lcd-menu-pf0530q-quiet-calibration.md`

## Authority Limits

This source record does not prove or authorize COM6 access, flash,
verify-flash, monitor, serial writes, XBee/RF writes, ESP-NOW live runtime,
relay GPIO writes, relay-expander writes, MicroSD/TFT action, wiring mutation,
DMM/current measurement, relay/load/mains work, erase, firmware
HTTP/SoftAP/WebSocket runtime, persistent config, external services, GitHub
publication, release, commit, or push. Any PF0530Q live record must carry its
own same-session Tier 3 evidence.
