# Four Relay KY-040 BBS LCD Menu PF0530P Live Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530P-LIVE-2026-06-01`

## Verified Facts

- The user explicitly authorized the same-session live gate with
  `SAFE STATE VERIFIED for COM6 PF0530P flash` and
  `Allow flash on COM6 for PF0530P encoder debounce calibration`.
- Read-only coordinator, live-bench, hardware safety, QA, and LCD UX reviewer
  lenses approved the named COM6-only PF0530P flash/verify/read-only monitor
  boundary with no unresolved P1/P2 blockers after rollback evidence was
  captured; all live-gate reviewers were closed after output capture.
- COM6 was rechecked through Windows esptool before programming as an ESP32
  target with MAC `<redacted-mac>`, 4 MB detected flash, and 3.3 V
  flash-voltage strap evidence.
- A full 4 MB rollback backup was captured before programming. The exact path,
  recovery command, and rollback SHA-256 are retained in ignored local
  evidence.
- PF0530P artifacts were built with ESP-IDF v6.0.1, copied into the ignored
  local evidence directory, and pinned before programming:
  - bootloader:
    `<redacted-sha256>`
  - partition table:
    `<redacted-sha256>`
  - app:
    `<redacted-sha256>`
- Windows esptool `write-flash` completed for the PF0530P bootloader,
  partition table, and app offsets, with per-segment hash verification.
- A separate Windows esptool `verify-flash` pass matched all three PF0530P
  artifacts.
- The reset boot monitor used no serial byte writes and captured:
  `LCD_INIT_OK addr=0x27`, `PF0530P BBS_LCD_READY`,
  `PF0530P BBS_INPUT_READY`, `cal=debounce-v2`, `ab_ms=5`,
  `step_lockout_ms=40`, 14 `BBS_MENU_HB`, 14 `BBS_LCD_RENDER`, 14
  `BBS_CURSOR`, one `BBS_GLYPH_BANK`, zero crash markers, and zero unsafe
  markers.
- The attended 150 second read-only monitor used `writes_sent=false`, captured
  75 `BBS_MENU_HB`, 75 `BBS_LCD_RENDER`, 75 `BBS_CURSOR`, zero crash markers,
  zero unsafe markers, and zero bad 20-character render row lengths.
- The attended monitor captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, zero `BBS_MENU_SELECT`, and zero `ENC_FILTER` lines.
- The combined transcript scan reported `readiness_ok: true`,
  `interaction_ok: false`, `no_crash_or_unsafe: true`, and zero bad render-row
  lengths.
- Linux and Windows cleanup checks found no lingering COM6/esptool/Python
  monitor process after the run.

## Assumptions

- COM6 remained connected to the intended ESP32 target during the full
  write/verify/monitor sequence.
- The attended monitor cues were delivered to the operator, but physical
  actuation must be confirmed by the user before treating the zero input events
  as a hardware/input-capture failure rather than a missed interaction window.
- If the user confirms they rotated or pressed during the window, the next
  troubleshooting lane is physical/input capture evidence on
  GPIO13/GPIO14/GPIO32 before more debounce or transitions-per-step tuning.

## Unknowns

- User visual report for the PF0530P LCD menu after flash is still pending.
- Whether physical encoder/button actuation occurred during the 150 second
  attended monitor is not confirmed in this record.
- Physical encoder direction, one-detent behavior, quick-rotation behavior,
  short-button behavior, and long-button behavior remain unaccepted because the
  attended transcript captured no input events.

## Validation

- PASS: `git diff --check` before live gate and final record update.
- PASS: ESP-IDF v6.0.1 no-flash build.
- PASS: full rollback backup captured before programming.
- PASS: PF0530P artifact hashes pinned before programming.
- PASS: Windows esptool write-flash completed on COM6 for the PF0530P
  bootloader, partition table, and app image.
- PASS: separate Windows esptool verify-flash matched all three PF0530P
  artifacts.
- PASS: reset boot monitor proved PF0530P runtime readiness, LCD init on
  address 0x27, and debounce-v2 input metadata with no serial byte writes.
- PASS: attended read-only monitor proved continued LCD rendering and
  heartbeats with zero crash/unsafe markers and zero bad render-row lengths.
- GAP: attended monitor did not prove encoder/button interaction because it
  captured zero input events.
- PASS: final post-record focused tests:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_comprehensive_bench_process`
  (`Ran 3 tests in 0.013s`)
- PASS: final post-record firmware/LCD tests:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (`Ran 30 tests in 0.150s`)
- PASS: final post-record generated menu freshness check:
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: final post-record firmware scaffold audit:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: final post-record scaffold verification:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
  (`PASS: ESP32 scaffold validation succeeded`)
- PASS: final post-record `git diff --check`.

## Files

- Ignored local evidence directory:
  `<redacted-local-evidence-dir>/`
- Source/build ledger:
  `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530p-debounce-cal.md`
- Task record:
  `.agents/TASK_LOG/0131-four-relay-ky040-bbs-lcd-menu-pf0530p-debounce-calibration.md`
- Hardware QA handoff:
  `.agents/handoffs/0095-four-relay-ky040-bbs-lcd-menu-pf0530p-input-report-to-hardware-qa.md`
- Firmware/project/prompt docs:
  `firmware/projects/four-relay-xbee-wifi/README.md`,
  `docs/projects/four-relay-xbee-wifi/README.md`,
  `docs/projects/espnow-bbs/lcd-encoder-field-console-plan.md`,
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

This live record proves only the named COM6 PF0530P write/verify/read-only
monitor gate. It does not prove accepted physical encoder/button interaction,
LCD readability by user visual report, XBee/RF writes, ESP-NOW runtime, relay
GPIO writes, relay-expander writes, MicroSD/TFT action, wiring mutation,
DMM/current measurement, relay/load/mains work, erase-flash, persistent config,
external services, GitHub publication, release, commit, or push.
