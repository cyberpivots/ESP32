# Task 0095 - Corrected ESP32 COM6 Peer COM15 Live Test

## Triage

- Verified facts: The user corrected the mapping: ESP32 DevKitC is `COM6` and
  peer XBee is `COM15`.
- Verified facts: Windows inventory showed both `COM6` and `COM15` present,
  with raw COM/PnP identifiers redacted in durable records.
- Verified facts: A no-flash `esptool` identity query connected to an ESP32 on
  `COM6` and identified the chip family as ESP32. The raw MAC remains
  local-only evidence.
- Verified facts: Passive `COM6` observation at `115200` captured serial bytes
  without writes, and read-query attempts saw ESP32 boot/app text rather than
  XBee command-mode `OK`.
- Verified facts: Peer `COM15` returned successful XBee API local-AT readback at
  `9600`, including `AP=2`, `AO=0`, `BD=3`, and `NP=0x0100`, with addresses
  redacted.
- Verified facts: `COM6` did not return XBee API local-AT responses at either
  `9600` or `115200`.
- Assumptions: The XBee remains wired to ESP32 GPIO16/GPIO17 as previously
  stated, antennas are attached, and relay/load/mains are disconnected.
- Unknowns: ESP32 firmware currently running on `COM6`, whether it is intended
  to bridge USB serial to UART2/GPIO16-GPIO17, ESP32-to-XBee UART direction,
  and physical voltage/current margin.
- Selected tier: Tier 3 live ESP32/XBee serial and RF-adjacent test.
- Owner role: XBee/radio integration with hardware, live-bench,
  communications, and QA lenses.
- Evidence need: Redacted port inventory, ESP32 identity proof on `COM6`, peer
  XBee readback on `COM15`, and corrected benign API `link_probe` proof.
- Mutation boundary: `COM6` and `COM15` only; passive serial observation,
  no-flash ESP32 identity query, fixed read-only XBee AT/API local-AT queries,
  and one bounded two-direction benign `link_probe` API transmit proof. No XBee
  setting writes, no `WR`, no `AC`, no `KY`, no firmware flash/update/recovery,
  no reset/restore beyond normal serial open/esptool hard-reset behavior, no
  range/throughput loop, no relay command payloads, and no relay/load/mains
  action.
- Validation plan: Accept corrected OTA/API proof only if each direction shows a
  source transmit-status frame plus a matching destination `0x90` receive packet
  for the benign payload.

## Evidence

Ignored local evidence directory:

```text
research/bench-records/xbee-readonly/local-esp32-uart-corrected-20260530T005613Z/
```

Key files:

- `list.json`
- `inventory.json`
- `passive-com6-115200.json`
- `esptool-chip-id-com6-retry.txt`
- `xbee-api-local-at-read-com6-com15.json`
- `xbee-api-local-at-read-com6-115200.json`
- `xbee-at-query-com6-115200-retry.json`
- `esp32-xbee-api-link-proof-corrected-redacted.json`
- `manifest.sha256`

Raw COM/PnP identifiers, ESP32 MAC, raw radio addresses, and any private serial
bytes remain local-only.

## Reviewer Quorum

- Coordinator: approved the corrected `COM6` ESP32 / `COM15` peer test
  boundary.
- Live Bench: approved no-flash ESP32 identity proof and bounded serial/radio
  observations only.
- Hardware: accepted the user's physical mapping as bench input while keeping
  voltage/current and wiring-direction proof open.
- Communications: approved fixed read queries and benign non-relay `link_probe`
  payloads only.
- QA: required source transmit status plus matching destination `0x90` receive
  packet before accepting OTA/API proof.

No subagents were spawned; the available subagent tool requires explicit user
authorization for delegation, so role lenses were run locally.

Weighted local decision result: approval ratio `1.0`, approval weight `15/15`,
no P1/P2 blockers for the named evidence steps.

## Outcome

The corrected mapping is verified at the host-serial level: `COM6` is an ESP32
serial device, and `COM15` is a healthy XBee API peer at `9600`.

The ESP32-connected XBee API bridge is not proven. `COM6` produced ESP32 serial
traffic and ESP32 identity proof, but did not return XBee API local-AT responses
at `9600` or `115200`.

The corrected `link_probe` proof did not meet acceptance criteria:

- `COM6 -> COM15`: no source transmit-status frame and no matching destination
  receive packet.
- `COM15 -> COM6`: peer `COM15` saw source transmit-status delivery OK, but
  the destination `0x90` receive packet was not observed on `COM6`.

This indicates the peer can get radio-layer delivery acknowledgement toward the
XBee associated with the `COM6` side, but the ESP32 `COM6` serial path is not
currently exposing bidirectional XBee API frames to the host.

## Decision

Decision: `ask_user`.

Next gate: confirm or flash/run an ESP32 firmware bridge that maps USB serial
`COM6` at the selected host baud to UART2 on GPIO16/GPIO17 at the XBee baud, or
authorize a separate firmware build/flash gate for that bridge.

Authority limits remain closed for firmware flash/update/recovery, XBee setting
writes, `WR`, `AC`, `KY`, reset/restore beyond the completed no-flash identity
query, range/throughput testing, relay-command payloads, relay/load/mains
action, public key/address/MAC exposure, and broad COM-port scans.
