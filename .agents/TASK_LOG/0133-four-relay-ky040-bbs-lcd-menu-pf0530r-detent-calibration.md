# Four Relay KY-040 BBS LCD Menu PF0530R Detent Calibration

Status: PF0530R flashed/verified on COM6; readiness accepted; physical input not accepted

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-01

## Routing

- Selected tier: Tier 2 source/build firmware, tests, docs, and records only
  for the initial PF0530R mutation; later same-session COM6 write/verify work
  used the explicit PF0530R Tier 3 gate recorded below.
- Owner role: Firmware owner with coordinator, QA, LCD UX, hardware-safety, and
  evidence-record lenses.
- Evidence need: source diff, generated menu output, focused tests, scaffold
  audits, scaffold verification, ESP-IDF v6.0.1 no-flash build, artifact
  hashes, and durable task/source/status records.
- Mutation boundary: PF0530R firmware/menu/test/docs/source records only. No
  COM6 access, flash, verify-flash, monitor, serial command writes, XBee/RF
  writes or tests, ESP-NOW runtime expansion, relay/load/mains, wiring
  mutation, DMM/current measurement, persistent config, external services,
  release, commit, or push.
- Reviewer disposition: local coordinator, firmware, QA, LCD UX,
  hardware-safety, and source-record lenses approved the named PF0530R
  source/build sequence with no unresolved P1/P2 blockers. Weighted disposition
  was 17/17. Project-local subagents were not spawned because the available
  multi-agent tool metadata required explicit user delegation.
- Tier 3 gate authority: the user later supplied
  `PF0530R-specific COM6 Tier 3 flash gate`, `SAFE STATE CONFIRMED`, and
  `LIVE FLASH APPROVED`. The live boundary opened only COM6 identity, rollback,
  PF0530R bootloader/partition/app write, separate verify-flash, read-only
  monitor, transcript scan, cleanup proof, and durable records.

## Verified Facts

- The user reported the PF0530Q image works but is not stable.
- PF0530Q was the previous written/verify-flashed COM6 image in this
  calibration lineage. PF0530R is now the latest written and separately
  verify-flashed COM6 image.
- PF0530R changes the active firmware ID and generated menu metadata to
  `PF0530R`.
- GPIO13/GPIO14/GPIO32 remain input-only with pullups; LCD GPIO21/GPIO22 remain
  display-only; `FR_DIAG_XBEE_BRIDGE_CLOSED 1` remains set.
- PF0530R keeps two A/B stable samples, 30 ms switch debounce, 75 ms switch
  guard, and 650 ms long press.
- PF0530R raises A/B candidate hold to 8 ms, raises combined A/B quiet time to
  15 ms, changes `FR_ENCODER_TRANSITIONS_PER_STEP` to 2, raises step lockout to
  90 ms, and emits at most one menu step only when accepted quadrature returns
  to detent A/B `3`.
- PF0530R reports `cal=detent-v4`, `ab_ms=8`, `quiet_ms=15`,
  `step_lockout_ms=90`, and detent telemetry.
- PF0530R adds `ENC_FILTER reason=detent_partial` and heartbeat/filter fields
  for detent returns, emitted detent steps, partial detents, raw burst/gap,
  quiet/debounce holds, stable A/B transitions, lockouts, invalid transitions,
  suppressed transitions, and queue drops.
- PF0530R does not add double-click behavior and does not change
  `bbs_lcd_menu.v1` or `bbs_lcd_render.v2` schemas.
- PF0530R live evidence captured same-session COM6 ESP32 identity, detected
  4 MB flash, 3.3 V flash-voltage strap, a full 4 MB rollback backup, pinned
  artifact hashes, COM6 write-flash success, separate verify-flash success,
  reset boot readiness, 150 second read-only monitor completion, transcript
  scan, and Linux/Windows cleanup proof.
- The PF0530R transcript scan reported `readiness_ok: true`,
  `no_crash_or_unsafe: true`, `render_rows_ok: true`, and
  `interaction_ok: false`.
- The PF0530R attended monitor captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, zero `BBS_MENU_SELECT`, and zero `ENC_FILTER` lines, so it
  is not accepted as physical encoder/button proof.

## Assumptions

- The reported instability is more likely bounce-driven extra movement,
  partial jitter, or inconsistent one-detent behavior than zero raw input.
- KY-040-style encoder idle with pullups is expected to rest at A/B `3`; PF0530R
  treats that as the detent-return point.
- PCNT, `espressif/knob`, and `espressif/button` remain deferred until live
  evidence proves raw A/B events exist but software decoding is still the
  failure.

## Unknowns

- Exact PF0530Q unstable pattern: double-step, missed-step, direction inversion,
  quick-rotation loss, or button noise.
- PF0530R physical direction, one-detent behavior, quick-rotation behavior,
  short press, long press, and LCD response under actual actuation.
- Whether PF0530R detent gating improves user-visible stability during actual
  physical actuation.

## Validation

- PASS: focused Python unit tests:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (`Ran 30 tests in 0.148s`)
- PASS: touched comprehensive bench-process test:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_comprehensive_bench_process`
  (`Ran 3 tests in 0.009s`)
- PASS: generated menu freshness check:
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: firmware scaffold audit:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: ESP-IDF v6.0.1 no-flash build:
  `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-pf0530r-detent-cal-build build`
  - App image: `/tmp/esp32-pf0530r-detent-cal-build/four_relay_xbee_wifi.bin`
  - App size: `0x2d8b0`; free in 1 MiB app partition: `0xd2750` (`82%`)
  - Bootloader size: `0x6610`; free before partition table: `0x9f0` (`9%`)
- PASS: final post-record focused Python unit tests:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (`Ran 30 tests in 0.145s`)
- PASS: final post-record comprehensive bench-process test:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_comprehensive_bench_process`
  (`Ran 3 tests in 0.013s`)
- PASS: final post-record generated menu freshness check:
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: final post-record firmware scaffold audit:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: scaffold verification:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
  (`PASS: ESP32 scaffold validation succeeded`)
- PASS: `git diff --check`.
- PASS: PF0530R Tier 3 same-session COM6 identity captured ESP32-D0WDQ6,
  4 MB flash, and 3.3 V flash-voltage strap evidence before write.
- PASS: full 4 MB pre-PF0530R rollback backup captured and hashed; recovery
  command retained in ignored local evidence.
- PASS: PF0530R bootloader, partition table, and app artifacts copied and
  hashed in ignored local evidence.
- PASS: Windows esptool write-flash completed for bootloader at `0x1000`,
  partition table at `0x8000`, and app at `0x10000`.
- PASS: separate Windows esptool verify-flash matched all three PF0530R
  artifacts.
- PASS: reset boot read-only monitor captured `LCD_INIT_OK addr=0x27`,
  `PF0530R BBS_LCD_READY`, `PF0530R BBS_INPUT_READY`, `cal=detent-v4`,
  `ab_ms=8`, `quiet_ms=15`, `step_lockout_ms=90`, `detent=3`, repeated
  heartbeat/render/cursor output, and zero crash/unsafe markers.
- PASS: 150 second attended read-only monitor completed with
  `writes_sent=false`, continued heartbeat/render output, zero bad render row
  lengths, and zero crash/unsafe markers.
- GAP: the live monitor captured zero input events, so PF0530R physical
  encoder/button behavior remains unaccepted.
- PASS: Linux and Windows cleanup checks found no lingering COM6/esptool/PF0530R
  monitor process.

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
- `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530r-detent-cal.md`
- `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530r-live.md`
- `.agents/handoffs/0097-four-relay-ky040-bbs-lcd-menu-pf0530r-to-hardware-qa.md`
- `docs/index.md`
- Ignored local live evidence:
  `<redacted-local-evidence-dir>/`

## Next Gate

PF0530R is flashed and verify-matched on COM6. The next useful gate is an
actual physical input acceptance pass: either a user visual/input report on the
currently flashed PF0530R image or a fresh read-only monitor with confirmed
actuation. Any further firmware flash or broader live surface still requires a
new explicit Tier 3 gate.

## Decision Footer

Decision: `pf0530r_flashed_verified_readiness_ok_input_unaccepted`. Next gate:
PF0530R physical input acceptance by operator report or read-only monitor with
confirmed actuation. Owner: Firmware owner with Hardware QA and Evidence
Records. Evidence: PF0530R source diff, generated XML outputs, source/build
records, focused unit tests, scaffold firmware audit, scaffold verification,
ESP-IDF no-flash build, artifact hashes, COM6 identity, 4 MB rollback backup,
write-flash, separate verify-flash, reset/read-only monitor transcripts,
transcript scan, cleanup proof, and `git diff --check`. Authority limits: no
further flash, serial writes, XBee/RF, relay/load/mains, wiring,
DMM/current, erase, persistent config, external services, release, commit, or
push without a separate explicit gate.
