# Four Relay KY-040 BBS LCD Menu PF0530U Responsive V7 Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530U-RESPONSIVE-V7-2026-06-02`

Date: 2026-06-02

## Scope

PF0530U is the responsive-v7 continuation after PF0530T restored live raw input
and select proof but emitted too few rotation steps for a usable menu.

## Verified Facts

- PF0530U changes firmware identity and generated menu metadata to `PF0530U`.
- GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` remain input-only with pullups.
- LCD GPIO21/GPIO22 remains display-only, and `FR_DIAG_XBEE_BRIDGE_CLOSED 1`
  remains set.
- PF0530U keeps polling authoritative with `FR_MENU_POLL_MS 2`,
  `FR_ENCODER_INTERRUPT_TELEMETRY 0U`, queue depth/drain `0`, and readiness
  `irq=poll`.
- PF0530U keeps per-edge raw serial logging disabled with
  `FR_ENCODER_RAW_EVENT_LOG_ENABLED 0U`.
- PF0530U emits rotation only from detent return with
  `FR_ENCODER_DETENT_GATED 1U`, `FR_ENCODER_TRANSITIONS_PER_STEP 1`, and
  `FR_ENCODER_STEP_LOCKOUT_MS 25`.
- PF0530U appends `cal=responsive-v7`, `detent_gate=1`, `raw_log=0`, and
  `poll_decoder=1` to readiness logs.
- The XML schema remains `bbs_lcd_menu.v1`; the render schema remains
  `bbs_lcd_render.v2`.

## Validation

- Pending: focused tests, generated menu freshness check, firmware scaffold
  audit, scaffold verification, ESP-IDF build, COM6 live proof, and final live
  record updates.

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
- `.agents/TASK_LOG/0136-four-relay-ky040-bbs-lcd-menu-pf0530u-responsive-v7.md`
- `.agents/handoffs/0100-four-relay-ky040-bbs-lcd-menu-pf0530u-to-hardware-qa.md`

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
