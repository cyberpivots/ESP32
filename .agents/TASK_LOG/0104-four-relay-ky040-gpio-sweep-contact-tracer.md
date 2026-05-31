# Task 0104 - Four Relay KY-040 GPIO Sweep Contact Tracer

## Task

- ID: 0104
- Owner role: Firmware with Hardware, QA, and Agent Operations lenses
- Status: Tier 3 COM6 `PF0530C` contact-tracer write/verify completed; user
  LCD observation pending
- Created: 2026-05-30
- Updated: 2026-05-30

## Triage

- Verified facts: `PF0530B` was written and separately verify-flashed to COM6
  under the evidence packet at
  `research/bench-records/xbee-readonly/local-ky040-row0-pf0530b-flash-20260530T161450Z/`.
- Verified facts: the user reported no change on any displayed `PF0530B`
  GPIO after the row-0 diagnostic flash.
- Verified facts: ESP-IDF GPIO documentation identifies GPIO34-39 as
  input-only and without software pull-up/down support; it also identifies
  strapping pins, flash/PSRAM pin cautions, UART0 flashing/debugging context,
  and `gpio_get_level()` use. Source ID: `SRC-ESP-IDF-GPIO`.
- Verified facts: the accepted LCD path uses GPIO21/GPIO22 and the accepted
  XBee bridge path uses GPIO17/GPIO16. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`,
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- Assumptions: relay/load/mains remain disconnected; no MicroSD, TFT, relay
  expander, or XBee/RF diagnostic is being accepted by this task.
- Unknowns: exact KY-040 module power, common ground, silkscreen wiring,
  jumper quality, continuity to ESP32 headers, and whether any signal lands on
  the new sweep pins.
- Selected tier: Tier 2 firmware/docs/audit mutation. Any flash remains Tier 3.
- Owner role: Firmware.
- Evidence need: exact GPIO allowlist, pull policy, static audit/unit coverage,
  task/source/status records, scaffold validation, and ESP-IDF no-flash build.
- Mutation boundary: `PF0530C` diagnostic firmware, audit/unit tests,
  task/source/status records, and project docs only.

## Scope

Included:

- Change diagnostic firmware ID to `PF0530C`.
- Replace the six-pin row-0 finder with a conservative contact-tracer sweep.
- Keep LCD row 0 sufficient by showing a two-second `HIT` line after any
  watched GPIO changes.
- Keep page display locked to the diagnostic page so encoder navigation is not
  required and cannot hide the diagnostic.
- Close XBee bridge forwarding in this diagnostic image with
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`.
- Use input-only GPIO configuration and no `gpio_set_level()`.

Excluded:

- COM6 flash, serial monitor, serial write, XBee/RF action, relay GPIO write,
  relay-expander write, MicroSD/TFT action, relay/load/mains work, erase,
  wiring mutation, decoder acceptance, hardware acceptance, final pin
  reassignment, commit, or push.

## GPIO Sweep Allowlist

The `PF0530C` sweep intentionally excludes GPIO6-11 flash pins, GPIO21/GPIO22
LCD pins, GPIO1/GPIO3 UART0 pins, GPIO16/GPIO17 XBee UART pins, GPIO0/GPIO2/
GPIO5/GPIO12/GPIO15 strapping-risk pins, and relay candidates GPIO25/GPIO26/
GPIO27/GPIO33.

| GPIO | Pull policy | Diagnostic role | Acceptance boundary |
| --- | --- | --- | --- |
| GPIO34 | No internal pull | Prior `CLK/A` candidate; input-only | Floating until external/module pullup is proven |
| GPIO35 | No internal pull | Prior `DT/B` candidate; input-only | Floating until external/module pullup is proven |
| GPIO36 | No internal pull | Broader input-only sweep candidate | Exposed-header continuity unproven |
| GPIO39 | No internal pull | Broader input-only sweep candidate | Exposed-header continuity unproven |
| GPIO13 | Internal pullup enabled | Prior `SW` and direct-GND stimulus candidate | Diagnostic only; no accepted final wiring |
| GPIO14 | Internal pullup enabled | Spare direct-GND stimulus candidate | Diagnostic only; no accepted final wiring |
| GPIO18 | No internal pull | Passive sweep candidate; historical MicroSD SCK lane | Diagnostic only; no storage acceptance |
| GPIO19 | No internal pull | Passive sweep candidate; historical MicroSD MISO lane | Diagnostic only; no storage acceptance |
| GPIO23 | No internal pull | Passive sweep candidate; historical MicroSD MOSI lane | Diagnostic only; no storage acceptance |
| GPIO32 | No internal pull | Passive sweep candidate; prior pin-finder/MicroSD CS lane | Diagnostic only; no storage acceptance |

## Reviewer Quorum

- Governance/Agent Operations, weight 5: approved repo-only PF0530C mutation
  with conditions; required excluded pins and closed XBee forwarding.
- Firmware, weight 3: approved input-only row-0 last-hit diagnostic with no
  encoder navigation dependency.
- Hardware, weight 3: approved only with flash, LCD, UART0, XBee, strapping,
  and relay/load/mains surfaces excluded or explicitly bounded.
- QA, weight 3: held mutation until this allowlist, audit/unit coverage, and
  durable records existed.
- Live-bench reviewer, weight 5: blocked PF0530C flash; prior PF0530B
  authority does not carry forward.

Weighted disposition after conditions: repo-only mutation proceeds to
automatable validation; live flash remains blocked.

## Implementation

- Added `FR_DIAG_FIRMWARE_ID "PF0530C"`.
- Added `FR_DIAG_XBEE_BRIDGE_CLOSED 1`.
- Added `FR_GPIO_SWEEP_COUNT 10` and the allowlisted GPIO table above.
- Added total change count and last-changed GPIO tracking.
- LCD row 0 now shows:
  - `PF0530C HIT ## C###` for two seconds after any watched GPIO changes,
  - `PF0530C RAW A#B#S#`,
  - `PF0530C TOT C###`,
  - `PF0530C ## L# C###` for each swept GPIO.
- Rows 1-3 show last-hit, total count, and pull-policy reminders.

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
- `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-pf0530c-gpio-sweep-build build`

The ESP-IDF no-flash build generated:

- `/tmp/esp32-four-relay-xbee-wifi-pf0530c-gpio-sweep-build/bootloader/bootloader.bin`
- `/tmp/esp32-four-relay-xbee-wifi-pf0530c-gpio-sweep-build/partition_table/partition-table.bin`
- `/tmp/esp32-four-relay-xbee-wifi-pf0530c-gpio-sweep-build/four_relay_xbee_wifi.bin`

Build artifact SHA-256 values:

- `ee464c58fcff157c59488c29f7c11a4b06daaefb50ebbd8a14b4b2127d01941a`
  `bootloader.bin`
- `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820`
  `partition-table.bin`
- `c56e9b818ac673b73016a2fea7f4f5c245cbfd170a73954badc98f9a8d78bc91`
  `four_relay_xbee_wifi.bin`

## Tier 3 Flash Results

COM6 `PF0530C` contact-tracer flash gate passed under
`research/bench-records/xbee-readonly/local-ky040-pf0530c-contact-tracer-flash-20260530T170711Z/`:

- `user-authority-safe-state.txt`: fresh `CONFIRMED: SAFE STATE` and
  `APPROVED FLASH PF0530C TO COM6 DEVICE` authority.
- `host-static-validation.txt`: refreshed local validation.
- `esp-idf-pf0530c-no-flash-build.txt`: refreshed ESP-IDF v6.0.1 no-flash
  build.
- `com6-esptool-identity.txt`: COM6 matched ESP32-D0WDQ6, MAC
  `78:e3:6d:0a:90:14`, 4 MB flash, and 3.3 V flash voltage.
- `com6-pre-flash-backups.txt`: 2 MB and 4 MB rollback reads completed.
- `com6-pre-flash-backups.sha256`: rollback backup hashes recorded.
- `build-artifacts.sha256`: staged `PF0530C` artifact hashes recorded.
- `recovery-command.txt`: full 4 MB rollback command recorded.
- `com6-pf0530c-contact-tracer-write-flash.txt`: write-flash completed with
  per-segment hash verification.
- `com6-pf0530c-contact-tracer-verify-flash.txt`: separate verify-flash
  matched all three flashed segments.
- `evidence-manifest.md`: authority, boundary, evidence files, and closed
  surfaces recorded.

Rollback backup SHA-256 values:

- `a558616264ac117374355791f378276dc337ad0ac159f7625ca443e727f84afd`
  `com6-pre-pf0530c-contact-tracer-2mb.bin`
- `e5feeb9d9294d03d2b408559ae41362d3f5c5ff7d0abdb773a378f21b8113e85`
  `com6-pre-pf0530c-contact-tracer-4mb.bin`

## Decision Footer

- Decision: ask_user.
- Next gate: user LCD row-0 observation of `PF0530C` during rotation,
  press/release, and any controlled direct-GND stimulus the user separately
  chooses to perform.
- Owner: Firmware with Hardware, QA, and Agent Operations lenses.
- Evidence: ESP-IDF GPIO source, prior KY-040 diagnostic records, PF0530B
  flash evidence, user no-change report, and this allowlist.
- Authority limits: no further flash, serial monitor/write, XBee/RF, relay
  GPIO write, relay-expander write, MicroSD/TFT action, relay/load/mains,
  erase, wiring mutation, decoder acceptance, hardware acceptance, final pin
  reassignment, commit, or push.
