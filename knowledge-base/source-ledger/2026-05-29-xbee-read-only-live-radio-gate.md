# Source Ledger - 2026-05-29 XBee Read-Only Live-Radio Gate

## Scope

Tier 2 continued XBee/XCTU study plus Tier 3 read-only live-radio gate review.
The implemented mutation is host-only tooling, tests, and records. The live
radio portion stopped before any serial port was opened.

No XBee setting write, `WR`, `AC`, API transmit frame, firmware
update/recovery, XCTU discovery, range/throughput test, ESP32 DIN/DOUT wiring,
relay/load/mains action, or public raw identifier/private COM mapping was
performed or accepted.

## Verified facts

- Digi documents XCTU local module discovery as a selected-port workflow for
  directly connected modules, port parameters, discovery, stopping discovery,
  and adding selected devices. Source ID:
  `SRC-DIGI-XCTU-LOCAL-DISCOVERY-2026-05-29`.
- Digi documents XBee-PRO 900HP `BD` baud-rate values; the standard value
  `0x03` maps to 9600 b/s default. Source ID:
  `SRC-DIGI-XBEE-900HP-BD-2026-05-29`.
- Existing AP, AO, NP, and 900HP/XSC user-guide sources remain the command/API
  references for the fixed read-only study boundary. Source IDs:
  `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
  `SRC-DIGI-XBEE-900HP-NP`,
  `SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-05-29`.
- `scripts/xbee_radio_study.py` now supports safe `--out` records under
  `research/bench-records/xbee-readonly/`, `identity-delta`, and
  `xctu-discovery-plan`. Source ID:
  `SRC-LOCAL-XBEE-READONLY-LIVE-GATE-2026-05-29`.

## Implementation evidence

- `identity-delta` compares inventory JSON files only, reports added/removed/
  changed host candidates, hashes or omits raw PnP/hardware IDs, and records
  `serialOpenAttempted: false`, `serialWritesAttempted: false`, and
  `xctuLaunchAttempted: false`.
- `xctu-discovery-plan` accepts selected `COMx` names, emits a locked manual
  checklist and blocked-operation list, and records `serialOpenAttempted:
  false`, `serialWritesAttempted: false`, `xctuLaunchAttempted: false`, and
  `xctuDiscoveryAttempted: false`.
- Ignored local evidence directory:
  `research/bench-records/xbee-readonly/local-20260529T043721Z/`.
- Host-only WSL and Windows inventories were captured with
  `serialOpenAttempted: false`. The Windows inventory was rerun after adding
  Windows-style XCTU install-path detection for Windows Python.
- The inventory-delta evidence is host/environment evidence only. It is not a
  one-at-a-time physical disconnect/reconnect mapping and does not prove which
  candidate host ports are XBee adapters.
- The local XCTU checklist example is locked and unaccepted because confirmed
  ports and physical evidence are missing.

## Reviewer quorum

- Governance review: no P1 blocker for host-only continuation; P1 blocker for
  any live serial/XCTU action without same-session Tier 3 evidence and
  authority.
- Evidence review: no P1 blocker for read-only continuation; P2 blockers for
  unresolved adapter identity, XBee Studio host evidence, and stale public
  wording were addressed in this pass.
- QA review: required tests for no-serial-open/no-serial-write behavior,
  identity-delta redaction, locked XCTU plan behavior, fixed readonly
  allowlist, and no `apply` command.
- Live-gate review: vetoed any port open until same-session physical isolation,
  adapter identity, voltage/header evidence, antenna state, recovery path, and
  cleanup criteria exist.

## Stop condition

The Tier 3 live-radio sequence stopped before opening a serial port. Required
evidence was unavailable in this session:

- physical confirmation of no ESP32 DIN/DOUT, relay/load/mains, TFT, MicroSD,
  battery/solar, or carrier wiring;
- one-at-a-time physical disconnect/reconnect mapping for the two XBee
  adapters;
- adapter voltage/header, DIN/DOUT, reset/sleep/flow-control, and antenna
  evidence;
- recovery path and cleanup criteria for unexpected XCTU, firmware, recovery,
  or command-mode behavior.

## Blocked items

- XBee adapter identity claims.
- Tier B AT reads.
- XCTU Discover/Add, all-port discovery, broad parameter scans, network/remote
  discovery, AT/API console transmit actions, write/apply controls, firmware
  tools, recovery, range test, and throughput test.
- Setting writes, `WR`, `AC`, factory reset, API transmit frames, ESP32 carrier
  wiring, relay/load/mains work, and public raw IDs/private COM mappings.
