# Custom Wireless Protocol Bridge Adapter Source Ledger

Date: 2026-05-25

## Sources Used

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIEF-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIDGE-SIM-2026-05-25`
- `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`
- `SRC-ESP-IDF-ESPNOW`

## Verified Facts

- [repo-verified] Gate C now has a simulator-only bridge adapter entry point,
  `process_bridge_request`, in
  `tools/simulators/custom_wireless_protocol/espnow_bbs_custom_protocol.py`.
- [repo-verified] The adapter accepts compact simulated bridge request frames
  for `msg_post`, `download_queue`, `telemetry_report`, `node_status`,
  `protocol_report`, `state_get`, and `control_intent`.
- [repo-verified] The adapter converts simulated `msg_post` and
  `download_queue` requests into packetized direct-message and file-chunk
  simulator jobs instead of treating ESP-NOW as a transparent stream.
- [repo-verified] The adapter rejects simulated state-changing request names
  `relay_set`, `flash`, `erase`, and `radio_set` with
  `state_changing_command_blocked`.

## Assumptions

- [assumption] The compact bridge request names are simulator fixtures only
  until owner review accepts a paired DOS-C bridge/operator implementation.
- [assumption] The adapter remains a bridge-boundary test harness and does not
  define final firmware ABI, persistent analytics schema, or live operator UI.

## Unknowns

- [unknown] No live DOSBox-X, Pi bridge, `/dev/ttyUSB0`, ESP32 coordinator,
  Win31, or OPCON transcript evidence was produced by this simulator task.
- [unknown] No firmware interface, serial transport change, radio behavior, or
  agricultural hardware profile was accepted by this task.

## Validation

- `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `python3 tools/simulators/custom_wireless_protocol/espnow_bbs_custom_protocol.py --demo`
- Additional validation is recorded in task
  `.agents/TASK_LOG/0040-custom-wireless-protocol-bridge-adapter.md`.

## Boundary Notes

- [non-goal] This ledger does not authorize flashing, serial writes, bridge
  runtime mutation, radio setting changes, PCAP, router/admin work, relay,
  XBee, TFT, MicroSD, load, mains, BLE pairing, ESP-WIFI-MESH live action,
  erase, monitor automation, or framework migration.
