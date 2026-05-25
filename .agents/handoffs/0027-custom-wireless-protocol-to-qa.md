# Handoff 0027 - Custom Wireless Protocol To QA

Task:
[../TASK_LOG/0038-custom-wireless-protocol-brief.md](../TASK_LOG/0038-custom-wireless-protocol-brief.md)

## Continue With

- Use
  [../../docs/projects/espnow-bbs/custom-wireless-protocol-brief.md](../../docs/projects/espnow-bbs/custom-wireless-protocol-brief.md)
  as the protocol research baseline.
- Keep Gate B simulator-only until direct message, file chunk, telemetry,
  node-status, custody ACK, and reporting fixtures pass without live hardware.
- Preserve the accepted
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`
  boundary unless a later explicit ADR changes it.

## Required Evidence Before Acceptance

- Simulator proof for line-size enforcement, ASCII/JSON compatibility,
  envelope encode/decode, fragmentation/reassembly, ACK/retry/dedupe, TTL,
  custody status, file resume, telemetry batching, and reporting fixtures.
- Source-backed schema or ADR for any public protocol type, field, status name,
  retention policy, or analytics export behavior.
- Hardware profiles before any selected ag sensor, GPS receiver, pivot
  controller, asset tracker, SDI-12 adapter, or Modbus adapter is treated as a
  project target.
- Fresh same-session read-only preflight, manifest/backups, explicit write
  authorization if firmware changes exist, bridge transcript, Win31/OPCON
  evidence, and cleanup before live acceptance.

## Closed Gates

Do not use this brief as live implementation authority. Keep flashing, serial
writes, bridge runtime mutation, radio setting changes, PCAP, router/admin
work, relay, XBee, TFT, MicroSD, load, mains, BLE pairing, ESP-WIFI-MESH live
action, erase, monitor automation, and framework migration closed unless a
later explicit gate opens them.
