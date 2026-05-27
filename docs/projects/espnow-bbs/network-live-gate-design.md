# ESP-NOW BBS Network Live-Gate Design

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

## Scope

This design packet adds simulator-visible network status and future live-gate
requirements for a self-healing branch. It is not a live radio run.

The accepted baseline remains:

`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`

Packet-driver, PCAP, router-admin changes, relay, XBee, TFT, MicroSD, load,
mains, live flashing, BLE pairing, Android builds, and dashboard state-changing
commands remain closed.

## Verified Facts

- ESP-NOW uses PMK and per-peer LMK material for encrypted unicast. The PMK
  encrypts LMKs, LMK absence means the paired unicast action frame is not
  encrypted, and encrypted multicast is not supported. Source ID:
  `SRC-ESP-IDF-ESPNOW`.
- ESP-NOW supports at most 20 paired devices; encrypted paired devices are
  capped at 17, with a default encrypted-peer limit of 7 unless configuration
  changes it. Source ID: `SRC-ESP-IDF-ESPNOW`.
- ESP-NOW send status is MAC-layer status, not proof that the application
  consumed a payload. Application-level ACK, timeout, retry, and duplicate
  handling stay required. Source ID: `SRC-ESP-IDF-ESPNOW`.
- ESP-WIFI-MESH documents root nodes, parent selection, routing tables,
  loop-back prevention, root election, and self-healing after root or parent
  failure. Source ID: `SRC-ESP-IDF-WIFI-MESH`.
- ESP-WIFI-MESH notes Wi-Fi WPA2-PSK for data transmission and AES for mesh
  networking information elements. Source ID: `SRC-ESP-IDF-WIFI-MESH`.
- ESP32 Wi-Fi, Bluetooth/BLE, and other 2.4 GHz modules share one RF module,
  so Wi-Fi/ESP-WIFI-MESH plus BLE must be treated as a coexistence risk until
  tested. Source ID: `SRC-ESP-IDF-RF-COEXIST`.
- ESP-IDF exposes BLE GAP, GATT server, and GATT client APIs. Source ID:
  `SRC-ESP-IDF-BLE-API`.
- ESP-IDF BLE SMP covers pairing, key generation/distribution, bonding, and
  link-layer security levels. Source ID: `SRC-ESP-IDF-BLE-SMP`.
- Android BLE documentation distinguishes central/peripheral roles from
  GATT client/server roles. In the documented phone-to-sensor model, the phone
  scans as central and acts as GATT client while the peripheral fulfills GATT
  requests as server. Source ID: `SRC-ANDROID-BLE-OVERVIEW`.
- Android BLE GATT connection examples use `connectGatt()` to connect to a
  BLE-device-hosted GATT server, with the Android caller acting as GATT client.
  Source ID: `SRC-ANDROID-BLE-GATT-CONNECT`.
- Android Bluetooth permissions depend on target API and scan/location use;
  Android 12+ uses Bluetooth runtime permissions such as scan, advertise, and
  connect, with location handling gated by whether scan results derive
  location. Source ID: `SRC-ANDROID-BLUETOOTH-PERMISSIONS`.

## Assumptions

- ESP-WIFI-MESH is the preferred future self-healing direction, but only as a
  proposed branch until ADR-0004 is accepted.
- BLE GATT is preferred over Bluetooth Classic serial for Android phone
  client-node integration.
- Android phones are client-node interfaces, not Pi admin consoles.
- The Pi bridge remains the admin and durable-spool boundary for this slice.

## Unknowns

- No ESP-WIFI-MESH router SSID, BSSID, channel, mesh ID, max-layer value,
  router policy, root-election mode, or root pinning policy has been accepted.
- No BLE service UUIDs, characteristic UUIDs, permission modes, MTU policy,
  bonding policy, or Android app package has been accepted.
- No coexistence performance evidence exists for simultaneous ESP-WIFI-MESH
  and BLE GATT on the live boards.
- No live mesh route-table, parent-change, root-election, or healing evidence
  has been captured.

## Dashboard Metadata

The Pi bridge may attach these optional fields to `state_get` and `diag_get`
responses for simulator-first proof. They are status only and must fit the
512-byte Win31 line limit:

| Field | Meaning |
| --- | --- |
| `crypto` | Current security summary, such as compact `pmk-lmk` or `mesh-aes`. |
| `mesh` | Mesh state, such as `proposed`, `disabled`, `sim`, or `live-gated`. |
| `mesh_root` | Root mode/status, such as `none`, `candidate`, or `elected`. |
| `mesh_parent` | Parent status, such as `none`, `selected`, or `lost`. |
| `mesh_layer` | Known layer number, or `-1` when unknown. |
| `mesh_heal` | Healing status, such as `untested`, `pending`, or `observed`. |
| `ble` | BLE status, such as `planned`, `disabled`, or `connected`. |
| `ble_role` | Expected local BLE role, such as compact `gatt-srv` for ESP32 client nodes. |
| `android` | Android client presence, such as `absent`, `seen`, or `connected`. |
| `admin_gate` | Gate state for all network mutation, normally `disabled`. |

The Windows 3.1 dashboard may render these fields in a Network view using
already received metadata. It must not add live network mutation commands.

## Full-Service Discovery Host Contract

`ADR-0009` accepts `mesh_discovery.v1` as the host-only source of truth for
future topology, node, service, capability, BLE/Android presence, and
healing-event summaries. Source ID:
`SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`.

The dashboard metadata fields above are derived summaries when discovery data
exists. They are not live mesh evidence and are not an authority for
state-changing network commands.

Host-only simulator summary requests are:

- `discovery_snapshot`
- `discovery_events`
- `service_catalog`
- `capability_report`

These summaries must remain schema-versioned, ASCII, and bounded to the
512-byte bridge line limit. They do not add Gate F radio service codes and do
not accept ESP-WIFI-MESH live action.

## Live-Gate Requirements

Before ESP-WIFI-MESH work can move beyond simulator/design status:

- Reconfirm board identity, power path, voltage levels, USB-only/no-load state,
  boot-pin exposure, attached peripherals, and isolation boundaries in the same
  session as any write.
- Capture complete backups and recovery commands before any flash.
- Record build hashes, SDK configuration source, and exact firmware image paths.
- Record router SSID/BSSID/channel policy, mesh ID, max layer/downstream
  limits, root-election or fixed-root policy, route-table proof, parent proof,
  root proof, and a deliberate failure/healing proof.
- Record RF coexistence configuration and a test that exercises mesh traffic
  while BLE scan/connect/GATT traffic is active.
- Record rollback to the accepted ESP-NOW baseline.

Before BLE GATT Android work can move beyond design status:

- Record Android API level, target SDK, Bluetooth permissions, and whether BLE
  scan results are used for location.
- Record ESP32 advertising contents and prove no secrets are advertised.
- Record bonding/SMP status and app-layer security for sensitive payloads.
- Record GATT service and characteristic inventory, properties, permissions,
  MTU assumptions, and test payload bounds.
- Record Android phone presence only as client-node interface evidence, not as
  Pi admin-console authority.

## Acceptance

Simulator acceptance for this slice is limited to the Win31 dashboard showing a
Network view over the accepted COM1/nullmodem bridge with zero serial errors and
no state-changing control execution.

Live acceptance remains blocked until a later gated run captures fresh
identity, backups, build hashes, recovery commands, mesh/BLE configuration,
route/healing/coexistence proof, Android GATT proof, and cleanup evidence.
