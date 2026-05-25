# Handoff 0028 - Custom Wireless Protocol Simulator To QA

Task:
[../TASK_LOG/0039-custom-wireless-protocol-simulator.md](../TASK_LOG/0039-custom-wireless-protocol-simulator.md)

## Continue With

- Review
  [../../tools/simulators/custom_wireless_protocol/espnow_bbs_custom_protocol.py](../../tools/simulators/custom_wireless_protocol/espnow_bbs_custom_protocol.py)
  and
  [../../tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py](../../tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py).
- Treat this as Gate B simulator proof only.
- Gate C should connect these fixtures to bridge/operator integration tests
  without live hardware, physical coordinator serial writes, or radio changes.

## Required Evidence Before Acceptance

- Passing simulator tests for bridge line validation, radio packet bounds,
  fragmentation/reassembly, missing-fragment detection, duplicate rejection,
  TTL expiry, custody ACKs, direct-message packets, file resume state,
  telemetry reports, node status, reporting frames, and non-executing control
  intents.
- Owner review before any public protocol type, field, status name, retention
  rule, or analytics export behavior is treated as final.
- Separate source-backed hardware profiles before ag telemetry, GPS pivot
  positioning, GPS asset tracking, SDI-12, or Modbus targets are implemented.

## Closed Gates

Do not treat the simulator as live proof. Keep flashing, serial writes, bridge
runtime mutation, radio setting changes, PCAP, router/admin work, relay, XBee,
TFT, MicroSD, load, mains, BLE pairing, ESP-WIFI-MESH live action, erase,
monitor automation, and framework migration closed unless a later explicit gate
opens them.
