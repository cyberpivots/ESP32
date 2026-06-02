# Four Relay KY-040 BBS LCD Menu PF0530S Raw-Liveness Calibration Source Ledger

Source ID: `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530S-RAW-LIVENESS-CAL-2026-06-01`

Date: 2026-06-01

## Scope

PF0530S is the raw-liveness recovery image after PF0530R was written and
separately verify-flashed on COM6 but the attended monitor captured zero
`ENC_RAW`, zero `ENC_EV`, zero `BBS_MENU_STEP`, zero `BBS_MENU_SELECT`, and
zero `ENC_FILTER` lines. The PF0530S source/build change is intended to prove
raw GPIO visibility first while keeping enough filtering to avoid obvious
bounce runaway.

## Verified Facts

- PF0530S changes firmware identity and generated menu metadata to `PF0530S`.
- Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530S-RAW-LIVENESS-CAL-2026-06-01`.
- GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` remain input-only with pullups.
- LCD GPIO21/GPIO22 remains display-only, and `FR_DIAG_XBEE_BRIDGE_CLOSED 1`
  remains set.
- PF0530S keeps two A/B stable samples, 30 ms switch debounce, 75 ms switch
  guard, and 650 ms long press.
- PF0530S sets:
  - `FR_ENCODER_AB_DEBOUNCE_MS 3`
  - `FR_ENCODER_AB_QUIET_MS 0`
  - `FR_ENCODER_TRANSITIONS_PER_STEP 1`
  - `FR_ENCODER_STEP_LOCKOUT_MS 45`
  - `FR_ENCODER_RAW_HEARTBEAT_MS 1000`
- PF0530S keeps detent counters as telemetry, but `fr_menu_handle_rotation()`
  no longer requires return to detent A/B `3` before emitting a menu step.
- PF0530S emits `ENC_BASE`, per-pin `ENC_GPIO_CONFIG`, ESP-IDF
  `gpio_dump_io_configuration(stdout, mask)`, and one-second `ENC_LEVEL_HB`
  raw-level heartbeats.
- PF0530S extends `BBS_MENU_HB` with raw levels, stable/candidate A/B,
  raw-transition counts, ISR counts, queue receive/drop counts, and poll count.
- PF0530S appends `cal=raw-live-v5`, `ab_ms=3`, `quiet_ms=0`,
  `step_lockout_ms=45`, `raw_hb_ms=1000`, `gpio_cfg=1`, and `poll_raw=1` to
  input readiness logs.
- The XML schema remains `bbs_lcd_menu.v1`; the render schema remains
  `bbs_lcd_render.v2`.

## Assumptions

- The latest user report refers to the currently flashed PF0530R behavior after
  physical operation.
- The current safe-state/live-flash authorization applies to this PF0530S
  continuation.
- PCNT, `espressif/knob`, and `espressif/button` remain deferred until PF0530S
  proves raw A/B transitions exist but the custom decoder remains unstable.

## Unknowns

- Whether `FR_ENCODER_STEP_LOCKOUT_MS 45` and the current queue/debounce path
  are stable enough for longer mixed-speed operation remains open.
- The later PF0530S live ledger records recovered raw liveness and
  input/menu/select response, but also records invalid/suppressed transitions
  and queue drops.

## Validation

- PASS: focused LCD/encoder unittest suite:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.lcd_bbs_menu.test_lcd_bbs_menu`
- PASS: generated menu freshness check:
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: broader scaffold audit, scaffold verification, ESP-IDF no-flash build,
  artifact hashes, and pre-flash `git diff --check` completed in the PF0530S
  gate.
- Later live proof is recorded separately under
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530S-LIVE-2026-06-01`.

## Files

- `firmware/projects/four-relay-xbee-wifi/main/main.c`
- `firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h`
- `tools/simulators/lcd_bbs_menu/bbs_lcd_menu.v1.xml`
- `tools/simulators/lcd_bbs_menu/generate_lcd_menu.py`
- `tools/simulators/lcd_bbs_menu/generated_menu.py`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py`
- `scripts/scaffold_audit_firmware.py`
- `firmware/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/four-relay-xbee-wifi/rotary-encoder-menu-plan.md`
- `docs/projects/espnow-bbs/lcd-encoder-field-console-plan.md`
- `research/triage-status.md`
- `research/development-status-ledger.md`
- `research/known-gaps.md`
- `docs/index.md`
- `knowledge-base/source-index.md`
- `.agents/TASK_LOG/0134-four-relay-ky040-bbs-lcd-menu-pf0530s-raw-liveness.md`

## Closed Surfaces

This source/build record by itself does not prove or authorize COM6 access,
flash, verify-flash, monitor, serial command writes, XBee/RF writes or tests,
ESP-NOW live runtime, relay GPIO writes, relay-expander writes, MicroSD/TFT
action, wiring mutation, DMM/current measurement, relay/load/mains work,
erase, persistent config, external services, GitHub publication, release,
commit, or push. The later Tier 3 continuation separately recorded only COM6
identity, rollback backup, bootloader/partition/app write, separate
verify-flash, reset/read-only monitor, attended read-only monitor, cleanup
proof, and durable records under
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530S-LIVE-2026-06-01`.
