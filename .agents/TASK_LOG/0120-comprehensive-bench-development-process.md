# Task 0120: Comprehensive Bench Development Process

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-31

## Goal

Implement the approved Tier 2 records-only process for comprehensive ESP32
bench development around the Windows 11 PC-attached COM6 lane, with a
`bench_state_packet.v1` artifact, index/linkage updates, PF0530L current-state
alignment, and scaffold audit coverage.

## Verified Facts

- The workspace contract requires Tier 2 read-only reviewer quorum before
  governance/process mutation.
- The current development-agent panel is advisory and read-only by default.
- PF0530L is the latest recorded COM6 LCD/menu UX live gate.
- PF0530L write-flash, separate verify-flash, read-only monitor, page/glyph
  auto-demo coverage, transcript scan, and cleanup proof are recorded.
- PF0530L captured zero `ENC_RAW`, zero `ENC_EV`, zero `BBS_MENU_STEP`, and
  zero `BBS_MENU_SELECT`, so physical encoder/button interaction remains
  unaccepted.
- XBee, RF, relay, load, mains, ESP-NOW/BBS/CBBS runtime, SoftAP/browser,
  serial-write, flash, persistent-config, credential, destructive-operation,
  external-service, release, and GitHub-publication surfaces remain separate
  gates.

## Assumptions

- The user's "comprehensive improvement" target means records/process routing
  across all active ESP32 bench lanes, not live hardware action in this task.
- COM6 is a claimed bench attachment until refreshed by a future same-session
  Tier 3 gate.
- Future live work should start with the smallest necessary evidence action
  after identity, recovery, no-load state, authority, and reviewer quorum are
  freshly present.

## Unknowns

- Current physical bench state, rail margin, LCD backpack pullup voltage,
  custom glyph readability, encoder/button physical interaction, relay module
  identity, live SoftAP/browser behavior, and CBBS live acceptance remain
  unproven.
- The current dirty worktree must still be stabilized before any release or
  GitHub publication gate.

## Reviewer Quorum

- Coordinator/Architecture-risk local lens, weight 5: approved records-only
  mutation, no live authority.
- Governance cartographer subagent, weight 2: conditional approve; requested a
  dedicated COM6 boundary packet and validation links.
- Evidence records subagent, weight 3: conditional approve; requested
  `bench_state_packet.v1`, PF0530L status alignment, and source/index updates.
- Local QA/live-bench gate lenses, weight 3: approved records-only boundary;
  blocked live bench activation.

Weighted approval: 13/13 conditional pass. No P1 blocker remains inside the
named records-only mutation boundary.

## Mutation Boundary

- `docs/prompt/comprehensive-bench-development-process.md`
- `knowledge-base/prompt-registry.md`
- `docs/index.md`
- `knowledge-base/source-index.md`
- `knowledge-base/source-ledger/2026-05-31-comprehensive-bench-development-process.md`
- this task record
- `scripts/scaffold_audit_agent_process.py`
- `tests/scaffold_audits/test_comprehensive_bench_process.py`
- `research/triage-status.md`
- `research/development-status-ledger.md`
- `research/known-gaps.md`

## Implementation

- Added a dedicated comprehensive bench-development process prompt.
- Defined the required `bench_state_packet.v1` fields and current default COM6
  packet values.
- Added a lane router for COM6 identity/recovery, LCD/encoder/menu, XBee,
  relay/power/load, ESP-NOW/BBS/CBBS, SoftAP/browser, and DevEx automation.
- Added source ledger, source-index, docs-index, and prompt-registry linkage.
- Added scaffold audit/test coverage for packet markers and closed Tier 3
  surfaces.
- Updated current research routing/gap records from PF0530H to PF0530L for
  the four-relay rotary encoder LCD menu lane.

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_comprehensive_bench_process`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- Closed-surface scan.
- `git diff --check`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_comprehensive_bench_process` (3 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `git diff --check`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (55 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: closed-surface scan returned only explicit stop-gate, denial, source
  ID, validation-command, or test-fixture references; no live authority was
  opened.

## Handoff

No handoff is required if validation passes. If a future agent opens live COM6
work, create a separate Tier 3 live-bench handoff with same-session identity,
recovery path, no-load safe state, explicit authority, reviewer quorum, and
closed-surface review.

## Closed Surfaces

Live hardware access, flashing, serial writes, serial monitor, RF transmit,
XBee setting writes, relay control, persistent settings writes, credential
access, destructive filesystem/device operations, external service changes,
GitHub publication, release gates, framework changes beyond accepted ADRs,
and any action where device identity or recovery path is not freshly proven
remain closed.
