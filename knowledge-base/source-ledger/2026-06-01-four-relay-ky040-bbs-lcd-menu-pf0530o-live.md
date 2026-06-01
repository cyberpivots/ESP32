# Four Relay KY-040 BBS LCD Menu PF0530O Live Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530O-LIVE-2026-06-01`

## Verified Facts

- The user explicitly authorized the same-session live gate with
  `SAFE STATE VERIFIED` and `Allow flash on COM6`.
- COM6 was rechecked through Windows esptool before programming as an ESP32
  target with 4 MB detected flash and 3.3 V flash-voltage strap evidence.
- A full 4 MB rollback backup was captured before programming. The rollback
  backup SHA-256 is retained in the ignored local evidence directory.
- PF0530O artifacts were rebuilt with ESP-IDF v6.0.1, copied into the ignored
  local evidence directory, and pinned before programming:
  - bootloader:
    `7c4061b011b1d8812653906ca2f9cb95fee1ca687f057119bacb8a508f3f9dcb`
  - partition table:
    `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820`
  - app:
    `301e6bed800d0d644a32da6512efadf08f14b540139c4e78a7b385e054f9db7b`
- Windows esptool `write-flash` completed for the PF0530O bootloader,
  partition table, and app offsets, with per-segment hash verification.
- A separate Windows esptool `verify-flash` pass matched all three PF0530O
  artifacts.
- The reset boot monitor used no serial byte writes and captured:
  `PF0530O BBS_LCD_READY`, `PF0530O BBS_INPUT_READY`, `LCD_INIT_OK addr=0x27`,
  `auto_cycle=off`, `cal=real-menu-v1`, `step=1`, `stable=2`,
  `sw_guard_ms=75`, `long_ms=650`, 14 `BBS_MENU_HB`, 14 `BBS_LCD_RENDER`, one
  `BBS_GLYPH_BANK`, zero crash markers, and zero unsafe markers.
- The attended 150 second read-only monitor used `writes_sent=false`, captured
  75 `BBS_MENU_HB`, 75 `BBS_LCD_RENDER`, 75 `BBS_CURSOR`, zero crash markers,
  zero unsafe markers, and zero bad 20-character render row lengths.
- The attended monitor captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT`.
- Linux and Windows cleanup checks found no lingering COM6/esptool/Python
  monitor process after the run.
- No host simulator, mock, or unit tests were run as acceptance.

## Assumptions

- COM6 remained connected to the intended ESP32 target during the full
  write/verify/monitor sequence.
- The attended monitor cues were delivered to the operator, but physical
  actuation must be confirmed by the user before treating the zero input events
  as a hardware/input-capture failure rather than a missed interaction window.
- If the user confirms they rotated and pressed during the window, the next
  troubleshooting lane is physical/input capture evidence on GPIO13/GPIO14/GPIO32
  before more debounce or transitions-per-step tuning.

## Unknowns

- User visual report for the PF0530O LCD menu after flash is still pending.
- Whether physical encoder/button actuation occurred during the 150 second
  attended monitor is not confirmed in this record.
- Physical encoder direction, one-detent behavior, quick-rotation behavior,
  short-button behavior, and long-button behavior remain unaccepted because the
  attended transcript captured no input events.

## Validation

- PASS: `git diff --check`
- PASS: ESP-IDF v6.0.1 no-flash build.
- PASS: full rollback backup captured before programming.
- PASS: PF0530O artifact hashes pinned before programming.
- PASS: Windows esptool write-flash completed on COM6 for the PF0530O
  bootloader, partition table, and app image.
- PASS: Separate Windows esptool verify-flash matched all three PF0530O
  artifacts.
- PASS: reset boot monitor proved PF0530O runtime readiness and LCD init on
  the real device.
- PASS: attended read-only monitor proved continued LCD rendering and heartbeats
  with zero crash/unsafe markers and zero bad render-row lengths.
- GAP: attended monitor did not prove encoder/button interaction because it
  captured zero input events.
- NOT RUN: host simulator, mock, or unit tests, per user instruction.

## Files

- Ignored local evidence directory:
  `research/bench-records/xbee-readonly/local-pf0530o-real-menu-cal-flash-20260601T112737Z/`
- Source/build ledger:
  `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530o-real-menu-cal.md`
- Task record:
  `.agents/TASK_LOG/0129-four-relay-ky040-bbs-lcd-menu-pf0530o-real-menu-calibration.md`
- Hardware QA handoff:
  `.agents/handoffs/0094-four-relay-ky040-bbs-lcd-menu-pf0530o-input-report-to-hardware-qa.md`
- Firmware/project/prompt docs:
  `firmware/projects/four-relay-xbee-wifi/README.md`,
  `docs/projects/four-relay-xbee-wifi/README.md`,
  `docs/projects/espnow-bbs/lcd-encoder-field-console-plan.md`,
  `docs/projects/espnow-bbs/lcd-menu-graphics-browser-agent-plan.md`,
  `docs/projects/four-relay-xbee-wifi/rotary-encoder-menu-plan.md`,
  `docs/prompt/comprehensive-bench-development-process.md`
- Current status records:
  `research/triage-status.md`, `research/known-gaps.md`,
  `research/development-status-ledger.md`
- Source index:
  `knowledge-base/source-index.md`
- Docs index:
  `docs/index.md`

## Authority Limits

This live record proves only the named COM6 PF0530O write/verify/read-only
monitor gate. It does not prove accepted physical encoder/button interaction,
LCD readability by user visual report, XBee/RF writes, ESP-NOW runtime, relay
GPIO writes, relay-expander writes, MicroSD/TFT action, wiring mutation,
DMM/current measurement, relay/load/mains work, erase-flash, persistent config,
external services, GitHub publication, release, commit, or push.
