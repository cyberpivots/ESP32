# Protocol Contract

Every protocol integration must eventually define:

- transport,
- framing,
- addressing,
- payload schema,
- retry behavior,
- timeout behavior,
- error handling,
- security assumptions,
- compatibility constraints,
- test vectors,
- source-index IDs or local design ADRs.

## Active protocol contract

`comm-protocols/wireless/xbee-api-four-relay.md` defines the current design
contract for XBee API telemetry/control messages in the
`four-relay-xbee-wifi` project.

Source IDs: `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
`SRC-DIGI-XBEE-900HP-USER-GUIDE`.

## Simulator protocol contract

`docs/projects/four-relay-xbee-wifi/dosbox-win31-simulator.md` defines the
simulator-only TCP protocol used by the DOS-C Windows 3.1 operator bridge.

Source IDs: `SRC-ESP-IDF-LWIP-SOCKETS`,
`SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19`.
