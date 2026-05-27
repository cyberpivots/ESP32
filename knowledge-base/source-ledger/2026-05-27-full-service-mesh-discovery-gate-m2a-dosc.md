# Full-Service Mesh Discovery Gate M2-A DOS-C Source Ledger

Date: 2026-05-27

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`

## Purpose

Record the paired DOS-C host-only bridge/operator implementation that supports
the ESP32 full-service mesh-discovery Gate M2-A planning status.

## Sources Used

- `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`
- DOS-C commit `62c4db6`
- ESP32 consolidation checkpoint commit `4dec626`

## Verified Facts

- [repo-verified] DOS-C commit `62c4db6` adds Win31-to-Pi bridge handlers for
  `discovery_snapshot`, `discovery_events`, `service_catalog`, and
  `capability_report`.
- [repo-verified] The handlers are host-only, read-only, deterministic,
  schema-versioned, ASCII JSON responses and retain the 512-byte bridge line
  limit.
- [repo-verified] `discovery_events` is capped at two local bridge events with
  truncated kind/detail fields and no raw request or body payloads.
- [repo-verified] `service_catalog` covers BBS messaging, file transfer,
  telemetry, node status, custody ACK, control intent, BLE presence, and
  Android metadata.
- [repo-verified] `capability_report` uses scalar status fields including
  `crypto`, `mesh`, `mesh_root`, `mesh_heal`, `ble`, `ble_role`, `android`,
  `admin_gate`, `control`, and `line_max`.
- [repo-verified] The Win31 operator request formatter/parser supports the four
  discovery request types and the Network/Link view displays read-only
  Network/Services status.
- [repo-verified] The Gate M2-A change did not extend DOS-C
  `software/espnow-bbs-bridge/coordinator_protocol.py` or the Pi-to-ESP32
  coordinator serial ABI.

## Assumptions

- Gate M2-A remains a Tier 2 host-only paired DOS-C support gate.
- Later firmware mapping review should start as Gate M3 design-only unless a
  future accepted ADR changes the boundary.

## Unknowns

- No live ESP-WIFI-MESH route-table, parent, root, healing, coexistence,
  flash, serial, cleanup, or live proof exists.
- No BLE UUID, Android package, permission proof, bonding/SMP proof,
  coexistence proof, or live GATT proof exists.
- No firmware mapping from ESP-WIFI-MESH APIs/events into `mesh_discovery.v1`
  is accepted.
- No router/admin policy mutation or PCAP proof is accepted.

## Local Records

- ESP32 task log:
  `.agents/TASK_LOG/0079-full-service-mesh-discovery-gate-m2a-dosc.md`
- ESP32 QA handoff:
  `.agents/handoffs/0068-full-service-mesh-discovery-gate-m2a-dosc-to-qa.md`
- ESP32 development plan: `research/development-plan.md`
- ESP32 status ledger: `research/development-status-ledger.md`
- DOS-C task log:
  `/mnt/h/dos-c/.agents/tasks/0050-full-service-mesh-discovery-gate-m2a-bridge-operator.md`
- DOS-C handoff:
  `/mnt/h/dos-c/.agents/handoffs/0042-full-service-mesh-discovery-gate-m2a-to-qa.md`
- DOS-C knowledge note:
  `/mnt/h/dos-c/knowledge-base/full-service-mesh-discovery-gate-m2a-2026-05-27.md`

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

## Stop Gates

Do not use Gate M2-A to authorize firmware runtime implementation, firmware
persistence, live ESP-WIFI-MESH, BLE pairing, Android app behavior,
router/admin mutation, flash, erase, monitor, serial-write expansion, PCAP,
relay, XBee, TFT, MicroSD, load, mains, release gating, cleanup acceptance, or
live proof.
