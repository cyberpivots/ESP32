# Custom Wireless Protocol Gate F Firmware ABI Source Ledger

Date: 2026-05-26

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-FIRMWARE-ABI-2026-05-26`

## Sources Used

- `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIEF-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIDGE-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-D-DOSC-PAIRING-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-E-BRIDGE-ABI-2026-05-25`
- `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-IMPLEMENTATION-2026-05-25`
- `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`
- `SRC-ESP-IDF-ESPNOW`

## Scope

Docs-only Gate F owner-review package for a proposed ESP-NOW BBS firmware ABI.

This task does not add firmware runtime code, does not wire packet jobs into
coordinator or peer firmware, and does not run live hardware.

## Verified Facts

- [repo-verified] Added proposed ADR
  `.agents/DECISIONS/ADR-0006-espnow-bbs-firmware-abi.md`.
- [repo-verified] The proposed ADR keeps Gate F `design-only` until owner
  acceptance.
- [repo-verified] The proposed ADR mirrors existing simulator constants for
  protocol version `1`, 512-byte bridge frames, 250-byte ESP-NOW v1-compatible
  radio packets, 32-byte headers, 190-byte bodies, and 16 fragments.
- [repo-verified] The proposed ADR mirrors existing simulator service code
  meanings for `direct_message`, `file_chunk`, `telemetry_report`,
  `node_status`, `custody_ack`, and `control_intent`.
- [repo-verified] The proposed ADR mirrors existing simulator custody code
  meanings for `none`, `queued`, `sent`, `delivered`, `acked`, `failed`, and
  `expired`.
- [repo-verified] Gate F does not add a Win31 export control, live bridge
  export request type, firmware analytics export ABI, serial write, flash,
  erase, monitor, BLE, mesh, PCAP, relay/XBee, TFT, MicroSD, load, or mains
  behavior.

## Assumptions

- [assumption] The simulator constants are the appropriate candidate ABI seed
  because they have local ESP32 host-test coverage and DOS-C fixture replay.
- [assumption] Firmware runtime migration should begin only after owner review
  accepts or replaces the proposed ADR.
- [assumption] The Pi bridge remains the durable BBS custody/export boundary
  unless a later accepted ADR changes that architecture.

## Unknowns

- [unknown] No accepted final firmware ABI exists.
- [unknown] Queue depths, memory budgets, timeout values, retry counts,
  scheduler priority, backpressure policy, firmware persistence format, flash
  wear policy, migration/versioning policy, and recovery behavior are not
  accepted.
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

Gate F now has a proposed ESP32 owner-review package. It remains design-only
until `ADR-0006` is accepted or replaced.

## Stop Gates

Do not use this planning package to authorize coordinator runtime migration,
peer runtime migration, serial writes, bridge export requests, Win31 export
controls, flash, erase, monitor, BLE, ESP-WIFI-MESH, PCAP, router/admin
mutation, relay, XBee, TFT, MicroSD, load, mains, or live proof work.
