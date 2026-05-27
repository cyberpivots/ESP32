# Full-Service Mesh Discovery Source Ledger

Date: 2026-05-27

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`

## Sources Used

- `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-PHASE-5-6-RUNTIME-DESIGN-REVIEW-2026-05-26`
- `SRC-LOCAL-MULTI-AGENTIC-DEFAULT-PROCESS-2026-05-27`
- `SRC-ESP-IDF-WIFI-MESH`
- `SRC-ESP-IDF-RF-COEXIST`
- `SRC-ESP-IDF-BLE-API`
- `SRC-ESP-IDF-BLE-SMP`
- `SRC-ANDROID-BLE-OVERVIEW`
- `SRC-ANDROID-BLE-GATT-CONNECT`
- `SRC-ANDROID-BLUETOOTH-PERMISSIONS`
- `SRC-ESP-MESH-LITE-2026-05-27`
- `SRC-ESP-MDF-ARCHIVED-2026-05-27`

## Scope

Host-only `mesh_discovery.v1` schema, simulator summaries, and planning records
for full-service mesh discovery.

This task does not add firmware runtime code, does not run live hardware, does
not pair BLE, and does not open ESP-WIFI-MESH live action.

## Review Quorum

Project-local read-only subagents were spawned after the user explicitly
authorized subagent use for this workspace.

- Governance/docs review: PASS for host-only scope; BLOCK for live/full-mesh
  migration claims.
- Evidence-boundary review: PASS for host-only scope; BLOCK for live mesh,
  BLE, Android app, router/admin, or firmware behavior claims.
- Protocol/schema review: PASS after secret exclusion, 512-byte bridge tests,
  runtime surface coverage, and no Gate F radio service-code changes.
- QA review: PASS after adding simulator coverage and durable records.

## Verified Facts

- [repo-verified] Added accepted `ADR-0009` for host-only
  `full-service-mesh-discovery.v1`.
- [repo-verified] Added design packet
  `docs/projects/espnow-bbs/full-service-mesh-discovery.md`.
- [repo-verified] Added `mesh_discovery.v1` simulator constants, host
  `DiscoveryNode` records, discovery events, service catalog, capability
  report, compact bridge summaries, recursive secret-field rejection, and
  expanded closed-live request rejection.
- [repo-verified] `discovery_snapshot`, `discovery_events`,
  `service_catalog`, and `capability_report` are host-only bridge summaries.
  They do not add Gate F radio service codes.
- [repo-verified] Host tests now pin schema defaults, topology snapshots,
  event names, node coalescing, stale/lost transition, healing summary,
  service/capability catalog, BLE/Android metadata, bridge-line bounds,
  recursive secret-field rejection, closed live controls, runtime summary
  inclusion, and unchanged Gate F radio ABI membership.
- [repo-verified] Tightened generated public source-index redaction in
  `scripts/build_github_pages.py` for hash-like evidence values after the
  fail-closed public manifest audit flagged existing SHA-256 strings in the
  generated bundle.
- [repo-verified] Existing accepted BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Assumptions

- [assumption] Full Services means host modeling of topology, node, service,
  capability, BLE/Android presence, and healing-event evidence.
- [assumption] ESP-WIFI-MESH remains the v1 transport target for future
  self-healing review because it matches the project topology and healing
  concepts already proposed by `ADR-0004`.
- [assumption] ESP-Mesh-Lite remains comparison/future research only.

## Unknowns

- [unknown] No live mesh route-table, parent, root, healing, coexistence,
  flash, or cleanup proof exists.
- [unknown] No BLE UUIDs, Android package, permission proof, bonding/SMP proof,
  coexistence proof, or live GATT proof exists.
- [unknown] No firmware mapping from ESP-WIFI-MESH APIs/events into
  `mesh_discovery.v1` is accepted.
- [unknown] ESP-MDF is not selected; ESP-Mesh-Lite is not selected.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 scripts/scaffold_audit_agent_process.py`
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: targeted `rg` checks for `mesh_discovery.v1`, `ADR-0009`,
  `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`,
  `SRC-ESP-MESH-LITE-2026-05-27`, and
  `SRC-ESP-MDF-ARCHIVED-2026-05-27`
- PASS: `git diff --check`

## Result

Gate M1 has a host-only accepted discovery contract and simulator proof.
Live mesh, BLE pairing, Android app behavior, router/admin mutation, firmware
runtime migration, and hardware mutation remain closed.

## Stop Gates

Do not use this package to authorize coordinator runtime migration, peer
runtime migration, firmware queue persistence, serial writes, bridge export
requests, Win31 export controls, flash, erase, monitor, BLE pairing,
ESP-WIFI-MESH live action, PCAP, router/admin mutation, relay, XBee, TFT,
MicroSD, load, mains, or live proof work.
