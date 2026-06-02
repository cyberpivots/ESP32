# Four Relay KY-040 BBS LCD Menu PF0530V PCNT Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-PCNT-SOURCE-BUILD-2026-06-02`

Date: 2026-06-02

## Scope

PF0530V is the source/build continuation after PF0530U was written and
verify-flashed but its post-flash monitors captured no physical input events.
PF0530V stops tuning the software detent gate and moves rotary A/B movement to
ESP-IDF PCNT quadrature counting while keeping the switch path poll/debounce
based.

## Verified Facts

- PF0530V changes firmware identity and generated menu metadata to `PF0530V`.
- GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` remain input-only with pullups.
- LCD GPIO21/GPIO22 remains display-only, and `FR_DIAG_XBEE_BRIDGE_CLOSED 1`
  remains set.
- The firmware now declares `esp_driver_pcnt` and includes
  `driver/pulse_cnt.h`.
- PCNT low/high limits are `-32767` and `32767`; recenter starts at count
  magnitude `30000`; glitch filter is `1000` ns; emitted steps use four PCNT
  counts per menu step and cap at four steps per poll.
- Readiness and heartbeat logs include `cal=pcnt-v1`, `decoder=pcnt`,
  `irq=pcnt`, `poll_decoder=0`, `ENC_PCNT_READY`, and `ENC_PCNT_HB`.
- The XML schema remains `bbs_lcd_menu.v1`; the render schema remains
  `bbs_lcd_render.v2`.

## Validation

- PASS: focused unit/audit bundle ran 60 tests.
- PASS: generated menu freshness check.
- PASS: firmware scaffold audit.
- PASS: agent-process scaffold audit.
- PASS: source, docs, and data scaffold audits.
- PASS: scaffold verification.
- PASS: ESP-IDF v6.0.1 no-flash build to `/tmp/esp32-pf0530v-pcnt-build`.
- PASS: final `git diff --check`.

## Files

- `firmware/projects/four-relay-xbee-wifi/main/main.c`
- `firmware/projects/four-relay-xbee-wifi/main/CMakeLists.txt`
- `firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h`
- `tools/simulators/lcd_bbs_menu/bbs_lcd_menu.v1.xml`
- `tools/simulators/lcd_bbs_menu/generate_lcd_menu.py`
- `tools/simulators/lcd_bbs_menu/generated_menu.py`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py`
- `tests/scaffold_audits/test_firmware_pcnt_accumulator.py`
- `scripts/scaffold_audit_firmware.py`
- `docs/index.md`
- `knowledge-base/source-index.md`
- `.agents/TASK_LOG/0138-four-relay-ky040-bbs-lcd-menu-pf0530v-pcnt-source-build.md`
- `.agents/handoffs/0102-four-relay-ky040-bbs-lcd-menu-pf0530v-to-hardware-qa.md`

## Closed Surfaces

This source/build record does not prove or authorize COM6 access, flash,
verify-flash, monitor, serial command writes, XBee/RF writes or tests, ESP-NOW
live runtime, relay GPIO writes, relay-expander writes, MicroSD/TFT action,
wiring mutation, DMM/current measurement, relay/load/mains work, erase,
persistent config, external services, GitHub publication, release, commit, or
push.
