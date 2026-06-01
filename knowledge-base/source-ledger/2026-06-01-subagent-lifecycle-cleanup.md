# Subagent Lifecycle Cleanup Source Ledger - 2026-06-01

## Scope

Tier 2 governance, hook, audit, test, and record update that makes agent
lifecycle cleanup explicit for Tier 2 and Tier 3 reviewer quorum. The change
responds to completed reviewer subagents occupying all available runtime slots
until the parent agent used `close_agent`.

## Source Basis

- `SRC-CODEX-HOOKS-2026-05-27`
- `SRC-CODEX-SUBAGENTS-2026-05-27`
- `SRC-CODEX-HOOKS-MANAGED-2026-05-28`
- `SRC-LOCAL-MULTI-AGENTIC-DEFAULT-PROCESS-2026-05-27`
- `SRC-LOCAL-MULTI-AGENTIC-CONTINUATION-DECISION-2026-05-27`
- `SRC-LOCAL-MULTI-AGENTIC-CONTINUOUS-ENFORCEMENT-2026-05-29`
- `SRC-LOCAL-MULTI-WINDOW-CODEX-SCHEDULER-2026-06-01`

## Verified Facts

- The active session exposed completed reviewer agent slots, and additional
  reviewer spawning initially failed with an agent-thread-limit error.
- The parent collected completed reviewer output with `wait_agent` and closed
  those completed agents with `close_agent` before spawning new reviewers.
- A fresh read-only Tier 2 reviewer quorum then ran for this lifecycle cleanup
  update:
  - Governance cartographer, weight 5: approve with conditions.
  - QA validation reviewer, weight 3: approve with conditions.
  - Tooling resource reviewer, weight 3: approve with conditions.
- Weighted disposition was 11/11 approval with no P1/P2 blocker for the named
  docs/hooks/audit/tests/records boundary.
- Repo-local hooks and audits can remind and test text fixtures, but only the
  parent agent's actual `close_agent` calls release visible Codex runtime slots.

## Assumptions

- Completed or stale reviewer slots should be cleaned up after their output is
  preserved.
- Local role-lens fallback is still valid when lifecycle state is unavailable
  or unsafe to act on, but the fallback record must say so.

## Unknowns

- Future Codex runtimes may expose different lifecycle metadata.
- Repo-local tests cannot prove all future runtime slot releases; they verify
  the workspace contract and hook/audit reminders.

## Outcome

- Added agent lifecycle cleanup language to the canonical contract, governance,
  roles, agent-coordination docs, prompt docs, and prompt registry.
- Added a project-local `SubagentStop` advisory hook and registered it in
  `.codex/hooks.json`.
- Updated project-local and managed hook text to require: inspect completed
  agents before spawning, use `wait_agent` for outstanding reviewers, close
  completed/stale agents with `close_agent`, close agents before fallback/final,
  and record fallback only after cleanup attempt.
- Added scaffold-audit and hook/admin test coverage for lifecycle markers and
  `bypassPermissions advisory only` behavior.

## Authority Limits

This task does not authorize live hardware, COM/serial access, flashing,
monitor, RF/XBee writes, relay/load/mains, `/etc/codex` mutation,
admin-strict installation, destructive git, GitHub publication, release,
commit, or push.

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
