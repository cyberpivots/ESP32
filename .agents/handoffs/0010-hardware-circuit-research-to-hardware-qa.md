# Handoff 0010 - Hardware Circuit Research To Hardware QA

## From

Hardware, Communications, QA

## To

Hardware, Communications, QA

## Summary

The project now has a consolidated source-backed hardware/circuit improvement
research package:

- `docs/projects/four-relay-xbee-wifi/hardware-circuit-improvement-research.md`
- `knowledge-base/source-ledger/2026-05-19-four-relay-hardware-circuit-improvement.md`

The package keeps protection parts, relay drivers, bench tools, XBee carrier
work, storage, TFT, mux, expander, and enclosure work at requirements level
until exact source or measurement evidence exists.

## Required next checks

- Hardware must identify the exact ESP32 board, expansion shield, relay module,
  MicroSD reader, TFT module, mux breakout, expander board, and any XBee carrier
  candidate before wiring decisions.
- Hardware must record single-source power, rail, current-limit, jumper,
  continuity, and brownout evidence before any module interconnects.
- Hardware and QA must prove relay input behavior with relay contacts
  disconnected or only a reviewed low-voltage dummy load.
- Communications must keep XBee work on the existing read-only Tier A/Tier B
  path until a separate settings-write package is authorized.
- QA must keep private bench records, raw uploads, vendor PDFs, and unredacted
  radio identifiers out of the public Pages artifact.

## Blockers

- Relay/load wiring remains blocked.
- Mains wiring design and procedures remain blocked.
- XBee setting writes, API transmit frames, relay commands, and ESP32 DIN/DOUT
  carrier wiring remain blocked.
- Final wiring diagrams, final schematics, PCB layout, and firmware source
  remain blocked by missing evidence.
- Protection component values and driver-stage selection remain blocked by
  missing rail/current/relay/load measurements.

## Evidence

- Research doc:
  `docs/projects/four-relay-xbee-wifi/hardware-circuit-improvement-research.md`.
- Source ledger:
  `knowledge-base/source-ledger/2026-05-19-four-relay-hardware-circuit-improvement.md`.
- Task record:
  `.agents/TASK_LOG/0013-hardware-circuit-improvement-research.md`.
