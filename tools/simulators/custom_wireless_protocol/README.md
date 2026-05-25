# Custom Wireless Protocol Simulator

This directory contains simulator-only helpers for the ESP-NOW BBS custom
wireless protocol Gate B and Gate C.

## Boundaries

- No hardware access.
- No serial commands.
- No flashing, erase, monitor, radio setting changes, relay, XBee, TFT,
  MicroSD, load, mains, PCAP, router/admin, BLE, or ESP-WIFI-MESH live action.
- The accepted BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Proof Surface

The simulator covers:

- 512-byte bridge line enforcement.
- ASCII JSON bridge frame validation.
- 250-byte ESP-NOW-v1-compatible radio packet budgeting.
- 32-byte header and 190-byte body constraints.
- Fragmentation, reassembly, missing-fragment detection, duplicate rejection,
  TTL expiry, custody ACKs, retry state, file resume status, telemetry reports,
  node status, reporting frames, and non-executing control intents.
- Simulated bridge request handling for compact OPCON-style `msg_post`,
  `download_queue`, `telemetry_report`, `node_status`, `protocol_report`, and
  `control_intent` frames.
- Explicit simulator rejection for state-changing bridge requests such as
  `relay_set`, `flash`, `erase`, and `radio_set`.

Run:

```sh
python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py
```
