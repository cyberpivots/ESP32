# ESP-NOW BBS Bridge ABI Draft

Date: 2026-05-25

Status: Draft Gate E candidate; not accepted as final firmware ABI.

## Verified Facts

- Gate E keeps the accepted live path unchanged:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- New simulator bridge fixtures use a compact ASCII JSON object per line,
  terminated by `\n`, with at most 512 bytes before the newline.
- New simulator bridge request fixtures carry `v:1`.
- The required request field is `type`.
- The draft request set is `msg_post`, `download_queue`, `telemetry_report`,
  `node_status`, `protocol_report`, `state_get`, and `control_intent`.
- `ADR-0009` adds separate host-only discovery summary request names:
  `discovery_snapshot`, `discovery_events`, `service_catalog`, and
  `capability_report`. They do not change the Gate E draft request set for
  final firmware ABI review. Source ID:
  `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`.
- The draft stable bridge error reasons are `version_required`,
  `version_invalid`, `line_too_long`, `non_ascii`, `json_invalid`,
  `payload_invalid`, `field_type_invalid`, `hex_invalid`,
  `message_type_unknown`, and `state_changing_command_blocked`.
- The ESP32 Gate C simulator rejects unversioned bridge requests by default.
  Unversioned frames remain accepted only in the explicitly named legacy
  Gate B/C compatibility test path.
- DOS-C Gate D simulator fixtures now include `v:1`. The live Win31
  `download_queue` request remains payload-free.

## Assumptions

- Gate E freezes a draft simulator bridge ABI candidate for owner review; it
  does not freeze final firmware behavior.
- The Pi bridge remains the durability and live operator boundary unless a later
  accepted ADR changes that architecture.
- `control_intent` records non-executing intent only and must not be treated as
  hardware control authority.

## Unknowns

- Final firmware packet structure, firmware job queues, and runtime migration
  policy are not accepted by this draft.
- Gate G local-admin redacted analytics export policy is accepted separately in
  `ADR-0005`; live bridge export requests and firmware export ABI remain
  unresolved.
- No new live bridge transcript, Win31/OPCON screenshot, ESP32 identity,
  flashing, radio, file-transfer, or physical serial proof was produced by
  Gate E.

## Sources

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIEF-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIDGE-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-D-DOSC-PAIRING-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-E-BRIDGE-ABI-2026-05-25`

## Stop Gates

Gate E does not authorize flashing, erase, monitor, physical serial writes,
radio setting changes, live bridge mutation, PCAP, router/admin work, BLE,
ESP-WIFI-MESH live action, relay, XBee, TFT, MicroSD, load, or mains work.
