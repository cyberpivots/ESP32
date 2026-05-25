# Custom Wireless Protocol Brief Source Ledger

Date: 2026-05-25

## Sources Used

- `SRC-ESP-IDF-ESPNOW`
- `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`
- `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-ESPNOW-LIVE-PREFLIGHT-2026-05-23`
- `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`
- `SRC-LINDSAY-FIELDNET-PIVOT-MONITOR-2026-05-25`
- `SRC-METER-TEROS12-2026-05-25`
- `SRC-SENTEK-DRILLDROP-2026-05-25`
- `SRC-IRROMETER-SOIL-SENSORS-2026-05-25`
- `SRC-GEOTAB-ASSET-TRACKING-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIEF-2026-05-25`

## Verified Facts

- [repo-verified] The accepted BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- [repo-verified] The bridge/operator side uses bounded ASCII JSON lines and
  keeps durable BBS storage on the Pi bridge side.
- [repo-verified] The current radio protocol evidence is packetized and
  bounded, with local source support for a 250-byte payload budget, 32-byte
  header, 190-byte body, and 16-fragment maximum.
- [live-verified] The 2026-05-23 corrected live proof records three
  `espnow-enc` peers, moving RX/TX/ACK counters, bridge transcript evidence,
  Win31 runtime evidence, and cleanup.
- [official-source-verified] ESP-NOW is connectionless action-frame transport
  and needs application-level reliability above MAC-layer send callbacks.
- [official-source-verified] Vendor sources support the existence of candidate
  telemetry classes for pivot monitoring, soil probes, and GPS asset tracking.

## Assumptions

- [assumption] The v1 custom protocol should keep the accepted
  serial-nullmodem BBS path and add packetized services behind the bridge.
- [assumption] The Pi bridge remains the durable store, reporting, and admin
  boundary until a later ADR changes that boundary.
- [assumption] ESP-NOW v1-compatible payload budgeting is the default until all
  participants and tests explicitly accept larger packets.

## Unknowns

- [unknown] No accepted local schema exists for ag telemetry, GPS pivot
  positioning, GPS asset tracking, file transfer, direct wireless messaging, or
  analytics export.
- [unknown] No live evidence exists for chunked BBS message delivery, live file
  transfer, ag telemetry, GPS telemetry, or reporting analytics over ESP-NOW.
- [unknown] No selected ag hardware profiles, power/voltage/isolation notes,
  connector notes, or sensor-protocol integration records exist.

## Boundary Notes

- [non-goal] This ledger does not authorize flashing, serial writes, relay
  control, XBee work, router/admin action, PCAP, BLE pairing, ESP-WIFI-MESH
  live action, erased flash, monitor automation, or framework migration.
- [non-goal] This ledger does not claim current live hardware state because no
  same-session read-only preflight or bridge runtime proof was run for this
  documentation task.
