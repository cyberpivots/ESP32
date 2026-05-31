# Task 0105 - Four Relay KY-040 DevKitC 13/14/32 Diagnostic

## Task

- ID: 0105
- Owner role: Firmware with Hardware, QA, and Agent Operations lenses
- Status: Tier 3 COM6 `PF0530D` write/verify completed; user LCD observation
  pending
- Created: 2026-05-30
- Updated: 2026-05-30

## Triage

- Verified facts: the user confirmed the new wiring as KY-040 `CLK` to ESP32
  DevKitC GPIO13, `DT` to GPIO14, `SW` to GPIO32, module `+` to ESP32 3V3,
  and a 100 nF capacitor across `+` and `GND`.
- Verified facts: the user supplied same-session `SAFE STATUS CONFIRMED` and
  `LIVE FLASH APPROVED ON COM6` authority for this gate.
- Verified facts: the accepted LCD path is GPIO21/GPIO22 and the accepted XBee
  bridge path is GPIO17/GPIO16. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`,
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- Verified facts: ESP-IDF GPIO documentation covers GPIO input reads, software
  pullups, strapping pins, flash/PSRAM cautions, and UART0 flashing/debugging
  context. Source ID: `SRC-ESP-IDF-GPIO`.
- Assumptions: relay/load/mains remain disconnected; the capacitor is only
  supply decoupling across `+` and `GND`; no serial monitor, XBee/RF, wiring
  mutation, relay action, load/mains action, erase, commit, or push is
  authorized.
- Unknowns: exact continuity quality to GPIO13/GPIO14/GPIO32, raw LCD
  transition results, rotation direction, switch behavior, boot behavior, and
  final menu/decoder acceptance.
- Selected tier: Tier 3 because the task includes firmware mutation plus COM6
  write/verify.
- Owner role: Firmware.
- Evidence need: repo validation, ESP-IDF no-flash build, COM6 identity,
  rollback backups, artifact hashes, recovery command, write-flash, separate
  verify-flash, and durable source/task records.
- Mutation boundary: `PF0530D` diagnostic firmware, audit/unit tests,
  task/source/status records, project docs, and COM6-only write/verify.

## Reviewer Quorum

- Coordinator/Agent Operations, weight 5: approved the named PF0530D boundary
  with same-session safe-state and live flash authority.
- Firmware, weight 3: approved GPIO13/GPIO14/GPIO32 input-only diagnostic with
  page-0 locked LCD output.
- Hardware, weight 3: approved only with module `+` on 3V3, the capacitor
  treated as supply decoupling, and relay/load/mains surfaces closed.
- QA, weight 3: approved only with guardrail tests, scaffold checks, no-flash
  build, rollback backups, write-flash, and separate verify-flash.
- Live-bench reviewer, weight 5: approved COM6 write/verify only; monitor,
  XBee/RF, wiring mutation, relay/load/mains, erase, and hardware acceptance
  remain closed.

Weighted disposition: 19/19 approved for the named Tier 3 gate, no P1/P2
blockers. No subagents were spawned because the available subagent tool
requires explicit user delegation; local role lenses were used.

## Implementation

- Changed diagnostic firmware ID to `PF0530D`.
- Changed encoder inputs to GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW`.
- Enabled internal pullups on GPIO13/GPIO14/GPIO32 and disabled pulldowns.
- Kept all diagnostic GPIOs input-only and kept `gpio_set_level()` absent.
- Locked LCD page 0 and displayed raw `CLK`/`DT`/`SW` levels, raw transition
  counts, position/button counts, per-pin level/count lines, and two-second
  `HIT` lines for the last changed pin.
- Kept `FR_DIAG_XBEE_BRIDGE_CLOSED 1` so the diagnostic image does not run
  the UART0-to-UART2 XBee bridge loop.

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
- COM6 identity, rollback backups, artifact hashes, recovery command,
  write-flash, and separate verify-flash.

## Validation Results

Passed:

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`
- `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-pf0530d-devkitc-13-14-32-build build`

Build artifact SHA-256 values:

- `88a3edd89b0f706919d28e1b880c522e0fb0c3dc7c9a401ba9c8479198aa1574`
  `pf0530d-bootloader.bin`
- `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820`
  `pf0530d-partition-table.bin`
- `b1c146bdea766438d28c8173c931472d91ae571ec0c298c6a7b61f0203dc90ed`
  `pf0530d-four_relay_xbee_wifi.bin`

## Tier 3 Flash Results

COM6 `PF0530D` diagnostic flash gate passed under
`research/bench-records/xbee-readonly/local-ky040-pf0530d-devkitc-13-14-32-flash-20260530T174346Z/`:

- `user-authority-safe-state.txt`: fresh safe-state, live flash authority, and
  user-confirmed wiring strings.
- `host-static-validation.txt`: refreshed local validation.
- `esp-idf-pf0530d-no-flash-build.txt`: refreshed ESP-IDF v6.0.1 no-flash
  build.
- `com6-esptool-identity.txt`: COM6 matched ESP32-D0WDQ6, MAC
  `78:e3:6d:0a:90:14`, 4 MB flash, and 3.3 V flash voltage.
- `com6-pre-flash-backups.txt`: 2 MB and 4 MB rollback reads completed.
- `com6-pre-flash-backups.sha256`: rollback backup hashes recorded.
- `build-artifacts.sha256`: staged `PF0530D` artifact hashes recorded.
- `recovery-command.txt`: full 4 MB rollback command recorded.
- `com6-pf0530d-devkitc-13-14-32-write-flash.txt`: write-flash completed with
  per-segment hash verification.
- `com6-pf0530d-devkitc-13-14-32-verify-flash.txt`: separate verify-flash
  matched all three flashed segments.
- `evidence-manifest.md`: authority, boundary, evidence files, hashes, and
  closed surfaces recorded.
- `post-flash-record-validation.txt`: final record-level audits and
  `git diff --check` passed after flash evidence updates.

Rollback backup SHA-256 values:

- `ef2028c1e176d79ef43168301dbf2dfad0476fbe1180d8f982be5fa1c0c6164a`
  `com6-pre-pf0530d-devkitc-13-14-32-2mb.bin`
- `4a601e4330c1583efd518526708093a25dd4b17a09ac9373d36ed464c79b89e8`
  `com6-pre-pf0530d-devkitc-13-14-32-4mb.bin`

## Decision Footer

- Decision: ask_user.
- Next gate: user LCD row-0 observation of `PF0530D` during rotation and
  switch press/release.
- Owner: Firmware with Hardware, QA, and Agent Operations lenses.
- Evidence: user wiring/safe-state/flash authority, ESP-IDF GPIO source,
  prior KY-040 diagnostic records, refreshed repo validation, no-flash build,
  COM6 identity, rollback backups, artifact hashes, write-flash, separate
  verify-flash, and evidence manifest.
- Authority limits: no serial monitor/write, XBee/RF, relay GPIO write,
  relay-expander write, MicroSD/TFT action, relay/load/mains, erase, wiring
  mutation, decoder acceptance, hardware acceptance, final pin reassignment,
  commit, or push.
