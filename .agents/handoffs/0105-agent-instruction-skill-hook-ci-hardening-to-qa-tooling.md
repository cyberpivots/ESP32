# Handoff 0105 - Agent Instruction, Skill, Hook, CI Hardening To QA/Tooling

## Current State

Task 0144 implemented repo-local hardening for instruction surfaces, shared hook
classifiers, skill routing, scaffold audits, durable records, CI validation,
and Git publication hygiene. The work stays inside the Tier 2 repo-local
boundary and does not authorize live hardware, `/etc/codex`, destructive git,
commit, push, PR, release, or Pages deployment.

## Files To Review

- `scripts/agent_process_classifiers.py`
- `.codex/hooks/pre_tool_use_agent_process.py`
- `.codex/hooks/user_prompt_submit_agent_process.py`
- `.codex/hooks/subagent_start_agent_process.py`
- `.codex/hooks/subagent_stop_agent_process.py`
- `.codex/admin/hooks/esp32_admin_policy.py`
- `.codex/agents/*.toml`
- `.codex/config.toml`
- `scripts/scaffold_audit_agent_process.py`
- `scripts/scaffold_audit_skills.py`
- `scripts/scaffold_audit_records.py`
- `scripts/git_publication_hygiene.py`
- `scripts/verify_scaffold.py`
- `tests/scaffold_audits/test_agent_process_classifiers.py`
- `tests/scaffold_audits/test_agent_process_hooks.py`
- `tests/scaffold_audits/test_admin_policy_hooks.py`
- `.github/workflows/scaffold-ci.yml`
- `.github/workflows/pages.yml`
- `.github/workflows/README.md`
- `docs/instruction-surface-map.md`
- `docs/agent-coordination.md`
- `docs/github-pages-public-site.md`
- `.agents/GOVERNANCE.md`
- `research/skills/available-skills.md`
- `knowledge-base/source-index.md`
- `knowledge-base/source-ledger/2026-06-02-agent-instruction-skill-hook-ci-hardening.md`
- `.agents/TASK_LOG/0144-agent-instruction-skill-hook-ci-hardening.md`

## QA Focus

- Confirm local and managed hooks both import the shared classifier and preserve
  `bypassPermissions` advisory-only behavior.
- Confirm read-only command chains do not produce noisy mutation warnings.
- Confirm Tier 3, `/etc/codex`, redirection/`tee`, destructive git, external
  publication, and serial/RF/relay/load/mains commands still classify as
  closed or mutating surfaces.
- Confirm `validation performed` alone does not trigger Stop-footer mutation
  enforcement.
- Confirm `xbee-radio-integration` is enabled and plugin cache paths are marked
  drift-prone.
- Confirm non-deploy PR CI does not upload or deploy Pages artifacts.
- Confirm no commit, push, PR, branch deletion, release, or deploy action was
  run or authorized.

## Still Open

Runtime hook trust, future subagent availability, and future lifecycle state
visibility cannot be proven by static repo files. Future Tier 2/Tier 3 tasks
must still attempt subagents when available and close reviewer agents after
capturing output.

## Validation

Final validation results are recorded in
[Task 0144](../TASK_LOG/0144-agent-instruction-skill-hook-ci-hardening.md).
