# Custom Wireless Protocol Simulator Source Ledger

Date: 2026-05-25

## Sources Used

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIEF-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`
- `SRC-ESP-IDF-ESPNOW`

## Verified Facts

- [repo-verified] Gate B now has a local simulator-only model under
  `tools/simulators/custom_wireless_protocol/`.
- [repo-verified] The simulator enforces a 512-byte ASCII JSON bridge line
  boundary, v1-compatible 250-byte radio packet budget, 32-byte header,
  190-byte body, and 16-fragment maximum.
- [repo-verified] The simulator tests cover direct-message packets, file chunk
  fragmentation/resume, telemetry reports, node status, custody ACK, duplicate
  rejection, TTL expiry, non-executing control intents, and compact reporting
  frames.
- [repo-verified] `comm-protocols/custom/README.md` documents that the
  simulator keeps direct messages, file chunks, interval telemetry, node
  status, custody ACKs, and control intents packetized rather than streamed.

## Assumptions

- [assumption] The simulator mirrors the current conservative ESP-NOW
  v1-compatible payload budget until an accepted ADR expands the packet size.
- [assumption] The simulator is a test harness and does not define final
  firmware ABI, persistent schema, or live bridge command surface.

## Unknowns

- [unknown] No firmware implementation, physical coordinator behavior, live
  bridge transcript, or Win31/OPCON state was produced by this simulator task.
- [unknown] Agricultural telemetry profiles, GPS payloads, analytics retention,
  and selected hardware profiles remain blocked on source-backed records and
  owner review.

## Validation

- `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `python3 tools/simulators/custom_wireless_protocol/espnow_bbs_custom_protocol.py --demo`
- Additional validation is recorded in task
  `.agents/TASK_LOG/0039-custom-wireless-protocol-simulator.md`.

## Boundary Notes

- [non-goal] This ledger does not authorize flashing, serial writes, bridge
  runtime mutation, radio setting changes, PCAP, router/admin work, relay,
  XBee, TFT, MicroSD, load, mains, BLE pairing, ESP-WIFI-MESH live action,
  erase, monitor automation, or framework migration.
