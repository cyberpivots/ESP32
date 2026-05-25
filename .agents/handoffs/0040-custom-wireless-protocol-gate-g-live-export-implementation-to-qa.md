# Handoff 0040 - Custom Wireless Protocol Gate G Live Export Implementation To QA

Task:
[../TASK_LOG/0051-custom-wireless-protocol-gate-g-live-export-implementation.md](../TASK_LOG/0051-custom-wireless-protocol-gate-g-live-export-implementation.md)

## Summary

Gate G v1 is opened only as a local-admin redacted JSON export from the DOS-C/Pi
bridge spool after accepted `ADR-0005`.

## Review Focus

- Confirm DOS-C export refuses in-memory spools, missing or non-accepted policy
  selection, existing destinations, and paths outside approved ignored roots.
- Confirm `analytics-report.v1.json` omits message bodies, file names, event
  details, and raw operator/client/message/file/node/device identifiers.
- Confirm simulator analytics policy fields reference accepted `ADR-0005` while
  still recording `simulator_only: true`.
- Confirm stale `analytics-report*.json` cleanup is limited to approved ignored
  export roots.

## Closed Lanes

Keep Win31/OPCON export controls, firmware export ABI, live bridge export
request types, flashing, serial-write expansion, monitor, erase, PCAP, BLE,
mesh, relay/XBee, TFT, MicroSD, load, mains, and router/admin mutation closed.
