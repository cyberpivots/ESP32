# Custom Wireless Protocol Gate F Owner-Review Source Ledger

Date: 2026-05-26

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`

## Sources Used

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-FIRMWARE-ABI-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-E-BRIDGE-ABI-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-D-DOSC-PAIRING-2026-05-25`
- `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-IMPLEMENTATION-2026-05-25`
- `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`
- `SRC-ESP-IDF-ESPNOW`

## Scope

Gate F owner-review quorum and host-only ABI freeze for the ESP-NOW BBS custom
wireless protocol firmware ABI design contract.

This task does not add firmware runtime code, does not wire packet jobs into
coordinator or peer firmware, and does not run live hardware.

## Review Quorum

- Governance/docs review: PASS, no P1/P2 blockers.
- Evidence-boundary review: PASS, no P1/P2 blockers.
- Protocol/ABI review: PASS, no P1/P2 blockers.
- QA review: PASS, no P1/P2 blockers.

## Verified Facts

- [repo-verified] `ADR-0006` is accepted as a design contract only.
- [repo-verified] The accepted contract preserves simulator constants for
  protocol version `1`, 512-byte bridge frames, 250-byte ESP-NOW v1-compatible
  radio packets, 32-byte headers, 190-byte bodies, and 16 fragments.
- [repo-verified] The accepted contract preserves simulator service code
  meanings for `direct_message`, `file_chunk`, `telemetry_report`,
  `node_status`, `custody_ack`, and `control_intent`.
- [repo-verified] The accepted contract preserves simulator custody code
  meanings for `none`, `queued`, `sent`, `delivered`, `acked`, `failed`, and
  `expired`.
- [repo-verified] Host-only tests now pin bridge request-set membership,
  service/custody code maps, frame budgets, packet header byte offsets, and
  packet header field ordering.
- [repo-verified] Gate F does not add a Win31 export control, live bridge export
  request type, firmware analytics export ABI, serial write, flash, erase,
  monitor, BLE, mesh, PCAP, relay/XBee, TFT, MicroSD, load, or mains behavior.

## Assumptions

- [assumption] The simulator constants are the appropriate ABI seed because they
  have local ESP32 host-test coverage and DOS-C fixture replay.
- [assumption] Firmware runtime migration should begin only after a separate
  owner gate accepts queue, scheduler, persistence, migration, recovery, and
  live-proof requirements.
- [assumption] The Pi bridge remains the durable BBS custody/export boundary
  unless a later accepted ADR changes that architecture.

## Unknowns

- [unknown] Queue depths, memory budgets, timeout values, retry counts,
  scheduler priority, backpressure policy, firmware persistence format, flash
  wear policy, migration/versioning policy, and recovery behavior are not
  accepted.
- [unknown] No coordinator or peer firmware runtime has implemented this ABI.
- [unknown] No live firmware runtime proof exists for Gate F packet jobs, queues,
  persistence, scheduler behavior, migration, or failure handling.

## Validation

- PASS: `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: `git diff --check`

## Result

Gate F has an accepted firmware ABI design contract only. Firmware runtime,
bridge export, Win31 export control, live proof, and hardware mutation remain
closed.

## Stop Gates

Do not use this owner-review package to authorize coordinator runtime migration,
peer runtime migration, serial writes, bridge export requests, Win31 export
controls, flash, erase, monitor, BLE, ESP-WIFI-MESH, PCAP, router/admin
mutation, relay, XBee, TFT, MicroSD, load, mains, or live proof work.
