# Task 0180: Full-Service Mesh Discovery Gate M3 Design Review

Status: completed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-05

Source IDs:
`SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M3-DESIGN-REVIEW-2026-06-05`,
`SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`,
`SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`,
`SRC-ESP-IDF-WIFI-MESH`,
`SRC-ESP-IDF-RF-COEXIST`,
`SRC-ESP-IDF-BLE-API`,
`SRC-ESP-IDF-BLE-SMP`,
`SRC-ANDROID-BLE-OVERVIEW`,
`SRC-ANDROID-BLE-GATT-CONNECT`,
`SRC-ANDROID-BLUETOOTH-PERMISSIONS`,
`SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`,
`SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-RUNTIME-REQUIREMENTS-2026-05-26`,
`SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-PHASE-5-6-RUNTIME-DESIGN-REVIEW-2026-05-26`,
`SRC-LOCAL-HOST-PROTOCOL-CUSTODY-REVIEW-2026-06-05`,
`SRC-LOCAL-AGENTIC-PLANNING-GUIDE-2026-06-05`

## Routing

- Verified facts: `docs/agentic-planning-guide.md` lists Mesh M3 design review
  as the second approved next sequence item. `ADR-0009` accepts
  `mesh_discovery.v1` only as a host-only simulator/design contract. Gate M2-A
  is recorded as host-only DOS-C companion bridge/operator support with no
  coordinator serial ABI expansion. Existing records stated no firmware
  mapping from ESP-WIFI-MESH APIs/events into `mesh_discovery.v1` was accepted
  before this task.
- Assumptions: M3 means a source-backed firmware mapping design review and
  fixture checklist only, not firmware implementation or build proof. Existing
  source-indexed ESP-IDF and Android/BLE records are sufficient for concept
  mapping, while exact firmware callback/API selections remain future
  implementation detail.
- Unknowns: no live ESP-WIFI-MESH route-table, parent/root, healing,
  coexistence, flash, serial, cleanup, BLE UUID, Android package, permission,
  bonding/SMP, GATT, router/admin, PCAP, or hardware proof exists. Firmware
  memory, queue, persistence, recovery, and coexistence budgets remain
  unmeasured.
- Selected tier: Tier 2 design/docs/records.
- Owner role: Communications with Architecture and QA.
- Evidence need: `ADR-0009`, M1/M2-A source ledgers, ESP-IDF mesh/coexistence
  source records, BLE/Android source records, Gate F/runtime records, Task
  0179 custody boundary, docs index, status/gap records, and read-only reviewer
  quorum output.
- Mutation boundary:
  `docs/architecture/espnow-bbs-mesh-m3-firmware-mapping.md`,
  `docs/projects/espnow-bbs/full-service-mesh-discovery.md`,
  `knowledge-base/source-index.md`,
  `knowledge-base/source-ledger/2026-06-05-full-service-mesh-discovery-gate-m3-design-review.md`,
  `docs/index.md`, `research/development-plan.md`,
  `research/development-status-ledger.md`, `research/triage-status.md`,
  `research/known-gaps.md`, this task record, and
  `.agents/handoffs/0128-full-service-mesh-discovery-gate-m3-design-review-to-qa-communications-architecture.md`.
- Reviewer quorum: read-only project-local subagents were spawned for
  development-panel coordination, protocol/bridge ABI review, evidence-record
  audit, QA validation, and off-grid communications domain review. All
  completed reviewers were waited and closed after output capture. Weighted
  disposition: 17/17 approval with conditions, threshold 70 percent. No P1
  blockers remained. P2 conditions required durable records/source coverage and
  are addressed by this task, source ledger, source-index row, handoff, design
  note, and status/gap updates.
- Gate authority: design notes, source-index/source-ledger/task/handoff/status
  records, and docs-index discoverability only. No Tier 3 authority is opened.
- Validation plan: run custom wireless protocol host tests, source/record/
  agent-process/scaffold audits, a closed-surface/source-ID scan over changed
  files, and `git diff --check`.
- Trust boundary: local repo records, accepted ADRs, source-indexed official
  sources, host-only tests, and captured reviewer votes. Hooks remain advisory
  under `bypassPermissions`.

## Implementation

- Added the M3 firmware-mapping design review note with a source-backed mapping
  matrix from ESP-WIFI-MESH concepts into `mesh_discovery.v1` targets.
- Recorded compatibility requirements that keep `mesh_discovery.v1`, Gate F
  service codes, coordinator serial ABI, bridge ABI, and Win31 transport
  unchanged.
- Added future M4 fixture requirements for event vectors, bridge bounds,
  secret rejection, live-action rejection, queue/custody isolation, and schema/
  ABI invariance.
- Updated the full-service mesh-discovery project doc and current status/gap
  records to mark M3 design review accepted while keeping implementation/live
  gates closed.
- Added durable Task 0180, source ledger, source-index row, handoff, and docs
  index links.

## Validation

Passed on 2026-06-05:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.custom_wireless_protocol.test_espnow_bbs_custom_protocol`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 180`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- Targeted source-ID and closed-surface `rg` scan over changed M3 files.
- `git diff --check`.

## Authority Limits

Still closed: firmware runtime implementation, firmware persistence,
coordinator/peer migration, framework changes, build proof, live
ESP-WIFI-MESH, BLE pairing, Android app behavior, router/admin mutation, PCAP,
flash, erase, monitor, serial writes, RF/XBee writes, relay/load/mains work,
release, publication, commit, push, PR, deploy, `/etc/codex/requirements.toml`,
and `admin-strict` installation.

## Handoff

[../handoffs/0128-full-service-mesh-discovery-gate-m3-design-review-to-qa-communications-architecture.md](../handoffs/0128-full-service-mesh-discovery-gate-m3-design-review-to-qa-communications-architecture.md)

## Decision

Decision: accept the bounded Tier 2 Gate M3 design review. Future work moves to
M4 build-only firmware adapter proof only after a separate gate; live mesh
remains M5/Tier 3 only.
