# Four Relay KY-040 BBS LCD Menu PF0530Q Quiet Calibration

Status: PF0530Q source/build and COM6 write/verify/readiness validated;
physical input acceptance remains pending

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-01

## Routing

- Selected tier: Tier 3 overall, with Tier 2 source/build firmware, tests,
  docs, and evidence-record mutation before COM6 live flash/verify/read-only
  monitor.
- Owner role: Firmware live-gate owner with coordinator, firmware, QA, LCD UX,
  hardware safety, and source-record reviewer lenses.
- Evidence need: prior calibration evidence review, source diff, generated menu
  output, focused tests, scaffold audits, scaffold verification, ESP-IDF v6.0.1
  no-flash build, COM6 identity, rollback backup, artifact hashes, COM6
  write-flash, separate verify-flash, reset boot monitor, read-only idle
  monitor, transcript scan, cleanup proof, and durable task/source/status
  records.
- Mutation boundary: PF0530Q firmware/menu/test/docs/source records plus one
  COM6-only Tier 3 write of the staged PF0530Q bootloader, partition table, and
  app offsets after pre-flash validation. No erase-flash, serial command writes,
  XBee/RF writes or tests, ESP-NOW runtime expansion, relay/load/mains, wiring
  mutation, DMM/current measurement, persistent config, external services,
  release, commit, or push.
- Reviewer disposition: local read-only coordinator, firmware, QA, LCD UX,
  hardware-safety, and source-record lenses approved the named PF0530Q
  source/build/live sequence with no unresolved P1/P2 blockers. Weighted
  disposition was 17/17. Project-local subagents were not spawned because the
  available multi-agent tool metadata required explicit user delegation.
- Tier 3 gate authority: the user first provided the PF0530P-specific gate, then
  clarified that no physical rotation occurred during the PF0530P monitor and
  supplied same-session continuation authority with `safe state confirmed live
  flash approved, continue`.

## Verified Facts

- The user clarified that they did not rotate during the PF0530P attended
  monitor, so the PF0530P zero-input transcript is not diagnostic of a debounce
  failure.
- Prior PF0530L/PF0530N interaction evidence showed the current GPIO interrupt
  plus software quadrature path can capture raw A/B events, decoded menu steps,
  and button selects during physical actuation.
- Prior calibration transcripts showed dense raw A/B bursts and invalid
  transitions, including multiple raw transitions within the same millisecond.
- PF0530Q changes the active firmware ID and generated menu metadata to
  `PF0530Q`.
- GPIO13/GPIO14/GPIO32 remain input-only with pullups; LCD GPIO21/GPIO22 remain
  display-only; `FR_DIAG_XBEE_BRIDGE_CLOSED 1` remains set.
- PF0530Q keeps one transition per menu step, two A/B stable samples, a 5 ms
  A/B candidate hold, 30 ms switch debounce, 75 ms switch guard, and 650 ms
  long press.
- PF0530Q adds `FR_ENCODER_AB_QUIET_MS 10`, changes step lockout to 60 ms, and
  accepts stable A/B updates through a combined two-bit pair filter.
- PF0530Q adds `cal=quiet-v3`, `quiet_ms=10`, `ENC_FILTER reason=ab_quiet`,
  raw A/B edge-gap telemetry, raw burst counters, A/B quiet-hold counters, and
  heartbeat raw-burst/gap fields.
- PF0530Q does not add double-click behavior and does not change
  `bbs_lcd_menu.v1` or `bbs_lcd_render.v2` schemas.
- COM6 was rechecked through Windows esptool before programming as an ESP32
  target with 4 MB detected flash and 3.3 V flash-voltage strap evidence.
- A full 4 MB rollback backup was captured before programming; the exact path,
  recovery command, and rollback SHA-256 are retained in ignored local evidence.
- The staged PF0530Q bootloader, partition table, and app artifacts matched the
  source/build artifact hashes below before programming.
- Windows esptool `write-flash` completed on COM6 for the PF0530Q bootloader,
  partition table, and app offsets with per-segment hash verification.
- A separate Windows esptool `verify-flash` pass matched all three PF0530Q
  artifacts.
- The reset boot read-only monitor captured `LCD_INIT_OK addr=0x27`,
  `PF0530Q BBS_LCD_READY`, `PF0530Q BBS_INPUT_READY`, `cal=quiet-v3`,
  `ab_ms=5`, `quiet_ms=10`, `step_lockout_ms=60`, 14 `BBS_MENU_HB`, 14
  `BBS_LCD_RENDER`, 14 `BBS_CURSOR`, one `BBS_GLYPH_BANK`, and zero crash/
  unsafe markers.
- The 60 second idle read-only monitor captured 30 `BBS_MENU_HB`, 30
  `BBS_LCD_RENDER`, 30 `BBS_CURSOR`, zero bad 20-character render-row lengths,
  zero crash/unsafe markers, and zero input events with
  `physical_actuation_expected=false`.
- The combined transcript scan reported `readiness_ok: true`,
  `interaction_ok: false`, `no_crash_or_unsafe: true`, and zero bad render-row
  lengths.
- Linux and Windows cleanup checks found no lingering COM6/esptool/PF0530Q
  monitor process after the run.

## Assumptions

- PF0530Q is an inferred calibration candidate for KY-040 LCD-menu user
  testing, not proof of accepted physical interaction.
- PCNT, `espressif/knob`, and `espressif/button` remain deferred until live
  evidence proves raw A/B events exist but software decoding is the failure.
- COM6 identity must be rechecked before flash; rollback and separate
  verify-flash evidence must exist before any live acceptance claim.

## Unknowns

- Exact current physical encoder bounce timing.
- Physical direction, one-detent behavior, quick-rotation behavior, short
  press, long press, and LCD response under PF0530Q.
- Whether PF0530Q quiet-window filtering improves the user-visible input
  behavior during actual physical actuation.

## Validation

- PASS: focused Python unit tests:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (`Ran 30 tests in 0.138s`)
- PASS: generated menu freshness check:
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: firmware scaffold audit:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: touched comprehensive bench-process test:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_comprehensive_bench_process`
  (`Ran 3 tests in 0.022s`)
- PASS: scaffold verification:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
  (`PASS: ESP32 scaffold validation succeeded`)
- PASS: ESP-IDF v6.0.1 no-flash build:
  `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-pf0530q-quiet-cal-build build`
  - App image: `/tmp/esp32-pf0530q-quiet-cal-build/four_relay_xbee_wifi.bin`
  - App size: `0x2d7c0`; free in 1 MiB app partition: `0xd2840` (`82%`)
  - Bootloader size: `0x6610`; free before partition table: `0x9f0` (`9%`)
- PASS: pre-flash `git diff --check`.
- PASS: same-session COM6 identity, flash-size, and flash-voltage strap
  evidence captured before write.
- PASS: full 4 MB rollback backup captured before programming; recovery command
  retained in ignored local evidence.
- PASS: staged PF0530Q artifact hashes pinned before programming.
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

## Build Artifacts

- Bootloader SHA-256:
  `<redacted-sha256>`
- Partition table SHA-256:
  `<redacted-sha256>`
- App SHA-256:
  `<redacted-sha256>`

## Files

- `firmware/projects/four-relay-xbee-wifi/main/main.c`
- `firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h`
- `firmware/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/four-relay-xbee-wifi/rotary-encoder-menu-plan.md`
- `docs/projects/espnow-bbs/lcd-encoder-field-console-plan.md`
- `docs/prompt/comprehensive-bench-development-process.md`
- `research/triage-status.md`
- `research/known-gaps.md`
- `research/development-status-ledger.md`
- `tools/simulators/lcd_bbs_menu/bbs_lcd_menu.v1.xml`
- `tools/simulators/lcd_bbs_menu/generate_lcd_menu.py`
- `tools/simulators/lcd_bbs_menu/generated_menu.py`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py`
- `tests/scaffold_audits/test_comprehensive_bench_process.py`
- `scripts/scaffold_audit_firmware.py`
- `knowledge-base/source-index.md`
- `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530q-quiet-cal.md`
- `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530q-live.md`
- `.agents/handoffs/0096-four-relay-ky040-bbs-lcd-menu-pf0530q-input-report-to-hardware-qa.md`
- `docs/index.md`
- Ignored local evidence directory:
  `<redacted-local-evidence-dir>/`

## Next Gate

Collect the user visual report for PF0530Q. Physical input acceptance needs a
fresh read-only interaction monitor with actual actuation and evidence of
`ENC_RAW`, `ENC_EV`, `BBS_MENU_STEP` in both directions, short and long
`BBS_MENU_SELECT`, readable LCD response, and zero crash/unsafe markers.

## Decision Footer

Decision: `flashed_verified_readiness_pass_input_unaccepted`. Next gate: user
visual report, then a fresh read-only physical-interaction monitor only if
physical input acceptance is requested. Owner: Firmware live-gate owner with
Hardware QA and Evidence Records. Evidence: reviewer lenses, PF0530Q source
diff, generated XML outputs, source/build/live records, focused unit tests,
scaffold audits, scaffold verification, no-flash ESP-IDF build, artifact
hashes, COM6 identity, rollback, write-flash, separate verify-flash, read-only
reset boot monitor, read-only idle monitor, transcript scan, cleanup proof, and
`git diff --check`. Approved mutation boundary: completed PF0530Q source/build
firmware/menu/tests/docs/records plus one COM6-only PF0530Q write/verify/
read-only monitor gate. Authority limits: no further flash, monitor, serial
writes, XBee/RF, relay/load/mains, wiring, DMM/current, erase, persistent
config, external services, release, commit, or push.
