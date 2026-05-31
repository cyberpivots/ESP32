# Handoff 0079 - XBee Two-Device Read-Only Study To QA

## Current State

The two-device XBee/XCTU study has a fresh no-serial Stage A1 packet. It is
still stopped before serial reads or XCTU discovery.

Ignored local evidence directory:

```text
research/bench-records/xbee-readonly/local-20260529T063940Z/
```

Local packet contents include:

- WSL no-serial `list` and `inventory` JSON.
- Windows no-serial `inventory` JSON.
- Physical-fact placeholders that keep adapter identity, antenna state,
  isolation, voltage/header/carrier, and DIN/DOUT state unknown.
- Recovery and cleanup rules.
- Weighted Stage A1 decision packet and decision output.
- SHA-256 manifest.

The local decision is `ask_user` because same-session physical evidence is
missing. No exact XBee adapter port is accepted.

After the user reported disconnecting one XBee adapter, fresh no-serial
inventories and offline identity deltas recorded one removed CP210x-style
candidate. The private mapping stays in ignored local evidence. Stage A2 still
returns `ask_user` because the second adapter mapping and physical notes are
missing.

## Files To Review

- `docs/projects/four-relay-xbee-wifi/xbee-read-only-bench-proof.md`
- `docs/projects/four-relay-xbee-wifi/xbee-radio-programming-study.md`
- `knowledge-base/source-ledger/2026-05-29-xbee-two-device-read-only-study.md`
- `knowledge-base/source-index.md`
- `research/development-status-ledger.md`
- `research/known-gaps.md`
- `.agents/TASK_LOG/0090-xbee-two-device-read-only-study.md`
- `.agents/handoffs/0079-xbee-two-device-read-only-study-to-qa.md`

## QA Focus

- Confirm public records do not include raw COM/PnP IDs, `SH`/`SL`, AES keys,
  passive bytes, full setting snapshots, or private two-port mappings.
- Confirm public records do not claim the two XBee adapter identities.
- Confirm the next action is to reconnect the first disconnected adapter,
  disconnect exactly the other XBee adapter, and provide markings/antenna/
  isolation notes; it is not a serial open or XCTU discovery.
- Confirm `readonly` remains fixed to `VR`, `HV`, `SH`, `SL`, `AP`, `AO`,
  `BD`, and `NP` and still requires `--confirm-sends-read-commands`.
- Confirm `xctu-discovery-plan` remains a locked checklist and no XCTU launch
  or discovery path was added.

## Still Blocked

Exact adapter identity, one-at-a-time disconnect/reconnect mapping, Tier B AT
readback, XCTU Discover/Add, all-port discovery, broad scans, network/remote
discovery, setting writes, `WR`, `AC`, API transmit frames, firmware
recovery/update, reset/restore, range/throughput tests, ESP32 carrier wiring,
relay/load/mains work, and public raw identifiers remain blocked.
