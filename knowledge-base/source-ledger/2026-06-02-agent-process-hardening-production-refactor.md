# Agent-Process Hardening Production Refactor Ledger

Source ID:
`SRC-LOCAL-AGENT-PROCESS-HARDENING-PRODUCTION-REFACTOR-2026-06-02`

Date: 2026-06-02

## Scope

This ledger records the Tier 2 repo-local production refactor for ESP32
agent-process hardening, managed-hook portability, classifier maintainability,
tests, audits, docs, and durable records.

## Verified Facts

- Required governance files were reread before mutation.
- Read-only reviewer quorum was attempted and captured before mutation.
- Reviewer lifecycle cleanup was performed after output capture.
- Reviewers identified the installed managed-hook import path as the P1
  production risk: the hook needed support modules copied next to it and
  temp-target install validation.
- The mutation stayed repo-local and did not install, remove, inspect, or modify
  `/etc/codex`.
- `scripts/agent_process_contracts.py` centralizes compact contract IDs and
  routing/subagent/bypass/lifecycle text for project and managed hooks.
- `scripts/agent_process_classifiers.py` now exposes structured classification
  results and preserves compatibility wrappers.
- `.codex/admin/install_admin_policy.py` supports `--target-dir PATH`, defaults
  to `/etc/codex`, and installs requirements, managed hook, classifier support,
  and contract support files together.
- Temp install tests and scaffold audit smoke execute the copied managed hook
  with sanitized `PYTHONPATH` from outside the repo.
- Current-session user direction explicitly records persistent standing
  authorization for project-local read-only subagent use in this workspace.
- The managed admin hook forces its installed hook directory to the front of
  `sys.path`, so sibling support modules outrank an ambient fallback `scripts/`
  directory.
- Scaffold audit admin dry-runs use temp `--target-dir` paths rather than the
  installer default `/etc/codex` target.
- Temp target removal reports `removed target requirements` so temp validation
  evidence is not described as system mutation.

## Files

- `scripts/agent_process_contracts.py`
- `scripts/agent_process_classifiers.py`
- `.codex/hooks/user_prompt_submit_agent_process.py`
- `.codex/hooks/subagent_start_agent_process.py`
- `.codex/hooks/subagent_stop_agent_process.py`
- `.codex/hooks/pre_tool_use_agent_process.py`
- `.codex/admin/hooks/esp32_admin_policy.py`
- `.codex/admin/install_admin_policy.py`
- `.codex/admin/README.md`
- `tests/scaffold_audits/test_agent_process_classifiers.py`
- `tests/scaffold_audits/test_admin_policy_hooks.py`
- `scripts/scaffold_audit_agent_process.py`
- `scripts/scaffold_audit_data.py`
- `AGENTS.md`
- `.agents/GOVERNANCE.md`
- `.agents/ROLES.md`
- `docs/agent-coordination.md`
- `docs/instruction-surface-map.md`
- `docs/index.md`
- `knowledge-base/source-index.md`
- `.agents/TASK_LOG/0145-agent-process-hardening-production-refactor.md`
- `.agents/handoffs/0106-agent-process-hardening-production-refactor-to-qa-tooling.md`

## Validation

Validation is recorded in Task 0145. Required checks include focused
hook/admin/classifier tests, full scaffold-audit unittest discovery, temp
install smoke, admin dry-runs for yolo-compatible and admin-strict profiles,
agent-process audit, skill audit, durable-record audit, publication hygiene
JSON report, scheduler self-test, scaffold verification, `git diff --check`,
and final git status.

The QA hardening validation also covers stale fallback support-module collision,
installed-copy `PreToolUse` denial, installed-copy `bypassPermissions` no-op,
temp-target admin dry-runs, no-space `/etc/codex` redirection classification,
and target-specific temp removal wording.

## Assumptions And Unknowns

- Runtime managed-hook trust cannot be proven from static repo files.
- Future subagent availability and lifecycle state visibility remain
  same-session runtime conditions.
- Standing user authorization is recorded in repo-local instruction surfaces,
  but runtime availability of subagent tools is still a same-session condition.
- Actual system `/etc/codex` state remains intentionally unverified because no
  system mutation or inspection authority was granted.

## Closed Surfaces

This record does not authorize `/etc/codex` mutation, admin-strict
installation, live hardware, COM/serial access, flashing, monitor, serial
writes, RF/XBee writes, relay/load/mains work, wiring mutation, firmware
behavior changes, destructive git, GitHub publication, release, commit, push,
PR creation, Pages deployment, or external service mutation.
