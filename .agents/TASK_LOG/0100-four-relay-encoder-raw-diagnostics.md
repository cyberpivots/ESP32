# Task 0100 - Four Relay Encoder Raw Diagnostics

## Task

- ID: 0100
- Owner role: Firmware with Hardware, Communications, QA, and Agent Operations
  lenses
- Status: Tier 3 COM6 GPIO13 diagnostic backup/write/verify completed;
  superseded for current KY-040 diagnosis by Task 0101
- Created: 2026-05-30
- Updated: 2026-05-30

## Triage

- Continuation note: Task 0101 records the later user observation that the raw
  LCD page is visible but `A/B/SW`, `ABCHG`, and `SWCHG` do not change, selects
  the ASIN `B06XQTHDRR` / Cylewet KY-040 branch, and refactors only GPIO13
  `SW` to use an internal pullup. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`.

- Verified facts: current COM6 bridge firmware preserves UART0 host `115200`,
  UART2 XBee `9600`, GPIO17/GPIO16, and no app logging after startup. Source
  ID: `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- Verified facts: accepted LCD proof uses I2C0 GPIO21/GPIO22 and a
  PCF8574/PCF8574A-class LCD page renderer. Source ID:
  `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`.
- Verified facts: the prior encoder-menu firmware configured GPIO34/GPIO35/
  GPIO36 as input-only encoder lines with internal pulls disabled. The user
  later reported GPIO36 is not exposed on the COM6 board, so this continuation
  remaps `SW` to GPIO13 before live flash. Source ID:
  `SRC-LOCAL-FOUR-RELAY-ENCODER-MENU-FIRMWARE-2026-05-30`.
- Verified facts: ESP-IDF v6.0.1 GPIO docs identify GPIO34-39 as input-only
  and without software pull-up/down support. Source ID: `SRC-ESP-IDF-GPIO`.
- Assumptions: raw LCD diagnostics are the correct next gate because the user
  reports the menu is visible but encoder rotation and button do not respond.
- Unknowns: exact encoder/module identity, onboard pullups, idle levels,
  switch polarity, PPR/detents, rail-current margin, boot behavior, and whether
  GPIO34/GPIO35/GPIO13 raw levels change during physical action.
- Selected tier: Tier 2 for firmware/docs/audit/source/task mutation; Tier 3
  for COM6 prepare, backup, flash, verify-flash, or live proof.
- Owner role: Firmware.
- Evidence need: source-backed diagnostic record, static/audit validation,
  ESP-IDF no-flash build, same-session physical facts, explicit COM6
  authority, rollback backups, write-flash, verify-flash, and user LCD raw
  observation.
- Mutation boundary: `main.c`, `scripts/scaffold_audit_firmware.py`,
  firmware/project docs, source/status/index/task records, and named COM6-only
  diagnostic backup/write/verify.
- Validation plan: host/static checks, scaffold audit unit tests, verifier,
  `git diff --check`, and ESP-IDF no-flash build if available.

## Scope

Included:

- Page 0 LCD raw diagnostics for GPIO34/GPIO35/GPIO13.
- Raw A/B transition counter and raw SW transition counter.
- Existing menu decoder retained for comparison after raw-level proof.
- Relay pages remain locked UI text only.
- Source coverage for GPIO, PCNT, knob, and button references.

Excluded:

- Relay GPIO writes or relay expander writes.
- XBee setting strings/commands, local-AT, RF tests, range, or throughput.
- Serial monitor.
- Wi-Fi, storage, erase, relay/load/mains expansion.
- Any COM6 action without a fresh Tier 3 gate.

## Implementation

- Added `raw_a`, `raw_b`, `raw_sw`, `raw_ab_transition_count`, and
  `raw_sw_transition_count` to the menu state.
- Added `fr_menu_sample_raw()` and call it from the 1 ms poll loop before
  decoder handling.
- Changed page 0 to show `ENC RAW DIAG`, raw `A/B/SW`, `ABCHG`, and `SWCHG`
  without requiring encoder navigation.
- Updated firmware audit markers to require the diagnostic strings and raw
  counters.

## Reviewer Quorum

Local read-only lenses only; no subagents were spawned because the available
subagent tool requires explicit user request despite the repo-local default
authorization language.

- Coordinator/architecture-risk, weight 5: approve Tier 2 diagnostic
  preparation only.
- Firmware, weight 3: approve raw GPIO display/counters while preserving
  existing UART/LCD/menu boundaries.
- Hardware, weight 3: approve unresolved-gap wording and stop before hardware
  conclusions without raw evidence.
- Communications, weight 2: approve because no XBee command generation,
  setting write, local-AT, RF, range, or throughput behavior is added.
- QA, weight 3: approve validation plan and durable task/source records.

Weighted approval: 16/16 for Tier 2 mutation, no P1/P2 blockers. Tier 3 COM6
diagnostic flash remains closed pending explicit authority and same-session
physical facts.

Fresh Tier 3 read-only subagent quorum for the COM6 raw diagnostic flash gate:

- Live-bench gate reviewer, weight 5: conditionally approves the planned
  COM6-only backup/write/verify boundary only after same-session explicit COM6
  diagnostic flash authority, relay/load/mains disconnected confirmation,
  fresh COM6 identity, rollback backups, hashes, and recovery path exist.
- QA validation reviewer, weight 3: conditionally approves the named COM6 raw
  diagnostic flash boundary only after P1 authority/isolation/identity blockers
  are cleared; rejects any completion claim without separate verify-flash and
  durable records.
- Evidence-record auditor, weight 3: confirms COM6 is the recorded ESP32 target
  and the raw diagnostic source/build are discoverable; does not approve live
  mutation until same-session authority and isolation are recorded.

Weighted disposition: 11/11 conditional approval for the named boundary after
P1 evidence is supplied. The user supplied same-session COM6 authority and
confirmed relay/load/mains disconnected. COM6 identity, rollback backups,
write-flash, and separate verify-flash completed for the named GPIO13
diagnostic image. No serial monitor, XBee/RF, relay, load, or mains action was
run in this continuation.

## Diagnostic Gate Completed

Completed before COM6 mutation:

- Explicit COM6 diagnostic flash authority.
- Same-session confirmation that relay/load/mains remain disconnected.
- COM6 esptool identity and rollback backup/hashes.
- COM6 write-flash and separate verify-flash.
- No serial monitor, XBee local-AT, RF, relay, load, or mains action.

User observation target after an authorized diagnostic flash:

- Page 0 shows `A`, `B`, and `SW` raw values.
- Rotating changes `A/B` values or increments `ABCHG`.
- Pressing changes `SW` value or increments `SWCHG`.

## Validation Results

Passed:

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`
- `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-encoder-raw-diag-build build`

The ESP-IDF build generated
`/tmp/esp32-four-relay-xbee-wifi-encoder-raw-diag-build/four_relay_xbee_wifi.bin`.

Fresh GPIO13 flash evidence packet:

- `research/bench-records/xbee-readonly/local-encoder-raw-diag-gpio13-flash-20260530T132827Z/`
- `host-static-validation.txt` records passing safe-core host tests, firmware
  audit, docs audit, source audit, agent-process audit, scaffold audit unit
  tests, `verify_scaffold.py`, and `git diff --check`.
- `esp-idf-build.txt` records a passing ESP-IDF v6.0.1 no-flash build to
  `/tmp/esp32-four-relay-xbee-wifi-encoder-raw-diag-gpio13-build`.
- `build-artifacts.sha256` records the copied flash artifacts:
  - bootloader `9d7113a05ef97d9b7eb3e95dc9e17f55daf9e8783976d5b85a4184d6dac21a25`
  - partition table `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820`
  - app `b9ea59db1fae28a32d75738319310aa69eb53d02a7eac36fc563efd2ae2577e2`
  - flash args `515b26f041abb87776c2441e15cf42b8e7794dfbf6f086c975b9db066bf6b18b`
- `com6-esptool-identity.txt` records that COM6 matched the recorded
  ESP32/CP210x target profile before mutation.
- `com6-pre-flash-backups.sha256` records rollback backup hashes:
  - 2 MB `c99c107f732cb07b5d36a54058e8ecc442f3d714dd25dffcfddd98e3e3afc1e6`
  - 4 MB `7b01c496dfd347ccceb76fa22cd899ce6cdb0226436fed2aa236a3ca76c6b8d2`
- `recovery-command.txt` records the 4 MB rollback write command.
- `com6-encoder-raw-diag-gpio13-write-flash.txt` records COM6 write-flash
  with per-segment hash verification.
- `com6-encoder-raw-diag-gpio13-verify-flash.txt` records separate COM6
  verify-flash digest matches.
- `evidence-manifest.md` records the evidence packet and closed surfaces.
- `visual-proof-raw-diag.txt` records the pending LCD observation procedure.

## Decision Footer

- Decision: ask_user.
- Next gate: user LCD raw diagnostic observation only.
- Owner: Firmware with Hardware, Communications, QA, and Agent Operations
  lenses.
- Evidence: GPIO13 diagnostic source, pre-flash validation, COM6 identity,
  rollback backups/hashes, recovery command, write-flash, and separate
  verify-flash are recorded.
- Approved mutation boundary: completed diagnostic firmware flash/write-verify
  to COM6 only, then user LCD observation of raw `A/B/SW`, `ABCHG`, and
  `SWCHG`.
- Validation: static/host/scaffold checks, ESP-IDF no-flash build, COM6
  backup, write-flash, and verify-flash passed; LCD proof remains pending.
- Durable records: this task log plus
  `knowledge-base/source-ledger/2026-05-30-four-relay-encoder-raw-diagnostics.md`.
- Authority limits: no serial monitor, XBee local-AT, RF, relay GPIO writes,
  relay-expander writes, XBee setting writes, relay/load/mains, or future flash
  beyond the named diagnostic gate.
