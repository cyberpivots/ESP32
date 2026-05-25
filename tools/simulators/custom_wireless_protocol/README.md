# Custom Wireless Protocol Simulator

This directory contains simulator-only helpers for the ESP-NOW BBS custom
wireless protocol Gate B, Gate C, and the Gate E draft bridge ABI candidate.

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
- ASCII JSON bridge frame validation with `v:1` required by default on new
  simulator bridge requests.
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
- Draft stable bridge error reasons for Gate E owner review:
  `version_required`, `version_invalid`, `line_too_long`, `non_ascii`,
  `json_invalid`, `payload_invalid`, `field_type_invalid`, `hex_invalid`,
  `message_type_unknown`, and `state_changing_command_blocked`.
- Simulator-only Gate G analytics report generation for retained counters,
  custody rollups, file rollups, telemetry rollups, and fixture-only
  client/user summaries.

The draft ABI is recorded in
`docs/projects/espnow-bbs/bridge-abi-draft.md`. It is not final firmware ABI
and does not authorize live bridge, serial, radio, or hardware changes.
Analytics reports are also simulator-only; their export boundary fields remain
`simulator_only: true`, `privacy_policy: unreviewed`, and
`retention: unresolved`.

Run:

```sh
python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py
python3 tools/simulators/custom_wireless_protocol/espnow_bbs_custom_protocol.py --analytics-demo
```
