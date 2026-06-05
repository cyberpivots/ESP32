# Task 0176 - XBee Hub-Spoke Host-Only Plan

## Summary

Implemented a source-backed, host-only XBee hub-spoke planning matrix and
simulator. The task corrected implementation-facing transmit-status records to
use 900HP Extended Transmit Status `0x8B` for `0x10` requests before adding
synthetic planning fixtures.

Source IDs:

- `SRC-DIGI-XBP9B-DPUT-001`
- `SRC-DIGI-XBEE-900HP-AP`
- `SRC-DIGI-XBEE-900HP-AO`
- `SRC-DIGI-XBEE-900HP-NP`
- `SRC-DIGI-XBEE-900HP-DELIVERY`
- `SRC-DIGI-XBEE-900HP-TO-2026-06-05`
- `SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-06-05`
- `SRC-DIGI-XCTU-SUPPORT-2026-06-05`
- `SRC-DIGI-XBEE-STUDIO-SUPPORT-2026-06-05`
- `SRC-LOCAL-XBEE-HUB-SPOKE-HOST-PLAN-2026-06-05`

## Routing

- Selected tier: Tier 2.
- Owner role: Communications with Tooling, QA, RNW bridge safety, and Agent
  Operations review.
- Evidence need: source-indexed Digi command/API facts, local XBee records,
  host-only tests, and durable task/source ledger.
- Mutation boundary: docs, source-index/source-ledger/task records, offline
  simulator, offline CLI command, tests, and Hardware Tools saved-evidence
  metadata.
- Gate authority: no Tier 3 authority. No serial open, AT read/write, `WR`,
  `AC`, `KY`, XCTU/XBee Studio launch, API transmit to hardware, RF/range/
  throughput, firmware update/recovery, bridge dispatch, wiring, relay/load/
  mains, release, commit, push, PR, or deploy.
- Trust boundary: synthetic fixture metadata only; no raw radio identifiers,
  keys, address plan, private COM mapping, passive bytes, or full setting
  snapshots.

## Authority Limits

Authority limits are host-only. This task accepts docs, records, simulator,
offline CLI, tests, and review-only product metadata. It does not authorize any
Tier 3 live bench, serial, RF, XBee write, firmware, bridge-dispatch, wiring,
relay/load/mains, release, publication, commit, push, PR, or deploy surface.

## Reviewer quorum

Read-only reviewers were spawned and closed:

- XBee protocol reviewer: approved host-only boundary with no P1 blockers.
- QA validation reviewer: approved with conditions for redaction, records, and
  no-live-surface tests.
- RNW bridge safety reviewer: approved review-only Hardware Tools boundary and
  kept `serial_write`/`rf_xbee_write` closed.
- Source research reviewer: initially found a P1 `0x89`/`0x8B` mismatch, then
  cleared the staged boundary after the first step was narrowed to correcting
  records to `0x8B` before simulator/tooling work.

Weighted result: 17/17 including coordinator after the staged correction; no
remaining P1/P2 blocker for host-only mutation. Tier 3 remains closed.

## Verified facts

- The current exact part is recorded as `XBP9B-DPUT-001`.
- Digi 900HP references support `AP=2`, `AO=0`, `NP`, `TO`, `0x10`, `0x8B`,
  and `0x90` planning facts.
- The repo already had offline XBee study tooling and blocked write-plan
  behavior; this task adds only host-only planning behavior.

## Assumptions

- Hub-spoke planning uses point-to-multipoint semantics for the current 10k
  part.
- Hardware Tools displays saved evidence only and does not dispatch native or
  host bridge calls.

## Unknowns

- Current radio settings, port identity, key state, address plan, antenna,
  carrier wiring, voltage, live payload limit, range, throughput, and field
  power behavior remain unverified.

## Validation

Validation completed on 2026-06-05:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py hub-spoke-plan --json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/xbee_hub_spoke -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_xbee_radio_study
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py self-test --json
PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py
pnpm test -- packages/cbbs-product/__tests__/product.test.ts packages/cbbs-product-ui/__tests__/ProductWindowsShell.test.tsx
pnpm --filter @cbbs/hardware-tools-windows test:windows
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 176
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'
git diff --check
```

All listed commands passed. `git diff --check` emitted only the existing CRLF
normalization warning for the dirty RNW C++ file.

## Decision

Decision: accept the bounded host-only implementation. The next continuation is
QA/Communications review of simulator semantics and any future Tier 3 live gate
only after same-session evidence and explicit authority.

## Handoff

[../handoffs/0126-xbee-hub-spoke-host-plan-to-qa-communications.md](../handoffs/0126-xbee-hub-spoke-host-plan-to-qa-communications.md)
