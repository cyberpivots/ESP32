# Task 0058: Custom Wireless Protocol Phase 5/6 Runtime Design Review

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-26

## Goal

Accept Phase 5 runtime design-review defaults and add a Phase 6 host-only
runtime prototype for the ESP-NOW BBS custom wireless protocol.

This task does not add coordinator or peer firmware runtime code, does not run
live hardware, and does not open serial-write, flash, export-control, BLE/mesh,
PCAP, relay/XBee/TFT/MicroSD/load/mains, or bridge/operator runtime behavior.

## Verified Facts

- `ADR-0007` accepts runtime requirements only.
- The accepted packet ABI, service codes, custody codes, packet budgets, and
  golden vectors remain under `ADR-0006`.
- The runtime prototype is host-only simulator code under
  `tools/simulators/custom_wireless_protocol/`.
- `control_intent` remains non-executing and report-only.

## Assumptions

- Balanced host defaults are suitable for simulator proof and later owner
  review, but they are not measured firmware memory budgets.
- Volatile runtime state remains the only accepted state model for this gate.

## Unknowns

- No ESP32 firmware runtime implementation or live runtime proof exists for the
  Phase 6 host prototype.
- Firmware memory budget, task ownership, persistence, migration, recovery, and
  wear policy remain unresolved.

## Implementation

- Added accepted `ADR-0008` for Phase 5/6 runtime design review.
- Added `espnow_bbs_runtime.py` as a host-only runtime scheduler model around
  the existing simulator.
- Added host tests for default runtime values, queue backpressure, atomic file
  admission, ACK priority, retry limit failure, expiry, duplicate dropping,
  non-executing `control_intent`, bridge-line rejection, and visible counters.
- Added durable source ledger/source-index coverage for
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-PHASE-5-6-RUNTIME-DESIGN-REVIEW-2026-05-26`.

## Validation

- PASS: `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: `git diff --check`

## Handoff

Continue with
[../handoffs/0047-custom-wireless-protocol-phase-5-6-runtime-design-review-to-qa.md](../handoffs/0047-custom-wireless-protocol-phase-5-6-runtime-design-review-to-qa.md).

## Stop Gates

Do not use this host-only prototype to authorize coordinator runtime migration,
peer runtime migration, firmware queue persistence, serial writes, bridge export
requests, Win31 export controls, flash, erase, monitor, BLE, ESP-WIFI-MESH,
PCAP, router/admin mutation, relay, XBee, TFT, MicroSD, load, mains, or live
proof work.
