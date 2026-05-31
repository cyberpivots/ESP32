# Source Ledger - 2026-05-30 Four Relay KY-040 Row-0 Diagnostic

## Scope

Tier 2 firmware/docs/audit update plus later same-session Tier 3 COM6
write/verify for the KY-040 no-response investigation. This refactors the
diagnostic display so LCD row 0 alone cycles through enough information to
troubleshoot when the encoder cannot navigate and lower LCD rows are not
visible.

The later Tier 3 gate authorized only COM6 write-flash and separate
verify-flash of the staged `PF0530B` image after the user supplied fresh
`FLASH APPROVED` and `SAFE STATE CONFIRMED`. No serial monitor, wiring,
XBee/RF action, relay GPIO write, relay-expander write, load, mains, erase,
decoder acceptance, hardware acceptance, or final pin reassignment is opened
by this record.

## Sources

- ESP-IDF GPIO constraints: `SRC-ESP-IDF-GPIO`.
- Selected KY-040 ASIN mirror:
  `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`.
- KY-040 module-family pullup/switch behavior:
  `SRC-ENVISTIA-KY040-GUIDE-2026-05-30`.
- Prior GPIO13 and pin-finder diagnostic records:
  `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`,
  `SRC-LOCAL-FOUR-RELAY-KY040-PIN-FINDER-DIAGNOSTIC-2026-05-30`.
- Same-session PF0530B flash evidence:
  `research/bench-records/xbee-readonly/local-ky040-row0-pf0530b-flash-20260530T161450Z/`.

## Verified Facts

- ESP-IDF GPIO documentation states GPIO34-39 do not have software-enabled
  pull-up/down support.
- The previous `PF0530A` diagnostic sampled GPIO34, GPIO35, GPIO13, GPIO14,
  GPIO32, and GPIO33 as input-only probes.
- GPIO34, GPIO35, GPIO14, GPIO32, and GPIO33 remain configured as inputs with
  internal pulls disabled. GPIO13 remains the only internally pulled-up input.
- The user reported only pin 34 was displayed, so the previous row layout was
  insufficient for the observed LCD/encoder failure mode.
- The `PF0530B` refactor cycles raw A/B/SW levels, raw transition counters,
  and each GPIO probe level/change-count view on LCD row 0.
- The COM6 `PF0530B` flash gate matched ESP32-D0WDQ6, MAC
  `78:e3:6d:0a:90:14`, 4 MB flash, and 3.3 V flash voltage before mutation.
- The same gate completed 2 MB and 4 MB rollback reads, artifact hashes,
  recovery command, write-flash with per-segment hash verification, and
  separate verify-flash digest matches.
- After the flash, the user reported no change on any displayed `PF0530B`
  pins.

## Assumptions

- LCD row 0 is the only reliable display surface for the next user test.
- The current no-change symptom remains hardware/electrical/pinout first, not
  a quadrature decoder failure.
- GPIO14/GPIO32/GPIO33 are temporary input-only probes; a changing count is a
  clue for continuity review, not final wiring evidence.

## Unknowns

- Exact bench KY-040 markings, onboard resistor values, pullup voltage, module
  rail current, and exact 3.3 V behavior.
- Continuity from KY-040 `CLK`/`DT`/`SW` to GPIO34/GPIO35/GPIO13.
- Whether any encoder signal is landing outside the `PF0530B` six-pin set.
- Why the displayed `PF0530B` pins did not change.

## Firmware Boundary

- `main/main.c` remains the only ESP-IDF firmware file changed.
- UART0 host `115200`, UART2 XBee `9600` on GPIO17/GPIO16, LCD I2C0
  GPIO21/GPIO22, decoder constants, menu pages, and locked relay UI text remain
  in place.
- LCD row 0 cycles once per second through:
  - raw A/B/SW levels,
  - raw A/B and SW transition counters,
  - GPIO34, GPIO35, GPIO13, GPIO14, GPIO32, and GPIO33 live level/change
    count lines.
- Rows 1-3 keep the paired pin-finder summary for full-LCD observations.
- The display counts are modulo-sized for LCD fit only; any count change needs
  power-off continuity confirmation before wiring changes.

## Reviewer Quorum

- Governance/Agent Operations, weight 5: approved bounded repo mutation and
  blocked live flash until Tier 3 preconditions are satisfied.
- Firmware/Hardware/Evidence lenses, weight 3 each in the governance summary:
  approved the row-0 scanner as diagnostic-only.
- QA, weight 3: approved repo-only mutation and required refreshed validation.
- Live-bench reviewer, weight 5: blocked write-flash until fresh `FLASH
  APPROVED` and `SAFE STATE CONFIRMED` for this new image; that blocker was
  cleared by same-session user authority/safe-state and current identity,
  rollback, hash, and recovery evidence.

Weighted disposition: repo mutation approved; later named COM6-only
write/verify gate completed after blocker clearance.

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
- `git diff --check`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-pf0530b-row0-build build`

The ESP-IDF no-flash build generated
`/tmp/esp32-four-relay-xbee-wifi-pf0530b-row0-build/four_relay_xbee_wifi.bin`.

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
- `host-static-validation.txt`: refreshed local validation.
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
- `user-pf0530b-no-change-observation.txt`: user-reported no-change result.

## Decision Footer

- Decision: superseded_by_gpio_sweep_contact_tracer.
- Next gate: repo-only `PF0530C` GPIO sweep contact-tracer validation, then a
  fresh Tier 3 PF0530C flash gate only if requested.
- Owner: Firmware with Hardware, QA, and Agent Operations lenses.
- Evidence: source-backed GPIO constraints, prior diagnostic records, reviewer
  quorum, and local validation.
- Authority limits: no further flash, serial monitor/write, XBee/RF, relay
  GPIO write, relay-expander write, XBee setting write, relay/load/mains,
  erase, decoder acceptance, hardware acceptance, final pin reassignment,
  commit, or push.
