# XBee Tier A No-Serial Identity Evidence Ledger

Date: 2026-06-05

Source ID:
`SRC-LOCAL-XBEE-TIER-A-NO-SERIAL-IDENTITY-EVIDENCE-2026-06-05`

## Scope

Tier 2 record-only/no-serial XBee identity-evidence status packet. This ledger
records reviewer quorum output, no-serial host validation, redaction limits,
and durable status updates. It does not complete Tier A and does not open any
serial, RF, XBee write, Digi GUI, firmware, wiring, relay/load, mains, release,
publication, commit, push, PR, or deploy authority.

## Source Coverage

- XBee host-only study tooling is recorded by
  `SRC-LOCAL-XBEE-RADIO-STUDY-2026-05-29`.
- The read-only bench proof baseline is recorded by
  `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18` and
  `SRC-LOCAL-XBEE-READONLY-LIVE-GATE-2026-05-29`.
- The first two-device no-serial Stage A1/A2 packet is recorded by
  `SRC-LOCAL-XBEE-TWO-DEVICE-READONLY-STUDY-2026-05-29`.
- Historical selected-port programming, benign RF proof, corrected mapping,
  and COM6 bridge retest are recorded by
  `SRC-LOCAL-XBEE-SELECTED-PORT-PROGRAMMING-2026-05-29`,
  `SRC-LOCAL-XBEE-OTA-LINK-PROOF-2026-05-29`,
  `SRC-LOCAL-CORRECTED-ESP32-COM6-PEER-COM15-LIVE-TEST-2026-05-30`, and
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- Host-only hub-spoke planning is recorded by
  `SRC-LOCAL-XBEE-HUB-SPOKE-HOST-PLAN-2026-06-05`.
- Digi and Waveshare source coverage remains under the existing XBee source
  rows for part identity, API frame planning, XCTU/XBee Studio reference
  tooling, and adapter boundary.

## Verified Facts

- The approved agentic sequence identifies XBee Tier A identity evidence as the
  next XBee continuation after PF0530W host validation.
- The active mutation boundary is record-only/no-serial.
- Read-only reviewers approved the named records boundary with 17/17 weighted
  approval and no P1/P2 blockers.
- `scripts/xbee_radio_study.py inventory --json` and `hub-spoke-plan --json`
  report no serial open in their packet metadata.
- `scripts/xbee_read_only_probe.py self-test --json` passed 21/21 tests.
- `scripts/xbee_read_only_probe.py list --json` returns an OK read-only list
  packet. Its boundary wording is in the payload and notes, not a top-level
  `serialOpenAttempted` field.
- XBee hub-spoke host tests, XBee radio-study scaffold tests, and four-relay
  safe-core host tests passed before this record mutation.

## Assumptions

- Public records can cite source IDs and redacted summaries but should not
  include raw COM/PnP mappings, `SH`/`SL`, AES keys, address plans, passive
  bytes, full snapshots, or private local evidence.
- Historical programming/RF/bridge records remain valid only for their named
  boundaries and do not prove current physical adapter identity.

## Unknowns

- Exact current two-adapter identity remains unresolved.
- The second one-at-a-time adapter disconnect/reconnect delta is not recorded.
- Same-session physical adapter markings, antenna state, isolation notes,
  voltage/header/carrier facts, recovery path, and cleanup evidence are not
  attached.
- Current radio settings, XCTU readiness, XBee Studio readiness, Tier B read
  safety, live RF behavior, range, throughput, relay payload readiness, and
  load/mains readiness remain unresolved.

## Authority Limits

This record does not authorize Tier B AT reads, XCTU selected-port local
discovery, XBee Studio operation, serial open, broad COM scans, API transmit,
RF/range/throughput, setting writes, `WR`, `AC`, `KY`, firmware update/recovery,
ESP32 carrier wiring, relay/load/mains, flash, erase, monitor, release,
publication, commit, push, PR, deploy, `/etc/codex/requirements.toml`, or
`admin-strict` mutation.

## Validation

Pre-record validation completed on 2026-06-05:

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py inventory --json`
  with `serialOpenAttempted=false`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py self-test --json`
  (21/21).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py list --json`
  returned an OK read-only list packet.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py hub-spoke-plan --json`
  with `serialOpenAttempted=false`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/xbee_hub_spoke -p 'test_*.py'`
  (5 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_xbee_radio_study`
  (16 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`.

Post-record validation completed on 2026-06-05:

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py self-test --json`
  (21/21).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py list --json`;
  result `ok=true`, with no top-level `serialOpenAttempted` field and a
  `readOnlyBoundary` payload.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py inventory --json`;
  result `ok=true`, `serialOpenAttempted=false`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py identity-delta --before /tmp/xbee-inventory-0182-before.json --after /tmp/xbee-inventory-0182-after.json --json`;
  result `ok=true`, `serialOpenAttempted=false`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py xctu-discovery-plan --ports COM15 COM6 --json`;
  result `ok=true`, `serialOpenAttempted=false`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py hub-spoke-plan --json`;
  result `ok=true`, `serialOpenAttempted=false`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/xbee_hub_spoke -p 'test_*.py'`
  (5 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_xbee_radio_study`
  (16 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 182`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `git diff --check`.

## Decision

Decision: accept the no-serial XBee identity-evidence status packet. Tier A
remains open until second-adapter one-at-a-time delta and same-session physical
adapter, antenna, isolation, voltage/header/carrier, recovery, and cleanup
evidence are recorded.
