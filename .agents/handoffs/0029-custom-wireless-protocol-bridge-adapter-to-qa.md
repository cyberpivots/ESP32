# Handoff 0029 - Custom Wireless Protocol Bridge Adapter To QA

Task:
[../TASK_LOG/0040-custom-wireless-protocol-bridge-adapter.md](../TASK_LOG/0040-custom-wireless-protocol-bridge-adapter.md)

## Continue With

- Review `process_bridge_request` in
  [../../tools/simulators/custom_wireless_protocol/espnow_bbs_custom_protocol.py](../../tools/simulators/custom_wireless_protocol/espnow_bbs_custom_protocol.py)
  and the bridge-adapter tests in
  [../../tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py](../../tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py).
- Treat this as Gate C simulator proof only.
- Pair any future bridge/operator implementation with DOS-C evidence while
  preserving the accepted serial-nullmodem path:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Required Evidence Before Acceptance

- Passing simulator tests for bridge request translation, packetized direct
  messages, file-queue fragmentation, telemetry/status report handling,
  compact reporting, non-executing control intents, state-changing request
  rejection, and non-ASCII rejection.
- Paired DOS-C bridge/operator fixtures before request names or field names are
  treated as accepted integration ABI.
- Bridge transcript plus Win31/OPCON evidence before any live acceptance claim.
- Owner review before any public protocol type, field, status name, retention
  rule, or analytics export behavior is treated as final.

## Closed Gates

Do not treat the simulator as live proof. Keep flashing, serial writes, bridge
runtime mutation, radio setting changes, PCAP, router/admin work, relay, XBee,
TFT, MicroSD, load, mains, BLE pairing, ESP-WIFI-MESH live action, erase,
monitor automation, and framework migration closed unless a later explicit gate
opens them.
