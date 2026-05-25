# Cross-Project Client UI Live-Gate Source Ledger

Date: 2026-05-24

Source index: [../source-index.md](../source-index.md)

## Sources Used

- `SRC-ESP-IDF-HTTP-SERVER`
- `SRC-ESP-IDF-WIFI`
- `SRC-ESP-IDF-WIFI-PROVISIONING-2026-05-24`
- `SRC-ESP-IDF-BLE-API`
- `SRC-ANDROID-BLE-OVERVIEW`
- `SRC-MDN-WEB-SERIAL-2026-05-24`
- `SRC-MDN-WEB-BLUETOOTH-2026-05-24`
- `SRC-ESP-IDF-RESTFUL-SERVER-EXAMPLE`
- `SRC-ESP-IDF-GPIO`
- `SRC-SALEAE-LOGIC-8`
- `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`
- `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`
- `SRC-LOCAL-CLIENT-UI-LIVE-GATE-2026-05-24`

## Verified Facts

- ESP-IDF HTTP Server and RESTful-server example documentation support the
  future Wi-Fi browser plan, but this task added no firmware or HTTP server
  implementation.
- ESP-IDF Wi-Fi documentation supports STA, SoftAP, and AP/STA planning, but no
  Wi-Fi mode, SSID, authentication mode, or addressing plan is accepted by this
  task.
- ESP-IDF Wi-Fi provisioning documentation covers a provisioning-manager
  example for station credentials, but no provisioning UX is accepted by this
  task.
- Android BLE and ESP-IDF BLE documentation support the later Android
  central/GATT-client and ESP32 peripheral/GATT-server model, but BLE remains
  design-only.
- MDN Web Serial and Web Bluetooth documentation were added as browser-client
  references, but browser serial/BLE live use remains blocked.
- The accepted Win31 serial-nullmodem proof path remains preserved by the new
  plan.

## Assumptions

- First user-facing live proof should prioritize phone and laptop browsers over
  BLE or Serial/UART clients.
- Future implementation should use a single safety supervisor shared by every
  client transport.
- The first state-changing live proof should use only a selected dummy output
  observed through an LED or logic-analyzer fixture.

## Unknowns

- No target board, GPIO, Wi-Fi mode, dummy fixture, browser support matrix,
  BLE UUID, Serial/UART framing, authentication, or coexistence proof has been
  accepted.
- No live client UI, firmware change, flash action, or hardware wiring change
  was performed.

## Stop Gate

This ledger does not authorize relay coil energizing, relay contacts, loads,
mains, firmware flash, firmware erase, monitor expansion, serial writes outside
the accepted command path, PCAP, router-admin work, BLE pairing, Web Bluetooth
live proof, Android app live proof, or replacement of the accepted Win31
serial-nullmodem proof path.

## Validation

- `python3 scripts/verify_scaffold.py`
- `git diff --check`
