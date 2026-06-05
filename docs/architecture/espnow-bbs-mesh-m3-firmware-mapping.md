# ESP-NOW BBS Mesh M3 Firmware Mapping Review

Source index: [../../knowledge-base/source-index.md](../../knowledge-base/source-index.md)

## Scope

Gate M3 is a Tier 2 design review for how a future firmware adapter might map
ESP-WIFI-MESH concepts and events into the existing host-only
`mesh_discovery.v1` contract.

This review does not accept firmware runtime implementation, framework changes,
build proof, flashing, monitor, serial writes, live ESP-WIFI-MESH, BLE pairing,
Android app behavior, router/admin mutation, PCAP, RF/XBee writes,
relay/load/mains work, release, publication, commit, push, PR, or deploy.

## Verified Facts

- `ADR-0009` accepts `mesh_discovery.v1` as a host-only simulator/design
  contract. Source ID:
  `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`.
- Gate M2-A accepts paired DOS-C bridge/operator support for read-only
  `discovery_snapshot`, `discovery_events`, `service_catalog`, and
  `capability_report` summaries, with no coordinator serial ABI expansion.
  Source ID:
  `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`.
- ESP-WIFI-MESH source coverage in the repository supports tree topology,
  root/parent selection, routing tables, loop-back prevention, self-healing
  after root/parent failure, and mesh WPA2-PSK/AES security notes. Source ID:
  `SRC-ESP-IDF-WIFI-MESH`.
- ESP32 Wi-Fi/BLE coexistence requires separate review before any live mesh
  plus BLE claim. Source ID: `SRC-ESP-IDF-RF-COEXIST`.
- Gate F and Phase 5/6 records keep the custom radio service map, custody
  lifecycle, runtime queues, and non-executing control intent host-only until a
  later implementation gate. Source IDs:
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`,
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-RUNTIME-REQUIREMENTS-2026-05-26`,
  and
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-PHASE-5-6-RUNTIME-DESIGN-REVIEW-2026-05-26`.
- Task 0179 clarifies that custody ACK execution semantics are separate from
  discovery summaries. Source ID:
  `SRC-LOCAL-HOST-PROTOCOL-CUSTODY-REVIEW-2026-06-05`.

## Assumptions

- M3 mapping starts from ESP-WIFI-MESH concepts that are already
  source-indexed in this workspace; exact firmware callback names remain
  future implementation detail unless separately sourced.
- `mesh_discovery.v1` remains unchanged for this review.
- BLE/Android fields remain presence and capability metadata only.

## Unknowns

- Exact firmware callback, event, and routing-table APIs to be used by a
  future adapter are not selected by this review.
- Firmware memory budget, queue budget, persistence model, recovery behavior,
  and RF coexistence measurements are not accepted.
- No live mesh route table, parent/root selection, healing, router/channel
  policy, BLE coexistence, Android GATT, flash, serial, cleanup, or rollback
  proof exists.

## Mapping Matrix

This table is a design constraint for a future M4 build-only adapter proof. It
is not runtime firmware acceptance.

| Source concept | `mesh_discovery.v1` target | Required inputs | Derived or lossy fields | Source IDs |
| --- | --- | --- | --- | --- |
| Mesh root election | `root_elected`, `root_switched`, node `rt`/root summary | Local node ID, selected root ID, prior root when known | Root-switch reason may be unknown until firmware records cause/source | `SRC-ESP-IDF-WIFI-MESH`, `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27` |
| Parent selection | `parent_selected`, node `p`/parent summary | Local node ID, parent node ID, layer if known | Parent RSSI and route quality may be absent or sampled separately | `SRC-ESP-IDF-WIFI-MESH`, `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27` |
| Routing table change | `route_added`, `route_removed` | Route node ID, local role/root context | Full routing table must be compacted before bridge exposure | `SRC-ESP-IDF-WIFI-MESH`, `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27` |
| Node presence refresh | `node_seen`, node record fields | Node ID, link type, role/layer when known, age/RSSI when available | MAC or raw identifiers require redaction policy before publication | `SRC-ESP-IDF-WIFI-MESH`, `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27` |
| Stale or missing node | `node_lost`, node health `lost` | Last-seen age, stale threshold selected by future firmware gate | Stale threshold is not accepted by this review | `SRC-ESP-IDF-WIFI-MESH`, `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27` |
| Self-healing start/observation | `heal_started`, `heal_observed`, summary `heal` | Loss/root/parent event sequence and observed recovery condition | Recovery quality and timing are not live proof without M5 evidence | `SRC-ESP-IDF-WIFI-MESH`, `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27` |
| Service visibility | `service_seen`, `service_catalog` | Local advertised service class from host/firmware mapping | Service catalog is a summary; it must not execute controls | `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`, `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26` |
| Capability visibility | `capability_seen`, `capability_report` | Capability class from host/firmware mapping | Counts are summaries and may hide node detail to preserve bridge bounds | `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`, `SRC-ESP-IDF-RF-COEXIST` |
| BLE/Android presence metadata | `ble_client_seen`, `capability_report.ble_android` | Presence/capability metadata only | No BLE UUID, bonding, pairing, GATT, Android app, or permission proof is accepted | `SRC-ESP-IDF-BLE-API`, `SRC-ESP-IDF-BLE-SMP`, `SRC-ANDROID-BLE-OVERVIEW`, `SRC-ANDROID-BLE-GATT-CONNECT`, `SRC-ANDROID-BLUETOOTH-PERMISSIONS` |

## Compatibility Requirements

- Keep `schema` as `mesh_discovery.v1`, `mode` as `sim` for host-only
  fixtures, and `admin_gate` as `disabled`.
- Keep `discovery_snapshot`, `discovery_events`, `service_catalog`, and
  `capability_report` as host bridge summaries only.
- Do not add these request names to the physical coordinator serial protocol.
- Do not add a Gate F radio service code for mesh discovery.
- Do not change the bridge ABI, coordinator serial ABI, Win31 transport, or
  Gate F packet layout.
- Do not couple `control_intent` or service catalog entries to relay, RF,
  flash, persistent, or other live actions.
- Keep bridge summaries ASCII, schema-versioned, and bounded to the existing
  512-byte bridge line limit.
- Reject recursive secret-bearing fields including PMK, LMK, bonding key,
  pairing token, Android identifier, raw message body, credential fields, and
  precise location fields.

## Fixture Requirements For Future M4

A future M4 build-only adapter proof should add host-only fixtures or tests for:

- `node_seen`, `parent_selected`, `root_elected`, `root_switched`,
  `route_added`, `route_removed`, `node_lost`, `heal_started`,
  `heal_observed`, `service_seen`, `capability_seen`, and `ble_client_seen`.
- Maximum-size `discovery_snapshot`, `discovery_events`, `service_catalog`,
  and `capability_report` bridge summaries that remain within the 512-byte
  line budget.
- Negative cases for secret-bearing fields, unknown fields, invalid limits, and
  live-action request names.
- Queue/custody isolation: discovery mapping must not enqueue radio packet
  jobs, mutate custody state, execute `control_intent`, or expose raw message
  bodies.
- Schema/ABI invariance checks for `mesh_discovery.v1`, Gate F service codes,
  coordinator serial ABI, bridge ABI, and Win31 transport.

## Gate Split

- M3: this design review and mapping matrix only.
- M4: future build-only firmware adapter proof with memory, queue, persistence,
  and coexistence review.
- M5: future live mesh proof only after fresh identity, backups, hashes,
  router/channel/mesh ID policy, rollback, route-table proof, root/parent
  failure proof, BLE coexistence proof, transcript, and cleanup.

## Decision

Accept the M3 mapping review as design-only. The future firmware adapter has a
source-backed mapping direction and fixture checklist, but no firmware mapping,
runtime behavior, build proof, live RF behavior, BLE behavior, Android behavior,
router/admin policy, release, or publication is accepted by this review.
