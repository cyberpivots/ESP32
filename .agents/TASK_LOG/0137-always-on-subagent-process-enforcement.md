# Task 0137 - Always-On Subagent Process Enforcement

## Triage

- Verified facts: `AGENTS.md` and repo governance already required coordinator
  triage for every prompt and reviewer quorum for Tier 2/Tier 3 work; the user
  explicitly requested stronger always-on subagent calling for this continuation.
- Assumptions: the enforceable repo-local improvement is mandatory subagent
  attempt language plus advisory hooks/audits, not a machine-wide
  `/etc/codex/requirements.toml` denial policy.
- Unknowns: future Codex runtime tool availability and lifecycle visibility
  remain outside static repo control.
- Selected tier: Tier 2 governance, hook, audit, test, and record mutation.
- Owner role: Agent Operations with coordinator, QA, tooling, and
  evidence-record lenses.
- Evidence need: governance diffs, hook text, prompt docs, prompt registry,
  scaffold audit coverage, task/handoff/source records, and validation output.
- Mutation boundary: agent-process docs, hooks, prompt registry, scaffold audit
  tests, status records, source index/ledger, task log, and handoff only. No
  firmware runtime authority, live hardware, COM/serial, flash, monitor,
  RF/XBee, relay/load/mains, `/etc/codex`, admin-strict install, commit, or
  push.
- Validation plan: focused agent hook/admin tests, agent-process scaffold audit,
  full scaffold verification, and `git diff --check`.

## Reviewer Disposition

- Earlier read-only quorum for this continuation approved mandatory subagent
  attempt semantics as long as repo policy did not install system-wide denial
  rules or claim runtime guarantees.
- Weighted result for the named source-only boundary: 20/20 approve, no P1/P2
  blockers.

## Work Completed

- Strengthened the multi-agent process from default-authorized subagents to
  mandatory subagent attempt for safe non-trivial Tier 1 mutation and Tier 2/
  Tier 3 reviewer quorum when tools are available and safe.
- Preserved local role-lens fallback only when subagents are unavailable,
  unsafe, or blocked by higher-priority tool policy, and only after lifecycle
  cleanup is attempted or recorded as not visible.
- Kept `bypassPermissions` advisory-only behavior and did not create, install,
  or rely on `/etc/codex/requirements.toml`.
- Updated hook text, prompt docs, prompt registry/status records, scaffold
  audit expectations, this task log, handoff, source ledger, source index, and
  docs index.

## Validation

- PASS: focused hook/admin/process tests were included in the 60-test bundle.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_data.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: final `git diff --check`.

## Authority Limits

This task opens no live hardware, COM/serial, flash, monitor, RF/XBee,
relay/load/mains, firmware behavior, system-wide policy, admin-strict install,
destructive git, GitHub publication, release, commit, or push authority.
