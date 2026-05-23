# ESP-NOW BBS Network Live-Gate Source Ledger

Date: 2026-05-23

## Sources Used

- `SRC-ESP-IDF-ESPNOW`
- `SRC-ESP-IDF-WIFI-MESH`
- `SRC-ESP-IDF-RF-COEXIST`
- `SRC-ESP-IDF-BLE-API`
- `SRC-ESP-IDF-BLE-SMP`
- `SRC-ANDROID-BLE-OVERVIEW`
- `SRC-ANDROID-BLE-GATT-CONNECT`
- `SRC-ANDROID-BLUETOOTH-PERMISSIONS`
- `SRC-LOCAL-ESPNOW-ENCRYPTED-PEER-2026-05-22`
- `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`

## Verified Facts

- The accepted baseline remains the Win31 OPCON COM1/nullmodem path through the
  Pi bridge to `/dev/ttyUSB0` and the ESP32 coordinator.
- ESP-NOW remains the accepted encrypted proof lane; ESP-WIFI-MESH is only a
  proposed future self-healing branch until ADR-0004 is accepted.
- Simulator-only metadata fields were defined for crypto, mesh, BLE, Android,
  and admin-gate status while preserving the 512-byte bridge line limit.
- BLE GATT is documented as a future Android client-node model with Android as
  central/GATT client and ESP32 client node as peripheral/GATT server.

## Assumptions

- Future ESP-WIFI-MESH work will use the accepted `espnow-bbs` ESP-IDF project
  lane if ADR-0004 is accepted.
- The Pi bridge remains the durable store and admin gate while Android phones
  remain client-node interfaces.

## Unknowns

- No live mesh root, parent, route-table, healing, or coexistence evidence has
  been captured.
- No Android BLE permission, bonding, SMP, GATT service, or app payload proof
  has been captured.
- No firmware migration from the accepted ESP-NOW proof is authorized by this
  ledger.
