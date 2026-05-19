# Handoff 0009 - XBee Read-Only Proof To Hardware Comms QA

## From

Hardware, Communications, QA

## To

Hardware, Communications, QA

## Summary

The XBee bench lane now has a dedicated read-only proof document and a local
probe script:

- `docs/projects/four-relay-xbee-wifi/xbee-read-only-bench-proof.md`
- `scripts/xbee_read_only_probe.py`

Tier A lists host serial candidates and can passively observe a selected port
without serial writes. Tier B sends the command-mode guard sequence and only
fixed AT read queries for `VR`, `HV`, `SH`, `SL`, `AP`, `AO`, `BD`, and `NP`,
and only after `--confirm-sends-read-commands`.

## Required next checks

- Hardware must identify the physical adapter serial port after USB attachment
  is confirmed.
- Hardware must measure the Waveshare adapter header voltage before any ESP32
  connection.
- Communications may run Tier B only after Tier A evidence exists and should
  keep `SH` and `SL` redacted unless the record remains local-only.
- QA must confirm no bench records with unredacted addresses are added to the
  public Pages artifact.

## Blockers

- XBee setting writes remain blocked.
- `WR`, `AC`, firmware updates, and factory reset actions remain blocked.
- API transmit frames and relay commands remain blocked.
- ESP32 DIN/DOUT carrier wiring remains blocked.
- Mains/load wiring remains blocked.

## Evidence

- Source-backed proof doc:
  `docs/projects/four-relay-xbee-wifi/xbee-read-only-bench-proof.md`.
- Source ledger:
  `knowledge-base/source-ledger/2026-05-18-xbee-read-only-bench-proof.md`.
- Task record:
  `.agents/TASK_LOG/0012-xbee-read-only-bench-proof.md`.
