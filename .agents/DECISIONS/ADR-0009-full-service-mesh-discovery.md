# ADR-0009: Full-Service Mesh Discovery Host Contract

Status: Accepted

Date: 2026-05-27

## Context

`ADR-0004` proposes ESP-WIFI-MESH as the future self-healing transport branch,
but it remains `Proposed` for live mesh migration. `ADR-0008` accepts only a
host-only runtime prototype for the custom wireless protocol.

The project needs a full-service discovery model for topology, node, service,
capability, BLE/Android presence, and healing-event evidence before any future
firmware or live mesh implementation can be reviewed.

## Verified Facts

- The accepted BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- ESP-WIFI-MESH is source-backed for tree topology, root/parent selection,
  routing tables, and self-healing concepts, but no live mesh proof exists.
- ESP32 Wi-Fi and BLE share RF resources, so any future mesh plus BLE proof
  requires coexistence evidence.
- Android remains modeled as BLE central / GATT client; the ESP32 client node
  remains modeled as BLE peripheral / GATT server.
- Existing Gate F packet service codes and golden vectors remain unchanged.
- The new host simulator schema is `mesh_discovery.v1`; it is separate from
  the Gate F radio packet ABI.

## Accepted Decision

Accept `full-service-mesh-discovery.v1` as a host-only simulator and design
contract.

The v1 transport target is ESP-WIFI-MESH. ESP-Mesh-Lite remains comparison and
future research only. ESP-MDF is not selected.

### Schema Defaults

- `schema = "mesh_discovery.v1"`
- `transport = "esp-wifi-mesh"`
- `mode = "sim"`
- `admin_gate = "disabled"`

### Discovery Model

Host discovery records cover:

- node identity and MAC
- link type, role, layer, parent, and root
- RSSI, seen age, and health
- services and capabilities
- security summary and source evidence

Host discovery events cover `node_seen`, `node_lost`, `parent_selected`,
`root_elected`, `root_switched`, `route_added`, `route_removed`,
`heal_started`, `heal_observed`, `service_seen`, `capability_seen`, and
`ble_client_seen`.

### Bridge Summaries

The simulator may answer these compact, schema-versioned, ASCII bridge request
types:

- `discovery_snapshot`
- `discovery_events`
- `service_catalog`
- `capability_report`

Responses must fit the existing 512-byte bridge line limit. These requests are
host summaries only and are not added to the accepted Gate F radio service-code
map.

### Security Boundary

Discovery payloads must not include PMKs, LMKs, BLE bonding keys, pairing
tokens, Android identifiers, raw message bodies, credential fields, or precise
location data. The simulator rejects recursive secret-bearing field names for
the discovery payload surface.

## Assumptions

- Full Services in this ADR means host modeling of topology, service catalog,
  capability inventory, BLE/Android presence metadata, and healing events.
- ESP-WIFI-MESH is the likely future self-healing substrate because it matches
  the project topology and healing needs already recorded in `ADR-0004`.
- BLE/Android data remains presence and capability metadata until a separate
  BLE live gate opens.

## Unknowns

- No live mesh route table, parent, root, healing, coexistence, flash, or
  cleanup proof exists.
- No BLE UUIDs, Android package, permission proof, bonding/SMP proof,
  coexistence proof, or live GATT proof exists.
- No firmware mapping from ESP-WIFI-MESH APIs/events into this schema is
  accepted yet.
- No ESP-Mesh-Lite or ESP-MDF implementation path is selected.

## Consequences

- Host simulator tests now pin `mesh_discovery.v1` schema defaults, compact
  bridge summaries, topology and healing events, service/capability catalogs,
  BLE/Android metadata, secret exclusion, closed live controls, and runtime
  report inclusion.
- Existing dashboard metadata fields such as `mesh`, `mesh_root`,
  `mesh_parent`, `mesh_layer`, `mesh_heal`, `ble`, and `android` are derived
  summaries, not the source of truth.
- Future Gate M work is ordered as:
  - M1: docs/ADR/research plus host simulator discovery schema.
  - M2: DOS-C companion bridge/operator fixture support and Win31 read-only
    Network/Services summary.
  - M3: firmware-design review for mapping ESP-WIFI-MESH events/APIs to the
    schema, still no live flash.
  - M4: build-only firmware adapter proof with memory/queue/coexistence review.
  - M5: live mesh proof only after fresh identity, backups, hashes,
    router/channel/mesh ID policy, rollback, route-table proof, root/parent
    failure proof, BLE coexistence proof, transcript, and cleanup.

## Review Quorum

- Governance/docs reviewer: PASS for host-only scope; live/full-mesh migration
  blockers recorded as stop gates.
- Evidence-boundary reviewer: PASS for host-only scope after source IDs and
  ESP-Mesh-Lite/ESP-MDF comparison gaps are recorded.
- Protocol/schema reviewer: PASS after adding secret exclusion, 512-byte bridge
  tests, runtime surface coverage, and no Gate F radio service-code changes.
- QA reviewer: PASS after adding simulator tests and durable records.

## Sources

- `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`
- `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-PHASE-5-6-RUNTIME-DESIGN-REVIEW-2026-05-26`
- `SRC-ESP-IDF-WIFI-MESH`
- `SRC-ESP-IDF-RF-COEXIST`
- `SRC-ESP-IDF-BLE-API`
- `SRC-ESP-IDF-BLE-SMP`
- `SRC-ANDROID-BLE-OVERVIEW`
- `SRC-ANDROID-BLE-GATT-CONNECT`
- `SRC-ANDROID-BLUETOOTH-PERMISSIONS`
- `SRC-ESP-MESH-LITE-2026-05-27`
- `SRC-ESP-MDF-ARCHIVED-2026-05-27`

## Stop Gates

This ADR does not authorize ESP-WIFI-MESH live action, firmware runtime
migration, coordinator or peer firmware code, firmware queue persistence,
serial writes, bridge export requests, Win31 export controls, flash, erase,
monitor, BLE pairing, Android app builds, PCAP, router/admin mutation, relay,
XBee, TFT, MicroSD, load, mains, or live proof.
