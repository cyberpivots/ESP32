# Task 0080: BBS UI System Operation Program

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-28

## Goal

Add a BBS UI System Operation Improvement Program to the singular tracked
development plan, refresh the current skill inventory, and preserve the
accepted ESP-NOW BBS serial-nullmodem baseline.

## Verified Facts

- `research/development-plan.md` is the singular current-action plan.
- `research/development-status-ledger.md` is the detailed evidence/status
  ledger.
- The accepted BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- Current GitHub and Canva plugin skills are installed under cache hash
  `be69e54e`, not the previously checked-in `004da724`.
- ESP32-local `esp32-live-gate-coordinator` and `win31-dashboard-vision-gate`
  skills exist under `.codex/skills/`.

## Assumptions

- This task authorizes documentation/status/source-record edits only.
- The program should route future UI and client work through named gates rather
  than creating a second roadmap.

## Unknowns

- No same-session live bench identity, no-load state, Windows Wi-Fi state,
  process cleanup proof, browser-device proof, or copied screenshot/OCR/CV
  evidence was captured by this task.
- No UI-0, M2-B, M3, Client-1, Client-2, or dummy-output proof is accepted yet.

## Reviewer Quorum

Project-local read-only reviewer subagents were used before mutation. The
repository stores the quorum summary, not raw subagent transcripts.

- Governance cartographer: approved the documentation/status/source-record
  boundary with task, handoff, source ledger, source index, and docs index.
- Evidence-record auditor: approved conditionally with a program-level source
  record, known-gap update, and closed-surface wording.
- UI/protocol analyst: approved host-only UI/protocol planning while preserving
  512-byte bridge bounds, no coordinator serial ABI expansion, and no Gate F
  service-code changes.
- Source/skill curator: approved skill inventory refresh to `be69e54e` plugin
  paths plus ESP32-local skills.
- QA validation reviewer: approved validation with scaffold checks,
  agent-process audit, scaffold audit unit tests, custom wireless protocol
  tests, changed-file source-ID scan, changed-file Markdown link check, and
  `git diff --check`.

## Mutation Boundary

- `research/development-plan.md`
- `research/development-status-ledger.md`
- `research/known-gaps.md`
- `research/triage-status.md`
- `research/skills/available-skills.md`
- `docs/index.md`
- `knowledge-base/source-index.md`
- `knowledge-base/source-ledger/2026-05-28-bbs-ui-system-operation-program.md`
- this task record
- `.agents/handoffs/0069-bbs-ui-system-operation-program-to-qa.md`

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- Changed-file source-ID scan.
- Changed-file Markdown link check.
- `git diff --check`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (9 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py` (32 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py` (10 tests)
- PASS: changed-file source-ID scan over 10 Markdown files.
- PASS: changed-file Markdown link check over 10 Markdown files.
- PASS: `git diff --check`

## Handoff

Continue with
[../handoffs/0069-bbs-ui-system-operation-program-to-qa.md](../handoffs/0069-bbs-ui-system-operation-program-to-qa.md).

## Closed Surfaces

Runtime public API changes, firmware ABI changes, bridge ABI changes,
coordinator serial ABI changes, Gate F service-code changes,
`mesh_discovery.v1` schema changes, Win31 transport changes, live browser
proof, firmware runtime migration, live hardware, prepare/flash/complete,
erase, monitor, physical serial writes, serial-write expansion, radio setting
changes, router/admin mutation, BLE, live mesh, PCAP, relay/XBee writes, TFT,
MicroSD, load, mains, release gating, and cleanup acceptance remain closed.
