# Task 0092 - XBee OTA Link Proof

## Triage

- Verified facts: Task 0091 programmed user-selected `COM15` and `COM6` to
  `AP=2`, `AO=0`, and `EE=1` with redacted key handling, then validated both
  ports with escaped API local-AT readback.
- Verified facts: The current user opened the next over-the-air communication
  proof gate while keeping relay/load/mains action closed.
- Assumptions: Both radios remained on USB adapters with antennas attached and
  no ESP32 GPIO, relay, load, or mains connection.
- Unknowns: Adapter markings, UART voltage, DIN/DOUT routing, final ESP32
  carrier wiring, regulatory deployment state, and real deployment range remain
  unresolved.
- Selected tier: Tier 3 live RF/API transmit proof.
- Owner role: XBee/radio integration with QA, live-bench, evidence, and
  communications role lenses.
- Evidence need: Local-only address readback, benign bidirectional API
  transmit proof, destination receive packets, source transmit-status frames,
  and redacted durable records.
- Mutation boundary: `COM15` and `COM6` only; local API AT reads for
  `SH`, `SL`, `AP`, `AO`, and `EE`; two benign API Transmit Request frames
  carrying `link_probe` payloads. No relay command payloads, no range/
  throughput loop, no setting writes, no firmware update/recovery,
  reset/restore, ESP32 wiring, or relay/load/mains action.
- Validation plan: Require both directions to show a source transmit status
  with successful delivery and a destination `0x90` receive packet whose
  payload hash and content match the sent `link_probe`.

## Work Completed

- Captured local-only selected-port address readback for `COM15` and `COM6`.
  Raw addresses remain private in ignored bench evidence and are not repeated
  in public records.
- Sent one benign `link_probe` payload from `COM15` to `COM6`.
- Sent one benign `link_probe` payload from `COM6` to `COM15`.
- Confirmed transmit-status frames and matching destination receive-packet
  frames in both directions.
- Did not send relay command payloads, run a range/throughput test, change
  settings, update firmware, reset/restore radios, wire ESP32, or touch
  relay/load/mains surfaces.

## Evidence

Ignored local evidence directory:

```text
research/bench-records/xbee-readonly/local-ota-20260529T223657Z/
```

Key files:

- `selected-port-address-readback-private.json`
- `ota-link-proof-redacted.json`
- `manifest.sha256`

Public records may cite this directory and summarize pass/fail status only.
They must not publish raw radio addresses, AES key material, raw COM/PnP
identifiers, or full private setting snapshots.

## Reviewer Quorum

- Coordinator: approved the named bidirectional link-proof boundary.
- Live Bench: approved only two benign selected-port API transmit probes, with
  range/throughput, firmware/recovery/reset/restore, ESP32 wiring, and
  relay/load/mains closed.
- Evidence: approved local-only address evidence and redacted public records.
- Communications: approved `link_probe` payloads as non-relay proof payloads.
- QA: approved acceptance criteria requiring transmit status and matching
  receive packet in each direction.

Weighted local decision result: approval ratio `1.0`, approval weight `15/15`,
no P1/P2 blockers, and decision `continue` through the named OTA proof gate.

## Outcome

Bidirectional over-the-air communication is proven locally for the selected
`COM15` and `COM6` XBee radios with the current encrypted API configuration.
Both directions passed: source transmit status was observed and the destination
received the matching `link_probe` payload.

This does not prove deployment range, throughput, relay command acceptance,
ESP32 carrier wiring, UART voltage, DIN/DOUT routing, antenna/regulatory
deployment readiness, or load/mains readiness.

## Validation

- `COM15 -> COM6` benign `link_probe`: PASS.
- `COM6 -> COM15` benign `link_probe`: PASS.
- Relay command payloads sent: none.
- Range/throughput test run: none.
- Setting writes during this gate: none.
