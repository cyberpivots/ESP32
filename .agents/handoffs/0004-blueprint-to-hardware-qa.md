# Handoff 0004 - DIY Bench Hardware Blueprint

## From

Hardware

## To

Hardware, QA

## Summary

The `four-relay-xbee-wifi` project now has a staged documentation-only bench
path:

- `docs/projects/four-relay-xbee-wifi/prototype-blueprint.md`
- `docs/projects/four-relay-xbee-wifi/bench-bring-up-runbook.md`
- `docs/projects/four-relay-xbee-wifi/mains-readiness-gate.md`
- `knowledge-base/source-ledger/2026-05-18-diy-bench-hardware-blockers.md`

The package keeps relay contacts disconnected or low-voltage only, keeps the
Waveshare adapter in PC dock/read-only role, and blocks mains switching until a
qualified review package exists.

## Required next checks

- Hardware must record ESP32 dev-board and shield identity, jumper state,
  selected single power source, regulator output, current limit, and GPIO
  continuity for `GPIO25`, `GPIO26`, `GPIO27`, and `GPIO33`.
- Hardware must record relay trigger polarity, input current, 3.3 V behavior,
  and `JD-VCC`/`VCC` behavior before any ESP32 relay-input wiring.
- Hardware must keep relay contacts disconnected or use only reviewed
  low-voltage dummy loads.
- Hardware must perform only XBee read-only discovery through the Waveshare PC
  dock; no setting writes.
- QA must reject any mains wiring instructions or load-switching claims until
  `mains-readiness-gate.md` is fully closed by qualified review evidence.

## Blockers

- ESP32/shield power path and candidate GPIO routing are unverified.
- Relay direct-GPIO 3.3 V/current gate is unresolved.
- XBee adapter serial path, voltage, and DIN/DOUT direction are unresolved.
- Mains readiness is hard blocked: load type, enclosure, overcurrent
  protection, grounding/bonding, strain relief, GFCI/de-energization,
  separation, labels/disconnect, test record, and qualified review are missing.

## Evidence

- Source IDs are recorded in `knowledge-base/source-index.md`.
- Blocker closure requirements are recorded in
  `knowledge-base/source-ledger/2026-05-18-diy-bench-hardware-blockers.md`.
- Bench sequence is recorded in
  `docs/projects/four-relay-xbee-wifi/bench-bring-up-runbook.md`.
