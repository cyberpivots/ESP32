# Handoff 0015 - Live Pi Coordinator Gate To Firmware Hardware QA

## From

Firmware, Hardware, Communications, QA

## To

Hardware, Firmware, QA, Communications

## Status

Closed for live Pi coordinator dashboard proof

## Context

The live Pi dashboard to ESP32 coordinator proof passed after the user
confirmed USB-only/no-load physical state. The Pi exposes the ESP32 USB-UART as
`/dev/ttyUSB0`, the coordinator firmware answers `hello`/`state`/`diag`, and
OPCON displayed physical coordinator telemetry through the accepted
serial-nullmodem bridge path.

## Continue With

- Hardware: keep relay/XBee/TFT/MicroSD/load/mains gates closed until separate
  source-backed physical evidence exists.
- Firmware: keep coordinator scope bounded unless ESP-NOW peer/channel/key
  proof is separately authorized.
- QA: use the physical coordinator proof artifacts as the accepted baseline for
  future dashboard regressions.
- Communications: ESP-NOW radio traffic remains unaccepted; peer/channel/key
  proof is a separate lane.

## Blockers

- ESP-NOW radio sends, relay/XBee actions, TFT or MicroSD mounts, load wiring,
  and mains work remain blocked outside this completed proof.

## Evidence

- Source ledger:
  `knowledge-base/source-ledger/2026-05-22-live-pi-coordinator-gate.md`.
- Task record:
  `.agents/TASK_LOG/0025-live-pi-coordinator-gate.md`.
- Ignored preflight:
  `research/bench-records/live-bench/live-pi-coordinator-preflight-20260522T031545Z.json`.
- Ignored Pi USB inventory:
  `research/bench-records/live-bench/local-pi-usb-serial-inventory-20260522T031618Z.txt`.
- Follow-up ignored Pi USB inventory:
  `research/bench-records/live-bench/local-pi-usb-serial-inventory-20260522T034146Z.txt`.
- Follow-up ignored UART probe:
  `research/bench-records/live-bench/local-pi-coordinator-uart-probe-20260522T034404Z.txt`.
- Follow-up ignored cleanup:
  `research/bench-records/live-bench/local-pi-coordinator-cleanup-20260522T034634Z.txt`.
- Private flash backup:
  `research/bench-records/live-bench/local-pi-read-flash-backup-20260522T035944Z.txt`.
- Coordinator flash:
  `research/bench-records/live-bench/local-pi-write-coordinator-flash-20260522T040654Z.txt`.
- Post-flash UART proof:
  `research/bench-records/live-bench/local-pi-coordinator-uart-probe-20260522T040719Z.txt`.
- Live dashboard proof summary:
  `research/bench-records/live-bench/physical-coordinator-20260522T040843Z/run-summary.txt`.
- Screenshot evidence is referenced by the summary and retained in Pi runtime
  storage; the screenshot binary is not committed to this repository.
- Final cleanup:
  `research/bench-records/live-bench/local-pi-final-cleanup-20260522T041027Z.txt`.
