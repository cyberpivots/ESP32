# Source Ledger - 2026-05-30 Four Relay KY-040 Diagnostic Refactor

## Scope

Tier 2 source/docs/audit/firmware diagnostic refactor for the selected KY-040
rotary encoder lane. This records the user-identified ASIN `B06XQTHDRR`,
updates the wiring plan, and enables only the GPIO13 internal pullup for the
active-low switch diagnostic.

This ledger was later updated for the same-session Tier 3 COM6 flash gate after
the user supplied `SAFE STATE CONFIRMED` and requested `Flash the device for
user testing (COM6)`. That gate authorized only COM6 write/verify of this
diagnostic image; it did not authorize serial monitor, radio, relay, load,
mains, erase, wiring acceptance, decoder changes, or hardware acceptance.

## Sources

- Selected module ASIN mirror:
  `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`.
- Prior GPIO13 raw diagnostic gate:
  `SRC-LOCAL-FOUR-RELAY-ENCODER-RAW-DIAGNOSTICS-2026-05-30`.
- ESP-IDF GPIO constraints: `SRC-ESP-IDF-GPIO`.
- ESP32-DevKitC reference context: `SRC-ESP32-DEVKITC`.
- Accepted LCD and XBee bridge lineage:
  `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`,
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- PEC11R is comparison-only for this lane: `SRC-BOURNS-PEC11R`.
- Same-session KY-040 diagnostic flash evidence:
  `research/bench-records/xbee-readonly/local-ky040-diag-flash-20260530T144153Z/`.

## Verified Facts

- The Manuals+ independent ASIN mirror identifies `B06XQTHDRR` as a Cylewet
  KY-040 module from Qianxin with `CLK`, `DT`, `SW`, `+`, and `GND`, 20 pulses
  per rotation, and typically active-low `SW`.
- The same mirror recommends 5 V for Arduino-style setup, so this record does
  not prove 3.3 V operation of the exact bench module.
- ESP-IDF GPIO docs state GPIO34-39 are input-only and have no
  software-enabled pullup or pulldown functions.
- GPIO13 is used as the switch input in the current diagnostic firmware and is
  not in the ESP32 GPIO34-39 no-software-pull group.
- User observation after the prior GPIO13 raw diagnostic flash: the raw LCD
  page is visible, but `A/B/SW`, `ABCHG`, and `SWCHG` do not change.
- The later COM6 KY-040 diagnostic flash gate matched the expected ESP32-D0WDQ6
  on COM6, MAC `78:e3:6d:0a:90:14`, 4 MB flash, and 3.3 V flash voltage before
  mutation.
- The same gate completed 2 MB and 4 MB rollback reads, artifact hashes, a
  recovery command, write-flash with per-segment hash verification, and separate
  verify-flash digest matches.

## Assumptions

- The user-identified ASIN is the exact encoder module on the bench.
- The KY-040 module will be tested only in the ESP32 3.3 V logic domain.
- The raw no-change symptom should be treated as hardware/electrical/pinout
  first, not as a quadrature decoder failure.

## Unknowns

- Exact bench module markings, onboard pullup values, pullup voltage, and
  continuity from KY-040 `CLK`/`DT`/`SW` to GPIO34/GPIO35/GPIO13.
- Whether A/B idle high and toggle low while rotating when the module is
  powered from ESP32 3V3.
- Whether `SW` idles high and pulls low when pressed with the GPIO13 internal
  pullup.
- Rail-current margin, cable/noise behavior, switch bounce, rotation direction,
  and boot behavior.

## Firmware Boundary

- GPIO34 remains the KY-040 `CLK`/A input with internal pulls disabled.
- GPIO35 remains the KY-040 `DT`/B input with internal pulls disabled.
- GPIO13 remains the KY-040 `SW` input and now enables only the ESP32 internal
  pullup for the active-low switch diagnostic.
- Existing raw A/B/SW display, transition counters, decoder constants, menu
  pages, LCD path, UART bridge, and locked relay UI text remain in place.
- No relay GPIO writes, relay-expander writes, XBee setting strings, serial
  monitor path, RF path, Wi-Fi start, storage mount, flash, or erase behavior is
  added.

## Wiring Plan

- KY-040 `GND` -> ESP32 `GND`.
- KY-040 `+` -> ESP32 `3V3` only, not `5V`.
- KY-040 `CLK` -> GPIO34.
- KY-040 `DT` -> GPIO35.
- KY-040 `SW` -> GPIO13.
- Follow the KY-040 module silkscreen, not assumed physical left/right order.

This is not hardware acceptance. Stop if the module only works from 5 V, if a
pullup reaches 5 V, or if continuity/pinout is uncertain.

## Reviewer Quorum

- Coordinator/architecture-risk, weight 5: approve Tier 2 mutation only after
  source coverage and targeted GPIO13-only pullup audit are added.
- Firmware, weight 3: approve GPIO13-only `SW` pullup while keeping
  GPIO34/GPIO35 internal pulls disabled and preserving decoder/menu behavior.
- Hardware/evidence, weight 3: approve only with selected-module source and
  unresolved-gap wording for exact bench electrical behavior.
- Communications, weight 2: approve because XBee setting writes, local-AT, RF,
  range, and throughput stay closed.
- QA, weight 3: approve only with targeted audit/unit coverage and static
  validation.

Weighted disposition after adding those conditions to the mutation plan: 16/16
for the named Tier 2 source/docs/audit/firmware diagnostic refactor. No Tier 3
authority is granted.

Later Tier 3 continuation reviewer disposition after the user supplied
same-session safe-state and COM6 flash authority:

- Coordinator/architecture-risk, weight 5: approved only the named COM6 flash
  after refreshed validation, COM6 identity, rollback backups, recovery command,
  artifact hashes, write-flash, and separate verify-flash.
- Firmware, weight 3: approved the current KY-040 diagnostic image only.
- Hardware/evidence, weight 3: approved write/verify based on user-supplied safe
  state; wiring/electrical acceptance remains pending.
- Communications, weight 2: approved because serial monitor, XBee local-AT, RF,
  range, throughput, and XBee setting writes stayed closed.
- QA, weight 3: approved after refreshed static validation and durable evidence
  records.

Weighted disposition: 16/16 for the named Tier 3 COM6 KY-040 diagnostic flash
gate, no P1/P2 blockers after validation passed. Subagents were not spawned
because the available delegation tool requires explicit user delegation.

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`
- ESP-IDF v6.0.1 no-flash build if available.

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
- `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-ky040-diag-refactor-build build`

The ESP-IDF no-flash build generated
`/tmp/esp32-four-relay-xbee-wifi-ky040-diag-refactor-build/four_relay_xbee_wifi.bin`.

Tier 3 COM6 flash gate passed under
`research/bench-records/xbee-readonly/local-ky040-diag-flash-20260530T144153Z/`:

- `host-static-validation.txt`: refreshed safe-core host tests, firmware/docs/
  source/agent audits, scaffold audit unit tests, `verify_scaffold.py`, and
  `git diff --check`.
- `esp-idf-build.txt`: ESP-IDF v6.0.1 no-flash build to
  `/tmp/esp32-four-relay-xbee-wifi-ky040-diag-live-build`.
- `com6-esptool-identity.txt`: COM6 matched ESP32-D0WDQ6, MAC
  `78:e3:6d:0a:90:14`, 4 MB flash, and 3.3 V flash voltage.
- `com6-pre-flash-backups.txt`: 2 MB and 4 MB rollback reads completed.
- `com6-pre-flash-backups.sha256`: rollback backup hashes recorded.
- `build-artifacts.sha256`: staged flash artifact hashes recorded.
- `recovery-command.txt`: full 4 MB rollback command recorded.
- `com6-ky040-diag-write-flash.txt`: write-flash completed with per-segment
  hash verification.
- `com6-ky040-diag-verify-flash.txt`: separate verify-flash matched all
  segments.
- `post-record-validation.txt`: final post-record host/static/scaffold audit
  pass.

## Bench Checklist For User Testing

- Power off: verify KY-040 module labels and continuity from `CLK`/`DT`/`SW` to
  GPIO34/GPIO35/GPIO13.
- USB power only: verify KY-040 `+` is about 3.3 V to GND.
- Verify A/B idle high and toggle low while rotating.
- Verify SW idles high and pulls low when pressed.
- The COM6 KY-040 diagnostic image is now flashed and verify-flash matched.
  Acceptance still requires LCD raw proof: `A/B` or `ABCHG` changes on rotation,
  and `SW` or `SWCHG` changes on press/release.

## Closed Surfaces

No further COM6 flash, serial monitor, XBee local-AT, RF link probe, range,
throughput, relay GPIO write, relay-expander write, XBee setting write,
relay/load/mains action, erase, decoder change, or hardware acceptance is opened
by this source record.
