# Task 0094 - ESP32-Connected XBee COM15 Live Test

## Triage

- Verified facts: The user reported that an ESP32 DevKitC on `COM15` is wired
  to an XBee device using GPIO16/GPIO17.
- Verified facts: Windows reported `COM15` as a present USB serial port, and
  local inventory recorded `COM15`, `COM6`, `COM11`, and `COM12` as host-visible
  COM ports with raw identifiers redacted.
- Verified facts: `COM15` accepted XBee command-mode readback at `9600` baud
  and returned `AP=2`, `AO=0`, `BD=3`, and `NP=100` with `SH`/`SL` redacted.
- Verified facts: `COM15` accepted XBee API local-AT read frames at `9600` baud
  and returned successful `0x88` responses for `VR`, `HV`, `SH`, `SL`, `AP`,
  `AO`, `BD`, and `NP`.
- Verified facts: A no-flash ESP32 `esptool` identity query on `COM15` failed
  with no serial data received.
- Verified facts: `COM6` did not return clean command-mode readback at `9600`
  during this gate and did not return API local-AT `0x88` responses at `9600`.
- Assumptions: The user's GPIO16/GPIO17 wiring statement is accurate, so the
  successful `COM15` XBee readback is treated as evidence for the current
  ESP32-connected XBee path. Relay/load/mains remained disconnected.
- Unknowns: Whether `COM15` is an ESP32 firmware bridge, a USB-serial adapter
  attached to the XBee path, or another transparent UART route; why ESP32
  bootloader sync failed; why `COM6` stopped responding to XBee readback; exact
  XBee carrier voltage/current margin and antenna state remain physical facts.
- Selected tier: Tier 3 live ESP32/XBee serial and radio-adjacent testing.
- Owner role: XBee/radio integration with hardware, live-bench, communications,
  and QA lenses.
- Evidence need: Host inventory, redacted XBee readback on `COM15`, bounded
  no-flash ESP32 identity attempt, and benign two-radio API proof attempt.
- Mutation boundary: `COM15` and `COM6` only; read-only AT queries; API
  local-AT read frames; one bounded two-direction benign `link_probe` API
  transmit proof attempt. No XBee setting writes, no `WR`, no `AC`, no `KY`, no
  firmware flash/update/recovery, no range/throughput loop, no relay command
  payloads, and no relay/load/mains action.
- Validation plan: Accept `COM15` path if fixed XBee readback and API local-AT
  readback pass with redacted addresses. Accept two-radio RF proof only if each
  direction shows source transmit status plus matching destination `0x90`
  receive packet.

## Evidence

Ignored local evidence directory:

```text
research/bench-records/xbee-readonly/local-esp32-uart-20260529T235908Z/
```

Key files:

- `list.json`
- `inventory.json`
- `xbee-at-query-com15-9600.json`
- `xbee-api-local-at-read-com15-com6.json`
- `esptool-chip-id-com15.txt`
- `esp32-xbee-api-link-proof-redacted.json`
- `manifest.sha256`

Raw COM/PnP identifiers, raw radio addresses, and any private serial evidence
remain local-only.

## Reviewer Quorum

- Coordinator: approved the named `COM15`/`COM6` testing boundary.
- Live Bench: approved no-flash serial identity/readback and benign
  `link_probe` proof attempts only.
- Hardware: accepted the user's wiring statement as a bench input, while
  keeping voltage/current/carrier proof open.
- Communications: approved fixed AT reads, API local-AT reads, and benign
  non-relay `link_probe` payloads.
- QA: required redacted evidence records and refused to mark OTA proof passed
  without matching destination receive packets.

No subagents were spawned; the available subagent tool requires explicit user
authorization for delegation, so role lenses were run locally.

Weighted local decision result: approval ratio `1.0`, approval weight `15/15`,
no P1/P2 blockers for the evidence steps performed.

## Outcome

`COM15` XBee access passed at `9600` baud. Command-mode readback and API
local-AT readback both returned the expected current XBee API configuration:
`AP=2`, `AO=0`, `BD=3`, and `NP=0x0100`/`100`, with addresses redacted.

The ESP32 bootloader identity proof did not pass: `esptool` could not connect
to an Espressif device on `COM15`.

The two-radio RF proof through this current setup did not pass. The bounded API
proof attempt saw `COM15 -> COM6` source transmit status with delivery OK, but
the destination `0x90` receive packet was not captured. The reverse direction
did not produce source transmit status. `COM6` also failed both command-mode
and API local-AT readback at `9600` during this gate.

## Decision

Decision: `ask_user` for the peer-side physical fact before another RF proof.

Next gate: confirm the peer XBee adapter/radio intended for `COM6` is connected,
powered, antenna-attached, and not held by XCTU/another serial client, or name
the replacement peer COM port.

Authority limits remain closed for firmware flash/update/recovery, XBee setting
writes, `WR`, `AC`, `KY`, reset/restore, range/throughput testing,
relay-command payloads, relay/load/mains action, public key/address exposure,
and broad COM-port scans.
