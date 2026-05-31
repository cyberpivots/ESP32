# Source Ledger - 2026-05-30 Four Relay KY-040 Pin Finder Diagnostic

## Scope

Tier 2 firmware/docs/audit update plus later same-session Tier 3 COM6
write/verify for the KY-040 no-response investigation. This adds a
firmware-only pin-finder LCD diagnostic page so user observation can show which
candidate GPIO changes during knob rotation or switch press.

The later Tier 3 gate authorized only COM6 write-flash and separate
verify-flash of the staged `PF0530A` image after the user supplied `FLASH
APPROVED` and `SAFE STATE CONFIRMED`. No serial monitor, wiring, XBee/RF
action, relay GPIO write, relay-expander write, load, mains, erase, decoder
acceptance, hardware acceptance, or final pin reassignment is opened by this
record.

## Sources

- ESP-IDF GPIO constraints: `SRC-ESP-IDF-GPIO`.
- Selected ASIN mirror: `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`.
- KY-040 module-family pullup/switch behavior:
  `SRC-ENVISTIA-KY040-GUIDE-2026-05-30`.
- Prior raw diagnostic and GPIO13 pullup records:
  `SRC-LOCAL-FOUR-RELAY-ENCODER-RAW-DIAGNOSTICS-2026-05-30`,
  `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`.
- Same-session PF0530A flash evidence:
  `research/bench-records/xbee-readonly/local-ky040-pin-finder-flash-20260530T153433Z/`.

## Verified Facts

- ESP-IDF GPIO documentation states GPIO34-39 do not have software-enabled
  pull-up/down support.
- The selected-module source identifies the user-provided ASIN `B06XQTHDRR` as
  a KY-040-style module with `CLK`, `DT`, `SW`, `+`, and `GND` pins.
- The Envistia KY-040 guide describes onboard 10 kOhm pullups on `CLK`, `DT`,
  and `SW`, 3.3 V compatibility for the module class, and `SW` pulling low when
  pressed and returning high through the pullup when released.
- The current firmware still maps intended KY-040 `CLK`/A to GPIO34, `DT`/B to
  GPIO35, and `SW` to GPIO13.
- The pin-finder diagnostic adds firmware ID `PF0530A` and an alternating LCD
  page that displays live level plus change count for GPIO34, GPIO35, GPIO13,
  GPIO14, GPIO32, and GPIO33.
- GPIO34, GPIO35, GPIO14, GPIO32, and GPIO33 are configured as inputs with
  internal pulls disabled. GPIO13 remains the only internally pulled-up input.
- The COM6 `PF0530A` flash gate matched ESP32-D0WDQ6, MAC
  `78:e3:6d:0a:90:14`, 4 MB flash, and 3.3 V flash voltage before mutation.
- The same gate completed 2 MB and 4 MB rollback reads, artifact hashes,
  recovery command, write-flash with per-segment hash verification, and
  separate verify-flash digest matches.

## Assumptions

- The current no-change symptom is still treated as hardware/electrical/pinout
  first, not as a quadrature decoder failure.
- GPIO14/GPIO32/GPIO33 are temporary input-only probes for discovering
  mislanded encoder wires.
- A changing pin-finder counter is a clue for follow-up continuity proof; it is
  not accepted wiring evidence by itself.

## Unknowns

- Exact bench module markings, onboard resistor values, pullup voltage, module
  rail current, and whether the exact module works from ESP32 3.3 V.
- Continuity from KY-040 `CLK`/`DT`/`SW` to GPIO34/GPIO35/GPIO13.
- Whether any encoder signal is actually landing on GPIO14, GPIO32, or GPIO33.
- A/B idle-high and toggle-low behavior, SW idle-high and pulls-low behavior,
  switch bounce, rotation direction, and boot behavior.
- User LCD observation after the COM6 `PF0530A` pin-finder flash.

## Firmware Boundary

- `main/main.c` remains the only ESP-IDF firmware file changed.
- UART0 host `115200`, UART2 XBee `9600` on GPIO17/GPIO16, LCD I2C0
  GPIO21/GPIO22, decoder constants, menu pages, and locked relay UI text remain
  in place.
- Page 0 alternates between the existing raw A/B/SW diagnostic and the new
  pin-finder display so the pin-finder page is visible even if the encoder
  cannot navigate.
- The pin-finder display format is:
  - `34:<level>/<count> 35:<level>/<count>`
  - `13:<level>/<count> 14:<level>/<count>`
  - `32:<level>/<count> 33:<level>/<count>`
- The display count is modulo 10000 for LCD fit only; validation must treat any
  changing count as diagnostic direction, not final proof.

## Reviewer Quorum

- Governance/Agent Operations, weight 5: approve repo-only Tier 2 mutation with
  no live authority and dirty-tree preservation.
- QA, weight 3: approve after refreshed host/static validation and no Tier 3
  surface changes.
- Evidence/Hardware, weight 3: approve if source records keep hardware
  acceptance unresolved and the new page is recorded as diagnostic-only.

Weighted disposition: 11/11 approve the repo-only Tier 2 pin-finder mutation,
no P1/P2 blockers.

Later Tier 3 continuation reviewer disposition after same-session user flash
authority and safe-state confirmation:

- Governance/Agent Operations, weight 5: approve after refreshed validation,
  COM6 identity, rollback backups, artifact hashes, recovery command, and
  dirty-tree preservation.
- Evidence/Hardware, weight 3: approve if hardware acceptance remains
  unresolved and records are updated.
- QA, weight 3: approve after required validation, write-flash, and separate
  verify-flash evidence.
- Live-bench reviewer, weight 5: initially blocked on incomplete pre-flash
  evidence, then approved after current COM6 identity, rollback backups,
  backup hashes, recovery command, staged artifact hashes, and evidence
  manifest were recorded.

Weighted disposition after blocker clearance: 16/16 approve the named Tier 3
COM6-only `PF0530A` write/verify gate, no P1/P2 blockers.

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
- ESP-IDF v6.0.1 no-flash build if available.

## Validation Results

Passed:

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary`
- `git diff --check`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-ky040-pin-finder-build build`

The ESP-IDF no-flash build generated
`/tmp/esp32-four-relay-xbee-wifi-ky040-pin-finder-build/four_relay_xbee_wifi.bin`.

Tier 3 COM6 PF0530A pin-finder flash gate passed under
`research/bench-records/xbee-readonly/local-ky040-pin-finder-flash-20260530T153433Z/`:

- `host-static-validation.txt`: refreshed firmware audit, focused pullup test,
  safe-core host tests, docs/source/agent audits, scaffold audit unit tests,
  `verify_scaffold.py`, and `git diff --check`.
- `esp-idf-build.txt`: ESP-IDF v6.0.1 no-flash build to
  `/tmp/esp32-four-relay-xbee-wifi-ky040-pin-finder-live-build`.
- `com6-esptool-identity.txt`: COM6 matched ESP32-D0WDQ6, MAC
  `78:e3:6d:0a:90:14`, 4 MB flash, and 3.3 V flash voltage.
- `com6-pre-flash-backups.txt`: 2 MB and 4 MB rollback reads completed.
- `com6-pre-flash-backups.sha256`: rollback backup hashes recorded.
- `build-artifacts.sha256`: staged `PF0530A` artifact hashes recorded,
  including app hash
  `446f4a2646de2deffabcb2f2376d82b63af9d6cdac2a1c91b200d37f4627db36`.
- `recovery-command.txt`: full 4 MB rollback command recorded.
- `com6-pf0530a-pin-finder-write-flash.txt`: write-flash completed with
  per-segment hash verification.
- `com6-pf0530a-pin-finder-verify-flash.txt`: separate verify-flash matched
  all segments.
- `evidence-manifest.md`: authority, boundary, evidence files, and closed
  surfaces recorded.
- `post-record-validation.txt`: final post-record audit pass.

## Bench Checklist For Future User Testing

1. Power off the ESP32 before touching wires.
2. Check the encoder board labels, not the left-to-right order.
3. Wire `GND` to `GND`, `+` to `3V3`, `CLK` to GPIO34, `DT` to GPIO35, and
   `SW` to GPIO13.
4. Do not use `5V` for the encoder while its signal pins go straight to the
   ESP32.
5. The COM6 `PF0530A` diagnostic image is now flashed and verify-flash
   matched. Turn the knob slowly and press the knob. Record exactly which LCD
   numbers change.
6. If the raw page still does not change, use the pin-finder page to see
   whether GPIO14, GPIO32, or GPIO33 changes, then confirm any result with
   power-off continuity before changing the wiring plan.

## Decision Footer

- Decision: ask_user.
- Next gate: user LCD observation after the COM6 `PF0530A` pin-finder flash.
- Owner: Firmware with Hardware, QA, Communications, and Agent Operations
  lenses.
- Evidence: ESP-IDF GPIO constraints, selected KY-040 ASIN source,
  module-family KY-040 guide, prior GPIO13 diagnostic records, and read-only
  reviewer quorum, host/static/scaffold checks, ESP-IDF v6.0.1 no-flash build,
  COM6 identity, rollback backups, artifact hashes, recovery command,
  write-flash, and separate verify-flash.
- Approved mutation boundary: KY-040 firmware/docs/audit/task/source/status
  records plus named COM6-only `PF0530A` write/verify.
- Authority limits: no further flash, serial monitor/write, XBee/RF, relay
  GPIO write, relay-expander write, XBee setting write, relay/load/mains,
  erase, decoder acceptance, hardware acceptance, final pin reassignment,
  commit, or push.
