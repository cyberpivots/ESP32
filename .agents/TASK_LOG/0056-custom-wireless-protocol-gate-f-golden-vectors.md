# Task 0056: Custom Wireless Protocol Gate F Golden Vectors

Date: 2026-05-26

Status: Completed - host-only assurance

## Scope

Add host-only packet golden-vector coverage for the accepted Gate F firmware ABI
design contract.

This task does not add firmware runtime code, does not run live hardware, and
does not open serial writes, flash, erase, monitor, BLE, mesh, PCAP,
relay/XBee, TFT, MicroSD, load, or mains work.

## Verified Facts

- `ADR-0006` is accepted as a firmware ABI design contract only.
- The host-only packet vector table covers `direct_message`, `file_chunk`,
  `telemetry_report`, `node_status`, `custody_ack`, and `control_intent`.
- Each vector asserts `encode_packet(packet).hex()` and
  `decode_packet(bytes.fromhex(hex))`.
- The vectors pin service code, flags, TTL, sequence, message ID, fragment
  index/count, source node, destination node, body length, custody status, and
  payload bytes for one representative packet per Gate F service.

## Assumptions

- The golden vectors are assurance fixtures for the simulator-derived ABI
  contract and should remain host-only until a separate runtime gate is
  accepted.
- Future DOS-C companion checks can read these same local ESP32 sources without
  changing bridge runtime behavior.

## Unknowns

- Firmware queue depths, memory budgets, timeout values, retry counts,
  scheduler priority, backpressure policy, persistence format, flash wear
  policy, migration/versioning policy, and recovery behavior remain unaccepted.
- No coordinator or peer firmware runtime has implemented the Gate F contract.
- No live Gate F runtime proof exists.

## Actions

- Added full packet golden-vector coverage to
  `tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`.
- Added source ledger
  `knowledge-base/source-ledger/2026-05-26-custom-wireless-protocol-gate-f-golden-vectors.md`.
- Updated `docs/index.md`, `knowledge-base/source-index.md`, and current status
  records to include the golden-vector assurance source.
- Kept runtime, live hardware, serial write, export-control, flash, erase,
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

- `.agents/handoffs/0045-custom-wireless-protocol-gate-f-golden-vectors-to-dosc.md`
