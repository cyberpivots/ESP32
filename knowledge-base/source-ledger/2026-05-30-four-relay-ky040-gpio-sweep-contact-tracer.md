# Source Ledger - 2026-05-30 Four Relay KY-040 GPIO Sweep Contact Tracer

## Scope

Tier 2 repo-only `PF0530C` firmware/docs/audit update plus later same-session
Tier 3 COM6 write/verify after the user reported that the `PF0530B` row-0
diagnostic showed no change on any displayed GPIO. This task changes the next
image from a six-pin encoder pin finder into a conservative LCD row-0 contact
tracer. The later flash gate writes and separately verifies that image only; it
does not accept any wiring.

## Sources

- ESP-IDF GPIO constraints: `SRC-ESP-IDF-GPIO`.
- LCD path source: `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`.
- XBee bridge path source:
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- Prior row-0 diagnostic source:
  `SRC-LOCAL-FOUR-RELAY-KY040-ROW0-DIAGNOSTIC-2026-05-30`.
- Selected KY-040 module sources:
  `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`,
  `SRC-ENVISTIA-KY040-GUIDE-2026-05-30`.
- Task record:
  `.agents/TASK_LOG/0104-four-relay-ky040-gpio-sweep-contact-tracer.md`.
- Same-session PF0530C flash evidence:
  `research/bench-records/xbee-readonly/local-ky040-pf0530c-contact-tracer-flash-20260530T170711Z/`.

## Verified Facts

- `PF0530B` was written and separately verify-flashed to COM6 under
  `research/bench-records/xbee-readonly/local-ky040-row0-pf0530b-flash-20260530T161450Z/`.
- The user reported no change on any displayed `PF0530B` pins.
- The previous six-pin diagnostic set was GPIO34, GPIO35, GPIO13, GPIO14,
  GPIO32, and GPIO33.
- ESP-IDF GPIO documentation records GPIO34-39 as input-only and without
  software-enabled internal pull-up/down support.
- The project LCD path is GPIO21/GPIO22, the current XBee UART bridge path is
  GPIO17/GPIO16, and relay candidates remain GPIO25/GPIO26/GPIO27/GPIO33 in
  the pin plan.

## Assumptions

- Relay/load/mains remain disconnected.
- The next useful firmware-only branch is finding whether any safe candidate
  GPIO changes, not changing the quadrature decoder.
- No MicroSD, TFT, relay expander, or XBee/RF surface is being accepted by this
  diagnostic.

## Unknowns

- Exact KY-040 module markings, onboard pullup values, pullup voltage, common
  ground, module power, jumper quality, and continuity to the ESP32 headers.
- Whether the encoder signals land on any GPIO outside the prior six-pin set.
- Whether GPIO36 or GPIO39 are exposed on the exact board/shield.
- Whether passive MicroSD-candidate pins GPIO18/GPIO19/GPIO23/GPIO32 have any
  external hardware attached in the current bench setup.
- User LCD observation of the `PF0530C` contact tracer after the COM6
  write/verify gate.

## GPIO Allowlist And Pull Policy

`PF0530C` excludes flash pins GPIO6-11, LCD pins GPIO21/GPIO22, UART0 pins
GPIO1/GPIO3, XBee UART pins GPIO16/GPIO17, strapping-risk pins GPIO0/GPIO2/
GPIO5/GPIO12/GPIO15, and relay candidates GPIO25/GPIO26/GPIO27/GPIO33.

| GPIO | Pull policy | Reason |
| --- | --- | --- |
| GPIO34 | No internal pull | Prior `CLK/A` candidate; input-only/no software pulls |
| GPIO35 | No internal pull | Prior `DT/B` candidate; input-only/no software pulls |
| GPIO36 | No internal pull | Broader input-only candidate; exposure unproven |
| GPIO39 | No internal pull | Broader input-only candidate; exposure unproven |
| GPIO13 | Internal pullup enabled | Prior `SW` candidate and direct-GND stimulus point |
| GPIO14 | Internal pullup enabled | Spare direct-GND stimulus point |
| GPIO18 | No internal pull | Passive sweep only; historical MicroSD SCK candidate |
| GPIO19 | No internal pull | Passive sweep only; historical MicroSD MISO candidate |
| GPIO23 | No internal pull | Passive sweep only; historical MicroSD MOSI candidate |
| GPIO32 | No internal pull | Passive sweep only; prior pin-finder/MicroSD CS candidate |

## Firmware Boundary

- `main/main.c` is the only ESP-IDF firmware source changed.
- `PF0530C` keeps probe pins input-only and uses no `gpio_set_level()`.
- The diagnostic page is pinned to LCD page 0, so encoder navigation is not
  required and cannot hide the tracer.
- LCD row 0 shows `PF0530C HIT ## C###` for two seconds after a watched GPIO
  changes, otherwise it cycles raw A/B/SW, total sweep count, and each swept
  GPIO level/change count.
- `FR_DIAG_XBEE_BRIDGE_CLOSED 1` prevents this diagnostic image from running
  the UART0-to-UART2 XBee bridge loop. The prior bridge image remains
  recoverable only through a separate flash gate or rollback.

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

The ESP-IDF no-flash build generated
`/tmp/esp32-four-relay-xbee-wifi-pf0530c-gpio-sweep-build/four_relay_xbee_wifi.bin`.

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

- `user-authority-safe-state.txt`: fresh user authority and safe-state
  confirmation.
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
- Evidence: ESP-IDF GPIO source, prior diagnostic records, PF0530B flash
  evidence, user no-change report, and exact PF0530C allowlist.
- Authority limits: no further flash, serial monitor/write, XBee/RF, relay
  GPIO write, relay-expander write, XBee setting write, MicroSD/TFT action,
  relay/load/mains, erase, wiring mutation, decoder acceptance, hardware
  acceptance, final pin reassignment, commit, or push.
