# Task 0101 - Four Relay KY-040 Diagnostic Refactor

## Task

- ID: 0101
- Owner role: Firmware with Hardware, Communications, QA, and Agent Operations
  lenses
- Status: Tier 3 COM6 KY-040 diagnostic write/verify completed; user LCD raw
  observation pending
- Created: 2026-05-30
- Updated: 2026-05-30

## Triage

- Verified facts: the user-identified ASIN `B06XQTHDRR` is indexed by an
  independent Manuals+ mirror as a Cylewet KY-040 rotary encoder module from
  Qianxin with `CLK`, `DT`, `SW`, `+`, and `GND`, 20 pulses per rotation, and
  typically active-low `SW`. Source ID:
  `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`.
- Verified facts: ESP-IDF GPIO docs identify GPIO34-39 as input-only and
  without software pull-up/down support. Source ID: `SRC-ESP-IDF-GPIO`.
- Verified facts: the prior GPIO13 diagnostic firmware displayed raw
  GPIO34/GPIO35/GPIO13 `A/B/SW`, `ABCHG`, and `SWCHG` on LCD page 0 after a
  named COM6 write/verify gate. Source ID:
  `SRC-LOCAL-FOUR-RELAY-ENCODER-RAW-DIAGNOSTICS-2026-05-30`.
- User-supplied observation: the raw page is visible but `A/B/SW`, `ABCHG`, and
  `SWCHG` do not change.
- Assumptions: the ASIN is the exact encoder module being tested, and the
  module will be tested in the ESP32 3.3 V logic domain.
- Unknowns: exact bench module markings, pullup values and voltage, continuity
  from KY-040 `CLK`/`DT`/`SW` to GPIO34/GPIO35/GPIO13, rail-current margin,
  boot behavior, A/B idle/toggle behavior, and SW idle/press behavior.
- Selected tier: Tier 2 for source/docs/audit/firmware diagnostic refactor.
  Tier 3 for any future COM6 flash, wiring, serial monitor, RF, relay, load, or
  mains action.
- Owner role: Firmware.
- Evidence need: selected-module source record, GPIO constraints, user raw LCD
  observation, targeted GPIO13-only pullup audit, status/source/task records,
  and no-flash validation logs.
- Mutation boundary: KY-040 records/docs/audit updates and GPIO13 switch
  pullup diagnostic refactor only.
- Validation plan: host/static checks, scaffold audit unit tests, verifier,
  `git diff --check`, and ESP-IDF no-flash build if available.

## Scope

Included:

- Add selected-module source coverage for `B06XQTHDRR` / Cylewet KY-040.
- Record `SRC-BOURNS-PEC11R` as comparison-only for this lane.
- Update wiring plan to KY-040 `GND` -> ESP32 `GND`, `+` -> ESP32 `3V3`,
  `CLK` -> GPIO34, `DT` -> GPIO35, `SW` -> GPIO13.
- Enable only GPIO13 internal pullup for active-low `SW`; keep GPIO34/GPIO35
  internal pulls disabled.
- Preserve raw LCD diagnostics and existing menu/decoder behavior.
- Later same-session Tier 3 continuation: flash the KY-040 diagnostic image to
  COM6 for user LCD testing after `SAFE STATE CONFIRMED`.

Excluded:

- Further COM6 flash, erase, or serial monitor beyond the named KY-040
  diagnostic write/verify gate.
- XBee local-AT, RF, range, throughput, setting writes, `WR`, `AC`, or `KY`.
- Relay GPIO writes, relay-expander writes, relay/load/mains action.
- Decoder, PCNT, relay behavior, menu behavior, or XBee bridge behavior
  changes beyond the GPIO13 switch pullup diagnostic.

## Reviewer Quorum

- Coordinator/architecture-risk, weight 5: approve Tier 2 mutation within the
  named boundary after source coverage and targeted audit proof are added.
- Firmware, weight 3: approve GPIO13-only switch pullup if GPIO34/GPIO35 remain
  internal-pull disabled.
- Hardware/evidence, weight 3: approve selected-module documentation only with
  unresolved-gap wording for exact bench electrical behavior.
- Communications, weight 2: approve because XBee setting writes, local-AT, RF,
  range, and throughput stay closed.
- QA, weight 3: approve after adding targeted GPIO13-only audit/unit coverage
  and no-behavior-change closed-surface validation.

Weighted result after those conditions are included: 16/16 for Tier 2 mutation,
no P1/P2 blockers. No Tier 3 authority is approved.

Tier 3 continuation reviewer disposition after the user supplied
`SAFE STATE CONFIRMED` and requested `Flash the device for user testing (COM6)`:

- Coordinator/architecture-risk, weight 5: approve only the named COM6 flash
  after identity, rollback backup, recovery command, artifact hashes, write, and
  separate verify evidence.
- Firmware, weight 3: approve the current KY-040 diagnostic image only.
- Hardware/evidence, weight 3: approve based on the user-supplied safe-state
  assertion for flash/write/verify only; hardware acceptance remains pending.
- Communications, weight 2: approve because serial monitor, XBee local-AT, RF,
  range, throughput, and XBee setting writes stay closed.
- QA, weight 3: approve only with refreshed static validation, write-flash,
  separate verify-flash, and durable records.

Weighted result: 16/16 for the named Tier 3 COM6 KY-040 diagnostic flash gate,
no P1/P2 blockers after validation passed. Subagents were not spawned because
the available delegation tool requires explicit user delegation.

## Implementation

- Added selected-module source coverage for the user-identified ASIN
  `B06XQTHDRR` / Cylewet KY-040 while keeping exact bench electrical behavior
  unresolved.
- Refactored encoder GPIO setup so GPIO34/GPIO35 remain internal-pull disabled
  and only GPIO13 enables the ESP32 internal pullup for active-low `SW`.
- Updated firmware audit markers and added
  `tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py` to prove the
  GPIO13-only pullup boundary.
- Updated project docs, firmware README, source index, source ledger, known
  gaps, development status, and triage status.
- Preserved raw LCD diagnostics, decoder/menu constants, UART bridge, LCD path,
  locked relay UI text, and closed XBee/relay/load/mains surfaces.
- Completed the same-session COM6 KY-040 diagnostic write/verify gate under
  `research/bench-records/xbee-readonly/local-ky040-diag-flash-20260530T144153Z/`.

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

Tier 3 COM6 flash gate passed:

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

## Decision Footer

- Decision: ask_user.
- Next gate: user LCD raw observation after the COM6 KY-040 diagnostic flash:
  rotate for `A/B` or `ABCHG` changes and press/release for `SW` or `SWCHG`
  changes.
- Owner: Firmware with Hardware, Communications, QA, and Agent Operations
  lenses.
- Evidence: selected-module source, ESP-IDF GPIO constraints, prior user raw LCD
  observation, targeted GPIO13-only pullup audit, COM6 identity, rollback
  backups, build hashes, recovery command, write-flash, and separate
  verify-flash.
- Approved mutation boundary: source/docs/audit/task records and GPIO13 switch
  pullup diagnostic refactor only.
- Validation: host/static/scaffold checks, ESP-IDF no-flash build, COM6
  write-flash, and separate verify-flash passed.
- Durable records: this task log plus
  `knowledge-base/source-ledger/2026-05-30-four-relay-ky040-diagnostic-refactor.md`.
- Authority limits: no further COM6 flash, serial monitor, XBee local-AT/RF,
  relay GPIO writes, relay-expander writes, XBee setting writes,
  relay/load/mains, erase, decoder change, or hardware acceptance.
