# Development Plan Consolidation Source Ledger - 2026-05-27

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-DEVELOPMENT-PLAN-CONSOLIDATION-2026-05-27`
- `SRC-LOCAL-ESPNOW-BBS-COMPANION-SOFTAP-LIVE-GATE-TOOLING-2026-05-27`

## Purpose

Record the source basis for consolidating active ESP32 planning into one tracked
development plan and indexing the previously unindexed companion SoftAP Gate 1
tooling status.

## Verified Facts

- [repo-verified] `research/development-status-ledger.md` remains the detailed
  current-status ledger.
- [repo-verified] `research/development-plan.md` was added as the singular
  current-action plan derived from the status ledger, ADRs, source index,
  known gaps, task logs, and handoffs.
- [repo-verified] Companion SoftAP Gate 1 tooling has task and handoff records
  at `.agents/TASK_LOG/0076-espnow-bbs-companion-softap-live-gate-tooling.md`
  and `.agents/handoffs/0065-espnow-bbs-companion-softap-live-gate-tooling-to-qa.md`.
- [repo-verified] Companion SoftAP Gate 1 is tooling-only and host-validated.
  It does not prove live SoftAP, Windows Wi-Fi mutation, physical dummy output,
  bridge proof, vision proof, completion proof, cleanup acceptance, flash,
  erase, monitor, relay, XBee, TFT, MicroSD, load, mains, or serial-write
  expansion.
- [repo-verified] The stale Win31 interface-improvement source ID was corrected
  to the indexed `SRC-LOCAL-WIN31-DASHBOARD-INTERFACE-IMPROVEMENT-2026-05-27`.
- [repo-verified] Known-gap and four-relay wording was normalized so completed
  simulator/protocol and disabled-skeleton work are not treated as open
  first-selection or all-firmware-deferred blockers.

## Assumptions

- Historical task logs and handoffs remain immutable evidence records.
- This consolidation is a routing/status pass, not a live proof, framework
  decision, hardware action, or firmware runtime migration.

## Unknowns

- No same-session live bench identity, SoftAP proof, Windows Wi-Fi proof,
  bridge transcript, vision gate, companion proof, physical output proof, or
  cleanup proof was captured by this task.
- No current evidence opens BLE, live ESP-WIFI-MESH, PCAP, relay, XBee, TFT,
  MicroSD, load, mains, erase, monitor, router/admin mutation, or serial-write
  expansion.

## Local Records

- Plan: `research/development-plan.md`
- Status ledger: `research/development-status-ledger.md`
- Task log: `.agents/TASK_LOG/0078-development-plan-consolidation.md`
- QA handoff: `.agents/handoffs/0067-development-plan-consolidation-to-qa.md`
- Companion SoftAP tooling task:
  `.agents/TASK_LOG/0076-espnow-bbs-companion-softap-live-gate-tooling.md`
- Companion SoftAP tooling handoff:
  `.agents/handoffs/0065-espnow-bbs-companion-softap-live-gate-tooling-to-qa.md`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- PASS: source-ID scan over changed Markdown files.
- PASS: Markdown link check over changed Markdown files.
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: closed-surface `rg` review over changed files; hits were blocked,
  unknown, or stop-gate references, not new authority.
- PASS: `git diff --check`

## Stop Gates

This consolidation does not authorize firmware framework selection, firmware
runtime migration, live hardware, live SoftAP proof, Windows Wi-Fi mutation,
physical output proof, flashing, wiring, radio changes, serial-write expansion,
relay/load/mains work, BLE, live ESP-WIFI-MESH, PCAP, router/admin mutation,
XBee writes, TFT, MicroSD, active runtime hook trust claims, or cleanup
acceptance.
