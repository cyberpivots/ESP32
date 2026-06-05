# Source Ledger - 2026-06-05 Full-Service Mesh Discovery Gate M3 Design Review

## Scope

Tier 2 design/docs/records update for Gate M3 firmware mapping review from
ESP-WIFI-MESH concepts into the existing host-only `mesh_discovery.v1`
contract.

This ledger records design direction and fixture requirements only. It does not
accept firmware runtime implementation, build proof, live ESP-WIFI-MESH, BLE
pairing, Android app behavior, router/admin mutation, serial/RF/XBee writes,
relay/load/mains, release, publication, commit, push, PR, or deploy.

## Source IDs

- `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M3-DESIGN-REVIEW-2026-06-05`
- `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`
- `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`
- `SRC-ESP-IDF-WIFI-MESH`
- `SRC-ESP-IDF-RF-COEXIST`
- `SRC-ESP-IDF-BLE-API`
- `SRC-ESP-IDF-BLE-SMP`
- `SRC-ANDROID-BLE-OVERVIEW`
- `SRC-ANDROID-BLE-GATT-CONNECT`
- `SRC-ANDROID-BLUETOOTH-PERMISSIONS`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-RUNTIME-REQUIREMENTS-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-PHASE-5-6-RUNTIME-DESIGN-REVIEW-2026-05-26`
- `SRC-LOCAL-HOST-PROTOCOL-CUSTODY-REVIEW-2026-06-05`
- `SRC-LOCAL-AGENTIC-PLANNING-GUIDE-2026-06-05`

## Verified Facts

- `ADR-0009` accepts `mesh_discovery.v1` as host-only and separates it from
  Gate F radio ABI.
- Gate M2-A records read-only DOS-C companion support for
  `discovery_snapshot`, `discovery_events`, `service_catalog`, and
  `capability_report`, with no coordinator serial ABI expansion.
- ESP-WIFI-MESH source coverage supports root/parent selection, routing table,
  loop-back prevention, and self-healing concepts.
- RF coexistence source coverage requires future review before any mesh plus
  BLE behavior is accepted.
- Task 0179 keeps custody ACK semantics separate from discovery summaries.
- Gate M3 creates a mapping matrix and future fixture checklist only.

## Assumptions

- Concept-level M3 mapping is useful before an M4 build-only adapter proof.
- Exact firmware callbacks, event names, queue policy, memory policy, and
  persistence policy remain implementation-gate decisions.
- BLE/Android information remains metadata unless a later BLE/Android gate
  accepts more behavior.

## Unknowns

- Exact firmware API/callback mapping is not accepted.
- No firmware build, memory, queue, persistence, coexistence, recovery, route
  table, parent/root, healing, BLE, Android, router/admin, cleanup, rollback,
  or live proof exists.

## Reviewer Quorum

Read-only project-local reviewers were spawned, waited, and closed after output
capture.

| Role | Weight | Vote | Disposition |
| --- | ---: | --- | --- |
| Development panel coordinator | 5 | approve with conditions | Required Task 0180, source ledger, handoff, source row, and design-only scope. |
| Protocol bridge ABI reviewer | 3 | approve with conditions | Required no firmware/schema/ABI/live claim and a mapping matrix/fixture checklist. |
| Evidence record auditor | 3 | approve with conditions | Required M3 durable records and source-index-backed claims. |
| QA validation reviewer | 3 | approve with conditions | Required host-only validation, source citations, and closed-surface scan. |
| Off-grid communications domain reviewer | 3 | approve with conditions | Required queue/custody isolation and M4/M5 gate split. |

Weighted disposition: 17/17 approved for the named Tier 2 mutation boundary.
Threshold: 70 percent. No P1 blockers remained. P2 record/source-coverage
conditions are addressed by the M3 design note and this durable record set.

## Validation

Passed on 2026-06-05:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.custom_wireless_protocol.test_espnow_bbs_custom_protocol`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 180`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- Targeted source-ID and closed-surface scans over changed files.
- `git diff --check`

## Decision

Decision: accept the M3 design review. The future M4 gate must remain
build-only and separately reviewed; live mesh remains a future Tier 3 M5 gate
with same-session evidence and recovery/cleanup proof.
