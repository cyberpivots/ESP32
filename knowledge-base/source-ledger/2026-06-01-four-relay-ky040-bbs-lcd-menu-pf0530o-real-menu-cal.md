# Four Relay KY-040 BBS LCD Menu PF0530O Real-Menu Calibration Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530O-REAL-MENU-CAL-2026-06-01`

## Verified Facts

- PF0530O is a source/build continuation after the PF0530N live and attended
  encoder/button evidence.
- The PF0530N attended retry captured raw encoder events, decoded encoder
  events, menu steps in both directions, five short button selections, ongoing
  LCD renders/heartbeats, and zero crash/unsafe markers; it did not capture a
  long button selection.
- PF0530O changes the active firmware ID to `PF0530O`.
- PF0530O keeps GPIO13/GPIO14/GPIO32 input-only encoder handling and keeps
  LCD writes display-only on GPIO21/GPIO22.
- PF0530O changes encoder calibration to one transition per menu step, two AB
  stable samples, a 75 ms switch guard, and a 650 ms long-press threshold.
- PF0530O decodes quadrature movement when stable A/B changes are accepted,
  not before stable A/B state is updated.
- PF0530O disables automatic menu cycling at boot so the real LCD menu remains
  operator-controlled during review.
- PF0530O updates the firmware/menu source wording away from simulator/demo
  labels and uses `gauge` for the gauge glyph bank.
- The ESP-IDF v6.0.1 no-flash build completed and generated the PF0530O app
  image.

## Assumptions

- One accepted transition per menu step is the correct next calibration for
  the current tactile encoder evidence. Live PF0530O review may prove it needs
  to be raised.
- Host/simulator validation is intentionally not used as acceptance for this
  calibration because the requested review surface is the actual LCD menu on
  the programmed device.
- A fresh Tier 3 COM6 gate will recheck identity and safe state before any
  write/verify/monitor action.

## Unknowns

- PF0530O was later written and separately verify-flashed to COM6 under the
  linked live gate; see
  `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530o-live.md`.
- Physical LCD visual timing, accepted encoder direction, one-detent behavior,
  quick-rotation behavior, and short/long button behavior under PF0530O remain
  unproven until the user visual/input report or a later read-only input gate.

## Validation

- PASS: `git diff --check`
- PASS: ESP-IDF v6.0.1 no-flash build:
  `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-pf0530o-real-menu-cal-build build`
- PASS: `four_relay_xbee_wifi.bin` size `0x2d390`, with `0xd2c70` bytes
  free in the smallest app partition.
- Artifact hashes:
  - bootloader:
    `7c4061b011b1d8812653906ca2f9cb95fee1ca687f057119bacb8a508f3f9dcb`
  - partition table:
    `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820`
  - app:
    `301e6bed800d0d644a32da6512efadf08f14b540139c4e78a7b385e054f9db7b`
- NOT RUN: host simulator, mock, or unit tests, per user instruction.

## Files

- `firmware/projects/four-relay-xbee-wifi/main/main.c`
- `firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h`
- `firmware/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/espnow-bbs/lcd-encoder-field-console-plan.md`
- `docs/projects/espnow-bbs/lcd-menu-graphics-browser-agent-plan.md`
- `docs/projects/four-relay-xbee-wifi/rotary-encoder-menu-plan.md`
- `docs/prompt/comprehensive-bench-development-process.md`
- `research/triage-status.md`
- `research/known-gaps.md`
- `research/development-status-ledger.md`
- `tools/simulators/lcd_bbs_menu/bbs_lcd_menu.v1.xml`
- `tools/simulators/lcd_bbs_menu/generate_lcd_menu.py`
- `tools/simulators/lcd_bbs_menu/generated_menu.py`
- `tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `.agents/TASK_LOG/0129-four-relay-ky040-bbs-lcd-menu-pf0530o-real-menu-calibration.md`
- `knowledge-base/source-index.md`
- `docs/index.md`

## Authority Limits

This source record does not prove or authorize COM6 access, flash, erase,
serial writes, XBee/RF writes, ESP-NOW live runtime, relay GPIO writes,
relay-expander writes, MicroSD/TFT action, wiring mutation, DMM/current
measurement, relay/load/mains work, firmware HTTP/SoftAP/WebSocket runtime,
persistent config, external services, GitHub publication, release, commit, or
push.
