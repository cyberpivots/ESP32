# Handoff 0124: CBBS XBee Known-Profile Write Gate Blocked To QA

From: XBee/radio gate coordinator

To: QA, XBee/radio, live-bench, hardware safety, KB records

Task:
[../TASK_LOG/0165-cbbs-xbee-known-profile-write-gate-blocked.md](../TASK_LOG/0165-cbbs-xbee-known-profile-write-gate-blocked.md)

## Summary

The XBee known-profile write gate is blocked. Historical COM15/COM6 evidence is
useful source context, but it is not same-session authority for another write.

## QA Focus

- Confirm Task 0163 does not open serial ports or add XBee write/apply code.
- Confirm future write packets require current readback backup, target diff,
  voltage/isolation/antenna evidence, local-only key handling, rollback, and
  redaction.
- Confirm `AC`, firmware update/recovery, range/throughput, relay/load/mains,
  and broad RF transmit remain closed.

## Closed Surfaces

No serial write, RF transmit, XBee setting write, `WR`, `AC`, `KY`, firmware
recovery/update, range/throughput test, ESP32 carrier acceptance,
relay/load/mains work, signing, release, deploy, commit, push, or PR is
authorized by this handoff.
