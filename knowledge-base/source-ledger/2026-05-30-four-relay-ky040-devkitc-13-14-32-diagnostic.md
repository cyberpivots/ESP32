# Source Ledger - 2026-05-30 Four Relay KY-040 DevKitC 13/14/32 Diagnostic

## Scope

Tier 3 `PF0530D` firmware/docs/audit update and COM6 write/verify gate for the
user-confirmed KY-040 wiring: `CLK` GPIO13, `DT` GPIO14, `SW` GPIO32, module
`+` on ESP32 3V3, and a 100 nF capacitor across `+` and `GND`. This diagnostic
is input-only and does not accept final wiring or decoder behavior.

## Sources

- ESP-IDF GPIO constraints: `SRC-ESP-IDF-GPIO`.
- LCD path source: `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`.
- XBee bridge path source:
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- Prior contact-tracer source:
  `SRC-LOCAL-FOUR-RELAY-KY040-GPIO-SWEEP-CONTACT-TRACER-2026-05-30`.
- Selected KY-040 module sources:
  `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`,
  `SRC-ENVISTIA-KY040-GUIDE-2026-05-30`.
- Task record:
  `.agents/TASK_LOG/0105-four-relay-ky040-devkitc-13-14-32-diagnostic.md`.
- Same-session PF0530D flash evidence:
  `research/bench-records/xbee-readonly/local-ky040-pf0530d-devkitc-13-14-32-flash-20260530T174346Z/`.

## Verified Facts

- The user confirmed `CLK` on GPIO13, `DT` on GPIO14, `SW` on GPIO32, encoder
  `+` on ESP32 3V3, and the 100 nF capacitor across encoder `+` and `GND`.
- The user supplied same-session safe-state and COM6 flash authority.
- The accepted LCD path remains GPIO21/GPIO22.
- The accepted XBee UART bridge path remains GPIO17/GPIO16, and PF0530D closes
  that bridge loop with `FR_DIAG_XBEE_BRIDGE_CLOSED 1`.

## Assumptions

- Relay/load/mains remain disconnected.
- The encoder module is powered from ESP32 3V3, not 5 V.
- The capacitor is not connected to any signal pin.
- The useful next proof is raw GPIO13/GPIO14/GPIO32 LCD behavior before any
  decoder or final pin-assignment cleanup.

## Unknowns

- Exact continuity quality, jumper quality, module pullup values, raw idle
  levels, raw transition behavior, rotation direction, switch behavior, rail
  margin, and boot behavior.
- Whether raw changes translate into quadrature position changes.
- Whether GPIO32 can remain an encoder switch input or must be returned to the
  provisional MicroSD CS investigation later.

## Firmware Boundary

- `main/main.c` is the only ESP-IDF firmware source changed.
- PF0530D keeps GPIO13/GPIO14/GPIO32 input-only, enables internal pullups on
  all three, disables pulldowns, and uses no `gpio_set_level()`.
- LCD page 0 is locked and shows firmware ID `PF0530D`, raw `CLK`/`DT`/`SW`
  levels, raw transition counts, position/button counts, per-pin level/count
  lines, and two-second `HIT` lines for changed pins.
- No serial monitor, XBee/RF action, relay GPIO write, relay-expander write,
  MicroSD/TFT action, relay/load/mains action, erase, final pin reassignment,
  commit, or push is in scope.

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

- `user-authority-safe-state.txt`: fresh user authority, safe-state
  confirmation, and user-confirmed wiring.
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
- Next gate: collect user LCD row-0 observation of `PF0530D` during rotation
  and switch press/release.
- Owner: Firmware with Hardware, QA, and Agent Operations lenses.
- Evidence: user wiring and authority, ESP-IDF GPIO source, prior KY-040
  diagnostic chain, refreshed repo validation, no-flash build, COM6 identity,
  rollback backups, artifact hashes, write-flash, separate verify-flash, and
  evidence manifest.
- Authority limits: no serial monitor/write, XBee/RF, relay GPIO write,
  relay-expander write, XBee setting write, MicroSD/TFT action, relay/load/
  mains, erase, wiring mutation, decoder acceptance, hardware acceptance,
  final pin reassignment, commit, or push.
