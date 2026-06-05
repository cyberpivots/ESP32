# Source Ledger - 2026-06-05 Host Protocol Custody Review

## Scope

Tier 2 host-only protocol/test/docs/records update for the custom wireless
custody ACK semantic contract. This ledger records a simulator and records
clarification only; it does not accept firmware runtime behavior, live
delivery, bridge dispatch, XBee live behavior, or persistence.

## Source IDs

- `SRC-LOCAL-HOST-PROTOCOL-CUSTODY-REVIEW-2026-06-05`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-GOLDEN-VECTORS-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-RUNTIME-REQUIREMENTS-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-PHASE-5-6-RUNTIME-DESIGN-REVIEW-2026-05-26`
- `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`
- `SRC-LOCAL-XBEE-HUB-SPOKE-HOST-PLAN-2026-06-05`
- `SRC-LOCAL-AGENTIC-PLANNING-GUIDE-2026-06-05`

## Verified Facts

- `docs/agentic-planning-guide.md` lists host protocol/custody review as the
  first approved continuation item.
- Existing Gate F records accept byte-level packet budgets, service codes,
  custody codes, and host-only packet golden vectors as design/test fixtures.
- The host-only simulator runtime applies custody ACKs through
  `ProtocolSimulator.apply_ack`, which reads JSON body fields through
  `decode_packet_body`.
- This slice requires a semantic custody ACK body to be ASCII JSON, requires
  body `ack` to match the packet `message_id`, and requires body `status` to
  match the packet custody status before updating a custody record.
- The plain `b"ack"` custody ACK golden vector remains a low-level packet
  codec fixture and is not a valid runtime ACK application proof by itself.
- XBee hub-spoke custody/backhaul work remains synthetic host-only planning
  and does not prove live radio behavior.

## Assumptions

- Matching packet header and JSON body fields is the least ambiguous host-only
  ACK policy for the simulator.
- Runtime ACK semantics can be clarified without changing the accepted Gate F
  byte layout or service-code assignments.
- Future firmware implementation should cite this record if it adopts the same
  semantic ACK checks, but this task does not require firmware code.

## Unknowns

- Whether future firmware runtime will encode and apply custody ACKs with the
  same semantic checks.
- Firmware memory budgets, persistence, retry storage, and recovery behavior.
- Live ESP-NOW delivery, live Pi bridge dispatch behavior, live XBee custody
  backhaul behavior, and cleanup proof.

## Reviewer Quorum

Read-only project-local reviewers were spawned, waited, and closed after output
capture.

| Role | Weight | Vote | Disposition |
| --- | ---: | --- | --- |
| Development panel coordinator | 5 | approve with conditions | Continue with host-only records/tests; no P1/P2 after conditions. |
| Protocol bridge ABI reviewer | 3 | approve with conditions | Pinned the ACK semantic coverage gap and required no ABI/live expansion. |
| Evidence record auditor | 3 | approve with conditions | Required Task 0179, source ledger, and handoff/crosswalk records. |
| QA validation reviewer | 3 | approve with conditions | Required focused validation and closed-surface wording. |

Weighted disposition: 14/14 approved for the named Tier 2 mutation boundary.
Threshold: 70 percent. No P1 blockers remained. The P2 conditions are addressed
by semantic ACK tests/docs and this durable record set.

## Validation

Passed on 2026-06-05:

- `pnpm test -- packages/cbbs-protocol/__tests__/contract.test.ts`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.custom_wireless_protocol.test_espnow_bbs_custom_protocol`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 179`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`

## Decision

Decision: accept the host-only simulator semantic clarification. Semantic
custody ACK application now has a JSON body/header consistency contract in the
simulator. This record does not authorize firmware runtime migration, live
ESP-NOW proof, live bridge dispatch, serial/RF/XBee writes, XBee profile
writes, relay/load/mains, release, publication, commit, push, PR, or deploy.
