# Handoff 0038 - Custom Wireless Protocol Gate G Live Export Policy To QA

Task:
[../TASK_LOG/0049-custom-wireless-protocol-gate-g-live-export-policy.md](../TASK_LOG/0049-custom-wireless-protocol-gate-g-live-export-policy.md)

## Status

Gate G is prepared for future live export review, but live analytics export
remains disabled. `ADR-0005` is proposed only.

## Verified Facts

- Owner review must accept retention period, privacy/redaction rules, export
  format, storage location, operator access, and cleanup expectations before a
  live analytics export surface is implemented.
- Until `ADR-0005` is accepted, reject live bridge/export requests, Win31/OPCON
  export controls, firmware ABI export behavior, and copied live export
  artifacts as out of scope.
- Simulator analytics tests remain the only Gate G execution surface.

## Closed Gates

Keep live bridge/export surfaces, flashing, serial writes, radio setting
changes, PCAP, router/admin mutation, BLE, ESP-WIFI-MESH live action, relay,
XBee, TFT, MicroSD, load, mains, erase, monitor, and accepted retention/privacy
policy closed unless a later explicit gate opens them.
