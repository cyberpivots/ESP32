# Handoff 0106 - Agent-Process Hardening Production Refactor To QA/Tooling

## Current State

Task 0145 productionizes the prior agent-process hardening pass for managed-hook
portability. The installer now supports temp `--target-dir` validation, installs
support modules next to the managed hook, and validates the copied hook without
repo `PYTHONPATH`. The QA hardening pass fixed import precedence so installed
sibling support modules outrank any ambient fallback `scripts/` directory,
changed scaffold audit dry-runs to temp `--target-dir` paths, persisted standing
user authorization for project-local read-only subagent use, and kept the work
Tier 2 and repo-local.

## Files To Review

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
- `docs/instruction-surface-map.md`
- `docs/index.md`
- `knowledge-base/source-index.md`
- `knowledge-base/source-ledger/2026-06-02-agent-process-hardening-production-refactor.md`
- `.agents/TASK_LOG/0145-agent-process-hardening-production-refactor.md`

## QA And Tooling Focus

- Confirm temp-target install, validate, and removal never touch `/etc/codex`.
- Confirm installed `esp32_admin_policy.py` runs from the temp hook directory
  with sanitized `PYTHONPATH` and no repo import path dependency.
- Confirm validate fails for missing, stale, or wrong-mode support modules.
- Confirm `bypassPermissions` remains advisory-only.
- Confirm structured classifier fields do not break existing wrappers.
- Confirm dry-run/install/validate/remove reports include SHA-256, mode, owner,
  diffs, backups, hook, requirements, and support modules.
- Confirm every-prompt hook text includes safe non-trivial Tier 1 and Tier 2/
  Tier 3 subagent-attempt guidance plus standing user authorization.

## Still Open

Runtime hook trust and future subagent lifecycle visibility cannot be proven by
static repo files. System `/etc/codex` state was intentionally not inspected or
mutated.

## Validation

Final validation results are recorded in
[Task 0145](../TASK_LOG/0145-agent-process-hardening-production-refactor.md).

## Closed Surfaces

No live hardware, COM/serial, flash, monitor, serial write, RF/XBee write,
relay/load/mains, firmware behavior change, `/etc/codex` mutation,
admin-strict install, destructive git, GitHub publication, release, commit,
push, PR, deploy, or external service mutation is authorized by this handoff.
