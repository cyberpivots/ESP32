# Source Ledger - 2026-05-29 XBee Selected-Port Programming

## Scope

Tier 3 selected-port programming of the two user-named XBee ports, `COM15` and
`COM6`, after selected-port readback and local key provisioning.

This task does not authorize future broad discovery, firmware update/recovery,
reset/restore, API transmit frames, range/throughput tests, ESP32 DIN/DOUT
wiring, relay/load/mains action, public raw identifiers, or public key
material.

## Verified Facts

- Same-session host inventory still found the Windows XCTU install and the
  selected serial candidates.
- `XCTUcmd --version`, `XCTUcmd --help`, and `XCTUcmd list_ports` evidence was
  captured locally. The available XCTU command-line surface did not provide a
  direct AT set command; no local XBee profile file was found in the checked
  standard locations.
- `COM15` and `COM6` both responded to selected-port readback at 9600 baud.
- `COM15` pre-write state included `AP=1`, `AO=0`, `BD=3`, `NP=100`, and
  `EE=0`.
- `COM6` pre-write state included `AP=0`, `AO=0`, `BD=3`, `NP=100`, and
  `EE=0`.
- `SH` and `SL` were redacted in selected-port readback evidence.
- A failed/no-stdin writer attempt did not produce a write record. A follow-up
  command-mode readback showed both radios still at their pre-write `AP` and
  `EE` values before the successful write.
- The successful selected-port write used only `AO=0`, `KY=<redacted>`,
  `EE=1`, `AP=2`, `WR`, and `CN`.
- Post-write escaped API local-AT readback returned `AP=02`, `AO=00`, and
  `EE=01` for both selected ports.
- Post-write API readback also returned `BD=00000003` and `NP=0100` for both
  selected ports.

## Evidence Packet

Ignored local evidence directory:

```text
research/bench-records/xbee-readonly/local-programming-20260529T190752Z/
```

Public records may cite this directory path and summarize redacted status only.
They must not publish AES key material, raw COM/PnP identifiers, unredacted
`SH`/`SL`, full setting snapshots, or private address plans.

## Reviewer Quorum

- Coordinator: approved only the named selected-port write gate.
- Live Bench: approved no firmware/recovery/reset/restore/transmit/range/
  ESP32-wiring/relay/load/mains action.
- Evidence: approved redacted local proof and no key persistence in records.
- Communications: approved the profile subset and API-mode validation.
- QA: approved durable redacted records and validation evidence.

Weighted local decision result: approval ratio `1.0`, approval weight `15/15`,
no P1/P2 blockers, and decision `continue` through the selected-port write and
post-write readback gate.

## Closed Surfaces

- No all-port discovery or broad parameter scan.
- No XCTU firmware update, firmware recovery, reset, or restore.
- No `AC`.
- No API transmit, range test, or throughput test.
- No ESP32 carrier wiring.
- No relay, load, or mains action.
- No public AES key, raw identifier, or full setting snapshot disclosure.

## Remaining Gaps

- Over-the-air communication between the two radios is not proven.
- Adapter markings, UART voltage, DIN/DOUT routing, and final carrier wiring
  remain unresolved.
- Antenna/regulatory deployment review remains unresolved.
- ESP32 command acceptance, relay command acceptance, and address allowlisting
  remain future gates.

## Validation

- PASS: selected-port pre-write readback for `COM15`.
- PASS: selected-port pre-write readback for `COM6`.
- PASS: redacted selected-port write record with no key material stored.
- PASS: escaped API local-AT post-write readback for `COM15`.
- PASS: escaped API local-AT post-write readback for `COM6`.
