# Task 0078: Development Plan Consolidation

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-27

## Goal

Consolidate active ESP32 planning into one tracked development plan while
preserving historical task logs, handoffs, ADRs, source ledgers, and bench
records as evidence.

## Verified Facts

- `research/development-status-ledger.md` is the canonical detailed status
  ledger.
- `research/development-plan.md` is the singular current-action plan added by
  this task.
- Companion SoftAP Gate 1 tooling was already implemented and host-validated in
  task 0076, but it was missing current status/source-index coverage before
  this consolidation.
- The stale Win31 dashboard interface source ID had one mismatched `DOSC`
  prefix in the backlog.
- No same-session live hardware, SoftAP, Windows Wi-Fi, physical output,
  bridge, vision, completion, or cleanup proof was captured by this task.

## Assumptions

- Historical records remain immutable; current truth is expressed in the plan,
  status ledger, source index, source ledger, task log, and handoff.
- This is a Tier 2 documentation/status/source-record pass.

## Unknowns

- No current live proof opens firmware runtime migration, BLE, live mesh, PCAP,
  relay, XBee, TFT, MicroSD, load, mains, erase, monitor, router/admin
  mutation, Windows Wi-Fi mutation, or serial-write expansion.
- No durable subagent transcript artifact is stored in this repository for the
  reviewer quorum summary below.

## Reviewer Quorum

Project-local read-only reviewer subagents were used before mutation, and the
checkpoint execution reran a read-only quorum before staging this consolidation.
The repository stores the quorum summary, not raw subagent transcripts.

- Governance cartographer: approved the Tier 2 documentation/status mutation
  boundary and next IDs.
- Evidence-record auditor: approved conditionally if 0076, stale source IDs,
  known-gap wording, and four-relay stale wording were corrected.
- QA validation reviewer: approved conditionally with mandatory source-ID,
  Markdown-link, public-site, closed-surface, scaffold, and diff checks.

## Mutation Boundary

- `research/development-plan.md`
- `research/development-status-ledger.md`
- `research/triage-status.md`
- `research/known-gaps.md`
- `docs/index.md`
- `docs/projects/espnow-bbs/win31-dashboard-interface-improvement-backlog.md`
- `docs/projects/four-relay-xbee-wifi/power-and-safety.md`
- `docs/projects/four-relay-xbee-wifi/prototype-blueprint.md`
- `knowledge-base/source-index.md`
- `knowledge-base/source-ledger/2026-05-27-development-plan-consolidation.md`
- this task record
- `.agents/handoffs/0067-development-plan-consolidation-to-qa.md`

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- Source-ID scan over changed Markdown files.
- Markdown link check over changed Markdown files.
- `python3 scripts/build_github_pages.py`
- `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- `python3 scripts/smoke_github_pages.py build/github-pages`
- Targeted closed-surface `rg` review over changed files.
- `git diff --check`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (9 tests)
- PASS: source-ID scan over changed Markdown files.
- PASS: Markdown link check over changed Markdown files.
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: targeted closed-surface `rg` review over changed files; hits were stop
  gates, unknowns, blocked status, or historical context, not new authority.
- PASS: `git diff --check`

## Handoff

Continue with
[../handoffs/0067-development-plan-consolidation-to-qa.md](../handoffs/0067-development-plan-consolidation-to-qa.md).

## Closed Surfaces

Firmware framework selection, firmware runtime implementation, live hardware,
live SoftAP proof, Windows Wi-Fi mutation, physical output proof, flashing,
erase, monitor, physical serial writes, serial-write expansion, radio setting
changes, router/admin mutation, BLE, live mesh, PCAP, relay/XBee writes, TFT,
MicroSD, load, mains, release gating, active runtime hook trust claims, hard
`PreToolUse` enforcement claims, and cleanup acceptance remain closed.
