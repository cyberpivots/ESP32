# Remote LCD XBee Solar Client Source Ledger

Date: 2026-05-26

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`

## Sources used

- `SRC-DIGI-XBP9B-DPUT-001`
- `SRC-DIGI-XBEE-PRO-900HP`
- `SRC-DIGI-XBEE-900HP-USER-GUIDE`
- `SRC-DIGI-XBEE-900HP-AP`
- `SRC-DIGI-XBEE-900HP-AO`
- `SRC-DIGI-XBEE-900HP-DELIVERY`
- `SRC-DIGI-XBEE-900HP-NP`
- `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`
- `SRC-NXP-PCF8574-74A`
- `SRC-BOURNS-PEC11R`
- `SRC-TI-BQ25185`
- `SRC-TI-BQ2970`
- `SRC-TI-BQ27441-G1`
- `SRC-UL-LIION-SAFETY`
- `SRC-ESP-IDF-GPIO`
- `SRC-ESP-IDF-UART`
- `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`

## Scope

Documentation-only scaffold for `remote-lcd-xbee-solar-client`.

This initial scaffold added no firmware source, framework files, XBee writes,
API transmit frames, ESP32 DIN/DOUT wiring, battery charging, solar wiring, or
bench action. Follow-on source ID
`SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26` records
the later private Git submodule implementation.

## Verified facts

- [repo-verified] Added project docs under
  `docs/projects/remote-lcd-xbee-solar-client/`.
- [repo-verified] Added hardware profile stubs for the 20x4 I2C LCD, rotary
  encoder, ESP32 client node, 18650 cell, BMS/protection, and solar
  charger/power path.
- [repo-verified] Reused existing XBee source coverage and preserved the
  read-only XBee gate.
- [source-verified] New source-index entries are candidate/reference-only for
  PCF8574/74A, PEC11R, BQ25185, BQ2970, BQ27441-G1, and UL lithium-ion safety
  guidance.
- [repo-verified] Exact LCD module, encoder, ESP32 board, 18650 cell, BMS
  board, solar panel, charger module, carrier, antenna, fuse/protection, and
  enclosure remain unresolved.

## Assumptions

- [superseded] The first scaffold treated requested submodules as internal
  monorepo module lanes. Follow-on task 0060 created real private Git
  submodules.
- [assumption] This lane is distinct from `four-relay-xbee-wifi`.

## Unknowns

- [unknown] No exact local hardware identity packet exists for this lane.
- [unknown] No power budget, pin map, firmware framework, XBee carrier, antenna,
  charger/power-path design, or enclosure design is accepted.
- [unknown] No live bench proof exists for this lane.

## Validation

- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: `git diff --check`

## Stop gates

Do not use this scaffold to authorize firmware implementation, framework
selection, XBee writes, API transmit frames, ESP32 DIN/DOUT wiring, battery
charging, solar connection, battery pack assembly, or power-path wiring.
