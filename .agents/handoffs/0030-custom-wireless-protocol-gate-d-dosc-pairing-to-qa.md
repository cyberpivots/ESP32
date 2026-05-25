# Handoff 0030 - Custom Wireless Protocol Gate D DOS-C Pairing To QA

Task:
[../TASK_LOG/0041-custom-wireless-protocol-gate-d-dosc-pairing.md](../TASK_LOG/0041-custom-wireless-protocol-gate-d-dosc-pairing.md)

## Continue With

- Review the DOS-C Gate D fixture module and replay tests under
  `/mnt/h/dos-c/tests/espnow_bbs_bridge/`.
- Review the ESP32 Gate C simulator adapter in
  [../../tools/simulators/custom_wireless_protocol/espnow_bbs_custom_protocol.py](../../tools/simulators/custom_wireless_protocol/espnow_bbs_custom_protocol.py)
  as the replay target.
- Treat this as Gate D simulator pairing only.
- Preserve the accepted serial-nullmodem path:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Required Evidence Before Acceptance

- Passing DOS-C fixture replay tests against ESP32 Gate C.
- Passing DOS-C bridge/operator host tests with live `download_queue` still
  payload-free.
- Explicit owner review before any `v:1` bridge ABI, request/response field,
  error reason, firmware-facing structure, report field, retention behavior, or
  export behavior is treated as accepted.
- Bridge transcript plus Win31/OPCON evidence before any live acceptance claim.

## Closed Gates

Do not treat Gate D as live proof. Keep flashing, serial writes, bridge runtime
mutation, radio setting changes, PCAP, router/admin work, relay, XBee, TFT,
MicroSD, load, mains, BLE pairing, ESP-WIFI-MESH live action, erase, monitor
automation, firmware ABI migration, and framework migration closed unless a
later explicit gate opens them.
