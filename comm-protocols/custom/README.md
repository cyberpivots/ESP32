# Custom Protocols

Seed area for repository-defined framing, payload schemas, and validation
vectors.

## ESP-NOW BBS Custom Wireless Protocol

The simulator-only proof for the ESP-NOW BBS custom protocol lives under
`tools/simulators/custom_wireless_protocol/` with regression tests in
`tests/custom_wireless_protocol/`.

Verified boundaries:

- The simulator keeps the accepted BBS path external to the radio payload:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- Bridge frames stay newline-delimited ASCII JSON and fit the 512-byte line
  budget.
- Gate E draft bridge ABI fixtures require `v:1` on new simulator requests.
  Legacy unversioned requests are accepted only through the explicitly marked
  Gate B/C compatibility test path.
- Radio packets stay v1-compatible with a 250-byte payload budget, 32-byte
  header, 190-byte body, and 16-fragment limit.
- Direct messages, file chunks, interval telemetry, node status, custody ACKs,
  and control intents are modeled as packetized services, not transparent
  streams.
- Simulated bridge requests translate compact OPCON-style `msg_post`,
  `download_queue`, `telemetry_report`, `node_status`, `protocol_report`,
  `state_get`, and `control_intent` frames into packetized simulator work or
  reporting frames.
- State-changing bridge request names such as `relay_set`, `flash`, `erase`,
  and `radio_set` are rejected by the simulator adapter.
- The Gate E draft stable error-reason set is `version_required`,
  `version_invalid`, `line_too_long`, `non_ascii`, `json_invalid`,
  `payload_invalid`, `field_type_invalid`, `hex_invalid`,
  `message_type_unknown`, and `state_changing_command_blocked`.
- Gate G analytics reports are simulator-only and now reference accepted
  ADR-0005 policy fields: `privacy_policy:
  adr-0005-redacted-local-operator-v1` and `retention: 7_days`.

Still unresolved:

- Gate E is a draft bridge ABI freeze candidate only. No firmware interface is
  accepted by this simulator.
- No live hardware, serial, radio, actual bridge runtime, or Win31/OPCON state
  is proven by these tests.
- Gate G live export is accepted only as a local-admin redacted JSON export
  from the DOS-C/Pi bridge spool. No Win31/OPCON export UI, firmware export ABI,
  or bridge export request type is accepted.
- Agricultural sensor, GPS, and reporting schemas remain blocked on
  source-backed hardware profiles and owner review.
