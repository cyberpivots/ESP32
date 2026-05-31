# Task 0103 - Four Relay KY-040 Row-0 Diagnostic

## Task

- ID: 0103
- Owner role: Firmware with Hardware, QA, and Agent Operations lenses
- Status: Tier 3 COM6 `PF0530B` row-0 diagnostic write/verify completed; user
  reported no displayed pin changes
- Created: 2026-05-30
- Updated: 2026-05-30

## Triage

- Verified facts: the prior `PF0530A` image sampled GPIO34, GPIO35, GPIO13,
  GPIO14, GPIO32, and GPIO33, but useful pin-finder values were on LCD rows
  below row 0.
- Verified facts: the user reported only pin 34 was displayed and encoder
  navigation cannot be used to change pages.
- Verified facts: ESP-IDF GPIO documentation says GPIO34-39 have no
  software-enabled pull-up/down support. Source ID: `SRC-ESP-IDF-GPIO`.
- Verified facts: the KY-040 diagnostic branch keeps GPIO34/GPIO35 internal
  pulls disabled and enables only GPIO13 internal pullup for the active-low
  switch diagnostic. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`,
  `SRC-LOCAL-FOUR-RELAY-KY040-PIN-FINDER-DIAGNOSTIC-2026-05-30`.
- Assumptions: LCD row 0 is the only reliable user-observed display surface;
  the KY-040 stays in the ESP32 3.3 V domain; GPIO14/GPIO32/GPIO33 remain
  temporary input-only probes.
- Unknowns: exact KY-040 module markings, pullup voltage, continuity to
  GPIO34/GPIO35/GPIO13, whether any signal lands outside the six-pin
  `PF0530B` probe set, and why no displayed pin changed.
- Selected tier: Tier 2 firmware/docs/audit refactor plus Tier 3 for any
  future COM6 flash.
- Owner role: Firmware.
- Evidence need: source-backed GPIO boundaries, read-only reviewer quorum,
  refreshed static/host validation, ESP-IDF no-flash build, and a separate
  Tier 3 evidence packet before any write-flash.
- Mutation boundary: row-0 KY-040 diagnostic display in `main.c`, firmware
  audit/unit markers, task/source/status records, and project docs only.

## Scope

Included:

- Change the diagnostic firmware ID to `PF0530B`.
- Add a row-0 auto-scanner that cycles through:
  - raw A/B/SW levels,
  - raw A/B and SW transition counters,
  - GPIO34, GPIO35, GPIO13, GPIO14, GPIO32, and GPIO33 live level/change
    count lines.
- Keep rows 1-3 as paired pin-finder summaries for full 20x4 LCD visibility.
- Keep all probe pins input-only.
- Keep GPIO34/GPIO35/GPIO14/GPIO32/GPIO33 internal pulls disabled.
- Keep GPIO13 as the only internally pulled-up probe.
- Preserve UART bridge behavior, LCD I2C behavior, relay locked UI text, and
  closed XBee/RF/relay/load/mains surfaces.

Excluded:

- Serial monitor, erase, wiring mutation, XBee local-AT/RF action, relay GPIO
  writes, relay-expander writes, relay/load/mains work, decoder acceptance,
  hardware acceptance, or final pin reassignment.

Later same-session Tier 3 continuation included only COM6 write-flash and
separate verify-flash after the user supplied fresh `FLASH APPROVED` and
`SAFE STATE CONFIRMED`, and after current COM6 identity, rollback backups,
artifact hashes, and recovery command were recorded.

## Reviewer Quorum

- Governance/Agent Operations, weight 5: approved bounded repo mutation and
  blocked live flash until Tier 3 preconditions are satisfied.
- Firmware/Hardware/Evidence lenses, weight 3 each in the governance summary:
  approved the row-0 scanner as a diagnostic-only aid; changing counters are
  clues, not wiring acceptance.
- QA, weight 3: approved repo-only mutation and required refreshed audits,
  focused unit coverage, docs/source records, and ESP-IDF build before any
  flash.
- Live-bench reviewer, weight 5: blocked write-flash until fresh `FLASH
  APPROVED` and `SAFE STATE CONFIRMED` for this new `PF0530B` image; that
  blocker was cleared by the user's same-session authority and safe-state
  confirmation plus current identity, rollback, hash, and recovery evidence.

Weighted result: repo mutation approved; later named COM6-only write/verify
gate completed after blocker clearance.

## Implementation

- Replaced the page-level raw/pin-finder alternation with a row-0 auto-scanner.
- Added compact 20-column-safe row-0 formats:
  - `PF0530B RAW A#B#S#`
  - `PF0530B AB### SW###`
  - `PF0530B ## L# C####`
- Kept the existing pin-finder sampling and lower-row pair display.
- Updated firmware audit and focused unit test markers for `PF0530B`.

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
- `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-pf0530b-row0-build build`

The ESP-IDF no-flash build generated:

- `/tmp/esp32-four-relay-xbee-wifi-pf0530b-row0-build/bootloader/bootloader.bin`
- `/tmp/esp32-four-relay-xbee-wifi-pf0530b-row0-build/partition_table/partition-table.bin`
- `/tmp/esp32-four-relay-xbee-wifi-pf0530b-row0-build/four_relay_xbee_wifi.bin`

Build artifact SHA-256 values:

- `a0dd4ac6b3fbe675829041db7f2dc2cca74611cad9e776caaf35cc124588a366`
  `bootloader.bin`
- `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820`
  `partition-table.bin`
- `c7236b6fcad7b660d9e1e228b3bd79035acb0af65f1bcebafb00e52d6e0ba952`
  `four_relay_xbee_wifi.bin`

Tier 3 COM6 `PF0530B` row-0 diagnostic flash gate passed under
`research/bench-records/xbee-readonly/local-ky040-row0-pf0530b-flash-20260530T161450Z/`:

- `user-authority-safe-state.txt`: fresh flash authority and safe-state
  confirmation.
- `host-static-validation.txt`: refreshed firmware audit, focused pullup test,
  safe-core host tests, docs/source/agent audits, scaffold audit unit tests,
  `verify_scaffold.py`, and `git diff --check`.
- `com6-esptool-identity.txt`: COM6 matched ESP32-D0WDQ6, MAC
  `78:e3:6d:0a:90:14`, 4 MB flash, and 3.3 V flash voltage.
- `com6-pre-flash-backups.txt`: 2 MB and 4 MB rollback reads completed.
- `com6-pre-flash-backups.sha256`: rollback backup hashes recorded.
- `build-artifacts.sha256`: staged `PF0530B` artifact hashes recorded.
- `recovery-command.txt`: full 4 MB rollback command recorded.
- `com6-pf0530b-row0-write-flash.txt`: write-flash completed with per-segment
  hash verification.
- `com6-pf0530b-row0-verify-flash.txt`: separate verify-flash matched all
  three flashed segments.
- `evidence-manifest.md`: authority, boundary, evidence files, and closed
  surfaces recorded.
- `user-pf0530b-no-change-observation.txt`: user-reported observation that no
  displayed `PF0530B` pins changed.

User observation after the flash:

- The user reported `NO CHANGE`.
- The user later clarified that no displayed pins changed and requested a new
  approach because the current pin config is not working.
- Treat this as a signal-discovery failure for the six-pin diagnostic set, not
  quadrature decoder acceptance, module rejection, hardware acceptance, or
  final pin reassignment.

## Decision Footer

- Decision: superseded_by_0104.
- Next gate: repo-only `PF0530C` GPIO sweep contact-tracer validation, then a
  fresh Tier 3 PF0530C flash gate only if requested.
- Owner: Firmware with Hardware, QA, and Agent Operations lenses.
- Evidence: ESP-IDF GPIO source, KY-040 diagnostic source records, reviewer
  quorum, and local validation.
- Authority limits: no further flash, serial monitor/write, XBee/RF, relay
  GPIO write, relay-expander write, relay/load/mains, erase, decoder
  acceptance, hardware acceptance, final pin reassignment, commit, or push.
