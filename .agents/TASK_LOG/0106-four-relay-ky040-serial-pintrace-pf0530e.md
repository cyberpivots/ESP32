# Task 0106 - Four Relay KY-040 Serial Pintrace PF0530E

## Task

- ID: 0106
- Owner role: Firmware with Hardware, QA, Agent Operations, and Live Bench
  lenses
- Status: Tier 3 implementation and COM6 live monitor complete; hardware
  actuation remains unconfirmed
- Created: 2026-05-30
- Updated: 2026-05-30

## Triage

- Verified facts: `PF0530D` was written and separately verify-flashed to COM6
  for GPIO13/GPIO14/GPIO32, but the user reported the encoder path still was
  not working and requested a new COM6 live-monitor approach.
- Verified facts: prior COM6 evidence identified an ESP32-D0WDQ6 revision v1.0
  with MAC `78:e3:6d:0a:90:14`, 4 MB flash, and 3.3 V flash voltage.
- Verified facts: Espressif DevKitC source coverage records that physical
  header position `J2-13` is `IO12`, `J2-14` is `GND`, `IO13` is `J2-15`,
  `IO14` is `J2-12`, and `IO32` is `J2-7`. Source ID:
  `SRC-ESP32-DEVKITC`.
- Verified facts: ESP-IDF GPIO source coverage records strapping pins, GPIO34
  through GPIO39 no software pull-up/down support, `gpio_get_level()`, and
  input configuration behavior. Source ID: `SRC-ESP-IDF-GPIO`.
- Assumptions: the user's same-thread safe-state and COM6 flash/monitor request
  apply to the named PF0530E gate; KY-040 `+` remains on ESP32 3V3; relay/load/
  mains remain disconnected.
- Unknowns: exact wire landing, KY-040 continuity, jumper quality, module
  pullups, rotation direction, and which GPIO changes during live testing.
- Selected tier: Tier 3 because this task includes firmware mutation, COM6
  flash, and serial monitoring.
- Owner role: Firmware.
- Evidence need: source-backed firmware change, repo validation, ESP-IDF
  no-flash build, COM6 identity, rollback backup, artifact hashes, write-flash,
  separate verify-flash, and serial transcript.
- Mutation boundary: `PF0530E` serial pintrace firmware, focused tests/audits,
  pyserial read-only monitor helper, task/source/status records, and COM6-only
  write/verify plus read-only serial monitor.

## Reviewer Quorum

- Coordinator/Agent Operations, weight 5: approved the named PF0530E boundary
  under the user's COM6 live-monitor request.
- Firmware, weight 3: approved a serial-first input-only GPIO contact tracer
  that does not depend on LCD navigation.
- Hardware, weight 3: approved only with 3.3 V encoder power assumed,
  input-only GPIO configuration, no internal pulls except GPIO13/GPIO14/
  GPIO32, and relay/load/mains surfaces closed.
- QA, weight 3: approved with focused tests, scaffold audits, no-flash build,
  rollback backup, write-flash, separate verify-flash, and serial transcript.
- Live Bench, weight 5: approved COM6-only flash/verify and read-only monitor;
  wiring mutation, relay/load/mains, XBee/RF, erase, and hardware acceptance
  remain closed.

Weighted disposition: 19/19 approved for the named Tier 3 gate, no P1/P2
blockers. No subagents were spawned because the available subagent tool
requires explicit user delegation; local role lenses were used.

## Implementation

- Changed diagnostic firmware ID to `PF0530E`.
- Added `FR_DIAG_SERIAL_PINTRACE 1` so the app runs the serial pintrace path
  instead of the LCD diagnostic path.
- Added input-only monitoring for GPIO0/GPIO2/GPIO4/GPIO5/GPIO12/GPIO13/
  GPIO14/GPIO15/GPIO16/GPIO17/GPIO18/GPIO19/GPIO21/GPIO22/GPIO23/GPIO25/
  GPIO26/GPIO27/GPIO32/GPIO33/GPIO34/GPIO35/GPIO36/GPIO39.
- Enabled internal pullups only on GPIO13/GPIO14/GPIO32 and disabled pulldowns
  on all watched pins.
- Added stable `EV` event printing and periodic `HB`/`ST` summaries on
  COM6/UART0.
- Moved the serial pintrace loop into a dedicated FreeRTOS task and changed
  the poll delay to a tick-safe 10 ms path after the first live monitor showed
  task-watchdog backtraces with the shorter poll delay.
- Added `tools/pf0530e_serial_pintrace_monitor.py`, which opens the selected
  serial port and reads only; it does not send serial bytes.

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`
- ESP-IDF v6.0.1 no-flash build.
- COM6 identity, fresh rollback backup, artifact hashes, recovery command,
  write-flash, separate verify-flash, and live serial transcript.

## Validation Results

- Repo validation passed after the tick-safe r4 patch:
  `scripts/scaffold_audit_firmware.py`, focused encoder boundary unit test,
  four-relay safe-core host tests, docs/source/agent audits, full scaffold
  audit unit discovery, `scripts/verify_scaffold.py`, and `git diff --check`.
- ESP-IDF v6.0.1 no-flash build passed for the r4 artifact set:
  `esp-idf-pf0530e-no-flash-build-r4.txt`.
- Final r4 hashes:
  bootloader `dd7b96aec043d81baff973bb2a0f446435946531076be6299d5f45d7dd32151c`,
  partition table
  `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820`,
  app `99143f70d964ad27b4279ac941eccf7050fcac2059b66dfea0d71631066f61e5`.
- COM6 identity was rechecked as ESP32-D0WDQ6 revision v1.0, MAC
  `78:e3:6d:0a:90:14`.
- R4 write-flash and separate verify-flash passed for bootloader, partition
  table, and app: `com6-pf0530e-write-flash-r4.txt` and
  `com6-pf0530e-verify-flash-r4.txt`.
- The r4 monitor ran from `2026-05-30T18:53:41.080+00:00` through
  `2026-05-30T19:03:41.111+00:00` with `writes_sent=false`.
- R4 transcript scan found no watchdog, backtrace, panic, or guru-meditation
  lines.
- R4 transcript `EV` lines appeared only during boot settling on GPIO0,
  GPIO5, and GPIO15. Final heartbeat still showed GPIO13 `CLK` level 1 count
  0, GPIO14 `DT` level 1 count 0, and GPIO32 `SW` level 1 count 0.
- No user message confirmed that the encoder was physically turned/pressed
  during the r4 monitor window, so this is not hardware-acceptance proof of a
  failed encoder path. If the encoder was actuated during the r4 window, the
  recorded evidence points away from firmware/decoder behavior and toward
  continuity, module power, common ground, jumper quality, or module failure.
- The r5 monitor restarted on the already-flashed PF0530E r4 image after the
  user explicitly requested monitoring and later confirmed the actuation
  sequence with `DONE`.
- R5 transcript: `pf0530e-serial-monitor-transcript-r5.txt`, 636 lines,
  `writes_sent=false`, first line
  `2026-05-30T19:31:08.018+00:00`, last captured heartbeat
  `2026-05-30T19:31:53.471+00:00`.
- R5 transcript scan found no watchdog, backtrace, panic, abort, assertion, or
  guru-meditation lines.
- R5 encoder evidence: GPIO13 `CLK` changed from count 52 to 72 with 20 `EV`
  lines; GPIO14 `DT` changed from count 40 to 70 with 30 `EV` lines; GPIO32
  `SW` changed from count 16 to 26 with 10 `EV` lines. Final levels were high
  on all three intended encoder pins.
- R5 interpretation: GPIO13/GPIO14/GPIO32 are physically changing on COM6, so
  the current problem is no longer "no pin changes." During the button-press
  window, GPIO32 `SW` changes coincided with GPIO14 `DT` changes, which remains
  an unresolved bench clue rather than a decoder conclusion.

## Decision Footer

- Decision: complete the PF0530E live-monitor implementation gate and record
  the r5 live actuation evidence.
- Next gate: refactor the application decoder/button handling for
  GPIO13/GPIO14/GPIO32, or run a separately approved direct bench isolation
  sequence for SW-only and DT-only behavior.
- Owner: Firmware with Hardware, QA, Agent Operations, and Live Bench lenses.
- Evidence: user request, source-backed DevKitC/GPIO/KY-040 records, prior
  PF0530D flash evidence, r4 build/write/verify logs, r4 serial transcript,
  and r5 user-confirmed live serial transcript.
- Approved mutation boundary: PF0530E firmware/tests/docs/records, COM6-only
  write/verify, and read-only COM6 monitoring.
- Authority limits: no wiring mutation, relay GPIO write, relay-expander write,
  XBee/RF, MicroSD/TFT, relay/load/mains, erase, hardware acceptance, final pin
  reassignment, commit, or push.
