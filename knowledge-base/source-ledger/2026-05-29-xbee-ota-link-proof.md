# Source Ledger - 2026-05-29 XBee OTA Link Proof

## Scope

Tier 3 bidirectional over-the-air link proof for the user-selected and already
programmed `COM15` and `COM6` XBee radios.

The proof used two benign API Transmit Request frames carrying `link_probe`
payloads. It did not send relay commands, run range/throughput tests, change
radio settings, update/recover firmware, reset/restore radios, wire ESP32, or
touch relay/load/mains hardware.

## Verified Facts

- Task 0091 had already validated both selected ports at `AP=2`, `AO=0`, and
  `EE=1`.
- Local-only API AT reads captured each selected radio address for this proof.
  Raw addresses remain in ignored local evidence only.
- `COM15 -> COM6` produced a source transmit-status frame and a destination
  `0x90` receive packet with the matching benign `link_probe` payload.
- `COM6 -> COM15` produced a source transmit-status frame and a destination
  `0x90` receive packet with the matching benign `link_probe` payload.
- Both proof payloads were 70 bytes and were not relay command payloads.
- The redacted local proof record reports `ok: true` for both directions.

## Evidence Packet

Ignored local evidence directory:

```text
research/bench-records/xbee-readonly/local-ota-20260529T223657Z/
```

Public records may cite the directory path and summarize pass/fail state only.
They must not publish raw radio addresses, AES key material, raw COM/PnP
identifiers, or private full setting snapshots.

## Reviewer Quorum

- Coordinator: approved the named bidirectional link-proof gate.
- Live Bench: approved only two benign selected-port RF probes.
- Evidence: approved local-only address handling and redacted records.
- Communications: approved `link_probe` as a non-relay payload.
- QA: approved acceptance criteria requiring transmit status plus matching
  receive packet in both directions.

Weighted local decision result: approval ratio `1.0`, approval weight `15/15`,
no P1/P2 blockers, and decision `continue` through this OTA proof gate.

## Closed Surfaces

- No relay command payloads.
- No range or throughput loop.
- No XBee setting writes.
- No firmware update, firmware recovery, reset, or restore.
- No ESP32 DIN/DOUT carrier wiring.
- No relay, load, or mains action.
- No public raw radio address or key disclosure.

## Remaining Gaps

- Deployment range and throughput are not proven.
- Relay command acceptance and source allowlisting are not proven.
- Adapter markings, UART voltage, DIN/DOUT routing, ESP32 carrier wiring, and
  antenna/regulatory deployment review remain unresolved.
- Load/mains readiness remains closed.

## Validation

- PASS: `COM15 -> COM6` transmit status and matching `0x90` receive packet.
- PASS: `COM6 -> COM15` transmit status and matching `0x90` receive packet.
