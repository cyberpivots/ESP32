# Handoff 0072: BBS UI UI-0/M2-B Host-Only Slice To QA

Date: 2026-05-28

Task:
[../TASK_LOG/0083-bbs-ui-ui0-m2b-host-slice.md](../TASK_LOG/0083-bbs-ui-ui0-m2b-host-slice.md)

## Current State

- UI-0 now has a ranked source-backed operator-facing improvement packet.
- M2-B now has host-only Network/Services UX proof tied to DOS-C commit
  `7f0b5df`.
- DOS-C `m2a.discovery.v1` is recorded as companion output derived from the
  ESP32 host `mesh_discovery.v1` contract. `mesh_discovery.v1` is unchanged.
- The accepted serial-nullmodem path remains unchanged:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## QA Focus

1. Confirm public Pages validation passes after the source-index update.
2. Confirm UI-0 and M2-B records stay host-only and do not claim screenshot,
   browser, live mesh, BLE, firmware mapping, or cleanup acceptance.
3. Confirm future M3 is design-only firmware mapping review and not a live
   mesh or runtime firmware gate.
4. Confirm future Client-1 starts with static/simulated or read-only browser
   evidence only.
5. Confirm future Client-2 requires a separate Tier 3 selected-board gate with
   same-session identity, power/voltage/boot-pin/isolation, recovery, browser
   evidence, and cleanup.

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

## Validation Recorded

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_github_pages.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_public_manifest.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_github_pages.py`
- PASS: changed-file source-ID scan.
- PASS: changed-file Markdown link check.
- PASS: closed-surface scan reviewed expected closed/future/no-authority hits.
- PASS: `git diff --check`

## Stop Gates

Do not use this slice to authorize runtime public API changes, firmware ABI
changes, bridge ABI changes, coordinator serial ABI changes, Gate F service-code
changes, `mesh_discovery.v1` schema changes, Win31 transport changes, live
browser proof, firmware runtime migration, prepare/flash/complete, erase,
monitor, serial-write expansion, BLE pairing, live ESP-WIFI-MESH, Android app
behavior, PCAP, router/admin mutation, relay, XBee writes, TFT, MicroSD, load,
mains, release gating, dummy-output control, or cleanup acceptance.
