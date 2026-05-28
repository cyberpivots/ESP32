# BBS UI System Operation Program Source Ledger - 2026-05-28

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-BBS-UI-SYSTEM-OPERATION-PROGRAM-2026-05-28`
- `SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-05-28`

## Purpose

Record the source basis for adding the BBS UI System Operation Improvement
Program to the singular ESP32 development plan and refreshing the current skill
inventory used to route the program.

## Verified Facts

- [repo-verified] `research/development-plan.md` remains the singular current
  action plan.
- [repo-verified] `research/development-status-ledger.md` remains the detailed
  evidence/status ledger.
- [repo-verified] The accepted live BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- [repo-verified] Gate M2-A DOS-C companion discovery support is host-only and
  does not extend the coordinator serial ABI.
- [repo-verified] ADR-0009 keeps `discovery_snapshot`,
  `discovery_events`, `service_catalog`, and `capability_report` separate from
  Gate F radio service codes and bounded to the existing 512-byte bridge line
  limit.
- [repo-verified] Current plugin skill paths use cache hash `be69e54e`; the
  previously checked-in `004da724` plugin paths are stale.
- [repo-verified] ESP32-local skills are present for live-gate coordination and
  Win31 dashboard vision-gate review.

## Assumptions

- This program is a Tier 2 planning/status/source-record update.
- UI-0 and M2-B should run before any Gate M3 mapping review or Client-1/2
  proof because they are the lowest-risk source-backed slices.
- Later panel voting can choose defaults inside an accepted mutation boundary,
  but factual claims still need source-index support or unresolved-gap notes.

## Unknowns

- No same-session live bench identity, no-load state, Wi-Fi state, process
  cleanup proof, browser-device proof, or screenshot/OCR/CV evidence was
  captured by this task.
- No UI-0 ranked improvement packet, M2-B host-only Network/Services UX proof,
  M3 firmware mapping design review, Client-1 static/simulated browser proof,
  Client-2 selected-board read-only Wi-Fi proof, or dummy-output proof is
  accepted yet.

## Reviewer Quorum

Read-only reviewer quorum was run before mutation. The repository stores this
summary, not raw subagent transcripts.

- Governance cartographer: approved the Tier 2 documentation/status/source
  boundary if the task log, handoff, source ledger, source index, and docs index
  were kept current.
- Evidence-record auditor: approved conditionally if a program-level source ID,
  source ledger, known-gap entry, and closed-surface boundaries were added.
- UI/protocol analyst: approved the host-only UI/protocol boundary and called
  out the need to keep discovery summaries separate from coordinator serial
  commands and Gate F radio service codes.
- Source/skill curator: approved refreshing `research/skills/available-skills.md`
  with `be69e54e` plugin paths and ESP32-local skills, without creating a
  broad new skill.
- QA validation reviewer: approved the mutation boundary with scaffold checks,
  agent-process audit, scaffold audit unit tests, source-ID scan, Markdown link
  check, custom wireless protocol tests, and `git diff --check`.

## Program Scope

- UI-0: review Win31/CBBS UI and current legibility/interface backlog for
  non-technical operator clarity.
- M2-B: strengthen host-only Network/Services discovery UX while proving
  512-byte bounds, read-only behavior, no coordinator serial ABI expansion, and
  no Gate F radio service-code changes.
- M3: plan firmware mapping review from ESP-WIFI-MESH events/APIs to
  `mesh_discovery.v1` as design and fixtures only.
- Client-1: plan static/simulated or read-only browser/client-node proof.
- Client-2: defer selected-board read-only Wi-Fi proof to a separate future
  Tier 3 gate; dummy-output control remains later.

## Local Records

- Plan: `research/development-plan.md`
- Status ledger: `research/development-status-ledger.md`
- Known gaps: `research/known-gaps.md`
- Triage status: `research/triage-status.md`
- Skill inventory: `research/skills/available-skills.md`
- Task log: `.agents/TASK_LOG/0080-bbs-ui-system-operation-program.md`
- QA handoff: `.agents/handoffs/0069-bbs-ui-system-operation-program-to-qa.md`

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

## Stop Gates

This program does not authorize runtime public API changes, firmware ABI
changes, bridge ABI changes, coordinator serial ABI changes, Gate F service-code
changes, `mesh_discovery.v1` schema changes, Win31 transport changes, live
browser proof, firmware runtime migration, prepare/flash/complete, erase,
monitor, serial-write expansion, BLE pairing, live ESP-WIFI-MESH, Android app
behavior, PCAP, router/admin mutation, relay, XBee writes, TFT, MicroSD, load,
mains, or cleanup acceptance.
