# Task Log 0038 - Custom Wireless Protocol Brief

## Task

- ID: 0038-custom-wireless-protocol-brief
- Owner role: Communications, Architect, QA
- Status: implemented as documentation-only Gate A
- Created: 2026-05-25
- Updated: 2026-05-25
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Create a verified research/design brief for a custom wireless protocol model
that separates streaming BBS integration from packetized radio services while
preserving the accepted OPCON/COM1/nullmodem/Pi bridge/coordinator path.

## Scope

Included:

- `docs/projects/espnow-bbs/custom-wireless-protocol-brief.md`
- `knowledge-base/source-ledger/2026-05-25-custom-wireless-protocol-brief.md`
- Source-index rows for the local brief and official/vendor ag telemetry
  sources.
- Known-gap updates for direct messaging, file transfer, telemetry, ag
  hardware profiles, GPS tracking, and analytics policy.
- QA handoff for the simulator-first protocol proof gate.

Excluded:

- Firmware changes, live preflight, flashing, serial writes, bridge runtime
  mutation, radio setting changes, PCAP, router/admin work, relay, XBee, TFT,
  MicroSD, load, mains, BLE pairing, ESP-WIFI-MESH live action, erase, monitor,
  or framework migration.

## Sources

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIEF-2026-05-25`
- `SRC-ESP-IDF-ESPNOW`
- `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`
- `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`

## Validation

- Documentation-only implementation.
- No hardware commands, serial writes, flashing, radio setting changes, or live
  bridge commands were run.
- Validation commands are recorded in the final task response for the current
  execution turn.

## Handoff

Continue through
[../handoffs/0027-custom-wireless-protocol-to-qa.md](../handoffs/0027-custom-wireless-protocol-to-qa.md)
for simulator-first protocol proof and acceptance review.
