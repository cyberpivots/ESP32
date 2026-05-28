# Task 0083: BBS UI UI-0/M2-B Host-Only Slice

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-28

## Goal

Start the separate BBS UI host-only slice by producing UI-0 ranked
operator-facing improvements, recording M2-B Network/Services UX proof, and
linking the paired DOS-C host-only implementation.

## Verified Facts

- `research/development-plan.md` identifies UI-0 and M2-B as the next safe
  host-only BBS UI slices.
- DOS-C commit `7f0b5df` adds host-only/read-only Network/Services wording and
  source tests for the paired operator surface.
- The accepted BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Assumptions

- This task authorizes documentation/status/source-record updates only in
  ESP32, plus references to the already-pushed DOS-C host-only proof.
- Fresh copied screenshots or browser proof are not required for the UI-0/M2-B
  host-only source packet.

## Unknowns

- No M3 firmware mapping review, Client-1 browser proof, Client-2 selected
  board proof, dummy-output proof, release proof, or cleanup proof is accepted.
- No live mesh, BLE, PCAP, router/admin, flash, serial-write, relay/XBee, TFT,
  MicroSD, load, or mains evidence is captured by this task.

## Reviewer Quorum

Project-local read-only reviewer subagents were used before mutation. The
repository stores the quorum summary, not raw subagent transcripts.

- Governance cartographer: no P1/P2 blockers for UI-0/M2-B if the slice stays
  host-only and gets new task/source/handoff records.
- UI/protocol analyst: no P1/P2 blockers; require schema distinction and DOS-C
  host tests before claiming M2-B proof.
- QA validation reviewer: P2 until Pages validation and paired DOS-C evidence
  are included. The validation plan includes both.

## Mutation Boundary

- `docs/projects/espnow-bbs/bbs-ui-ui0-m2b-host-slice.md`
- `research/development-plan.md`
- `research/development-status-ledger.md`
- `research/known-gaps.md`
- `research/triage-status.md`
- `docs/index.md`
- `knowledge-base/source-index.md`
- `knowledge-base/source-ledger/2026-05-28-bbs-ui-ui0-m2b-host-slice.md`
- this task record
- `.agents/handoffs/0072-bbs-ui-ui0-m2b-host-slice-to-qa.md`

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_github_pages.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_public_manifest.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_github_pages.py`
- Changed-file source-ID scan.
- Changed-file Markdown link check.
- Closed-surface scan.
- `git diff --check`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (9 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py` (32 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py` (10 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_github_pages.py` (64 public files)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_public_manifest.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_github_pages.py`
- PASS: changed-file source-ID scan over 10 Markdown files.
- PASS: changed-file Markdown link check over 10 Markdown files.
- PASS: closed-surface scan reviewed expected hits in verified-fact,
  unknown, remaining-gap, QA-focus, or stop-gate context.
- PASS: `git diff --check`

## Handoff

Continue with
[../handoffs/0072-bbs-ui-ui0-m2b-host-slice-to-qa.md](../handoffs/0072-bbs-ui-ui0-m2b-host-slice-to-qa.md).

## Closed Surfaces

Runtime public API changes, firmware ABI changes, bridge ABI changes,
coordinator serial ABI changes, Gate F service-code changes,
`mesh_discovery.v1` schema changes, Win31 transport changes, live browser
proof, firmware runtime migration, live hardware, prepare/flash/complete,
erase, monitor, physical serial writes, serial-write expansion, radio setting
changes, router/admin mutation, BLE, live mesh, PCAP, relay/XBee writes, TFT,
MicroSD, load, mains, release gating, dummy-output control, and cleanup
acceptance remain closed.
