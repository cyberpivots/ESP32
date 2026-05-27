# Task 0075: Full-Service Mesh Discovery Host Contract

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-27

## Goal

Implement the Full Services plan as a Tier 2, host-only discovery contract for
mesh topology, peer/node discovery, service/capability discovery, BLE/Android
presence metadata, and healing-event evidence.

This task does not run live mesh, BLE pairing, flashing, serial writes,
router/admin mutation, relay, XBee, TFT, MicroSD, load, mains, or firmware
runtime migration.

## Verified Facts

- `ADR-0004` remains a proposed self-healing transport branch, not live mesh
  authorization.
- `ADR-0008` remains host-only runtime prototype authority, not firmware
  runtime migration.
- The accepted BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- `mesh_discovery.v1` is host-only and separate from the Gate F radio packet
  ABI.
- Project-local read-only subagents were spawned for governance, evidence,
  protocol, and QA review after the user explicitly authorized subagent use.

## Assumptions

- Full Services means host modeling and compact summaries, not live discovery.
- BLE/Android v1 discovery is presence/capability metadata only.
- ESP-Mesh-Lite remains future comparison and ESP-MDF is not selected.

## Unknowns

- No live mesh route-table, parent, root, healing, coexistence, flash, or
  cleanup proof exists.
- No BLE UUIDs, Android package, permission proof, bonding/SMP proof,
  coexistence proof, or live GATT proof exists.
- No firmware mapping from ESP-WIFI-MESH APIs/events into `mesh_discovery.v1`
  is accepted.

## Implementation

- Added accepted `ADR-0009` for the host-only full-service discovery contract.
- Added design packet
  `docs/projects/espnow-bbs/full-service-mesh-discovery.md`.
- Added simulator support for `mesh_discovery.v1`, host discovery nodes,
  discovery events, service catalog, capability report, compact 512-byte bridge
  summaries, recursive secret-field rejection, and additional blocked live
  request names.
- Added runtime support for discovery summary requests without queuing radio
  packet jobs.
- Added tests for schema defaults, separation from Gate F radio ABI, topology
  snapshot generation, event coverage, node coalescing, stale/lost transition,
  healing summary, service/capability reports, BLE/Android metadata, bridge
  bounds, secret exclusion, closed live controls, and runtime report inclusion.
- Added source ledger/source-index coverage for
  `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`.
- Tightened the generated public source-index sanitizer to redact standalone
  hash-like evidence values so the existing public manifest audit remains
  fail-closed.

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

## Handoff

Continue with
[../handoffs/0064-full-service-mesh-discovery-to-qa.md](../handoffs/0064-full-service-mesh-discovery-to-qa.md).

## Stop Gates

Do not use this host-only package to authorize coordinator runtime migration,
peer runtime migration, firmware queue persistence, serial writes, bridge
export requests, Win31 export controls, flash, erase, monitor, BLE pairing,
ESP-WIFI-MESH live action, PCAP, router/admin mutation, relay, XBee, TFT,
MicroSD, load, mains, or live proof work.
