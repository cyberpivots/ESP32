# Task 0088 - XBee Read-Only Live-Radio Gate

## Triage

- Verified facts: Task 0086 records the offline XBee study CLI; Task 0087
  records XCTU 6.5.13.2 host install proof only; current code lacked
  `identity-delta`, `xctu-discovery-plan`, and `--out` support before this
  task.
- Assumptions: The requested continuation authorizes host-only tooling/docs
  work and planning for a read-only Tier 3 gate, but does not waive physical
  evidence, identity, recovery, or cleanup prerequisites for a serial port
  open.
- Unknowns: Which candidate host ports, if any, are the two XBee adapters;
  adapter/carrier voltage, DIN/DOUT direction, reset/sleep/flow-control state,
  antenna state, current radio settings, current baud, and recovery path.
- Selected tier: Tier 2 docs/tooling plus Tier 3 read-only live-radio gate
  review.
- Owner role: Tooling, with Communications, Hardware, Agent Operations, and QA
  lenses.
- Evidence need: Official Digi local-discovery/BD source refresh, no-serial
  tests, local-only host inventories, identity-delta output, locked XCTU
  checklist, and explicit stop condition for the live-radio gate.
- Mutation boundary: `scripts/xbee_radio_study.py`, focused tests,
  XBee/XCTU docs, source index, source ledger, status/gap/index records,
  task/handoff records, and private XBee submodule notes. No serial port open,
  XCTU launch/discovery, radio read, setting write, firmware operation, API
  transmit, ESP32 wiring, relay/load/mains action, or public raw identifiers.
- Validation plan: Focused XBee study unit tests, read-only probe self-test and
  list, safe-core host tests, scaffold audit discovery, scaffold verification,
  docs audit, and diff checks in parent and submodule.

## Work Completed

- Extended `scripts/xbee_radio_study.py` with safe `--out` support under
  `research/bench-records/xbee-readonly/`.
- Added `identity-delta --before FILE --after FILE --json` for file-only
  inventory comparison with raw PnP/hardware ID redaction.
- Added `xctu-discovery-plan --ports COMx COMy --json` to emit a locked XCTU
  selected-port local-discovery checklist without launching XCTU.
- Updated focused tests to cover no-serial behavior, output-path safety,
  identity-delta redaction, locked XCTU plan behavior, parser coverage, and no
  `apply` command.
- Captured ignored local WSL and Windows host inventories under
  `research/bench-records/xbee-readonly/local-20260529T043721Z/`; all inventory
  records show `serialOpenAttempted: false`.
- Recorded a live-gate stop condition because same-session physical isolation,
  adapter mapping, voltage/carrier, antenna, recovery, and cleanup evidence
  were missing.
- Updated public docs/status/source records and private `rlxsc-xbee-pro-s3b`
  notes.

## Reviewer Quorum

- Governance cartographer: no P1 blocker for host-only continuation; P1 for
  any live serial/XCTU operation without same-session Tier 3 authority and
  evidence.
- Evidence auditor: no P1 blocker for read-only continuation; required public
  COM wording redaction and split XCTU host proof from XBee Studio/live GUI
  evidence.
- QA validation reviewer: required `identity-delta` and
  `xctu-discovery-plan` implementation/tests before claiming those commands are
  safe.
- Live-bench reviewer: P1 veto on opening any serial port until physical
  isolation, adapter identity, voltage/header evidence, antenna state,
  recovery path, and cleanup criteria are present.

## Live Gate Outcome

The Tier 3 live-radio gate stopped before any serial port was opened. No Tier B
AT readback, XCTU Discover/Add, all-port discovery, broad parameter scan,
network/remote discovery, AT/API console action, firmware operation, recovery,
range test, throughput test, setting write, `WR`, `AC`, API transmit frame,
ESP32 DIN/DOUT wiring, relay/load/mains action, or public raw identifier/private
COM mapping was performed.

## Validation

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py self-test --json`:
  PASS, 21/21.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py list --json`:
  PASS; no serial port was opened by the list command.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_xbee_radio_study`:
  PASS, 14 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`:
  PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`:
  PASS, 34 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`: PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`: PASS.
- Parent and submodule `git diff --check`: PASS.
