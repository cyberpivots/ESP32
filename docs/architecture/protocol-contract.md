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
