# Handoff 0076 - XCTU Install Proof To QA

## Current State

XCTU is installed on the Windows host as a reference GUI tool. The install gate
was host-tooling only: no serial port was opened, no XBee device was added or
discovered in XCTU, and no radio read/write/transmit/firmware/range-test action
was used.

## Evidence To Review

- `knowledge-base/source-ledger/2026-05-29-xctu-download-install.md`
- `docs/projects/four-relay-xbee-wifi/xbee-radio-programming-study.md`
- `scripts/xbee_radio_study.py`
- `tests/scaffold_audits/test_xbee_radio_study.py`
- Local ignored evidence under
  `research/bench-records/xctu-install/local-20260529T033010Z/`

## QA Focus

- Confirm public records include the installer SHA-256 and install outcome
  without publishing raw COM/PnP identifiers or screenshots.
- Confirm `inventory` detects per-user Windows `XCTU-NG` installs and still
  does not open serial ports.
- Confirm the Digi USB RF driver prompt is documented as host-driver software
  only, not as proof of XBee adapter identity.
- Confirm no new `apply`, serial-write, API transmit, firmware, or range-test
  path exists in the repo tooling.

## Still Blocked

Live adapter identity, read-only radio backup/readback, setting writes, `WR`,
`AC`, API transmit frames, firmware recovery/update, range tests, ESP32 carrier
wiring, relay/load/mains work, and live RF evidence remain blocked until a
future explicit Tier 3 gate.
