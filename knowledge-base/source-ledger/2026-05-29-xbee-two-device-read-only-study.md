# Source Ledger - 2026-05-29 XBee Two-Device Read-Only Study

## Scope

Fresh no-serial Stage A1 evidence and public record updates for a two-device
XBee/XCTU read-only study. The live-radio portion stopped before serial opens
or XCTU discovery because exact adapter identity and same-session physical
evidence are still missing.

No XBee setting write, `WR`, `AC`, API transmit frame, firmware
update/recovery, XCTU launch/discovery, all-port discovery, broad parameter
scan, range/throughput test, ESP32 DIN/DOUT wiring, relay/load/mains action,
or public raw identifier/private port mapping was performed or accepted.

## Verified Facts

- Fresh no-serial WSL inventory and Windows inventory records were captured in
  ignored local evidence under
  `research/bench-records/xbee-readonly/local-20260529T063940Z/`.
- The no-serial inventories recorded `serialOpenAttempted: false`.
- The Windows inventory showed multiple CP210x-style serial candidates; this
  is candidate host inventory only and does not prove which two physical
  adapters are XBee adapters.
- WSL still exposed legacy serial entries only for this packet; no usable
  `/dev/ttyUSB*` XBee adapter identity was proved.
- XCTU is still a reference GUI tool only. It was not launched and no discovery
  was run in this packet.
- The local weighted decision packet evaluated to `ask_user` with approval
  ratio `1.0` and no P1/P2 blockers because same-session physical evidence is
  missing.
- After the user reported disconnecting one XBee adapter, fresh no-serial
  inventories and offline identity deltas recorded one removed CP210x-style
  candidate. The exact private mapping remains local-only and is not a public
  identity claim.

## Evidence Packet

Ignored local evidence directory:

```text
research/bench-records/xbee-readonly/local-20260529T063940Z/
```

Public records may cite the directory path and summarize counts/statuses only.
They must not publish raw COM/PnP IDs, `SH`/`SL`, AES keys, passive bytes, full
setting snapshots, or private two-port mappings.

## Reviewer Quorum

- Coordinator: no P1/P2 blocker for public docs/source/status mutation inside
  the redacted no-serial boundary.
- Evidence: no P1/P2 blocker for the record shape if physical facts remain
  explicit placeholders until observed.
- Live Bench: no P1 blocker for no-serial Stage A1; Tier B reads and XCTU
  discovery remain blocked until exact adapter identity, physical isolation,
  voltage/carrier, antenna, recovery, and cleanup evidence exist.
- QA: no P1/P2 blocker for record mutation with scaffold validation and manual
  redaction review.
- Communications: no P1/P2 blocker if all closed surfaces remain closed.

## Stage Decision

`scripts/agent_process_decision.py` returned `ask_user`.

Initial required physical action was to disconnect exactly one XBee USB
adapter. That action produced one local-only candidate removal delta.

Current required physical action: reconnect the first disconnected XBee USB
adapter, then disconnect exactly the other XBee USB adapter, leave all
ESP32/relay/load/mains surfaces untouched, and provide both adapters' markings
plus antenna and isolation notes.

## Blocked Items

- Exact XBee adapter identity.
- One-at-a-time disconnect/reconnect deltas for the two adapters.
- Tier B fixed AT reads.
- XCTU selected-port local discovery.
- All-port discovery, broad scans, network/remote discovery, AT/API console
  transmit, writes, `WR`, `AC`, firmware update/recovery, reset/restore, API
  transmit frames, range/throughput tests, ESP32 carrier wiring,
  relay/load/mains work, and public raw identifiers.

## Validation

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py self-test --json`:
  PASS, 21/21.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py list --json`:
  PASS; no serial port was opened.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py inventory --json`:
  PASS; `serialOpenAttempted` was false.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_agent_process_decision tests.scaffold_audits.test_xbee_radio_study`:
  PASS, 22 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`:
  PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`:
  PASS, 45 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`: PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`: PASS.
- Parent and XBee submodule `git diff --check`: PASS.
- Public-diff redaction scan for raw/private COM/PnP and sensitive XBee
  patterns: PASS, no matches.
