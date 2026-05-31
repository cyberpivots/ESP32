# Source Ledger - 2026-05-30 Four Relay Encoder Raw Diagnostics

## Scope

Tier 2 firmware/docs/audit preparation and Tier 3 COM6-only backup/write/verify
for a temporary LCD diagnostics build that displays raw encoder GPIO levels and
transition counters before any decoder or switch-behavior fix is selected. This
record includes the GPIO13 switch remap after the user reported GPIO36 is not
exposed on the COM6 ESP32 board.

Continuation note: `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`
records the later user observation that the raw LCD page is visible but
`A/B/SW`, `ABCHG`, and `SWCHG` do not change, selects the ASIN
`B06XQTHDRR` / Cylewet KY-040 branch, and refactors only GPIO13 `SW` to use an
internal pullup.

## Sources

- Prior encoder-menu firmware and COM6 write/verify record:
  `SRC-LOCAL-FOUR-RELAY-ENCODER-MENU-FIRMWARE-2026-05-30`.
- Accepted LCD display-status proof:
  `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`.
- Accepted COM6 XBee bridge proof:
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- ESP-IDF GPIO source: `SRC-ESP-IDF-GPIO`.
- ESP-IDF PCNT source for a possible later decoder fix:
  `SRC-ESP-IDF-PCNT`.
- Espressif component references retained for comparison only:
  `SRC-ESPRESSIF-KNOB-1-0-2`, `SRC-ESPRESSIF-BUTTON-4-1-6`.

## Verified Facts

- The diagnostic firmware preserves UART0 host `115200`, UART2 XBee `9600`,
  TX GPIO17, RX GPIO16, no hardware flow control, and app logging disabled
  after startup.
- The diagnostic firmware preserves LCD I2C0 GPIO21/GPIO22 at 100 kHz and the
  existing PCF8574/PCF8574A candidate-address LCD path.
- The diagnostic firmware keeps GPIO34/GPIO35/GPIO13 configured as inputs with
  internal pullups and pulldowns disabled after the user reported GPIO36 is not
  exposed on the COM6 board.
- LCD page 0 now displays raw `A`, `B`, and `SW` levels from
  GPIO34/GPIO35/GPIO13 without requiring encoder navigation.
- LCD page 0 now displays raw A/B transition count and raw SW transition count
  so physical rotation or press can be checked before changing the decoder.
- Relay pages remain locked UI text only.
- Firmware does not add relay GPIO writes, relay expander writes, XBee setting
  strings, Wi-Fi start, storage mounting, erase, flash, monitor, or RF
  behavior.
- The user authorized the COM6 diagnostic flash and confirmed relay/load/mains
  disconnected for this named gate.
- COM6 matched the recorded ESP32/CP210x target profile before mutation.
- Rollback backups completed before flashing: 2 MB
  `c99c107f732cb07b5d36a54058e8ecc442f3d714dd25dffcfddd98e3e3afc1e6` and
  full 4 MB
  `7b01c496dfd347ccceb76fa22cd899ce6cdb0226436fed2aa236a3ca76c6b8d2`.
- COM6 write-flash completed for the GPIO13 diagnostic image at offsets
  `0x1000`, `0x8000`, and `0x10000` with per-segment hash verification.
- Separate COM6 verify-flash completed with matching digests for all flashed
  segments.

## Assumptions

- Raw GPIO diagnostics are the next useful proof gate because user-observed LCD
  menu presence with encoder nonresponse does not identify whether the failure
  is electrical, switch polarity/debounce, or quadrature decoding.
- A later PCNT or button-component change should be considered only after raw
  GPIO evidence shows usable transitions.

## Unknowns

- Exact encoder/module identity, onboard pullup values, idle raw levels,
  PPR/detents, switch polarity, rail-current margin, boot behavior, and header
  continuity remain unresolved.
- No user-observed raw A/B/SW diagnostic result exists yet.

## Reviewer Quorum

Local read-only lenses only; no subagents were spawned because the available
subagent tool requires explicit user request despite the repo-local default
authorization language.

- Coordinator/architecture-risk, weight 5: approve diagnostic-first repo
  mutation only; Tier 3 flash remains closed.
- Firmware, weight 3: approve raw level/counter display while preserving the
  existing bridge, LCD, locked relay pages, and decoder for comparison.
- Hardware, weight 3: approve unresolved-gap wording and stop before any
  hardware claim without raw evidence.
- Communications, weight 2: approve no XBee command generation, setting write,
  local-AT, RF, range, or throughput action.
- QA, weight 3: approve audit/source/task records and no-flash validation.

Weighted approval: 16/16 for the named Tier 2 diagnostic-preparation boundary,
no P1/P2 blockers. No Tier 3 live action is approved by this record.

Fresh Tier 3 read-only subagent quorum for the COM6 raw diagnostic flash gate:

- Live-bench gate reviewer, weight 5: conditionally approves only the COM6-only
  backup/write/verify boundary after same-session explicit authority,
  relay/load/mains isolation, fresh COM6 identity, rollback backups, hashes,
  and recovery path.
- QA validation reviewer, weight 3: conditionally approves only the named COM6
  raw diagnostic write/verify boundary after P1 authority/isolation/identity
  blockers are cleared and rejects any completion claim without separate
  verify-flash and durable records.
- Evidence-record auditor, weight 3: confirms COM6 is the recorded ESP32 target
  and the source/build are discoverable; does not approve live mutation until
  same-session authority and isolation are recorded.

Weighted disposition: 11/11 conditional approval for the named boundary after
P1 evidence is supplied. The user supplied same-session COM6 authority and
confirmed relay/load/mains disconnected. COM6 identity, rollback backups,
write-flash, and separate verify-flash completed for the named GPIO13
diagnostic image. No serial monitor, XBee/RF, relay, load, or mains action was
run in this continuation.

## Validation Plan

- Host safe-core tests.
- Firmware, documentation, source, and agent-process audits.
- Scaffold audit unit tests.
- `scripts/verify_scaffold.py`.
- `git diff --check`.
- ESP-IDF v6.0.1 no-flash build when the local toolchain is available.

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
- `com6-pre-flash-backups.sha256` records rollback backup hashes.
- `recovery-command.txt` records the 4 MB rollback write command.
- `com6-encoder-raw-diag-gpio13-write-flash.txt` records COM6 write-flash
  with per-segment hash verification.
- `com6-encoder-raw-diag-gpio13-verify-flash.txt` records separate COM6
  verify-flash digest matches.
- `evidence-manifest.md` records the evidence packet and closed surfaces.
- `visual-proof-raw-diag.txt` records the pending LCD observation procedure.

## Diagnostic Decision Tree

- If raw A/B/SW levels and counters stay fixed while rotating/pressing, stop
  firmware fix work and record a hardware/electrical gap for pullups,
  continuity, module identity, or pin mapping.
- If raw SW changes but button events do not count, patch switch polarity or
  debounce and keep raw SW visible until accepted.
- If raw A/B changes but position does not, replace or supplement the software
  decoder with an ESP32-supported quadrature path such as PCNT, or a bounded
  state-machine fallback if PCNT validation is unsuitable.
- If raw levels and decoded counts both work, remove diagnostics only after the
  accepted menu behavior is proven by a later live gate.

## Closed Surfaces

- No serial monitor, XBee local-AT, RF link probe, range, throughput, relay
  GPIO write, relay-expander write, XBee setting write, relay/load/mains
  action, or hardware acceptance is opened by this source record.
