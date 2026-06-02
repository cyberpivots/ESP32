# Four Relay KY-040 BBS LCD Menu PF0530S Raw-Liveness Recovery

Status: PF0530S COM6 raw-liveness proof accepted; rotary stability open

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-01

## Routing

- Selected tier: Tier 3 because the requested continuation includes firmware
  mutation, COM6 write/verify flash, reset monitor, and attended hardware
  interaction proof.
- Owner role: Firmware owner with coordinator, QA, LCD UX, hardware-safety, and
  evidence-record lenses.
- Evidence need: source diff, generated menu output, focused tests, scaffold
  audits, scaffold verification, ESP-IDF v6.0.1 no-flash build, artifact
  hashes, COM6 identity, full 4 MB rollback backup, COM6 write-flash, separate
  verify-flash, reset boot transcript, attended read-only transcript, transcript
  scan, cleanup proof, and durable task/source/status records.
- Mutation boundary: PF0530S firmware/menu/test/docs/source records plus COM6
  bootloader, partition table, and app write only. No erase, serial command
  writes, XBee/RF writes or tests, relay GPIO writes, relay-expander writes,
  ESP-NOW runtime expansion, wiring changes, DMM/current/load/mains, persistent
  config, external services, release, commit, or push.
- Reviewer disposition: local coordinator, firmware, QA, LCD UX,
  hardware-safety, and evidence-record lenses approved the named PF0530S
  boundary with no unresolved P1/P2 blockers. Weighted disposition was 15/15.
  Project-local subagents were not spawned because the available multi-agent
  tool metadata requires explicit user delegation and no lifecycle list was
  exposed for cleanup.
- Tier 3 gate authority: the supplied continuation plan records the user's
  `SAFE STATE IS CONFIRMED` and `LIVE FLASH APPROVED` statements for this COM6
  PF0530S continuation. This authority opens only the named COM6 identity,
  rollback, write, verify, read-only monitor, attended read-only monitor,
  cleanup, and records boundary.

## Verified Facts

- PF0530R is documented as written and separately verify-flashed on COM6 with
  readiness/render proof.
- The PF0530R attended monitor captured zero input event lines, so PF0530R is
  not accepted as physical encoder/button proof.
- PF0530E/L/N records prove GPIO13/GPIO14/GPIO32 have produced physical input
  events before under prior images.
- PF0530S changes the active firmware ID and generated menu metadata to
  `PF0530S`.
- GPIO13/GPIO14/GPIO32 remain input-only with pullups; LCD GPIO21/GPIO22 remain
  display-only; `FR_DIAG_XBEE_BRIDGE_CLOSED 1` remains set.
- PF0530S keeps two A/B stable samples, 30 ms switch debounce, 75 ms switch
  guard, and 650 ms long press.
- PF0530S uses 3 ms A/B debounce, 0 ms quiet window, one accepted transition
  per step, and 45 ms step lockout.
- PF0530S emits boot baseline `ENC_BASE`, per-pin `ENC_GPIO_CONFIG`, ESP-IDF
  GPIO config dump, one-second `ENC_LEVEL_HB`, and extended `BBS_MENU_HB`
  raw/ISR/queue/poll counters.
- COM6 PF0530S write-flash and separate verify-flash completed for only the
  bootloader, partition table, and app offsets.
- Reset boot proof captured PF0530S readiness, raw-live-v5 metadata,
  baseline/config/heartbeat telemetry, and zero crash/unsafe markers.
- The attended read-only monitor captured nonzero raw A/B and switch events,
  nonzero ISR events on GPIO13/GPIO14/GPIO32, menu steps in both directions,
  short selects, long selects, visible LCD/menu response, and zero
  crash/unsafe markers.
- Linux and Windows cleanup checks found no lingering COM6/esptool/PF0530S
  monitor process.

## Assumptions

- The prior safe-state/live-flash authority applies to this PF0530S
  continuation.
- The reported PF0530R zero-input monitor reflects either hidden raw visibility
  or a live hardware/input path issue that should be made explicit before more
  debounce tuning.

## Unknowns

- Whether the PF0530S decoder is stable enough for longer mixed-speed use
  remains open.
- The attended monitor recorded invalid/suppressed transitions and queue drops,
  so stability tuning remains a follow-up.

## Validation

- PASS: focused Python unit tests:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (`Ran 30 tests`)
- PASS: generated menu freshness check:
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: firmware scaffold audit:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: scaffold verification:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: ESP-IDF v6.0.1 no-flash build:
  `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-pf0530s-raw-live-build build`
- PASS: pre-flash `git diff --check`.
- PASS: COM6 Windows inventory and esptool identity captured the intended
  ESP32 target, 4 MB flash, and 3.3 V flash-voltage strap evidence.
- PASS: full 4 MB rollback backup captured before programming; SHA-256 is
  retained in ignored local evidence.
- PASS: PF0530S staged artifacts were hashed before programming.
- PASS: Windows esptool write-flash completed for PF0530S bootloader,
  partition table, and app only.
- PASS: separate Windows esptool verify-flash matched all three PF0530S
  artifacts.
- PASS: reset boot monitor captured `PF0530S`, `LCD_INIT_OK`,
  `BBS_LCD_READY`, `BBS_INPUT_READY`, `cal=raw-live-v5`, `ENC_BASE`,
  GPIO13/GPIO14/GPIO32 `ENC_GPIO_CONFIG`, GPIO config dump start, 33
  `ENC_LEVEL_HB`, no serial byte writes, and zero crash/unsafe markers.
- PASS: attended 150 second read-only monitor captured 450 A/B raw events, 84
  switch raw events, GPIO13/GPIO14/GPIO32 ISR events, 27 clockwise steps, 21
  counterclockwise steps, 14 short selects, 4 long selects, LCD/menu response,
  no serial byte writes, and zero crash/unsafe markers.
- GAP: full rotary stability remains open because the attended scan also
  recorded 15 invalid transitions, 31 A/B suppressions, five step-lockout
  filters, and final heartbeat `queue_drop=57`.
- PASS: cleanup checks found no lingering Linux or Windows COM6/esptool/PF0530S
  monitor process.

## Next Gate

PF0530S no longer points to a hardware/input visibility blocker: raw A/B and
switch liveness were recovered under attended actuation. Next work should tune
decoder/queue/debounce behavior under a separate gate before claiming stable
physical rotary acceptance.

## Decision Footer

Decision: `pf0530s_raw_liveness_accepted_stability_open`. Next gate: bounded
PF0530S/PF0530T stability tuning or acceptance proof if requested. Owner:
Firmware owner with Hardware QA and Evidence Records. Evidence: source diff,
focused tests, generated-file check, audits/build, COM6 identity, rollback,
write/verify flash, reset boot transcript, attended read-only transcript,
transcript scans, cleanup proof, and live source ledger. Authority limits: no
erase, serial command writes, XBee/RF, relay/load/mains, wiring, DMM/current,
persistent config, external services, release, commit, or push.
