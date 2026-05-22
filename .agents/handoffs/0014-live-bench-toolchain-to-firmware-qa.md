# Handoff 0014 - Live Bench Toolchain To Firmware QA

## From

Firmware, Hardware, Communications, QA, Release

## To

Firmware, QA, Hardware, Communications

## Status

Open

## Context

The live-bench cycle closed read-only identity and build-proof gaps for
`four-relay-xbee-wifi`. The workspace now has a repeatable preflight script,
fresh COM6 and Pi identity evidence, EIM-based ESP-IDF v6.0.1 activation proof,
and a passing build for the disabled ESP-IDF skeleton.

## Continue With

- Firmware: keep the disabled skeleton buildable under ESP-IDF v6.0.1 after
  sourcing `/home/cyber/.espressif/tools/activate_idf_v6.0.1.sh`.
- QA: preserve host tests, protocol tests, scaffold verification, public
  manifest audit, Pages smoke checks, and `git diff --check`.
- Hardware: collect separate physical USB-only, no-load, no relay/TFT/MicroSD
  or XBee wiring evidence before any future flash gate.
- Communications: keep XBee and ESP-NOW work read-only or simulated until a
  separate gate authorizes writes or radio traffic.

## Blockers

- Firmware flashing and monitor automation remain blocked.
- Relay switching, relay GPIO writes, expander writes, and load wiring remain
  blocked.
- XBee setting writes, XBee API transmit frames, and ESP-NOW radio sends remain
  blocked.
- TFT and MicroSD wiring or mounts remain blocked.
- Mains work remains blocked.
- OpenOCD udev-rule installation was not completed by EIM because elevated
  permissions are required.
- A private recovery record and flash backup, or an explicit sourced reason a
  backup is not possible, are still required before any future flashing review.

## Evidence

- Live bench source ledger:
  `knowledge-base/source-ledger/2026-05-21-live-bench-toolchain.md`.
- Toolchain record:
  `knowledge-base/toolchain/four-relay-xbee-wifi-toolchain.md`.
- Bench runbook:
  `docs/projects/four-relay-xbee-wifi/bench-bring-up-runbook.md`.
- Preflight script:
  `scripts/live_bench_preflight.py`.
- Task record:
  `.agents/TASK_LOG/0024-live-bench-toolchain.md`.
