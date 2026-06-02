# Four Relay KY-040 BBS LCD Menu PF0530Q Live Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530Q-LIVE-2026-06-01`

## Verified Facts

- The user supplied same-session continuation authority with `safe state
  confirmed live flash approved, continue` after clarifying they did not rotate
  during the PF0530P monitor.
- Local read-only coordinator, firmware, QA, LCD UX, hardware-safety, and
  source-record lenses approved the named PF0530Q source/build/live sequence
  with no unresolved P1/P2 blockers. Weighted disposition was 17/17. Subagents
  were not spawned because available multi-agent tool metadata required
  explicit user delegation.
- COM6 was rechecked through Windows esptool before programming as an ESP32
  target with MAC `<redacted-mac>`, 4 MB detected flash, and 3.3 V
  flash-voltage strap evidence.
- A full 4 MB rollback backup was captured before programming. The exact path,
  recovery command, and rollback SHA-256 are retained in ignored local
  evidence.
- PF0530Q artifacts were built with ESP-IDF v6.0.1, copied into the ignored
  local evidence directory, and pinned before programming:
  - bootloader:
    `<redacted-sha256>`
  - partition table:
    `<redacted-sha256>`
  - app:
    `<redacted-sha256>`
- Windows esptool `write-flash` completed for the PF0530Q bootloader,
  partition table, and app offsets, with per-segment hash verification.
- A separate Windows esptool `verify-flash` pass matched all three PF0530Q
  artifacts.
- The reset boot monitor used no serial byte writes and captured:
  `LCD_INIT_OK addr=0x27`, `PF0530Q BBS_LCD_READY`,
  `PF0530Q BBS_INPUT_READY`, `cal=quiet-v3`, `ab_ms=5`, `quiet_ms=10`,
  `step_lockout_ms=60`, 14 `BBS_MENU_HB`, 14 `BBS_LCD_RENDER`, 14
  `BBS_CURSOR`, one `BBS_GLYPH_BANK`, zero crash markers, and zero unsafe
  markers.
- The 60 second idle read-only monitor used `writes_sent=false` and
  `physical_actuation_expected=false`, captured 30 `BBS_MENU_HB`, 30
  `BBS_LCD_RENDER`, 30 `BBS_CURSOR`, zero crash markers, zero unsafe markers,
  and zero bad 20-character render row lengths.
- The combined transcript scan reported `readiness_ok: true`,
  `interaction_ok: false`, `no_crash_or_unsafe: true`, and zero bad render-row
  lengths.
- The combined transcript captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, zero `BBS_MENU_SELECT`, and zero `ENC_FILTER` lines. This is
  expected for the no-actuation idle monitor and is not a physical input
  acceptance result.
- Linux and Windows cleanup checks found no lingering COM6/esptool/PF0530Q
  monitor process after the run.

## Assumptions

- COM6 remained connected to the intended ESP32 target during the full
  write/verify/monitor sequence.
- The idle monitor intentionally did not ask for physical encoder/button
  actuation, matching the user's instruction to proceed from inferred
  calibration changes instead of the prior user-cue method.
- Physical interaction acceptance still requires a later live transcript with
  actual encoder/button actuation and a user visual report.

## Unknowns

- Physical encoder direction, one-detent behavior, quick-rotation behavior,
  short-button behavior, long-button behavior, and LCD response under PF0530Q
  remain unaccepted.
- Whether PF0530Q quiet-window filtering improves user-visible behavior remains
  unknown until actuation evidence exists.

## Validation

- PASS: ESP-IDF v6.0.1 no-flash build.
- PASS: pre-flash focused firmware/LCD tests.
- PASS: generated menu freshness check.
- PASS: firmware scaffold audit.
- PASS: scaffold verification.
- PASS: pre-flash `git diff --check`.
- PASS: same-session COM6 identity, flash-size, and flash-voltage strap
  evidence captured before write.
- PASS: full 4 MB rollback backup captured before programming; recovery command
  retained in ignored local evidence.
- PASS: PF0530Q artifact hashes pinned before programming.
- PASS: Windows esptool write-flash completed on COM6 for the PF0530Q
  bootloader, partition table, and app image.
- PASS: separate Windows esptool verify-flash matched all three PF0530Q
  artifacts.
- PASS: reset boot monitor proved PF0530Q runtime readiness, LCD init on
  address 0x27, and quiet-v3 input metadata with no serial byte writes.
- PASS: 60 second idle read-only monitor proved continued LCD rendering and
  heartbeats with zero crash/unsafe markers and zero bad render-row lengths.
- PASS: transcript scan reported readiness OK and no crash/unsafe markers.
- PASS: Linux and Windows cleanup checks found no lingering COM6/esptool/PF0530Q
  monitor process.
- GAP: physical encoder/button interaction remains unaccepted because the live
  monitor intentionally did not include physical actuation.
- PASS: final post-record focused tests:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (`Ran 30 tests in 0.185s`)
- PASS: final post-record comprehensive bench-process test:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_comprehensive_bench_process`
  (`Ran 3 tests in 0.020s`)
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
  `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530q-quiet-cal.md`
- Task record:
  `.agents/TASK_LOG/0132-four-relay-ky040-bbs-lcd-menu-pf0530q-quiet-calibration.md`
- Hardware QA handoff:
  `.agents/handoffs/0096-four-relay-ky040-bbs-lcd-menu-pf0530q-input-report-to-hardware-qa.md`
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

This live record proves only the named COM6 PF0530Q write/verify/read-only
monitor gate. It does not prove accepted physical encoder/button interaction,
LCD readability by user visual report, XBee/RF writes, ESP-NOW runtime, relay
GPIO writes, relay-expander writes, MicroSD/TFT action, wiring mutation,
DMM/current measurement, relay/load/mains work, erase-flash, persistent config,
external services, GitHub publication, release, commit, or push.
