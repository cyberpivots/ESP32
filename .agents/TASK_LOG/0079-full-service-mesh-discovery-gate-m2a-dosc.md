# Task 0079: Full-Service Mesh Discovery Gate M2-A DOS-C Companion

Status: implemented-host-only; validated with caveat

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-27

## Goal

Record the paired DOS-C Gate M2-A companion implementation for full-service
mesh discovery and move ESP32 planning status forward without opening live
mesh, BLE, Android, firmware runtime, router/admin, serial-write, PCAP, or
hardware surfaces.

## Verified Facts

- ESP32 checkpoint commit `4dec626` pushed the consolidated development routing
  before paired-repo mutation.
- DOS-C commit `62c4db6` adds host-only bridge/operator support for
  `discovery_snapshot`, `discovery_events`, `service_catalog`, and
  `capability_report`.
- The DOS-C implementation keeps responses ASCII, schema-versioned, read-only,
  deterministic, and bounded to the existing 512-byte bridge line budget.
- The DOS-C implementation did not extend `coordinator_protocol.py` or the
  Pi-to-ESP32 coordinator serial ABI.
- The Win31 operator surface formats and parses the four discovery request
  types and shows read-only Network/Services status.

## Assumptions

- Gate M2-A is Tier 2 host-only paired-repo record work.
- DOS-C commit `62c4db6` is the durable proof reference for ESP32 planning
  status until a later source-indexed DOS-C change supersedes it.

## Unknowns

- No live ESP-WIFI-MESH route-table, parent, root, healing, coexistence,
  flash, serial, or cleanup proof exists.
- No BLE UUID, Android package, permission, bonding/SMP, coexistence, or live
  GATT proof exists.
- No firmware mapping from ESP-WIFI-MESH APIs/events into `mesh_discovery.v1`
  is accepted.
- No current same-session hardware identity, no-load state, listener/process
  inventory, or recovery proof was captured by this task.

## Reviewer Quorum

Project-local read-only reviewer quorum was used before paired-repo mutation.
The repository records the quorum summary, not raw subagent transcripts.

- Governance reviewer: no P1/P2 blocker if ESP32 consolidation was checkpointed
  before Gate M2-A and the work stayed host-only.
- Evidence reviewer: no P1 blocker; required durable DOS-C and paired ESP32
  records.
- UI/protocol reviewer: no P1 blocker; required read-only Win31-to-Pi bridge
  surface, schema versioning, capped discovery events, and no coordinator
  serial ABI expansion.

## Mutation Boundary

- `.agents/TASK_LOG/0079-full-service-mesh-discovery-gate-m2a-dosc.md`
- `.agents/handoffs/0068-full-service-mesh-discovery-gate-m2a-dosc-to-qa.md`
- `knowledge-base/source-ledger/2026-05-27-full-service-mesh-discovery-gate-m2a-dosc.md`
- `knowledge-base/source-index.md`
- `docs/index.md`
- `research/development-plan.md`
- `research/development-status-ledger.md`
- `research/triage-status.md`
- `research/known-gaps.md`

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `python3 scripts/build_github_pages.py`
- `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- `python3 scripts/smoke_github_pages.py build/github-pages`
- Source-ID and closed-surface scans over changed records.
- `git diff --check`

## Paired DOS-C Validation

- PASS: `python3 -m unittest tests.espnow_bbs_bridge.test_bridge_protocol`
- PASS: `bash tests/espnow_bbs_bridge/run_tests.sh`
- PASS: focused Win31 operator protocol C test build/run for
  `tests/win31_operator/test_operator_protocol.c`
- PASS: `bash software/win31-operator/build-watcom.sh`
- PASS: targeted guard confirming the new discovery request names were not
  added to `software/espnow-bbs-bridge/coordinator_protocol.py` or firmware
  serial ABI headers.
- PASS: DOS-C `git diff --check` for the Gate M2-A change set.
- CAVEAT: DOS-C full `bash tests/win31_operator/run_host_tests.sh` and
  `bash scripts/verify_scaffold.sh` were blocked by unrelated dirty Star Trek
  fullscreen-fill worktree changes outside the Gate M2-A mutation boundary.

## ESP32 Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (9 tests)
- PASS: `python3 scripts/build_github_pages.py` (63 public files)
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: source-ID scan for
  `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`
  across changed records.
- PASS: closed-surface `rg` review over changed records; hits were closed,
  blocked, host-only, unknown, or stop-gate context, not new authority.
- PASS: `git diff --check`

## Handoff

Continue with
[../handoffs/0068-full-service-mesh-discovery-gate-m2a-dosc-to-qa.md](../handoffs/0068-full-service-mesh-discovery-gate-m2a-dosc-to-qa.md).

## Closed Surfaces

Firmware runtime implementation, firmware persistence, live ESP-WIFI-MESH,
BLE pairing, Android app behavior, router/admin mutation, flash, erase,
monitor, serial-write expansion, PCAP, relay, XBee, TFT, MicroSD, load, mains,
release gating, and live proof remain closed.
