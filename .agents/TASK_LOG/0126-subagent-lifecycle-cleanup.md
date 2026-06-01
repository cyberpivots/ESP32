# Task 0126 - Subagent Lifecycle Cleanup

## Triage

- Verified facts: completed PF0530N reviewer agents occupied all visible
  subagent slots until the parent collected their results and closed them with
  `close_agent`; a fresh read-only lifecycle-cleanup quorum then approved this
  Tier 2 boundary at 11/11 weight with no P1/P2 blocker.
- Assumptions: the correct fix is a parent-agent operational protocol plus
  repo-local advisory hooks/audits, not filesystem cleanup or system policy.
- Unknowns: future runtime lifecycle metadata and close-agent observability may
  differ; repo-local tests cannot guarantee runtime slot release.
- Selected tier: Tier 2 governance/hook/audit/test/records.
- Owner role: Agent Operations, with QA and Tooling review.
- Evidence need: current governance files, hook fixtures, scaffold audit,
  read-only reviewer outputs, source records, and validation commands.
- Mutation boundary: `AGENTS.md`, `.agents/GOVERNANCE.md`, `.agents/ROLES.md`,
  `.codex/hooks.json`, `.codex/hooks/*.py`, `.codex/admin/hooks/esp32_admin_policy.py`,
  prompt/coordination docs, prompt registry, scaffold audit/tests, source
  index/ledger, task/handoff/status records. No firmware behavior, live
  hardware, COM/serial, flash, monitor, RF/XBee, relay/load/mains,
  `/etc/codex`, commit, or push.
- Validation plan: focused hook/admin/decision tests, full scaffold audit
  discovery, agent-process scaffold audit, scaffold verification, and
  `git diff --check`.

## Reviewer Quorum

- Governance cartographer, weight 5: approved with conditions; required
  lifecycle cleanup language, hook/audit markers, and durable records.
- QA validation reviewer, weight 3: approved with conditions; required tests
  for lifecycle markers, explicit source records, and unknowns about runtime
  observability.
- Tooling resource reviewer, weight 3: approved with conditions; required
  wording that repo-local hooks cannot guarantee runtime slot release and
  must remain advisory under `bypassPermissions`.

Weighted result: 11/11 approve, no P1/P2 blockers, `ready_for_mutation` for the
named Tier 2 boundary only.

## Work Completed

- Made agent lifecycle cleanup mandatory around Tier 2 and Tier 3 reviewer
  quorum: inspect completed agents before spawning, use `wait_agent`, close
  completed/stale agents with `close_agent`, close agents before fallback/final,
  and record fallback only after cleanup attempt.
- Added repo-local `SubagentStop` advisory hook coverage.
- Updated managed hook advisory text and regression tests without adding any
  `/etc/codex` requirement or hard yolo block.
- Updated source index, source ledger, prompt registry, docs index, status
  ledger, triage status, and this task/handoff pair.

## Validation

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_agent_process_hooks tests.scaffold_audits.test_admin_policy_hooks tests.scaffold_audits.test_agent_process_decision`:
  PASS, 31 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`:
  PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`:
  PASS, 67 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`: PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`:
  PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`:
  PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_data.py`: PASS.
- `git diff --check`: PASS.

## Authority Limits

No live hardware, COM/serial, flash, monitor, RF/XBee, relay/load/mains,
firmware behavior change, `/etc/codex` mutation, admin-strict installation,
destructive git, GitHub publication, release, commit, or push is authorized or
performed by this task.
