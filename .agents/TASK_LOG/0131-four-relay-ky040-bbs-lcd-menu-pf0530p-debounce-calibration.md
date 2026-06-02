# Four Relay KY-040 BBS LCD Menu PF0530P Debounce Calibration

Status: PF0530P source/build and COM6 write/verify/readiness validated; input
interaction gap remains

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-01

## Routing

- Selected tier: Tier 2 source/build firmware, tests, docs, and evidence-record
  mutation, then Tier 3 COM6 write/verify/read-only monitor after the user
  supplied the exact same-session gate phrases.
- Owner role: Firmware live-gate owner with coordinator/agent-ops, hardware
  safety, QA, LCD UX, and source-research reviewer lenses.
- Evidence need: current PF0530O source/live record review, read-only reviewer
  quorum, source diff, generated menu output, focused tests, scaffold audits,
  ESP-IDF v6.0.1 no-flash build, COM6 identity, rollback backup, artifact
  hashes, COM6 write-flash, separate verify-flash, reset boot monitor, attended
  read-only monitor, transcript scan, cleanup proof, and durable
  task/source/status records.
- Mutation boundary: PF0530P firmware/menu/test/docs/source records plus one
  COM6-only Tier 3 write of the staged PF0530P bootloader, partition table,
  and app offsets, followed by separate verify-flash and read-only monitors.
  No erase-flash, serial command writes, XBee/RF, ESP-NOW runtime expansion,
  relay/load/mains, wiring mutation, DMM/current measurement, persistent
  config, external services, release, commit, or push.
- Reviewer disposition: read-only coordinator, firmware, QA, LCD UX, and
  source-research agents returned conditional approval with no P1/P2 blockers.
  Weighted disposition meets the 70 percent threshold for the named Tier 2
  source/build boundary. Lifecycle state was not listable before spawning;
  completed reviewer output was captured and all five agents were closed before
  mutation records were finalized.
- Tier 3 gate authority: the user provided
  `SAFE STATE VERIFIED for COM6 PF0530P flash` and
  `Allow flash on COM6 for PF0530P encoder debounce calibration`.
- Tier 3 reviewer disposition: coordinator, live-bench, hardware safety, QA,
  and LCD UX reviewers returned conditional approval for the named COM6-only
  PF0530P gate with no unresolved P1/P2 blockers after rollback evidence was
  captured. All live-gate reviewers were closed after output capture.

## Verified Facts

- PF0530O live records show COM6 write/verify/read-only LCD readiness/render/
  heartbeat proof with zero captured input events; that is an evidence gap, not
  proof of a debounce failure.
- PF0530P changes the active firmware ID and generated menu metadata to
  `PF0530P`.
- GPIO13/GPIO14/GPIO32 remain input-only with pullups; LCD GPIO21/GPIO22 remain
  display-only; `FR_DIAG_XBEE_BRIDGE_CLOSED 1` remains set.
- PF0530P adds `FR_ENCODER_AB_DEBOUNCE_MS 5` and
  `FR_ENCODER_STEP_LOCKOUT_MS 40`.
- PF0530P keeps one transition per menu step, two AB stable samples, 30 ms
  switch debounce, 75 ms switch guard, and 650 ms long press.
- PF0530P adds `ENC_FILTER` telemetry for `ab_debounce`, `step_lockout`,
  `invalid`, and `sw_guard`; appends held time to `BBS_MENU_SELECT`; and adds
  heartbeat counters for debounce holds, accepted stable A/B transitions, step
  lockouts, invalid transitions, suppressed transitions, and queue drops.
- PF0530P does not add double-click behavior and does not change
  `bbs_lcd_menu.v1` or `bbs_lcd_render.v2`.
- COM6 was rechecked through Windows esptool before programming as an ESP32
  target with 4 MB detected flash and 3.3 V flash-voltage strap evidence.
- A full 4 MB rollback backup was captured before programming; the exact path
  and rollback SHA-256 are retained in ignored local evidence.
- The staged PF0530P bootloader, partition table, and app artifacts matched the
  source/build artifact hashes below before programming.
- Windows esptool `write-flash` completed on COM6 for the PF0530P bootloader,
  partition table, and app offsets with per-segment hash verification.
- A separate Windows esptool `verify-flash` pass matched all three PF0530P
  artifacts.
- The reset boot read-only monitor captured `LCD_INIT_OK addr=0x27`,
  `PF0530P BBS_LCD_READY`, `PF0530P BBS_INPUT_READY`, `cal=debounce-v2`,
  `ab_ms=5`, `step_lockout_ms=40`, 14 `BBS_MENU_HB`, 14 `BBS_LCD_RENDER`, 14
  `BBS_CURSOR`, one `BBS_GLYPH_BANK`, and zero crash/unsafe markers.
- The attended 150 second read-only monitor captured 75 `BBS_MENU_HB`, 75
  `BBS_LCD_RENDER`, 75 `BBS_CURSOR`, zero bad 20-character render-row lengths,
  zero crash/unsafe markers, and zero `ENC_RAW`, `ENC_EV`, `BBS_MENU_STEP`, or
  `BBS_MENU_SELECT` lines.
- Linux and Windows cleanup checks found no lingering COM6/esptool/Python
  monitor process after the run.

## Assumptions

- The 5 ms A/B candidate hold and 40 ms step lockout are calibration candidates
  for future user testing, not accepted physical behavior.
- PCNT, `espressif/knob`, and `espressif/button` remain deferred until live
  evidence proves the current software path is the failure after raw A/B events
  are present.
- The attended monitor cue sequence was announced, but physical actuation must
  be confirmed by the user before treating zero input events as a hardware or
  input-capture failure.
- Future COM6 live actions need a fresh Tier 3 gate; the completed authority
  applies only to the PF0530P COM6 flash/verify/read-only monitor run recorded
  here.

## Unknowns

- Whether physical actuation occurred during the PF0530O attended monitor.
- Whether physical actuation occurred during the PF0530P attended monitor.
- User visual report for the PF0530P LCD menu after flash is still pending.
- Physical direction, one-detent behavior, quick rotation, short press, long
  press, and LCD response under PF0530P remain unaccepted because the attended
  transcript captured no input events.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (`Ran 30 tests in 0.181s`)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_comprehensive_bench_process`
  (`Ran 3 tests in 0.011s`)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-pf0530p-debounce-cal-build build`
  - App image: `/tmp/esp32-pf0530p-debounce-cal-build/four_relay_xbee_wifi.bin`
  - App size: `0x2d690`; free in 1 MiB app partition: `0xd2970` (`82%`)
  - Bootloader size: `0x6610`; free before partition table: `0x9f0` (`9%`)
- PASS: `git diff --check`
- PASS: same-session COM6 identity, flash-size, and flash-voltage strap
  evidence captured before write.
- PASS: full 4 MB rollback backup captured before programming; recovery command
  retained in ignored local evidence.
- PASS: staged PF0530P artifact hashes pinned before programming.
- PASS: Windows esptool write-flash completed on COM6 for the PF0530P
  bootloader, partition table, and app image.
- PASS: separate Windows esptool verify-flash matched all three PF0530P
  artifacts.
- PASS: reset boot monitor proved PF0530P runtime readiness, LCD init on
  address 0x27, and debounce-v2 input metadata with no serial byte writes.
- PASS: attended read-only monitor proved continued LCD rendering and
  heartbeats with zero crash/unsafe markers and zero bad render-row lengths.
- PASS: transcript scan reported readiness OK and no crash/unsafe markers.
- PASS: Linux and Windows cleanup checks found no lingering COM6/esptool/Python
  monitor process.
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
- `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530p-debounce-cal.md`
- `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530p-live.md`
- `.agents/handoffs/0095-four-relay-ky040-bbs-lcd-menu-pf0530p-input-report-to-hardware-qa.md`
- `docs/index.md`
- Ignored local evidence directory:
  `<redacted-local-evidence-dir>/`

## Next Gate

Ask for the user visual/input report from the PF0530P attended window. If the
user confirms they rotated or pressed the encoder during the cue sequence and
the device still captured zero input events, open a fresh read-only
physical/input-capture gate for GPIO13/GPIO14/GPIO32 before further debounce or
quadrature tuning.

## Decision Footer

Decision: `flashed_verified_readiness_pass_input_gap`. Next gate: user
visual/input report, then a fresh read-only physical/input-capture gate only if
the user confirms actuation occurred during the zero-input PF0530P window.
Owner: Firmware live-gate owner with Hardware QA and Evidence Records.
Evidence: reviewer quorum, PF0530P source diff, generated XML outputs,
task/source/status records, focused unit tests, scaffold audits, scaffold
verification, no-flash ESP-IDF build, artifact hashes, COM6 identity, rollback,
write-flash, separate verify-flash, read-only reset boot monitor, attended
read-only monitor, transcript scan, cleanup proof, and `git diff --check`.
Approved mutation boundary: completed PF0530P source/build firmware/menu/tests/
docs/records plus one COM6-only PF0530P write/verify/read-only monitor gate.
Authority limits: no further flash, monitor, serial writes, XBee/RF,
relay/load/mains, wiring, DMM/current, erase, persistent config, external
services, release, commit, or push.
