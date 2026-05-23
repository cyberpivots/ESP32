# ADR-0004: ESP-NOW BBS Self-Healing Transport Branch

Status: Proposed

Date: 2026-05-23

## Context

The accepted live Windows 3.1 dashboard path is:

`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`

The current accepted radio proof is an encrypted ESP-NOW one-coordinator /
one-peer lane. That proof remains the baseline. A future branch needs a
self-healing network architecture for client-node mobility and parent/root
failure recovery without reopening packet-driver, PCAP, router-admin, relay,
XBee, TFT, MicroSD, load, or mains gates.

## Decision

Propose ESP-WIFI-MESH as the future self-healing transport branch for the
`espnow-bbs` lane.

This ADR does not accept migration yet. No firmware behavior, live build,
flash command, router setting, BLE pairing, Android application build, or
dashboard state-changing command is authorized by this ADR.

BLE GATT is proposed as the Android phone client-node integration model:

- Android phone: BLE central and GATT client.
- ESP32 client node: BLE peripheral and GATT server.

## Rationale

ESP-WIFI-MESH provides a source-backed tree network model with root election,
parent selection, routing tables, and documented self-healing behavior. That
matches the desired self-healing client-node branch better than extending the
current single-hop ESP-NOW proof without a new topology decision.

BLE GATT keeps Android phones as user/client interfaces rather than Pi admin
consoles, and it matches Android's documented central/peripheral and
GATT-client/GATT-server examples.

## Consequences

- The current encrypted ESP-NOW proof remains accepted baseline behavior.
- ESP-WIFI-MESH is only a proposed future transport until this ADR is accepted
  or replaced.
- Future live work must capture router SSID/BSSID/channel policy, mesh ID,
  root-election mode, max layer/downstream limits, route-table proof,
  self-healing proof, RF coexistence configuration, BLE GATT service inventory,
  Android permission evidence, backups, build hashes, recovery commands, and
  cleanup evidence.
- RF coexistence testing is mandatory before treating Wi-Fi mesh plus BLE as
  accepted on one ESP32 radio.

## Sources

- `SRC-ESP-IDF-ESPNOW`
- `SRC-ESP-IDF-WIFI-MESH`
- `SRC-ESP-IDF-RF-COEXIST`
- `SRC-ESP-IDF-BLE-API`
- `SRC-ESP-IDF-BLE-SMP`
- `SRC-ANDROID-BLE-OVERVIEW`
- `SRC-ANDROID-BLE-GATT-CONNECT`
- `SRC-ANDROID-BLUETOOTH-PERMISSIONS`
