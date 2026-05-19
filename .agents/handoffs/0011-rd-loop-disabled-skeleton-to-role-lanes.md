# Handoff 0011 - R&D Loop Disabled Skeleton To Role Lanes

## From

Architect, Firmware, QA, Release

## To

Architect, Hardware, Communications, Firmware, QA, Release

## Summary

The project now has a canonical milestone-based R&D loop and the first
project-local disabled ESP-IDF skeleton:

- `docs/projects/four-relay-xbee-wifi/rd-loop.md`
- `firmware/projects/four-relay-xbee-wifi/`
- `tests/four_relay_safe_core/`

The skeleton contains pure C host-testable logic for relay state, safety,
config defaults, HTTP route classification, storage status, and XBee API2
frame encode/decode. It does not write GPIO, use an expander, write XBee
settings, transmit XBee API frames to hardware, flash firmware, or mutate live
bench state.

## Required next checks

- Architect must keep later cycles aligned to the M0-M5 loop and record the
  role-lane disposition.
- Hardware must continue closing board/shield, relay, XBee carrier, MicroSD,
  TFT, mux, expander, tools, enclosure, and load gates with measured evidence.
- Communications must keep XBee work read-only until a separate write-gated
  package is authorized.
- Firmware may expand host-testable modules, but must keep hardware-facing
  outputs disabled until the relevant hardware gate is closed.
- QA must preserve negative tests for `hardware_gate_open`, unsafe state
  changes, invalid XBee frames, storage fallback, and public artifact safety.
- Release must keep public bundles allowlist-only and exclude private evidence.

## Blockers

- Relay/load wiring remains blocked.
- Mains/load design and public load wiring procedure remain blocked.
- XBee setting writes, API transmit frames to hardware, relay commands, and
  ESP32 DIN/DOUT carrier wiring remain blocked.
- Relay GPIO writes and relay-expander writes remain blocked.
- ESP-IDF build/flash validation remains blocked until ESP-IDF v6.0.1 tooling
  is installed and recorded.
- Hardware gate closure remains blocked by missing physical evidence.

## Evidence

- R&D loop doc:
  `docs/projects/four-relay-xbee-wifi/rd-loop.md`.
- Firmware skeleton:
  `firmware/projects/four-relay-xbee-wifi/README.md`.
- Host test runner:
  `tests/four_relay_safe_core/run_host_tests.py`.
- Task record:
  `.agents/TASK_LOG/0014-rd-loop-disabled-skeleton.md`.
