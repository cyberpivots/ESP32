# Custom Wireless Protocol Phase 5/6 Runtime Design Review Source Ledger

Date: 2026-05-26

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-PHASE-5-6-RUNTIME-DESIGN-REVIEW-2026-05-26`

## Sources Used

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-GOLDEN-VECTORS-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-RUNTIME-REQUIREMENTS-2026-05-26`
- `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`

## Scope

Host-only Phase 5 runtime design review and Phase 6 simulator runtime
prototype for the ESP-NOW BBS custom wireless protocol.

This task does not add coordinator or peer firmware runtime code, does not wire
packet jobs into firmware runtime, and does not run live hardware.

## Verified Facts

- [repo-verified] Added accepted `ADR-0008` for host-only Phase 5/6 runtime
  design review.
- [repo-verified] Added `espnow_bbs_runtime.py` with bounded host runtime
  defaults, atomic packet-job admission, deterministic dispatch order,
  retry/expiry handling, duplicate handling, bridge-visible counters, and
  non-executing `control_intent`.
- [repo-verified] Host tests pin queue-full behavior, 16-fragment admission,
  17-fragment rejection, ACK dispatch priority, retry-limit terminal failure,
  expiry, duplicate dropping, bridge-line rejection, and runtime counters.
- [repo-verified] Firmware runtime implementation, persistence, serial writes,
  bridge export requests, Win31 export controls, flash, erase, monitor, BLE,
  mesh, PCAP, relay/XBee, TFT, MicroSD, load, mains, and live proof remain
  closed.

## Assumptions

- [assumption] Balanced host defaults are acceptable simulator defaults for
  design review and future implementation comparison.
- [assumption] Firmware memory budgets and task ownership must be measured in a
  later implementation gate before C runtime code is accepted.

## Unknowns

- [unknown] No coordinator or peer firmware runtime has implemented this host
  runtime design.
- [unknown] No live proof packet has exercised Phase 6 host runtime behavior on
  ESP32 firmware.
- [unknown] Persistence, migration/versioning, retention, wear policy, and
  recovery behavior are not accepted.

## Validation

- PASS: `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: `git diff --check`

## Result

Phase 5/6 now has a host-only runtime design and simulator prototype. Firmware
runtime, bridge/operator mutation, live proof, and hardware mutation remain
closed.

## Stop Gates

Do not use this host-only package to authorize coordinator runtime migration,
peer runtime migration, firmware queue persistence, serial writes, bridge export
requests, Win31 export controls, flash, erase, monitor, BLE, ESP-WIFI-MESH,
PCAP, router/admin mutation, relay, XBee, TFT, MicroSD, load, mains, or live
proof work.
