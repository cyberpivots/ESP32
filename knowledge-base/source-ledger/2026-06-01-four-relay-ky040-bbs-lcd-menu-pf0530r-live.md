# Four Relay KY-040 BBS LCD Menu PF0530R Live Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530R-LIVE-2026-06-01`

## Verified Facts

- The user supplied same-session PF0530R live authority with:
  `PF0530R-specific COM6 Tier 3 flash gate`, `SAFE STATE CONFIRMED`, and
  `LIVE FLASH APPROVED`.
- Local read-only coordinator, firmware, QA, LCD UX, hardware-safety, and
  source-record lenses approved the named PF0530R COM6 write/verify/read-only
  monitor boundary with no unresolved P1/P2 blockers. Weighted disposition was
  17/17. Subagents were not spawned because available multi-agent tool metadata
  required explicit user delegation.
- Same-session pre-flash checks passed: focused LCD/encoder tests,
  comprehensive bench-process test, generated-menu freshness check, firmware
  scaffold audit, scaffold verification, `git diff --check`, and ESP-IDF
  v6.0.1 no-flash build.
- COM6 was rechecked through Windows esptool before programming as an ESP32
  target with MAC `<redacted-mac>`, 4 MB detected flash, and 3.3 V
  flash-voltage strap evidence.
- A full 4 MB pre-PF0530R rollback backup was captured before programming.
  The exact path, recovery command, and rollback SHA-256 are retained in
  ignored local evidence.
- PF0530R artifacts were built with ESP-IDF v6.0.1, copied into ignored local
  evidence, and pinned before programming:
  - bootloader:
    `<redacted-sha256>`
  - partition table:
    `<redacted-sha256>`
  - app:
    `<redacted-sha256>`
- Windows esptool `write-flash` completed for the PF0530R bootloader,
  partition table, and app offsets, with per-segment hash verification.
- A separate Windows esptool `verify-flash` pass matched all three PF0530R
  artifacts.
- The reset boot monitor used no serial byte writes and captured:
  `LCD_INIT_OK addr=0x27`, `PF0530R BBS_LCD_READY`,
  `PF0530R BBS_INPUT_READY`, `cal=detent-v4`, `ab_ms=8`, `quiet_ms=15`,
  `step_lockout_ms=90`, `detent=3`, 14 `BBS_MENU_HB`, 14 `BBS_LCD_RENDER`,
  14 `BBS_CURSOR`, one `BBS_GLYPH_BANK`, zero crash markers, and zero unsafe
  markers.
- The 150 second attended read-only monitor used `writes_sent=false` and
  `physical_actuation_expected=true`; it captured continued heartbeat/render
  output, zero bad render-row lengths, zero crash markers, and zero unsafe
  markers.
- The combined transcript scan reported `readiness_ok: true`,
  `interaction_ok: false`, `no_crash_or_unsafe: true`,
  `render_rows_ok: true`, `serial_write_free: true`, and
  `attended_monitor_complete: true`.
- The combined transcript captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, zero `BBS_MENU_SELECT`, and zero `ENC_FILTER` lines.
  Therefore PF0530R physical encoder/button behavior is not accepted by this
  run.
- Linux and Windows cleanup checks found no lingering COM6/esptool/PF0530R
  monitor process after the run.

## Assumptions

- COM6 remained connected to the intended ESP32 target during the full
  write/verify/monitor sequence.
- The attended monitor did not capture physical actuation; its zero-input
  counts prove only readiness and idle stability, not encoder stability.
- PF0530R should remain the current written image for the next operator visual
  and input report unless a later gate changes it.

## Unknowns

- Physical encoder direction, one-detent behavior, fast rotation behavior,
  short-button behavior, long-button behavior, and LCD response under actual
  PF0530R actuation remain unaccepted.
- Whether PF0530R detent gating improves the user-reported PF0530Q instability
  remains unknown until actuation evidence or a user report exists.

## Validation

- PASS: pre-flash focused firmware/LCD tests.
- PASS: pre-flash comprehensive bench-process test.
- PASS: pre-flash generated menu freshness check.
- PASS: pre-flash firmware scaffold audit.
- PASS: pre-flash scaffold verification.
- PASS: pre-flash ESP-IDF v6.0.1 no-flash build.
- PASS: pre-flash `git diff --check`.
- PASS: same-session COM6 identity, flash-size, and flash-voltage strap
  evidence captured before write.
- PASS: full 4 MB rollback backup captured before programming; recovery
  command retained in ignored local evidence.
- PASS: PF0530R artifact hashes pinned before programming.
- PASS: Windows esptool write-flash completed on COM6 for the PF0530R
  bootloader, partition table, and app image.
- PASS: separate Windows esptool verify-flash matched all three PF0530R
  artifacts.
- PASS: reset boot monitor proved PF0530R runtime readiness, LCD init on
  address `0x27`, detent-v4 input metadata, and no serial byte writes.
- PASS: 150 second attended read-only monitor completed with continued LCD
  rendering and heartbeats, zero crash/unsafe markers, and zero bad render-row
  lengths.
- PASS: transcript scan reported readiness OK, render rows OK, no crash/unsafe
  markers, serial-write-free monitor proof, and complete attended monitor.
- GAP: physical encoder/button interaction remains unaccepted because the live
  transcript captured zero `ENC_RAW`, zero `ENC_EV`, zero `BBS_MENU_STEP`, zero
  `BBS_MENU_SELECT`, and zero `ENC_FILTER`.
- PASS: Linux and Windows cleanup checks found no lingering COM6/esptool/PF0530R
  monitor process.

## Files

- Ignored local evidence directory:
  `<redacted-local-evidence-dir>/`
- Source/build ledger:
  `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530r-detent-cal.md`
- Task record:
  `.agents/TASK_LOG/0133-four-relay-ky040-bbs-lcd-menu-pf0530r-detent-calibration.md`
- Hardware QA handoff:
  `.agents/handoffs/0097-four-relay-ky040-bbs-lcd-menu-pf0530r-to-hardware-qa.md`
- Current status records:
  `research/triage-status.md`, `research/known-gaps.md`,
  `research/development-status-ledger.md`
- Source index:
  `knowledge-base/source-index.md`
- Docs index:
  `docs/index.md`

## Authority Limits

This live record proves only the named COM6 PF0530R write/verify/read-only
monitor gate. It does not prove accepted physical encoder/button interaction,
LCD readability by user visual report, XBee/RF writes, ESP-NOW runtime, relay
GPIO writes, relay-expander writes, MicroSD/TFT action, wiring mutation,
DMM/current measurement, relay/load/mains work, erase-flash, persistent config,
external services, GitHub publication, release, commit, or push.
