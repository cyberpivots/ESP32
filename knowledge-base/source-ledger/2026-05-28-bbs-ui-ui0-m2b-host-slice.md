# BBS UI UI-0/M2-B Host-Only Slice Source Ledger - 2026-05-28

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-BBS-UI-UI0-M2B-HOST-SLICE-2026-05-28`
- `SRC-LOCAL-BBS-UI-SYSTEM-OPERATION-PROGRAM-2026-05-28`
- `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`

## Purpose

Record the source basis for starting the BBS UI System Operation Improvement
Program with UI-0 and M2-B as host-only paired ESP32/DOS-C evidence slices.

## Verified Facts

- [repo-verified] The accepted BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- [repo-verified] UI-0 and M2-B were the planned next host-only/source-backed
  slices under the BBS UI System Operation Improvement Program.
- [repo-verified] DOS-C commit `7f0b5df` adds Network/Services wording and a
  source test for host-only/read-only/512-byte/schema/no-serial-ABI boundaries.
- [repo-verified] DOS-C commit `7819b93` refreshes the BBS records after a
  later unrelated offgrid submodule pointer update allowed the broad DOS-C
  scaffold check to pass.
- [repo-verified] DOS-C `m2a.discovery.v1` is companion output derived from
  the ESP32 host `mesh_discovery.v1` contract. This slice does not change
  `mesh_discovery.v1`.
- [repo-verified] The slice keeps runtime public APIs, firmware ABI, bridge
  ABI, coordinator serial ABI, Gate F service codes, and Win31 transport
  unchanged.

## Assumptions

- UI-0 can be accepted as a ranked source-backed packet without fresh copied
  screenshot evidence.
- M2-B can be accepted as host-only UX/source proof because it validates the
  existing DOS-C M2-A bridge/operator surface, not live firmware or radio work.

## Unknowns

- No fresh screenshot/OCR/CV packet, browser proof, selected-board evidence,
  live mesh proof, BLE proof, Android proof, router/admin proof, firmware
  mapping review, flash proof, serial-write proof, relay/XBee/TFT/MicroSD
  proof, load/mains proof, dummy-output proof, release proof, or cleanup proof
  exists for this slice.

## Reviewer Quorum

Read-only reviewer quorum ran before mutation. The repository stores this
summary, not raw subagent transcripts.

- Governance cartographer: no P1/P2 blockers if UI-0/M2-B use a new
  task/handoff/source record and stay host-only.
- UI/protocol analyst: no P1/P2 blockers; distinguish DOS-C
  `m2a.discovery.v1` companion output from ESP32 `mesh_discovery.v1`.
- QA validation reviewer: P2 until Pages validation and paired DOS-C host
  evidence are included. This slice includes both in the validation plan.

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_github_pages.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_public_manifest.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_github_pages.py`
- Changed-file source-ID scan.
- Changed-file Markdown link check.
- Closed-surface scan.
- `git diff --check`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (9 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py` (32 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py` (10 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_github_pages.py` (64 public files)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_public_manifest.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_github_pages.py`
- PASS: changed-file source-ID scan over 10 Markdown files.
- PASS: changed-file Markdown link check over 10 Markdown files.
- PASS: closed-surface scan reviewed expected hits in verified-fact,
  unknown, remaining-gap, QA-focus, or stop-gate context.
- PASS: `git diff --check`

## Stop Gates

This slice does not authorize runtime public API changes, firmware ABI changes,
bridge ABI changes, coordinator serial ABI changes, Gate F service-code
changes, `mesh_discovery.v1` schema changes, Win31 transport changes, live
browser proof, firmware runtime migration, prepare/flash/complete, erase,
monitor, physical serial writes, serial-write expansion, BLE pairing, live
ESP-WIFI-MESH, Android app behavior, PCAP, router/admin mutation, relay, XBee
writes, TFT, MicroSD, load, mains, release gating, dummy-output control, or
cleanup acceptance.
