# ESP-NOW BBS Full-Service Mesh Discovery

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

## Scope

This packet defines `mesh_discovery.v1` as a host-only discovery contract for
topology, node, service, capability, BLE/Android presence, and healing-event
evidence.

The accepted baseline remains:

`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`

This packet does not run live mesh, BLE pairing, flashing, serial writes,
router/admin mutation, relay, XBee, TFT, MicroSD, load, mains, or firmware
runtime migration.

## Verified Facts

- ESP-WIFI-MESH is the v1 transport target for future self-healing design
  because the project has already proposed it in `ADR-0004`. Source IDs:
  `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`,
  `SRC-ESP-IDF-WIFI-MESH`.
- ESP-WIFI-MESH source material covers tree topology, root/parent selection,
  routing tables, root/parent failure handling, and self-healing concepts.
  Source ID: `SRC-ESP-IDF-WIFI-MESH`.
- ESP32 Wi-Fi and BLE coexistence requires explicit review before live proof.
  Source ID: `SRC-ESP-IDF-RF-COEXIST`.
- Android BLE remains modeled as central/GATT client, with the ESP32 client
  node as BLE peripheral/GATT server. Source IDs:
  `SRC-ANDROID-BLE-OVERVIEW`, `SRC-ANDROID-BLE-GATT-CONNECT`.
- Android Bluetooth permissions and location handling remain metadata until a
  separate BLE live gate opens. Source ID:
  `SRC-ANDROID-BLUETOOTH-PERMISSIONS`.
- ESP-Mesh-Lite is comparison/future research only; ESP-MDF is not selected.
  Source IDs: `SRC-ESP-MESH-LITE-2026-05-27`,
  `SRC-ESP-MDF-ARCHIVED-2026-05-27`.

## Assumptions

- `mesh_discovery.v1` stays host-only until a later accepted ADR maps firmware
  ESP-WIFI-MESH APIs/events into the schema.
- BLE/Android discovery is presence and capability metadata only for v1.
- The Pi bridge remains the durable BBS custody and operator boundary.

## Unknowns

- No live mesh route-table, parent, root, healing, coexistence, flash, or
  cleanup proof exists.
- No BLE UUIDs, Android package, permission proof, bonding/SMP proof,
  coexistence proof, or live GATT proof exists.
- No router SSID/BSSID/channel policy, mesh ID, root-election policy,
  max-layer policy, or rollback packet is accepted for a live mesh gate.

## Schema Defaults

| Field | Value |
| --- | --- |
| `schema` | `mesh_discovery.v1` |
| `transport` | `esp-wifi-mesh` |
| `mode` | `sim` |
| `admin_gate` | `disabled` |

## Record Model

Each host discovery node record carries:

- node identity and MAC
- link type, role, layer, parent, and root
- RSSI, seen age, and health
- service and capability lists
- security summary and source evidence

Discovery payloads must not include PMKs, LMKs, BLE bonding keys, pairing
tokens, Android identifiers, raw message bodies, credential fields, or precise
location data.

## Event Model

Accepted host event names are:

- `node_seen`
- `node_lost`
- `parent_selected`
- `root_elected`
- `root_switched`
- `route_added`
- `route_removed`
- `heal_started`
- `heal_observed`
- `service_seen`
- `capability_seen`
- `ble_client_seen`

Healing acceptance remains future work. The v1 simulator only records the event
shape and host summary behavior.

## Service Catalog

The v1 host catalog includes:

- BBS messaging
- file transfer
- telemetry
- node status
- custody ACK
- non-executing control intent
- BLE client presence
- Android client metadata

## Bridge Summaries

The host simulator supports compact, schema-versioned, ASCII summaries:

| Request | Purpose |
| --- | --- |
| `discovery_snapshot` | Compact node/topology snapshot. |
| `discovery_events` | Recent discovery and healing events. |
| `service_catalog` | v1 service names. |
| `capability_report` | Capability counts and BLE/Android metadata summary. |

Responses must fit the existing 512-byte bridge line limit. These request names
do not add Gate F radio service codes and do not authorize live bridge
authority.

## Derived Dashboard Fields

Existing live-safe dashboard fields such as `mesh`, `mesh_root`,
`mesh_parent`, `mesh_layer`, `mesh_heal`, `ble`, and `android` should be
derived from `mesh_discovery.v1` summaries when this data is presented. They
are not the source of truth.

## Future Gates

- Gate M1: this host ADR/design/research plus simulator schema.
- Gate M2: DOS-C companion bridge/operator fixture support and Win31 read-only
  Network/Services summary.
- Gate M3: firmware-design review for mapping ESP-WIFI-MESH APIs/events to the
  schema, still no live flash.
- Gate M4: build-only firmware adapter proof with memory/queue/coexistence
  review.
- Gate M5: live mesh proof only after fresh identity, backups, hashes,
  router/channel/mesh ID policy, rollback, route-table proof, root/parent
  failure proof, BLE coexistence proof, transcript, and cleanup.

## Validation

The host simulator tests cover schema defaults, topology snapshots, events,
service and capability reports, BLE/Android presence metadata, duplicate node
coalescing, stale/lost transitions, healing-event summaries, 512-byte bridge
bounds, recursive secret-field rejection, closed live controls, runtime report
inclusion, and unchanged Gate F radio service-code membership.
