# Task Log 0036 - Cross-Project Client UI Live-Gate

## Task

- ID: 0036-client-ui-live-gate
- Owner role: Architect, Communications, QA
- Status: implemented as design-only live-gate plan
- Created: 2026-05-24
- Updated: 2026-05-24
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Add a source-backed cross-project live-gate plan for improving ESP32
hardware/software dashboard UX, prioritizing Wi-Fi browser clients on phone and
laptop while keeping BLE and Serial/UART as later fallback or parity paths.

## Scope

Included:

- Cross-project architecture document for Wi-Fi web first, BLE later, and
  Serial/UART later.
- Dummy-output-only first control authority with safety-lock, all-off, visible
  reject reasons, monotonic sequence, and source-transport logging rules.
- Minimum REST-style interface contract for `GET /api/state`,
  `POST /api/safety-lock`, `POST /api/all-off`, and
  `POST /api/dummy-output/{channel}`.
- Live-gate proof ladder from source-backed design through simulated UI,
  read-only Wi-Fi live proof, dummy-output proof, and later BLE/Serial parity
  plans.
- Source-index, source-ledger, known-gap, docs-index, and QA handoff updates.

Excluded:

- Firmware changes, framework files, web UI implementation, BLE code, Android
  app code, serial client code, live browser proof, live hardware mutation,
  firmware flash, firmware erase, monitor expansion, serial writes outside the
  accepted command path, relay, XBee, TFT, MicroSD, load, mains, PCAP,
  router-admin work, and replacement of the accepted Win31 serial-nullmodem
  proof path.

## Sources

- `SRC-ESP-IDF-HTTP-SERVER`
- `SRC-ESP-IDF-WIFI`
- `SRC-ESP-IDF-WIFI-PROVISIONING-2026-05-24`
- `SRC-ESP-IDF-BLE-API`
- `SRC-ANDROID-BLE-OVERVIEW`
- `SRC-MDN-WEB-SERIAL-2026-05-24`
- `SRC-MDN-WEB-BLUETOOTH-2026-05-24`
- `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`
- `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`
- `SRC-LOCAL-CLIENT-UI-LIVE-GATE-2026-05-24`

## Artifacts

- [../../docs/architecture/client-ui-live-gate.md](../../docs/architecture/client-ui-live-gate.md)
- [../../knowledge-base/source-ledger/2026-05-24-client-ui-live-gate.md](../../knowledge-base/source-ledger/2026-05-24-client-ui-live-gate.md)
- [../../research/known-gaps.md](../../research/known-gaps.md)
- [../../knowledge-base/source-index.md](../../knowledge-base/source-index.md)

## Validation

- `python3 scripts/verify_scaffold.py`
- `git diff --check`

## Handoff

Continue through
[../handoffs/0026-client-ui-live-gate-to-qa.md](../handoffs/0026-client-ui-live-gate-to-qa.md)
before implementing a static UI, firmware endpoint, BLE client, or Serial/UART
client.
