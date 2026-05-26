# Task 0054: Custom Wireless Protocol Gate F Firmware ABI Planning

Date: 2026-05-26

Status: Completed - owner review pending

## Scope

Create a docs-only Gate F owner-review package for the ESP-NOW BBS custom
wireless protocol firmware ABI.

## Verified Facts

- Gate E is a draft bridge ABI candidate, not final firmware ABI.
- Gate G is accepted only as a local-admin redacted JSON export under
  `ADR-0005`.
- Gate H structured live acceptance is accepted for the existing
  serial-nullmodem path and does not accept firmware ABI runtime behavior.
- The Gate F package added proposed ADR
  `.agents/DECISIONS/ADR-0006-espnow-bbs-firmware-abi.md`.
- The Gate F package added source ledger
  `knowledge-base/source-ledger/2026-05-26-custom-wireless-protocol-gate-f-firmware-abi.md`.

## Assumptions

- The next useful Gate F action is owner review of the proposed ADR, not
  firmware runtime migration.
- The existing simulator constants are the appropriate candidate seed for owner
  review.

## Unknowns

- `ADR-0006` is not accepted.
- Firmware queue depth, timeout, retry, scheduler, persistence, migration, and
  recovery policy are not accepted.
- No live firmware runtime proof exists for Gate F.

## Actions

- Added a proposed firmware ABI ADR for Gate F owner review.
- Added a Gate F source ledger.
- Updated documentation and research indexes/status records to point at the
  proposed Gate F package.
- Left runtime, live hardware, serial write, export-control, flash, erase,
  monitor, BLE, mesh, PCAP, relay/XBee, TFT, MicroSD, load, and mains gates
  closed.

## Validation

- PASS: `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: `git diff --check`

## Handoff

- `.agents/handoffs/0043-custom-wireless-protocol-gate-f-firmware-abi-to-owners.md`
