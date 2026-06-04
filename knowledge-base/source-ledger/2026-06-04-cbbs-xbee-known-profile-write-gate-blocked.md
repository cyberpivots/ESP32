# CBBS XBee Known-Profile Write Gate Blocked Ledger

Date: 2026-06-04

Source ID:
`SRC-LOCAL-CBBS-XBEE-KNOWN-PROFILE-WRITE-GATE-BLOCKED-2026-06-04`

## Scope

Record the 2026-06-04 XBee known-profile write decision. The gate is blocked;
no serial/RF/XBee mutation is accepted.

## Verified Facts

- Task 0091 previously accepted a selected-port programming boundary for
  `COM15` and `COM6`.
- Later records corrected `COM6` as the ESP32 bridge target and `COM15` as the
  peer XBee.
- The XBee reviewer rejected any live write now because no same-session
  identity/readback backup, physical evidence, or rollback packet exists.

## Assumptions

- A future known-profile write would be limited to `AP=2`, `AO=0`, `EE=1`,
  `BD=3`, optional local-only redacted `KY`, and `WR`, with `AC` excluded
  unless separately authorized.

## Unknowns

- Current port identity, radio settings, key state, adapter/carrier voltage,
  DIN/DOUT routing, antenna/isolation state, and rollback inputs.

## Authority Limits

No serial open/write, XBee setting write, `WR`, `AC`, `KY`, API transmit, RF
test, firmware update/recovery, ESP32 carrier acceptance, relay/load/mains
action, release, publication, or deploy is authorized.

## Validation

Offline XBee study tests and read-only inventory tooling remain the validation
baseline until a separate same-session live gate is accepted.
