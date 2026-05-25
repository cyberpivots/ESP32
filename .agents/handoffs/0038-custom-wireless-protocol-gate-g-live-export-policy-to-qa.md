# Handoff 0038 - Custom Wireless Protocol Gate G Live Export Policy To QA

Task:
[../TASK_LOG/0049-custom-wireless-protocol-gate-g-live-export-policy.md](../TASK_LOG/0049-custom-wireless-protocol-gate-g-live-export-policy.md)

## Status

Gate G was prepared for future live export review by this handoff. It has since
been superseded: `ADR-0005` is accepted and implementation is tracked in
task 0051.

## Verified Facts

- At the time of this handoff, owner review still needed to accept retention
  period, privacy/redaction rules, export format, storage location, operator
  access, and cleanup expectations before implementation.
- At the time of this handoff, live bridge/export requests, Win31/OPCON export
  controls, firmware ABI export behavior, and copied live export artifacts were
  out of scope.
- This handoff is superseded by task 0051 for the local-admin redacted JSON
  export surface.

## Closed Gates

Keep flashing, serial writes, radio setting changes, PCAP, router/admin
mutation, BLE, ESP-WIFI-MESH live action, relay, XBee, TFT, MicroSD, load,
mains, erase, and monitor closed unless a later explicit gate opens them. Gate G
export is open only for the local-admin redacted JSON surface from task 0051.
