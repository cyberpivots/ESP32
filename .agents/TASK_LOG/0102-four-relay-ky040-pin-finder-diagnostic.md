# Task 0102 - Four Relay KY-040 Pin Finder Diagnostic

## Task

- ID: 0102
- Owner role: Firmware with Hardware, Communications, QA, and Agent Operations
  lenses
- Status: Tier 3 COM6 PF0530A pin-finder write/verify completed; user LCD
  observation pending
- Created: 2026-05-30
- Updated: 2026-05-30

## Triage

- Verified facts: ESP-IDF GPIO docs state GPIO34-39 do not have
  software-enabled pull-up/down support. Source ID: `SRC-ESP-IDF-GPIO`.
- Verified facts: the user-identified ASIN `B06XQTHDRR` is indexed by a
  Manuals+ mirror as a KY-040 module with `CLK`, `DT`, `SW`, `+`, and `GND`
  pins. Source ID: `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`.
- Verified facts: the Envistia KY-040 guide describes onboard 10 kOhm pullups
  on `CLK`, `DT`, and `SW`, module-family 3.3 V compatibility, and active-low
  switch behavior returning high through a pullup when released. Source ID:
  `SRC-ENVISTIA-KY040-GUIDE-2026-05-30`.
- Verified facts: the existing KY-040 GPIO13 diagnostic branch preserves raw
  LCD diagnostics, keeps GPIO34/GPIO35 internal pulls disabled, enables only
  GPIO13 internal pullup for active-low `SW`, and keeps relay/XBee/live
  surfaces closed. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`.
- Assumptions: the current no-response symptom is hardware/electrical/pinout
  first; the selected KY-040 stays in the ESP32 3.3 V domain; GPIO14/GPIO32/
  GPIO33 are temporary input-only probes, not final assignments.
- Unknowns: exact bench KY-040 markings, onboard pullup values/voltage,
  continuity to GPIO34/GPIO35/GPIO13, whether any signal lands on
  GPIO14/GPIO32/GPIO33, raw LCD behavior, and boot behavior.
- Selected tier: Tier 2 repo-only firmware/docs/audit/status update. Later
  same-session continuation was Tier 3 for the user-approved COM6 PF0530A
  write/verify gate. Any further flash, serial monitor/write, wiring, XBee/RF,
  relay/load/mains, erase, decoder acceptance, or hardware acceptance remains
  Tier 3.
- Owner role: Firmware.
- Evidence need: source IDs above, read-only reviewer quorum, audit/unit
  coverage, and no-flash validation.
- Mutation boundary: KY-040 diagnostic firmware/docs/audit/task/source/status
  records only.
- Validation plan: focused firmware audit/unit test, safe-core host tests,
  docs/sources/agent audits, scaffold audit discovery, `verify_scaffold.py`,
  `git diff --check`, and ESP-IDF v6.0.1 no-flash build if available.

## Scope

Included:

- Add firmware ID `PF0530A` on the LCD diagnostic pages.
- Keep the existing raw GPIO34/GPIO35/GPIO13 page.
- Add an input-only pin-finder page for GPIO34, GPIO35, GPIO13, GPIO14,
  GPIO32, and GPIO33 live level plus change count.
- Configure all probe pins as inputs only.
- Keep internal pulls disabled on GPIO34/GPIO35/GPIO14/GPIO32/GPIO33.
- Keep GPIO13 as the only internally pulled-up probe for active-low `SW`.
- Preserve decoder/menu constants, UART bridge behavior, LCD I2C path, locked
  relay UI text, and closed XBee/relay/load/mains surfaces.
- Update audits, focused unit coverage, source index, source ledger, project
  docs, and status records.

Excluded from the original repo-only mutation:

- Flash, verify-flash, erase, or serial monitor.
- Wiring, continuity measurement, or live bench proof.
- XBee local-AT, RF, range, throughput, or setting writes.
- Relay GPIO writes, relay-expander writes, relay/load/mains action.
- Decoder changes, hardware acceptance, or final pin reassignment.

Later same-session Tier 3 continuation included only COM6 write-flash and
separate verify-flash of the staged `PF0530A` image after user `FLASH
APPROVED` and `SAFE STATE CONFIRMED`.

## Reviewer Quorum

- Governance/Agent Operations, weight 5: approve repo-only Tier 2 mutation
  with dirty-tree preservation and no live authority.
- QA, weight 3: approve repo-only mutation after refreshed host/static
  validation and no Tier 3 surface changes.
- Evidence/Hardware, weight 3: approve if source records keep hardware
  acceptance unresolved and the pin-finder page is diagnostic-only.

Weighted result: 11/11 approve repo-only Tier 2 mutation, no P1/P2 blockers.

Later Tier 3 continuation reviewer disposition after the user supplied
same-session flash authority and safe-state confirmation:

- Governance/Agent Operations, weight 5: approve after refreshed validation,
  COM6 identity, rollback backups, artifact hashes, recovery command, and
  dirty-tree preservation.
- Evidence/Hardware, weight 3: approve if hardware acceptance remains
  unresolved and the live evidence packet is recorded.
- QA, weight 3: approve after the required command set, COM6-only write-flash,
  and separate verify-flash.
- Live-bench reviewer, weight 5: initially blocked on missing pre-flash
  evidence, then approved after current COM6 identity, rollback backups,
  backup hashes, recovery command, staged artifact hashes, and evidence
  manifest were recorded.

Weighted result after blocker clearance: 16/16 approve the named Tier 3
COM6-only `PF0530A` write/verify gate, no P1/P2 blockers.

## Implementation

- Added `PF0530A` firmware ID.
- Added pin-finder probe state and change counters.
- Configured GPIO14, GPIO32, and GPIO33 as additional input-only probes with
  internal pulls disabled.
- Kept GPIO34/GPIO35 internal pulls disabled and GPIO13 internal pullup enabled.
- Made page 0 alternate between raw A/B/SW diagnostics and the pin-finder page
  so the probe page is visible even if encoder navigation is not working.
- Extended firmware audit markers and focused unit tests for the pullup and
  pin-finder boundary.
- Updated durable docs/source records to preserve unresolved hardware
  acceptance boundaries.

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

## Decision Footer

- Decision: ask_user.
- Next gate: user LCD observation after the COM6 `PF0530A` pin-finder flash:
  check the raw page and pin-finder page during rotation and switch press/
  release.
- Owner: Firmware with Hardware, Communications, QA, and Agent Operations
  lenses.
- Evidence: ESP-IDF GPIO source, selected KY-040 ASIN source, Envistia KY-040
  module-family guide, prior GPIO13 diagnostic records, read-only reviewer
  quorum, COM6 identity, rollback backups, artifact hashes, recovery command,
  write-flash, and separate verify-flash.
- Approved mutation boundary: KY-040 diagnostic firmware/docs/audit/task/
  source/status records plus named COM6-only `PF0530A` write/verify.
- Validation: host/static/scaffold checks, ESP-IDF v6.0.1 no-flash build,
  COM6 write-flash, separate verify-flash, and post-record audit pass.
- Durable records: this task log plus
  `knowledge-base/source-ledger/2026-05-30-four-relay-ky040-pin-finder-diagnostic.md`.
- Authority limits: no further flash, serial monitor/write, wiring, XBee
  local-AT/RF, relay GPIO writes, relay-expander writes, XBee setting writes,
  relay/load/mains, erase, decoder acceptance, hardware acceptance, final pin
  reassignment, commit, or push.
