# Custom Wireless Protocol Gate F Runtime Requirements Source Ledger

Date: 2026-05-26

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-RUNTIME-REQUIREMENTS-2026-05-26`

## Sources Used

- `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-D-DOSC-PAIRING-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-E-BRIDGE-ABI-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-GOLDEN-VECTORS-2026-05-26`
- `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`
- `SRC-ESP-IDF-ESPNOW`

## Scope

Host-only Gate F runtime requirements for a future firmware runtime
implementation.

This task does not add firmware runtime code, does not wire packet jobs into
coordinator or peer firmware, and does not run live hardware.

## Verified Facts

- [repo-verified] Added accepted requirements-only `ADR-0007`.
- [repo-verified] `ADR-0007` requires bounded packet-job queues,
  bridge-visible backpressure/failure reasons, custody lifecycle rules,
  retry/expiry behavior, scheduler/backpressure requirements, volatile-only
  recovery, and live-proof prerequisites.
- [repo-verified] Firmware queue/custody persistence remains blocked behind a
  later persistence/wear-policy ADR.
- [repo-verified] Host tests pin custody retry eligibility, terminal custody
  states, retry-limit behavior, missing-fragment failure, and non-executing
  `control_intent`.
- [repo-verified] Gate F remains requirements-only and does not add coordinator
  runtime migration, peer runtime migration, serial writes, bridge export
  requests, Win31 export controls, flash, erase, monitor, BLE, mesh, PCAP,
  relay/XBee, TFT, MicroSD, load, mains, or live proof behavior.

## Assumptions

- [assumption] The first runtime implementation slice should use volatile
  firmware state only because the Pi bridge remains the durable BBS custody
  boundary.
- [assumption] Exact numeric queue, retry, timeout, and scheduler values should
  be selected during a future implementation review.

## Unknowns

- [unknown] Queue depths, memory budgets, timeout values, retry counts,
  scheduler priority, backpressure thresholds, firmware persistence format,
  flash wear policy, migration/versioning policy, and recovery behavior are not
  finalized.
- [unknown] No coordinator or peer firmware runtime has implemented these
  requirements.
- [unknown] No live firmware runtime proof exists for Gate F packet queues,
  scheduler behavior, retry/expiry, recovery, or failure handling.

## Validation

- PASS: `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: `git diff --check`

## Result

Gate F now has accepted runtime requirements for future implementation review.
Firmware runtime, bridge export, Win31 export control, live proof, and hardware
mutation remain closed.

## Stop Gates

Do not use this requirements package to authorize coordinator runtime migration,
peer runtime migration, serial writes, bridge export requests, Win31 export
controls, flash, erase, monitor, BLE, ESP-WIFI-MESH, PCAP, router/admin
mutation, relay, XBee, TFT, MicroSD, load, mains, or live proof work.
