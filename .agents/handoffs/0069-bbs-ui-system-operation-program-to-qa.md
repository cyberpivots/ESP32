# Handoff 0069: BBS UI System Operation Program To QA

Date: 2026-05-28

Task:
[../TASK_LOG/0080-bbs-ui-system-operation-program.md](../TASK_LOG/0080-bbs-ui-system-operation-program.md)

## Current State

- `research/development-plan.md` now contains the BBS UI System Operation
  Improvement Program inside the singular tracked plan.
- The program is Tier 2 documentation/status/source-record routing only.
- `research/skills/available-skills.md` now records the current `be69e54e`
  plugin cache paths and ESP32-local live-gate/vision-gate skills.
- The accepted serial-nullmodem path remains unchanged:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## QA Focus

1. Confirm future UI-0 and M2-B work stays host-only unless a separate gate
   opens a narrower surface.
2. Confirm `discovery_snapshot`, `discovery_events`, `service_catalog`, and
   `capability_report` remain read-only summaries bounded to the existing
   512-byte bridge line limit.
3. Confirm future M2-B records do not expand coordinator serial ABI or Gate F
   radio service codes.
4. Confirm screenshot/OCR/CV evidence remains corroboration only and transcript
   proof remains authoritative for BBS behavior.
5. Confirm Client-1 browser work starts static/simulated or read-only, and
   Client-2 live selected-board proof requires a future Tier 3 gate with
   identity, power/voltage/boot-pin/isolation, recovery, browser evidence, and
   cleanup.

## Validation Recorded

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`
- PASS: changed-file source-ID scan.
- PASS: changed-file Markdown link check.
- PASS: `git diff --check`

## Stop Gates

Do not use this program to authorize runtime public API changes, firmware ABI
changes, bridge ABI changes, coordinator serial ABI changes, Gate F service-code
changes, `mesh_discovery.v1` schema changes, Win31 transport changes, live
browser proof, firmware runtime migration, prepare/flash/complete, erase,
monitor, serial-write expansion, BLE pairing, live ESP-WIFI-MESH, Android app
behavior, PCAP, router/admin mutation, relay, XBee writes, TFT, MicroSD, load,
mains, release gating, or cleanup acceptance.
