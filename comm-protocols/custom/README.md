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
- Radio packets stay v1-compatible with a 250-byte payload budget, 32-byte
  header, 190-byte body, and 16-fragment limit.
- Direct messages, file chunks, interval telemetry, node status, custody ACKs,
  and control intents are modeled as packetized services, not transparent
  streams.
- Simulated bridge requests translate compact OPCON-style `msg_post`,
  `download_queue`, `telemetry_report`, `node_status`, `protocol_report`, and
  `control_intent` frames into packetized simulator work or reporting frames.
- State-changing bridge request names such as `relay_set`, `flash`, `erase`,
  and `radio_set` are rejected by the simulator adapter.

Still unresolved:

- No firmware interface is accepted by this simulator.
- No live hardware, serial, radio, actual bridge runtime, or Win31/OPCON state
  is proven by these tests.
- Agricultural sensor, GPS, and reporting schemas remain blocked on
  source-backed hardware profiles and owner review.
