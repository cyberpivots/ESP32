# Four Relay KY-040 BBS LCD Menu PF0530T Responsive Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530T-RESPONSIVE-2026-06-02`

Date: 2026-06-02

## Scope

PF0530T is the responsiveness recovery image after PF0530S proved raw liveness
but remained unstable. PF0530T prioritizes usable LCD menu movement over
diagnostic verbosity.

## Verified Facts

- PF0530T changes firmware identity and generated menu metadata to `PF0530T`.
- GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` remain input-only with pullups.
- LCD GPIO21/GPIO22 remains display-only, and `FR_DIAG_XBEE_BRIDGE_CLOSED 1`
  remains set.
- PF0530T makes polling the authoritative decoder path:
  `FR_MENU_POLL_MS 2`, `FR_ENCODER_INTERRUPT_TELEMETRY 0U`, queue depth/drain
  `0`, and readiness `irq=poll`.
- PF0530T disables per-edge raw serial logging with
  `FR_ENCODER_RAW_EVENT_LOG_ENABLED 0U`.
- PF0530T emits rotation only from detent return with
  `FR_ENCODER_DETENT_GATED 1U`, `FR_ENCODER_TRANSITIONS_PER_STEP 2`, and
  `FR_ENCODER_STEP_LOCKOUT_MS 25`.
- PF0530T uses `FR_ENCODER_AB_STABLE_SAMPLES 1`,
  `FR_ENCODER_AB_DEBOUNCE_MS 1`, `FR_ENCODER_AB_QUIET_MS 0`,
  `FR_ENCODER_SW_DEBOUNCE_MS 30`, `FR_ENCODER_SW_GUARD_MS 25`, and
  `FR_ENCODER_LONG_PRESS_MS 650`.
- PF0530T appends `cal=responsive-v6`, `detent_gate=1`, `raw_log=0`, and
  `poll_decoder=1` to input readiness logs.
- The XML schema remains `bbs_lcd_menu.v1`; the render schema remains
  `bbs_lcd_render.v2`.

## Assumptions

- PF0530S's queue/drop instability was at least partly caused by interrupt-fed
  event pressure and per-edge serial logging.
- Detent-gated polling with a shorter lockout should be more usable for a real
  LCD menu than transition-per-step diagnostic decoding.

## Unknowns

- Physical one-detent feel and fast-scroll behavior remain live-proof items.

## Validation

- PASS: focused LCD/encoder unittest suite.
- PASS: generated menu freshness check.
- PASS: firmware scaffold audit.
- PASS: ESP-IDF v6.0.1 no-flash build:
  `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-pf0530t-responsive-build build`
- Pending: scaffold verification, `git diff --check`, COM6 live proof, and
  final live record updates.

## Files

- `firmware/projects/four-relay-xbee-wifi/main/main.c`
- `firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h`
- `tools/simulators/lcd_bbs_menu/bbs_lcd_menu.v1.xml`
- `tools/simulators/lcd_bbs_menu/generate_lcd_menu.py`
- `tools/simulators/lcd_bbs_menu/generated_menu.py`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py`
- `scripts/scaffold_audit_firmware.py`
- `docs/index.md`
- `knowledge-base/source-index.md`
- `.agents/TASK_LOG/0135-four-relay-ky040-bbs-lcd-menu-pf0530t-responsive.md`
- `.agents/handoffs/0099-four-relay-ky040-bbs-lcd-menu-pf0530t-to-hardware-qa.md`

## Closed Surfaces

This source/build record by itself does not prove or authorize COM6 access,
flash, verify-flash, monitor, serial command writes, XBee/RF writes or tests,
ESP-NOW live runtime, relay GPIO writes, relay-expander writes, MicroSD/TFT
action, wiring mutation, DMM/current measurement, relay/load/mains work,
erase, persistent config, external services, GitHub publication, release,
commit, or push. The active Tier 3 continuation separately opens only COM6
identity, rollback backup, bootloader/partition/app write, separate
verify-flash, reset/read-only monitor, attended read-only monitor, cleanup
proof, and durable records.
