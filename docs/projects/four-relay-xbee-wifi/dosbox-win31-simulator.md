# DOS-C Windows 3.1 Simulator Bridge

## Verified Facts

- The current project safe-core contract uses public relay channels `1..4` and
  rejects out-of-range channels. Source ID:
  `SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19`.
- ESP-IDF's lwIP documentation identifies BSD sockets as the supported
  application-facing socket API in ESP-IDF. Source ID:
  `SRC-ESP-IDF-LWIP-SOCKETS`.
- The simulator in `tools/simulators/esp32_gateway_tcp/` is host-side Python
  only. It does not flash firmware, write GPIO, write XBee settings, transmit
  XBee frames, or touch live hardware.

## Protocol

- TCP port: `31331`.
- Framing: newline-delimited ASCII JSON.
- Maximum line length: 512 bytes before newline.
- Messages from DOS-C guest: `hello`, `ping`, `state_get`, and future
  `relay_set`.
- Messages from simulator: `ack`, `state`, and `error`.
- `relay_set` is accepted as a visible UI intent but returns
  `control_disabled` in v1.
- `state` responses are compacted to remain within the 512-byte line limit
  used by the DOS-C Windows 3.1 client.

## Assumptions

- The first proof is DOSBox-X SLIRP from guest `10.0.2.15` to Pi-host gateway
  `10.0.2.2:31331`.
- The simulator state mirrors the existing safe-core shape closely enough for
  UI and protocol proofing, while real relay, XBee, storage, and safety logic
  remains in the firmware lane.

## Unknowns

- Live DOSBox-X SLIRP packet flow from the Windows 3.1 operator app is not yet
  accepted.
- PCAP bridge behavior on wired `eth0` is not yet accepted and remains gated by
  Pi identity, `cap_net_raw`, rollback, and capture-redaction evidence.
- No live ESP32 socket task is implemented in firmware in this v1 simulator
  pass.
