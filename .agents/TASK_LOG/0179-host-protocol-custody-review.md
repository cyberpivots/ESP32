# Task 0179: Host Protocol Custody Review

Status: completed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-05

Source IDs:
`SRC-LOCAL-HOST-PROTOCOL-CUSTODY-REVIEW-2026-06-05`,
`SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`,
`SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`,
`SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-GOLDEN-VECTORS-2026-05-26`,
`SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-RUNTIME-REQUIREMENTS-2026-05-26`,
`SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-PHASE-5-6-RUNTIME-DESIGN-REVIEW-2026-05-26`,
`SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`,
`SRC-LOCAL-XBEE-HUB-SPOKE-HOST-PLAN-2026-06-05`,
`SRC-LOCAL-AGENTIC-PLANNING-GUIDE-2026-06-05`

## Routing

- Verified facts: the 2026-06-05 committed baseline was clean and aligned with
  `origin/main` before this continuation. The agentic planning guide lists
  host protocol/custody review as the first approved next sequence item.
  Existing custom wireless tests pinned byte-level Gate F packet golden
  vectors, while the simulator runtime applied custody ACKs by reading JSON
  body fields. No checked-in Task 0179, source ledger, or handoff existed
  before this slice.
- Assumptions: the safe continuation is a host-only semantic-contract
  clarification for the simulator and records. Low-level packet golden vectors
  remain codec fixtures and are not rewritten by this slice. No post-slice
  commit or push is authorized by this task record.
- Unknowns: firmware runtime behavior, firmware memory budgets, persistence,
  live ESP-NOW delivery, live bridge dispatch, serial/RF/XBee behavior, XBee
  custody-backhaul runtime behavior, and live cleanup proof remain unverified.
- Selected tier: Tier 2 protocol/tests/docs/records.
- Owner role: Communications with QA, Agent Operations, and Evidence Records.
- Evidence need: custom wireless simulator/tests, accepted Gate F ADR/source
  records, XBee host-only plan records, docs index, source index, reviewer
  quorum output, and focused host-only validation.
- Mutation boundary: `tools/simulators/custom_wireless_protocol/espnow_bbs_custom_protocol.py`,
  `tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`,
  `tools/simulators/custom_wireless_protocol/README.md`,
  `comm-protocols/custom/README.md`, `knowledge-base/source-index.md`,
  `knowledge-base/source-ledger/2026-06-05-host-protocol-custody-review.md`,
  `docs/index.md`, `research/development-status-ledger.md`,
  `research/known-gaps.md`, this task record, and
  `.agents/handoffs/0127-host-protocol-custody-review-to-qa-communications.md`.
- Reviewer quorum: project-local read-only subagents were spawned for
  development-panel coordination, protocol/bridge ABI review, evidence-record
  audit, and QA validation. All completed reviewers were waited and closed
  after output capture. Weighted disposition: 14/14 approval with conditions,
  threshold 70 percent. No P1 blockers remained. The P2 conditions were to add
  durable Task 0179/source-ledger/handoff coverage, correct the nonexistent
  `docs/source` path assumption, keep proof host-only, and pin custody ACK
  semantic behavior.
- Gate authority: host-only tests, simulator semantics, docs, source index,
  task, source ledger, and handoff records. No Tier 3 authority is opened.
- Validation plan: run `pnpm test -- packages/cbbs-protocol/__tests__/contract.test.ts`,
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.custom_wireless_protocol.test_espnow_bbs_custom_protocol`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 179`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`, and
  `git diff --check`.
- Trust boundary: local repo source records, accepted ADRs, host-only tests,
  and captured reviewer votes. Hooks remain advisory under
  `bypassPermissions`; scheduler lifecycle advisories do not block operator
  intent.

## Implementation

- Updated the host-only simulator ACK application path so semantic
  `custody_ack` packets must carry ASCII JSON whose `ack` field matches the
  packet `message_id` and whose body `status` matches the packet custody
  status.
- Added tests proving the JSON ACK body survives encode/decode and updates the
  intended custody record, plus negative tests for malformed plain-text ACK
  bodies, mismatched ACK targets, and mismatched ACK statuses.
- Documented that byte-level golden vectors remain codec fixtures and do not
  prove runtime ACK acceptance by themselves.
- Added durable source-index, source-ledger, docs-index, status-ledger,
  known-gap, task, and handoff coverage for this host protocol/custody review.

## Validation

Passed on 2026-06-05:

- `pnpm test -- packages/cbbs-protocol/__tests__/contract.test.ts`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.custom_wireless_protocol.test_espnow_bbs_custom_protocol`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 179`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- `git diff --check`.

## Authority Limits

Still closed: live bench, prepare/flash/complete, erase, monitor, serial
writes, RF/XBee writes, XBee profile writes, API transmit to hardware,
HostCommandBridge live dispatch, native adapter execution, shell execution,
firmware runtime migration, firmware persistence, BLE, Web Bluetooth, Web
Serial, live mesh, PCAP, router/admin mutation, Windows Wi-Fi mutation,
relay/load/mains, wiring-under-power, signing, Store/App Installer
distribution, EAS, App Center, release, publication, commit, push, PR, deploy,
`/etc/codex/requirements.toml`, and `admin-strict` installation.

## Handoff

[../handoffs/0127-host-protocol-custody-review-to-qa-communications.md](../handoffs/0127-host-protocol-custody-review-to-qa-communications.md)

## Decision

Decision: accept the bounded Tier 2 host protocol/custody semantic review. The
simulator now distinguishes semantic JSON custody ACK application from
low-level byte codec fixtures. Firmware runtime, persistence, live bridge
dispatch, ESP-NOW delivery, and XBee live/backhaul behavior remain closed for
future gates.
