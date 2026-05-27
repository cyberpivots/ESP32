# Handoff 0067: Development Plan Consolidation To QA

Date: 2026-05-27

Task:
[../TASK_LOG/0078-development-plan-consolidation.md](../TASK_LOG/0078-development-plan-consolidation.md)

## Current State

- `research/development-plan.md` is the singular current-action plan.
- `research/development-status-ledger.md` remains the detailed status and
  evidence ledger.
- Companion SoftAP Gate 1 tooling is indexed as host/tooling-only status.
- Historical task logs, handoffs, ADRs, source ledgers, and bench records remain
  evidence records, not rewritten current truth.

## QA Focus

1. Confirm the plan and status ledger stay mutually consistent after future
   lane changes.
2. Confirm source IDs in changed files exist in `knowledge-base/source-index.md`
   or are explicitly marked unresolved.
3. Confirm Markdown links in changed records resolve.
4. Confirm public docs builds do not publish private paths, raw live evidence,
   `.agents/` records, vendor PDFs, or unsupported hardware claims.
5. Confirm closed-surface references do not become authority for live hardware,
   firmware runtime, SoftAP, Wi-Fi, BLE, mesh, relay, XBee, TFT, MicroSD, load,
   mains, router/admin, serial-write, erase, monitor, or cleanup actions.

## Validation Recorded

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- PASS: source-ID scan over changed Markdown files.
- PASS: Markdown link check over changed Markdown files.
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: closed-surface `rg` review over changed files.
- PASS: `git diff --check`

## Stop Gates

Do not use this consolidation to authorize live SoftAP proof, Windows Wi-Fi
mutation, physical output proof, firmware runtime migration, firmware
persistence, live hardware, flash, erase, monitor, serial-write expansion,
radio changes, router/admin mutation, BLE, live ESP-WIFI-MESH, PCAP, relay,
XBee writes, TFT, MicroSD, load, mains, release gating, active runtime hook
trust claims, hard `PreToolUse` enforcement claims, or cleanup acceptance.
