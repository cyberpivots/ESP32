# Custom Wireless Protocol Simulator

This directory contains simulator-only helpers for the ESP-NOW BBS custom
wireless protocol Gate B, Gate C, the Gate E draft bridge ABI candidate, the
Phase 5/6 host-only runtime design prototype, and the host-only
`mesh_discovery.v1` discovery contract accepted by ADR-0009.

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
  `download_queue`, `telemetry_report`, `node_status`, `protocol_report`,
  `state_get`, and `control_intent` frames.
- Explicit simulator rejection for state-changing bridge requests such as
  `relay_set`, `flash`, `erase`, and `radio_set`.
- Draft stable bridge error reasons for Gate E owner review:
  `version_required`, `version_invalid`, `line_too_long`, `non_ascii`,
  `json_invalid`, `payload_invalid`, `field_type_invalid`, `hex_invalid`,
  `message_type_unknown`, and `state_changing_command_blocked`.
- Simulator-only Gate G analytics report generation for retained counters,
  custody rollups, file rollups, telemetry rollups, and fixture-only
  client/user summaries.
- Host-only Phase 6 runtime scheduling through `espnow_bbs_runtime.py`:
  balanced queue defaults, atomic backpressure, custody ACK priority, retry
  limit, expiry, duplicate handling, volatile reset, and bridge-visible runtime
  counters.
- Host-only `mesh_discovery.v1` summaries for discovery snapshots, discovery
  events, service catalog, capability reports, BLE/Android presence metadata,
  stale/lost topology transitions, and healing-event evidence.
- Recursive discovery payload rejection for secret-bearing fields such as PMK,
  LMK, pairing token, bonding key, Android identifiers, raw message bodies,
  credential fields, and precise location fields.
- Explicit simulator rejection for additional live-action request names such as
  `ble_pair`, `live_mesh`, `mesh_start`, `router_admin`, `serial_write`,
  `xbee_write`, `pcap_start`, and `monitor`.

The draft ABI is recorded in
`docs/projects/espnow-bbs/bridge-abi-draft.md`. It is not final firmware ABI
and does not authorize live bridge, serial, radio, or hardware changes.
Analytics reports are also simulator-only, but their policy fields now reference
accepted ADR-0005: `privacy_policy: adr-0005-redacted-local-operator-v1` and
`retention: 7_days`. Simulator reports still record
`simulator_only: true`, no live bridge request, no Win31 export control, and no
firmware export request.
Discovery summaries are also simulator-only: `schema:
mesh_discovery.v1`, `mode: sim`, and `admin_gate: disabled`. They do not add
Gate F radio service codes and do not authorize ESP-WIFI-MESH live action.

Run:

```sh
python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py
python3 tools/simulators/custom_wireless_protocol/espnow_bbs_custom_protocol.py --analytics-demo
```
