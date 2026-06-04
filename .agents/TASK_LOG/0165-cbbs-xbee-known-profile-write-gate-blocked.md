# Task 0165: CBBS XBee Known-Profile Write Gate Blocked

Status: completed - blocked at live gate

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-04

Source IDs:
`SRC-LOCAL-CBBS-XBEE-KNOWN-PROFILE-WRITE-GATE-BLOCKED-2026-06-04`

## Routing

- Verified facts: prior Task 0091 accepted selected-port programming for
  `COM15` and `COM6` only, and prior later tasks corrected `COM6` as the ESP32
  bridge target and `COM15` as the peer XBee.
- Assumptions: the intended future known-profile write set is `AP=2`, `AO=0`,
  `EE=1`, `BD=3`, optional redacted `KY`, then `WR`.
- Unknowns: current port identity, current radio readback, adapter markings,
  antenna/isolation state, carrier voltage, DIN/DOUT routing, key handling,
  rollback packet, and current redacted manifest.
- Selected tier: Tier 3 serial/RF/XBee write gate review.
- Owner role: XBee/radio protocol with live-bench, hardware safety, QA, and KB
  lenses.
- Evidence need: same-session exact port identity, redacted readback backup,
  target diff, voltage/isolation/antenna evidence, local-only key handling,
  rollback plan, redacted transcript, manifest hashes, no-secret scan, and
  cleanup proof.
- Mutation boundary: durable blocked-gate records only.
- Reviewer quorum: XBee/radio and live-bench reviewers returned P1 blockers for
  any live write; coordinator and QA kept serial/RF writes closed.
- Gate authority: no serial open, setting write, `WR`, `KY`, API transmit, RF
  probe, firmware recovery, or relay/load/mains action is authorized.
- Validation plan: keep XBee CLI self-tests/offline write-plan checks passing;
  future live work must start with read-only inventory/readback.
- Trust boundary: offline planning only; no live serial/RF action.

## Blockers

- P1: no same-session physical confirmation, port identity, current readback
  backup, or rollback packet exists.
- P1: no current voltage/isolation/antenna/carrier/DIN/DOUT evidence exists.
- P1: key material is intentionally absent from repo records; any `KY` write
  needs a local-only handling plan and cannot be rolled back from public logs.

## Authority Limits

No serial write, `WR`, `AC`, `KY`, `AP/AO/EE/BD` setting write, API transmit,
RF range/throughput test, firmware update/recovery, ESP32 DIN/DOUT acceptance,
relay/load/mains work, signing, release, deploy, commit, push, or PR is
authorized by this task.

## Validation

Validation is record-only for this blocked gate. Existing XBee offline tests
must continue to pass under Task 0163 validation.

## Decision

Decision: the known-profile XBee write gate is blocked until a fresh same-session
Tier 3 packet supplies physical evidence, readback backup, rollback, redaction,
and reviewer approval.

## Handoff

Handoff:
[../handoffs/0124-cbbs-xbee-known-profile-write-gate-blocked-to-qa.md](../handoffs/0124-cbbs-xbee-known-profile-write-gate-blocked-to-qa.md)
