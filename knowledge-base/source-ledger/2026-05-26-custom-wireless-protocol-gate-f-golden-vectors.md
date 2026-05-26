# Custom Wireless Protocol Gate F Golden Vectors Source Ledger

Date: 2026-05-26

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-GOLDEN-VECTORS-2026-05-26`

## Sources Used

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-FIRMWARE-ABI-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-E-BRIDGE-ABI-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-D-DOSC-PAIRING-2026-05-25`
- `SRC-ESP-IDF-ESPNOW`

## Scope

Host-only golden-vector assurance for the accepted Gate F firmware ABI design
contract.

This task does not add firmware runtime code, does not wire packet jobs into
coordinator or peer firmware, and does not run live hardware.

## Verified Facts

- [repo-verified] Added a full packet golden-vector table to
  `tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`.
- [repo-verified] The table covers `direct_message`, `file_chunk`,
  `telemetry_report`, `node_status`, `custody_ack`, and `control_intent`.
- [repo-verified] Each vector asserts both `encode_packet(packet).hex()` and
  `decode_packet(bytes.fromhex(hex))`.
- [repo-verified] The vectors pin the accepted `ADR-0006` packet byte layout:
  version, service code, flags, TTL, sequence number, message ID, fragment
  index, fragment count, source node, destination node, body length, custody
  status, and body bytes.
- [repo-verified] Gate F remains a design contract only and does not add a
  firmware runtime queue, persistence store, scheduler, bridge export request,
  Win31 export control, serial write, flash, erase, monitor, BLE, mesh, PCAP,
  relay/XBee, TFT, MicroSD, load, or mains behavior.

## Assumptions

- [assumption] Golden vectors are the appropriate host-only assurance artifact
  before any runtime implementation gate.
- [assumption] DOS-C companion checks should verify source/ABI parity without
  changing live bridge or Win31 operator behavior.

## Unknowns

- [unknown] Queue depths, memory budgets, timeout values, retry counts,
  scheduler priority, backpressure policy, firmware persistence format, flash
  wear policy, migration/versioning policy, and recovery behavior are not
  accepted.
- [unknown] No coordinator or peer firmware runtime has implemented this ABI.
- [unknown] No live firmware runtime proof exists for Gate F packet jobs,
  queues, persistence, scheduler behavior, migration, or failure handling.

## Validation

- PASS: `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: `git diff --check`

## Result

Gate F now has host-only packet golden vectors for all accepted service codes.
Firmware runtime, bridge export, Win31 export control, live proof, and hardware
mutation remain closed.

## Stop Gates

Do not use this assurance package to authorize coordinator runtime migration,
peer runtime migration, serial writes, bridge export requests, Win31 export
controls, flash, erase, monitor, BLE, ESP-WIFI-MESH, PCAP, router/admin
mutation, relay, XBee, TFT, MicroSD, load, mains, or live proof work.
