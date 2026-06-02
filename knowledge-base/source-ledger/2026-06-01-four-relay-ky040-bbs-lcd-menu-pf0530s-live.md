# Four Relay KY-040 BBS LCD Menu PF0530S Live Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530S-LIVE-2026-06-01`

Date: 2026-06-01 local, evidence captured 2026-06-02 UTC

## Scope

This ledger records the user-authorized PF0530S COM6 live gate after the
PF0530R attended monitor captured zero input events. PF0530S was built to prove
raw GPIO liveness first while preserving the closed bridge, relay, RF, wiring,
DMM/current, load/mains, erase, persistent-config, commit, and push surfaces.

## Verified Facts

- The supplied continuation plan records the user's same-session PF0530S COM6
  authority with `SAFE STATE IS CONFIRMED` and `LIVE FLASH APPROVED`.
- Local coordinator, firmware, QA, LCD UX, hardware-safety, and evidence-record
  lenses approved the named PF0530S boundary with no unresolved P1/P2 blockers.
  Weighted disposition was 15/15. Subagents were not spawned because the
  available multi-agent tool metadata required explicit user delegation and no
  lifecycle list was exposed for cleanup.
- Same-session pre-flash checks passed: focused LCD/encoder tests, generated
  menu freshness check, firmware scaffold audit, scaffold verification,
  ESP-IDF v6.0.1 no-flash build, and `git diff --check`.
- COM6 was checked through Windows inventory and Windows esptool as a Silicon
  Labs CP210x USB to UART Bridge on COM6 attached to an ESP32-D0WDQ6 revision
  v1.0 target. The full MAC and exact local evidence path are retained only in
  ignored local evidence.
- Esptool reported 4 MB flash and 3.3 V flash-voltage strap evidence.
- A full 4 MB pre-PF0530S rollback backup was captured before programming.
  Rollback hash and recovery command are retained in ignored local evidence.
- PF0530S artifacts were built with ESP-IDF v6.0.1, copied into ignored local
  evidence, and pinned before programming:
  - bootloader:
    `<redacted-sha256>`
  - partition table:
    `<redacted-sha256>`
  - app:
    `<redacted-sha256>`
- Windows esptool `write-flash` completed for the PF0530S bootloader at
  `0x1000`, partition table at `0x8000`, and app at `0x10000`, with per-segment
  hash verification.
- A separate Windows esptool `verify-flash` pass matched all three PF0530S
  artifacts.
- The reset boot monitor used no serial byte writes and captured `PF0530S`,
  `LCD_INIT_OK`, `BBS_LCD_READY`, `BBS_INPUT_READY`, `cal=raw-live-v5`,
  `ENC_BASE`, `ENC_GPIO_CONFIG` for GPIO13/GPIO14/GPIO32, ESP-IDF GPIO config
  dump start, 33 `ENC_LEVEL_HB` lines, and zero crash/unsafe markers.
- The 150 second attended read-only monitor used `writes_sent=false` and
  captured 146 `ENC_LEVEL_HB`, 450 `ENC_RAW kind=ab`, 84 `ENC_RAW kind=sw`,
  `ENC_EV` counts on GPIO13/GPIO14/GPIO32, 27 clockwise menu steps, 21
  counterclockwise menu steps, 18 `BBS_MENU_SELECT`, 14 short selects, and 4
  long selects.
- The attended transcript proved visible LCD/menu response through
  `BBS_LCD_RENDER` and `BBS_CURSOR` movement while menu pages and detail rows
  changed.
- The reset and attended transcripts captured zero `Guru Meditation`,
  `Backtrace`, `panic`, `abort`, `Brownout`, `WDT`, and `LCD_INIT_FAIL`
  markers.
- Linux and Windows cleanup checks found no lingering COM6/esptool/PF0530S
  monitor process after the run.

## Assumptions

- COM6 remained connected to the intended ESP32 target for the full identity,
  rollback, write, verify, reset monitor, and attended monitor sequence.
- The attended cue sequence was applied during the 150 second read-only
  monitor.
- PCNT, `espressif/knob`, and `espressif/button` remain comparison references
  until custom decoder stability work needs a different implementation path.

## Unknowns

- PF0530S proves raw liveness, but full rotary stability remains open.
- The attended scan recorded 15 invalid transitions, 31 A/B suppressions, five
  step-lockout filters, and final heartbeat `queue_drop=57`.
- Longer mixed-speed operation may still require queue depth, debounce,
  lockout, or decoder tuning.

## Validation

- PASS: focused LCD/encoder unittest suite:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.lcd_bbs_menu.test_lcd_bbs_menu`
- PASS: generated menu freshness check:
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: firmware scaffold audit:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: scaffold verification:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: ESP-IDF v6.0.1 no-flash build:
  `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-pf0530s-raw-live-build build`
- PASS: pre-flash `git diff --check`.
- PASS: COM6 identity, flash-size, and flash-voltage strap evidence captured.
- PASS: full 4 MB rollback backup captured before programming.
- PASS: PF0530S artifact hashes pinned before programming.
- PASS: COM6 write-flash completed for bootloader, partition table, and app.
- PASS: separate COM6 verify-flash matched bootloader, partition table, and
  app.
- PASS: reset boot monitor proved PF0530S readiness, raw-live-v5 metadata,
  baseline/config/heartbeat telemetry, no serial byte writes, and no
  crash/unsafe markers.
- PASS: attended read-only monitor proved raw A/B and switch liveness, both
  menu directions, short selects, long selects, visible menu response, no
  serial byte writes, and no crash/unsafe markers.
- GAP: full rotary stability remains open because the transcript also captured
  invalid/suppressed transitions and queue drops.
- PASS: Linux and Windows cleanup checks found no lingering COM6/esptool/PF0530S
  monitor process.

## Files

- Ignored local evidence directory:
  `<redacted-local-evidence-dir>/`
- Evidence manifest:
  `<redacted-local-evidence-dir>/evidence-manifest.md`
- Source/build ledger:
  `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530s-raw-liveness-cal.md`
- Task record:
  `.agents/TASK_LOG/0134-four-relay-ky040-bbs-lcd-menu-pf0530s-raw-liveness.md`
- Hardware QA handoff:
  `.agents/handoffs/0098-four-relay-ky040-bbs-lcd-menu-pf0530s-to-hardware-qa.md`
- Current status records:
  `research/triage-status.md`, `research/known-gaps.md`,
  `research/development-status-ledger.md`
- Source index:
  `knowledge-base/source-index.md`
- Docs index:
  `docs/index.md`

## Authority Limits

This live record proves only the named COM6 PF0530S identity, rollback,
write-flash, separate verify-flash, reset monitor, attended read-only monitor,
and cleanup gate. It does not prove or authorize XBee/RF writes or tests,
ESP-NOW runtime expansion, relay GPIO writes, relay-expander writes,
MicroSD/TFT action, wiring mutation, DMM/current measurement, relay/load/mains
work, erase-flash, persistent config mutation, external services, GitHub
publication, release, commit, or push.
