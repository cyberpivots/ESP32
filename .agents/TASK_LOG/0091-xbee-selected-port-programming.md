# Task 0091 - XBee Selected-Port Programming

## Triage

- Verified facts: The user selected `COM15` and `COM6` as the two XBee ports
  after the prior two-device study stopped at the mapping gate.
- Verified facts: Same-session readback on `COM15` and `COM6` succeeded at
  9600 baud before writes. `COM15` reported `AP=1`, `AO=0`, `BD=3`, and
  `EE=0`; `COM6` reported `AP=0`, `AO=0`, `BD=3`, and `EE=0`.
- Verified facts: XCTU 6.5.13 command-line evidence was captured. `XCTUcmd`
  exposes `list_ports`, `load_profile`, and `update_firmware`; no local XBee
  profile file was found in the checked standard locations.
- Assumptions: The user's selected ports, isolated bench state, attached
  antennas, and provided local key value were authoritative for this Tier 3
  gate. The key value remains secret material and is not recorded here.
- Unknowns: Exact physical adapter labels, UART voltage measurements, carrier
  DIN/DOUT routing, and over-the-air communication proof remain outside this
  task.
- Selected tier: Tier 3 live selected-port radio setting write.
- Owner role: XBee/radio integration with QA, live-bench, evidence, and
  communications role lenses.
- Evidence need: Selected-port pre-write readback, redacted write evidence,
  and post-write API local-AT readback.
- Mutation boundary: Only `COM15` and `COM6`; only `AO=0`, `KY=<redacted>`,
  `EE=1`, `AP=2`, `WR`, and `CN`. No `AC`, firmware update/recovery,
  reset/restore, API transmit frame, range/throughput test, ESP32 wiring,
  relay/load/mains action, or public key/identifier exposure.
- Validation plan: Validate final state with escaped API local-AT readback,
  checking `AP=02`, `AO=00`, and `EE=01` on both selected ports.

## Work Completed

- Captured same-session no-serial host inventory and XCTU command-line
  evidence in ignored local bench records.
- Captured selected-port pre-write readback on `COM15` and `COM6`; `SH`/`SL`
  stayed redacted.
- Stopped and re-read the radios after an attempted no-stdin writer refused or
  hung without producing a write record; the recovery readback showed no
  setting change before the successful write.
- Programmed both selected ports with the project profile subset:
  `AO=0`, `KY=<redacted>`, `EE=1`, `AP=2`, and `WR`.
- Validated both radios using escaped API local-AT frames after `AP=2`.
  `COM15` and `COM6` both returned `AP=02`, `AO=00`, `EE=01`, `BD=00000003`,
  and `NP=0100`.

## Evidence

Ignored local evidence directory:

```text
research/bench-records/xbee-readonly/local-programming-20260529T190752Z/
```

Key files:

- `baseline-inventory.json`
- `pre-readback-inventory.json`
- `com15-readback.json`
- `com6-readback.json`
- `post-hang-state-command-mode.json`
- `selected-port-write-redacted.json`
- `post-write-api-readback.json`
- `xctucmd-list-ports.txt`
- `xctucmd-version.txt`
- `xctucmd-help.txt`
- `manifest.sha256`

The local evidence records do not store the AES key value. Public records must
not publish raw COM/PnP identifiers, `SH`/`SL`, AES keys, full setting
snapshots, or private address plans.

## Reviewer Quorum

- Coordinator: approved the named selected-port write boundary.
- Live Bench: approved only `COM15` and `COM6`, with firmware/recovery,
  reset/restore, transmit, range test, ESP32 wiring, and relay/load/mains
  closed.
- Evidence: approved redacted local evidence only; key material remains absent
  from durable records.
- Communications: approved the project profile subset and API local-AT
  validation, with no RF transmit proof claim.
- QA: approved the record shape with source/doc validation and redaction
  checks.

Weighted local decision result: approval ratio `1.0`, approval weight `15/15`,
no P1/P2 blockers, and decision `continue` through the selected-port write and
post-write validation gate.

## Outcome

Selected-port programming is complete for the requested two radios. This task
accepts only local selected-port setting read/write/readback evidence. It does
not prove over-the-air communication, range, throughput, relay command
acceptance, ESP32 carrier wiring, legal/regulatory deployment state, adapter
voltage, DIN/DOUT routing, or load/mains readiness.

## Validation

- `COM15` pre-write selected-port readback: PASS.
- `COM6` pre-write selected-port readback: PASS.
- Redacted selected-port write record: PASS, no key material stored.
- Escaped API post-write readback: PASS for both selected ports.
- Post-write expected checks: PASS for `AP=02`, `AO=00`, and `EE=01` on both
  selected ports.
