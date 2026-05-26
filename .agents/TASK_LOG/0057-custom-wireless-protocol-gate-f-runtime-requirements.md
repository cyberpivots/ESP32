# Task 0057: Custom Wireless Protocol Gate F Runtime Requirements

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-26

## Goal

Accept a host-only Gate F runtime requirements owner gate for a future ESP-NOW
BBS custom wireless protocol firmware runtime implementation.

This task does not add coordinator or peer runtime code, does not run live
hardware, and does not open serial-write, flash, export-control, BLE/mesh, PCAP,
relay/XBee/TFT/MicroSD/load/mains, or bridge-runtime behavior.

## Verified Facts

- `ADR-0006` is accepted as a firmware ABI design contract only.
- Gate F packet golden vectors cover all accepted service codes and full
  encoded bytes.
- The simulator models bounded packet bodies, fragment limits, custody states,
  retry eligibility, missing-fragment failure, and non-executing
  `control_intent`.
- The accepted serial-nullmodem BBS path and Pi bridge custody/export boundary
  remain unchanged.

## Assumptions

- A future runtime implementation should begin from volatile firmware state
  only because the Pi bridge owns durable BBS custody.
- Exact queue depths, timeout values, retry counts, scheduler priorities, and
  memory budgets require a separate implementation review.

## Unknowns

- No coordinator or peer firmware runtime has implemented Gate F packet queues,
  scheduler behavior, persistence, migration, or recovery.
- No live proof packet has exercised Gate F runtime requirements.

## Implementation

- Added accepted requirements-only ADR
  `.agents/DECISIONS/ADR-0007-espnow-bbs-gate-f-runtime-requirements.md`.
- Added host-only tests for custody retry/terminal semantics, retry-limit
  behavior, missing-fragment failure, and non-executing `control_intent`.
- Added source ledger and source-index coverage for
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-RUNTIME-REQUIREMENTS-2026-05-26`.
- Updated docs index, development status, known gaps, triage status, and the
  custom wireless protocol brief.

## Validation

- PASS: `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: `git diff --check`

## Handoff

Continue with
[../handoffs/0046-custom-wireless-protocol-gate-f-runtime-requirements-to-dosc.md](../handoffs/0046-custom-wireless-protocol-gate-f-runtime-requirements-to-dosc.md).

## Stop Gates

Do not use this requirements gate to authorize coordinator runtime migration,
peer runtime migration, serial writes, bridge export requests, Win31 export
controls, flash, erase, monitor, BLE, ESP-WIFI-MESH, PCAP, router/admin
mutation, relay, XBee, TFT, MicroSD, load, mains, or live proof work.
